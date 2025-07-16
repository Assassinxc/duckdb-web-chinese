---
---
layout: docu
redirect_from:
- /docs/operations_manual/non-deterministic_behavior
title: 非确定性行为
---

DuckDB 中的多个操作符表现出非确定性行为。
最显著的是，SQL 使用集合语义，允许结果以不同的顺序返回。
DuckDB 利用这一点来提高性能，尤其是在执行多线程查询时。
其他因素，如使用不同的编译器、操作系统和硬件架构，也可能导致顺序发生变化。
本页面记录了非确定性行为是_预期行为_的情况。
如果您希望使查询变得确定性，请参阅[“处理非确定性”部分](#working-around-non-determinism)。

## 集合语义

非确定性的常见来源之一是 SQL 所使用的集合语义。
例如，如果您重复运行以下查询，可能会得到两个不同的结果：

```sql
SELECT *
FROM (
    SELECT 'A' AS x
    UNION
    SELECT 'B' AS x
);
```

结果 `A`, `B` 和 `B`, `A` 都是正确的。

## 不同平台上的不同结果：`array_distinct`

`array_distinct` 函数可能在不同平台上返回不同的顺序结果[1]：

```sql
SELECT array_distinct(['A', 'A', 'B', NULL, NULL]) AS arr;
```

对于这个查询，`[A, B]` 和 `[B, A]` 都是有效结果。

## 多线程下的浮点数聚合操作

浮点数不精确性可能在多线程配置中导致不同结果：
例如，[`stddev` 和 `corr` 可能产生非确定性结果`](https://github.com/duckdb/duckdb/issues/13763)：

```sql
CREATE TABLE tbl AS
    SELECT 'ABCDEFG'[floor(random() * 7 + 1)::INT] AS s, 3.7 AS x, i AS y
    FROM range(1, 1_000_000) r(i);

SELECT s, stddev(x) AS standard_deviation, corr(x, y) AS correlation
FROM tbl
GROUP BY s
ORDER BY s;
```

该查询的预期标准差和相关系数在所有 `s` 值下都为 0。
然而，当在多个线程上执行时，由于浮点数不精确性，查询可能会返回小数值（`0 <= z < 10e-16`）。

## 处理非确定性

对于大多数用例，非确定性不会导致任何问题。
然而，有些情况下需要确定性结果。
在这些情况下，可以尝试以下解决方法：

1. 限制线程数量以防止多线程引入的非确定性。

   ```sql
   SET threads = 1;
   ```

2. 强制排序。例如，您可以使用 [`ORDER BY ALL` 子句]({% link docs/stable/sql/query_syntax/orderby.md %}#order-by-all)：

   ```sql
   SELECT *
   FROM (
       SELECT 'A' AS x
       UNION
       SELECT 'B' AS x
   )
   ORDER BY ALL;
   ```

   您也可以使用 [`list_sort`]({% link docs/stable/sql/functions/list.md %}#list_sortlist) 对列表进行排序：

   ```sql
   SELECT list_sort(array_distinct(['A', 'A', 'B', NULL, NULL])) AS i
   ORDER BY i;
   ```

   同时，也可以引入[确定性洗牌]({% post_url 2024-08-19-duckdb-tricks-part-1 %}#shuffling-data)。