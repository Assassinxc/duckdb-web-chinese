---
---
layout: docu
redirect_from:
- /docs/api/python/expression
- /docs/api/python/expression/
- /docs/clients/python/expression
title: 表达式 API
---

`Expression` 类表示一个 [表达式]({% link docs/stable/sql/expressions/overview.md %}) 的实例。

## 为什么使用表达式 API？

使用此 API 可以动态构建表达式，这些表达式通常由解析器从查询字符串中创建。
这允许您跳过该步骤，并对使用的表达式进行更精细的控制。

以下是目前通过 API 支持的表达式列表。

## 列表达式

此表达式通过名称引用列。

```python
import duckdb
import pandas as pd

df = pd.DataFrame({
    'a': [1, 2, 3, 4],
    'b': [True, None, False, True],
    'c': [42, 21, 13, 14]
})
```

选择单个列：

```python
col = duckdb.ColumnExpression('a')
duckdb.df(df).select(col).show()
```

```text
┌───────┐
│   a   │
│ int64 │
├───────┤
│     1 │
│     2 │
│     3 │
│     4 │
└───────┘
```

选择多个列：

```python
col_list = [
        duckdb.ColumnExpression('a') * 10,
        duckdb.ColumnExpression('b').isnull(),
        duckdb.ColumnExpression('c') + 5
    ]
duckdb.df(df).select(*col_list).show()
```

```text
┌──────────┬─────────────┬─────────┐
│ (a * 10) │ (b IS NULL) │ (c + 5) │
│  int64   │   boolean   │  int64  │
├──────────┼─────────────┼─────────┤
│       10 │ false       │      47 │
│       20 │ true        │      26 │
│       30 │ false       │      18 │
│       40 │ false       │      19 │
└──────────┴─────────────┴─────────┘
```

## 星号表达式

此表达式选择输入源的所有列。

可选地，可以提供一个 `exclude` 列表来过滤掉表中的列。
该 `exclude` 列表可以包含字符串或表达式。

```python
import duckdb
import pandas as pd

df = pd.DataFrame({
    'a': [1, 2, 3, 4],
    'b': [True, None, False, True],
    'c': [42, 21, 13, 14]
})

star = duckdb.StarExpression(exclude = ['b'])
duckdb.df(df).select(star).show()
```

```text
┌───────┬───────┐
│   a   │   c   │
│ int64 │ int64 │
├───────┼───────┤
│     1 │    42 │
│     2 │    21 │
│     3 │    13 │
│     4 │    14 │
└───────┴───────┘
```

## 常量表达式

此表达式包含一个值。

```python
import duckdb
import pandas as pd

df = pd.DataFrame({
    'a': [1, 2, 3, 4],
    'b': [True, None, False, True],
    'c': [42, 21, 13, 14]
})

const = duckdb.ConstantExpression('hello')
duckdb.df(df).select(const).show()
```

```text
┌─────────┐
│ 'hello' │
│ varchar │
├─────────┤
│ hello   │
│ hello   │
│ hello   │
│ hello   │
└─────────┘
```

## Case 表达式

此表达式包含一个 `CASE WHEN (...) THEN (...) ELSE (...) END` 表达式。
默认情况下 `ELSE` 是 `NULL`，可以使用 `.else(value = ...)` 设置。
可以通过 `.when(condition = ..., value = ...)` 添加额外的 `WHEN (...) THEN (...)` 块。

```python
import duckdb
import pandas as pd
from duckdb import (
    ConstantExpression,
    ColumnExpression,
    CaseExpression
)

df = pd.DataFrame({
    'a': [1, 2, 3, 4],
    'b': [True, None, False, True],
    'c': [42, 21, 13, 14]
})

hello = ConstantExpression('hello')
world = ConstantExpression('world')

case = \
    CaseExpression(condition = ColumnExpression('b') == False, value = world) \
    .otherwise(hello)
duckdb.df(df).select(case).show()
```

```text
┌──────────────────────────────────────────────────────────┐
│ CASE  WHEN ((b = false)) THEN ('world') ELSE 'hello' END │
│                         varchar                          │
├──────────────────────────────────────────────────────────┤
│ hello                                                    │
│ hello                                                    │
│ world                                                    │
│ hello                                                    │
└──────────────────────────────────────────────────────────┘
```

## 函数表达式

此表达式包含一个函数调用。
可以通过提供函数名和任意数量的表达式作为参数来构建。

```python
import duckdb
import pandas as pd
from duckdb import (
    ConstantExpression,
    ColumnExpression,
    FunctionExpression
)

df = pd.DataFrame({
    'a': [1, 2, 3, 4],
    'b': [True, None, False, True],
    'c': [42, 21, 13, 14]
})

multiply_by_2 = FunctionExpression('multiply', ColumnExpression('a'), ConstantExpression(2))
duckdb.df(df).select(multiply_by_2).show()
```

```text
┌────────────────┐
│ multiply(a, 2) │
│     int64      │
├────────────────┤
│              2 │
│              4 │
│              6 │
│              8 │
└────────────────┘
```

## SQL 表达式

此表达式包含任何有效的 SQL 表达式。

```python
import duckdb
import pandas as pd

from duckdb import SQLExpression

df = pd.DataFrame({
    'a': [1, 2, 3, 4],
    'b': [True, None, False, True],
    'c': [42, 21, 13, 14]
})

duckdb.df(df).filter(
    SQLExpression("b is true")
).select(
    SQLExpression("a").alias("selecting_column_a"),
    SQLExpression("case when a = 1 then 1 else 0 end").alias("selecting_case_expression"),
    SQLExpression("1").alias("constant_numeric_column"),
    SQLExpression("'hello'").alias("constant_text_column")
).aggregate(
    aggr_expr=[
        SQLExpression("SUM(selecting_column_a)").alias("sum_a"), 
        "selecting_case_expression" , 
        "constant_numeric_column", 
        "constant_text_column"
    ],
).show()
```

```text
┌────────┬───────────────────────────┬─────────────────────────┬──────────────────────┐
│ sum_a  │ selecting_case_expression │ constant_numeric_column │ constant_text_column │
│ int128 │           int32           │          int32          │       varchar        │
├────────┼───────────────────────────┼─────────────────────────┼──────────────────────┤
│      4 │                         0 │                       1 │ hello                │
│      1 │                         1 │                       1 │ hello                │
└────────┴───────────────────────────┴─────────────────────────┴──────────────────────┘
```

## 常见操作

`Expression` 类还包含许多可用于任何 `Expression` 类型的操作。

| 操作                      | 描述                                                                                                                 |
|---------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| `.alias(name: str)`       | 对表达式应用别名                                                                                          |
| `.cast(type: DuckDBPyType)` | 对表达式应用指定类型的转换                                                                       |
| `.isin(*exprs: Expression)` | 创建一个 [`IN` 表达式]({% link docs/stable/sql/expressions/in.md %}#in) 与提供的表达式列表进行比较         |
| `.isnotin(*exprs: Expression)` | 创建一个 [`NOT IN` 表达式]({% link docs/stable/sql/expressions/in.md %}#not-in) 与提供的表达式列表进行比较  |
| `.isnotnull()`            | 检查表达式是否不为 `NULL`                                                                                 |
| `.isnull()`               | 检查表达式是否为 `NULL`                                                                                     |

### 排序操作

当表达式传递给 `DuckDBPyRelation.order()` 时，可以应用以下排序操作。

| 操作                      | 描述                                                                        |
|---------------------------|------------------------------------------------------------------------------|
| `.asc()`                  | 表示此表达式应按升序排序                                                     |
| `.desc()`                 | 表示此表达式应按降序排序                                                     |
| `.nulls_first()`          | 表示此表达式的空值应优先于非空值                                             |
| `.nulls_last()`           | 表示此表达式的空值应出现在非空值之后                                          |