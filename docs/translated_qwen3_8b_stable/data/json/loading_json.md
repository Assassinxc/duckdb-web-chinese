---
---
layout: docu
redirect_from:
- /docs/data/json/loading_json
title: 加载 JSON
---

DuckDB 的 JSON 读取器可以通过分析 JSON 文件自动推断应使用哪些配置标志。这在大多数情况下都能正常工作，应作为首选选项。在极少数情况下，当 JSON 读取器无法确定正确的配置时，可以手动配置 JSON 读取器以正确解析 JSON 文件。

## `read_json` 函数

`read_json` 是加载 JSON 文件的最简单方法：它会自动尝试确定 JSON 读取器的正确配置。它还会自动推断列的类型。
在以下示例中，我们使用 [`todos.json`](/data/json/todos.json) 文件，

```sql
SELECT *
FROM read_json('todos.json')
LIMIT 5;
```

| userId | id |                              title                              | completed |
|-------:|---:|-----------------------------------------------------------------|-----------|
| 1      | 1  | delectus aut autem                                              | false     |
| 1      | 2  | quis ut nam facilis et officia qui                              | false     |
| 1      | 3  | fugiat veniam minus                                             | false     |
| 1      | 4  | et porro tempora                                                | true      |
| 1      | 5  | laboriosam mollitia et enim quasi adipisci quia provident illum | false     |

我们也可以使用 `read_json` 创建一个持久表：

```sql
CREATE TABLE todos AS
    SELECT *
    FROM read_json('todos.json');
DESCRIBE todos;
```

<div class="monospace_table"></div>

| column_name | column_type | null | key  | default | extra |
|-------------|-------------|------|------|---------|-------|
| userId      | UBIGINT     | YES  | NULL | NULL    | NULL  |
| id          | UBIGINT     | YES  | NULL | NULL    | NULL  |
| title       | VARCHAR     | YES  | NULL | NULL    | NULL  |
| completed   | BOOLEAN     | YES  | NULL | NULL    | NULL  |

如果我们为部分列指定类型，`read_json` 将会排除未指定的列：

```sql
SELECT *
FROM read_json(
        'todos.json',
        columns = {userId: 'UBIGINT', completed: 'BOOLEAN'}
    )
LIMIT 5;
```

请注意，只有 `userId` 和 `completed` 列会被显示：

| userId | completed |
|-------:|----------:|
| 1      | false     |
| 1      | false     |
| 1      | false     |
| 1      | true      |
| 1      | false     |

可以通过提供一个通配符或文件列表一次读取多个文件。更多信息请参阅 [多文件部分]({% link docs/stable/data/multiple_files/overview.md %}).

## 读取 JSON 对象的函数

以下表函数用于读取 JSON：

| 函数 | 描述 |
|:---|:---|
| `read_json_objects(filename)`      | 从 `filename` 读取一个 JSON 对象，其中 `filename` 也可以是文件列表或通配符模式。 |
| `read_ndjson_objects(filename)`    | `read_json_objects` 的别名，`format` 参数设置为 `newline_delimited`。 |
| `read_json_objects_auto(filename)` | `read_json_objects` 的别名，`format` 参数设置为 `auto`。 |

### 参数

这些函数具有以下参数：

| 名称 | 描述 | 类型 | 默认值 |
|:--|:-----|:-|:-|
| `compression` | 文件的压缩类型。默认情况下，将根据文件扩展名自动检测（例如，`t.json.gz` 使用 gzip，`t.json` 使用 none）。选项包括 `none`、`gzip`、`zstd` 和 `auto_detect`。 | `VARCHAR` | `auto_detect` |
| `filename` | 是否在结果中包含额外的 `filename` 列。自 DuckDB v1.3.0 起，`filename` 列会自动添加为虚拟列，此选项仅保留以兼容性。 | `BOOL` | `false` |
| `format` | 可以是 `auto`、`unstructured`、`newline_delimited` 和 `array` 中的一种。 | `VARCHAR` | `array` |
| `hive_partitioning` | 是否将路径解释为 [Hive 分区路径]({% link docs/stable/data/partitioning/hive_partitioning.md %})。 | `BOOL` | (自动检测) |
| `ignore_errors` | 是否忽略解析错误（仅在 `format` 为 `newline_delimited` 时有效）。 | `BOOL` | `false` |
| `maximum_sample_files` | 用于自动检测的最大 JSON 文件样本数。 | `BIGINT` | `32` |
| `maximum_object_size` | JSON 对象的最大大小（以字节为单位）。 | `UINTEGER` | `16777216` |

`format` 参数指定如何从文件中读取 JSON。
使用 `unstructured` 时，读取顶层 JSON，例如对于 `birds.json`：

```json
{
  "duck": 42
}
{
  "goose": [1, 2, 3]
}
```

```sql
FROM read_json_objects('birds.json', format = 'unstructured');
```

将读取两个对象：

```text
┌──────────────────────────────┐
│             json             │
│             json             │
├──────────────────────────────┤
│ {\n    "duck": 42\n}         │
│ {\n    "goose": [1, 2, 3]\n} │
└──────────────────────────────┘
```

使用 `newline_delimited` 时，读取 [NDJSON](https://github.com/ndjson/ndjson-spec)，每个 JSON 之间用换行符（`\n`）分隔，例如对于 `birds-nd.json`：

```json
{"duck": 42}
{"goose": [1, 2, 3]}
```

```sql
FROM read_json_objects('birds-nd.json', format = 'newline_delimited');
```

也将读取两个对象：

```text
┌──────────────────────┐
│         json         │
│         json         │
├──────────────────────┤
│ {"duck": 42}         │
│ {"goose": [1, 2, 3]} │
└──────────────────────┘
```

使用 `array` 时，每个数组元素都会被读取，例如对于 `birds-array.json`：

```json
[
    {
        "duck": 42
    },
    {
        "goose": [1, 2, 3]
    }
]
```

```sql
FROM read_json_objects('birds-array.json', format = 'array');
```

将再次读取两个对象：

```text
┌──────────────────────────────────────┐
│                 json                 │
│                 json                 │
├──────────────────────────────────────┤
│ {\n        "duck": 42\n    }         │
│ {\n        "goose": [1, 2, 3]\n    } │
└──────────────────────────────────────┘
```

## 作为表读取 JSON 的函数

DuckDB 还支持将 JSON 作为表读取，使用以下函数：

| 函数 | 描述 |
|:---------|:----------------|
| `read_json(filename)`        | 从 `filename` 读取 JSON，其中 `filename` 也可以是文件列表或通配符模式。 |
| `read_json_auto(filename)`   | `read_json` 的别名。 |
| `read_ndjson(filename)`      | `read_json` 的别名，`format` 参数设置为 `newline_delimited`。 |
| `read_ndjson_auto(filename)` | `read_json` 的别名，`format` 参数设置为 `newline_delimited`。 |

### 参数

除了 `maximum_object_size`、`format`、`ignore_errors` 和 `compression`，这些函数还有其他参数：

| 名称 | 描述 | 类型 | 默认值 |
|:--|:------|:-|:-|
| `auto_detect` | 是否自动检测键名和值的数据类型 | `BOOL` | `true` |
| `columns` | 一个结构体，指定 JSON 文件中包含的键名和值类型（例如，`{key1: 'INTEGER', key2: 'VARCHAR'}`）。如果启用了 `auto_detect`，这些将被推断 | `STRUCT` | `(empty)` |
| `dateformat` | 指定解析日期时使用的日期格式。详见 [日期格式]({% link docs/stable/sql/functions/dateformat.md %}) | `VARCHAR` | `iso` |
| `maximum_depth` | 自动模式检测类型时的最大嵌套深度。设置为 -1 以完全检测嵌套 JSON 类型 | `BIGINT` | `-1` |
| `records` | 可以是 `auto`、`true` 或 `false` | `VARCHAR` | `auto` |
| `sample_size` | 定义用于自动 JSON 类型检测的样本对象数量。设置为 -1 以扫描整个输入文件 | `UBIGINT` | `20480` |
| `timestampformat` | 指定解析时间戳时使用的日期格式。详见 [日期格式]({% link docs/stable/sql/functions/dateformat.md %}) | `VARCHAR` | `iso`|
| `union_by_name` | 是否将多个 JSON 文件的模式 [统一]({% link docs/stable/data/multiple_files/combining_schemas.md %}) | `BOOL` | `false` |
| `map_inference_threshold` | 控制自动检测的列数的阈值；如果 JSON 模式自动检测会推断一个字段具有 _超过_ 该阈值数量的子字段的 `STRUCT` 类型，则推断为 `MAP` 类型。设置为 `-1` 以禁用 `MAP` 推断 | `BIGINT` | `200` |
| `field_appearance_threshold` | JSON 读取器将每个 JSON 字段的出现次数除以自动检测样本大小。如果对象中字段的平均值小于此阈值，则会默认使用一个 `MAP` 类型，其值类型为合并的字段类型 | `DOUBLE` | `0.1` |

请注意，DuckDB 可以将 JSON 数组直接转换为其内部的 `LIST` 类型，缺失的键会变成 `NULL`：

```sql
SELECT *
FROM read_json(
    ['birds1.json', 'birds2.json'],
    columns = {duck: 'INTEGER', goose: 'INTEGER[]', swan: 'DOUBLE'}
);
```

<div class="monospace_table"></div>

| duck |   goose   | swan |
|-----:|-----------|-----:|
| 42   | [1, 2, 3] | NULL |
| 43   | [4, 5, 6] | 3.3  |

DuckDB 可以自动检测这些类型：

```sql
SELECT goose, duck FROM read_json('*.json.gz');
SELECT goose, duck FROM '*.json.gz'; -- 等效
```

DuckDB 可以读取（并自动检测）各种格式，通过 `format` 参数指定。
查询一个包含 `array` 的 JSON 文件，例如：

```json
[
  {
    "duck": 42,
    "goose": 4.2
  },
  {
    "duck": 43,
    "goose": 4.3
  }
]
```

可以像查询包含 `unstructured` JSON 的 JSON 文件一样查询：

```json
{
    "duck": 42,
    "goose": 4.2
}
{
    "duck": 43,
    "goose": 4.3
}
```

两者都可以作为表读取：

```sql
SELECT
FROM read_json('birds.json');
```

<div class="monospace_table"></div>

| duck | goose |
|-----:|------:|
|   42 |   4.2 |
|   43 |   4.3 |

如果您的 JSON 文件不包含“记录”，即，除了对象之外的任何其他类型的 JSON，DuckDB 仍可以读取它。
通过 `records` 参数指定。
`records` 参数指定 JSON 是否包含应解包为单独列的记录。
DuckDB 也会尝试自动检测这一点。
例如，考虑以下文件，`birds-records.json`：

```json
{"duck": 42, "goose": [1, 2, 3]}
{"duck": 43, "goose": [4, 5, 6]}
```

```sql
SELECT *
FROM read_json('birds-records.json');
```

查询结果为两列：

<div class="monospace_table"></div>

| duck | goose   |
|-----:|:--------|
|   42 | [1,2,3] |
|   43 | [4,5,6] |

您也可以将 `records` 设置为 `false` 来读取同一文件，以获得一个列，该列是一个包含数据的 `STRUCT`：

<div class="monospace_table"></div>

| json |
|:-----|
| {'duck': 42, 'goose': [1,2,3]} |
| {'duck': 43, 'goose': [4,5,6]} |

如需更多复杂数据的读取示例，请参阅 [“Shredding Deeply Nested JSON, One Vector at a Time” 博客文章]({% post_url 2023-03-03-json %}).

## 使用 `FORMAT json` 的 `COPY` 语句加载数据

当安装了 `json` 扩展时，`FORMAT json` 支持 `COPY FROM`、`IMPORT DATABASE`、`COPY TO` 和 `EXPORT DATABASE`。详见 [`COPY` 语句]({% link docs/stable/sql/statements/copy.md %}) 和 [`IMPORT` / `EXPORT` 子句]({% link docs/stable/sql/statements/export.md %}).

默认情况下，`COPY` 期望的是换行分隔的 JSON。如果您更倾向于复制 JSON 数组的数据，可以指定 `ARRAY true`，例如，

```sql
COPY (SELECT * FROM range(5) r(i))
TO 'numbers.json' (ARRAY true);
```

将创建以下文件：

```json
[
	{"i":0},
	{"i":1},
	{"i":2},
	{"i":3},
	{"i":4}
]
```

可以将其读回 DuckDB 中如下：

```sql
CREATE TABLE numbers (i BIGINT);
COPY numbers FROM 'numbers.json' (ARRAY true);
```

格式可以自动检测如下：

```sql
CREATE TABLE numbers (i BIGINT);
COPY numbers FROM 'numbers.json' (AUTO_DETECT true);
```

我们也可以从自动检测的模式创建表：

```sql
CREATE TABLE numbers AS
    FROM 'numbers.json';
```

### 参数

| 名称 | 描述 | 类型 | 默认值 |
|:--|:-----|:-|:-|
| `auto_detect` | 是否自动检测键名和值的数据类型 | `BOOL` | `false` |
| `columns` | 一个结构体，指定 JSON 文件中包含的键名和值类型（例如，`{key1: 'INTEGER', key2: 'VARCHAR'}`）。如果启用了 `auto_detect`，这些将被推断 | `STRUCT` | `(empty)` |
| `compression` | 文件的压缩类型。默认情况下，将根据文件扩展名自动检测（例如，`t.json.gz` 使用 gzip，`t.json` 使用 none）。选项包括 `uncompressed`、`gzip`、`zstd` 和 `auto_detect`。 | `VARCHAR` | `auto_detect` |
| `convert_strings_to_integers` | 是否将表示整数值的字符串转换为数值类型。 | `BOOL` | `false` |
| `dateformat` | 指定解析日期时使用的日期格式。详见 [日期格式]({% link docs/stable/sql/functions/dateformat.md %}) | `VARCHAR` | `iso` |
| `filename` | 是否在结果中包含额外的 `filename` 列。 | `BOOL` | `false` |
| `format` | 可以是 `auto, unstructured, newline_delimited, array` 中的一种。 | `VARCHAR` | `array` |
| `hive_partitioning` | 是否将路径解释为 [Hive 分区路径]({% link docs/stable/data/partitioning/hive_partitioning.md %})。 | `BOOL` | `false` |
| `ignore_errors` | 是否忽略解析错误（仅在 `format` 为 `newline_delimited` 时有效）。 | `BOOL` | `false` |
| `maximum_depth` | 自动模式检测类型时的最大嵌套深度。设置为 -1 以完全检测嵌套 JSON 类型。 | `BIGINT` | `-1` |
| `maximum_object_size` | JSON 对象的最大大小（以字节为单位）。 | `UINTEGER` | `16777216` |
| `records` | 可以是 `auto`、`true` 或 `false`。 | `VARCHAR` | `records` |
| `sample_size` | 定义用于自动 JSON 类型检测的样本对象数量。设置为 -1 以扫描整个输入文件。 | `UBIGINT` | `20480` |
| `timestampformat` | 指定解析时间戳时使用的日期格式。详见 [日期格式]({% link docs/stable/sql/functions/dateformat.md %})。 | `VARCHAR` | `iso`|
| `union_by_name` | 是否将多个 JSON 文件的模式 [统一]({% link docs/stable/data/multiple_files/combining_schemas.md %})。 | `BOOL` | `false` |