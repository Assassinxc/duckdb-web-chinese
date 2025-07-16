---
---
layout: docu
redirect_from:
- /docs/operations_manual/embedding_duckdb
- /docs/stable/operations_manual/embedding_duckdb
title: 嵌入 DuckDB
---

## CLI 客户端

[命令行界面（CLI）客户端]({% link docs/stable/clients/cli/overview.md %}) 适用于交互式使用场景，而非嵌入式使用。
因此，它具有更多功能，这些功能可能被恶意用户滥用。
例如，CLI 客户端具有 `.sh` 功能，允许执行任意的 shell 命令。
此功能仅存在于 CLI 客户端中，而不在任何其他 DuckDB 客户端中。

```sql
.sh ls
```

> 提示 通过 shell 命令调用 DuckDB 的 CLI 客户端以**嵌入 DuckDB**是**不推荐**的。建议使用其中一个客户端库，例如 [Python]({% link docs/stable/clients/python/overview.md %})、[R]({% link docs/stable/clients/r.md %})、[Java]({% link docs/stable/clients/java.md %}) 等。