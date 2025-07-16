---
---
layout: docu
redirect_from:
- /docs/guides/import/query_postgres
- /docs/guides/import/query_postgres/
- /docs/guides/database_integration/postgres
title: PostgreSQL 导入
---

要在运行中的 PostgreSQL 数据库上直接执行查询，需要使用 [`postgres` 扩展]({% link docs/stable/core_extensions/postgres.md %}）。

## 安装和加载

可以使用 `INSTALL` SQL 命令安装该扩展。这只需要运行一次。

```sql
INSTALL postgres;
```

要加载 `postgres` 扩展以便使用，使用 `LOAD` SQL 命令：

```sql
LOAD postgres;
```

## 使用

安装了 `postgres` 扩展后，可以使用 `postgres_scan` 函数从 PostgreSQL 查询表：

```sql
-- 从数据库 "mydb" 的 schema "public" 中扫描表 "mytable"
SELECT * FROM postgres_scan('host=localhost port=5432 dbname=mydb', 'public', 'mytable');
```

`postgres_scan` 函数的第一个参数是 [PostgreSQL 连接字符串](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING)，它以 `{key}={value}` 格式提供了一组连接参数。以下是有效的参数列表。

| 名称       | 描述                          | 默认值        |
| ---------- | ----------------------------- | -------------- |
| `host`     | 要连接的主机名                 | `localhost`    |
| `hostaddr` | 主机 IP 地址                  | `localhost`    |
| `port`     | 端口号                        | `5432`         |
| `user`     | PostgreSQL 用户名             | [操作系统用户名] |
| `password` | PostgreSQL 密码               |                |
| `dbname`   | 数据库名称                    | [用户名]       |
| `passfile` | 存储密码的文件名              | `~/.pgpass`    |

或者，可以使用 `ATTACH` 命令将整个数据库附加进来。这允许你像查询普通数据库一样查询 PostgreSQL 数据库中的所有表。

```sql
-- 使用给定的连接字符串附加 PostgreSQL 数据库
ATTACH 'host=localhost port=5432 dbname=mydb' AS test (TYPE postgres);
-- 现在可以像查询普通表一样查询表 "tbl_name"
SELECT * FROM test.tbl_name;
-- 将活动数据库切换为 "test"
USE test;
-- 列出所有表
SHOW TABLES;
```

如需更多信息，请参阅 [PostgreSQL 扩展文档]({% link docs/stable/core_extensions/postgres.md %})。