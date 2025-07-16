---
---
layout: docu
redirect_from:
- /docs/guides/python/sql_on_arrow
title: SQL on Apache Arrow
---

DuckDB 可以查询多种不同类型的 Apache Arrow 对象。

## Apache Arrow 表

[Arrow 表](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html) 存储在本地变量中，可以像 DuckDB 中的普通表一样进行查询。

```python
import duckdb
import pyarrow as pa

# 连接到内存数据库
con = duckdb.connect()

my_arrow_table = pa.Table.from_pydict({'i': [1, 2, 3, 4],
                                       'j': ["one", "two", "three", "four"]})

# 查询 Apache Arrow 表 "my_arrow_table" 并返回为 Arrow 表
results = con.execute("SELECT * FROM my_arrow_table WHERE i = 2").arrow()
```

## Apache Arrow 数据集

[Arrow 数据集](https://arrow.apache.org/docs/python/dataset.html) 存储为变量也可以像普通表一样进行查询。
数据集可用于指向 Parquet 文件目录以分析大型数据集。
DuckDB 会将列选择和行过滤下推到数据集扫描操作中，以便只将必要的数据加载到内存中。

```python
import duckdb
import pyarrow as pa
import tempfile
import pathlib
import pyarrow.parquet as pq
import pyarrow.dataset as ds

# 连接到内存数据库
con = duckdb.connect()

my_arrow_table = pa.Table.from_pydict({'i': [1, 2, 3, 4],
                                       'j': ["one", "two", "three", "four"]})

# 创建示例 Parquet 文件并保存在文件夹中
base_path = pathlib.Path(tempfile.gettempdir())
(base_path / "parquet_folder").mkdir(exist_ok = True)
pq.write_to_dataset(my_arrow_table, str(base_path / "parquet_folder"))

# 使用 Arrow 数据集链接到 Parquet 文件
my_arrow_dataset = ds.dataset(str(base_path / 'parquet_folder/'))

# 查询 Apache Arrow 数据集 "my_arrow_dataset" 并返回为 Arrow 表
results = con.execute("SELECT * FROM my_arrow_dataset WHERE i = 2").arrow()
```

## Apache Arrow 扫描器

[Arrow 扫描器](https://arrow.apache.org/docs/python/generated/pyarrow.dataset.Scanner.html) 存储为变量也可以像普通表一样进行查询。扫描器会遍历数据集并选择特定列或应用行级过滤。这与 DuckDB 将列选择和过滤下推到 Arrow 数据集的方式类似，但使用的是 Arrow 计算操作。Arrow 可以使用异步 IO 快速访问文件。

```python
import duckdb
import pyarrow as pa
import tempfile
import pathlib
import pyarrow.parquet as pq
import pyarrow.dataset as ds
import pyarrow.compute as pc

# 连接到内存数据库
con = duckdb.connect()

my_arrow_table = pa.Table.from_pydict({'i': [1, 2, 3, 4],
                                       'j': ["one", "two", "three", "four"]})

# 创建示例 Parquet 文件并保存在文件夹中
base_path = pathlib.Path(tempfile.gettempdir())
(base_path / "parquet_folder").mkdir(exist_ok = True)
pq.write_to_dataset(my_arrow_table, str(base_path / "parquet_folder"))

# 使用 Arrow 数据集链接到 Parquet 文件
my_arrow_dataset = ds.dataset(str(base_path / 'parquet_folder/'))

# 定义在扫描过程中应用的过滤器
# 等价于 "WHERE i = 2"
scanner_filter = (pc.field("i") == pc.scalar(2))

arrow_scanner = ds.Scanner.from_dataset(my_arrow_dataset, filter = scanner_filter)

# 查询 Apache Arrow 扫描器 "arrow_scanner" 并返回为 Arrow 表
results = con.execute("SELECT * FROM arrow_scanner").arrow()
```

## Apache Arrow RecordBatchReader

[Arrow RecordBatchReader](https://arrow.apache.org/docs/python/generated/pyarrow.RecordBatchReader.html) 是 Arrow 的流式二进制格式的读取器，也可以直接像表一样进行查询。这种流式格式在将 Arrow 数据发送用于进程间通信或不同语言运行时之间的通信等任务时非常有用。

```python
import duckdb
import pyarrow as pa

# 连接到内存数据库
con = duckdb.connect()

my_recordbatch = pa.RecordBatch.from_pydict({'i': [1, 2, 3, 4],
                                             'j': ["one", "two", "three", "four"]})

my_recordbatchreader = pa.ipc.RecordBatchReader.from_batches(my_recordbatch.schema, [my_recordbatch])

# 查询 Apache Arrow RecordBatchReader "my_recordbatchreader" 并返回为 Arrow 表
results = con.execute("SELECT * FROM my_recordbatchreader WHERE i = 2").arrow()
```