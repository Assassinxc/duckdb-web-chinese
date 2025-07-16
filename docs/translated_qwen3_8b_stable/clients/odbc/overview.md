---
---
github_repository: https://github.com/duckdb/duckdb-odbc
layout: docu
title: ODBC API 概述
redirect_from:
- /docs/clients/odbc/overview
- /docs/clients/odbc/overview/
---

> DuckDB ODBC 客户端的最新版本是 {{ site.current_duckdb_odbc_short_version }}。

ODBC（开放数据库连接）是一种 C 风格的 API，它提供了对不同类型的数据库管理系统（DBMS）的访问。
ODBC API 由驱动管理器（DM）和 ODBC 驱动程序组成。

驱动管理器是系统库的一部分，例如 unixODBC，它管理用户应用程序与 ODBC 驱动程序之间的通信。
通常，应用程序会链接到 DM，它使用数据源名称（DSN）查找正确的 ODBC 驱动程序。

ODBC 驱动程序是 DBMS 对 ODBC API 的实现，它处理该 DBMS 的所有内部操作。

DM 将用户应用程序对 ODBC 函数的调用映射到执行该功能的正确 ODBC 驱动程序，并返回相应的值。

## DuckDB ODBC 驱动程序

根据 [核心接口一致性](https://docs.microsoft.com/en-us/sql/odbc/reference/develop-app/core-interface-conformance?view=sql-server-ver15)，DuckDB 支持 ODBC 版本 3.0。

ODBC 驱动程序适用于所有操作系统。访问 [安装页面]({% link docs/installation/index.html %}) 获取直接链接。