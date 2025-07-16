---
---
layout: docu
redirect_from:
- /docs/api/c
- /docs/api/c/
- /docs/api/c/overview
- /docs/api/c/overview/
- /docs/clients/c/overview
title: 概述
---

> DuckDB C API 的最新版本是 {{ site.current_duckdb_version }}。

DuckDB 实现了一个自定义的 C API，其设计在某种程度上参考了 SQLite C API。该 API 包含在 `duckdb.h` 头文件中。继续阅读 [启动与关闭]({% link docs/stable/clients/c/connect.md %}) 以开始使用，或查看 [完整 API 概览]({% link docs/stable/clients/c/api.md %}).

我们还提供了一个 SQLite API 包装器，这意味着如果你的应用程序是基于 SQLite C API 编写的，你可以重新链接到 DuckDB，应用程序应该仍然可以正常运行。有关更多信息，请查看我们的源代码仓库中的 [`sqlite_api_wrapper`](https://github.com/duckdb/duckdb/tree/main/tools/sqlite3_api_wrapper) 文件夹。

## 安装

DuckDB C API 可以作为 `libduckdb` 包的一部分进行安装。请参阅 [安装页面](../../installation?environment=cplusplus) 以获取详细信息。