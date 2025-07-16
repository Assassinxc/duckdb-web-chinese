---
---
layout: docu
redirect_from:
- /docs/guides/performance/how-to-tune-workloads
- /docs/guides/performance/how-to-tune-workloads/
- /docs/guides/performance/how_to_tune_workloads
title: 工作负载调优
---

## `preserve_insertion_order` 选项

在导入或导出数据集（从/到 Parquet 或 CSV 格式）时，如果数据集远大于可用内存，可能会发生内存不足错误：

```console
内存不足错误：无法分配大小为 ... 的数据 (.../... 已使用)
```

在这些情况下，考虑将 [`preserve_insertion_order` 配置选项]({% link docs/stable/configuration/overview.md %}) 设置为 `false`：

```sql
SET preserve_insertion_order = false;
```

这允许系统重新排序不包含 `ORDER BY` 子句的任何结果，从而潜在地减少内存使用。

## 并行处理（多核处理）

### 行组对并行处理的影响

DuckDB 根据 _[行组]({% link docs/stable/internals/storage.md %}#row-groups)_ 并行化工作负载，即一组在存储级别一起存储的行。
DuckDB 数据库格式中的一个行组最多包含 122,880 行。
并行处理从行组级别开始，因此，对于要在 _k_ 个线程上运行的查询，它需要至少扫描 _k_ * 122,880 行。

### 线程过多

请注意，在某些情况下，DuckDB 可能会启动 _过多线程_（例如，由于超线程技术），这可能导致性能下降。在这种情况下，手动限制线程数量使用 [`SET threads = X`]({% link docs/stable/configuration/pragmas.md %}#threads) 会很有帮助。

## 大于内存的工作负载（离内存处理）

DuckDB 的一个主要优势是支持大于内存的工作负载，即能够处理大于可用系统内存的数据集（也称为 _离内存处理_）。
它还可以运行中间结果无法放入内存的查询。
本节解释了 DuckDB 中大于内存处理的先决条件、范围和已知限制。

### 写入磁盘

DuckDB 通过将数据写入磁盘来支持大于内存的工作负载。
在默认配置下，DuckDB 会创建 `⟨database_file_name⟩.tmp`{:.language-sql .highlight} 临时目录（在持久模式下）或 `.tmp`{:.language-sql .highlight} 目录（在内存模式下）。此目录可以通过 [`temp_directory` 配置选项]({% link docs/stable/configuration/pragmas.md %}#temp-directory-for-spilling-data-to-disk) 进行更改，例如：

```sql
SET temp_directory = '/path/to/temp_dir.tmp/';
```

### 阻塞操作符

一些操作符必须等到其输入的最后一行被看到后才能输出单行。
这些称为 _阻塞操作符_，因为它们需要缓冲其整个输入，
并且是关系型数据库系统中最耗费内存的操作符。
主要的阻塞操作符如下：

* _分组:_ [`GROUP BY`]({% link docs/stable/sql/query_syntax/groupby.md %})
* _连接:_ [`JOIN`]({% link docs/stable/sql/query_syntax/from.md %}#joins)
* _排序:_ [`ORDER BY`]({% link docs/stable/sql/query_syntax/orderby.md %})
* _窗口:_ [`OVER ... (PARTITION BY ... ORDER BY ...)`]({% link docs/stable/sql/functions/window_functions.md %})

DuckDB 支持所有这些操作符的大于内存处理。

### 限制

DuckDB 努力确保即使工作负载大于内存也能完成。
不过，目前仍有一些限制：

* 如果同一查询中出现多个阻塞操作符，DuckDB 仍可能由于这些操作符的复杂交互而抛出内存不足异常。
* 一些 [聚合函数]({% link docs/stable/sql/functions/aggregates.md %})，如 `list()` 和 `string_agg()`，不支持将数据卸载到磁盘。
* 使用排序的 [聚合函数]({% link docs/stable/sql/functions/aggregates.md %}#order-by-clause-in-aggregate-functions) 是整体性的，即它们需要所有输入才能开始聚合。由于 DuckDB 无法将某些复杂的中间聚合状态卸载到磁盘，这些函数在处理大型数据集时可能导致内存不足异常。
* `PIVOT` 操作 [内部使用 `list()` 函数]({% link docs/stable/sql/statements/pivot.md %}#internals)，因此受到相同的限制。

## 性能分析

如果查询的性能不如预期，值得研究其查询计划：

* 使用 [`EXPLAIN`]({% link docs/stable/guides/meta/explain.md %}) 打印物理查询计划，而无需实际运行查询。
* 使用 [`EXPLAIN ANALYZE`]({% link docs/stable/guides/meta/explain_analyze.md %}) 运行并分析查询。这将显示查询中每个步骤的 CPU 时间。请注意，由于多线程，各个步骤时间的总和将大于整个查询的处理时间。

查询计划可以指出性能问题的根本原因。一些通用方向：

* 避免使用嵌套循环连接，改用哈希连接。
* 一个扫描操作如果没有对后续应用的过滤条件进行过滤下推，会导致不必要的 IO。尝试重写查询以应用下推。
* 避免使用导致操作符基数爆炸到数十亿元组的不良连接顺序。

## 预备语句

[预备语句]({% link docs/stable/sql/query_syntax/prepared_statements.md %}) 在多次运行相同查询（但参数不同）时可以提高性能。当语句被预备时，它会完成查询执行过程的几个初始部分（解析、计划等），并缓存这些输出。当执行时，这些步骤可以被跳过，从而提高性能。这主要对重复运行的小查询（运行时间 < 100ms）并使用不同的参数集有益。

请注意，DuckDB 并不是以快速执行大量小查询为主要设计目标。相反，它优化了运行较大、不频繁查询的性能。

## 查询远程文件

DuckDB 在读取远程文件时使用同步 IO。这意味着每个 DuckDB 线程每次最多只能发起一个 HTTP 请求。如果查询必须在网络上发起许多小请求，将 DuckDB 的 [`threads` 设置]({% link docs/stable/configuration/pragmas.md %}#threads) 提高到超过 CPU 核心数量（大约是 CPU 核心数的 2-5 倍）可以提高并行度和性能。

### 避免读取不必要的数据

读取远程文件的工作负载中，主要瓶颈可能是 IO。这意味着，减少不必要的读取数据可以带来显著的好处。

一些基本的 SQL 技巧可以帮助：

* 避免 `SELECT *`。只选择实际使用的列。DuckDB 会尝试只下载实际需要的数据。
* 在可能的情况下，对远程 Parquet 文件应用过滤条件。DuckDB 可以使用这些过滤条件减少扫描的数据量。
* 通过经常用于过滤的列对数据进行 [排序]({% link docs/stable/sql/query_syntax/orderby.md %}) 或 [分区]({% link docs/stable/data/partitioning/partitioned_writes.md %})：这可以提高过滤条件在减少 IO 方面的效果。

要检查查询传输了多少远程数据，可以使用 [`EXPLAIN ANALYZE`]({% link docs/stable/guides/meta/explain_analyze.md %}) 来打印远程文件查询的总请求数和总数据传输量。

### 避免多次读取数据

DuckDB 不会自动缓存远程文件的数据。这意味着，对远程文件运行两次查询将下载所需数据两次。因此，如果数据需要多次访问，存储在本地可能更有意义。为了说明这一点，我们来看一个例子：

考虑以下查询：

```sql
SELECT col_a + col_b FROM 's3://bucket/file.parquet' WHERE col_a > 10;
SELECT col_a * col_b FROM 's3://bucket/file.parquet' WHERE col_a > 10;
```

这些查询会从 `s3://bucket/file.parquet` 两次下载 `col_a` 和 `col_b` 列。现在考虑以下查询：

```sql
CREATE TABLE local_copy_of_file AS
    SELECT col_a, col_b FROM 's3://bucket/file.parquet' WHERE col_a > 10;

SELECT col_a + col_b FROM local_copy_of_file;
SELECT col_a * col_b FROM local_copy_of_file;
```

在此情况下，DuckDB 会首先将 `col_a` 和 `col_b` 从 `s3://bucket/file.parquet` 复制到本地表，然后两次查询本地内存中的列。请注意，过滤条件 `WHERE col_a > 10` 也仅应用一次。

需要注意的是，这里有一个重要的注意事项。前两个查询完全是流式处理，内存占用很小，而第二个查询需要完全材料化 `col_a` 和 `col_b` 列。这意味着在某些罕见情况下（例如高速网络但内存有限），下载数据两次可能反而更有利。

## 使用连接的最佳实践

DuckDB 在多次重用相同的数据库连接时会表现最佳。在每次查询时断开连接并重新连接会产生一些开销，这会降低运行许多小查询时的性能。DuckDB 还会缓存一些数据和元数据在内存中，当最后一个打开的连接关闭时，这些缓存将丢失。通常，一个单一的连接效果最佳，但也可以使用连接池。

使用多个连接可以并行化一些操作，尽管通常并非必要。DuckDB 会尽可能在每个查询内部进行并行化，但在所有情况下都无法进行并行化。使用多个连接可以并发处理更多操作。这在 DuckDB 不受 CPU 限制而受其他资源（如网络传输速度）限制的情况下可能更有帮助。

## 持久化 vs. 内存表

DuckDB 支持 [轻量级压缩技术]({% post_url 2022-10-28-lightweight-compression %})。目前，这些压缩技术仅应用于持久化（磁盘上）数据库。

DuckDB 不会对内存表进行压缩。原因在于压缩是在检查点过程中进行的，而内存表不会被检查点。

在某些情况下，这可能导致一些反直觉的性能结果，即查询在磁盘表上执行得比在内存表上更快。例如，[TPC-H 工作负载]({% link docs/stable/core_extensions/tpch.md %}) 的 Q1 在磁盘模式下执行得比内存模式更快：

```sql
INSTALL tpch;
LOAD tpch;
CALL dbgen(sf = 30);
.timer on
PRAGMA tpch(1);
```

| 数据库设置         | 执行时间 |
|--------------------|----------:|
| 内存数据库         | 4.80 秒   |
| 持久化数据库       | 0.57 秒   |