---
---
layout: docu
redirect_from:
- /docs/guides/python/jupyter
title: Jupyter Notebooks
---

DuckDB 的 Python 客户端可以在不进行任何额外配置的情况下直接用于 Jupyter 笔记本。
然而，可以使用额外的库来简化 SQL 查询开发。
本指南将介绍如何利用这些额外的库。
查看 Python 部分的其他指南，了解如何使用 DuckDB 和 Python 一起。

在此示例中，我们使用 [JupySQL](https://github.com/ploomber/jupysql) 包。此示例工作流也作为 [Google Colab 笔记本](https://colab.research.google.com/drive/1bNfU8xRTu8MQJnCbyyDRxvptklLb0ExH?usp=sharing) 提供。

## 库安装

四个额外的库可以改善 Jupyter 笔记本中使用 DuckDB 的体验。

1. [jupysql](https://github.com/ploomber/jupysql): 将 Jupyter 代码单元格转换为 SQL 单元格
2. [Pandas](https://github.com/pandas-dev/pandas): 清洁表格可视化和与其他分析工具的兼容性
3. [matplotlib](https://github.com/matplotlib/matplotlib): 使用 Python 进行绘图
4. [duckdb-engine (DuckDB SQLAlchemy 驱动)](https://github.com/Mause/duckdb_engine): SQLAlchemy 用于连接 DuckDB（可选）

如果 Jupyter Notebook 尚未安装，请从命令行运行这些 `pip install` 命令。否则，请参阅上方的 Google Colab 链接以获取笔记本内的示例：

```bash
pip install duckdb
```

安装 Jupyter Notebook

```bash
pip install notebook
```

或者 JupyterLab：

```bash
pip install jupyterlab
```

安装支持库：

```bash
pip install jupysql pandas matplotlib duckdb-engine
```

## 库导入和配置

打开 Jupyter Notebook 并导入相关库。

在 jupysql 中设置配置，以直接将数据输出到 Pandas 并简化输出到笔记本的内容。

```python
%config SqlMagic.autopandas = True
%config SqlMagic.feedback = False
%config SqlMagic.displaycon = False
```

### 原生连接 DuckDB

要连接到 DuckDB，请运行：

```python
import duckdb
import pandas as pd

%load_ext sql
conn = duckdb.connect()
%sql conn --alias duckdb
```

> 警告 [变量]({% link docs/stable/sql/statements/set_variable.md %}) 在原生 DuckDB 连接中不被识别。

### 通过 SQLAlchemy 连接 DuckDB

或者，您可以使用 `duckdb_engine` 通过 SQLAlchemy 连接到 DuckDB。请参阅 [性能和功能差异](https://jupysql.ploomber.io/en/latest/tutorials/duckdb-native-sqlalchemy.html)。

```python
import duckdb
import pandas as pd
# 不需要导入 duckdb_engine
# jupysql 将根据连接字符串自动检测所需的驱动！

# 导入 jupysql Jupyter 扩展以创建 SQL 单元格
%load_ext sql
```
可以连接到一个新的 [内存 DuckDB]({% link docs/stable/clients/python/dbapi.md %}#in-memory-connection)，[默认连接]({% link docs/stable/clients/python/dbapi.md %}#default-connection) 或文件数据库：

```sql
%sql duckdb:///:memory:
```

```sql
%sql duckdb:///:default:
```

```sql
%sql duckdb:///path/to/file.db
```

> 如果您提供 `duckdb:///:default:` 作为 SQLAlchemy 连接字符串，`%sql` 命令和 `duckdb.sql` 将共享相同的 [默认连接]({% link docs/stable/clients/python/dbapi.md %}).

## 查询 DuckDB

可以使用 `%sql` 在行首运行单行 SQL 查询。查询结果将显示为 Pandas DataFrame。

```sql
%sql SELECT 'Off and flying!' AS a_duckdb_column;
```

可以通过在单元格开头放置 `%%sql` 将整个 Jupyter 单元格用作 SQL 单元格。查询结果将显示为 Pandas DataFrame。

```sql
%%sql
SELECT
    schema_name,
    function_name
FROM duckdb_functions()
ORDER BY ALL DESC
LIMIT 5;
```

要将查询结果存储在 Python 变量中，请使用 `<<` 作为赋值运算符。
这可以与 `%sql` 和 `%%sql` Jupyter 魔法一起使用。

```sql
%sql res << SELECT 'Off and flying!' AS a_duckdb_column;
```

如果设置了 `%config SqlMagic.autopandas = True` 选项，则变量是一个 Pandas DataFrame，否则它是一个 `ResultSet`，可以通过 `DataFrame()` 函数转换为 Pandas。

## 查询 Pandas 数据框

DuckDB 可以找到并查询 Jupyter 笔记本中存储为变量的任何数据框。

```python
input_df = pd.DataFrame.from_dict({"i": [1, 2, 3],
                                   "j": ["one", "two", "three"]})
```

在 `FROM` 子句中，查询的数据框可以像其他表一样指定。

```sql
%sql output_df << SELECT sum(i) AS total_i FROM input_df;
```
> 警告 当使用 SQLAlchemy 连接，并且 DuckDB >= 1.1.0 时，请确保运行 `%sql SET python_scan_all_frames=true`，以使 Pandas 数据框可查询。

## 可视化 DuckDB 数据

在 Python 中绘制数据集最常见的方法是使用 Pandas 加载数据，然后使用 matplotlib 或 seaborn 进行绘图。
这种方法需要将所有数据加载到内存中，效率非常低。
JupySQL 的绘图模块在 SQL 引擎中运行计算。
这将内存管理委托给引擎，并确保中间计算不会占用过多内存，从而高效地绘制大规模数据集。

### 箱线图 & 直方图

要创建箱线图，请调用 `%sqlplot boxplot`，并传递要绘制的表名和列名。
在此情况下，表名是本地存储的 Parquet 文件的路径。

```python
from urllib.request import urlretrieve

_ = urlretrieve(
    "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet",
    "yellow_tripdata_2021-01.parquet",
)

%sqlplot boxplot --table yellow_tripdata_2021-01.parquet --column trip_distance
```

![trip_distance 列的箱线图](/images/trip-distance-boxplot.png)

### 安装和加载 DuckDB httpfs 扩展

DuckDB 的 [httpfs 扩展]({% link docs/stable/core_extensions/httpfs/overview.md %}) 允许通过 http 远程查询 Parquet 和 CSV 文件。
这些示例查询了一个包含纽约市历史出租车数据的 Parquet 文件。
使用 Parquet 格式可以让 DuckDB 只加载所需的行和列到内存，而不是下载整个文件。
DuckDB 还可以处理本地 [Parquet 文件]({% link docs/stable/data/parquet/overview.md %)}，这可能在查询整个 Parquet 文件或运行需要文件大量子集的多个查询时是有利的。

```sql
%%sql
INSTALL httpfs;
LOAD httpfs;
```

现在，创建一个按第 90 百分位数过滤的查询。
注意使用 `--save` 和 `--no-execute` 函数。
这告诉 JupySQL 存储查询，但跳过执行。它将在下一次绘图调用中被引用。

```sql
%%sql --save short_trips --no-execute
SELECT *
FROM 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet'
WHERE trip_distance < 6.3
```

要创建直方图，请调用 `%sqlplot histogram` 并传递表名、要绘制的列名和桶数。
这使用 `--with short-trips`，因此 JupySQL 使用之前定义的查询，因此只绘制数据的子集。

```python
%sqlplot histogram --table short_trips --column trip_distance --bins 10 --with short_trips
```

![trip_distance 列的直方图](/images/trip-distance-histogram.png)

## 总结

现在，您可以通过简单且高效的方式在 SQL 和 Pandas 之间切换！您可以直接通过引擎绘制大规模数据集（避免下载整个文件和将所有数据加载到内存中的 Pandas）。数据框可以作为 SQL 中的表读取，SQL 结果可以输出到数据框。祝您分析愉快！

`jupysql` 的替代方案是 [`magic_duckdb`](https://github.com/iqmo-org/magic_duckdb)。