---
---
layout: docu
redirect_from:
- /docs/sql/data_types/list
title: 列表类型
---

`LIST` 列用于编码值的列表。列中的字段可以具有不同长度的值，但它们必须具有相同的底层类型。`LIST` 通常用于存储数字数组，但也可以包含任何统一的数据类型，包括其他 `LIST` 和 `STRUCT`。

`LIST` 与 PostgreSQL 的 `ARRAY` 类型类似。DuckDB 使用 `LIST` 术语，但为了 PostgreSQL 兼容性，提供了一些 [`array_` 函数]({% link docs/stable/sql/functions/list.md %}).

有关嵌套数据类型的比较，请参阅 [数据类型概述]({% link docs/stable/sql/data_types/overview.md %}).

> 对于存储固定长度的列表，DuckDB 使用 [`ARRAY` 类型]({% link docs/stable/sql/data_types/array.md %}).

## 创建列表

可以使用 [`list_value(expr, ...)`]({% link docs/stable/sql/functions/list.md %}#list_valueany-) 函数或等效的方括号表示法 `[expr, ...]` 来创建列表。表达式可以是常量或任意表达式。要从表列创建列表，请使用 [`list`]({% link docs/stable/sql/functions/aggregates.md %}#general-aggregate-functions) 聚合函数。

整数列表：

```sql
SELECT [1, 2, 3];
```

包含 `NULL` 值的字符串列表：

```sql
SELECT ['duck', 'goose', NULL, 'heron'];
```

包含 `NULL` 值的列表列表：

```sql
SELECT [['duck', 'goose', 'heron'], NULL, ['frog', 'toad'], []];
```

使用 `list_value` 函数创建列表：

```sql
SELECT list_value(1, 2, 3);
```

创建一个包含 `INTEGER` 列表列和 `VARCHAR` 列表列的表：

```sql
CREATE TABLE list_table (int_list INTEGER[], varchar_list VARCHAR[]);
```

## 从列表中检索

可以通过使用方括号和切片表示法，或通过 [列表函数]({% link docs/stable/sql/functions/list.md %}) 如 `list_extract` 来检索列表中的一个或多个值。为了与将列表称为数组的系统兼容，提供了多个等效函数作为别名。例如，函数 `array_slice`。

<div class="monospace_table"></div>

<!-- markdownlint-disable MD052 -->

| 示例                                  | 结果     |
|:-----------------------------------------|:-----------|
| SELECT ['a', 'b', 'c'][3]                | 'c'        |
| SELECT ['a', 'b', 'c'][-1]               | 'c'        |
| SELECT ['a', 'b', 'c'][2 + 1]            | 'c'        |
| SELECT list_extract(['a', 'b', 'c'], 3)  | 'c'        |
| SELECT ['a', 'b', 'c'][1:2]              | ['a', 'b'] |
| SELECT ['a', 'b', 'c'][:2]               | ['a', 'b'] |
| SELECT ['a', 'b', 'c'][-2:]              | ['b', 'c'] |
| SELECT list_slice(['a', 'b', 'c'], 2, 3) | ['b', 'c'] |

<!-- markdownlint-disable MD052 -->

## 比较和排序

`LIST` 类型可以使用所有 [比较运算符]({% link docs/stable/sql/expressions/comparison_operators.md %}) 进行比较。
这些比较可以用于 [逻辑表达式]({% link docs/stable/sql/expressions/logical_operators.md %})，例如 `WHERE` 和 `HAVING` 子句，并返回 [`BOOLEAN` 值]({% link docs/stable/sql/data_types/boolean.md %}).

`LIST` 的排序通过以下规则按位置定义，其中 `min_len = min(len(l1), len(l2))`.

* **相等。** 如果对于每个 `i` 在 `[1, min_len]` 中，`l1[i] = l2[i]`，则 `l1` 和 `l2` 相等。
* **小于。** 对于 `[1, min_len]` 中的第一个索引 `i`，其中 `l1[i] != l2[i]`：
  如果 `l1[i] < l2[i]`，则 `l1` 小于 `l2`。

`NULL` 值的比较遵循 PostgreSQL 的语义。
在平局时使用较低的嵌套级别进行区分。

以下查询返回 `true` 作为比较结果。

```sql
SELECT [1, 2] < [1, 3] AS result;
```

```sql
SELECT [[1], [2, 4, 5]] < [[2]] AS result;
```

```sql
SELECT [ ] < [1] AS result;
```

这些查询返回 `false`。

```sql
SELECT [ ] < [ ] AS result;
```

```sql
SELECT [1, 2] < [1] AS result;
```

这些查询返回 `NULL`。

```sql
SELECT [1, 2] < [1, NULL, 4] AS result;
```

## 函数

参见 [列表函数]({% link docs/stable/sql/functions/list.md %}).