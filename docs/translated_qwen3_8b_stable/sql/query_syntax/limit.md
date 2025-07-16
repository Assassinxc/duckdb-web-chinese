---
---
layout: docu
railroad: query_syntax/orderby.js
redirect_from:
- /docs/sql/query_syntax/limit
title: LIMIT 和 OFFSET 子句
---

`LIMIT` 是一个输出修饰符。逻辑上它是在查询的最后应用。`LIMIT` 子句限制了获取的行数。`OFFSET` 子句表示从哪个位置开始读取值，即前 `OFFSET` 个值会被忽略。

请注意，虽然可以不使用 `ORDER BY` 子句使用 `LIMIT`，但没有 `ORDER BY` 子句时结果可能不是确定的。不过这在某些情况下仍然有用，例如当你想要快速查看数据的快照时。

## 示例

从 addresses 表中选择前 5 行：

```sql
SELECT *
FROM addresses
LIMIT 5;
```

从 addresses 表中选择第 5 行开始的 5 行（即忽略前 5 行）：

```sql
SELECT *
FROM addresses
LIMIT 5
OFFSET 5;
```

选择人口最多的前 5 个城市：

```sql
SELECT city, count(*) AS population
FROM addresses
GROUP BY city
ORDER BY population DESC
LIMIT 5;
```

从 addresses 表中选择 10% 的行：

```sql
SELECT *
FROM addresses
LIMIT 10%;
```

## 语法

<div id="rrdiagram"></div>

---