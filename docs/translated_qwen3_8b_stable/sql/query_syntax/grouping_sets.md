---
---
layout: docu
railroad: query_syntax/groupby.js
redirect_from:
- /docs/sql/query_syntax/grouping_sets
title: GROUPING SETS
---

`GROUPING SETS`、`ROLLUP` 和 `CUBE` 可以在 `GROUP BY` 子句中使用，以在同一查询中对多个维度进行分组。
请注意，此语法不兼容 [`GROUP BY ALL`]({% link docs/stable/sql/query_syntax/groupby.md %}#group-by-all)。

## 示例

计算沿提供的四个不同维度的平均收入：

```sql
-- 语法 () 表示空集（即计算未分组的聚合）
SELECT city, street_name, avg(income)
FROM addresses
GROUP BY GROUPING SETS ((city, street_name), (city), (street_name), ());
```

计算沿相同维度的平均收入：

```sql
SELECT city, street_name, avg(income)
FROM addresses
GROUP BY CUBE (city, street_name);
```

计算沿维度 `(city, street_name)`、`(city)` 和 `()` 的平均收入：

```sql
SELECT city, street_name, avg(income)
FROM addresses
GROUP BY ROLLUP (city, street_name);
```

## 描述

`GROUPING SETS` 在单个查询中对不同的 `GROUP BY 子句` 执行相同的聚合操作。

```sql
CREATE TABLE students (course VARCHAR, type VARCHAR);
INSERT INTO students (course, type)
VALUES
    ('CS', 'Bachelor'), ('CS', 'Bachelor'), ('CS', 'PhD'), ('Math', 'Masters'),
    ('CS', NULL), ('CS', NULL), ('Math', NULL);
```

```sql
SELECT course, type, count(*)
FROM students
GROUP BY GROUPING SETS ((course, type), course, type, ());
```

| course |   type   | count_star() |
|--------|----------|-------------:|
| Math   | NULL     | 1            |
| NULL   | NULL     | 7            |
| CS     | PhD      | 1            |
| CS     | Bachelor | 2            |
| Math   | Masters  | 1            |
| CS     | NULL     | 2            |
| Math   | NULL     | 2            |
| CS     | NULL     | 5            |
| NULL   | NULL     | 3            |
| NULL   | Masters  | 1            |
| NULL   | Bachelor | 2            |
| NULL   | PhD      | 1            |

在上面的查询中，我们按四个不同的组集进行分组：`course, type`、`course`、`type` 和 `()`（空组）。结果中对于未在分组集中的组，显示为 `NULL`，即上述查询等价于以下 `UNION ALL` 子句的语句：

```sql
-- 按 course, type 分组：
SELECT course, type, count(*)
FROM students
GROUP BY course, type
UNION ALL
-- 按 type 分组：
SELECT NULL AS course, type, count(*)
FROM students
GROUP BY type
UNION ALL
-- 按 course 分组：
SELECT course, NULL AS type, count(*)
FROM students
GROUP BY course
UNION ALL
-- 不分组：
SELECT NULL AS course, NULL AS type, count(*)
FROM students;
```

`CUBE` 和 `ROLLUP` 是用于轻松生成常用分组集的语法糖。

`ROLLUP` 子句将为一个分组集生成所有“子组”，例如，`ROLLUP (country, city, zip)` 会生成分组集 `(country, city, zip), (country, city), (country), ()`。这可以用于生成不同级别的分组详情。它将生成 `n+1` 个分组集，其中 `n` 是 `ROLLUP` 子句中的项数。

`CUBE` 会为所有输入的组合生成分组集，例如，`CUBE (country, city, zip)` 将生成 `(country, city, zip), (country, city), (country, zip), (city, zip), (country), (city), (zip), ()`。这将生成 `2^n` 个分组集。

## 使用 `GROUPING_ID()` 识别分组集

`GROUPING SETS`、`ROLLUP` 和 `CUBE` 生成的超级聚合行通常可以通过分组列中返回的 `NULL` 值来识别。但如果分组列中使用了实际的 `NULL` 值，那么区分结果集中的 `NULL` 值是数据本身还是由分组结构生成的 `NULL` 值可能会变得困难。`GROUPING_ID()` 或 `GROUPING()` 函数旨在识别结果中生成超级聚合行的组。

`GROUPING_ID()` 是一个聚合函数，它接受构成分组的列表达式。它返回一个 `BIGINT` 值。对于非超级聚合行，返回值为 `0`。但对于超级聚合行，它返回一个整数值，该值标识生成超级聚合的组的表达式组合。此时，一个示例可能有助于理解。考虑以下查询：

```sql
WITH days AS (
    SELECT
        year("generate_series")    AS y,
        quarter("generate_series") AS q,
        month("generate_series")   AS m
    FROM generate_series(DATE '2023-01-01', DATE '2023-12-31', INTERVAL 1 DAY)
)
SELECT y, q, m, GROUPING_ID(y, q, m) AS "grouping_id()"
FROM days
GROUP BY GROUPING SETS (
    (y, q, m),
    (y, q),
    (y),
    ()
)
ORDER BY y, q, m;
```

这些是结果：

|  y   |  q   |  m   | grouping_id() |
|-----:|-----:|-----:|--------------:|
| 2023 | 1    | 1    | 0             |
| 2023 | 1    | 2    | 0             |
| 2023 | 1    | 3    | 0             |
| 2023 | 1    | NULL | 1             |
| 2023 | 2    | 4    | 0             |
| 2023 | 2    | 5    | 0             |
| 2023 | 2    | 6    | 0             |
| 2023 | 2    | NULL | 1             |
| 2023 | 3    | 7    | 0             |
| 2023 | 3    | 8    | 0             |
| 2023 | 3    | 9    | 0             |
| 2023 | 3    | NULL | 1             |
| 2023 | 4    | 10   | 0             |
| 2023 | 4    | 11   | 0             |
| 2023 | 4    | 12   | 0             |
| 2023 | 4    | NULL | 1             |
| 2023 | NULL | NULL | 3             |
| NULL | NULL | NULL | 7             |

在这个示例中，最低级别的分组是在月份级别，由分组集 `(y, q, m)` 定义。对应于该级别的结果行是简单的聚合行，`GROUPING_ID(y, q, m)` 函数返回 `0`。分组集 `(y, q)` 会生成月份级别的超级聚合行，`m` 列留出 `NULL` 值，`GROUPING_ID(y, q, m)` 返回 `1`。分组集 `(y)` 会生成季度级别的超级聚合行，`m` 和 `q` 列留出 `NULL` 值，`GROUPING_ID(y, q, m)` 返回 `3`。最后，`()` 分组集会产生一个超级聚合行，`y`、`q` 和 `m` 均为 `NULL`，`GROUPING_ID(y, q, m)` 返回 `7`。

为了理解返回值与分组集之间的关系，可以将 `GROUPING_ID(y, q, m)` 视为一个位字段，其中第一个位对应 `GROUPING_ID()` 最后一个传入的表达式，第二个位对应倒数第二个传入的表达式，依此类推。通过将 `GROUPING_ID()` 转换为 `BIT` 可能会更清晰：

```sql
WITH days AS (
    SELECT
        year("generate_series")    AS y,
        quarter("generate_series") AS q,
        month("generate_series")   AS m
    FROM generate_series(DATE '2023-01-01', DATE '2023-12-31', INTERVAL 1 DAY)
)
SELECT
    y, q, m,
    GROUPING_ID(y, q, m) AS "grouping_id(y, q, m)",
    right(GROUPING_ID(y, q, m)::BIT::VARCHAR, 3) AS "y_q_m_bits"
FROM days
GROUP BY GROUPING SETS (
    (y, q, m),
    (y, q),
    (y),
    ()
)
ORDER BY y, q, m;
```

返回的结果如下：

|  y   |  q   |  m   | grouping_id(y, q, m) | y_q_m_bits |
|-----:|-----:|-----:|---------------------:|------------|
| 2023 | 1    | 1    | 0                    | 000        |
| 2023 | 1    | 2    | 0                    | 000        |
| 2023 | 1    | 3    | 0                    | 000        |
| 2023 | 1    | NULL | 1                    | 001        |
| 2023 | 2    | 4    | 0                    | 000        |
| 2023 | 2    | 5    | 0                    | 000        |
| 2023 | 2    | 6    | 0                    | 000        |
| 2023 | 2    | NULL | 1                    | 001        |
| 2023 | 3    | 7    | 0                    | 000        |
| 2023 | 3    | 8    | 0                    | 000        |
| 2023 | 3    | 9    | 0                    | 000        |
| 2023 | 3    | NULL | 1                    | 001        |
| 2023 | 4    | 10   | 0                    | 000        |
| 2023 | 4    | 11   | 0                    | 000        |
| 2023 | 4    | 12   | 0                    | 000        |
| 2023 | 4    | NULL | 1                    | 001        |
| 2023 | NULL | NULL | 3                    | 011        |
| NULL | NULL | NULL | 7                    | 111        |

请注意，传递给 `GROUPING_ID()` 的表达式数量或它们的顺序与 `GROUPING SETS` 子句（或 `ROLLUP` 和 `CUBE` 所暗示的组）中的实际分组定义无关。只要传递给 `GROUPING_ID()` 的表达式是 `GROUPING SETS` 子句中出现的表达式，`GROUPING_ID()` 将会在该表达式被提升到超级聚合时设置对应位的位。

## 语法

<div id="rrdiagram"></div>

---