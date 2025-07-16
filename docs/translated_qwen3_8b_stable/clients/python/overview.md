---
---
layout: docu
redirect_from:
- /docs/api/python
- /docs/api/python/
- /docs/api/python/overview
- /docs/api/python/overview/
- /docs/clients/python/overview
title: Python API
---

> DuckDB Python客户端的最新版本是 {{ site.current_duckdb_version }}。

## 安装

可以通过 [pip](https://pip.pypa.io) 安装 DuckDB Python API：`pip install duckdb`。请参阅 [安装页面]({% link docs/installation/index.html %}?environment=python) 获取更多详情。也可以通过 [conda](https://docs.conda.io) 进行安装：`conda install python-duckdb -c conda-forge`。

**Python 版本：**
DuckDB 需要 Python 3.9 或更高版本。

## 基础 API 使用

使用 DuckDB 运行 SQL 查询最直接的方式是使用 `duckdb.sql` 命令。

```python
import duckdb

duckdb.sql("SELECT 42").show()
```

这会使用一个 **内存数据库** 来运行查询，该数据库存储在 Python 模块中。查询的结果返回为一个 **关系**。关系是对查询的符号表示。查询在获取结果或请求打印到屏幕时才会执行。

可以通过将关系存储在变量中并在后续查询中引用它们来引用关系，这样可以逐步构建查询。

```python
import duckdb

r1 = duckdb.sql("SELECT 42 AS i")
duckdb.sql("SELECT i * 2 AS k FROM r1").show()
```

## 数据输入

DuckDB 可以从各种格式的数据中读取数据，包括磁盘上的和内存中的。更多信息请参阅 [数据摄入页面]({% link docs/stable/clients/python/data_ingestion.md %}).

```python
import duckdb

duckdb.read_csv("example.csv")                # 从 CSV 文件中读取数据到关系
duckdb.read_parquet("example.parquet")        # 从 Parquet 文件中读取数据到关系
duckdb.read_json("example.json")              # 从 JSON 文件中读取数据到关系

duckdb.sql("SELECT * FROM 'example.csv'")     # 直接查询 CSV 文件
duckdb.sql("SELECT * FROM 'example.parquet'") # 直接查询 Parquet 文件
duckdb.sql("SELECT * FROM 'example.json'")    # 直接查询 JSON 文件
```

### 数据框

DuckDB 可以直接查询 Pandas 数据框、Polars 数据框和 Arrow 表。
请注意，这些是只读的，即不能通过 [`INSERT`]({% link docs/stable/sql/statements/insert.md %}) 或 [`UPDATE` 语句]({% link docs/stable/sql/statements/update.md %}) 编辑这些表。

#### Pandas

要直接查询 Pandas 数据框，请运行：

```python
import duckdb
import pandas as pd

pandas_df = pd.DataFrame({"a": [42]})
duckdb.sql("SELECT * FROM pandas_df")
```

```text
┌───────┐
│   a   │
│ int64 │
├───────┤
│    42 │
└───────┘
```

#### Polars

要直接查询 Polars 数据框，请运行：

```python
import duckdb
import polars as pl

polars_df = pl.DataFrame({"a": [42]})
duckdb.sql("SELECT * FROM polars_df")
```

```text
┌───────┐
│   a   │
│ int64 │
├───────┤
│    42 │
└───────┘
```

#### PyArrow

要直接查询 PyArrow 表，请运行：

```python
import duckdb
import pyarrow as pa

arrow_table = pa.Table.from_pydict({"a": [42]})
duckdb.sql("SELECT * FROM arrow_table")
```

```text
┌───────┐
│   a   │
│ int64 │
├───────┤
│    42 │
└───────┘
```

## 结果转换

DuckDB 支持将查询结果高效地转换为多种格式。更多信息请参阅 [结果转换页面]({% link docs/stable/clients/python/conversion.md %}).

```python
import duckdb

duckdb.sql("SELECT 42").fetchall()   # Python 对象
duckdb.sql("SELECT 42").df()         # Pandas 数据框
duckdb.sql("SELECT 42").pl()         # Polars 数据框
duckdb.sql("SELECT 42").arrow()      # Arrow 表
duckdb.sql("SELECT 42").fetchnumpy() # NumPy 数组
```

## 写入磁盘数据

DuckDB 支持将关系对象直接写入磁盘的多种格式。可以使用 [`COPY` 语句]({% link docs/stable/sql/statements/copy.md %}) 通过 SQL 作为替代方式将数据写入磁盘。

```python
import duckdb

duckdb.sql("SELECT 42").write_parquet("out.parquet") # 写入 Parquet 文件
duckdb.sql("SELECT 42").write_csv("out.csv")         # 写入 CSV 文件
duckdb.sql("COPY (SELECT 42) TO 'out.parquet'")      # 复制到 Parquet 文件
```

## 连接选项

应用程序可以通过 `duckdb.connect()` 方法打开一个新的 DuckDB 连接。

### 使用内存数据库

使用 `duckdb.sql()` 时，DuckDB 操作的是一个 **内存数据库**，即不会在磁盘上持久化任何表。
不带参数调用 `duckdb.connect()` 方法返回一个连接，该连接也使用内存数据库：

```python
import duckdb

con = duckdb.connect()
con.sql("SELECT 42 AS x").show()
```

### 持久化存储

`duckdb.connect(dbname)` 创建一个连接到 **持久化** 数据库。
写入该连接的数据将被持久化，并且可以通过重新连接到同一文件从 Python 和其他 DuckDB 客户端重新加载。

```python
import duckdb

# 创建一个连接到名为 'file.db' 的文件
con = duckdb.connect("file.db")
# 创建表并加载数据
con.sql("CREATE TABLE test (i INTEGER)")
con.sql("INSERT INTO test VALUES (42)")
# 查询表
con.table("test").show()
# 显式关闭连接
con.close()
# 注意：当连接超出作用域时也会隐式关闭
```

您也可以使用上下文管理器来确保连接被关闭：

```python
import duckdb

with duckdb.connect("file.db") as con:
    con.sql("CREATE TABLE test (i INTEGER)")
    con.sql("INSERT INTO test VALUES (42)")
    con.table("test").show()
    # 上下文管理器会自动关闭连接
```

### 配置

`duckdb.connect()` 接受一个 `config` 字典，其中可以指定 [配置选项]({% link docs/stable/configuration/overview.md %}#configuration-reference)。例如：

```python
import duckdb

con = duckdb.connect(config = {'threads': 1})
```

### 连接对象和模块

连接对象和 `duckdb` 模块可以互换使用——它们支持相同的方法。唯一的区别是，当使用 `duckdb` 模块时，会使用一个全局的内存数据库。

> 如果您正在开发一个供他人使用的包，并在该包中使用 DuckDB，建议您创建连接对象，而不是使用 `duckdb` 模块的方法。这是因为 `duckdb` 模块使用的是共享的全局数据库——如果从多个不同的包中使用，可能会导致难以调试的问题。

### 在并行 Python 程序中使用连接

`DuckDBPyConnection` 对象不是线程安全的。如果您希望从多个线程写入同一个数据库，请使用 [`DuckDBPyConnection.cursor()` 方法]({% link docs/stable/clients/python/reference/index.md %}#duckdb.DuckDBPyConnection.cursor) 为每个线程创建一个游标。

## 加载和安装扩展

DuckDB 的 Python API 提供了安装和加载 [扩展]({% link docs/stable/core_extensions/overview.md %}) 的功能，这些功能等同于运行 `INSTALL` 和 `LOAD` SQL 命令。安装并加载 [`spatial` 扩展]({% link docs/stable/core_extensions/spatial/overview.md %}) 的示例如下：

```python
import duckdb

con = duckdb.connect()
con.install_extension("spatial")
con.load_extension("spatial")
```

### 社区扩展

要加载 [社区扩展]({% link community_extensions/index.md %})，请使用 `repository="community"` 参数调用 `install_extension` 方法。

例如，安装并加载 `h3` 社区扩展如下：

```python
import duckdb

con = duckdb.connect()
con.install_extension("h3", repository="community")
con.load_extension("h3")
```

### 未签名扩展

要加载 [未签名扩展]({% link docs/stable/core_extensions/overview.md %}#unsigned-extensions)，请使用 `config = {"allow_unsigned_extensions": "true"}` 参数调用 `duckdb.connect()` 方法。