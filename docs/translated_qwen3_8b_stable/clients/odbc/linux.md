---
---
github_repository: https://github.com/duckdb/duckdb-odbc
layout: docu
redirect_from:
- /docs/api/odbc/linux
- /docs/api/odbc/linux/
- /docs/clients/odbc/linux
title: Linux平台ODBC API
---

## 驱动管理器

需要一个驱动管理器来管理应用程序与ODBC驱动之间的通信。
我们已经测试并支持`unixODBC`，它是一个完整的Linux平台ODBC驱动管理器。
用户可以通过命令行安装它：

在基于Debian的发行版（Ubuntu、Mint等）上运行：

```bash
sudo apt-get install unixodbc odbcinst
```

在基于Fedora的发行版（Amazon Linux、RHEL、CentOS等）上运行：

```bash
sudo yum install unixODBC
```

## 配置驱动

1. 下载与您的架构对应的ODBC Linux资源：

   <!-- markdownlint-disable MD034 -->

   * [x86_64 (AMD64)](https://github.com/duckdb/duckdb-odbc/releases/download/v{{ site.current_duckdb_odbc_version }}/duckdb_odbc-linux-amd64.zip)
   * [arm64 (AArch64)](https://github.com/duckdb/duckdb-odbc/releases/download/v{{ site.current_duckdb_odbc_version }}/duckdb_odbc-linux-aarch64.zip)

   <!-- markdownlint-enable MD034 -->

2. 该包包含以下文件：

   * `libduckdb_odbc.so`：DuckDB驱动。
   * `unixodbc_setup.sh`：一个用于在Linux系统上辅助配置的设置脚本。

   要提取这些文件，请运行：

   ```bash
   mkdir duckdb_odbc && unzip duckdb_odbc-linux-amd64.zip -d duckdb_odbc
   ```

3. `unixodbc_setup.sh`脚本用于配置DuckDB ODBC驱动。它基于`unixODBC`包，该包提供了一些用于处理ODBC设置和测试的命令，例如`odbcinst`和`isql`。

   使用`-u`或`-s`选项运行以下命令以配置DuckDB ODBC。

   `-u`选项基于用户的主目录来设置ODBC初始化文件。

   ```bash
   ./unixodbc_setup.sh -u
   ```

   `-s`选项更改系统级别的文件，这些文件对所有用户可见，因此需要root权限。

   ```bash
   sudo ./unixodbc_setup.sh -s
   ```

   `--help`选项显示`unixodbc_setup.sh`的用法。

   ```bash
   ./unixodbc_setup.sh --help
   ```

   ```text
   使用方式：./unixodbc_setup.sh <level> [options]

   示例：./unixodbc_setup.sh -u -db ~/database_path -D ~/driver_path/libduckdb_odbc.so

   level：
   -s：系统级别，使用'sudo'在系统级别配置DuckDB ODBC，更改的文件为：/etc/odbc[inst].ini
   -u：用户级别，配置DuckDB ODBC在用户级别，更改的文件为：~/.odbc[inst].ini。

   选项：
   -db database_path>：DuckDB数据库文件路径，默认为':memory:'（若未提供）
   -D driver_path：驱动文件路径（即libduckdb_odbc.so的路径），默认使用基础脚本目录
   ```

4. Linux平台的ODBC设置基于`.odbc.ini`和`.odbcinst.ini`文件。

   这些文件可以放置在用户主目录`/home/⟨username⟩`{:.language-sql .highlight} 或系统目录`/etc`{:.language-sql .highlight} 中。
   驱动管理器优先使用用户配置文件，而非系统文件。

   配置参数的详细信息，请参阅[ODBC配置页面]({% link docs/stable/clients/odbc/configuration.md %})。