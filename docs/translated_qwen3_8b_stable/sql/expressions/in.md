---
---
layout: docu
railroad: expressions/in.js
redirect_from:
- /docs/sql/expressions/in
title: IN 运算符
---

`IN` 运算符检查左侧表达式是否包含在右侧（RHS）的 _集合_ 中。  
右侧支持的集合包括元组、列表、映射和返回单列的子查询。

<div id="rrdiagram"></div>

## `IN (val1, val2, ...)` (元组)

`IN` 运算符在元组 `(val1, val2, ...)` 上返回 `true` 如果表达式出现在 RHS 中，返回 `false` 如果表达式不在 RHS 中且 RHS 中没有 `NULL` 值，或返回 `NULL` 如果表达式不在 RHS 中且 RHS 中有 `NULL` 值。

```sql
SELECT 'Math' IN ('CS', 'Math');
```

```text
true
```

```sql
SELECT 'English' IN ('CS', 'Math');
```

```text
false
```

```sql
SELECT 'Math' IN ('CS', 'Math', NULL);
```

```text
true
```

```sql
SELECT 'English' IN ('CS', 'Math', NULL);
```

```text
NULL
```

## `IN [val1, val2, ...]` (列表)

`IN` 运算符按照 Python 中的语义在列表上进行操作。  
与 [`IN tuple` 运算符](#in-val1-val2--tuple) 不同，表达式右侧的 `NULL` 值不会影响结果：

```sql
SELECT 'Math' IN ['CS', 'Math', NULL];
```

```text
true
```

```sql
SELECT 'English' IN ['CS', 'Math', NULL];
```

```text
false
```

## `IN` 映射

`IN` 运算符按照 Python 中的语义在 [映射]({% link docs/stable/sql/data_types/map.md %}) 上进行操作，即检查键（而非值）是否存在：

```sql
SELECT 'key1' IN MAP {'key1': 50, 'key2': 75};
```

```text
true
```

```sql
SELECT 'key3' IN MAP {'key1': 50, 'key2': 75};
```

```text
false
```

## `IN` 子查询

`IN` 运算符可以与返回单列的 [子查询]({% link docs/stable/sql/expressions/subqueries.md %}) 一起使用。  
例如：

```sql
SELECT 42 IN (SELECT unnest([32, 42, 52]) AS x);
```

```text
true
```

如果子查询返回多于一列，则会抛出 Binder 错误：

```sql
SELECT 42 IN (SELECT unnest([32, 42, 52]) AS x, 'a' AS y);
```

```console
Binder 错误：
子查询返回 2 列 - 预期 1 列
```

## `NOT IN`

`NOT IN` 可用于检查元素是否不在集合中。  
`x NOT IN y` 等价于 `NOT (x IN y)`。