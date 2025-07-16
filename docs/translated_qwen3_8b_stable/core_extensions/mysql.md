---
---
github_repository: https://github.com/duckdb/duckdb-mysql
layout: docu
title: MySQL 扩展
redirect_from:
- /docs/extensions/mysql
- /docs/extensions/mysql/
- /docs/stable/extensions/mysql
- /docs/stable/extensions/mysql/
---

MySQL 扩展允许 DuckDB 直接从运行中的 MySQL 实例读取和写入数据。数据可以直接从底层的 MySQL 数据库进行查询。数据可以从 MySQL 表加载到 DuckDB 表，也可以反过来。

## 安装和加载

要安装 `mysql` 扩展，请运行：

```sql
INSTALL mysql;
```

扩展在首次使用时会自动加载。如果您更倾向于手动加载，可以运行：

```sql
LOAD mysql;
```

## 从 MySQL 读取数据

要使 MySQL 数据库对 DuckDB 可用，请使用 `ATTACH` 命令并指定 `mysql` 或 `mysql_scanner` 类型：

```sql
ATTACH 'host=localhost user=root port=0 database=mysql' AS mysqldb (TYPE mysql);
USE mysqldb;
```

### 配置

连接字符串决定了如何连接到 MySQL 的一组 `key=value` 参数。未提供任何选项的参数将被替换为其默认值，如下面的表格所示。连接信息也可以通过 [环境变量](https://dev.mysql.com/doc/refman/8.3/en/environment-variables.html) 指定。如果没有显式提供选项，MySQL 扩展将尝试从环境变量中读取。

<div class="monospace_table"></div>

| 设置     | 默认值        | 环境变量         |
|----------|--------------|------------------|
| database | NULL         | MYSQL_DATABASE   |
| host     | localhost    | MYSQL_HOST       |
| password |              | MYSQL_PWD        |
| port     | 0            | MYSQL_TCP_PORT   |
| socket   | NULL         | MYSQL_UNIX_PORT  |
| user     | _current user_ | MYSQL_USER       |
| ssl_mode | preferred    |                  |
| ssl_ca   |              |                  |
| ssl_capath |            |                  |
| ssl_cert |              |                  |
| ssl_cipher |            |                  |
| ssl_crl |              |                  |
| ssl_crlpath |           |                  |
| ssl_key |              |                  |

### 通过 Secrets 配置

MySQL 连接信息也可以通过 [secrets](/docs/configuration/secrets_manager) 指定。可以使用以下语法创建一个 secret。

```sql
CREATE SECRET (
    TYPE mysql,
    HOST '127.0.0.1',
    PORT 0,
    DATABASE mysql,
    USER 'mysql',
    PASSWORD ''
);
```

当调用 `ATTACH` 时，secret 中的信息将被使用。我们可以留空连接字符串，以使用 secret 中存储的所有信息。

```sql
ATTACH '' AS mysql_db (TYPE mysql);
```

我们也可以使用连接字符串来覆盖单个选项。例如，要连接到不同的数据库，同时仍使用相同的凭据，可以仅覆盖数据库名称，如下所示。

```sql
ATTACH 'database=my_other_db' AS mysql_db (TYPE mysql);
```

默认情况下，创建的 secrets 是临时的。可以使用 [`CREATE PERSISTENT SECRET` 命令]({% link docs/stable/configuration/secrets_manager.md %}#persistent-secrets) 持久化 secrets。持久化 secrets 可以跨会话使用。

#### 管理多个 Secrets

可以使用命名 secrets 来管理多个 MySQL 数据库实例的连接。在创建时，可以为 secrets 指定名称。

```sql
CREATE SECRET mysql_secret_one (
    TYPE mysql,
    HOST '127.0.0.1',
    PORT 0,
    DATABASE mysql,
    USER 'mysql',
    PASSWORD ''
);
```

然后可以通过 `ATTACH` 中的 `SECRET` 参数显式引用 secret。

```sql
ATTACH '' AS mysql_db_one (TYPE mysql, SECRET mysql_secret_one);
```

### SSL 连接

[`ssl` 连接参数](https://dev.mysql.com/doc/refman/8.4/en/using-encrypted-connections.html) 可用于建立 SSL 连接。下面是支持的参数描述。

| 设置     | 描述                                                                                                                                      |
|----------|-------------------------------------------------------------------------------------------------------------------------------------------|
| ssl_mode | 用于连接到服务器的安全状态：`disabled, required, verify_ca, verify_identity or preferred`（默认值：`preferred`）                       |
| ssl_ca   | 证书颁发机构（CA）证书文件的路径名称                                                                                                     |
| ssl_capath | 包含受信任的 SSL CA 证书文件的目录路径名称                                                                                               |
| ssl_cert | 客户端公钥证书文件的路径名称                                                                                                             |
| ssl_cipher | SSL 加密允许的密码列表                                                                                                                  |
| ssl_crl | 包含证书吊销列表的文件路径名称                                                                                                           |
| ssl_crlpath | 包含证书吊销列表文件的目录路径名称                                                                                                       |
| ssl_key | 客户端私钥文件的路径名称                                                                                                                 |

### 读取 MySQL 表

MySQL 数据库中的表可以像普通的 DuckDB 表一样读取，但底层数据在查询时直接从 MySQL 读取。

```sql
SHOW ALL TABLES;
```

<div class="monospace_table"></div>

|      name       |
|-----------------|
| signed_integers |

```sql
SELECT * FROM signed_integers;
```

<div class="monospace_table"></div>

|  t   |   s    |    m     |      i      |          b           |
|-----:|-------:|---------:|------------:|---------------------:|
| -128 | -32768 | -8388608 | -2147483648 | -9223372036854775808 |
| 127  | 32767  | 8388607  | 2147483647  | 9223372036854775807  |
| NULL | NULL   | NULL     | NULL        | NULL                 |

为了防止系统不断从 MySQL 重新读取表，特别是对于大表，可能需要在 DuckDB 中创建 MySQL 数据库的副本。

可以使用标准 SQL 将数据从 MySQL 复制到 DuckDB，例如：

```sql
CREATE TABLE duckdb_table AS FROM mysqlscanner.mysql_table;
```

## 写入数据到 MySQL

除了从 MySQL 读取数据，还可以使用标准 SQL 查询创建表、将数据摄入 MySQL 并对 MySQL 数据库进行其他修改。

这允许您使用 DuckDB 将存储在 MySQL 数据库中的数据导出为 Parquet，或从 Parquet 文件中读取数据到 MySQL。

下面是创建 MySQL 中新表并加载数据的简要示例。

```sql
ATTACH 'host=localhost user=root port=0 database=mysqlscanner' AS mysql_db (TYPE mysql);
CREATE TABLE mysql_db.tbl (id INTEGER, name VARCHAR);
INSERT INTO mysql_db.tbl VALUES (42, 'DuckDB');
```

许多 MySQL 表的操作都受到支持。所有这些操作都会直接修改 MySQL 数据库，并且后续操作的结果可以通过 MySQL 读取。请注意，如果不想进行修改，可以使用带有 `READ_ONLY` 属性的 `ATTACH`，以防止对底层数据库进行修改。例如：

```sql
ATTACH 'host=localhost user=root port=0 database=mysqlscanner' AS mysql_db (TYPE mysql, READ_ONLY);
```

## 支持的操作

以下是支持的操作列表。

### `CREATE TABLE`

```sql
CREATE TABLE mysql_db.tbl (id INTEGER, name VARCHAR);
```

### `INSERT INTO`

```sql
INSERT INTO mysql_db.tbl VALUES (42, 'DuckDB');
```

### `SELECT`

```sql
SELECT * FROM mysql_db.tbl;
```

| id |  name  |
|---:|--------|
| 42 | DuckDB |

### `COPY`

```sql
COPY mysql_db.tbl TO 'data.parquet';
COPY mysql_db.tbl FROM 'data.parquet';
```

您也可以使用 [`COPY FROM DATABASE` 语句]({% link docs/stable/sql/statements/copy.md %}#copy-from-database--to) 创建数据库的完整副本：

```sql
COPY FROM DATABASE mysql_db TO my_duckdb_db;
```

### `UPDATE`

```sql
UPDATE mysql_db.tbl
SET name = 'Woohoo'
WHERE id = 42;
```

### `DELETE`

```sql
DELETE FROM mysql_db.tbl
WHERE id = 42;
```

### `ALTER TABLE`

```sql
ALTER TABLE mysql_db.tbl
ADD COLUMN k INTEGER;
```

### `DROP TABLE`

```sql
DROP TABLE mysql_db.tbl;
```

### `CREATE VIEW`

```sql
CREATE VIEW mysql_db.v1 AS SELECT 42;
```

### `CREATE SCHEMA` 和 `DROP SCHEMA`

```sql
CREATE SCHEMA mysql_db.s1;
CREATE TABLE mysql_db.s1.integers (i INTEGER);
INSERT INTO mysql_db.s1.integers VALUES (42);
SELECT * FROM mysql_db.s1.integers;
```

| i  |
|---:|
| 42 |

```sql
DROP SCHEMA mysql_db.s1;
```

### 事务

```sql
CREATE TABLE mysql_db.tmp (i INTEGER);
BEGIN;
INSERT INTO mysql_db.tmp VALUES (42);
SELECT * FROM mysql_db.tmp;
```

这将返回：

| i  |
|---:|
| 42 |

```sql
ROLLBACK;
SELECT * FROM mysql_db.tmp;
```

这将返回一个空表。

> MySQL 中的 DDL 语句不是事务性的。

## 在 MySQL 中运行 SQL 查询

### `mysql_query` 表函数

`mysql_query` 表函数允许您在附加的数据库中运行任意的读取查询。`mysql_query` 接收要执行查询的附加 MySQL 数据库名称以及要执行的 SQL 查询。查询的结果将被返回。单引号字符串通过重复单引号来转义。

```sql
mysql_query(attached_database::VARCHAR, query::VARCHAR)
```

例如：

```sql
ATTACH 'host=localhost database=mysql' AS mysqldb (TYPE mysql);
SELECT * FROM mysql_query('mysqldb', 'SELECT * FROM cars LIMIT 3');
```

### `mysql_execute` 函数

`mysql_execute` 函数允许在 MySQL 中运行任意查询，包括更新数据库模式和内容的语句。

```sql
ATTACH 'host=localhost database=mysql' AS mysqldb (TYPE mysql);
CALL mysql_execute('mysqldb', 'CREATE TABLE my_table (i INTEGER)');
```

## 设置

|                 名称                 |                          描述                           | 默认值  |
|--------------------------------------|----------------------------------------------------------------|---------|
| `mysql_bit1_as_boolean`              | 是否将 `BIT(1)` 列转换为 `BOOLEAN`                         | `true`  |
| `mysql_debug_show_queries`           | DEBUG 设置：打印发送到 MySQL 的所有查询到标准输出         | `false` |
| `mysql_experimental_filter_pushdown` | 是否使用过滤下推（当前为实验性功能）                       | `false` |
| `mysql_tinyint1_as_boolean`          | 是否将 `TINYINT(1)` 列转换为 `BOOLEAN`                     | `true`  |

## 模式缓存

为了避免持续从 MySQL 获取模式数据，DuckDB 会缓存模式信息，例如表名、列名等。如果通过其他连接到 MySQL 实例对模式进行了更改（例如向表中添加了新列），缓存的模式信息可能会过时。在这种情况下，可以执行 `mysql_clear_cache` 函数来清除内部缓存。

```sql
CALL mysql_clear_cache();
```