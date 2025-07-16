---
---
layout: docu
redirect_from:
- /docs/api/python/data_ingestion
- /docs/api/python/data_ingestion/
- /docs/clients/python/data_ingestion
title: 数据摄入
---

此页面包含使用 DuckDB 向 Python 摄入数据的示例。首先，导入 DuckDB 模块：

```python
import duckdb
```

然后，继续以下任一章节。

## CSV 文件

CSV 文件可以使用 `read_csv` 函数读取，该函数可以在 Python 中调用，也可以直接在 SQL 中调用。默认情况下，`read_csv` 函数会通过从提供的文件中采样来尝试自动检测 CSV 设置。

使用完全自动检测设置从文件中读取：

```python
duckdb.read_csv("example.csv")
```

从文件夹中读取多个 CSV 文件：

```python
duckdb.read_csv("folder/*.csv")
```

指定 CSV 内部格式的选项：

```python
duckdb.read_csv("example.csv", header = False, sep = ",")
```

覆盖前两列的类型：

```python
duckdb.read_csv("example.csv", dtype = ["int", "varchar"])
```

直接在 SQL 中读取 CSV 文件：

```python
duckdb.sql("SELECT * FROM 'example.csv'")
```

在 SQL 中调用 `read_csv`：

```python
duckdb.sql("SELECT * FROM read_csv('example.csv')")
```

更多信息请参阅 [CSV 导入]({% link docs/stable/data/csv/overview.md %}) 页面。

## Parquet 文件

Parquet 文件可以使用 `read_parquet` 函数读取，该函数可以在 Python 中调用，也可以直接在 SQL 中调用。

从单个 Parquet 文件中读取：

```python
duckdb.read_parquet("example.parquet")
```

从文件夹中读取多个 Parquet 文件：

```python
duckdb.read_parquet("folder/*.parquet")
```

从 [https]({% link docs/stable/core_extensions/httpfs/overview.md %}) 读取 Parquet 文件：

```python
duckdb.read_parquet("https://some.url/some_file.parquet")
```

读取 Parquet 文件列表：

```python
duckdb.read_parquet(["file1.parquet", "file2.parquet", "file3.parquet"])
```

直接在 SQL 中读取 Parquet 文件：

```python
duckdb.sql("SELECT * FROM 'example.parquet'")
```

在 SQL 中调用 `read_parquet`：

```python
duckdb.sql("SELECT * FROM read_parquet('example.parquet')")
```

更多信息请参阅 [Parquet 加载]({% link docs/stable/data/parquet/overview.md %}) 页面。

## JSON 文件

JSON 文件可以使用 `read_json` 函数读取，该函数可以在 Python 中调用，也可以直接在 SQL 中调用。默认情况下，`read_json` 函数会自动检测文件是否包含换行符分隔的 JSON 或常规 JSON，并会检测 JSON 文件中存储的对象的模式。

从单个 JSON 文件中读取：

```python
duckdb.read_json("example.json")
```

从文件夹中读取多个 JSON 文件：

```python
duckdb.read_json("folder/*.json")
```

直接在 SQL 中读取 JSON 文件：

```python
duckdb.sql("SELECT * FROM 'example.json'")
```

在 SQL 中调用 `read_json`：

```python
duckdb.sql("SELECT * FROM read_json_auto('example.json')")
```

## 直接访问 DataFrame 和 Arrow 对象

DuckDB 能够自动查询某些 Python 变量，通过其变量名（就像它是一个表一样）。
这些类型包括：Pandas DataFrame、Polars DataFrame、Polars LazyFrame、NumPy 数组、[关系]({% link docs/stable/clients/python/relational_api.md %}) 以及 Arrow 对象。

只有在 `sql()` 或 `execute()` 调用位置对 Python 代码可见的变量才能以这种方式使用。
通过 [替换扫描]({% link docs/stable/clients/c/replacement_scans.md %}) 可以访问这些变量。要完全禁用替换扫描，请使用：

```sql
SET python_enable_replacements = false;
```

DuckDB 支持查询多种类型的 Apache Arrow 对象，包括 [表](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html)、[数据集](https://arrow.apache.org/docs/python/generated/pyarrow.dataset.Dataset.html)、[RecordBatchReaders](https://arrow.apache.org/docs/python/generated/pyarrow.ipc.RecordBatchStreamReader.html) 和 [扫描器](https://arrow.apache.org/docs/python/generated/pyarrow.dataset.Scanner.html)。更多信息请参阅 Python [指南]({% link docs/stable/guides/overview.md %}#python-client)。

```python
import duckdb
import pandas as pd

test_df = pd.DataFrame.from_dict({"i": [1, 2, 3, 4], "j": ["one", "two", "three", "four"]})
print(duckdb.sql("SELECT * FROM test_df").fetchall())
```

```text
[(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four')]
```

DuckDB 还支持将 DataFrame 或 Arrow 对象“注册”为虚拟表，类似于 SQL 的 `VIEW`。这在查询以其他方式存储的 DataFrame/Arrow 对象（如类变量或字典中的值）时非常有用。以下是 Pandas 的示例：

如果您的 Pandas DataFrame 存储在另一个位置，以下是一个手动注册的示例：

```python
import duckdb
import pandas as pd

my_dictionary = {}
my_dictionary["test_df"] = pd.DataFrame.from_dict({"i": [1, 2, 3, 4], "j": ["one", "two", "three", "four"]})
duckdb.register("test_df_view", my_dictionary["test_df"])
print(duckdb.sql("SELECT * FROM test_df_view").fetchall())
```

```text
[(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four')]
```

您还可以从 DataFrame（或视图）的内容中在 DuckDB 中创建一个持久表：

```python
# 从 DataFrame 的内容创建一个新表
con.execute("CREATE TABLE test_df_table AS SELECT * FROM test_df")
# 从 DataFrame 的内容插入到现有表中
con.execute("INSERT INTO test_df_table SELECT * FROM test_df")
```

### Pandas DataFrame – `object` 列

`pandas.DataFrame` 中的 `object` 类型列需要一些特殊处理，因为它们存储任意类型的值。
在将这些列转换为 DuckDB 之前，我们首先进行一个分析阶段。
在分析阶段，会分析该列的所有行的样本以确定目标类型。
默认情况下，样本大小设为 1000。
如果在分析阶段选择的类型不正确，这将导致“无法转换值：”错误，此时您需要增加样本大小。
可以通过设置 `pandas_analyze_sample` 配置选项来更改样本大小。

```python
# 示例：设置样本大小为 100,000
duckdb.execute("SET GLOBAL pandas_analyze_sample = 100_000")
```

### 注册对象

您可以使用 [`DuckDBPyConnection.register()` 函数]({% link docs/stable/clients/python/reference/index.md %}#duckdb.DuckDBPyConnection.register) 将 Python 对象注册为 DuckDB 表。

具有相同名称的对象的优先级如下：

* 通过 `DuckDBPyConnection.register()` 显式注册的对象
* 原生 DuckDB 表和视图
* [替换扫描]({% link docs/stable/clients/c/replacement_scans.md %})