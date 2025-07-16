---
---
layout: docu
redirect_from:
- /docs/api/python/spark_api
- /docs/api/python/spark_api/
- /docs/clients/python/spark_api
title: Spark API
---

DuckDB 的 Spark API 实现了 [PySpark API](https://spark.apache.org/docs/3.5.0/api/python/reference/index.html)，允许您使用熟悉的 Spark API 与 DuckDB 进行交互。
所有语句均通过我们的 [关系型 API]({% link docs/stable/clients/python/relational_api.md %}) 转换为 DuckDB 的内部计划，并通过 DuckDB 的查询引擎执行。

> 警告 DuckDB 的 Spark API 当前仍为实验性功能，部分功能尚未实现。我们非常欢迎您的反馈。如果您发现缺少任何功能，请通过 [Discord](https://discord.duckdb.org) 或 [GitHub](https://github.com/duckdb/duckdb/issues) 报告。

## 示例

```python
from duckdb.experimental.spark.sql import SparkSession as session
from duckdb.experimental.spark.sql.functions import lit, col
import pandas as pd

spark = session.builder.getOrCreate()

pandas_df = pd.DataFrame({
    'age': [34, 45, 23, 56],
    'name': ['Joan', 'Peter', 'John', 'Bob']
})

df = spark.createDataFrame(pandas_df)
df = df.withColumn(
    'location', lit('Seattle')
)
res = df.select(
    col('age'),
    col('location')
).collect()

print(res)
```

```text
[
    Row(age=34, location='Seattle'),
    Row(age=45, location='Seattle'),
    Row(age=23, location='Seattle'),
    Row(age=56, location='Seattle')
]
```

## 贡献指南

欢迎为实验性的 Spark API 提交贡献。
在进行贡献时，请遵循以下指南：

* 请使用我们的 `pytest` 测试框架，而非临时文件。
* 添加新功能时，请确保方法签名与 [PySpark API](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/index.html) 中的保持一致。