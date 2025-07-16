---
---
layout: docu
title: TRY 表达式
---

`TRY` 表达式确保子（标量）表达式中由于输入行导致的错误会使得这些行的结果为 `NULL`，而不是导致查询抛出错误。

> `TRY` 表达式灵感来源于 [`TRY_CAST` 表达式]({% link docs/stable/sql/expressions/cast.md %}#try_cast)。

## 示例

以下调用在没有 `TRY` 表达式的情况下会返回错误。
当它们被封装为 `TRY` 表达式时，会返回 `NULL`：

### 类型转换

#### 不使用 `TRY`

```sql
SELECT 'abc'::INTEGER;
```

```console
转换错误：
无法将字符串 'abc' 转换为 INT32
```

#### 使用 `TRY`

```sql
SELECT TRY('abc'::INTEGER);
```

```text
NULL
```

### 对零取对数

#### 不使用 `TRY`

```sql
SELECT ln(0);
```

```console
超出范围错误：
无法对零取对数
```

#### 使用 `TRY`

```sql
SELECT TRY(ln(0));
```

```text
NULL
```

### 转换多行

#### 不使用 `TRY`

```sql
WITH cte AS (FROM (VALUES ('123'), ('test'), ('235')) t(a))
SELECT a::INTEGER AS x FROM cte;
```

```console
转换错误：
无法将字符串 'test' 转换为 INT32
```

#### 使用 `TRY`

```sql
WITH cte AS (FROM (VALUES ('123'), ('test'), ('235')) t(a))
SELECT TRY(a::INTEGER) AS x FROM cte;
```

<div class="center_aligned_header_table"></div>

|  x   |
|-----:|
| 123  |
| NULL |
| 235  |

## 局限性

`TRY` 不能与易变函数或 [标量子查询]({% link docs/stable/sql/expressions/subqueries.md %}#scalar-subquery) 一起使用。
例如：

```sql
SELECT TRY(random())
```

```console
绑定错误：
不能将 TRY 与易变函数一起使用
```