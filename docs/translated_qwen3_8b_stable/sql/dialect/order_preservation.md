---
---
layout: docu
redirect_from:
- /docs/sql/dialect/order_preservation
title: 顺序保留
---

对于许多操作，DuckDB 会保留行的顺序，这与 Pandas 等数据框库类似。

## 示例

以下表格为例：

```sql
CREATE TABLE tbl AS
    SELECT *
    FROM (VALUES (1, 'a'), (2, 'b'), (3, 'c')) t(x, y);

SELECT *
FROM tbl;
```

| x | y |
|--:|---|
| 1 | a |
| 2 | b |
| 3 | c |

我们来看一个返回 `x` 为奇数的行的查询：

```sql
SELECT *
FROM tbl
WHERE x % 2 == 1;
```

| x | y |
|--:|---|
| 1 | a |
| 3 | c |

由于在原始表中 `(1, 'a')` 出现在 `(3, 'c')` 之前，因此在这个表中也保证 `(1, 'a')` 会出现在 `(3, 'c')` 之前。

## 子句

以下子句保证原始行顺序被保留：

* `COPY`（参见 [插入顺序](#insertion-order)）
* `FROM` 单个表
* `LIMIT`
* `OFFSET`
* `SELECT`
* `UNION ALL`
* `WHERE`
* 带有空 `OVER` 子句的窗口函数
* 公共表表达式和表子查询，只要它们仅包含上述组件

> 提示 `row_number() OVER ()` 可以将原始行顺序转换为一个显式的列，可以在默认不保留行顺序的操作中引用。在物化表中，可以使用 `rowid` 虚拟列达到相同的效果。

以下操作 **不** 保证行顺序被保留：

* `FROM` 多个表和/或子查询
* `JOIN`
* `UNION`
* `USING SAMPLE`
* `GROUP BY`（特别是输出顺序未定义，且行在 [顺序敏感的聚合函数](https://duckdb.org/docs/sql/functions/aggregates.html#order-by-clause-in-aggregate-functions) 中的输入顺序也未定义，除非在聚合函数中显式指定）
* `ORDER BY`（具体来说，`ORDER BY` 可能不使用 [稳定算法](https://en.m.wikipedia.org/wiki/Stable_algorithm)）
* 标量子查询

## 插入顺序

默认情况下，以下组件保留插入顺序：

* [CSV 读取器]({% link docs/stable/data/csv/overview.md %}#order-preservation)（`read_csv` 函数）
* [JSON 读取器]({% link docs/stable/data/json/overview,md %}#order-preservation)（`read_json` 函数）
* [Parquet 读取器]({% link docs/stable/data/parquet/overview.md %}#order-preservation)（`read_parquet` 函数）

插入顺序的保留由 `preserve_insertion_order` [配置选项]({% link docs/stable/configuration/overview.md %}) 控制。
此设置默认为 `true`，表示应保留顺序。
要更改此设置，请使用：

```sql
SET preserve_insertion_order = false;
```