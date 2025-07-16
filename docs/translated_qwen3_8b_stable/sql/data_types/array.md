---
---
layout: docu
redirect_from:
- /docs/sql/data_types/array
title: 数组类型
---

`ARRAY` 列用于存储固定大小的数组。列中的所有字段必须具有相同的长度和相同的基础类型。数组通常用于存储数字数组，但也可以包含任何统一的数据类型，包括 `ARRAY`、[`LIST`]({% link docs/stable/sql/data_types/list.md %}) 和 [`STRUCT`]({% link docs/stable/sql/data_types/struct.md %}) 类型。

数组可用于存储诸如 [词嵌入](https://en.wikipedia.org/wiki/Word_embedding) 或图像嵌入之类的向量。

要存储可变长度列表，请使用 [`LIST` 类型]({% link docs/stable/sql/data_types/list.md %})。有关嵌套数据类型的比较，请参阅 [数据类型概览]({% link docs/stable/sql/data_types/overview.md %}).

> PostgreSQL 中的 `ARRAY` 类型允许可变长度字段。DuckDB 的 `ARRAY` 类型是固定长度的。

## 创建数组

可以使用 [`array_value(expr, ...)` 函数]({% link docs/stable/sql/functions/array.md %}#array_valueindex) 创建数组。

使用 `array_value` 函数进行构造：

```sql
SELECT array_value(1, 2, 3);
```

您始终可以隐式地将数组转换为列表（并使用列表函数，如 `list_extract`、`[i]`）：

```sql
SELECT array_value(1, 2, 3)[2];
```

您可以将列表转换为数组（维度必须匹配）：

```sql
SELECT [3, 2, 1]::INTEGER[3];
```

数组可以嵌套：

```sql
SELECT array_value(array_value(1, 2), array_value(3, 4), array_value(5, 6));
```

数组可以存储结构体：

```sql
SELECT array_value({'a': 1, 'b': 2}, {'a': 3, 'b': 4});
```

## 定义数组字段

可以使用 `⟨TYPE_NAME⟩[⟨LENGTH⟩]`{:.language-sql .highlight} 语法创建数组。例如，要创建一个存储 3 个整数的数组字段，请运行：

```sql
CREATE TABLE array_table (id INTEGER, arr INTEGER[3]);
INSERT INTO array_table VALUES (10, [1, 2, 3]), (20, [4, 5, 6]);
```

## 从数组中检索值

可以使用括号和切片符号，或通过 [列表函数]({% link docs/stable/sql/functions/list.md %}#list-functions) 如 `list_extract` 和 `array_extract` 从数组中检索一个或多个值。使用 [定义数组字段](#defining-an-array-field) 中的示例。

以下查询用于提取数组的第二个元素，它们是等效的：

```sql
SELECT id, arr[1] AS element FROM array_table;
SELECT id, list_extract(arr, 1) AS element FROM array_table;
SELECT id, array_extract(arr, 1) AS element FROM array_table;
```

| id | element |
|---:|--------:|
| 10 | 1       |
| 20 | 4       |

使用切片符号返回一个 `LIST`：

```sql
SELECT id, arr[1:2] AS elements FROM array_table;
```

| id | elements |
|---:|----------|
| 10 | [1, 2]   |
| 20 | [4, 5]   |

## 函数

所有 [`LIST` 函数]({% link docs/stable/sql/functions/list.md %}) 都适用于 `ARRAY` 类型。此外，还支持一些 `ARRAY` 原生函数。
请参阅 [`ARRAY` 函数]({% link docs/stable/sql/functions/array.md %}#array-native-functions).

## 示例

创建示例数据：

```sql
CREATE TABLE x (i INTEGER, v FLOAT[3]);
CREATE TABLE y (i INTEGER, v FLOAT[3]);
INSERT INTO x VALUES (1, array_value(1.0::FLOAT, 2.0::FLOAT, 3.0::FLOAT));
INSERT INTO y VALUES (1, array_value(2.0::FLOAT, 3.0::FLOAT, 4.0::FLOAT));
```

计算叉积：

```sql
SELECT array_cross_product(x.v, y.v)
FROM x, y
WHERE x.i = y.i;
```

计算余弦相似度：

```sql
SELECT array_cosine_similarity(x.v, y.v)
FROM x, y
WHERE x.i = y.i;
```

## 排序

`ARRAY` 实例的排序使用字典序定义。`NULL` 值大于所有其他值，并且彼此相等。

## 参见

如需更多函数，请参阅 [列表函数]({% link docs/stable/sql/functions/list.md %}).