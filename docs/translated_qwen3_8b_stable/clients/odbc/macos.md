---
---
github_repository: https://github.com/duckdb/duckdb-odbc
layout: docu
redirect_from:
- /docs/api/odbc/macos
- /docs/api/odbc/macos/
- /docs/clients/odbc/macos
title: macOS 上的 ODBC API
---

1. 需要一个驱动程序管理器来管理应用程序与 ODBC 驱动程序之间的通信。DuckDB 支持 `unixODBC`，它是 macOS 和 Linux 的完整 ODBC 驱动程序管理器。用户可以通过 [Homebrew](https://brew.sh/) 从命令行安装它：

   ```bash
   brew install unixodbc
   ```

2. <!-- markdownlint-disable MD034 --> DuckDB 提供了一个适用于 macOS 的通用 [ODBC 驱动程序](https://github.com/duckdb/duckdb-odbc/releases/download/v{{ site.current_duckdb_odbc_version }}/duckdb_odbc-osx-universal.zip)（支持 Intel 和 Apple Silicon 处理器）。要下载它，请运行：

   ```bash
   wget https://github.com/duckdb/duckdb-odbc/releases/download/v{{ site.current_duckdb_odbc_version }}/duckdb_odbc-osx-universal.zip
   ```

   <!-- markdownlint-enable MD034 -->

3. 该归档文件包含 `libduckdb_odbc.dylib` 二进制文件。要将其提取到目录中，请运行：

   ```bash
   mkdir duckdb_odbc && unzip duckdb_odbc-osx-universal.zip -d duckdb_odbc
   ```

4. 配置 ODBC 驱动程序有两种方式，可以通过配置文件初始化，也可以通过 [`SQLDriverConnect`](https://learn.microsoft.com/en-us/sql/odbc/reference/syntax/sqldriverconnect-function?view=sql-server-ver16) 连接。也可以将两者结合使用。

   此外，ODBC 驱动程序支持 DuckDB 中包含的所有 [配置选项]({% link docs/stable/configuration/overview.md %})。

   > 如果在 `SQLDriverConnect` 传递的连接字符串和 `odbc.ini` 文件中都设置了相同的配置项，
   > 则 `SQLDriverConnect` 传递的配置项具有优先权。

   配置参数的详细信息，请参阅 [ODBC 配置页面]({% link docs/stable/clients/odbc/configuration.md %}).

5. 配置完成后，可以使用 ODBC 客户端来验证安装。unixODBC 使用一个名为 `isql` 的命令行工具。

   使用 `odbc.ini` 中定义的 DSN 作为 `isql` 的参数。

   ```bash
   isql DuckDB
   ```

   ```text
   +---------------------------------------+
   | 已连接！                              |
   |                                       |
   | sql-statement                         |
   | help [tablename]                      |
   | echo [string]                         |
   | quit                                  |
   |                                       |
   +---------------------------------------+
   ```

   ```sql
   SQL> SELECT 42;
   ```

   ```text
   +------------+
   | 42         |
   +------------+
   | 42         |
   +------------+

   SQLRowCount 返回 -1
   1 行已获取
   ```