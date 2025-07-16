---
---
layout: docu
redirect_from:
- /docs/operations_manual/footprint_of_duckdb/reclaiming_space
title: 空间回收
---

DuckDB 使用单文件格式，这在回收磁盘空间方面存在一些固有的限制。

## `CHECKPOINT`

要回收删除行后释放的空间，请使用 [`CHECKPOINT` 语句]({% link docs/stable/sql/statements/checkpoint.md %} )。

## `VACUUM`

[`VACUUM` 语句]({% link docs/stable/sql/statements/vacuum.md %} ) 不会触发删除操作的清理，因此不会回收空间。

## 通过复制进行数据库压缩

要压缩数据库，您可以使用 [`COPY FROM DATABASE` 语句]({% link docs/stable/sql/statements/copy.md %}#copy-from-database--to) 创建数据库的新鲜副本。在以下示例中，我们首先连接到原始数据库 `db1`，然后连接到新的（空）数据库 `db2`。接着，我们将 `db1` 的内容复制到 `db2`。

```sql
ATTACH 'db1.db' AS db1;
ATTACH 'db2.db' AS db2;
COPY FROM DATABASE db1 TO db2;
```