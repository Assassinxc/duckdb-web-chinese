---
---
layout: docu
railroad: query_syntax/values.js
redirect_from:
- /docs/sql/query_syntax/values
title: VALUES 子句
---

`VALUES` 子句用于指定固定数量的行。`VALUES` 子句可以作为独立语句使用，也可以作为 `FROM` 子句的一部分，或者作为 `INSERT INTO` 语句的输入。

## 示例

生成两行并直接返回：

```sql
VALUES ('Amsterdam', 1), ('London', 2);
```

作为 `FROM` 子句的一部分生成两行，并重命名列：

```sql
SELECT *
FROM (VALUES ('Amsterdam', 1), ('London', 2)) cities(name, id);
```

生成两行并将它们插入到表中：

```sql
INSERT INTO cities
VALUES ('Amsterdam', 1), ('London', 2);
```

直接从 `VALUES` 子句创建表：

```sql
CREATE TABLE cities AS
    SELECT *
    FROM (VALUES ('Amsterdam', 1), ('London', 2)) cities(name, id);
```

## 语法

<div id="rrdiagram"></div>