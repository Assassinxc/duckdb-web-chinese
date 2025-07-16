---
---
layout: docu
railroad: query_syntax/sample.js
redirect_from:
- /docs/sql/query_syntax/sample
title: SAMPLE 子句
---

`SAMPLE` 子句允许您在基础表的样本上运行查询。这可以在牺牲结果准确性的情况下显著加快查询的处理速度。样本也可用于在探索数据集时快速查看数据快照。`SAMPLE` 子句在 `FROM` 子句中的任何内容之后立即应用（即在任何连接之后，但在 `WHERE` 子句或任何聚合之前）。有关更多信息，请参阅 [`SAMPLE`]({% link docs/stable/sql/samples.md %}) 页面。

## 示例

使用默认（系统）抽样从地址表中选择 1% 的样本：

```sql
SELECT *
FROM addresses
USING SAMPLE 1%;
```

使用伯努利抽样从地址表中选择 1% 的样本：

```sql
SELECT *
FROM addresses
USING SAMPLE 1% (bernoulli);
```

从子查询中选择 10 行的样本：

```sql
SELECT *
FROM (SELECT * FROM addresses)
USING SAMPLE 10 ROWS;
```

## 语法

<div id="rrdiagram"></div>