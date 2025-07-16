---
---
layout: docu
redirect_from:
- /docs/connect
- /docs/connect/
- /docs/connect/overview
title: 连接
---

## 连接或创建数据库

要使用 DuckDB，您必须首先创建到数据库的连接。确切的语法在 [客户端 API]({% link docs/stable/clients/overview.md %}) 中有所不同，但通常涉及传递一个参数来配置持久化。

## 持久化

DuckDB 可以以持久模式运行，其中数据保存在磁盘上，也可以以内存模式运行，其中整个数据集存储在主内存中。

> 提示 无论是持久数据库还是内存数据库，都会使用磁盘溢出（spilling to disk）来支持大于内存的工作负载（即，非内存处理）。

### 持久数据库

要创建或打开一个持久数据库，请在创建连接时设置数据库文件的路径，例如 `my_database.duckdb`。
此路径可以指向一个已有的数据库，也可以指向一个尚不存在的文件，DuckDB 会根据需要在该位置打开或创建数据库。
该文件可以具有任意扩展名，但 `.db` 或 `.duckdb` 是两种常见的选择，`.ddb` 有时也会被使用。

从 v0.10 开始，DuckDB 的存储格式是 [向后兼容的]({% link docs/stable/internals/storage.md %}#backward-compatibility)，即 DuckDB 可以读取由旧版本 DuckDB 生成的数据库文件。
例如，DuckDB v0.10 可以读取并处理由之前版本 DuckDB（v0.9）创建的文件。
如需了解更多关于 DuckDB 存储格式的信息，请参阅 [存储页面]({% link docs/stable/internals/storage.md %}).

### 内存数据库

DuckDB 可以以内存模式运行。在大多数客户端中，可以通过将特殊值 `:memory:` 作为数据库文件传递，或省略数据库文件参数来激活此模式。在内存模式下，不会将任何数据持久化到磁盘，因此，当进程结束时，所有数据都会丢失。