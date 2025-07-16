---
---
layout: docu
railroad: statements/attach.js
redirect_from:
- /docs/sql/statements/attach
title: ATTACH 和 DETACH 语句
---

DuckDB 允许连接和断开数据库文件。

## 示例

使用别名从名称中推断（`file`）连接数据库 `file.db`：

```sql
ATTACH 'file.db';
```

使用显式别名（`file_db`）连接数据库 `file.db`：

```sql
ATTACH 'file.db' AS file_db;
```

以只读模式连接数据库 `file.db`：

```sql
ATTACH 'file.db' (READ_ONLY);
```

以 16 kB 的块大小连接数据库 `file.db`：

```sql
ATTACH 'file.db' (BLOCK_SIZE 16_384);
```

连接 SQLite 数据库以进行读写（有关更多信息，请参阅 [`sqlite` 扩展]({% link docs/stable/core_extensions/sqlite.md %})）：

```sql
ATTACH 'sqlite_file.db' AS sqlite_db (TYPE sqlite);
```

如果推断的数据库别名 `file` 不存在，则连接数据库 `file.db`：

```sql
ATTACH IF NOT EXISTS 'file.db';
```

如果显式数据库别名 `file_db` 不存在，则连接数据库 `file.db`：

```sql
ATTACH IF NOT EXISTS 'file.db' AS file_db;
```

将数据库 `file2.db` 作为别名 `file_db` 连接，并在存在时替换现有别名：

```sql
ATTACH OR REPLACE 'file2.db' AS file_db;
```

在连接的数据库 `file` 中创建表：

```sql
CREATE TABLE file.new_table (i INTEGER);
```

断开别名为 `file` 的数据库：

```sql
DETACH file;
```

显示所有连接的数据库列表：

```sql
SHOW DATABASES;
```

将默认数据库更改为 `file`：

```sql
USE file;
```

## `ATTACH`

`ATTACH` 语句将一个新的数据库文件添加到目录中，可以从中读取和写入。
请注意，连接定义不会在会话之间持久化：当启动一个新会话时，您必须重新连接所有数据库。

### 连接语法

<div id="rrdiagram1"></div>

`ATTACH` 允许 DuckDB 在多个数据库文件上操作，并允许在不同的数据库文件之间传输数据。

`ATTACH` 支持 HTTP 和 S3 端点。对于这些端点，默认情况下它会创建只读连接。
因此，以下两个命令是等效的：

```sql
ATTACH 'https://blobs.duckdb.org/databases/stations.duckdb' AS stations_db;
ATTACH 'https://blobs.duckdb.org/databases/stations.duckdb' AS stations_db (READ_ONLY);
```

同样，以下两个连接到 S3 的命令是等效的：

```sql
ATTACH 's3://duckdb-blobs/databases/stations.duckdb' AS stations_db;
ATTACH 's3://duckdb-blobs/databases/stations.duckdb' AS stations_db (READ_ONLY);
```

> 在 DuckDB 版本 1.1.0 之前，对于 HTTP 和 S3 端点，必须指定 `READ_ONLY` 标志。

### 显式存储版本

[DuckDB v1.2.0 引入了 `STORAGE_VERSION` 选项]({% post_url 2025-02-05-announcing-duckdb-120 %}#explicit-storage-versions)，允许显式指定存储版本。
使用此功能，您可以选择使用更新的向前不兼容功能：

```sql
ATTACH 'file.db' (STORAGE_VERSION 'v1.2.0');
```

此设置指定了能够读取数据库文件的最小 DuckDB 版本。当使用此选项写入数据库文件时，生成的文件无法被早于指定版本的 DuckDB 发行版打开。它们可以被指定版本和所有更新的 DuckDB 版本读取。

有关更多详细信息，请参阅 [“存储”页面]({% link docs/stable/internals/storage.md %}#explicit-storage-versions)。

## `DETACH`

`DETACH` 语句允许先前连接的数据库文件被关闭并断开，释放数据库文件上的任何锁。

请注意，无法从默认数据库断开：如果您希望这样做，请使用 [`USE` 语句]({% link docs/stable/sql/statements/use.md %}) 将默认数据库更改为另一个数据库。例如，如果您连接到一个持久数据库，可以通过以下命令切换到内存数据库：

```sql
ATTACH ':memory:' AS memory_db;
USE memory_db;
```

> 警告 关闭连接，例如调用 [`Python 中的 close() 函数]({% link docs/stable/clients/python/dbapi.md %}#connection)，不会释放数据库文件上的锁，因为文件句柄由主 DuckDB 实例（在 Python 中，`duckdb` 模块）持有。

### 断开语法

<div id="rrdiagram2"></div>

## 选项

| 名称         | 描述                                                                                                                 | 类型      | 默认值     |
|--------------|-----------------------------------------------------------------------------------------------------------------------------|-----------|------------|
| `access_mode` | 数据库的访问模式 (**AUTOMATIC**, **READ_ONLY**, 或 **READ_WRITE**)。                                                  | `VARCHAR` | `automatic` |
| `type`        | 文件类型 (**DUCKDB** 或 **SQLITE**)，或从输入字符串字面量推导（MySQL, PostgreSQL）。                                   | `VARCHAR` | `DUCKDB`   |
| `block_size`  | 新数据库文件的块大小。必须是 2 的幂，并且在 [16384, 262144] 范围内。不能为现有文件设置此值。                        | `UBIGINT` | `262144`   |

## 名称限定

目录对象的完全限定名称包含 *目录*、*模式* 和 *对象名*。例如：

连接数据库 `new_db`：

```sql
ATTACH 'new_db.db';
```

在数据库 `new_db` 中创建模式 `my_schema`：

```sql
CREATE SCHEMA new_db.my_schema;
```

在模式 `my_schema` 中创建表 `my_table`：

```sql
CREATE TABLE new_db.my_schema.my_table (col INTEGER);
```

引用表 `my_table` 中的列 `col`：

```sql
SELECT new_db.my_schema.my_table.col FROM new_db.my_schema.my_table;
```

请注意，通常不需要完全限定名称。当名称未完全限定时，系统会使用 *目录搜索路径* 来查找要引用的条目。默认的目录搜索路径包括系统目录、临时目录和最初连接的数据库，以及 `main` 模式。

另外请注意 [标识符和数据库名称的规则]({% link docs/stable/sql/dialect/keywords_and_identifiers.md %}#database-names)。

### 默认数据库和模式

当创建表时没有指定任何限定符，表将在默认数据库的默认模式中创建。默认数据库是在系统创建时启动的数据库，而默认模式是 `main`。

在默认数据库中创建表 `my_table`：

```sql
CREATE TABLE my_table (col INTEGER);
```

### 更改默认数据库和模式

可以使用 `USE` 命令更改默认数据库和模式。

将默认数据库模式设置为 `new_db.main`：

```sql
USE new_db;
```

将默认数据库模式设置为 `new_db.my_schema`：

```sql
USE new_db.my_schema;
```

### 解决冲突

当只提供一个限定符时，系统可以将其解释为 *目录* 或 *模式*，只要没有冲突。例如：

```sql
ATTACH 'new_db.db';
CREATE SCHEMA my_schema;
```

创建表 `new_db.main.tbl`：

```sql
CREATE TABLE new_db.tbl (i INTEGER);
```

创建表 `default_db.my_schema.tbl`：

```sql
CREATE TABLE my_schema.tbl (i INTEGER);
```

如果我们创建冲突（即，同时有同名的模式和目录），系统会要求使用完全限定路径：

```sql
CREATE SCHEMA new_db;
CREATE TABLE new_db.tbl (i INTEGER);
```

```console
Binder 错误：
对目录或模式 "new_db" 的模糊引用 - 请使用完全限定路径，例如 "memory.new_db"
```

### 更改目录搜索路径

可以通过设置 `search_path` 配置选项来调整目录搜索路径，该选项使用逗号分隔的值列表，这些值将出现在搜索路径中。以下示例演示了在两个数据库中搜索：

```sql
ATTACH ':memory:' AS db1;
ATTACH ':memory:' AS db2;
CREATE table db1.tbl1 (i INTEGER);
CREATE table db2.tbl2 (j INTEGER);
```

使用完全限定名称引用表：

```sql
SELECT * FROM db1.tbl1;
SELECT * FROM db2.tbl2;
```

或者设置搜索路径并使用表名引用表：

```sql
SET search_path = 'db1,db2';
SELECT * FROM tbl1;
SELECT * FROM tbl2;
```

## 事务语义

在多个数据库上运行查询时，系统会为每个数据库打开独立的事务。默认情况下，事务是*延迟*启动的 —— 当查询中首次引用某个数据库时，会为该数据库启动事务。可以通过 `SET immediate_transaction_mode = true` 来切换此行为，使其在所有连接的数据库中立即启动事务。

虽然可以同时有多个事务活动 —— 系统只支持在单个事务中对单个连接的数据库进行*写入*。如果您尝试在单个事务中向多个连接的数据库写入，将抛出以下错误：

```console
试图在已经修改数据库 "db1" 的事务中向数据库 "db2" 写入 -
单个事务只能向单个连接的数据库写入。
```

这个限制的原因是，系统不维护跨连接数据库的事务原子性。事务只在每个数据库文件内部是原子的。通过限制全局事务只能写入单个数据库文件，可以保持原子性保证。