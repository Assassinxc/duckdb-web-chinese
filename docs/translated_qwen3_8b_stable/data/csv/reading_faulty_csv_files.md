---
---
layout: docu
redirect_from:
- /docs/data/csv/reading_faulty_csv_files
title: 读取损坏的CSV文件
---

CSV文件可以呈现各种形式，其中一些文件包含大量错误，使得干净地读取这些文件变得困难。为了帮助用户读取这些文件，DuckDB支持详细的错误信息、跳过错误行的功能，以及将错误行存储到临时表中，以协助用户进行数据清洗。

## 结构错误

DuckDB支持检测和跳过多种结构错误。在本节中，我们将通过示例逐一介绍每种错误。
对于这些示例，请考虑以下表格：

```sql
CREATE TABLE people (name VARCHAR, birth_date DATE);
```

DuckDB检测到以下错误类型：

* `CAST`: 当CSV文件中的某一列无法转换为预期的模式值时，会发生类型转换错误。例如，行`Pedro,The 90s`会导致错误，因为字符串`The 90s`无法转换为日期。
* `MISSING COLUMNS`: 如果CSV文件中的一行包含的列数少于预期，会发生此错误。在我们的示例中，我们期望两列；因此，只包含一个值的行，例如`Pedro`，会导致此错误。
* `TOO MANY COLUMNS`: 如果CSV文件中的一行包含的列数多于预期，会发生此错误。在我们的示例中，任何包含超过两列的行都会导致此错误，例如`Pedro,01-01-1992,pdet`。
* `UNQUOTED VALUE`: CSV行中的引号值在结尾时必须取消引号；如果引号值在整个过程中保持引号，会导致错误。例如，假设我们的扫描器使用`quote='"'`，行`"pedro"holanda, 01-01-1992`会显示为未引号值错误。
* `LINE SIZE OVER MAXIMUM`: DuckDB有一个参数设置CSV文件的最大行大小，默认设置为2,097,152字节。假设我们的扫描器设置为`max_line_size = 25`，行`Pedro Holanda, 01-01-1992`会导致错误，因为它超过25字节。
* `INVALID ENCODING`: DuckDB支持UTF-8字符串、UTF-16和Latin-1编码。包含其他字符的行将导致错误。例如，行`pedro\xff\xff, 01-01-1992`会引发问题。

### CSV错误的结构

默认情况下，执行CSV读取时，如果遇到任何结构错误，扫描器会立即停止扫描过程并将错误抛给用户。
这些错误旨在提供尽可能多的信息，使用户可以直接在CSV文件中评估这些错误。

这是一个完整的错误信息示例：

```console
转换错误：
CSV错误在第5648行
原始行：Pedro,The 90s
在转换“birth_date”列时发生错误。日期字段值超出范围：“The 90s”，预期格式为(DD-MM-YYYY)

“date”列被转换为类型DATE
此类型是从CSV文件中自动检测到的。
可能的解决方案：
* 手动设置该列的类型以覆盖类型，例如：types={'birth_date': 'VARCHAR'}
* 将样本大小设置为更大的值以使自动检测扫描更多值，例如：sample_size=-1
* 使用COPY语句从现有表中自动推导类型。

  文件= people.csv
  分隔符 = , (自动检测)
  引号 = " (自动检测)
  转义符 = " (自动检测)
  新行 = \r\n (自动检测)
  标头 = true (自动检测)
  跳过行 = 0 (自动检测)
  日期格式 = (DD-MM-YYYY) (自动检测)
  时间戳格式 =  (自动检测)
  null_padding=0
  sample_size=20480
  ignore_errors=false
  all_varchar=0
```

第一部分为我们提供了有关错误发生位置的信息，包括行号、原始CSV行和哪个字段有问题：

```console
转换错误：
CSV错误在第5648行
原始行：Pedro,The 90s
在转换“birth_date”列时发生错误。日期字段值超出范围：“The 90s”，预期格式为(DD-MM-YYYY)
```

第二部分为我们提供了可能的解决方案：

```console
“date”列被转换为类型DATE
此类型是从CSV文件中自动检测到的。
可能的解决方案：
* 手动设置该列的类型以覆盖类型，例如：types={'birth_date': 'VARCHAR'}
* 将样本大小设置为更大的值以使自动检测扫描更多值，例如：sample_size=-1
* 使用COPY语句从现有表中自动推导类型。
```

由于该字段的类型是自动检测到的，这表明应将该字段定义为`VARCHAR`或充分利用数据集进行类型检测。

最后，最后一部分展示了扫描器中使用的某些选项，这些选项可能导致错误，并表明它们是自动检测到的还是用户手动设置的。

## 使用`ignore_errors`选项

在某些情况下，CSV文件可能包含多个结构错误，用户仅希望跳过这些错误并读取正确的数据。通过使用`ignore_errors`选项，可以读取包含错误的CSV文件。设置此选项后，包含会导致CSV解析器生成错误的数据的行将被忽略。在我们的示例中，我们将演示一个类型转换错误，但请注意，我们结构错误部分中描述的任何错误都会导致错误行被跳过。

例如，考虑以下CSV文件，[`faulty.csv`](/data/faulty.csv)：

```csv
Pedro,31
Oogie Boogie, three
```

如果读取CSV文件，并指定第一列是`VARCHAR`，第二列是`INTEGER`，加载文件将失败，因为字符串`three`无法转换为`INTEGER`。

例如，以下查询将抛出类型转换错误。

```sql
FROM read_csv('faulty.csv', columns = {'name': 'VARCHAR', 'age': 'INTEGER'});
```

但是，设置`ignore_errors`后，文件的第二行被跳过，只输出完整的第一行。例如：

```sql
FROM read_csv(
    'faulty.csv',
    columns = {'name': 'VARCHAR', 'age': 'INTEGER'},
    ignore_errors = true
);
```

输出：

| name  | age |
|-------|-----|
| Pedro | 31  |

需要注意的是，CSV解析器受到投影下推优化的影响。因此，如果我们只选择名称列，两行都将被视为有效，因为年龄的类型转换错误将永远不会发生。例如：

```sql
SELECT name
FROM read_csv('faulty.csv', columns = {'name': 'VARCHAR', 'age': 'INTEGER'});
```

输出：

|     name     |
|--------------|
|     Pedro    |
| Oogie Boogie |

## 获取损坏的CSV行

能够读取损坏的CSV文件很重要，但对于许多数据清洗操作，还需要知道哪些行是损坏的，以及解析器在这些行上发现了哪些错误。对于这些场景，可以使用DuckDB的CSV拒绝表功能。
默认情况下，此功能会创建两个临时表。

1. `reject_scans`: 存储有关CSV扫描器参数的信息
2. `reject_errors`: 存储有关每个损坏的CSV行及其在哪个CSV扫描器中发生的信息。

请注意，我们结构错误部分中描述的任何错误都会存储在拒绝表中。此外，如果一行有多个错误，同一行会存储多个条目，每个错误一个条目。

### 拒绝扫描

CSV拒绝扫描表返回以下信息：

| 列名 | 描述 | 类型 |
|:--|:-----|:-|
| `scan_id` | DuckDB中用于表示该扫描器的内部ID | `UBIGINT` |
| `file_id` | 扫描器可能在多个文件上运行，因此file_id表示扫描器中的唯一文件 | `UBIGINT` |
| `file_path` | 文件路径 | `VARCHAR` |
| `delimiter` | 用于分隔符，例如； | `VARCHAR` |
| `quote` | 用于引号，例如" | `VARCHAR` |
| `escape` | 用于转义符，例如" | `VARCHAR` |
| `newline_delimiter` | 用于新行分隔符，例如\r\n | `VARCHAR` |
| `skip_rows` | 如果有行从文件顶部被跳过 | `UINTEGER` |
| `has_header` | 如果文件有标题 | `BOOLEAN` |
| `columns` | 文件的模式（即所有列名和类型） | `VARCHAR` |
| `date_format` | 日期类型的格式 | `VARCHAR` |
| `timestamp_format` | 时间戳类型的格式 | `VARCHAR` |
| `user_arguments` | 用户手动设置的任何额外扫描器参数 | `VARCHAR` |

### 拒绝错误

CSV拒绝错误表返回以下信息：

| 列名 | 描述 | 类型 |
|:--|:-----|:-|
| `scan_id` | DuckDB中用于表示该扫描器的内部ID，用于与拒绝扫描表连接 | `UBIGINT` |
| `file_id` | 表示扫描器中的唯一文件的file_id，用于与拒绝扫描表连接 | `UBIGINT` |
| `line` | 错误发生的CSV文件中的行号 | `UBIGINT` |
| `line_byte_position` | 错误发生的行的起始字节位置 | `UBIGINT` |
| `byte_position` | 错误发生的字节位置 | `UBIGINT` |
| `column_idx` | 如果错误发生在特定列中，该列的索引 | `UBIGINT` |
| `column_name` | 如果错误发生在特定列中，该列的名称 | `VARCHAR` |
| `error_type` | 发生的错误类型 | `ENUM` |
| `csv_line` | 原始CSV行 | `VARCHAR` |
| `error_message` | DuckDB生成的错误信息 | `VARCHAR` |

## 参数

以下列出的参数用于`read_csv`函数配置CSV拒绝表。

| 名称 | 描述 | 类型 | 默认 |
|:--|:-----|:-|:-|
| `store_rejects` | 如果设置为true，文件中的任何错误将被跳过并存储在默认的拒绝临时表中。 | `BOOLEAN` | False |
| `rejects_scan` | 存储损坏CSV文件扫描信息的临时表名称。 | `VARCHAR` | reject_scans |
| `rejects_table` | 存储CSV文件中损坏行信息的临时表名称。 | `VARCHAR` | reject_errors |
| `rejects_limit` | 从CSV文件记录到拒绝表中的损坏记录数的上限。0表示不应用限制。 | `BIGINT` | 0 |

要将损坏的CSV行信息存储在拒绝表中，用户只需将`store_rejects`选项设置为true。例如：

```sql
FROM read_csv(
    'faulty.csv',
    columns = {'name': 'VARCHAR', 'age': 'INTEGER'},
    store_rejects = true
);
```

然后，您可以查询`reject_scans`和`reject_errors`表，以获取有关被拒绝的元组的信息。例如：

```sql
FROM reject_scans;
```

输出：

<div class="monospace_table"></div>

| scan_id | file_id |             file_path             | delimiter | quote | escape | newline_delimiter | skip_rows | has_header |               columns                | date_format | timestamp_format |   user_arguments   |
|---------|---------|-----------------------------------|-----------|-------|--------|-------------------|-----------|-----------:|--------------------------------------|-------------|------------------|--------------------|
| 5       | 0       | faulty.csv | ,         | "     | "      | \n                | 0         | false      | {'name': 'VARCHAR','age': 'INTEGER'} |             |                  | store_rejects=true |

```sql
FROM reject_errors;
```

输出：

<div class="monospace_table"></div>

| scan_id | file_id | line | line_byte_position | byte_position | column_idx | column_name | error_type |      csv_line       |                                   error_message                                    |
|---------|---------|------|--------------------|---------------|------------|-------------|------------|---------------------|------------------------------------------------------------------------------------|
| 5       | 0       | 2    | 10                 | 23            | 2          | age         | CAST       | Oogie Boogie, three | Error when converting column "age". Could not convert string " three" to 'INTEGER' |