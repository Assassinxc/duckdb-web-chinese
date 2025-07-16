---
---
layout: docu
railroad: query_syntax/groupby.js
redirect_from:
- /docs/sql/query_syntax/groupby
title: GROUP BY 子句
---

`GROUP BY` 子句指定哪些分组列用于执行 `SELECT` 子句中的任何聚合操作。
如果指定了 `GROUP BY` 子句，查询始终是一个聚合查询，即使 `SELECT` 子句中没有聚合操作。

当指定了 `GROUP BY` 子句时，所有在分组列中数据匹配的元组（即属于同一组的所有元组）将被合并。
分组列本身的值不会改变，其他列可以使用 [聚合函数]({% link docs/stable/sql/functions/aggregates.md %})（如 `count`、`sum`、`avg` 等）进行合并。

## `GROUP BY ALL`

使用 `GROUP BY ALL` 对 `SELECT` 语句中未被聚合函数包裹的所有列进行分组。
这简化了语法，允许将列列表维护在一个位置，并通过保持 `SELECT` 的粒度与 `GROUP BY` 的粒度一致来防止错误（例如，防止重复）。请参见下面的示例以及[“使用 DuckDB 实现更友好的 SQL”博客文章]({% post_url 2022-05-04-friendlier-sql %}#group-by-all) 中的更多示例。

## 多维分组

通常，`GROUP BY` 子句沿一个维度进行分组。
使用 [`GROUPING SETS`、`CUBE` 或 `ROLLUP` 子句]({% link docs/stable/sql/query_syntax/grouping_sets.md %}) 可以沿多个维度进行分组。
更多信息请参见 [`GROUPING SETS`]({% link docs/stable/sql/query_syntax/grouping_ming.md %}) 页面。

## 示例

统计 `addresses` 表中属于每个不同城市的条目数：

```sql
SELECT city, count(*)
FROM addresses
GROUP BY city;
```

计算每个城市每个街道名称的平均收入：

```sql
SELECT city, street_name, avg(income)
FROM addresses
GROUP BY city, street_name;
```

### `GROUP BY ALL` 示例

按城市和街道名称分组以去除任何重复值：

```sql
SELECT city, street_name
FROM addresses
GROUP BY ALL;
```

计算每个城市每个街道名称的平均收入。由于 `income` 被封装在聚合函数中，因此不需要将其包含在 `GROUP BY` 中：

```sql
SELECT city, street_name, avg(income)
FROM addresses
GROUP BY ALL;
-- GROUP BY city, street_name:
```

## 语法

<div id="rrdiagram"></div>