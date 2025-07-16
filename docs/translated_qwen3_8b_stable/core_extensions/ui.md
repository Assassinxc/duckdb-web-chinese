---
---
github_repository: https://github.com/duckdb/duckdb-ui
layout: docu
title: UI 扩展
redirect_from:
- /docs/stable/extensions/ui
- /docs/stable/extensions/ui/
- /docs/extensions/ui
- /docs/extensions/ui/
---

`ui` 扩展为本地 DuckDB 实例添加了一个用户界面。

该 UI 由 [MotherDuck](https://motherduck.com/) 构建和维护。
其功能概览可以在 [MotherDuck 文档](https://motherduck.com/docs/getting-started/motherduck-quick-tour/) 中找到。

## 要求

* 一个带有浏览器的环境。
* 任何 DuckDB 客户端，除了 Wasm、v1.2.1 或更高版本。

## 使用方法

从命令行启动 UI：

```bash
duckdb -ui
```

从 SQL 启动 UI：

```sql
CALL start_ui();
```

运行其中任意一种方式都会在默认浏览器中打开 UI。

该 UI 连接到启动时的 DuckDB 实例，
因此你之前加载的所有数据都将可用。
由于此实例是本地进程（非 Wasm），它可以利用你本地环境的所有资源：所有核心、内存和文件。
关闭此实例会导致 UI 停止工作。

该 UI 由嵌入在 DuckDB 中的 HTTP 服务器提供服务。
若要启动此服务器而不启动浏览器，请运行：

```sql
CALL start_ui_server();
```

然后，你可以通过访问 `http://localhost:4213` 在浏览器中加载 UI。

要停止 HTTP 服务器，请运行：

```sql
CALL stop_ui_server();
```

## 本地查询执行

默认情况下，DuckDB UI 会在本地完全运行你的查询：你的查询和数据永远不会离开你的电脑。
如果你想通过 UI 使用 [MotherDuck](https://motherduck.com/)，你必须显式选择并登录 MotherDuck。

## 配置

### 本地端口

可以通过 SQL 命令配置 HTTP 服务器的本地端口，例如：

```sql
SET ui_local_port = 4213;
```

也可以使用环境变量 `ui_local_port`。

默认端口是 4213。（为什么？4 = D，21 = U，3 = C）

### 远程 URL

本地 HTTP 服务器从远程 HTTP 服务器获取 UI 的文件，以便保持最新。

默认的远程服务器 URL 是 <https://ui.duckdb.org>。

可以通过 SQL 命令配置其他远程 URL，例如：

```sql
SET ui_remote_url = 'https://ui.duckdb.org';
```

也可以使用环境变量 `ui_remote_port`。

此设置主要用于测试目的。

请确保你信任任何配置的 URL，因为应用程序可以访问你加载到 DuckDB 中的数据。

由于此风险，只有在 `allow_unsigned_extensions` 启用时，此设置才会被尊重。

### 轮询间隔

UI 扩展在后台线程中轮询某些信息。
它会监视已连接数据库列表的变化，并检测你是否连接到 MotherDuck。

这些检查耗时非常短，因此默认轮询间隔很短（284 毫秒）。
你可以通过 SQL 命令配置它，例如：

```sql
SET ui_polling_interval = 284;
```

也可以使用环境变量 `ui_polling_interval`。

将轮询间隔设置为 0 会完全禁用轮询。
这不推荐，因为 UI 中的数据库列表可能会过时，而且某些连接到 MotherDuck 的方式可能无法正常工作。

## 小贴士

### 使用 DuckDB UI 打开 CSV 文件

使用 [DuckDB CLI 客户端]({% link docs/stable/clients/cli/overview.md %})，
你可以通过 [`-cmd` 参数]({% link docs/stable/clients/cli/arguments.md %}) 以 CSV 文件作为视图启动 UI：

```bash
duckdb -cmd "CREATE VIEW ⟨view_name⟩ AS FROM '⟨filename⟩.csv';" -ui
```

### 以只读模式运行 UI

DuckDB UI 内部使用 DuckDB 表作为存储（例如，保存笔记本）。
因此，直接在只读数据库上运行 UI 是不支持的 [详见](https://github.com/duckdb/duckdb-ui/issues/61)：

```bash
duckdb -ui -readonly read_only_test.db
```

在 UI 中，这会引发以下错误：

```console
Catalog Error: SET schema: No catalog + schema named "memory.main" found.
```

要解决此问题，可以在另一个数据库文件上运行 UI：

```bash
duckdb -ui ui_catalog.db
```

然后打开一个笔记本并连接到数据库：

```sql
ATTACH 'test.db' (READ_ONLY) AS my_db;
USE my_db
```

## 局限性

* 当前 UI 不支持基于 ARM 的 Windows 平台（`windows_arm64` 和 `windows_arm64_mingw`）。