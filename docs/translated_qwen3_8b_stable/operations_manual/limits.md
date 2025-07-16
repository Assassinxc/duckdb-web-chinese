---
---
layout: docu
redirect_from:
- /docs/operations_manual/limits
title: 限制
---

本页面包含DuckDB的内置限制值。

## 限制值

| 限制 | 默认值 | 配置选项 | 说明 |
|---|---|---|---|
| 数组大小 | 100000 | - | |
| BLOB大小 | 4 GB | - | |
| 表达式深度 | 1000 | [`max_expression_depth`]({% link docs/stable/configuration/overview.md %}) | |
| 向量内存分配 | 128 GB | - | |
| 内存使用 | RAM的80% | [`memory_limit`]({% link docs/stable/configuration/pragmas.md %}#memory-limit) | 注意：此限制仅适用于缓冲区管理器。 |
| 字符串大小 | 4 GB | - | |
| 临时目录大小 | 无限制 | [`max_temp_directory_size`]({% link docs/stable/configuration/overview.md %}) | |

## 数据库文件大小

DuckDB对单个DuckDB数据库文件的大小没有实际限制。
我们有使用15 TB+磁盘空间的数据库文件，并且它们运行良好。
不过，连接到如此巨大的数据库可能需要几秒钟，而且[检查点]({% link docs/stable/sql/statements/checkpoint.md %})可能会变慢。