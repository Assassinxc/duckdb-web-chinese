---
---
layout: docu
redirect_from:
- /docs/api/python/function
- /docs/api/python/function/
- /docs/clients/python/function
title: Python 函数 API
---

您可以从 Python 函数创建一个 DuckDB 用户定义函数 (UDF)，以便在 SQL 查询中使用。
与常规 [函数]({% link docs/stable/sql/functions/overview.md %}) 类似，它们需要具有名称、返回类型和参数类型。

以下是一个使用调用第三方库的 Python 函数的示例。

```python
import duckdb
from duckdb.typing import *
from faker import Faker

def generate_random_name():
    fake = Faker()
    return fake.name()

duckdb.create_function("random_name", generate_random_name, [], VARCHAR)
res = duckdb.sql("SELECT random_name()").fetchall()
print(res)
```

```text
[('Gerald Ashley',)]
```

## 创建函数

要注册一个 Python UDF，可以使用 DuckDB 连接的 `create_function` 方法。以下是语法：

```python
import duckdb
con = duckdb.connect()
con.create_function(name, function, parameters, return_type)
```

`create_function` 方法接受以下参数：

1. `name`：表示 UDF 在连接目录中的唯一名称的字符串。
2. `function`：您希望注册为 UDF 的 Python 函数。
3. `parameters`：标量函数可以作用于一个或多个列。此参数接收用作输入的列类型列表。
4. `return_type`：标量函数每行返回一个元素。此参数指定函数的返回类型。
5. `type`（可选）：DuckDB 支持内置 Python 类型和 PyArrow 表。默认情况下，假定使用内置类型，但您可以指定 `type = 'arrow'` 来使用 PyArrow 表。
6. `null_handling`（可选）：默认情况下，`NULL` 值会自动处理为 `NULL`-in `NULL`-out。用户可以通过设置 `null_handling = 'special'` 来指定 `NULL` 值的期望行为。
7. `exception_handling`（可选）：默认情况下，当 Python 函数抛出异常时，它会重新抛出该异常。用户可以通过将此参数设置为 `'return_null'` 来禁用此行为，并返回 `NULL`。
8. `side_effects`（可选）：默认情况下，函数预期对于相同的输入会产生相同的结果。如果函数的结果受到任何形式的随机性的影响，必须将 `side_effects` 设置为 `True`。

要注销一个 UDF，可以使用 `remove_function` 方法并传入 UDF 名称：

```python
con.remove_function(name)
```

### 使用部分函数

DuckDB UDF 也可以使用 [Python 部分函数](https://docs.python.org/3/library/functools.html#functools.partial) 创建。

在下面的例子中，我们展示了如何使用自定义日志器返回执行时间的 ISO 格式，总是跟随在 UDF 创建时传递的参数和函数调用提供的输入参数的拼接：

```python
from datetime import datetime
import duckdb
import functools


def get_datetime_iso_format() -> str:
    return datetime.now().isoformat()


def logger_udf(func, arg1: str, arg2: int) -> str:
    return ' '.join([func(), arg1, str(arg2)])
    
    
with duckdb.connect() as con:
    con.sql("select * from range(10) tbl(id)").to_table("example_table")
    
    con.create_function(
        'custom_logger',
        functools.partial(logger_udf, get_datetime_iso_format, 'logging data')
    )
    rel = con.sql("SELECT custom_logger(id) from example_table;")
    rel.show()

    con.create_function(
        'another_custom_logger',
        functools.partial(logger_udf, get, ':')
    )
    rel = con.sql("SELECT another_custom_logger(id) from example_table;")
    rel.show()
```

```text
┌───────────────────────────────────────────┐
│             custom_logger(id)             │
│                  varchar                  │
├───────────────────────────────────────────┤
│ 2025-03-27T12:07:56.811251 logging data 0 │
│ 2025-03-27T12:07:56.811264 logging data 1 │
│ 2025-03-27T12:07:56.811266 logging data 2 │
│ 2025-03-27T12:07:56.811268 logging data 3 │
│ 2025-03-27T12:07:56.811269 logging data 4 │
│ 2025-03-27T12:07:56.811270 logging data 5 │
│ 2025-03-27T12:07:56.811271 logging data 6 │
│ 2025-03-27T12:07:56.811272 logging data 7 │
│ 2025-03-27T12:07:56.811274 logging data 8 │
│ 2025-03-27T12:07:56.811275 logging data 9 │
├───────────────────────────────────────────┤
│                  10 rows                  │
└───────────────────────────────────────────┘

┌────────────────────────────────┐
│   another_custom_logger(id)    │
│            varchar             │
├────────────────────────────────┤
│ 2025-03-27T12:07:56.812106 : 0 │
│ 2025-03-27T12:07:56.812116 : 1 │
│ 2025-03-27T12:07:56.812118 : 2 │
│ 2025-03-27T12:07:56.812119 : 3 │
│ 2025-03-27T12:07:56.812121 : 4 │
│ 2025-03-27T12:07:56.812122 : 5 │
│ 2025-03-27T12:07:56.812123 : 6 │
│ 2025-03-27T12:07:56.812124 : 7 │
│ 2025-03-27T12:07:56.812126 : 8 │
│ 2025-03-27T12:07:56.812127 : 9 │
├────────────────────────────────┤
│            10 rows             │
└────────────────────────────────┘
```

## 类型注解

当函数具有类型注解时，通常可以省略所有可选参数。
使用 `DuckDBPyType`，我们可以隐式地将许多已知类型转换为 DuckDB 的类型系统。
例如：

```python
import duckdb

def my_function(x: int) -> str:
    return x

duckdb.create_function("my_func", my_function)
print(duckdb.sql("SELECT my_func(42)"))
```

```text
┌─────────────┐
│ my_func(42) │
│   varchar   │
├─────────────┤
│ 42          │
└─────────────┘
```

如果只能推断参数列表的类型，您需要将 `parameters` 设置为 `None`。

## `NULL` 处理

默认情况下，当函数接收到一个 `NULL` 值时，它会立即返回 `NULL`，这是默认的 `NULL` 处理的一部分。
当不希望如此时，您需要显式地将此参数设置为 `"special"`。

```python
import duckdb
from duckdb.typing import *

def dont_intercept_null(x):
    return 5

duckdb.create_function("dont_intercept", dont_intercept_null, [BIGINT], BIGINT)
res = duckdb.sql("SELECT dont_intercept(NULL)").fetchall()
print(res)
```

```text
[(None,)]
```

使用 `null_handling="special"`：

```python
import duckdb
from duckdb.typing import *

def dont_intercept_null(x):
    return 5

duckdb.create_function("dont_intercept", dont_intercept_null, [BIGINT], BIGINT, null_handling="special")
res = duckdb.sql("SELECT dont_intercept(NULL)").fetchall()
print(res)
```

```text
[(5,)]
```

> 当函数可以返回 `NULL` 时，始终使用 `null_handling="special"`。

```python
import duckdb
from duckdb.typing import VARCHAR


def return_str_or_none(x: str) -> str | None:
    if not x:
        return None
    
    return x

duckdb.create_function(
    "return_str_or_none",
    return_str_or_none,
    [VARCHAR],
    VARCHAR,
    null_handling="special"
)
res = duckdb.sql("SELECT return_str_or_none('')").fetchall()
print(res)
```

```text
[(None,)]
```

## 异常处理

默认情况下，当 Python 函数抛出异常时，我们会将其转发（重新抛出）。
如果您希望禁用此行为，并返回 `NULL`，则需要将此参数设置为 `"return_null"`。

```python
import duckdb
from duckdb.typing import *

def will_throw():
    raise ValueError("ERROR")

duckdb.create_function("throws", will_throw, [], BIGINT)
try:
    res = duckdb.sql("SELECT throws()").fetchall()
except duckdb.InvalidInputException as e:
    print(e)

duckdb.create_function("doesnt_throw", will_throw, [], BIGINT, exception_handling="return_null")
res = duckdb.sql("SELECT doesnt_throw()").fetchall()
print(res)
```

```console
Invalid Input Error: Python exception occurred while executing the UDF: ValueError: ERROR

At:
  ...(5): will_throw
  ...(9): <module>
```

```text
[(None,)]
```

## 副作用

默认情况下，DuckDB 会假设创建的函数是一个 *纯* 函数，这意味着当给予相同的输入时，它会产生相同的输出。
如果您的函数不遵循这个规则，例如，您的函数使用了随机性，那么您需要将此函数标记为具有 `side_effects`。

例如，该函数每次调用都会生成一个新的计数。

```python
def count() -> int:
    old = count.counter;
    count.counter += 1
    return old

count.counter = 0
```

如果我们创建这个函数而不标记其具有副作用，结果将是以下内容：

```python
con = duckdb.connect()
con.create_function("my_counter", count, side_effects=False)
res = con.sql("SELECT my_counter() FROM range(10)").fetchall()
print(res)
```

```text
[(0,), (0,), (0,), (0,), (0,), (0,), (0,), (0,), (0,), (0,)]
```

显然，当添加 `side_effects=True` 时，结果是我们期望的：

```python
con.remove_function("my_counter")
count.counter = 0
con.create_function("my_counter", count, side_effects=True)
res = con.sql("SELECT my_counter() FROM range(10)").fetchall()
print(res)
```

```text
[(0,), (1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,)]
```

## Python 函数类型

目前支持两种函数类型，`native`（默认）和 `arrow`。

### Arrow

如果函数预计会接收 Arrow 数组，请将 `type` 参数设置为 `'arrow'`。

这将让系统知道要向函数提供最多 `STANDARD_VECTOR_SIZE` 个元组的 Arrow 数组，并且期望函数返回相同数量的元组数组。

### Native

当函数类型设置为 `native` 时，函数会每次提供一个元组，并期望返回一个值。
这在与不基于 Arrow 运行的 Python 库（如 `faker`）交互时可能很有用：

```python
import duckdb

from duckdb.typing import *
from faker import Faker

def random_date():
    fake = Faker()
    return fake.date_between()

duckdb.create_function("random_date", random_date, [], DATE, type="native")
res = duckdb.sql("SELECT random_date()").fetchall()
print(res)
```

```text
[(datetime.date(2019, 5, 15),)]
```