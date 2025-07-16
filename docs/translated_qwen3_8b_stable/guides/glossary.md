---
---
layout: docu
redirect_from:
- /docs/guides/glossary
title: 术语表
---

本页面包含一些在DuckDB中常用的常见术语的解释。

## 术语

### 内置数据库管理系统

DBMS运行在客户端应用程序的进程中，而不是作为单独的进程运行，这与传统的客户端-服务器架构不同。另一种说法是**可嵌入**的数据库管理系统。一般来说，应避免使用“嵌入式数据库管理系统”这一术语，因为它可能与针对嵌入式系统的DBMS（例如在微控制器上运行的系统）产生混淆。

### 替换扫描

在DuckDB中，当查询中使用的表名在目录中不存在时，会使用替换扫描。这些扫描可以替代表，使用其他数据源。使用替换扫描使DuckDB能够例如无缝读取[Pandas DataFrames]({% link docs/stable/guides/python/sql_on_pandas.md %})，或从远程源读取输入数据，而无需显式调用执行此操作的函数（例如从https读取Parquet文件）({% link docs/stable/guides/network_cloud_storage/http_import.md %}）。如需详细信息，请参阅[C API – 替换扫描页面]({% link docs/stable/clients/c/replacement_scans.md %}).

### 扩展

DuckDB具有灵活的扩展机制，允许动态加载扩展。这些扩展可以通过提供对额外文件格式的支持、引入新类型以及领域特定功能来扩展DuckDB的功能。如需详细信息，请参阅[扩展页面]({% link docs/stable/core_extensions/overview.md %}).

### 平台

平台是操作系统（如Linux、macOS、Windows）、系统架构（如AMD64、ARM64）以及可选的编译器（如GCC4）的组合。平台用于分发DuckDB二进制文件和[扩展包]({% link docs/stable/extensions/extension_distribution.md %}#platforms)。