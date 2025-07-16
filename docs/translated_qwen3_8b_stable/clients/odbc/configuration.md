---
---
github_repository: https://github.com/duckdb/duckdb-odbc
layout: docu
redirect_from:
- /docs/api/odbc/configuration
- /docs/api/odbc/configuration/
- /docs/clients/odbc/configuration
title: ODBC 配置
---

本页面文档说明使用 ODBC 配置的文件，[`odbc.ini`](#odbcini-and-odbcini) 和 [`odbcinst.ini`](#odbcinstini-and-odbcinstini)。
这些文件可以放置在用户主目录中作为点文件（`.odbc.ini` 和 `.odbcinst.ini`），或者放在系统目录中。
有关平台特定的详细信息，请参阅 [Linux]({% link docs/stable/clients/odbc/linux.md %})、[macOS]({% link docs/stable/clients/odbc/macos.md %}) 和 [Windows]({% link docs/stable/clients/odbc/windows.md %}) 页面。

## `odbc.ini` 和 `.odbc-ini`

`odbc.ini` 文件包含驱动程序的 DSN，可以具有特定的配置项。
`odbc.ini` 的示例（使用 DuckDB）：

```ini
[DuckDB]
Driver = DuckDB Driver
Database = :memory:
access_mode = read_only
```

这些行对应以下参数：

* `[DuckDB]`：括号之间的内容是 DuckDB 的 DSN。
* `Driver`：描述驱动程序的名称，以及在 `odbcinst.ini` 中查找配置的位置。
* `Database`：描述 DuckDB 使用的数据库名称，也可以是系统中 `.db` 文件的路径。
* `access_mode`：连接数据库的模式。

## `odbcinst.ini` 和 `.odbcinst.ini`

`odbcinst.ini` 文件包含系统中安装的 ODBC 驱动程序的一般配置。
驱动程序部分以括号中的驱动程序名称开头，然后是该驱动程序的特定配置项。

`odbcinst.ini` 的示例（使用 DuckDB）：

```ini
[ODBC]
Trace = yes
TraceFile = /tmp/odbctrace

[DuckDB Driver]
Driver = /path/to/libduckdb_odbc.dylib
```

这些行对应以下参数：

* `[ODBC]`：ODBC 配置部分。
* `Trace`：使用选项 `yes` 启用 ODBC 跟踪文件。
* `TraceFile`：ODBC 跟踪文件的绝对系统文件路径。
* `[DuckDB Driver]`：安装的 DuckDB 驱动程序部分。
* `Driver`：DuckDB 驱动程序的绝对系统文件路径。请根据您的配置进行更改。