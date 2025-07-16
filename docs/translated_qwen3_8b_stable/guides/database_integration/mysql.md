---
---
layout: docu
redirect_from:
- /docs/guides/import/query_mysql
- /docs/guides/import/query_mysql/
- /docs/guides/database_integration/mysql
title: MySQL 导入
---

要直接在运行中的 MySQL 数据库上执行查询，需要使用 [`mysql` 扩展]({% link docs/stable/core_extensions/mysql.md %}).

## 安装和加载

可以使用 `INSTALL` SQL 命令安装该扩展。这只需要运行一次。

```sql
INSTALL mysql;
```

要加载 `mysql` 扩展以进行使用，使用 `LOAD` SQL 命令：

```sql
LOAD mysql;
```

## 使用

在安装了 `mysql` 扩展后，可以使用以下命令连接到 MySQL 数据库：

```sql
ATTACH 'host=localhost user=root port=0 database=mysqlscanner' AS mysql_db (TYPE mysql, READ_ONLY);
USE mysql_db;
```

`ATTACH` 使用的字符串是 PostgreSQL 风格的连接字符串（_不是_ MySQL 连接字符串！）。它是一系列以 `{key}={value}` 格式提供的连接参数。下面是有效的参数列表。未提供任何选项将使用其默认值。

| 设置      | 默认值     |
|-----------|------------|
| `database` | `NULL`     |
| `host`    | `localhost`|
| `password`|            |
| `port`    | `0`        |
| `socket`  | `NULL`     |
| `user`    | 当前用户   |

您可以直接读取和写入 MySQL 数据库：

```sql
CREATE TABLE tbl (id INTEGER, name VARCHAR);
INSERT INTO tbl VALUES (42, 'DuckDB');
```

有关支持的操作列表，请参见 [MySQL 扩展文档]({% link docs/stable/core_extensions/mysql.md %}#supported-operations).