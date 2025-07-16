---
---
github_repository: https://github.com/duckdb/duckdb-postgres
layout: docu
title: PostgreSQL 扩展
redirect_from:
- /docs/extensions/postgres
- /docs/extensions/postgres/
- /docs/stable/extensions/postgres
- /docs/stable/extensions/postgres/
---

`postgres` 扩展允许 DuckDB 直接从正在运行的 PostgreSQL 数据库实例中读取和写入数据。数据可以直接从底层 PostgreSQL 数据库进行查询。数据可以从 PostgreSQL 表加载到 DuckDB 表，也可以反过来。有关实现细节和背景信息，请参阅[官方公告]({% post_url 2022-09-30-postgres-scanner %})。

## 安装和加载

`postgres` 扩展将在首次使用时从官方扩展仓库中透明地[自动加载]({% link docs/stable/core_extensions/overview.md %}#autoloading-extensions)。
如果您希望手动安装和加载它，请运行：

```sql
INSTALL postgres;
LOAD postgres;
```

## 连接

要使 PostgreSQL 数据库对 DuckDB 可用，使用 `ATTACH` 命令并指定 `postgres` 或 `postgres_scanner` 类型。

要以读写模式连接到运行在本地主机上的 PostgreSQL 实例的 `public` 模式，请运行：

```sql
ATTACH '' AS postgres_db (TYPE postgres);
```

要以只读模式连接到具有给定参数的 PostgreSQL 实例，请运行：

```sql
ATTACH 'dbname=postgres user=postgres host=127.0.0.1' AS db (TYPE postgres, READ_ONLY);
```

默认情况下，会附加所有模式。在处理大型实例时，仅附加特定模式可能很有用。这可以通过使用 `SCHEMA` 命令实现。

```sql
ATTACH 'dbname=postgres user=postgres host=127.0.0.1' AS db (TYPE postgres, SCHEMA 'public');
```

### 配置

`ATTACH` 命令接受一个 [`libpq` 连接字符串](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING)
或一个 [PostgreSQL URI](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING-URIS) 作为输入。

以下是一些示例连接字符串和常用参数。完整的可用参数列表请参阅[PostgreSQL 文档](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-PARAMKEYWORDS)。

```text
dbname=postgresscanner
host=localhost port=5432 dbname=mydb connect_timeout=10
```

| 名称       | 描述                          | 默认值        |
| ---------- | ------------------------------------ | -------------- |
| `dbname`   | 数据库名称                        | [user]         |
| `host`     | 要连接的主机名称           | `localhost`    |
| `hostaddr` | 主机 IP 地址                      | `localhost`    |
| `passfile` | 密码存储的文件名 | `~/.pgpass`    |
| `password` | PostgreSQL 密码                  | (空)        |
| `port`     | 端口号                          | `5432`         |
| `user`     | PostgreSQL 用户名                 | _当前用户_ |

一个示例 URI 是 `postgresql://username@hostname/dbname`。

### 通过 Secrets 配置

PostgreSQL 连接信息也可以通过 [secrets](/docs/configuration/secrets_manager) 指定。以下语法可用于创建 secret。

```sql
CREATE SECRET (
    TYPE postgres,
    HOST '127.0.0.1',
    PORT 5432,
    DATABASE postgres,
    USER 'postgres',
    PASSWORD ''
);
```

在调用 `ATTACH` 时会使用 secret 中的信息。我们可以通过留空 PostgreSQL 连接字符串来使用 secret 中存储的所有信息。

```sql
ATTACH '' AS postgres_db (TYPE postgres);
```

我们可以通过 PostgreSQL 连接字符串覆盖个别选项。例如，要连接到不同的数据库同时仍使用相同的凭据，可以仅覆盖数据库名称，如下所示。

```sql
ATTACH 'dbname=my_other_db' AS postgres_db (TYPE postgres);
```

默认情况下，创建的 secrets 是临时的。可以使用 [`CREATE PERSISTENT SECRET` 命令]({% link docs/stable/configuration/secrets_manager.md %}#persistent-secrets) 保留 secrets。持久化 secrets 可以在会话之间使用。

#### 管理多个 Secrets

可以使用命名 secrets 来管理多个 PostgreSQL 数据库实例的连接。在创建时可以为 secrets 指定名称。

```sql
CREATE SECRET postgres_secret_one (
    TYPE postgres,
    HOST '127.0.0.1',
    PORT 5432,
    DATABASE postgres,
    USER 'postgres',
    PASSWORD ''
);
```

然后可以在 `ATTACH` 中使用 `SECRET` 参数显式引用 secret。

```sql
ATTACH '' AS postgres_db_one (TYPE postgres, SECRET postgres_secret_one);
```

### 通过环境变量配置

PostgreSQL 连接信息也可以通过 [环境变量](https://www.postgresql.org/docs/current/libpq-envars.html) 指定。
这在生产环境中特别有用，因为连接信息由外部管理并传入到环境变量中。

```bash
export PGPASSWORD="secret"
export PGHOST=localhost
export PGUSER=owner
export PGDATABASE=mydatabase
```

然后，要连接，请启动 `duckdb` 进程并运行：

```sql
ATTACH '' AS p (TYPE postgres);
```

## 使用

PostgreSQL 数据库中的表可以像普通的 DuckDB 表一样读取，但在查询时会直接从 PostgreSQL 读取底层数据。

```sql
SHOW ALL TABLES;
```

<div class="monospace_table"></div>

| name  |
| ----- |
| uuids |

```sql
SELECT * FROM uuids;
```

<div class="monospace_table"></div>

| u                                    |
| ------------------------------------ |
| 6d3d2541-710b-4bde-b3af-4711738636bf |
| NULL                                 |
| 00000000-0000-0000-0000-000000000001 |
| ffffffff-ffff-ffff-ffff-ffffffffffff |

为了防止系统持续从 PostgreSQL 重新读取表，特别是对于大型表，可能希望在 DuckDB 中创建 PostgreSQL 数据库的副本。

可以使用标准 SQL 将数据从 PostgreSQL 复制到 DuckDB，例如：

```sql
CREATE TABLE duckdb_table AS FROM postgres_db.postgres_tbl;
```

## 将数据写入 PostgreSQL

除了从 PostgreSQL 读取数据，该扩展还允许您使用标准 SQL 查询创建表、将数据写入 PostgreSQL 并对 PostgreSQL 数据库进行其他修改。

这使您可以使用 DuckDB 将存储在 PostgreSQL 数据库中的数据导出到 Parquet，或从 Parquet 文件读取数据到 PostgreSQL。

以下是一个在 PostgreSQL 中创建新表并加载数据的简要示例。

```sql
ATTACH 'dbname=postgresscanner' AS postgres_db (TYPE postgres);
CREATE TABLE postgres_db.tbl (id INTEGER, name VARCHAR);
INSERT INTO postgres_db.tbl VALUES (42, 'DuckDB');
```

支持对 PostgreSQL 表的许多操作。所有这些操作都直接修改 PostgreSQL 数据库，然后可以使用 PostgreSQL 读取后续操作的结果。
请注意，如果不想进行修改，可以使用 `READ_ONLY` 属性运行 `ATTACH`，以防止修改底层数据库。例如：

```sql
ATTACH 'dbname=postgresscanner' AS postgres_db (TYPE postgres, READ_ONLY);
```

以下是支持的操作列表。

### `CREATE TABLE`

```sql
CREATE TABLE postgres_db.tbl (id INTEGER, name VARCHAR);
```

### `INSERT INTO`

```sql
INSERT INTO postgres_db.tbl VALUES (42, 'DuckDB');
```

### `SELECT`

```sql
SELECT * FROM postgres_db.tbl;
```

|   id | name   |
| ---: | ------ |
|   42 | DuckDB |

### `COPY`

可以在 PostgreSQL 和 DuckDB 之间复制表：

```sql
COPY postgres_db.tbl TO 'data.parquet';
COPY postgres_db.tbl FROM 'data.parquet';
```

这些复制操作使用 [PostgreSQL 二进制线编码](https://www.postgresql.org/docs/current/sql-copy.html)。
DuckDB 还可以使用这种编码将数据写入文件，您可以选择使用自己的客户端将文件加载到 PostgreSQL 中，如果您想自行管理连接：

```sql
COPY 'data.parquet' TO 'pg.bin' WITH (FORMAT postgres_binary);
```

生成的文件相当于使用 DuckDB 将文件复制到 PostgreSQL，然后使用 `psql` 或其他客户端从 PostgreSQL 导出：

DuckDB:

```sql
COPY postgres_db.tbl FROM 'data.parquet';
```

PostgreSQL:

```sql
\copy tbl TO 'data.bin' WITH (FORMAT BINARY);
```

您还可以使用 [`COPY FROM DATABASE` 语句]({% link docs/stable/sql/statements/copy.md %}#copy-from-database--to) 创建数据库的完整副本：

```sql
COPY FROM DATABASE postgres_db TO my_duckdb_db;
```

### `UPDATE`

```sql
UPDATE postgres_db.tbl
SET name = 'Woohoo'
WHERE id = 42;
```

### `DELETE`

```sql
DELETE FROM postgres_db.tbl
WHERE id = 42;
```

### `ALTER TABLE`

```sql
ALTER TABLE postgres_db.tbl
ADD COLUMN k INTEGER;
```

### `DROP TABLE`

```sql
DROP TABLE postgres_db.tbl;
```

### `CREATE VIEW`

```sql
CREATE VIEW postgres_db.v1 AS SELECT 42;
```

### `CREATE SCHEMA` / `DROP SCHEMA`

```sql
CREATE SCHEMA postgres_db.s1;
CREATE TABLE postgres_db.s1.integers (i INTEGER);
INSERT INTO postgres_db.s1.integers VALUES (42);
SELECT * FROM postgres_db.s1.integers;
```

|    i |
| ---: |
|   42 |

```sql
DROP SCHEMA postgres_db.s1;
```

## `DETACH`

```sql
DETACH postgres_db;
```

### 事务

```sql
CREATE TABLE postgres_db.tmp (i INTEGER);
BEGIN;
INSERT INTO postgres_db.tmp VALUES (42);
SELECT * FROM postgres_db.tmp;
```

此返回：

|    i |
| ---: |
|   42 |

```sql
ROLLBACK;
SELECT * FROM postgres_db.tmp;
```

此返回一个空表。

## 在 PostgreSQL 中运行 SQL 查询

### `postgres_query` 表函数

`postgres_query` 表函数允许您在附加的数据库中运行任意的读取查询。`postgres_query` 接收要执行查询的附加 PostgreSQL 数据库名称以及要执行的 SQL 查询。查询的结果将返回。单引号字符串通过重复单引号来转义。

```sql
postgres_query(attached_database::VARCHAR, query::VARCHAR)
```

例如：

```sql
ATTACH 'dbname=postgresscanner' AS postgres_db (TYPE postgres);
SELECT * FROM postgres_query('postgres_db', 'SELECT * FROM cars LIMIT 3');
```

<!--
    CREATE TABLE cars (brand VARCHAR, model VARCHAR, color VARCHAR);
    INSERT INTO cars VALUES
      ('Ferrari', 'Testarossa', 'red'),
      ('Aston Martin', 'DB2', 'blue'),
      ('Bentley', 'Mulsanne', 'gray')
    ;
-->

| brand        | model      | color |
| ------------ | ---------- | ----- |
| Ferrari      | Testarossa | red   |
| Aston Martin | DB2        | blue  |
| Bentley      | Mulsanne   | gray  |

### `postgres_execute` 函数

`postgres_execute` 函数允许在 PostgreSQL 中运行任意查询，包括更新数据库模式和内容的语句。

```sql
ATTACH 'dbname=postgresscanner' AS postgres_db (TYPE postgres);
CALL postgres_execute('postgres_db', 'CREATE TABLE my_table (i INTEGER)');
```

## 设置

该扩展公开了以下配置参数。

| 名称                              | 描述                                                                  | 默认值 |
| --------------------------------- | ---------------------------------------------------------------------------- | ------- |
| `pg_array_as_varchar`             | 将 PostgreSQL 数组读取为 varchar - 启用读取混合维度数组 | `false` |
| `pg_connection_cache`             | 是否使用连接缓存                                   | `true`  |
| `pg_connection_limit`             | 最大并发 PostgreSQL 连接数                      | `64`    |
| `pg_debug_show_queries`           | DEBUG 设置：打印发送到 PostgreSQL 的所有查询到标准输出                | `false` |
| `pg_experimental_filter_pushdown` | 是否使用过滤下推（目前实验性）               | `true`  |
| `pg_pages_per_task`               | 每个任务的页面数量                                                 | `1000`  |
| `pg_use_binary_copy`              | 是否使用 BINARY 复制读取数据                               | `true`  |
| `pg_null_byte_replacement`        | 写入 Postgres 时，将 NULL 字节替换为给定字符   | `NULL`  |
| `pg_use_ctid_scan`                | 是否使用表 ctids 并行扫描                     | `true`  |

## 模式缓存

为了避免必须持续从 PostgreSQL 获取模式数据，DuckDB 会缓存模式信息，如表名、列名等。如果通过其他连接对 PostgreSQL 实例的模式进行了更改，例如向表中添加了新列，缓存的模式信息可能会过时。在这种情况下，可以执行 `pg_clear_cache` 函数来清除内部缓存。

```sql
CALL pg_clear_cache();
```

> 已弃用 旧的 `postgres_attach` 函数已弃用。建议切换到新的 `ATTACH` 语法。