---
---
layout: docu
title: 处理大型数据库
---

本页面包含有关处理大型DuckDB数据库文件的信息。虽然大多数DuckDB数据库都远低于1 TB，
但在我们的[2024用户调查]({% post_url 2024-10-04-duckdb-user-survey-analysis %}#dataset-sizes)中，1%的受访者使用了2 TB或更大的DuckDB文件（相当于约10 TB的CSV文件）。

DuckDB的[原生数据库格式]({% link docs/stable/internals/storage.md %})支持无实际限制的大型数据库文件，不过在处理大型数据库文件时需要注意以下几点。

1. 对象存储系统的文件大小限制通常低于基于块的存储系统。例如，[AWS S3将文件大小限制为5 TB](https://aws.amazon.com/s3/faqs/)。

2. 对DuckDB数据库进行检查点操作可能会很慢。例如，在[TPC-H]({% link docs/stable/core_extensions/tpch.md %}) SF1000数据库中向表添加几行后进行检查点操作，大约需要5秒。

3. 在基于块的存储系统上，处理大型文件时文件的大小对性能有较大影响。在Linux系统上，DuckDB在处理大型文件时使用XFS性能最佳。

如需存储大量数据，可以考虑使用[DuckLake湖仓格式](https://ducklake.select/)。