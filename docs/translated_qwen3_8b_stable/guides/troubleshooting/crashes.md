---
---
layout: docu
title: 系统崩溃
---

DuckDB 通过一个广泛的测试套件进行了[彻底的测试]({% link why_duckdb.md %}#thoroughly-tested)。
然而，仍然可能发生错误，这些错误有时会导致系统崩溃。
本页面包含有关如何排查 DuckDB 崩溃的实用信息。

## 崩溃类型

存在几种主要的崩溃类型：

* **终止信号：** 进程会以 `SIGSEGV`（段错误）、`SIGABRT` 等方式终止：这些情况不应该发生。请[提交问题](#submitting-an-issue)。

* **内部错误：** 某些操作可能导致 [`Internal Error`]({% link docs/stable/dev/internal_errors.md %})，例如：

  ```console
  INTERNAL 错误：
  尝试访问大小为 3 的向量的索引 3
  ```

  在遇到内部错误后，DuckDB 会进入受限模式，任何进一步的操作都会导致以下错误信息：

  ```console
  FATAL 错误：
  数据库由于之前的致命错误而失效。
  在再次使用数据库之前必须重启数据库。
  ```

* **内存不足错误：** DuckDB 的崩溃也可能是操作系统终止进程的症状。
  例如，许多 Linux 发行版运行 [OOM reaper 或 OOM killer 进程](https://learn.redhat.com/t5/Platform-Linux/Out-of-Memory-Killer/td-p/48828)，该进程终止进程以释放内存，从而防止操作系统内存耗尽。
  如果您的 DuckDB 会话被 OOM reaper 终止，请参阅[“OOM 错误”页面]({% link docs/stable/guides/troubleshooting/oom_errors.md %})

## 数据恢复

如果您的 DuckDB 会话在崩溃前正在写入一个持久化数据库文件，
则可能会在数据库旁边有一个名为 `⟨database_filename⟩.wal`{:.language-sql .highlight} 的 WAL（[写前日志](https://en.wikipedia.org/wiki/Write-ahead_logging)）文件。
要从 WAL 文件中恢复数据，只需在持久化数据库上启动一个新的 DuckDB 会话。
DuckDB 将重放写前日志并执行一个 [检查点操作]({% link docs/stable/sql/statements/checkpoint.md %})，将数据库恢复到崩溃前的状态。

## 崩溃排查

### 使用最新的稳定版和预览版构建

DuckDB 不断改进，因此您遇到的错误可能已经在代码库中修复。
首先，尝试升级到[**最新稳定版构建**]({% link docs/installation/index.html %}?version=stable)。
如果这不能解决问题，请尝试使用[**预览版构建**]({% link docs/installation/index.html %}?version=main)（也称为“夜间构建”）。

如果您希望使用带有[开放拉取请求](https://github.com/duckdb/duckdb/pulls)的代码库运行 DuckDB，
您可以尝试[从源代码构建]({% link docs/stable/dev/building/overview.md %}).

### 搜索现有问题

有人可能已经报告了导致崩溃的错误。
请在[GitHub 问题跟踪器](https://github.com/duckdb/duckdb/issues)中搜索错误信息，查看可能相关的现有问题。
DuckDB 拥有庞大的社区，可能会有针对此问题的解决方法。

### 禁用查询优化器

某些崩溃是由 DuckDB 的查询优化器组件引起的。
要确定是否是优化器导致崩溃，请尝试禁用优化器并重新运行查询：

```sql
PRAGMA disable_optimizer;
```

如果查询成功完成，则崩溃是由一个或多个优化器规则引起的。
要确定具体导致崩溃的规则，您可以尝试[选择性地禁用优化器规则]({% link docs/stable/configuration/pragmas.md %}#selectively-disabling-optimizers)。这样，您的查询仍然可以利用优化器的其余规则。

### 尝试隔离问题

某些问题是由不同组件和扩展之间的交互，或者是某些特定平台或客户端语言引起的。
您通常可以将问题隔离到一个更小的问题。

#### 使用纯 SQL 复现问题

问题也可能由于客户端库之间的差异而出现。
要了解是否如此，请尝试使用 [DuckDB CLI 客户端]({% link docs/stable/clients/cli/overview.md %}) 用纯 SQL 查询来复现问题。
如果您无法在命令行客户端中复现问题，那么很可能是与客户端库有关。

#### 不同的硬件配置

根据我们的经验，一些崩溃是由于硬件故障（过热硬盘、超频 CPU 等）引起的。
因此，尝试在另一台计算机上运行相同的任务可能值得尝试。

#### 分解查询

将查询分解为多个较小的查询，每个查询使用单独的 DuckDB 扩展和 SQL 功能是一个好主意。

例如，如果您有一个查询，其目标是 AWS S3 存储桶中的数据集并对其执行两个连接操作，请尝试将其重写为以下一系列较小的步骤。
手动下载数据集的文件并将其加载到 DuckDB 中。
然后分别执行第一次连接和第二次连接。
如果多步骤方法在某个步骤仍然导致崩溃，则触发崩溃的查询是构建最小可复现示例的良好基础。如果多步骤方法有效且不再崩溃，请尝试重建原始查询并观察哪个步骤重新引入了错误。
在这两种情况下，您将更清楚问题的根源，并且可能找到一个可以立即使用的解决方法。
无论如何，请考虑[提交问题](#submitting-an-issue)，并分享您的发现。