---
---
layout: docu
redirect_from:
- /docs/guides/python/sql_on_pandas
title: Pandas 上的 SQL
---

本地变量中存储的 Pandas DataFrames 可以像 DuckDB 中的常规表一样进行查询。

```python
import duckdb
import pandas

# 创建一个 Pandas dataframe
my_df = pandas.DataFrame.from_dict({'a': [42]})

# 查询 Pandas DataFrame "my_df"
# 注意：duckdb.sql 连接到默认的内存数据库连接
results = duckdb.sql("SELECT * FROM my_df").df()
```

通过 [替换扫描]({% link docs/stable/clients/c/replacement_scans.md %})，Pandas DataFrames 与 DuckDB SQL 查询实现了无缝集成。该功能将访问 `my_df` 表（在 DuckDB 中不存在）的实例替换为读取 `my_df` dataframe 的表函数。