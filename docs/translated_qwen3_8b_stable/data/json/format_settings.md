---
---
layout: docu
redirect_from:
- /docs/data/json/format_settings
title: JSON格式设置
---

JSON扩展可以尝试在将`format`设置为`auto`时确定JSON文件的格式。
以下是一些示例JSON文件及其应使用的`format`设置。

在以下每个示例中，`format`设置并非必需，因为DuckDB能够正确推断，但为了说明目的而包含。
以下形状的查询在每种情况下都能正常运行：

```sql
SELECT *
FROM filename.json;
```

#### 格式：`newline_delimited`

设置`format = 'newline_delimited'`可以解析换行分隔的JSON。
每一行都是一个JSON对象。

我们使用示例文件 [`records.json`](/data/records.json)，其内容如下：

```json
{"key1":"value1", "key2": "value1"}
{"key1":"value2", "key2": "value2"}
{"key1":"value3", "key2": "value3"}
```

```sql
SELECT *
FROM read_json('records.json', format = 'newline_delimited');
```

<div class="monospace_table"></div>

|  key1  |  key2  |
|--------|--------|
| value1 | value1 |
| value2 | value2 |
| value3 | value3 |

#### 格式：`array`

如果JSON文件包含一个JSON对象数组（格式化或未格式化），可以使用`array_of_objects`。
为了演示其用途，我们使用示例文件 [`records-in-array.json`](/data/records-in-array.json)：

```json
[
    {"key1":"value1", "key2": "value1"},
    {"key1":"value2", "key2": "value2"},
    {"key1":"value3", "key2": "value3"}
]
```

```sql
SELECT *
FROM read_json('records-in-array.json', format = 'array');
```

<div class="monospace_table"></div>

|  key1  |  key2  |
|--------|--------|
| value1 | value1 |
| value2 | value2 |
| value3 | value3 |

#### 格式：`unstructured`

如果JSON文件包含的是非换行分隔的JSON或数组，可以使用`unstructured`。
为了演示其用途，我们使用示例文件 [`unstructured.json`](/data/unstructured.json)：

```json
{
    "key1":"value1",
    "key2":"value1"
}
{
    "key1":"value2",
    "key2":"value2"
}
{
    "key1":"value3",
    "key2":"value3"
}
```

```sql
SELECT *
FROM read_json('unstructured.json', format = 'unstructured');
```

<div class="monospace_table"></div>

|  key1  |  key2  |
|--------|--------|
| value1 | value1 |
| value2 | value2 |
| value3 | value3 |

### 记录设置

JSON扩展可以尝试在设置`records = auto`时确定JSON文件是否包含记录。
当`records = true`时，JSON扩展期望JSON对象，并将JSON对象的字段解包为单独的列。

继续使用相同的示例文件 [`records.json`](/data/records.json)：

```json
{"key1":"value1", "key2": "value1"}
{"key1":"value2", "key2": "value2"}
{"key1":"value3", "key2": "value3"}
```

```sql
SELECT *
FROM read_json('records.json', records = true);
```

<div class="monospace_table"></div>

|  key1  |  key2  |
|--------|--------|
| value1 | value1 |
| value2 | value2 |
| value3 | value3 |

当`records = false`时，JSON扩展不会解包顶层对象，而是创建`STRUCT`：

```sql
SELECT *
FROM read_json('records.json', records = false);
```

<div class="monospace_table"></div>

|               json               |
|----------------------------------|
| {'key1': value1, 'key2': value1} |
| {'key1': value2, 'key2': value2} |
| {'key1': value3, 'key2': value3} |

如果拥有非对象的JSON，这尤其有用，例如 [`arrays.json`](/data/arrays.json)：

```json
[1, 2, 3]
[4, 5, 6]
[7, 8, 9]
```

```sql
SELECT *
FROM read_json('arrays.json', records = false);
```

<div class="monospace_table"></div>

|   json    |
|-----------|
| [1, 2, 3] |
| [4, 5, 6] |
| [7, 8, 9] |