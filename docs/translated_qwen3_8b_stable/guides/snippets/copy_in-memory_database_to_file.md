---
---
layout: docu
redirect_from:
- /docs/guides/snippets/copy_in-memory_database_to_file
title: 将内存数据库复制到文件
---

想象以下场景 – 你以内存模式启动了DuckDB，但希望将数据库的状态持久化到磁盘。
要实现此目的，请**连接到一个新的基于磁盘的数据库**，并使用 [`COPY FROM DATABASE ... TO` 命令]({% link docs/stable/sql/statements/copy.md %}#copy-from-database--to)：

```sql
ATTACH 'my_database.db';
COPY FROM DATABASE memory TO my_database;
DETACH my_database;
```

> 在连接到该数据库文件之前，请确保该基于磁盘的数据库文件不存在。