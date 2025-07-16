---
---
layout: docu
redirect_from:
- /docs/guides/python/relational_api_pandas
title: Pandas上的关系型API
---

DuckDB 提供了一个关系型 API，可用于链接查询操作。这些操作是延迟评估的，这样 DuckDB 可以优化其执行。这些操作符可以作用于 Pandas 数据框、DuckDB 表或视图（这些视图可以指向任何 DuckDB 可以读取的底层存储格式，例如 CSV 或 Parquet 文件等）。以下我们展示了一个从 Pandas 数据框读取并返回数据框的简单示例。

```python
import duckdb
import pandas

# 连接到内存数据库
con = duckdb.connect()

input_df = pandas.DataFrame.from_dict({'i': [1, 2, 3, 4],
                                       'j': ["one", "two", "three", "four"]})

# 从数据框创建一个 DuckDB 关系
rel = con.from_df(input_df)

# 链接关系型操作符（这是一个延迟操作，因此操作尚未执行）
# 等效于：SELECT i, j, i*2 AS two_i FROM input_df WHERE i >= 2 ORDER BY i DESC LIMIT 2
transformed_rel = rel.filter('i >= 2').project('i, j, i*2 AS two_i').order('i DESC').limit(2)

# 通过请求 .df() 来触发执行
# .df() 可以添加在上述链的末尾，这里分开是为了更清晰
output_df = transformed_rel.df()
```

关系型操作符还可以用于分组、聚合、查找值的唯一组合、连接、并集等。它们还可以直接将结果插入 DuckDB 表或写入 CSV。

请参见 [这些额外示例](https://github.com/duckdb/duckdb/blob/main/examples/python/duckdb-python.py) 以及 [`DuckDBPyRelation` 类上可用的关系型方法]({% link docs/stable/clients/python/reference/index.md %}#duckdb.DuckDBPyRelation)。