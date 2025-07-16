---
---
layout: docu
redirect_from:
- /docs/guides/python/export_pandas
title: 导出到 Pandas
---

可以使用 `df()` 函数将查询结果转换为 [Pandas](https://pandas.pydata.org/) DataFrame。

```python
import duckdb

# 将任意 SQL 查询结果读取到 Pandas DataFrame 中
results = duckdb.sql("SELECT 42").df()
results
```

```text
   42
0  42
```

## 参见

DuckDB 也支持 [从 Pandas 导入]({% link docs/stable/guides/python/import_pandas.md %})。