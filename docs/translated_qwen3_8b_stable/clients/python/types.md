---
---
layout: docu
redirect_from:
- /docs/api/python/types
- /docs/api/python/types/
- /docs/clients/python/types
title: 类型 API
---

`DuckDBPyType` 类表示我们 [数据类型]({% link docs/stable/sql/data_types/overview.md %}) 的类型实例。

## 从其他类型转换

为了使 API 尽可能易于使用，我们添加了从现有类型对象到 DuckDBPyType 实例的隐式转换。
这意味着在任何期望 DuckDBPyType 对象的地方，也可以提供以下选项中的任意一种。

### Python 内建类型

下表显示了 Python 内建类型到 DuckDB 类型的映射。

<div class="monospace_table"></div>

| 内建类型 | DuckDB 类型 |
|:---------------|:------------|
| bool           | BOOLEAN     |
| bytearray      | BLOB        |
| bytes          | BLOB        |
| float          | DOUBLE      |
| int            | BIGINT      |
| str            | VARCHAR     |

### NumPy 类型

下表显示了 NumPy 类型到 DuckDB 类型的映射。

<div class="monospace_table"></div>

| 类型        | DuckDB 类型 |
|:------------|:------------|
| bool        | BOOLEAN     |
| float32     | FLOAT       |
| float64     | DOUBLE      |
| int16       | SMALLINT    |
| int32       | INTEGER     |
| int64       | BIGINT      |
| int8        | TINYINT     |
| uint16      | USMALLINT   |
| uint32      | UINTEGER    |
| uint64      | UBIGINT     |
| uint8       | UTINYINT    |

### 嵌套类型

#### `list[child_type]`

`list` 类型对象映射到子类型的 `LIST` 类型。
这也可以任意嵌套。

```python
import duckdb
from typing import Union

duckdb.typing.DuckDBPyType(list[dict[Union[str, int], str]])
```

```text
MAP(UNION(u1 VARCHAR, u2 BIGINT), VARCHAR)[]
```

#### `dict[key_type, value_type]`

`dict` 类型对象映射到键类型和值类型的 `MAP` 类型。

```python
import duckdb

print(duckdb.typing.DuckDBPyType(dict[str, int]))
```

```text
MAP(VARCHAR, BIGINT)
```

#### `{'a': field_one, 'b': field_two, .., 'n': field_n}`

`dict` 对象映射到由字典的键和值组成的 `STRUCT`。

```python
import duckdb

print(duckdb.typing.DuckDBPyType({'a': str, 'b': int}))
```

```text
STRUCT(a VARCHAR, b BIGINT)
```

#### `Union[type_1, ... type_n]`

`typing.Union` 对象映射到提供的类型的 `UNION` 类型。

```python
import duckdb
from typing import Union

print(duckdb.typing.DuckDBPyType(Union[int, str, bool, bytearray]))
```

```text
UNION(u1 BIGINT, u2 VARCHAR, u3 BOOLEAN, u4 BLOB)
```

### 创建函数

对于内建类型，您可以使用 `duckdb.typing` 中定义的常量：

<div class="monospace_table"></div>

| DuckDB 类型    |
|:---------------|
| BIGINT         |
| BIT            |
| BLOB           |
| BOOLEAN        |
| DATE           |
| DOUBLE         |
| FLOAT          |
| HUGEINT        |
| INTEGER        |
| INTERVAL       |
| SMALLINT       |
| SQLNULL        |
| TIME_TZ        |
| TIME           |
| TIMESTAMP_MS   |
| TIMESTAMP_NS   |
| TIMESTAMP_S    |
| TIMESTAMP_TZ   |
| TIMESTAMP      |
| TINYINT        |
| UBIGINT        |
| UHUGEINT       |
| UINTEGER       |
| USMALLINT      |
| UTINYINT       |
| UUID           |
| VARCHAR        |

对于复杂类型，可以在 `DuckDBPyConnection` 对象或 `duckdb` 模块上使用方法。
在任何接受 `DuckDBPyType` 的地方，我们也会接受可以隐式转换为 `DuckDBPyType` 的类型对象。

#### `list_type` | `array_type`

参数：

* `child_type: DuckDBPyType`

#### `struct_type` | `row_type`

参数：

* `fields: Union[list[DuckDBPyType], dict[str, DuckDBPyType]]`

#### `map_type`

参数：

* `key_type: DuckDBPyType`
* `value_type: DuckDBPyType`

#### `decimal_type`

参数：

* `width: int`
* `scale: int`

#### `union_type`

参数：

* `members: Union[list[DuckDBPyType], dict[str, DuckDBPyType]]`

#### `string_type`

参数：

* `collation: Optional[str]`