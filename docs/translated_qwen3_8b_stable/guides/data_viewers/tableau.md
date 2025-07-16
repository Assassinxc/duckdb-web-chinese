---
---
layout: docu
redirect_from:
- /docs/guides/data_viewers/tableau
title: Tableau – 数据可视化工具
---

[Tableau](https://www.tableau.com/) 是一种流行的商业数据可视化工具。
除了大量的内置连接器外，
它还通过 ODBC 和 JDBC 连接器提供通用的数据库连接功能。

Tableau 有两个主要版本：桌面版和在线版（服务器版）。

* 对于桌面版，连接到 DuckDB 数据库与在嵌入式环境（如 Python）中工作类似。
* 对于在线版，由于 DuckDB 是进程内运行的，因此数据必须位于服务器本身

或在可以从服务器访问的远程数据存储桶中。

## 数据库创建

当使用 DuckDB 数据库文件时，
数据集实际上不需要导入到 DuckDB 表中；
只需创建数据的视图即可。
例如，以下代码将在当前 DuckDB 代码库中创建一个 `h2oai` Parquet 测试文件的视图：

```sql
CREATE VIEW h2oai AS (
    FROM read_parquet('/Users/username/duckdb/data/parquet-testing/h2oai/h2oai_group_small.parquet')
);
```

请注意，您应使用本地文件的完整路径，以便从 Tableau 内部找到它们。
另外请注意，您需要使用与创建文件时所用的 DuckDB 工具（如 Python 模块、命令行）所使用的数据库格式兼容的驱动程序版本。

## 安装 JDBC 驱动程序

Tableau 提供了如何 [安装 JDBC 驱动程序](https://help.tableau.com/current/pro/desktop/en-gb/jdbc_tableau.htm)
的文档，供 Tableau 使用。

> Tableau（桌面版和服务器版）在您添加或修改驱动程序时都需要重启。

### 驱动程序链接

此处的链接是与 Tableau 兼容的 JDBC 驱动程序的最新版本。
如果您要连接到数据库文件，
您需要确保该文件是使用与文件兼容的 DuckDB 版本创建的。
另外，请检查是否只安装了一个驱动程序版本，因为有多个文件名在使用中。

<!-- markdownlint-disable MD034 -->
下载 [JAR 文件](https://repo1.maven.org/maven2/org/duckdb/duckdb_jdbc/{{ site.current_duckdb_java_version }}/duckdb_jdbc-{{ site.current_duckdb_java_version }}.jar)。
<!-- markdownlint-enable MD034 -->

* macOS：复制到 `~/Library/Tableau/Drivers/`
* Windows：复制到 `C:\Program Files\Tableau\Drivers`
* Linux：复制到 `/opt/tableau/tableau_driver/jdbc`。

## 使用 PostgreSQL 语法

如果您只是想做一些简单的事情，可以尝试直接连接到 JDBC 驱动程序
并使用 Tableau 提供的 PostgreSQL 语法。

1. 创建一个包含您的视图和/或数据的 DuckDB 文件。
2. 启动 Tableau。
3. 在“连接”>“到服务器”>“更多…”中点击“其他数据库（JDBC）”，这将打开连接对话框。在 URL 中输入 `jdbc:duckdb:/User/username/path/to/database.db`。在语法中选择 PostgreSQL。其余字段可以忽略：

![Tableau PostgreSQL](/images/guides/tableau/tableau-osx-jdbc.png)

然而，像 `median` 和 `percentile` 聚合函数等功能将缺失。
为了使数据源连接更兼容 PostgreSQL 语法，
请使用下面描述的 DuckDB taco 连接器。

## 安装 Tableau DuckDB 连接器

虽然可以使用 Tableau 提供的 PostgreSQL 语法与 DuckDB JDBC 驱动程序通信，
但我们强烈建议使用 [DuckDB "taco" 连接器](https://github.com/motherduckdb/duckdb-tableau-connector)。
此连接器已完全测试过与 Tableau 语法生成器的兼容性，
并且比提供的 PostgreSQL 语法更兼容。

如何安装和使用该连接器的文档在其仓库中，
但基本上您需要
[`duckdb_jdbc.taco`](https://github.com/motherduckdb/duckdb-tableau-connector/raw/main/packaged-connector/duckdb_jdbc-v1.0.0-signed.taco) 文件。
（尽管 Tableau 文档中提到的是这样，但真正的安全风险在于 JDBC 驱动程序代码，
而不是 Taco 中少量的 JavaScript。）

### 服务器（在线）

在 Linux 上，将 Taco 文件复制到 `/opt/tableau/connectors`。
在 Windows 上，将 Taco 文件复制到 `C:\Program Files\Tableau\Connectors`。
然后执行以下命令以禁用签名验证：

```bash
tsm configuration set -k native_api.disable_verify_connector_plugin_signature -v true
```

```bash
tsm pending-changes apply
```

最后一条命令将重启服务器以应用新设置。

### macOS

将 Taco 文件复制到 `/Users/[User]/Documents/My Tableau Repository/Connectors` 文件夹。
然后通过命令行参数禁用签名验证来从终端启动 Tableau Desktop：

```bash
/Applications/Tableau\ Desktop\ ⟨year⟩.⟨quarter⟩.app/Contents/MacOS/Tableau -DDisableVerifyConnectorPluginSignature=true
```

您也可以使用以下脚本通过 AppleScript 封装此操作：

```tableau
do shell script "\"/Applications/Tableau Desktop 2023.2.app/Contents/MacOS/Tableau\" -DDisableVerifyConnectorPluginSignature=true"
quit
```

通过 [Script Editor](https://support.apple.com/guide/script-editor/welcome/mac)
（位于 `/Applications/Utilities`）创建此文件，
并 [将其保存为打包应用程序](https://support.apple.com/guide/script-editor/save-a-script-as-an-app-scpedt1072/mac)：

![tableau-applescript](/images/guides/tableau/applescript.png)

然后您可以通过双击该文件启动 Tableau。
在获得升级时，您需要更改脚本中的应用程序名称。

### Windows 桌面

将 Taco 文件复制到 `C:\Users\[Windows User]\Documents\My Tableau Repository\Connectors` 目录。
然后通过 `-DDisableVerifyConnectorPluginSignature=true` 参数启动 Tableau Desktop 以禁用签名验证。

## 输出

加载完成后，您可以对数据运行查询！
以下是来自 Parquet 测试文件的第一个 H2O.ai 基准查询结果：

![tableau-parquet](/images/guides/tableau/h2oai-group-by-1.png)