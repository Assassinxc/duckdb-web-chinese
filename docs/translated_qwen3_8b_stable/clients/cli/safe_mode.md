---
---
layout: docu
redirect_from:
- /docs/clients/cli/safe_mode
title: 安全模式
---

DuckDB CLI 客户端支持“安全模式”。
在安全模式下，CLI 无法访问除最初连接的数据库文件之外的其他外部文件，并且无法与主机文件系统进行交互。

这会产生以下影响：

* 以下 [点命令]({% link docs/stable/clients/cli/dot_commands.md %}) 将被禁用：
    * `.cd`
    * `.excel`
    * `.import`
    * `.log`
    * `.once`
    * `.open`
    * `.output`
    * `.read`
    * `.sh`
    * `.system`
* 自动补全功能不再扫描文件系统以查找建议的自动补全目标。
* [`getenv` 函数]({% link docs/stable/clients/cli/overview.md %}#reading-environment-variables) 将被禁用。
* [`enable_external_access` 选项]({% link docs/stable/configuration/overview.md %}#configuration-reference) 被设置为 `false`。这意味着：
    * `ATTACH` 无法连接到文件中的数据库。
    * `COPY` 无法读取或写入文件。
    * 如 `read_csv`、`read_parquet`、`read_json` 等函数无法从外部源读取数据。

一旦激活安全模式，便无法在同一个 DuckDB CLI 会话中禁用。

如需了解如何在安全环境中运行 DuckDB，请参阅 [“保护 DuckDB”页面]({% link docs/stable/operations_manual/securing_duckdb/overview.md %})。