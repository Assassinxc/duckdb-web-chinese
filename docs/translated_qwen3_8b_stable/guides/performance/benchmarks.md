---
---
layout: docu
redirect_from:
- /docs/guides/performance/benchmarks
title: 基准测试
---

在我们性能指南中的多个建议中，我们使用微基准测试来支持我们的主张。对于这些基准测试，我们使用了来自 [TPC-H 基准测试]({% link docs/stable/core_extensions/tpch.md %}) 和 [LDBC 社交网络基准测试的 BI 工作负载](https://github.com/ldbc/ldbc_snb_bi/blob/main/snb-bi-pre-generated-data-sets.md#compressed-csvs-in-the-composite-merged-fk-format) 的数据集。

<!--
## 基准测试环境

性能指南中的基准测试运行在一台 2022 年款的 MacBook Pro 上，搭载 12 核 M2 Pro 处理器，32 GiB 内存和 1 TB 磁盘。
-->

## 数据集

我们使用 [LDBC BI SF300 数据集的 Comment 表](https://blobs.duckdb.org/data/ldbc-sf300-comments.tar.zst) (20 GB 的 `.tar.zst` 归档文件，解压为 `.csv.gz` 文件后为 21 GB)，
而其他数据集使用该表的 [`creationDate` 列](https://blobs.duckdb.org/data/ldbc-sf300-comments-creationDate.parquet) (4 GB 的 `.parquet` 文件)。

基准测试中使用的 TPC 数据集是使用 DuckDB [tpch 扩展]({% link docs/stable/core_extensions/tpch.md %}) 生成的。

## 关于基准测试的说明

[运行公平的基准测试很困难](https://hannes.muehleisen.org/publications/DBTEST2018-performance-testing.pdf)，尤其是在进行系统间比较时。
在 DuckDB 上运行基准测试时，请确保您使用的是最新版本（最好是 [预览构建版本]({% link docs/installation/index.html %}?version=main)）。
如果您对基准测试结果有任何疑问，欢迎随时联系我们 `gabor@duckdb.org`。

## 基准测试免责声明

请注意，本指南中展示的基准测试结果并不代表官方的 TPC 或 LDBC 基准测试结果。相反，它们仅使用了 TPC-H 和 LDBC BI 基准测试框架提供的数据集和部分查询，省略了工作负载中的其他部分，例如更新操作。