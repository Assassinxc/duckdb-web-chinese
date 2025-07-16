---
---
layout: docu
title: 日志记录
---

DuckDB 包含一个日志记录机制，用于向用户提供额外的信息，例如查询执行详情、性能指标和系统事件。

## 基础知识

DuckDB 的日志记录机制可以通过 pragma 启用或禁用。默认情况下，日志存储在一个名为 `duckdb_logs` 的特殊表中，可以像查询其他表一样进行查询。

示例：

```sql
PRAGMA enable_logging;
-- 运行一些查询...
SELECT * FROM duckdb_logs;
```

## 日志级别

DuckDB 支持不同的日志级别，用于控制日志的详细程度：

* `ERROR`: 仅记录错误信息
* `WARNING`: 记录警告和错误信息
* `INFO`: 记录一般信息、警告和错误信息（默认）
* `DEBUG`: 记录详细的调试信息
* `TRACE`: 记录非常详细的跟踪信息

可以通过以下方式设置日志级别：

```sql
PRAGMA enable_logging;
SET logging_level = 'TRACE';
```

## 日志类型

在 DuckDB 中，日志信息可以与一个相关的日志类型关联。日志类型有两个主要目标。首先，它们允许使用 includelists 和 excludelist 来限制记录哪些类型日志信息。其次，日志类型可以具有预定义的消息模式，这使得 DuckDB 能够自动将消息解析为结构化数据类型。

### 日志专用类型

要仅记录特定类型的日志信息：

```sql
PRAGMA enable_logging('HTTP');
```

上述 pragma 会自动设置正确的日志级别，并将 `HTTP` 类型添加到 `enabled_log_types` 设置中。

### 结构化日志记录

一些日志类型（如 `HTTP`）会具有相关联的消息模式。要让 DuckDB 自动解析消息，可以使用 `duckdb_logs_parsed()` 宏。例如：

```sql
SELECT request.headers FROM duckdb_logs_parsed('HTTP');
```

### 可用日志类型的列表

这是 DuckDB 中可用日志类型的（非详尽）列表。

| 日志类型     | 描述                                               | 结构化 |
|--------------|----------------------------------------------------|--------|
| `QueryLog`   | 记录在 DuckDB 中执行的查询                         | 否     |
| `FileSystem` | 记录所有与 DuckDB 文件系统交互的文件系统操作       | 是     |
| `HTTP`       | 记录所有来自 DuckDB 内部 HTTP 客户端的 HTTP 通信 | 是     |

## 日志存储

默认情况下，DuckDB 将日志记录到内存中的日志存储。或者，DuckDB 可以直接将日志记录到 `stdout`，使用以下命令：

```sql
PRAGMA enable_logging;
SET logging_storage = 'stdout';
```