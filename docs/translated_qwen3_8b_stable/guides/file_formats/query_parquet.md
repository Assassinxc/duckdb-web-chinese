---
---
layout: docu
redirect_from:
- /docs/guides/import/query_parquet
- /docs/guides/import/query_parquet/
- /docs/guides/file_formats/query_parquet
title: 查询 Parquet 文件
---

要直接对 Parquet 文件运行查询，请在查询的 `FROM` 子句中使用 `read_parquet` 函数。

```sql
SELECT * FROM read_parquet('input.parquet');
```

Parquet 文件将并行处理。过滤条件会自动下推到 Parquet 扫描中，仅读取相关的列。

如需更多信息，请参阅博客文章 [“使用 DuckDB 精确查询 Parquet 文件”]({% post_url 2021-06-25-querying-parquet %})。