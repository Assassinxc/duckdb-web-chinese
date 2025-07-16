---
---
layout: docu
redirect_from:
- /docs/guides/performance/my-workload-is-slow
- /docs/guides/performance/my-workload-is-slow/
- /docs/guides/performance/my_workload_is_slow
title: 我的工作负载很慢
---

如果您发现DuckDB中的工作负载运行缓慢，我们建议您进行以下检查。每个要点都有更详细的说明链接。

1. 您的内存是否足够？如果每线程有[1-4 GB内存]({% link docs/stable/guides/performance/environment.md %}#cpu-and-memory)，DuckDB的性能最佳。
1. 您是否使用了快速磁盘？网络附加磁盘（如云块存储）会导致写密集型和[内存不足]({% link docs/stable/guides/performance/how_to_tune_workloads.md %}#spilling-to-disk)的工作负载变慢。在云环境中运行此类工作负载时，建议使用实例附加存储（NVMe SSD）。
1. 您是否使用了索引或约束（主键、唯一等）？如果可能，请尝试[禁用它们]({% link docs/stable/guides/performance/schema.md %}#indexing)，这可以提升加载和更新性能。
1. 您是否使用了正确的类型？例如，[使用`TIMESTAMP`来编码日期时间值]({% link docs/stable/guides/performance/schema.md %}#types)。
1. 您是否从Parquet文件中读取？如果是，这些文件的[行组大小是否在10万到100万之间]({% link docs/stable/guides/performance/file_formats.md %}#the-effect-of-row-group-sizes)，以及文件大小是否在100MB到10GB之间？
1. 查询计划是否正确？使用 [`EXPLAIN`]({% link docs/stable/guides/performance/how_to_tune_workloads.md %}#profiling) 来研究它。
1. 该工作负载是否[并行运行]({% link docs/stable/guides/performance/how_to_tune_workloads.md %}#parallelism)？使用`htop`或操作系统的任务管理器来观察这一点。
1. DuckDB是否使用了过多线程？尝试[限制线程数量]({% link docs/stable/guides/performance/how_to_tune_workloads.md %}#parallelism-multi-core-processing)。

您是否了解其他常见问题？如果是，请点击下方的 _报告内容问题_ 链接，并描述这些问题及其解决方法。