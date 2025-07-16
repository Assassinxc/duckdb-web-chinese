---
---
layout: docu
redirect_from:
- /docs/guides/performance/environment
title: 环境
---

DuckDB 运行的环境对性能有明显的影响。本页面重点介绍硬件配置和操作系统对性能的影响。

## 硬件配置

### CPU

DuckDB 在 AMD64 (x86_64) 和 ARM64 (AArch64) CPU 架构上都能高效运行。

### 内存

> 最佳实践：每个线程应至少分配 1-4 GB 内存。

#### 最小内存需求

一般来说，DuckDB 每个线程需要至少 125 MB 的内存。
例如，如果你使用 8 个线程，至少需要 1 GB 的内存。
如果你在内存受限的环境中工作，可以考虑 [限制线程数量]({% link docs/stable/configuration/pragmas.md %}#threads)，例如通过执行以下命令：

```sql
SET threads = 4;
```

#### 用于理想性能的内存

用于理想性能的内存需求取决于多个因素，包括数据集大小和要执行的查询。
可能令人惊讶的是，_查询_ 对内存需求的影响更大。
包含大量多对多表连接的工作负载会产生大量的中间数据集，因此需要更多的内存来完全装入内存进行评估。
作为近似估算，以聚合操作为主的工作负载每个线程需要 1-2 GB 内存，以连接操作为主的工作负载每个线程需要 3-4 GB 内存。

#### 大于内存的工作负载

DuckDB 可以通过将数据溢出到磁盘来处理大于内存的工作负载。
这得益于 _out-of-core_（非内存）支持，用于分组、连接、排序和窗口操作。
请注意，大于内存的工作负载可以在持久化模式和内存模式下进行处理，因为 DuckDB 在这两种模式下都会将数据溢出到磁盘。

### 本地磁盘

**磁盘类型。**
DuckDB 的磁盘模式最适合使用 SSD 和 NVMe 磁盘。虽然 HDD 也支持，但会带来较低的性能，尤其是写入操作。

**磁盘模式与内存模式。**
出人意料的是，使用磁盘模式的 DuckDB 实例可能比内存模式的实例更快，这是因为压缩的优势。
了解更多，请参阅 [“如何调优工作负载”页面]({% link docs/stable/guides/performance/how_to_tune_workloads.md %}#persistent-vs-in-memory-tables)。

**文件系统。**
在 Linux 上，[DuckDB 最佳运行于 XFS 文件系统](https://www.phoronix.com/review/linux-615-filesystems/5)，但也兼容其他文件系统，如 ext4。
在 Windows 上，我们推荐使用 NTFS 并避免使用 FAT32。

> 请注意，DuckDB 数据库内置了校验和，因此不需要文件系统进行完整性检查以防止数据损坏。

### 网络附加磁盘

**云磁盘。** DuckDB 在网络支持的云磁盘（如 [AWS EBS](https://aws.amazon.com/ebs/)）上运行良好，适用于只读和读写工作负载。

**网络附加存储。**
网络附加存储可以为 DuckDB 提供只读工作负载服务。
然而，_不建议在网络附加存储 (NAS) 上以读写模式运行 DuckDB。_
这些配置包括 [NFS](https://en.wikipedia.org/wiki/Network_File_System)、
网络驱动器如 [SMB](https://en.wikipedia.org/wiki/Server_Message_Block) 和
[Samba](https://en.wikipedia.org/wiki/Samba_(software))。
根据用户报告，网络附加存储上运行读写工作负载可能导致缓慢且不可预测的性能，
以及由于底层文件系统引起的错误。

> 警告：避免在网络附加存储上以读写模式运行 DuckDB。

> 最佳实践：如果工作负载大于内存或快速数据加载很重要，使用快速磁盘很重要。仅在可靠（例如云磁盘）且保证高 IO 的情况下使用网络支持磁盘。

## 操作系统

我们推荐使用最新稳定版本的操作系统：macOS、Windows 和 Linux 都经过了充分测试，DuckDB 可以在这些系统上以高性能运行。

### Linux

DuckDB 可以在过去约 5 年内发布的所有主流 Linux 发行版上运行。
如果你没有特别偏好，我们建议使用 Ubuntu Linux LTS，因为其稳定性，以及大多数 DuckDB Linux 测试套件作业都在 Ubuntu 工作者上运行。

#### glibc vs. musl libc

DuckDB 可以使用 [glibc](https://www.gnu.org/software/libc/)（默认）和 [musl libc](https://www.musl-libc.org/) 构建（请参阅 [构建指南]({% link docs/stable/dev/building/linux.md %})）。
然而请注意，使用 musl libc 构建的 DuckDB 二进制文件性能较低。
在实践中，这可能导致计算密集型工作负载的性能下降超过 5 倍。
因此，建议在运行 DuckDB 时使用带有 glibc 的 Linux 发行版，以实现性能导向的工作负载。

## 内存分配器

如果你的系统使用 [`jemalloc`]({% link docs/stable/core_extensions/jemalloc.md %}) 作为默认内存分配器，并且你有一个多核 CPU，请考虑 [启用分配器的后台线程]({% link docs/stable/core_extensions/jemalloc.md %}#background-threads)。