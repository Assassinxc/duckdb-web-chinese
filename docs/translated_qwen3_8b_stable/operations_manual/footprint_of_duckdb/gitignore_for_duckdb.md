---
---
layout: docu
redirect_from:
- /docs/operations_manual/footprint_of_duckdb/gitignore_for_duckdb
title: DuckDB 的 .gitignore 配置
---

如果你在使用 Git 仓库进行开发，可能希望配置你的 [Gitignore](https://git-scm.com/docs/gitignore) 来防止跟踪 [DuckDB 生成的文件]({% link docs/stable/operations_manual/footprint_of_duckdb/files_created_by_duckdb.md %}).
这些可能包括 DuckDB 数据库、预写日志（write ahead log）和临时文件。

## .gitignore 示例配置

以下展示了 DuckDB 的 .gitignore 配置片段示例。

### 忽略临时文件，保留数据库

如果你希望保留数据库文件在版本控制系统中，可以使用以下配置：

```text
*.wal
*.tmp/
```

### 忽略数据库和临时文件

如果你希望同时忽略数据库和临时文件，可以将 Gitignore 文件扩展以包含数据库文件。
实现此目的的精确 Gitignore 配置取决于你用于 DuckDB 数据库的扩展名（如 `.duckdb`、`.db`、`.ddb` 等）。
例如，如果你的 DuckDB 文件使用 `.duckdb` 扩展名，可以将以下行添加到你的 `.gitignore` 文件中：

```text
*.duckdb*
*.wal
*.tmp/
```