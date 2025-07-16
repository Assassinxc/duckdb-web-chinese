---
---
layout: docu
redirect_from:
- /docs/connect/concurrency
title: 并发
---

## 并发处理

DuckDB 提供了两种可配置的并发选项：

1. 一个进程可以同时读写数据库。
2. 多个进程可以读取数据库，但不能写入（`access_mode = 'READ_ONLY'`）({% link docs/stable/configuration/overview.md %}#configuration-reference)。

使用选项 1 时，DuckDB 通过结合 [MVCC (多版本并发控制)](https://en.wikipedia.org/wiki/Multiversion_concurrency_control) 和乐观并发控制（详见 [单进程内的并发](#concurrency-within-a-single-process)），支持多个写入线程，但所有操作都在同一个写入进程中进行。这种并发模型的原因是为了在内存中缓存数据以加快分析查询，而不是在每次查询时来回读取磁盘。它还允许缓存函数指针、数据库目录和其他项目，从而使同一连接上的后续查询更快。

> DuckDB 优化了批量操作，因此执行许多小事务并不是主要的设计目标。

## 单进程内的并发

DuckDB 根据以下规则支持单进程内的并发。只要没有写冲突，多个并发写入操作将成功。追加操作永远不会冲突，即使是在同一张表上。多个线程也可以同时更新不同的表或同一张表的不同子集。当两个线程同时尝试编辑（更新或删除）同一行时，乐观并发控制就会发挥作用。在这种情况下，第二个尝试编辑的线程将因冲突错误而失败。

## 从多个进程写入 DuckDB

从多个进程写入 DuckDB 不是自动支持的，也不是主要设计目标（详见 [并发处理](#handling-concurrency)）。

如果多个进程必须写入同一个文件，可以采用几种设计模式，但需要在应用程序逻辑中实现。例如，每个进程可以获取跨进程互斥锁，然后以读写模式打开数据库并在查询完成后关闭它。另一种方法是，如果另一个进程已经连接到数据库，每个进程可以重试连接（在查询完成后确保关闭连接）。另一个替代方案是，在 MySQL、PostgreSQL 或 SQLite 数据库上执行多进程事务，并使用 DuckDB 的 [MySQL]({% link docs/stable/core_extensions/mysql.md %})、[PostQSQL]({% link docs/stable/core_extensions/postgres.md %}) 或 [SQLite]({% link docs/stable/core_extensions/sqlite.md %}) 扩展，定期执行这些数据上的分析查询。

其他选项包括将数据写入 Parquet 文件，并使用 DuckDB 的 [读取多个 Parquet 文件]({% link docs/stable/data/parquet/overview.md %}) 能力，采用类似的方法处理 [CSV 文件]({% link docs/stable/data/csv/overview.md %})，或者创建一个 Web 服务器来接收请求并管理对 DuckDB 的读写操作。

## 乐观并发控制

DuckDB 使用 [乐观并发控制](https://en.wikipedia.org/wiki/Optimistic_concurrency_control)，这是一种通常被认为是读取密集型分析数据库系统最佳选择的方法，因为它加快了读取查询的处理速度。因此，任何同时修改同一行的事务都会导致事务冲突错误：

```console
事务冲突：不能更新已被修改的表！
```

> 提示：遇到事务冲突时，常见的解决方法是重新运行该事务。