---
---
layout: docu
redirect_from:
- /docs/guides/import/http_import
- /docs/guides/import/http_import/
- /docs/guides/network_cloud_storage/http_import
title: HTTP Parquet 导入
---

通过 HTTP(S) 加载 Parquet 文件需要使用 [`httpfs` 扩展]({% link docs/stable/core_extensions/httpfs/overview.md %})。可以通过 `INSTALL` SQL 命令进行安装。只需要运行一次即可。

```sql
INSTALL httpfs;
```

为了使用 `httpfs` 扩展，可以使用 `LOAD` SQL 命令：

```sql
LOAD httpfs;
```

在设置好 `httpfs` 扩展后，可以通过 `http(s)` 读取 Parquet 文件：

```sql
SELECT * FROM read_parquet('https://⟨domain⟩/path/to/file.parquet');
```

例如：

```sql
SELECT * FROM read_parquet('https://duckdb.org/data/prices.parquet');
```

如果 URL 以 `.parquet` 结尾，可以省略 `read_parquet` 函数：

```sql
SELECT * FROM read_parquet('https://duckdb.org/data/holdings.parquet');
```

此外，由于 DuckDB 的 [替换扫描机制]({% link docs/stable/clients/c/replacement_scans.md %})，`read_parquet` 函数本身也可以被省略：

```sql
SELECT * FROM 'https://duckdb.org/data/holdings.parquet';
```