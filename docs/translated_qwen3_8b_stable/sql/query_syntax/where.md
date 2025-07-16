---
---
layout: docu
railroad: query_syntax/where.js
redirect_from:
- /docs/sql/query_syntax/where
title: WHERE 子句
---

`WHERE` 子句指定要应用于数据的任何筛选条件。这允许您只选择感兴趣的数据子集。逻辑上，`WHERE` 子句在 `FROM` 子句之后立即应用。

## 示例

选择所有 `id` 等于 3 的行：

```sql
SELECT *
FROM table_name
WHERE id = 3;
```

选择所有与给定 **区分大小写** 的 `LIKE` 表达式匹配的行：

```sql
SELECT *
FROM table_name
WHERE name LIKE '%mark%';
```

选择所有与给定 **不区分大小写** 的表达式匹配的行，该表达式使用 `ILIKE` 运算符构造：

```sql
SELECT *
FROM table_name
WHERE name ILIKE '%mark%';
```

选择所有与给定复合表达式匹配的行：

```sql
SELECT *
FROM table_name
WHERE id = 3 OR id = 7;
```

## 语法

<div id="rrdiagram"></div>