---
layout: docu
railroad: statements/copy.js
redirect_from:
- /docs/sql/statements/copy
title: COPY 语句
---

## 示例

将 CSV 文件读入 `lineitem` 表，使用自动检测的 CSV 选项：

```sql
COPY lineitem FROM 'lineitem.csv';
```

将 CSV 文件读入 `lineitem` 表，使用手动指定的 CSV 选项：

```sql
COPY lineitem FROM 'lineitem.csv' (DELIMITER '|');
```

将 Parquet 文件读入 `lineitem` 表：

```sql
COPY lineitem FROM 'lineitem.pq' (FORMAT parquet);
```

将 JSON 文件读入 `lineitem` 表，使用自动检测的选项：

```sql
COPY lineitem FROM 'lineitem.json' (FORMAT json, AUTO_DETECT true);
```

将 CSV 文件读入 `lineitem` 表，使用双引号：

```sql
COPY lineitem FROM "lineitem.csv";
```

将 CSV 文件读入 `lineitem` 表，省略引号：

```sql
COPY lineitem FROM lineitem.csv;
```

将表写入 CSV 文件：

```sql
COPY lineitem TO 'lineitem.csv' (FORMAT csv, DELIMITER '|', HEADER);
```

将表写入 CSV 文件，使用双引号：

```sql
COPY lineitem TO "lineitem.csv";
```

将表写入 CSV 文件，省略引号：

```sql
COPY lineitem TO lineitem.csv;
```

将查询结果写入 Parquet 文件：

```sql
COPY (SELECT l_orderkey, l_partkey FROM lineitem) TO 'lineitem.parquet' (COMPRESSION zstd);
```

将数据库 `db1` 的全部内容复制到数据库 `db2`：

```sql
COPY FROM DATABASE db1 TO db2;
```

仅复制模式（目录元素），但不复制任何数据：

```sql
COPY FROM DATABASE db1 TO db2 (SCHEMA);
```

## 概述

`COPY` 在 DuckDB 和外部文件之间移动数据。`COPY ... FROM` 从外部文件导入数据到 DuckDB。`COPY ... TO` 将数据从 DuckDB 写入外部文件。`COPY` 命令可用于 `CSV`、`PARQUET` 和 `JSON` 文件。

## `COPY ... FROM`

`COPY ... FROM` 从外部文件导入数据到现有表中。数据会附加到表中已有的数据。文件中的列数必须与表 `table_name` 中的列数匹配，并且列的内容必须可以转换为表的列类型。如果无法实现这一点，则会抛出错误。

如果指定了列列表，`COPY` 仅会复制文件中指定列的数据。如果表中存在不在列列表中的列，`COPY ... FROM` 会为这些列插入默认值。

将逗号分隔的文件 `test.csv`（无标题）的内容复制到表 `test` 中：

```sql
COPY test FROM 'test.csv';
```

将带有标题的逗号分隔文件 `categories.csv` 的内容复制到 `category` 表中：

```sql
COPY category FROM 'categories.csv' (HEADER);
```

将 `lineitem.tbl` 的内容复制到 `lineitem` 表中，其中内容由竖线字符 (`|`) 分隔：

```sql
COPY lineitem FROM 'lineitem.tbl' (DELIMITER '|');
```

将 `lineitem.tbl` 的内容复制到 `lineitem` 表中，其中分隔符、引号字符和标题的存在由自动检测确定：

```sql
COPY lineitem FROM 'lineitem.tbl' (AUTO_DETECT true);
```

将逗号分隔文件 `names.csv` 的内容读入 `category` 表的 `name` 列。表中的其他列将填充其默认值：

```sql
COPY category(name) FROM 'names.csv';
```

将 Parquet 文件 `lineitem.parquet` 的内容读入 `lineitem` 表：

```sql
COPY lineitem FROM 'lineitem.parquet' (FORMAT parquet);
```

将换行符分隔的 JSON 文件 `lineitem.ndjson` 的内容读入 `lineitem` 表：

```sql
COPY lineitem FROM 'lineitem.ndjson' (FORMAT json);
```

将 JSON 文件 `lineitem.json` 的内容读入 `lineitem` 表：

```sql
COPY lineitem FROM 'lineitem.json' (FORMAT json, ARRAY true);
```

### 语法

<div id="rrdiagram1"></div>

> 为了与 PostgreSQL 兼容，DuckDB 接受一些不完全符合此处所示铁路图的 `COPY ... FROM` 语句。例如，以下是一个有效的语句：
>
> ```sql
> COPY tbl FROM 'tbl.csv' WITH DELIMITER '|' CSV HEADER;
> ```

## `COPY ... TO`

`COPY ... TO` 将数据从 DuckDB 导出到外部 CSV 或 Parquet 文件。它拥有与 `COPY ... FROM` 几乎相同的选项集，但在 `COPY ... TO` 的情况下，这些选项指定如何将文件写入磁盘。任何由 `COPY ... TO` 创建的文件都可以通过使用类似的选项集的 `COPY ... FROM` 语句复制回数据库中。

`COPY ... TO` 函数可以指定一个表名或一个查询。当指定表名时，整个表的内容将被写入结果文件。当指定查询时，将执行查询并将查询结果写入结果文件。

将 `lineitem` 表的内容复制到带有标题的 CSV 文件中：

```sql
COPY lineitem TO 'lineitem.csv';
```

将 `lineitem` 表的内容复制到文件 `lineitem.tbl` 中，其中列由竖线字符 (`|`) 分隔，包括标题行：

```sql
COPY lineitem TO 'lineitem.tbl' (DELIMITER '|');
```

使用制表符分隔符创建一个无标题的 TSV 文件：

```sql
COPY lineitem TO 'lineitem.tsv' (DELIMITER '\t', HEADER false);
```

将 `lineitem` 表的 `l_orderkey` 列复制到文件 `orderkey.tbl` 中：

```sql
COPY lineitem(l_orderkey) TO 'orderkey.tbl' (DELIMITER '|');
```

将查询结果复制到文件 `query.csv` 中，包括带有列名的标题：

```sql
COPY (SELECT 42 AS a, 'hello' AS b) TO 'query.csv' (DELIMITER ',');
```

将查询结果复制到 Parquet 文件 `query.parquet` 中：

```sql
COPY (SELECT 42 AS a, 'hello' AS b) TO 'query.parquet' (FORMAT parquet);
```

将查询结果复制到换行符分隔的 JSON 文件 `query.ndjson` 中：

```sql
COPY (SELECT 42 AS a, 'hello' AS b) TO 'query.ndjson' (FORMAT json);
```

将查询结果复制到 JSON 文件 `query.json` 中：

```sql
COPY (SELECT 42 AS a, 'hello' AS b) TO 'query.json' (FORMAT json, ARRAY true);
```

返回作为 `COPY` 语句的一部分写入的文件及其列统计信息：

```sql
COPY (SELECT l_orderkey, l_comment FROM lineitem) TO 'lineitem_part.parquet' (RETURN_STATS);
```

|       filename        | count  | file_size_bytes | footer_size_bytes |                                                                                   column_statistics                                                                                    | partition_keys |
|-----------------------|-------:|----------------:|------------------:|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|
| lineitem_part.parquet | 600572 | 8579141         | 1445              | {'"l_comment"'={column_size_bytes=7642227, max=zzle. slyly, min=' Tiresias above the blit', null_count=0}, '"l_orderkey"'={column_size_bytes=935457, max=600000, min=1, null_count=0}} | NULL           |

注意：对于嵌套列（例如 struct），列统计信息是按每个部分定义的。例如，如果我们有一个列 `name STRUCT(field1 INTEGER, field2 INTEGER)`，则列统计信息将包含 `name.field1` 和 `name.field2` 的统计信息。

### `COPY ... TO` 选项

可以提供零个或多个复制选项作为复制操作的一部分。`WITH` 指定符是可选的，但如果指定了任何选项，必须使用括号。参数值可以带单引号或不带单引号传递。

任何布尔类型的选项都可以以多种方式启用或禁用。您可以写 `true`、`ON` 或 `1` 来启用选项，写 `false`、`OFF` 或 `0` 来禁用选项。`BOOLEAN` 值也可以省略，例如，仅传递 `(HEADER)`，则默认为 `true`。

除少数例外情况外，以下选项适用于使用 `COPY` 写入的所有格式。

| 名称 | 描述 | 类型 | 默认 |
|:--|:-----|:-|:-|
| `FORMAT` | 指定要使用的复制函数。默认值将根据文件扩展名选择（例如，`.parquet` 会生成 Parquet 文件）。如果文件扩展名未知，则选择 `CSV`。Vanilla DuckDB 提供 `CSV`、`PARQUET` 和 `JSON`，但可以通过 [`extensions`]({% link docs/stable/core_extensions/overview.md %}) 添加额外的复制函数。 | `VARCHAR` | `auto` |
| `USE_TMP_FILE` | 如果原始文件存在，是否首先写入临时文件（`target.csv.tmp`）。这可以防止在写入过程中取消时覆盖现有文件。 | `BOOL` | `auto` |
| `OVERWRITE_OR_IGNORE` | 是否允许覆盖已存在的文件。仅在与 `PARTITION_BY` 一起使用时才生效。 | `BOOL` | `false` |
| `OVERWRITE` | 当 `true` 时，所有目标目录中的现有文件将被删除（不支持远程文件系统）。仅在与 `PARTITION_BY` 一起使用时才生效。 | `BOOL` | `false` |
| `APPEND` | 当 `true` 时，如果生成的文件名模式已经存在，路径将被重新生成以确保不覆盖现有文件。仅在与 `PARTITION_BY` 一起使用时才生效。 | `BOOL` | `false` |
| `FILENAME_PATTERN` | 设置用于文件名的模式，可以包含 `{uuid}` / `{uuidv4}` 或 `{uuidv7}` 来填充生成的 [UUID]({% link docs/stable/sql/data_types/numeric.md %}#universally-unique-identifiers-uuids)（v4 或 v7），以及 `{i}`，它被替换为递增的索引。仅在与 `PARTITION_BY` 一起使用时才生效。 | `VARCHAR` | `auto` |
| `FILE_EXTENSION` | 设置应分配给生成文件的文件扩展名。 | `VARCHAR` | `auto` |
| `PER_THREAD_OUTPUT` | 当 `true` 时，`COPY` 命令为每个线程生成一个文件，而不是总共生成一个文件。这允许更快的并行写入。 | `BOOL` | `false` |
| `FILE_SIZE_BYTES` | 如果设置了此参数，`COPY` 过程会创建一个包含导出文件的目录。如果文件超过设置的限制（以字节如 `1000` 或人类可读格式如 `1k` 指定），过程会在目录中创建新文件。此参数与 `PER_THREAD_OUTPUT` 配合使用。请注意，大小是作为近似值使用的，文件偶尔可能略微超过限制。 | `VARCHAR` 或 `BIGINT` | (empty) |
| `PARTITION_BY` | 使用 Hive 分区方案进行分区的列。有关分区写入的更多信息，请参阅 [分区写入部分]({% link docs/stable/data/partitioning/partitioned_writes.md %})。 | `VARCHAR[]` | (empty) |
| `PRESERVE_ORDER` | 在复制操作期间是否 [保留顺序]({% link docs/stable/sql/dialect/order_preservation.md %})。默认值为 `preserve_insertion_order` [配置选项]({% link docs/stable/configuration/overview.md %}) 的值。 | `BOOL`| (*) |
| `RETURN_FILES` | 是否在查询结果中包含创建的文件路径（作为 `files VARCHAR[]` 列）。 | `BOOL` | `false` |
| `RETURN_STATS` | 是否返回作为 `COPY` 语句的一部分写入的文件及其列统计信息。 | `BOOL`| `false` |
| `WRITE_PARTITION_COLUMNS` | 是否将分区列写入文件。仅在与 `PARTITION_BY` 一起使用时才生效。 | `BOOL` | `false` |

### 语法

<div id="rrdiagram2"></div>

> 为了与 PostgreSQL 兼容，DuckDB 接受一些不完全符合此处所示铁路图的 `COPY ... TO` 语句。例如，以下是一个有效的语句：
>
> ```sql
> COPY (SELECT 42 AS x, 84 AS y) TO 'out.csv' WITH DELIMITER '|' CSV HEADER;
> ```

## `COPY FROM DATABASE ... TO`

`COPY FROM DATABASE ... TO` 语句将一个附加数据库的全部内容复制到另一个附加数据库。这包括模式（包括约束、索引、序列、宏和数据本身）。

```sql
ATTACH 'db1.db' AS db1;
CREATE TABLE db1.tbl AS SELECT 42 AS x, 3 AS y;
CREATE MACRO db1.two_x_plus_y(x, y) AS 2 * x + y;

ATTACH 'db2.db' AS db2;
COPY FROM DATABASE db1 TO db2;
SELECT db2.two_x_plus, y) AS z FROM db2.tbl;
```

| z  |
|---:|
| 87 |

要仅复制 `db1` 的 **模式** 到 `db2`，但不复制数据，请在语句中添加 `SCHEMA`：

```sql
COPY FROM DATABASE db1 TO db2 (SCHEMA);
```

### 语法

<div id="rrdiagram3"></div>

## 格式特定选项

### CSV 选项

以下选项适用于写入 CSV 文件。

| 名称 | 描述 | 类型 | 默认 |
|:--|:-----|:-|:-|
| `COMPRESSION` | 文件的压缩类型。默认情况下，将根据文件扩展名自动检测（例如，`file.csv.gz` 将使用 `gzip`，`file.csv.zst` 将使用 `zstd`，`file.csv` 将使用 `none`）。选项包括 `none`、`gzip`、`zstd`。 | `VARCHAR` | `auto` |
| `DATEFORMAT` | 指定写入日期时使用的日期格式。参见 [日期格式]({% link docs/stable/sql/functions/dateformat.md %})。 | `VARCHAR` | (empty) |
| `DELIM` 或 `SEP` | 在每行中分隔列的字符。 | `VARCHAR` | `,` |
| `ESCAPE` | 在匹配 `quote` 值的字符前应出现的字符。 | `VARCHAR` | `"` |
| `FORCE_QUOTE` | 始终添加引号的列列表，即使不需要。 | `VARCHAR[]` | `[]` |
| `HEADER` | 是否为 CSV 文件写入标题。 | `BOOL` | `true` |
| `NULLSTR` | 表示 `NULL` 值的字符串。 | `VARCHAR` | (empty) |
| `PREFIX` | 以指定字符串前缀 CSV 文件。此选项必须与 `SUFFIX` 一起使用，并且需要将 `HEADER` 设置为 `false`。| `VARCHAR` | (empty) |
| `SUFFIX` | 在 CSV 文件末尾添加指定字符串作为后缀。此选项必须与 `PREFIX` 一起使用，并且需要将 `HEADER` 设置为 `false`。| `VARCHAR` | (empty) |
| `QUOTE` | 在数据值被引用时使用的引号字符。 | `VARCHAR` | `"` |
| `TIMESTAMPFORMAT` | 指定写入时间戳时使用的日期格式。参见 [日期格式]({% link docs/stable/sql/functions/dateformat.md %})。 | `VARCHAR` | (empty) |

### Parquet 选项

以下选项适用于写入 Parquet 文件。

| 名称 | 描述 | 类型 | 默认 |
|:--|:-----|:-|:-|
| `COMPRESSION` | 要使用的压缩格式（`uncompressed`、`snappy`、`gzip`、`zstd`、`brotli`、`lz4`、`lz4_raw`）。 | `VARCHAR` | `snappy` |
| `COMPRESSION_LEVEL` | 压缩级别，设置在 1（最低压缩，最快）和 22（最高压缩，最慢）之间。仅支持 zstd 压缩。 | `BIGINT` | `3` |
| `FIELD_IDS` | 每个列的 `field_id`。传递 `auto` 以尝试自动推断。 | `STRUCT` | (empty) |
| `ROW_GROUP_SIZE_BYTES` | 每个行组的目标大小。您可以传递一个可读字符串（如 `2MB`）或一个整数（即字节数）。此选项仅在您已发出 `SET preserve_insertion_order = false;` 时使用，否则被忽略。 | `BIGINT` | `row_group_size * 1024` |
| `ROW_GROUP_SIZE` | 每个行组的目标大小，即行数。 | `BIGINT` | 122880 |
| `ROW_GROUPS_PER_FILE` | 如果当前文件已有指定数量的行组，则创建一个新的 Parquet 文件。如果多个线程处于活动状态，文件中的行组数可能略微超过指定数量，以限制锁定量——类似于 `FILE_SIZE_BYTES` 的行为。但如果 `per_thread_output` 已设置，每个文件仅由一个线程写入，结果将再次准确。 | `BIGINT` |  (empty) |
| `PARQUET_VERSION` | 要使用的 parquet 版本（`V1`、`V2`）。 | `VARCHAR` | `V1` |

一些 `FIELD_IDS` 示例如下。

自动分配 `field_ids`：

```sql
COPY
    (SELECT 128 AS i)
    TO 'my.parquet'
    (FIELD_IDS 'auto');
```

设置列 `i` 的 `field_id` 为 42：

```sql
COPY
    (SELECT 128 AS i)
    TO 'my.parquet'
    (FIELD_IDS {i: 42});
```

设置列 `i` 的 `field_id` 为 42，列 `j` 的 `field_id` 为 43：

```sql
COPY
    (SELECT 128 AS i, 256 AS j)
    TO 'my.parquet'
    (FIELD_IDS {i: 42, j: 43});
```

设置列 `my_struct` 的 `field_id` 为 43，列 `i`（嵌套在 `my_struct` 中）的 `field_id` 为 43：

```sql
COPY
    (SELECT {i: 128} AS my_struct)
    TO 'my.parquet'
    (FIELD_IDS {my_struct: {__duckdb_field_id: 42, i: 43}});
```

设置列 `my_list` 的 `field_id` 为 42，列 `element`（列表子项的默认名称）的 `field_id` 为 43：

```sql
COPY
    (SELECT [128, 256] AS my_list)
    TO 'my.parquet'
    (FIELD_IDS {my_list: {__duckdb_field_id: 42, element: 43}});
```

设置列 `my_map` 的 `field_id` 为 42，列 `key` 和 `value`（映射子项的默认名称）的 `field_id` 为 43 和 44：

```sql
COPY
    (SELECT MAP {'key1' : 128, 'key2': 256} my_map)
    TO 'my.parquet'
    (FIELD_IDS {my_map: {__duckdb_field_id: 42, key: 43, value: 44}});
```

### JSON 选项

以下选项适用于写入 `JSON` 文件。

| 名称 | 描述 | 类型 | 默认 |
|:--|:-----|:-|:-|
| `ARRAY` | 是否写入 JSON 数组。如果 `true`，写入记录的 JSON 数组；如果 `false`，写入换行符分隔的 JSON。 | `BOOL` | `false` |
| `COMPRESSION` | 文件的压缩类型。默认情况下，将根据文件扩展名自动检测（例如，`file.json.gz` 将使用 `gzip`，`file.json.zst` 将使用 `zstd`，`file.json` 将使用 `none`）。选项包括 `none`、`gzip`、`zstd`。 | `VARCHAR` | `auto` |
| `DATEFORMAT` | 指定写入日期时使用的日期格式。参见 [日期格式]({% link docs/stable/sql/functions/dateformat.md %})。 | `VARCHAR` | (empty) |
| `TIMESTAMPFORMAT` | 指定写入时间戳时使用的日期格式。参见 [日期格式]({% link docs/stable/sql/functions/dateformat.md %})。 | `VARCHAR` | (empty) |

## 局限性

`COPY` 不支持表之间的复制。要复制表之间，使用 [`INSERT 语句`]({% link docs/stable/sql/statements/insert.md %})：

```sql
INSERT INTO tbl2
    FROM tbl1;
```