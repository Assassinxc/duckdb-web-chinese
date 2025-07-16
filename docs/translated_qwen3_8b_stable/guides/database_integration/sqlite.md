---
---
layout: docu
redirect_from:
- /docs/guides/import/query_sqlite
- /docs/guides/import/query_sqlite/
- /docs/guides/database_integration/sqlite
title: SQLite 导入
---

要直接在 SQLite 文件上运行查询，需要使用 `sqlite` 扩展。

## 安装和加载

可以使用 `INSTALL` SQL 命令安装该扩展。这只需要运行一次。

```sql
INSTALL sqlite;
```

要加载 `sqlite` 扩展以供使用，请使用 `LOAD` SQL 命令：

```sql
LOAD sqlite;
```

## 使用

安装 SQLite 扩展后，可以使用 `sqlite_scan` 函数从 SQLite 查询表：

```sql
-- 从 SQLite 文件 "test.db" 扫描表 "tbl_name"
SELECT * FROM sqlite_scan('test.db', 'tbl_name');
```

或者，可以使用 `ATTACH` 命令将整个文件附加。这允许您像查询普通数据库一样查询 SQLite 数据库文件中的所有表。

```sql
-- 附加 SQLite 文件 "test.db"
ATTACH 'test.db' AS test (TYPE sqlite);
-- 现在可以像查询普通表一样查询表 "tbl_name"
SELECT * FROM test.tbl_name;
-- 切换到 "test" 数据库
USE test;
-- 列出文件中的所有表
SHOW TABLES;
```

如需更多信息，请参阅 [SQLite 扩展文档]({% link docs/stable/core_extensions/sqlite.md %})。