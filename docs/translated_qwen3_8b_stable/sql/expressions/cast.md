---
---
layout: docu
railroad: expressions/cast.js
redirect_from:
- /docs/sql/expressions/cast
title: 类型转换
---

<div id="rrdiagram"></div>

类型转换指的是将一个特定数据类型中的值转换为另一个对应数据类型的值的操作。
类型转换可以是隐式或显式的。此处描述的语法执行的是显式转换。有关类型转换的更多信息，请参见[类型转换页面]({% link docs/stable/sql/data_types/typecasting.md %}).

## 显式类型转换

显式类型转换的标准 SQL 语法是 `CAST(expr AS TYPENAME)`，其中 `TYPENAME` 是 [DuckDB 数据类型]({% link docs/stable/sql/data_types/overview.md %}) 的名称（或别名）。DuckDB 还支持 PostgreSQL 中也存在的简写形式 `expr::TYPENAME`。

```sql
SELECT CAST(i AS VARCHAR) AS i
FROM generate_series(1, 3) tbl(i);
```

| i |
|---|
| 1 |
| 2 |
| 3 |

```sql
SELECT i::DOUBLE AS i
FROM generate_series(1, 3) tbl(i);
```

|  i  |
|----:|
| 1.0 |
| 2.0 |
| 3.0 |

### 类型转换规则

并非所有类型转换都是可行的。例如，无法将 `INTEGER` 转换为 `DATE`。当转换无法成功进行时，转换也可能抛出错误。例如，尝试将字符串 `'hello'` 转换为 `INTEGER` 会导致错误。

```sql
SELECT CAST('hello' AS INTEGER);
```

```console
转换错误：
无法将字符串 'hello' 转换为 INT32
```

转换的具体行为取决于源类型和目标类型。例如，当从 `VARCHAR` 转换到其他任何类型时，会尝试将字符串转换。

### `TRY_CAST`

当希望不抛出错误，而是返回 `NULL` 值时，可以使用 `TRY_CAST`。`TRY_CAST` 从不会抛出错误，如果转换不可行，它将返回 `NULL`。

```sql
SELECT TRY_CAST('hello' AS INTEGER) AS i;
```

|  i   |
|------|
| NULL |

## `cast_to_type` 函数

`cast_to_type` 函数允许根据另一个列的类型，将表达式转换为相应的类型。
例如：

```sql
SELECT cast_to_type('42', NULL::INTEGER) AS result;
```

```text
┌───────┐
│  res  │
│ int32 │
├───────┤
│  42   │
└───────┘
```

该函数在 [宏]({% link docs/stable/guides/snippets/sharing_macros.md %}) 中特别有用，因为它允许你维护类型。这有助于创建可以处理不同类型的通用宏。例如，以下宏在输入是 `INTEGER` 时向数字添加一个值：

```sql
CREATE TABLE tbl(i INT, s VARCHAR);
INSERT INTO tbl VALUES (42, 'hello world');

CREATE MACRO conditional_add(col, nr) AS
    CASE
        WHEN typeof(col) == 'INTEGER' THEN cast_to_type(col::INTEGER + nr, col)
        ELSE col
    END;
SELECT conditional_add(COLUMNS(*), 100) FROM tbl;
```

```text
┌───────┬─────────────┐
│   i   │      s      │
│ int32 │   varchar   │
├───────┼─────────────┤
│  142  │ hello world │
└───────┴─────────────┘
```

请注意，`CASE` 语句需要在所有代码路径中返回相同的类型。我们可以通过对输入列进行所需类型的转换来执行任何加法操作——但我们需要将加法结果转换回源类型，以使绑定正常工作。