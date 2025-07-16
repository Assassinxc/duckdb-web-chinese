---
---
layout: docu
redirect_from:
- /docs/guides/python/export_arrow
title: 导出到 Apache Arrow
---

可以使用 `arrow` 函数将查询的所有结果导出为 [Apache Arrow 表](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html)。或者，也可以使用 `fetch_record_batch` 函数将结果返回为 [RecordBatchReader](https://arrow.apache.org/docs/python/generated/pyarrow.ipc.RecordBatchStreamReader.html)，并逐批读取结果。此外，使用 DuckDB 的 [Relational API]({% link docs/stable/guides/python/relational_api_pandas.md %}) 构建的关系也可以导出。

## 导出到 Apache Arrow 表

```python
import duckdb
import pyarrow as pa

my_arrow_table = pa.Table.from_pydict({'i': [1, 2, 3, 4],
                                       'j': ["one", "two", "three", "four"]})

# 查询 Apache Arrow 表 "my_arrow_table" 并返回为 Arrow 表
results = duckdb.sql("SELECT * FROM my_arrow_table").arrow()
```

## 导出为 RecordBatchReader

```python
import duckdb
import pyarrow as pa

my_arrow_table = pa.Table.from_pydict({'i': [1, 2, 3, 4],
                                       'j': ["one", "two", "three", "four"]})

# 查询 Apache Arrow 表 "my_arrow_table" 并返回为 Arrow RecordBatchReader
chunk_size = 1_000_000
results = duckdb.sql("SELECT * FROM my_arrow_table").fetch_record_batch(chunk_size)

# 遍历结果。当 RecordBatchReader 为空时会抛出 StopIteration 异常
while True:
    try:
        # 在此处处理一个块（此处仅为示例，打印内容）
        print(results.read_next_batch().to_pandas())
    except StopIteration:
        print('已获取所有批次')
        break
```

## 从 Relational API 导出

Arrow 对象也可以从 Relational API 导出。可以使用 `arrow` 或 `to_arrow_table` 函数将关系转换为 Arrow 表，或者使用 `record_batch` 函数将关系转换为记录批次。可以使用 `arrow` 或别名 `fetch_arrow_table` 将结果导出为 Arrow 表，或者使用 `fetch_arrow_reader` 导出为 RecordBatchReader。

```python
import duckdb

# 连接到内存数据库
con = duckdb.connect()

con.execute('CREATE TABLE integers (i integer)')
con.execute('INSERT INTO integers VALUES (0), (1), (2), (3), (4), (5), (6), (7), (8), (9), (NULL)')

# 从表创建关系，并将整个关系导出为 Arrow
rel = con.table("integers")
relation_as_arrow = rel.arrow() # 或 .to_arrow_table()

# 或者，使用该关系计算一个结果，并将该结果导出为 Arrow
res = rel.aggregate("sum(i)").execute()
result_as_arrow = res.arrow() # 或 fetch_arrow_table()
```