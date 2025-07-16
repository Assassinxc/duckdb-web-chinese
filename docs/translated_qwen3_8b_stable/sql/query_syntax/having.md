---
---
layout: docu
railroad: query_syntax/groupby.js
redirect_from:
- /docs/sql/query_syntax/having
title: HAVING 子句
---

`HAVING` 子句可以在 `GROUP BY` 子句之后使用，以提供在分组完成后进行筛选的条件。在语法方面，`HAVING` 子句与 `WHERE` 子句相同，但 `WHERE` 子句在分组之前执行，而 `HAVING` 子句在分组之后执行。

## 示例

统计 `addresses` 表中每个不同 `city` 的条目数量，过滤掉数量低于 50 的城市：

```sql
SELECT city, count(*)
FROM addresses
GROUP BY city
HAVING count(*) >= 50;
```

计算每个 `street_name` 每个城市的平均收入，过滤掉平均 `income` 大于中位数 `income` 两倍的城市：

```sql
SELECT city, street_name, avg(income)
FROM addresses
GROUP BY city, street_name
HAVING avg(income) > 2 * median(income);
```

## 语法

<div id="rrdiagram"></div>