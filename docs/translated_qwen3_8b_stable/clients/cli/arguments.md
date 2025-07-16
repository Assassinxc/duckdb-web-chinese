---
---
layout: docu
redirect_from:
- /docs/cli/arguments
- /docs/cli/arguments/
- /docs/clients/cli/arguments
title: 命令行参数
---

下面的表格总结了 DuckDB 的命令行选项。
要列出所有命令行选项，请使用以下命令：

```bash
duckdb -help
```

有关 CLI shell 中可用的点命令，请参阅 [点命令页面]({% link docs/stable/clients/cli/dot_commands.md %}).

<!-- markdownlint-disable MD056 -->

| 参数          | 描述                                                                                                   |
| ------------- | ----------------------------------------------------------------------------------------------------- |
| `-append`     | 将数据库追加到文件末尾                                                                                 |
| `-ascii`      | 设置 [输出模式]({% link docs/stable/clients/cli/output_formats.md %}) 为 `ascii`                      |
| `-bail`       | 在遇到错误后停止                                                                                       |
| `-batch`      | 强制使用批量 I/O                                                                                       |
| `-box`        | 设置 [输出模式]({% link docs/stable/clients/cli/output_formats.md %}) 为 `box`                         |
| `-column`     | 设置 [输出模式]({% link docs/stable/clients/cli/output_formats.md %}) 为 `column`                      |
| `-cmd COMMAND` | 在读取 `stdin` 之前运行 `COMMAND`                                                                      |
| `-c COMMAND`  | 运行 `COMMAND` 并退出                                                                                   |
| `-csv`        | 设置 [输出模式]({% link docs/stable/clients/cli/output_formats.md %}) 为 `csv`                         |
| `-echo`       | 在执行前打印命令                                                                                       |
| `-f FILENAME` | 运行 `FILENAME` 中的脚本并退出。注意：会先读取并执行 `~/.duckdbrc`（如果存在）                         |
| `-init FILENAME` | 在启动时运行 `FILENAME` 中的脚本（而不是 `~/.duckdbrc`）                                               |
| `-header`     | 启用标题                                                                                               |
| `-help`       | 显示此消息                                                                                             |
| `-html`       | 设置 [输出模式]({% link docs/stable/clients/cli/output_formats.md %}) 为 HTML                         |
| `-interactive` | 强制使用交互式 I/O                                                                                     |
| `-json`       | 设置 [输出模式]({% link docs/stable/clients/cli/output_formats.md %}) 为 `json`                        |
| `-line`       | 设置 [输出模式]({% link docs/stable/clients/cli/output_formats.md %}) 为 `line`                        |
| `-list`       | 设置 [输出模式]({% link docs/stable/clients/cli/output_formats.md %}) 为 `list`                        |
| `-markdown`   | 设置 [输出模式]({% link docs/stable/clients/cli/output_formats.md %}) 为 `markdown`                    |
| `-newline SEP` | 设置输出行分隔符。默认值：`\n`                                                                         |
| `-nofollow`   | 拒绝打开指向数据库文件的符号链接                                                                       |
| `-noheader`   | 关闭标题                                                                                               |
| `-no-stdin`   | 处理选项后退出，而不是读取 stdin                                                                       |
| `-nullvalue TEXT` | 设置 `NULL` 值的文本字符串。默认值：`NULL`                                                             |
| `-quote`      | 设置 [输出模式]({% link docs/stable/clients/cli/output_formats.md %}) 为 `quote`                       |
| `-readonly`   | 以只读方式打开数据库。此选项还支持通过 HTTPS 连接到远程数据库                                         |
| `-s COMMAND`  | 运行 `COMMAND` 并退出                                                                                   |
| `-separator SEP` | 设置输出列分隔符为 `SEP`。默认值：`|`                                                                   |
| `-table`      | 设置 [输出模式]({% link docs/stable/clients/cli/output_formats.md %}) 为 `table`                       |
| `-ui`         | 加载并启动 [DuckDB UI]({% link docs/stable/core_extensions/ui.md %})。如果 UI 尚未安装，它会安装 `ui` 扩展 |
| `-unsigned`   | 允许加载 [无签名扩展]({% link docs/stable/core_extensions/overview.md %}#unsigned-extensions)。此选项旨在用于开发扩展。请参阅 [保护 DuckDB 页面]({% link docs/stable/operations_manual/securing_duckdb/securing_extensions.md %}) 以了解如何安全地设置 DuckDB |
| `-version`    | 显示 DuckDB 版本                                                                                       |

<!-- markdownlint-enable MD056 -->

## 传递参数序列

请注意，CLI 参数按顺序处理，与 SQLite CLI 的行为类似。
例如：

```bash
duckdb -csv -c 'SELECT 42 AS hello' -json -c 'SELECT 84 AS world'
```

返回以下结果：

```text
hello
42
[{"world":84}]
```