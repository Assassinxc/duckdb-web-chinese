---
---
layout: docu
railroad: query_syntax/filter.js
redirect_from:
- /docs/sql/query_syntax/filter
title: FILTER 子句
---

`FILTER` 子句可以作为 `SELECT` 语句中聚合函数的可选部分。它会以与 `WHERE` 子句过滤行相同的方式过滤传入聚合函数的数据行，但仅针对特定的聚合函数。

在以下多种情况下，`FILTER` 子句非常有用，包括评估具有不同过滤条件的多个聚合函数，以及创建数据集的透视视图。与下面将讨论的更传统的 `CASE WHEN` 方法相比，`FILTER` 提供了更清晰的语法用于数据透视。

一些聚合函数也不会过滤掉 `NULL` 值，因此使用 `FILTER` 子句可以在某些情况下返回有效的结果，而 `CASE WHEN` 方法则不能。这种情况发生在 `first` 和 `last` 函数中，这些函数在非聚合的透视操作中很有用，目标是简单地将数据重新定向为列，而不是重新聚合数据。`FILTER` 还在使用 `list` 和 `array_agg` 函数时改进了 `NULL` 处理，因为 `CASE WHEN` 方法会将 `NULL` 值包含在列表结果中，而 `FILTER` 子句会将其移除。

## 示例

返回以下结果：

* 总行数
* `i <= 5` 的行数
* `i` 为奇数的行数

```sql
SELECT
    count() AS total_rows,
    count() FILTER (i <= 5) AS lte_five,
    count() FILTER (i % 2 = 1) AS odds
FROM generate_series(1, 10) tbl(i);
```

<div class="monospace_table"></div>

| total_rows | lte_five | odds |
|:---|:---|:---|
| 10 | 5 | 5 |

> 仅通过计数满足条件的行也可以使用布尔 `sum` 聚合函数实现，例如：`sum(i <= 5)`。

可以使用不同的聚合函数，也可以使用多个 `WHERE` 表达式：

```sql
SELECT
    sum(i) FILTER (i <= 5) AS lte_five_sum,
    median(i) FILTER (i % 2 = 1) AS odds_median,
    median(i) FILTER (i % 2 = 1 AND i <= 5) AS odds_lte_five_median
FROM generate_series(1, 10) tbl(i);
```

<div class="monospace_table"></div>

| lte_five_sum | odds_median | odds_lte_five_median |
|:---|:---|:---|
| 15 | 5.0 | 3.0 |

`FILTER` 子句也可以用于将数据从行转换为列。这是一种静态透视，因为列必须在 SQL 运行时之前定义。然而，这种类型的语句可以在宿主编程语言中动态生成，以利用 DuckDB 的 SQL 引擎进行快速、大于内存的透视操作。

首先生成一个示例数据集：

```sql
CREATE TEMP TABLE stacked_data AS
    SELECT
        i,
        CASE WHEN i <= rows * 0.25  THEN 2022
             WHEN i <= rows * 0.5   THEN 2023
             WHEN i <= rows * 0.75  THEN 2024
             WHEN i <= rows * 0.875 THEN 2025
             ELSE NULL
             END AS year
    FROM (
        SELECT
            i,
            count(*) OVER () AS rows
        FROM generate_series(1, 100_000_000) tbl(i)
    ) tbl;
```

按年份“透视”数据（将每个年份移至单独的列）：

```sql
SELECT
    count(i) FILTER (year = 2022) AS "2022",
    count(i) FILTER (year = 2023) AS "2023",
    count(i) FILTER (year = 2024) AS "2024",
    count(i) FILTER (year = 2025) AS "2025",
    count(i) FILTER (year IS NULL) AS "NULLs"
FROM stacked_data;
```

这种语法产生的结果与上面的 `FILTER` 子句相同：

```sql
SELECT
    count(CASE WHEN year = 2022 THEN i END) AS "2022",
    count(CASE WHEN year = 2023 THEN i END) AS "2023",
    count(CASE WHEN year = 2024 THEN i END) AS "2024",
    count(CASE WHEN year = 2025 THEN i END) AS "2025",
    count(CASE WHEN year IS NULL THEN i END) AS "NULLs"
FROM stacked_data;
```

<div class="monospace_table"></div>

|   2022   |   2023   |   2024   |   2025   |  NULLs   |
|:---|:---|:---|:---|:---|
| 25000000 | 25000000 | 25000000 | 12500000 | 12500000 |

然而，当使用不忽略 `NULL` 值的聚合函数时，`CASE WHEN` 方法可能不会按预期工作。`first` 函数属于此类，因此在这种情况下更推荐使用 `FILTER`。

按年份“透视”数据（将每个年份移至单独的列）：

```sql
SELECT
    first(i) FILTER (year = 2022) AS "2022",
    first(i) FILTER (year = 2023) AS "2023",
    first(i) FILTER (year = 2024) AS "2024",
    first(i) FILTER (year = 2025) AS "2025",
    first(i) FILTER (year IS NULL) AS "NULLs"
FROM stacked_data;
```

<div class="monospace_table"></div>

|   2022   |   2023   |   2024   |   2025   |  NULLs   |
|:---|:---|:---|:---|:---|
| 1474561 | 25804801 | 50749441 | 76431361 | 87500001 |

这将产生 `NULL` 值，当 `CASE WHEN` 子句的首次评估返回 `NULL` 时：

```sql
SELECT
    first(CASE WHEN year = 2022 THEN i END) AS "2022",
    first(CASE WHEN year = 2023 THEN i END) AS "2023",
    first(CASE WHEN year = 2024 THEN i END) AS "2024",
    first(CASE WHEN year = 2025 THEN i END) AS "2025",
    first(CASE WHEN year IS NULL THEN i END) AS "NULLs"
FROM stacked_data;
```

<div class="monospace_table"></div>

|   2022   |   2023   |   2024   |   2025   |  NULLs   |
|:---|:---|:---|:---|:---|
| 1228801 | NULL | NULL | NULL | NULL  |

## 聚合函数语法（包括 `FILTER` 子句）

<div id="rrdiagram"></div>