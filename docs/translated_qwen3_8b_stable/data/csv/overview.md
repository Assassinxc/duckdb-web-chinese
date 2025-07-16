---
---
layout: docu
redirect_from:
- /docs/data/csv
- /docs/data/csv/
- /docs/data/csv/overview
title: CSV 导入
---

## 示例

以下示例使用 [`flights.csv`](/data/flights.csv) 文件。

从磁盘读取 CSV 文件，自动推断选项：

```sql
SELECT * FROM 'flights.csv';
```

使用 `read_csv` 函数并使用自定义选项：

```sql
SELECT *
FROM read_csv('flights.csv',
    delim = '|',
    header = true,
    columns = {
        'FlightDate': 'DATE',
        'UniqueCarrier': 'VARCHAR',
        'OriginCityName': 'VARCHAR',
        'DestCityName': 'VARCHAR'
    });
```

从标准输入读取 CSV 文件，自动推断选项：

```bash
cat flights.csv | duckdb -c "SELECT * FROM read_csv('/dev/stdin')"
```

将 CSV 文件读入表中：

```sql
CREATE TABLE ontime (
    FlightDate DATE,
    UniqueCarrier VARCHAR,
    OriginCityName VARCHAR,
    DestCityName VARCHAR
);
COPY ontime FROM 'flights.csv';
```

或者，可以使用 [`CREATE TABLE .. AS SELECT` 语句]({% link docs/stable/sql/statements/create_table.md %}#create-table--as-select-ctas) 不手动指定模式来创建表：

```sql
CREATE TABLE ontime AS
    SELECT * FROM 'flights.csv';
```

我们可以使用 [`FROM`-first 语法]({% link docs/stable/sql/query_syntax/from.md %}#from-first-syntax) 来省略 `SELECT *`。

```sql
CREATE TABLE ontime AS
    FROM 'flights.csv';
```

## CSV 加载

CSV 加载，即导入 CSV 文件到数据库，是一个非常常见，但令人惊讶地具有挑战性的任务。虽然 CSV 文件表面上看起来简单，但在 CSV 文件中却存在大量的不一致性，这使得加载它们成为一个挑战。CSV 文件种类繁多，经常损坏，而且没有模式。CSV 读取器需要处理所有这些不同的情况。

DuckDB 的 CSV 读取器可以通过使用 [CSV 识别器]({% post_url 2023-10-27-csv-sniffer %}) 来分析 CSV 文件，自动推断应使用的配置标志。这在大多数情况下都能正常工作，应作为首选选项。在极少数情况下，CSV 读取器无法确定正确的配置时，可以手动配置 CSV 读取器以正确解析 CSV 文件。有关更多信息，请参阅 [自动检测页面]({% link docs/stable/data/csv/auto_detection.md %}).

## 参数

以下是可传递给 [`read_csv` 函数](#csv-functions) 的参数。在适用的情况下，这些参数也可以传递给 [`COPY` 语句]({% link docs/stable/sql/statements/copy.md %}#copy-to).

| 名称 | 描述 | 类型 | 默认 |
|:--|:-----|:-|:-|
| `all_varchar` | 跳过类型检测并假设所有列都是 `VARCHAR` 类型。此选项仅支持 `read_csv` 函数。 | `BOOL` | `false` |
| `allow_quoted_nulls` | 允许将带引号的值转换为 `NULL` 值 | `BOOL` | `true` |
| `auto_detect` | [自动检测 CSV 参数]({% link docs/stable/data/csv/auto_detection.md %})。 | `BOOL` | `true` |
| `auto_type_candidates` | 识别器在检测列类型时使用的类型。`VARCHAR` 类型始终作为后备选项包含在内。请参阅 [示例](#auto_type_candidates-details)。 | `TYPE[]` | [默认类型](#auto_type_candidates-details) |
| `buffer_size` | 用于读取文件的缓冲区大小，以字节为单位。必须足够大以容纳四行，并且会显著影响性能。 | `BIGINT` | `16 * max_line_size` |
| `columns` | 列名和类型，作为结构（例如 `{'col1': 'INTEGER', 'col2': 'VARCHAR'}`）。使用此选项会禁用自动检测。 | `STRUCT` | (empty) |
| `comment` | 用于开始注释的字符。以注释字符（可选地前面有空格字符）开头的行将被完全忽略；其他包含注释字符的行将仅解析到该点。 | `VARCHAR` | (empty) |
| `compression` | 用于压缩 CSV 文件的方法。默认情况下，这会从文件扩展名中自动检测（例如，`t.csv.gz` 会使用 gzip，`t.csv` 会使用 `none`）。选项包括 `none`、`gzip`、`zstd`。 | `VARCHAR` | `auto` |
| `dateformat` | [日期格式]({% link docs/stable/sql/functions/dateformat.md %})，用于解析和写入日期。 | `VARCHAR` | (empty) |
| `date_format` | `dateformat` 的别名；仅在 `COPY` 语句中可用。 | `VARCHAR` | (empty) |
| `decimal_separator` | 数字的十进制分隔符。 | `VARCHAR` | `.` |
| `delim` | 用于分隔每行内列的分隔符字符，例如 `,` `;` `\t`。分隔符字符可以多达 4 字节，例如 🦆。`sep` 的别名。 | `VARCHAR` | `,` |
| `delimiter` | `delim` 的别名；仅在 `COPY` 语句中可用。 | `VARCHAR` | `,` |
| `escape` | 用于转义 `quote` 字符的字符串。 | `VARCHAR` | `"` |
| `encoding` | CSV 文件使用的编码。选项包括 `utf-8`、`utf-16`、`latin-1`。`COPY` 语句中不可用（始终使用 `utf-8`）。 | `VARCHAR` | `utf-8` |
| `filename` | 将包含文件的路径添加到每一行，作为名为 `filename` 的字符串列。返回的路径是根据传递给 `read_csv` 的路径或通配符模式确定的，而不是仅仅根据文件名。自 DuckDB v1.3.0 起，`filename` 列会自动作为虚拟列添加，此选项仅出于兼容性原因保留。 | `BOOL` | `false` |
| `force_not_null` | 不将指定列中的值与 `NULL` 字符串匹配。在默认情况下（`NULL` 字符串为空），这意味着空值将被读取为零长度字符串而不是 `NULL`。 | `VARCHAR[]` | `[]` |
| `header` | 每个文件的第一行包含列名。 | `BOOL` | `false` |
| `hive_partitioning` | 将路径解释为 [Hive 分区路径]({% link docs/stable/data/partitioning/hive_partitioning.md %})。 | `BOOL` | (auto-detected) |
| `ignore_errors` | 忽略遇到的任何解析错误。 | `BOOL` | `false` |
| `max_line_size` 或 `maximum_line_size`。`COPY` 语句中不可用。 | 最大行大小，以字节为单位。 | `BIGINT` | 2000000 |
| `names` 或 `column_names` | 列名，作为列表。请参阅 [示例]({% link docs/stable/data/csv/tips.md %}#provide-names-if-the-file-does-not-contain-a-header)。 | `VARCHAR[]` | (empty) |
| `new_line` | 新行字符。选项包括 `'\r'`、`'\n'` 或 `'\r\n'`。CSV 解析器仅区分单字符和双字符行分隔符。因此，它不会区分 `'\r'` 和 `'\n'`。| `VARCHAR` | (empty) |
| `normalize_names` | 规范化列名。这将从列名中删除任何非字母数字字符。保留的 SQL 关键字列名前面会加上下划线字符 (`_`)。 | `BOOL` | `false` |
| `null_padding` | 当一行缺少列时，将右侧的剩余列填充为 `NULL` 值。 | `BOOL` | `false` |
| `nullstr` 或 `null` | 表示 `NULL` 值的字符串。 | `VARCHAR` 或 `VARCHAR[]` | (empty) |
| `parallel` | 使用并行 CSV 读取器。 | `BOOL` | `true` |
| `quote` | 用于引用值的字符串。 | `VARCHAR` | `"` |
| `rejects_scan` | [临时表名称，用于存储故障扫描信息]({% link docs/stable/data/csv/reading_faulty_csv_files.md %}#reject-scans)。 | `VARCHAR` | `reject_scans` |
| `rejects_table` | [临时表名称，用于存储故障行信息]({% link docs/stable/data/csv/reading_faulty_csv_files.md %}#reject-errors)。 | `VARCHAR` | `reject_errors` |
| `rejects_limit` | 每个文件中记录在 rejects 表中的故障行数上限。将此设置为 `0` 表示不限制。 | `BIGINT` | `0` |
| `sample_size` | [自动检测参数]({% link docs/stable/data/csv/auto_detection.md %}) 的样本行数。 | `BIGINT` | 20480 |
| `sep` | 用于分隔每行内列的分隔符字符，例如 `,` `;` `\t`。分隔符字符可以多达 4 字节，例如 🦆。`delim` 的别名。 | `VARCHAR` | `,` |
| `skip` | 每个文件开始时要跳过的行数。 | `BIGINT` | 0 |
| `store_rejects` | 跳过任何有错误的行并将它们存储在 rejects 表中。 | `BOOL` | `false` |
| `strict_mode` | 强制 CSV 读取器的严格级别。当设置为 `true` 时，解析器在遇到任何问题时会抛出错误。当设置为 `false` 时，解析器会尝试读取结构错误的文件。需要注意的是，读取结构错误的文件可能会导致歧义；因此，应谨慎使用此选项。 | `BOOL` | `true` |
| `thousands` | 用于识别数值中的千位分隔符的字符。它必须是一个单字符，并且与 `decimal_separator` 选项不同。| `VARCHAR` | (empty) |
| `timestampformat` | [时间戳格式]({% link docs/stable/sql/functions/dateformat.md %})，用于解析和写入时间戳。 | `VARCHAR` | (empty) |
| `timestamp_format` | `timestampformat` 的别名；仅在 `COPY` 语句中可用。 | `VARCHAR` | (empty) |
| `types` 或 `dtypes` 或 `column_types` | 列类型，可以是列表（按位置）或结构（按名称）。请参阅 [示例]({% link docs/stable/data/csv/tips.md %}#override-the-types-of-specific-columns)。 | `VARCHAR[]` 或 `STRUCT` | (empty) |
| `union_by_name` | 通过列名而不是位置从不同文件对齐列。使用此选项会增加内存使用量。 | `BOOL` | `false` |

> 提示 DuckDB 的 CSV 读取器支持 UTF-8（默认）、UTF-16 和 Latin-1 编码（请参阅 `encoding` 选项）。
> 为了转换不同编码的文件，我们建议使用 [`iconv` 命令行工具](https://linux.die.net/man/1/iconv)。
>
> ```bash
> iconv -f ISO-8859-2 -t UTF-8 input.csv > input-utf-8.csv
> ```

### `auto_type_candidates` 详细信息

`auto_type_candidates` 选项允许您指定 CSV 读取器在 [列数据类型检测]({% link docs/stable/data/csv/auto_detection.md %}#type-detection) 时应考虑的数据类型。
使用示例：

```sql
SELECT * FROM read_csv('csv_file.csv', auto_type_candidates = ['BIGINT', 'DATE']);
```

`auto_type_candidates` 选项的默认值为 `['SQLNULL', 'BOOLEAN', 'BIGINT', 'DOUBLE', 'TIME', 'DATE', 'TIMESTAMP', 'VARCHAR']`。

## CSV 函数

`read_csv` 会自动尝试使用 [CSV 识别器]({% post_url 2023-10-27-csv-sniffer %}) 确定 CSV 读取器的正确配置。它还会自动推断列的类型。如果 CSV 文件有标题，它将使用标题中找到的名称来命名列。否则，列将被命名为 `column0, column1, column2, ...`。使用 [`flights.csv`](/data/flights.csv) 文件的一个示例：

```sql
SELECT * FROM read_csv('flights.csv');
```

| FlightDate | UniqueCarrier | OriginCityName |  DestCityName   |
|------------|---------------|----------------|-----------------|
| 1988-01-01 | AA            | New York, NY   | Los Angeles, CA |
| 1988-01-02 | AA            | New York, NY   | Los Angeles, CA |
| 1988-01-03 | AA            | New York, NY   | Los Angeles, CA |

路径可以是相对路径（相对于当前工作目录）或绝对路径。

我们也可以使用 `read_csv` 创建一个持久表：

```sql
CREATE TABLE ontime AS
    SELECT * FROM read_csv('flights.csv');
DESCRIBE ontime;
```

|  column_name   | column_type | null | key  | default | extra |
|----------------|-------------|------|------|---------|-------|
| FlightDate     | DATE        | YES  | NULL | NULL    | NULL  |
| UniqueCarrier  | VARCHAR     | YES  | NULL | NULL    | NULL  |
| OriginCityName | VARCHAR     | YES  | NULL | NULL    | NULL  |
| DestCityName   | VARCHAR     | YES  | NULL | NULL    | NULL  |

```sql
SELECT * FROM read_csv('flights.csv', sample_size = 20_000);
```

如果我们明确设置 `delim` / `sep`、`quote`、`escape` 或 `header`，我们可以绕过此特定参数的自动检测：

```sql
SELECT * FROM read_csv('flights.csv', header = true);
```

通过提供一个通配符或文件列表，可以一次读取多个文件。有关更多信息，请参阅 [多个文件部分]({% link docs/stable/data/multiple_files/overview.md %}).

## 使用 `COPY` 语句写入

[`COPY` 语句]({% link docs/stable/sql/statements/copy.md %}#copy-to) 可用于将数据从 CSV 文件加载到表中。此语句的语法与 PostgreSQL 中使用的相同。为了使用 `COPY` 语句加载数据，我们首先必须创建具有正确模式的表（这与 CSV 文件中的列顺序和数据类型相匹配）。`COPY` 会自动检测 CSV 的配置选项。

```sql
CREATE TABLE ontime (
    flightdate DATE,
    uniquecarrier VARCHAR,
    origincityname VARCHAR,
    destcityname VARCHAR
);
COPY ontime FROM 'flights.csv';
SELECT * FROM ontime;
```

| flightdate | uniquecarrier | origincityname |  destcityname   |
|------------|---------------|----------------|-----------------|
| 1988-01-01 | AA            | New York, NY   | Los Angeles, CA |
| 1988-01-02 | AA            | New York, NY   | Los Angeles, CA |
| 1988-01-03 | AA            | New York, NY   | Los Angeles, CA |

如果我们想手动指定 CSV 格式，可以使用 `COPY` 的配置选项。

```sql
CREATE TABLE ontime (flightdate DATE, uniquecarrier VARCHAR, origincityname VARCHAR, destcityname VARCHAR);
COPY ontime FROM 'flights.csv' (DELIMITER '|', HEADER);
SELECT * FROM ontime;
```

## 读取损坏的 CSV 文件

DuckDB 支持读取损坏的 CSV 文件。详细信息，请参阅 [读取损坏的 CSV 文件页面]({% link docs/stable/data/csv/reading_faulty_csv_files.md %}).

## 顺序保持

CSV 读取器尊重 `preserve_insertion_order` [配置选项]({% link docs/stable/configuration/overview.md %}) 来 [保持插入顺序]({% link docs/stable/sql/dialect/order_preservation.md %}).
当 `true`（默认值）时，CSV 读取器返回的结果集中行的顺序与从文件（或文件）中读取的对应行的顺序相同。
当 `false` 时，无法保证顺序会保持。

## 写入 CSV 文件

DuckDB 可以使用 [`COPY ... TO` 语句]({% link docs/stable/sql/statements/copy.md %}#copy--to) 写入 CSV 文件。