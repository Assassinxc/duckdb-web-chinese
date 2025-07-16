---
---
layout: docu
redirect_from:
- /docs/data/csv/auto_detection
title: CSV 自动检测
---

在使用 `read_csv` 时，系统会尝试使用 [CSV sniff]({% post_url 2023-10-27-csv-sniffer %}) 自动推断如何读取 CSV 文件。
这一步是必要的，因为 CSV 文件不是自描述的，而且存在许多不同的方言。自动检测的工作原理如下：

* 检测 CSV 文件的方言（分隔符、引号规则、转义）
* 检测每一列的数据类型
* 检测文件是否包含标题行

默认情况下，系统会尝试自动检测所有选项。但是，用户可以单独覆盖这些选项。这在系统出错时可能会很有用。例如，如果分隔符选择错误，我们可以通过调用 `read_csv` 并显式指定分隔符（例如 `read_csv('file.csv', delim = '|')`）来覆盖它。

## 采样大小

类型检测通过在文件的样本上操作来进行。
可以通过设置 `sample_size` 参数来修改样本的大小。
默认的样本大小是 20,480 行。
将 `sample_size` 参数设置为 `-1` 表示读取整个文件进行采样：

```sql
SELECT * FROM read_csv('my_csv_file.csv', sample_size = -1);
```

采样的方式进行取决于文件的类型。如果我们从磁盘上的普通文件中读取，系统会跳转到文件中并尝试从文件的不同位置进行采样。
如果我们从无法跳转的文件中读取 – 例如 `.gz` 压缩的 CSV 文件或 `stdin` – 采样只能从文件的开头进行。

## `sniff_csv` 函数

可以使用 `sniff_csv(filename)` 函数将 CSV sniff 作为单独的步骤运行，该函数返回一个包含单行的表格，显示检测到的 CSV 属性。
`sniff_csv` 函数接受一个可选的 `sample_size` 参数来配置采样的行数。

```sql
FROM sniff_csv('my_file.csv');
FROM sniff_csv('my_file.csv', sample_size = 1000);
```

| 列名        | 描述                                   | 示例                                                           |
|-------------|----------------------------------------|----------------------------------------------------------------|
| `Delimiter` | 分隔符                                 | `,`                                                             |
| `Quote`     | 引号字符                               | `"`                                                             |
| `Escape`    | 转义字符                               | `\`                                                             |
| `NewLineDelimiter` | 新行分隔符                         | `\r\n`                                                          |
| `Comment`   | 注释字符                               | `#`                                                             |
| `SkipRows`  | 跳过的行数                             | 1                                                               |
| `HasHeader` | CSV 是否包含标题行                     | `true`                                                          |
| `Columns`   | 列类型编码为 `LIST` 的 `STRUCT`s       | `({'name': 'VARCHAR', 'age': 'BIGINT'})`                        |
| `DateFormat` | 日期格式                               | `%d/%m/%Y`                                                      |
| `TimestampFormat` | 时间戳格式                         | `%Y-%m-%dT%H:%M:%S.%f`                                          |
| `UserArguments` | 用于调用 `sniff_csv` 的参数         | `sample_size = 1000`                                            |
| `Prompt`    | 可用于读取 CSV 的提示语句               | `FROM read_csv('my_file.csv', auto_detect=false, delim=',', ...)` |

### 提示

`Prompt` 列包含一个带有 sniff 检测配置的 SQL 命令。

```sql
-- 在 CLI 中使用行模式以获取完整命令
.mode line
SELECT Prompt FROM sniff_csv('my_file.csv');
```

```text
Prompt = FROM read_csv('my_file.csv', auto_detect=false, delim=',', quote='"', escape='"', new_line='\n', skip=0, header=true, columns={...});
```

## 检测步骤

### 方言检测

方言检测通过尝试使用一组考虑值来解析样本进行。检测到的方言是每行具有（1）一致的列数，以及（2）每行具有最多列的方言。

以下方言会被考虑用于自动方言检测。

<!-- markdownlint-disable MD056 -->

| 参数        | 考虑值         |
|-------------|----------------|
| `delim`     | `,` `|` `;` `\t` |
| `quote`     | `"` `'` (空)   |
| `escape`    | `"` `'` `\` (空) |

<!-- markdownlint-enable MD056 -->

考虑以下示例文件 [`flights.csv`](/data/flights.csv):

```csv
FlightDate|UniqueCarrier|OriginCityName|DestCityName
1988-01-01|AA|New York, NY|Los Angeles, CA
1988-01-02|AA|New York, NY|Los Angeles, CA
1988-01-03|AA|New York, NY|Los Angeles, CA
```

在此文件中，方言检测工作如下：

* 如果我们按 `|` 分隔，每行都会被分成 `4` 列
* 如果我们按 `,` 分隔，第 2-4 行被分成 `3` 列，而第一行被分成 `1` 列
* 如果我们按 `;` 分隔，每行都会被分成 `1` 列
* 如果我们按 `\t` 分隔，每行都会被分成 `1` 列

在此示例中，系统选择 `|` 作为分隔符。所有行被分成相同数量的列，且每行有超过一列，这意味着分隔符实际上出现在 CSV 文件中。

### 类型检测

在检测到方言后，系统会尝试确定每一列的数据类型。请注意，这一步仅在调用 `read_csv` 时执行。在 `COPY` 语句中，将使用目标表的类型。

类型检测通过尝试将每一列的值转换为候选类型进行。如果转换失败，候选类型将从该列的候选类型集合中移除。在处理完所有样本后，选择具有最高优先级的剩余候选类型。默认的候选类型集合如下，按优先级顺序排列：

<div class="monospace_table"></div>

|   类型   |
|----------|
| BOOLEAN  |
| BIGINT   |
| DOUBLE   |
| TIME     |
| DATE     |
| TIMESTAMP |
| VARCHAR  |

所有内容都可以转换为 `VARCHAR`，因此，这个类型具有最低的优先级，意味着如果无法转换为其他类型，所有列都会被转换为 `VARCHAR`。
在 [`flights.csv`](/data/flights.csv) 中，`FlightDate` 列将被转换为 `DATE`，而其他列将被转换为 `VARCHAR`。

CSV 读取器应考虑的候选类型集合可以通过 [`auto_type_candidates`]({% link docs/stable/data/csv/overview.md %}#auto_type_candidates-details) 选项显式指定。

除了默认的候选类型集合，还可以通过 `auto_type_candidates` 选项指定的其他类型包括：

<div class="monospace_table"></div>

|   类型   |
|----------|
| DECIMAL  |
| FLOAT    |
| INTEGER  |
| SMALLINT |
| TINYINT  |

尽管可以自动检测的数据类型集合看起来相当有限，但 CSV 读取器可以通过下一部分中描述的 `types` 选项配置为读取任意复杂的类型。

可以通过使用 `all_varchar` 选项完全禁用类型检测。如果设置此选项，所有列将保持为 `VARCHAR`（如 CSV 文件中原始出现的类型）。

请注意，使用引号字符与不使用引号字符（例如 `"42"` 和 `42`）对于类型检测没有区别。
带引号的字段不会被转换为 `VARCHAR`，相反，sniffer 会尝试找到具有最高优先级的类型候选。

#### 覆盖类型检测

可以使用 `types` 选项单独覆盖检测到的类型。此选项可以接受以下两种选项之一：

* 一个类型定义列表（例如 `types = ['INTEGER', 'VARCHAR', 'DATE']`）。这会按 CSV 文件中列的出现顺序覆盖列的类型。
* 或者，`types` 接受一个 `name` → `type` 映射，用于覆盖单个列的选项（例如 `types = {'quarter': 'INTEGER'}`）。

使用 `types` 选项可以指定的列类型集合不像 `auto_type_candidates` 选项中的类型那样有限：任何有效的类型定义都可以被 `types` 选项接受。（要获取有效的类型定义，请使用 [`typeof()`]({% link docs/stable/sql/functions/utility.md %}#typeofexpression) 函数，或者使用 [`DESCRIBE`]({% link docs/stable/guides/meta/describe.md %}) 结果的 `column_type` 列。）

`sniff_csv()` 函数的 `Column` 字段返回一个包含列名和类型的结构体，可以作为覆盖类型的依据。

## 标题检测

标题检测通过检查候选标题行是否在文件的其他行中在类型上有所不同来进行。例如，在 [`flights.csv`](/data/flights.csv) 中，我们可以看到标题行只包含 `VARCHAR` 列 – 而值中 `FlightDate` 列包含 `DATE` 值。因此，系统将第一行定义为标题行，并从标题行中提取列名。

在没有标题行的文件中，列名将被生成为 `column0`、`column1` 等。

请注意，如果所有列都是 `VARCHAR` 类型，标题检测将无法正确进行 – 在这种情况下，系统无法区分标题行和其他行。在这种情况下，系统假设文件包含标题。可以通过将 `header` 选项设置为 `false` 来覆盖此行为。

### 日期和时间戳

DuckDB 默认支持 [ISO 8601 格式](https://en.wikipedia.org/wiki/ISO_8601) 的时间戳、日期和时间。不幸的是，不是所有的日期和时间都使用此标准进行格式化。因此，CSV 读取器还支持 `dateformat` 和 `timestampformat` 选项。使用此格式，用户可以指定一个 [格式字符串]({% link docs/stable/sql/functions/dateformat.md %}) 来指示如何读取日期或时间戳。

作为自动检测的一部分，系统会尝试判断日期和时间是否以不同的表示形式存储。这并不总是可能的，因为表示形式中存在歧义。例如，日期 `01-02-2000` 可以被解析为 1 月 2 日或 2 月 1 日。通常，这些歧义可以通过后续遇到的日期来解决。例如，如果我们后来遇到日期 `21-02-2000`，那么我们知道格式必须是 `DD-MM-YYYY`。`MM-DD-YYYY` 不再可能，因为没有 21 月。

如果数据无法解决这些歧义，系统会有一个优先顺序的日期格式列表。如果系统选择错误，用户可以手动指定 `dateformat` 和 `timestampformat` 选项。

系统考虑的日期格式（`dateformat`）如下。在存在歧义的情况下，优先选择较高的条目（即 ISO 8601 优先于 `MM-DD-YYYY`）。

<div class="monospace_table"></div>

| dateformat |
|------------|
| ISO 8601   |
| %y-%m-%d   |
| %Y-%m-%d   |
| %d-%m-%y   |
| %d-%m-%Y   |
| %m-%d-%y   |
| %m-%d-%Y   |

系统考虑的时间戳格式（`timestampformat`）如下。在存在歧义的情况下，优先选择较高的条目。

<div class="monospace_table"></div>

|   timestampformat    |
|----------------------|
| ISO 18601            |
| %y-%m-%d %H:%M:%S    |
| %Y-%m-%d %H:%M:%S    |
| %d-%m-%y %H:%M:%S    |
| %d-%m-%Y %H:%M:%S    |
| %m-%d-%y %I:%M:%S %p |
| %m-%d-%Y %I:%M:%S %p |
| %Y-%m-%d %H:%M:%S.%f |