---
---
github_repository: https://github.com/duckdb/duckdb-odbc
layout: docu
redirect_from:
- /docs/api/odbc/windows
- /docs/api/odbc/windows/
- /docs/clients/odbc/windows
title: Windows平台ODBC API
---

在Windows平台上使用DuckDB ODBC API需要以下步骤：

1. Microsoft Windows需要一个ODBC驱动程序管理器来管理应用程序与ODBC驱动程序之间的通信。
   Windows上的驱动程序管理器以DLL文件`odbccp32.dll`的形式提供，并包含其他文件和工具。
   如需详细信息，请参阅[通用ODBC组件文件](https://docs.microsoft.com/en-us/previous-versions/windows/desktop/odbc/dn170563(v=vs.85))。

2. <!-- markdownlint-disable MD034 --> DuckDB将ODBC驱动程序作为资产发布。对于Windows，可以从[Windows ODBC资产（x86_64/AMD64）](https://github.com/duckdb/duckdb-odbc/releases/download/v{{ site.current_duckdb_odbc_version }}/duckdb_odbc-windows-amd64.zip)下载。<!-- markdownlint-enable MD034 -->

3. 该压缩包包含以下工件：

   * `duckdb_odbc.dll`：为Windows编译的DuckDB驱动程序。
   * `duckdb_odbc_setup.dll`：由Windows ODBC数据源管理器工具使用的设置DLL。
   * `odbc_install.exe`：用于帮助Windows配置的安装脚本。

   将压缩包解压到一个目录中（例如`duckdb_odbc`）。

4. `odbc_install.exe`二进制文件用于在Windows上配置DuckDB ODBC驱动程序。它依赖于`Odbccp32.dll`，该文件提供了配置ODBC注册表项的功能。

   在永久目录中（例如`duckdb_odbc`），双击`odbc_install.exe`。

   需要Windows管理员权限。如果没有管理员权限，将出现用户账户控制提示。

5. `odbc_install.exe`将默认DSN配置添加到ODBC注册表中，并使用默认数据库`:memory:`。

### Windows DSN设置

安装完成后，可以使用Windows ODBC数据源管理器工具`odbcad32.exe`更改默认DSN配置或添加新的配置。

它也可以通过Windows开始菜单启动：

<img src="/images/blog/odbc/launch_odbcad.png" style="width: 60%; height: 60%"/>

### 默认DuckDB DSN

新安装的DSN在Windows ODBC数据源管理器工具的***系统DSN***中可见：

![Windows ODBC配置工具](/images/blog/odbc/odbcad32_exe.png)

### 更改DuckDB DSN

在选择默认DSN（即`DuckDB`）或添加新配置时，将显示以下设置窗口：

![DuckDB Windows DSN设置](/images/blog/odbc/duckdb_DSN_setup.png)

此窗口允许您设置DSN以及与该DSN关联的数据库文件路径。

## 更详细的Windows设置

有两种方法可以配置ODBC驱动程序，一种是按照下面详细说明修改注册表项，
另一种是使用[`SQLDriverConnect`](https://learn.microsoft.com/en-us/sql/odbc/reference/syntax/sqldriverconnect-function?view=sql-server-ver16)进行连接。
也可以将这两种方法结合使用。

此外，ODBC驱动程序支持DuckDB中包含的所有[配置选项]({% link docs/stable/configuration/overview.md %})。

> 如果在传递给`SQLDriverConnect`的连接字符串和`odbc.ini`文件中都设置了配置项，
> 则传递给`SQLDriverConnect`的配置项将具有优先权。

有关配置参数的详细信息，请参阅[ODBC配置页面]({% link docs/stable/clients/odbc/configuration.md %}）。

### 注册表项

Windows上的ODBC设置基于注册表项（参见[ODBC组件的注册表项](https://docs.microsoft.com/en-us/sql/odbc/reference/install/registry-entries-for-odbc-components?view=sql-server-ver15)）。
ODBC条目可以放置在当前用户的注册表项（`HKCU`）或系统注册表项（`HKLM`）中。

我们已经测试并使用了基于`HKLM->SOFTWARE->ODBC`的系统注册表项。
`odbc_install.exe`会修改此条目，该条目包含两个子项：`ODBC.INI`和`ODBCINST.INI`。

`ODBC.INI`是用户通常插入驱动程序DSN注册表项的位置。

例如，DuckDB的DSN注册表项如下所示：

![`HKLM->SOFTWARE->ODBC->ODBC.INI->DuckDB`](/images/blog/odbc/odbc_ini-registry-entry.png)

`ODBCINST.INI`包含每个ODBC驱动程序的一个条目和其他为[Windows ODBC配置](https://docs.microsoft.com/en-us/sql/odbc/reference/install/registry-entries-for-odbc-components?view=sql-server-ver15)预定义的键。

### 更新ODBC驱动程序

当发布新版本的ODBC驱动程序时，安装新版本将覆盖现有版本。
然而，安装程序并不总是会更新注册表中的版本号。
为了确保使用正确的版本，
请检查`HKEY_LOCAL_MACHINE\SOFTWARE\ODBC\ODBCINST.INI\DuckDB Driver`是否具有最新的版本，
并确保`HKEY_LOCAL_MACHINE\SOFTWARE\ODBC\ODBC.INI\DuckDB\Driver`指向新驱动程序的正确路径。