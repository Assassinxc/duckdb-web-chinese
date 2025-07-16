---
---
github_repository: https://github.com/duckdb/duckdb-sqlite
layout: docu
title: SQLite 扩展
redirect_from:
- /docs/extensions/sqlite
- /docs/extensions/sqlite/
- /docs/stable/extensions/sqlite
- /docs/stable/extensions/sqlite/
---

SQLite 扩展允许 DuckDB 直接从 SQLite 数据库文件中读取和写入数据。可以对底层 SQLite 表中的数据直接进行查询。数据可以从 SQLite 表加载到 DuckDB 表中，也可以反过来进行。

## 安装和加载

`sqlite` 扩展将在首次使用时从官方扩展仓库中透明地[自动加载]({% link docs/stable/core_extensions/overview.md %}#autoloading-extensions)。
如果您希望手动安装和加载它，请运行：

```sql
INSTALL sqlite;
LOAD sqlite;
```

## 使用

要使 SQLite 文件对 DuckDB 可用，请使用 `ATTACH` 语句并指定 `sqlite` 或 `sqlite_scanner` 类型。附加的 SQLite 数据库支持读写操作。

例如，要附加到 [`sakila.db` 文件](https://github.com/duckdb/sqlite_scanner/raw/main/data/db/sakila.db)，请运行：

```sql
ATTACH 'sakila.db' (TYPE sqlite);
USE sakila;
```

文件中的表可以像普通 DuckDB 表一样读取，但查询时底层数据会直接从文件中的 SQLite 表读取。

```sql
SHOW TABLES;
```

<div class="monospace_table"></div>

|          name          |
|------------------------|
| actor                  |
| address                |
| category               |
| city                   |
| country                |
| customer               |
| customer_list          |
| film                   |
| film_actor             |
| film_category          |
| film_list              |
| film_text              |
| inventory              |
| language               |
| payment                |
| rental                 |
| sales_by_film_category |
| sales_by_store         |
| staff                  |
| staff_list             |
| store                  |

您可以使用 SQL 查询这些表，例如使用 [`sakila-examples.sql`](https://github.com/duckdb/sqlite_scanner/blob/main/data/sql/sakila-examples.sql) 中的示例查询：

```sql
SELECT
    cat.name AS category_name,
    sum(ifnull(pay.amount, 0)) AS revenue
FROM category cat
LEFT JOIN film_category flm_cat
       ON cat.category_id = flm_cat.category_id
LEFT JOIN film fil
       ON flm_cat.film_id = fil.film_id
LEFT JOIN inventory inv
       ON fil.film_id = inv.film_id
LEFT JOIN rental ren
       ON inv.inventory_id = ren.inventory_id
LEFT JOIN payment pay
       ON ren.rental_id = pay.rental_id
GROUP BY cat.name
ORDER BY revenue DESC
LIMIT 5;
```

## 数据类型

SQLite 是一个[弱类型数据库系统](https://www.sqlite.org/datatype3.html)。因此，存储数据到 SQLite 表时，类型不会被强制执行。以下是在 SQLite 中有效的 SQL：

```sql
CREATE TABLE numbers (i INTEGER);
INSERT INTO numbers VALUES ('hello');
```

DuckDB 是一个强类型数据库系统，因此它要求所有列都具有定义的类型，并且系统会严格检查数据的正确性。

在查询 SQLite 时，DuckDB 必须推断出特定的列类型映射。DuckDB 会遵循 SQLite 的 [类型亲和规则](https://www.sqlite.org/datatype3.html#type_affinity)，并有一些扩展。

1. 如果声明的类型包含字符串 `INT`，则将其转换为 `BIGINT` 类型。
2. 如果列的声明类型包含任何字符串 `CHAR`、`CLOB` 或 `TEXT`，则将其转换为 `VARCHAR`。
3. 如果列的声明类型包含字符串 `BLOB` 或没有指定类型，则将其转换为 `BLOB`。
4. 如果列的声明类型包含任何字符串 `REAL`、`FLOA`、`DOUB`、`DEC` 或 `NUM`，则将其转换为 `DOUBLE`。
5. 如果声明的类型是 `DATE`，则将其转换为 `DATE`。
6. 如果声明的类型包含字符串 `TIME`，则将其转换为 `TIMESTAMP`。
7. 如果以上都不适用，则将其转换为 `VARCHAR`。

由于 DuckDB 要求对应列只包含正确类型值，因此无法将字符串 "hello" 加载到 `BIGINT` 类型的列中。因此，在读取上面的 "numbers" 表时会抛出错误：

```console
类型不匹配错误：列 "i" 中的无效类型：列声明为整数，但找到 "hello" 类型为 "text"。
```

可以通过设置 `sqlite_all_varchar` 选项来避免此错误：

```sql
SET GLOBAL sqlite_all_varchar = true;
```

当设置此选项时，它会覆盖上述类型转换规则，而是始终将 SQLite 列转换为 `VARCHAR` 列。请注意，此设置必须在调用 `sqlite_attach` 之前设置。

## 直接打开 SQLite 数据库

SQLite 数据库也可以直接打开，并且可以像使用 DuckDB 数据库文件一样透明使用。在任何客户端中，连接时可以提供 SQLite 数据库文件的路径，从而打开 SQLite 数据库。

例如，使用 shell，可以按如下方式打开 SQLite 数据库：

```bash
duckdb sakila.db
```

```sql
SELECT first_name
FROM actor
LIMIT 3;
```

| first_name |
|------------|
| PENELOPE   |
| NICK       |
| ED         |

## 将数据写入 SQLite

除了从 SQLite 读取数据，该扩展还允许您创建新的 SQLite 数据库文件、创建表、将数据导入 SQLite 并使用标准 SQL 查询对 SQLite 数据库文件进行其他修改。

这使您可以使用 DuckDB 将存储在 SQLite 数据库中的数据导出为 Parquet，或将 Parquet 文件中的数据读取到 SQLite 中。

以下是创建新 SQLite 数据库并加载数据的简要示例。

```sql
ATTACH 'new_sqlite_database.db' AS sqlite_db (TYPE sqlite);
CREATE TABLE sqlite_db.tbl (id INTEGER, name VARCHAR);
INSERT INTO sqlite_db.tbl VALUES (42, 'DuckDB');
```

生成的 SQLite 数据库可以然后从 SQLite 中读取。

```bash
sqlite3 new_sqlite_database.db
```

```sql
SQLite version 3.39.5 2022-10-14 20:58:05
sqlite> SELECT * FROM tbl;
```

```text
id  name  
--  ------
42  DuckDB
```

支持许多 SQLite 表的操作。所有这些操作都会直接修改 SQLite 数据库，之后可以使用 SQLite 读取后续操作的结果。

## 并发性

DuckDB 可以在不同的线程或单独的进程中读取或修改 SQLite 数据库，而 DuckDB 或 SQLite 从不同的线程或进程读取或修改相同的数据库。同一时间可以有多个线程或进程读取 SQLite 数据库，但同一时间只能有一个线程或进程写入数据库。数据库锁定由 SQLite 库处理，而不是 DuckDB。在同一进程中，SQLite 使用互斥锁。从不同进程访问时，SQLite 使用文件系统锁。锁机制还依赖于 SQLite 的配置，如 WAL 模式。更多信息请参阅 [SQLite 的锁定文档](https://www.sqlite.org/lockingv3.html)。

> 警告 将多个 SQLite 库的副本链接到同一应用程序中可能会导致应用程序错误。更多信息请参阅 [sqlite_scanner 问题 #82](https://github.com/duckdb/sqlite_scanner/issues/82)。

## 设置

该扩展公开了以下配置参数。

| 名称                              | 描述                                                                  | 默认值 |
| --------------------------------- | ---------------------------------------------------------------------------- | ------- |
| `sqlite_debug_show_queries`       | 调试设置：打印发送到 SQLite 的所有查询到标准输出                    | `false` |

## 支持的操作

以下是支持的操作列表。

### `CREATE TABLE`

```sql
CREATE TABLE sqlite_db.tbl (id INTEGER, name VARCHAR);
```

### `INSERT INTO`

```sql
INSERT INTO sqlite_db.tbl VALUES (42, 'DuckDB');
```

### `SELECT`

```sql
SELECT * FROM sqlite_db.tbl;
```

| id |  name  |
|---:|--------|
| 42 | DuckDB |

### `COPY`

```sql
COPY sqlite_db.tbl TO 'data.parquet';
COPY sqlite_db.tbl FROM 'data.parquet';
```

### `UPDATE`

```sql
UPDATE sqlite_db.tbl SET name = 'Woohoo' WHERE id = 42;
```

### `DELETE`

```sql
DELETE FROM sqlite_db.tbl WHERE id = 42;
```

### `ALTER TABLE`

```sql
ALTER TABLE sqlite_db.tbl ADD COLUMN k INTEGER;
```

### `DROP TABLE`

```sql
DROP TABLE sqlite_db.tbl;
```

### `CREATE VIEW`

```sql
CREATE VIEW sqlite_db.v1 AS SELECT 42;
```

### 事务

```sql
CREATE TABLE sqlite_db.tmp (i INTEGER);
```

```sql
BEGIN;
INSERT INTO sqlite_db.tmp VALUES (42);
SELECT * FROM sqlite_db.tmp;
```

| i  |
|---:|
| 42 |

```sql
ROLLBACK;
SELECT * FROM sqlite_db.tmp;
```

| i |
|--:|
|   |

> 已弃用 旧的 `sqlite_attach` 函数已弃用。建议切换到新的 [`ATTACH` 语法]({% link docs/stable/sql/statements/attach.md %})。