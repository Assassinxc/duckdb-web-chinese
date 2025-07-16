---
---
layout: docu
redirect_from:
- /docs/guides/performance/file-formats
- /docs/guides/performance/file-formats/
- /docs/guides/performance/file_formats
title: 文件格式
---

## 处理 Parquet 文件

DuckDB 对 Parquet 文件有先进的支持，包括 [直接查询 Parquet 文件]({% post_url 2021-06-25-querying-parquet %}).
在决定是直接查询这些文件还是先将它们加载到数据库时，需要考虑几个因素。

### 直接查询 Parquet 文件的原因

**基本统计信息的可用性：** Parquet 文件使用列式存储格式，并包含诸如 [zonemap]({% link docs/stable/guides/performance/indexing.md %}#zonemaps) 的基本统计信息。由于这些特性，DuckDB 可以在 Parquet 文件上利用诸如投影和过滤下推等优化。因此，结合投影、过滤和聚合的工作负载在 Parquet 文件上运行时通常表现良好。

**存储考虑：** 从 Parquet 文件加载数据将需要大约相同的空间用于 DuckDB 数据库文件。因此，如果可用磁盘空间有限，直接在 Parquet 文件上运行查询可能更值得。

### 不直接查询 Parquet 文件的原因

**缺乏高级统计信息：** DuckDB 数据库格式具有 [HyperLogLog 统计信息](https://en.wikipedia.org/wiki/HyperLogLog)，而 Parquet 文件没有。这些统计信息提高了基数估算的准确性，特别是在查询包含大量连接操作符时尤为重要。

**提示。** 如果您发现 DuckDB 在 Parquet 文件上生成次优的连接顺序，请尝试将 Parquet 文件加载到 DuckDB 表中。改进的统计信息很可能有助于获得更好的连接顺序。

**重复查询：** 如果您计划在相同的数据集上运行多个查询，将数据加载到 DuckDB 中是有价值的。查询始终会稍微快一些，随着时间推移，这会抵消初始加载时间。

**高解压缩时间：** 一些 Parquet 文件使用如 gzip 等重量级压缩算法进行压缩。在这种情况下，每次访问文件时都需要昂贵的解压缩时间。同时，Snappy、LZ4 和 zstd 等轻量级压缩方法解压缩更快。您可以使用 [`parquet_metadata` 函数]({% link docs/stable/data/parquet/metadata.md %}#parquet-metadata) 来确定使用的压缩算法。

#### 微基准测试：在 DuckDB 数据库和 Parquet 上运行 TPC-H

[TPC-H 基准]({% link docs/stable/core_extensions/tpch.md %}) 上的查询在 Parquet 文件上运行时，速度比在 DuckDB 数据库上慢约 1.1-5.0 倍。

> 最佳实践 如果您有存储空间，并且有大量连接操作的工作负载和/或计划在相同的数据集上运行许多查询，请首先将 Parquet 文件加载到数据库中。Parquet 文件的压缩算法和行组大小对性能有很大影响：使用 [`parquet_metadata` 函数]({% link docs/stable/data/parquet/metadata.md %}#parquet-metadata) 来研究这些内容。

### 行组大小的影响

DuckDB 在行组大小为每组 10 万到 100 万行的 Parquet 文件上表现最佳。这是因为 DuckDB 只能 [按行组并行处理]({% link docs/stable/guides/performance/how_to_tune_workloads.md %}#parallelism-multi-core-processing) – 所以如果 Parquet 文件有一个单个巨大的行组，它只能由一个线程处理。您可以使用 [`parquet_metadata` 函数]({% link docs/stable/data/parquet/metadata.md %}#parquet-metadata) 来确定 Parquet 文件中有多少行组。在写入 Parquet 文件时，使用 [`row_group_size`]({% link docs/stable/sql/statements/copy.md %}#parquet-options) 选项。

#### 微基准测试：在不同行组大小下运行聚合查询

我们使用不同的行组大小对 Parquet 文件运行一个简单的聚合查询，选择的行组大小在 960 和 1,966,080 之间。结果如下。

| 行组大小 | 执行时间 |
|---------------:|---------------:|
| 960            | 8.77 s         |
| 1920           | 8.95 s         |
| 3840           | 4.33 s         |
| 7680           | 2.35 s         |
| 15360          | 1.58 s         |
| 30720          | 1.17 s         |
| 61440          | 0.94 s         |
| 122880         | 0.87 s         |
| 245760         | 0.93 s         |
| 491520         | 0.95 s         |
| 983040         | 0.97 s         |
| 1966080        | 0.88 s         |

结果表明，行组大小小于 5000 的情况下会有显著的负面影响，使运行时间比理想大小的行组大 5-10 倍，而行组大小在 5000 到 20000 之间的表现仍然比最佳性能低 1.5-2.5 倍。在行组大小超过 10 万的情况下，差异很小：最佳和最差运行时间之间的差距约为 10%。

### Parquet 文件大小

DuckDB 也可以在多个 Parquet 文件之间并行处理。建议所有文件的总行组数至少与 CPU 线程数相同。例如，一台有 10 个线程的机器，10 个文件每个有 1 个行组或 1 个文件有 10 个行组都可以实现完全并行。同时，保持单个 Parquet 文件的大小适中也是有益的。

> 最佳实践 单个 Parquet 文件的理想范围是每文件 100 MB 至 10 GB。

### Hive 分区用于过滤下推

在查询许多带有过滤条件的文件时，使用 [Hive 格式文件夹结构]({% link docs/stable/data/partitioning/hive_partitioning.md %}) 按过滤条件所用的列对数据进行分区可以提高性能。DuckDB 只需要读取满足过滤条件的文件夹和文件。这在查询远程文件时尤其有帮助。

### 关于读取和写入 Parquet 文件的更多提示

有关读取和写入 Parquet 文件的提示，请参见 [Parquet 提示页面]({% link docs/stable/data/parquet/tips.md %}).

## 加载 CSV 文件

CSV 文件通常以压缩格式如 GZIP 存储（`.csv.gz`）。DuckDB 可以在运行时解压缩这些文件。实际上，这通常比先解压缩文件再加载更快，因为减少了 IO。

| 架构 | 加载时间 |
|---|--:|
| 从 GZIP 压缩的 CSV 文件（`.csv.gz`）加载 | 107.1 s |
| 解压缩（使用并行 `gunzip`）并从解压后的 CSV 文件加载 | 121.3 s |

### 加载许多小 CSV 文件

[CSV 读取器]({% link docs/stable/data/csv/overview.md %}) 会在所有文件上运行 [CSV 探针]({% post_url 2023-10-27-csv-sniffer %})。对于许多小文件，这可能导致不必要的高开销。
加速此过程的一个潜在优化是关闭探针。假设所有文件具有相同的 CSV 方言和列名/类型，可以按如下方式获取探针选项：

```sql
.mode line
SELECT Prompt FROM sniff_csv('part-0001.csv');
```

```text
Prompt = FROM read_csv('file_path.csv', auto_detect=false, delim=',', quote='"', escape='"', new_line='\n', skip=0, header=true, columns={'hello': 'BIGINT', 'world': 'VARCHAR'});
```

然后，您可以通过例如应用 [文件名扩展（通配符）]({% link docs/stable/sql/functions/pattern_matching.md %}#globbing) 来调整 `read_csv` 命令，并使用探针检测的其余选项运行：

```sql
FROM read_csv('part-*.csv', auto_detect=false, delim=',', quote='"', escape='"', new_line='\n', skip=0, header=true, columns={'hello': 'BIGINT', 'world': 'VARCHAR'});
```