---
---
layout: docu
title: 内存不足错误
---

DuckDB 拥有业界领先的非内存内核查询引擎，可以将数据溢出到磁盘进行大于内存的处理。
我们不断努力改进 DuckDB，以提高其可扩展性，并尽可能防止内存不足错误。
不过，如果您运行包含多个[阻塞操作符]({% link docs/stable/guides/performance/how_to_tune_workloads.md %}#blocking-operators)、某些聚合函数、`PIVOT`操作等的查询，或者您的可用内存相对于数据集大小非常有限，仍可能会遇到内存不足错误。

## 内存不足错误的类型

内存不足错误主要以两种形式发生：

### `OutOfMemoryException`

大多数情况下，DuckDB 会因为 `OutOfMemoryException` 而出现内存不足错误。
例如：

```console
duckdb.duckdb.OutOfMemoryException: 内存不足错误：无法固定大小为 256.0 KiB 的块（已使用 476.7 MiB/476.8 MiB）
```

### OOM Reaper（Linux）

许多 Linux 发行版都有一个[OOM killer 或 OOM reaper 进程](https://learn.redhat.com/t5/Platform-Linux/Out-of-Memory-Killer/td-p/48828)，其目的是防止内存过度分配。
如果 OOM reaper 终止了您的进程，您通常会看到以下信息，其中显示 DuckDB 正在运行：

```console
Killed
```

要获取更详细的诊断信息，请使用 [`dmesg` 命令](https://en.wikipedia.org/wiki/Dmesg)（您可能需要 `sudo`）检查诊断信息：

```bash
sudo dmesg
```

如果进程被 OOM killer/reaper 终止，您将找到类似以下的条目：

```console
[Fri Apr 18 02:04:10 2025] 内存不足：终止进程 54400 (duckdb) total-vm:1037911068kB, anon-rss:770031964kB, file-rss:0kB, shmem-rss:0kB, UID:1000 pgtables:1814612kB oom_score_adj:0
```

## 解决内存不足错误

为了防止内存不足错误，请尝试减少内存使用。
为此，请参考[“如何调整工作负载”页面]({% link docs/stable/guides/performance/how_to_tune_workloads.md %}）。
简要说明如下：

* 使用 `SET threads = ...` 命令减少线程数量。
* 如果您的查询从文件中读取大量数据或写入大量数据，请尝试将 `preserve_insertion_order` 选项设置为 `false`：`SET preserve_insertion_order = false`。
* 将内存限制设置为默认值的 80% 以下（请参阅[限制页面]({% link docs/stable/operations_manual/limits.md %}））。这可能很有帮助，因为一些 DuckDB 操作绕过了缓冲区管理器，可能会保留比内存限制允许更多的内存。如果您观察到这种情况，请使用 `SET memory_limit = ...` 将内存限制设置为系统内存的 50-60%。
* 将查询拆分为子查询。这可以让您查看中间结果“膨胀”发生在哪个位置，从而导致查询内存不足。

## 参见

如需更多关于 DuckDB 内存管理的信息，请参阅[“DuckDB 中的内存管理”博客文章]({% post_url 2024-07-09-memory-management %})。