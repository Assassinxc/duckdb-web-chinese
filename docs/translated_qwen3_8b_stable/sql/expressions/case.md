---
---
layout: docu
railroad: expressions/case.js
redirect_from:
- /docs/sql/expressions/case
title: CASE 表达式
---

<div id="rrdiagram"></div>

`CASE` 表达式根据条件执行类似开关的操作。其基本形式与许多编程语言中使用的三元条件表达式相同（`CASE WHEN cond THEN a ELSE b END` 等同于 `cond ? a : b`）。使用单个条件时，也可以用 `IF(cond, a, b)` 表达。

```sql
CREATE OR REPLACE TABLE integers AS SELECT unnest([1, 2, 3]) AS i;
SELECT i, CASE WHEN i > 2 THEN 1 ELSE 0 END AS test
FROM integers;
```

| i | test |
|--:|-----:|
| 1 | 0    |
| 2 | 0    |
| 3 | 1    |

这等同于：

```sql
SELECT i, IF(i > 2, 1, 0) AS test
FROM integers;
```

`CASE` 表达式中的 `WHEN cond THEN expr` 部分可以链式使用，只要其中任意一个条件对单个元组返回 true，对应的表达式就会被求值并返回。

```sql
CREATE OR REPLACE TABLE integers AS SELECT unnest([1, 2, 3]) AS i;
SELECT i, CASE WHEN i = 1 THEN 10 WHEN i = 2 THEN 20 ELSE 0 END AS test
FROM integers;
```

| i | test |
|--:|-----:|
| 1 | 10   |
| 2 | 20   |
| 3 | 0    |

`CASE` 表达式的 `ELSE` 子句是可选的。如果没有提供 `ELSE` 子句，并且没有任何条件匹配，`CASE` 表达式将返回 `NULL`。

```sql
CREATE OR REPLACE TABLE integers AS SELECT unnest([1, 2, 3]) AS i;
SELECT i, CASE WHEN i = 1 THEN 10 END AS test
FROM integers;
```

| i | test |
|--:|-----:|
| 1 | 10   |
| 2 | NULL |
| 3 | NULL |

也可以在 `CASE` 之后、`WHEN` 之前提供一个单独的表达式。当这样做时，`CASE` 表达式实际上会被转换为一个 switch 语句。

```sql
CREATE OR REPLACE TABLE integers AS SELECT unnest([1, 2, 3]) AS i;
SELECT i, CASE i WHEN 1 THEN 10 WHEN 2 THEN 20 WHEN 3 THEN 30 END AS test
FROM integers;
```

| i | test |
|--:|-----:|
| 1 | 10   |
| 2 | 20   |
| 3 | 30   |

这等同于：

```sql
SELECT i, CASE WHEN i = 1 THEN 10 WHEN i = 2 THEN 20 WHEN i = 3 THEN 30 END AS test
FROM integers;
```