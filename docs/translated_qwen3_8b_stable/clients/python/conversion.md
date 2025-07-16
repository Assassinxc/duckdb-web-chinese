---
---
layout: docu
redirect_from:
- /docs/api/python/conversion
- /docs/api/python/conversion/
- /docs/api/python/result_conversion
- /docs/api/python/result_conversion/
- /docs/clients/python/conversion
title: DuckDB 与 Python 之间的转换
---

本页面文档说明了将 [Python 对象转换为 DuckDB](#object-conversion-python-object-to-duckdb) 和 [DuckDB 结果转换为 Python](#result-conversion-duckdb-results-to-python) 的规则。

## 对象转换：Python 对象到 DuckDB

这是 Python 对象类型到 DuckDB [逻辑类型]({% link docs/stable/sql/data_types/overview.md %}) 的映射：

* `None` → `NULL`
* `bool` → `BOOLEAN`
* `datetime.timedelta` → `INTERVAL`
* `str` → `VARCHAR`
* `bytearray` → `BLOB`
* `memoryview` → `BLOB`
* `decimal.Decimal` → `DECIMAL` / `DOUBLE`
* `uuid.UUID` → `UUID`

其余的转换规则如下。

### `int`

由于 Python 中的整数可以具有任意大小，因此无法进行一对一的转换。
相反，我们会按以下顺序进行这些类型转换，直到其中一个成功：

* `BIGINT`
* `INTEGER`
* `UBIGINT`
* `UINTEGER`
* `DOUBLE`

当使用 DuckDB Value 类时，可以设置目标类型，这将影响转换过程。

### `float`

这些类型转换将按以下顺序尝试，直到其中一个成功：

* `DOUBLE`
* `FLOAT`

### `datetime.datetime`

对于 `datetime`，如果 `pandas.isnull` 可用，我们将检查它是否为 `NULL`，如果返回 `true`，则返回 `NULL`。
我们将检查 `datetime.datetime.min` 和 `datetime.datetime.max` 来分别转换为 `-inf` 和 `+inf`。

如果 `datetime` 具有 tzinfo，我们将使用 `TIMESTAMPTZ`，否则它将变成 `TIMESTAMP`。

### `datetime.time`

如果 `time` 具有 tzinfo，我们将使用 `TIMETZ`，否则它将变成 `TIME`。

### `datetime.date`

`date` 转换为 `DATE` 类型。
我们将检查 `datetime.date.min` 和 `datetime.date.max` 来分别转换为 `-inf` 和 `+inf`。

### `bytes`

`bytes` 默认转换为 `BLOB`，当它被用于构造 `BITSTRING` 类型的 Value 对象时，它会映射为 `BITSTRING`。

### `list`

`list` 会变成其子项“最宽松”的类型所构成的 `LIST` 类型，例如：

```python
my_list_value = [
    12345,
    "test"
]
```

将变成 `VARCHAR[]`，因为 12345 可以转换为 `VARCHAR`，但 `test` 无法转换为 `INTEGER`。

```sql
[12345, test]
```

### `dict`

`dict` 对象可以转换为 `STRUCT(...)` 或 `MAP(..., ...)`，具体取决于其结构。
如果字典的结构类似于以下内容：

```python
import duckdb

my_map_dict = {
    "key": [
        1, 2, 3
    ],
    "value": [
        "one", "two", "three"
    ]
}

duckdb.values(my_map_dict)
```

那么我们将将其转换为两个列表压缩后的键值对的 `MAP`。
上面的例子会变成 `MAP(INTEGER, VARCHAR)`：

```text
┌─────────────────────────┐
│ {1=one, 2=two, 3=three} │
│  map(integer, varchar)  │
├─────────────────────────┤
│ {1=one, 2=two, 3=three} │
└─────────────────────────┘
```

如果字典是由 [函数]({% link docs/stable/clients/python/function.md %}) 返回的，
函数将返回 `MAP`，因此必须指定 `return_type`。提供无法转换为 `MAP` 的返回类型将引发错误：

```python
import duckdb
duckdb_conn = duckdb.connect()

def get_map() -> dict[str,list[str]|list[int]]:
    return {
        "key": [
            1, 2, 3
        ],
        "value": [
            "one", "two", "three"
        ]
    }

duckdb_conn.create_function("get_map", get_map, return_type=dict[int, str])

duckdb_conn.sql("select get_map()").show()

duckdb_conn.create_function("get_map_error", get_map)

duckdb_conn.sql("select get_map_error()").show()
```
 ```text
┌─────────────────────────┐
│        get_map()        │
│  map(bigint, varchar)   │
├─────────────────────────┤
│ {1=one, 2=two, 3=three} │
└─────────────────────────┘

ConversionException: Conversion Error: Type VARCHAR can't be cast as UNION(u1 VARCHAR[], u2 BIGINT[]). VARCHAR can't be implicitly cast to any of the union member types: VARCHAR[], BIGINT[]
```

> 字段名称很重要，两个列表必须具有相同的大小。

否则，我们将尝试将其转换为 `STRUCT`。

```python
import duckdb

my_struct_dict = {
    1: "one",
    "2": 2,
    "three": [1, 2, 3],
    False: True
}

duckdb.values(my_struct_dict)
```
会变成：

```text
┌────────────────────────────────────────────────────────────────────┐
│      {'1': 'one', '2': 2, 'three': [1, 2, 3], 'False': true}       │
│ struct("1" varchar, "2" integer, three integer[], "false" boolean) │
├────────────────────────────────────────────────────────────────────┤
│ {'1': one, '2': 2, 'three': [1, 2, 3], 'False': true}              │
└────────────────────────────────────────────────────────────────────┘
```

如果字典是由 [函数]({% link docs/stable/clients/python/function.md %}) 返回的，
由于 [自动转换]({% link docs/stable/clients/python/types.md %}#dictkey_type-value_type)，函数将返回 `MAP`。要返回 `STRUCT`，必须提供 `return_type`：
```python
import duckdb
from duckdb.typing import BOOLEAN, INTEGER, VARCHAR
from duckdb import list_type, struct_type

duckdb_conn = duckdb.connect()

my_struct_dict = {
    1: "one",
    "2": 2,
    "three": [1, 2, 3],
    False: True
}

def get_struct() -> dict[str|int|bool,str|int|list[int]|bool]:
    return my_struct_dict

duckdb_conn.create_function("get_struct_as_map", get_struct)

duckdb_conn.sql("select get_struct_as_map()").show()

duckdb_conn.create_function("get_struct", get_struct, return_type=struct_type({
    1: VARCHAR,
    "2": INTEGER,
    "three": list_type(duckdb.typing.INTEGER),
    False: BOOLEAN
}))

duckdb_conn.sql("select get_struct()").show()
```

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                         get_struct_as_map()                                          │
│ map(union(u1 varchar, u2 bigint, u3 boolean), union(u1 varchar, u2 bigint, u3 bigint[], u4 boolean)) │
├──────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ {1=one, 2=2, three=[1, 2, 3], false=true}                                                            │
└──────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│                            get_struct()                            │
│ struct("1" varchar, "2" integer, three integer[], "false" boolean) │
├────────────────────────────────────────────────────────────────────┤
│ {'1': one, '2': 2, 'three': [1, 2, 3], 'False': true}              │
└────────────────────────────────────────────────────────────────────┘
```
> 字典中的每个 `key` 都会被转换为字符串。

### `tuple`

`tuple` 默认转换为 `LIST`，当它被用于构造 `STRUCT` 类型的 Value 对象时，会转换为 `STRUCT`。

### `numpy.ndarray` 和 `numpy.datetime64`

`ndarray` 和 `datetime64` 通过调用 `tolist()` 并转换其结果进行转换。

## 结果转换：DuckDB 结果到 Python

DuckDB 的 Python 客户端提供了多种额外的方法，可用于高效地获取数据。

### NumPy

* `fetchnumpy()` 以 NumPy 数组字典的形式获取数据

### Pandas

* `df()` 以 Pandas DataFrame 的形式获取数据
* `fetchdf()` 是 `df()` 的别名
* `fetch_df()` 是 `df()` 的别名
* `fetch_df_chunk(vector_multiple)` 将结果的一部分获取到 DataFrame 中。每个 chunk 返回的行数是向量大小（默认为 2048）乘以 `vector_multiple`（默认为 1）。

### Apache Arrow

* `arrow()` 以 [Arrow 表](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html) 的形式获取数据
* `fetch_arrow_table()` 是 `arrow()` 的别名
* `fetch_record_batch(chunk_size)` 返回 [Arrow 记录批次读取器](https://arrow.apache.org/docs/python/generated/pyarrow.ipc.RecordBatchStreamReader.html)，每个批次包含 `chunk_size` 行

### Polars

* `pl()` 以 Polars DataFrame 的形式获取数据

### 示例

以下是一些使用这些功能的示例。更多信息请参见 [Python 指南]({% link docs/stable/guides/overview.md %}#python-client)。

以 Pandas DataFrame 的形式获取：

```python
df = con.execute("SELECT * FROM items").fetchdf()
print(df)
```

```text
       item   value  count
0     jeans    20.0      1
1    hammer    42.2      2
2    laptop  2000.0      1
3  chainsaw   500.0     10
4    iphone   300.0      2
```

以 NumPy 数组字典的形式获取：

```python
arr = con.execute("SELECT * FROM items").fetchnumpy()
print(arr)
```

```text
{'item': masked_array(data=['jeans', 'hammer', 'laptop', 'chainsaw', 'iphone'],
             mask=[False, False, False, False, False],
       fill_value='?',
            dtype=object), 'value': masked_array(data=[20.0, 42.2, 2000.0, 500.0, 300.0],
             mask=[False, False, False, False, False],
       fill_value=1e+20), 'count': masked_array(data=[1, 2, 1, 10, 2],
             mask=[False, False, False, False, False],
       fill_value=999999,
            dtype=int32)}
```

以 Arrow 表的形式获取。转换为 Pandas 仅用于美观打印：

```python
tbl = con.execute("SELECT * FROM items").fetch_arrow_table()
print(tbl.to_pandas())
```

```text
       item    value  count
0     jeans    20.00      1
1    hammer    42.20      2
2    laptop  2000.00      1
3  chainsaw   500.00     10
4    iphone   300.00      2
```