---
---
layout: docu
redirect_from:
- /docs/guides/python/import_arrow
title: 从 Apache Arrow 导入
---

`CREATE TABLE AS` 和 `INSERT INTO` 可用于从任何查询创建表。我们可以通过在查询中引用 Apache Arrow 对象来创建表或插入到现有表中。此示例从 [Arrow 表](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html) 进行导入，但 DuckDB 可以根据 [SQL on Arrow 指南]({% link docs/stable/guides/python/sql_on_arrow.md %}) 查询不同的 Apache Arrow 格式。

```python
import duckdb
import pyarrow as pa

# 连接到内存数据库
my_arrow = pa.Table.from_pydict({'a': [42]})

# 从 DataFrame "my_arrow" 创建表 "my_table"
duckdb.sql("CREATE TABLE my_table AS SELECT * FROM my_arrow")

# 从 DataFrame "my_arrow" 插入到表 "my_table"
duckdb.sql("INSERT INTO my_table SELECT * FROM my_arrow")
```