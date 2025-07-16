---
---
layout: docu
redirect_from:
- /docs/guides/python/import_pandas
title: 从Pandas导入
---

[`CREATE TABLE ... AS`]({% link docs/stable/sql/statements/create_table.md %}#create-table--as-select-ctas) 和 [`INSERT INTO`]({% link docs/stable/sql/statements/insert.md %}) 可用于从任意查询创建表。
我们可以通过在查询中引用 [Pandas](https://pandas.pydata.org/) 的 DataFrame 来创建表或插入到现有表中。
无需手动注册 DataFrame –
由于 [replacement scans]({% link docs/stable/guides/glossary.md %}#replacement-scan)，DuckDB 可以通过名称在 Python 进程中找到它们。

```python
import duckdb
import pandas

# 创建一个 Pandas DataFrame
my_df = pandas.DataFrame.from_dict({'a': [42]})

# 从 DataFrame "my_df" 创建表 "my_table"
# 注意：duckdb.sql 连接到默认的内存数据库连接
duckdb.sql("CREATE TABLE my_table AS SELECT * FROM my_df")

# 从 DataFrame "my_df" 插入到表 "my_table"
duckdb.sql("INSERT INTO my_table SELECT * FROM my_df")
```

如果列的顺序不同或 DataFrame 中不包含所有列，请使用 [`INSERT INTO ... BY NAME`]({% link docs/stable/sql/statements/insert.md %}#insert-into--by-name)：

```python
duckdb.sql("INSERT INTO my_table BY NAME SELECT * FROM my_df")
```

## 参见

DuckDB 还支持 [导出到 Pandas]({% link docs/stable/guides/python/export_pandas.md %})。