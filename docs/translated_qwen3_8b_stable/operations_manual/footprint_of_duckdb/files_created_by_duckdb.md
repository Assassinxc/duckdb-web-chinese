---
---
layout: docu
redirect_from:
- /docs/operations_manual/footprint_of_duckdb/files_created_by_duckdb
title: DuckDB 创建的文件
---

DuckDB 会在磁盘上创建若干文件和目录。本页面列出了全局和本地的文件。

## 全局文件和目录

DuckDB 会在用户的主目录（用 `~` 表示）中创建以下全局文件和目录：

| 位置 | 描述 | 是否跨版本共享 | 是否跨客户端共享 |
|-------|-------------------|--|--|
| `~/.duckdbrc` | 该文件的内容在启动 [DuckDB CLI 客户端]({% link docs/stable/clients/cli/overview.md %}) 时执行。命令可以是 [点命令]({% link docs/stable/clients/cli/dot_commands.md %}) 或 SQL 语句。该文件的命名遵循 `~/.bashrc` 和 `~/.zshrc` “运行命令” 文件的命名规则。 | 是 | 仅 CLI 使用 |
| `~/.duckdb_history` | 历史文件，类似于 `~/.bash_history` 和 `~/.zsh_history`。用于 [DuckDB CLI 客户端]({% link docs/stable/clients/cli/overview.md %})。 | 是 | 仅 CLI 使用 |
| `~/.duckdb/extensions` | 已安装 [扩展]({% link docs/stable/core_extensions/overview.md %}) 的二进制文件。 | 否 | 是 |
| `~/.duckdb/stored_secrets` | 由 [Secrets manager]({% link docs/stable/configuration/secrets_manager.md %}) 创建的 [持久化密钥]({% link docs/stable/configuration/secrets_manager.md %}#persistent-secrets)。 | 是 | 是 |

## 本地文件和目录

DuckDB 会在工作目录（用于内存连接）或相对于数据库文件的位置（用于持久连接）创建以下文件和目录：

| 名称 | 描述 | 示例 |
|-------|-------------------|---|
| `⟨database_filename⟩`{:.language-sql .highlight} | 数据库文件。仅在磁盘模式下创建。该文件可以具有任何扩展名，常见的扩展名包括 `.duckdb`、`.db` 和 `.ddb`。 | `weather.duckdb` |
| `.tmp/` | 临时目录。仅在内存模式下创建。 | `.tmp/` |
| `⟨database_filename⟩.tmp/`{:.language-sql .highlight} | 临时目录。仅在磁盘模式下创建。 | `weather.tmp/` |
| `⟨database_filename⟩.wal`{:.language-sql .highlight} | [预写日志](https://en.wikipedia.org/wiki/Write-ahead_logging) 文件。如果 DuckDB 正常退出，WAL 文件会在退出时被删除。如果 DuckDB 崩溃，WAL 文件用于恢复数据。 | `weather.wal` |

如果你正在使用 Git 仓库，并希望禁用 Git 对这些文件的跟踪，请参阅 [DuckDB 的 `.gitignore` 使用指南]({% link docs/stable/operations_manual/footprint_of_duckdb/gitignore_for_duckdb.md %})。