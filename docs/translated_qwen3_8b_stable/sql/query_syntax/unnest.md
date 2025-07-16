---
---
layout: docu
redirect_from:
- /docs/sql/query_syntax/unnest
title: 展开
---

## 示例

展开列表，生成 3 行 (1, 2, 3)：

```sql
SELECT unnest([1, 2, 3]);
```

展开结构体，生成两列 (a, b)：

```sql
SELECT unnest({'a': 42, 'b': 84});
```

递归展开结构体列表：

```sql
SELECT unnest([{'a': 42, 'b': 84}, {'a': 100, 'b': NULL}], recursive := true);
```

使用 `max_depth` 限制递归展开的深度：

```sql
SELECT unnest([[[1, 2], [3, 4]], [[5, 6], [7, 8, 9], []], [[10, 11]]], max_depth := 2);
```

`unnest` 特殊函数用于展开列表或结构体一层。该函数可以像普通标量函数一样使用，但只能在 `SELECT` 子句中使用。调用 `unnest` 并传入 `recursive` 参数，可以展开多层列表和结构体。使用 `max_depth` 参数可以限制展开的深度（默认假设为递归展开）。

### 展开列表

展开列表，生成 3 行 (1, 2, 3)：

```sql
SELECT unnest([1, 2, 3]);
```

展开列表，生成 3 行 ((1, 10), (2, 10), (3, 10))：

```sql
SELECT unnest([1, 2, 3]), 10;
```

展开两个大小不同的列表，生成 3 行 ((1, 10), (2, 11), (3, NULL))：

```sql
SELECT unnest([1, 2, 3]), unnest([10, 11]);
```

从子查询展开列表列：

```sql
SELECT unnest(l) + 10 FROM (VALUES ([1, 2, 3]), ([4, 5])) tbl(l);
```

空结果：

```sql
SELECT unnest([]);
```

空结果：

```sql
SELECT unnest(NULL);
```

对列表使用 `unnest` 会为每个列表项生成一行。同一 `SELECT` 子句中的普通标量表达式会在每行中重复。当在同一个 `SELECT` 子句中展开多个列表时，列表会并排展开。如果一个列表比另一个长，较短的列表会用 `NULL` 值填充。

空列表和 `NULL` 列表都会展开为零行。

### 展开结构体

展开结构体，生成两列 (a, b)：

```sql
SELECT unnest({'a': 42, 'b': 84});
```

展开结构体，生成两列 (a, b)：

```sql
SELECT unnest({'a': 42, 'b': {'x': 84}});
```

对结构体使用 `unnest` 会为结构体中的每个条目生成一列。

### 递归展开

递归展开列表列表，生成 5 行 (1, 2, 3, 4, 5)：

```sql
SELECT unnest([[1, 2, 3], [4, 5]], recursive := true);
```

递归展开结构体列表，生成两列的两行 (a, b)：

```sql
SELECT unnest([{'a': 42, 'b': 84}, {'a': 100, 'b': NULL}], recursive := true);
```

展开结构体，生成两列 (a, b)：

```sql
SELECT unnest({'a': [1, 2, 3], 'b': 88}, recursive := true);
```

调用 `unnest` 并传入 `recursive` 设置会完全展开列表，然后完全展开结构体。这可以用于完全扁平化包含多层列表或结构体列表的列。请注意，结构体内的列表不会被展开。

### 设置展开的最大深度

`max_depth` 参数允许限制递归展开的最大深度（默认假设为递归展开，因此无需单独指定）。
例如，将 `max_depth` 设置为 2 会生成以下结果：

```sql
SELECT unnest([[[1, 2], [3, 4]], [[5, 6], [7, 8, 9], []], [[10, 11]]], max_depth := 2) AS x;
```

|     x     |
|-----------|
| [1, 2]    |
| [3, 4]    |
| [5, 6]    |
| [7, 8, 9] |
| []        |
| [10, 11]  |

同时，将 `max_depth` 设置为 3 会生成以下结果：

```sql
SELECT unnest([[[1, 2], [3, 4]], [[5, 6], [7, 8, 9], []], [[10, 11]]], max_depth := 3) AS x;
```

| x  |
|---:|
| 1  |
| 2  |
| 3  |
| 4  |
| 5  |
| 6  |
| 7  |
| 8  |
| 9  |
| 10 |
| 11 |

### 跟踪列表项的位置

为了跟踪原始列表中每个项的位置，`unnest` 可以与 [`generate_subscripts`]({% link docs/stable/sql/functions/list.md %}#generate_subscripts) 一起使用：

```sql
SELECT unnest(l) AS x, generate_subscripts(l, 1) AS index
FROM (VALUES ([1, 2, 3]), ([4, 5])) tbl(l);
```

| x | index |
|--:|------:|
| 1 | 1     |
| 2 | 2     |
| 3 | 3     |
| 4 | 1     |
| 5 | 2     |