---
---
layout: docu
railroad: statements/update.js
redirect_from:
- /docs/sql/statements/update
title: UPDATE 语句
---

`UPDATE` 语句用于修改表中行的值。

## 示例

对于所有 `i` 为 `NULL` 的行，将其值设置为 0：

```sql
UPDATE tbl
SET i = 0
WHERE i IS NULL;
```

将所有 `i` 的值设置为 1，所有 `j` 的值设置为 2：

```sql
UPDATE tbl
SET i = 1, j = 2;
```

## 语法

<div id="rrdiagram"></div>

`UPDATE` 会修改满足条件的所有行中指定列的值。只需在 `SET` 子句中提及需要修改的列；未显式修改的列将保留其之前的值。

## 从其他表更新

可以基于另一个表的值来更新表。这可以通过在 `FROM` 子句中指定一个表，或使用子查询语句来实现。这两种方法都能提高性能，通过批量完成 `UPDATE` 操作。

```sql
CREATE OR REPLACE TABLE original AS
    SELECT 1 AS key, 'original value' AS value
    UNION ALL
    SELECT 2 AS key, 'original value 2' AS value;

CREATE OR REPLACE TABLE new AS
    SELECT 1 AS key, 'new value' AS value
    UNION ALL
    SELECT 2 AS key, 'new value 2' AS value;

SELECT *
FROM original;
```

| key |      value       |
|-----|------------------|
| 1   | original value   |
| 2   | original value 2 |

```sql
UPDATE original
    SET value = new.value
    FROM new
    WHERE original.key = new.key;
```

或者：

```sql
UPDATE original
    SET value = (
        SELECT
            new.value
        FROM new
        WHERE original.key = new.key
    );
```

```sql
SELECT *
FROM original;
```

| key |    value    |
|-----|-------------|
| 1   | new value   |
| 2   | new value 2 |

## 从同一表更新

与上述情况唯一的不同之处在于，目标表和源表都必须指定不同的表别名。
在本例中 `AS true_original` 和 `AS new` 都是必需的。

```sql
UPDATE original AS true_original
    SET value = (
        SELECT
            new.value || ' a change!' AS value
        FROM original AS new
        WHERE true_original.key = new.key
    );
```

## 使用连接进行更新

为了选择要更新的行，`UPDATE` 语句可以使用 `FROM` 子句，并通过 `WHERE` 子句表达连接。例如：

```sql
CREATE TABLE city (name VARCHAR, revenue BIGINT, country_code VARCHAR);
CREATE TABLE country (code VARCHAR, name VARCHAR);
INSERT INTO city VALUES ('Paris', 700, 'FR'), ('Lyon', 200, 'FR'), ('Brussels', 400, 'BE');
INSERT INTO country VALUES ('FR', 'France'), ('BE', 'Belgium');
```

为了增加法国所有城市的收入，将 `city` 表和 `country` 表进行连接，并按后者进行过滤：

```sql
UPDATE city
SET revenue = revenue + 100
FROM country
WHERE city.country_code = country.code
  AND country.name = 'France';
```

```sql
SELECT *
FROM city;
```

|   name   | revenue | country_code |
|----------|--------:|--------------|
| Paris    | 800     | FR           |
| Lyon     | 300     | FR           |
| Brussels | 400     | BE           |

## Upsert（插入或更新）

详情请参阅 [插入文档]({% link docs/stable/sql/statements/insert.md %}#on-conflict-clause)。