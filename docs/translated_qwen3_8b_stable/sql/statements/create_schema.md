---
---
layout: docu
railroad: statements/createschema.js
redirect_from:
- /docs/sql/statements/create_schema
title: CREATE SCHEMA 语句
---

`CREATE SCHEMA` 语句用于在目录中创建一个模式。默认模式为 `main`。

## 示例

创建一个模式：

```sql
CREATE SCHEMA s1;
```

如果模式尚不存在则创建：

```sql
CREATE SCHEMA IF NOT EXISTS s2;
```

如果模式存在则创建或替换：

```sql
CREATE OR REPLACE SCHEMA s2;
```

在模式中创建表：

```sql
CREATE TABLE s1.t (id INTEGER PRIMARY KEY, other_id INTEGER);
CREATE TABLE s2.t (id INTEGER PRIMARY KEY, j VARCHAR);
```

计算两个模式中表之间的连接：

```sql
SELECT *
FROM s1.t s1t, s2.t s2t
WHERE s1t.other_id = s2t.id;
```

## 语法

<div id="rrdiagram"></div>

---