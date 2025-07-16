---
---
layout: docu
railroad: statements/delete.js
redirect_from:
- /docs/sql/statements/delete
title: DELETE 语句
---

`DELETE` 语句用于从表名标识的表中删除行。  
如果未提供 `WHERE` 子句，则表中的所有记录都会被删除。  
如果提供了 `WHERE` 子句，则只有那些使得 `WHERE` 子句结果为真的行会被删除。表达式结果为假或 `NULL` 的行将被保留。

## 示例

从数据库中删除满足条件 `i = 2` 的行：

```sql
DELETE FROM tbl WHERE i = 2;
```

删除表 `tbl` 中的所有行：

```sql
DELETE FROM tbl;
```

### `USING` 子句

`USING` 子句允许根据其他表或子查询的内容进行删除操作。

### `RETURNING` 子句

`RETURNING` 子句允许返回被删除的值。它使用与 `SELECT` 子句相同的语法，但不支持 `DISTINCT` 修饰符。

```sql
CREATE TABLE employees(name VARCHAR, age INTEGER);
INSERT INTO employees VALUES ('Kat', 32);
DELETE FROM employees RETURNING name, 2025 - age AS approx_birthyear;
```

| name | approx_birthyear |
|------|-----------------:|
| Kat  | 1993             |

## 语法

<div id="rrdiagram"></div>

## `TRUNCATE` 语句

`TRUNCATE` 语句用于从表中删除所有行，其作用等同于不带 `WHERE` 子句的 `DELETE FROM`：

```sql
TRUNCATE tbl;
```

## 关于回收内存和磁盘空间的限制

运行 `DELETE` 不意味着空间会被回收。通常，行只会被标记为已删除。DuckDB 在执行 [`CHECKPOINT`]({% link docs/stable/sql/statements/checkpoint.md %}) 时才会回收空间。[`VACUUM`]({% link docs/stable/sql/statements/vacuum.md %}) 目前不回收空间。