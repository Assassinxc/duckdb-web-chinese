---
---
layout: docu
redirect_from:
- /docs/guides/meta/list_tables
title: 列表表
---

`SHOW TABLES` 命令可用于获取 [选定模式]({% link docs/stable/sql/statements/use.md %}) 中所有表的列表。

```sql
CREATE TABLE tbl (i INTEGER);
SHOW TABLES;
```

| name |
|------|
| tbl  |

使用 `SHOW` 或 `SHOW ALL TABLES` 可以获取 **所有** 附加数据库和模式中的表列表。

```sql
CREATE TABLE tbl (i INTEGER);
CREATE SCHEMA s1;
CREATE TABLE s1.tbl (v VARCHAR);
SHOW ALL TABLES;
```

| database | schema | table_name | column_names | column_types | temporary |
|----------|--------|------------|--------------|--------------|-----------|
| memory   | main   | tbl        | [i]          | [INTEGER]    | false     |
| memory   | s0     | tbl        | [v]          | [VARCHAR]    | false     |

要查看单个表的模式，请使用 [`DESCRIBE` 命令]({% link docs/stable/guides/meta/describe.md %}).

## 参见

还定义了 SQL 标准的 [`information_schema`]({% link docs/stable/sql/meta/information_schema.md %}) 视图。此外，DuckDB 为与 SQLite 和 PostgreSQL 兼容，还定义了 `sqlite_master` 和许多 [PostgreSQL 系统目录表](https://www.postgresql.org/docs/16/catalogs.html)。