---
---
blurb: NULL 值表示缺失的值。
layout: docu
redirect_from:
- /docs/sql/data_types/nulls
title: NULL 值
---

`NULL` 值是用于表示 SQL 中缺失数据的特殊值。任何类型的列都可以包含 `NULL` 值。逻辑上，`NULL` 值可以被视为“该字段的值未知”。

`NULL` 值可以插入到没有 `NOT NULL` 限定符的任何字段中：

```sql
CREATE TABLE integers (i INTEGER);
INSERT INTO integers VALUES (NULL);
```

`NULL` 值在查询的许多部分以及许多函数中具有特殊语义：

> 与 `NULL` 值进行任何比较都会返回 `NULL`，包括 `NULL = NULL`。

你可以使用 `IS NOT DISTINCT FROM` 来执行一个等值比较，其中 `NULL` 值相互比较相等。使用 `IS (NOT) NULL` 来检查一个值是否为 `NULL`。

```sql
SELECT NULL = NULL;
```

```text
NULL
```

```sql
SELECT NULL IS NOT DISTINCT FROM NULL;
```

```text
true
```

```sql
SELECT NULL IS NULL;
```

```text
true
```

## NULL 和函数

一个具有 `NULL` 作为输入参数的函数**通常**会返回 `NULL`。

```sql
SELECT cos(NULL);
```

```text
NULL
```

`coalesce` 函数是这一规则的例外：它接受任意数量的参数，并返回每行中第一个非 `NULL` 的参数。如果所有参数都是 `NULL`，`coalesce` 也会返回 `NULL`。

```sql
SELECT coalesce(NULL, NULL, 1);
```

```text
1
```

```sql
SELECT coalesce(10, 20);
```

```text
10
```

```sql
SELECT coalesce(NULL, NULL);
```

```text
NULL
```

`ifnull` 函数是 `coalesce` 的两个参数版本。

```sql
SELECT ifnull(NULL, 'default_string');
```

```text
default_string
```

```sql
SELECT ifnull(1, 'default_string');
```

```text
1
```

## `NULL` 和 `AND` / `OR`

当使用 `AND` 和 `OR` 时，`NULL` 值具有特殊的行为。
详细信息请参见[Boolean 类型文档]({% link docs/stable/sql/data_types/boolean.md %}).

## `NULL` 和 `IN` / `NOT IN`

`... IN ⟨包含 NULL 的内容⟩` 的行为与 `... IN ⟨不包含 NULL 的内容⟩` 不同。
详细信息请参见[`IN` 文档]({% link docs/stable/sql/expressions/in.md %}).

## `NULL` 和聚合函数

`NULL` 值在大多数聚合函数中被忽略。

不忽略 `NULL` 值的聚合函数包括：`first`、`last`、`list` 和 `array_agg`。要从这些聚合函数中排除 `NULL` 值，可以使用 [`FILTER` 子句]({% link docs/stable/sql/query_syntax/filter.md %}).

```sql
CREATE TABLE integers (i INTEGER);
INSERT INTO integers VALUES (1), (10), (NULL);
```

```sql
SELECT min(i) FROM integers;
```

```text
1
```

```sql
SELECT max(i) FROM integers;
```

```text
10
```