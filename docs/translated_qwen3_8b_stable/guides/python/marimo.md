---
---
layout: docu
title: marimo 笔记本
---

[marimo](https://github.com/marimo-team/marimo) 是一个开源的反应式 Python 和 SQL 笔记本，与 DuckDB 的 Python 客户端紧密集成，使你可以在单个 Git 可版本控制的笔记本中混合使用 Python 和 SQL。与传统笔记本不同，当你运行一个单元格或与 UI 元素交互时，marimo 会自动（或延迟）运行受影响的单元格，保持代码和输出的一致性。其与 DuckDB 的集成使其非常适合进行数据的交互式操作，而其作为 Python 文件的表示形式使你能够轻松地将笔记本作为脚本运行。

## 安装

开始之前，从终端安装 marimo 和 DuckDB：

```bash
pip install "marimo[sql]" # 或 uv add "marimo[sql]"
```

安装支持库：

```bash
pip install "polars[pyarrow]" # 或 uv add "polars[pyarrow]"
```

运行教程：

```bash
marimo tutorial sql
```

## 在 marimo 中使用 SQL

通过 `marimo edit notebook.py` 从终端创建一个笔记本。创建 SQL 单元格有三种方式：

1. 右键点击 **+** 按钮并选择 **SQL 单元格**
2. 通过单元格菜单将任何空单元格转换为 SQL
3. 点击笔记本底部的 SQL 按钮

<img src="/images/guides/marimo/marimo-sql-button.png"/>

在 marimo 中，SQL 单元格在显示上像是在编写 SQL，但通过 `mo.sql()` 函数将其序列化为标准的 Python 代码，这样你的笔记本保持为纯 Python 代码，而无需特殊语法或魔术命令。

```python
df = mo.sql(f"SELECT 'Off and flying!' AS a_duckdb_column")
```

这是因为 marimo 将笔记本存储为纯 Python 代码，[出于许多原因](https://marimo.io/blog/python-not-json)，例如 Git 友好的差异和将笔记本作为 Python 脚本运行。

SQL 语句本身是一个 f-string，允许你使用 `{}` 将 Python 值插值到查询中（后面会展示）。特别是，这意味着你的 SQL 查询可以依赖于 UI 元素或其他 Python 值的值，所有这些都是 marimo 数据流图的一部分。

> 警告 注意！
> 如果你的 SQL 查询中包含用户生成的内容，请确保对输入进行消毒以防止 SQL 注入。

## 连接自定义的 DuckDB 连接

要连接自定义的 DuckDB 连接而不是使用默认的全局连接，请创建一个单元格并创建一个 DuckDB 连接作为 Python 变量：

```python
import duckdb

# 创建 DuckDB 连接
conn = duckdb.connect("path/to/my/duckdb.db")
```

marimo 会自动发现该连接，并允许你在 SQL 单元格的连接下拉菜单中选择它。

<div align="center">
  <figure>
    <img src="/images/guides/marimo/marimo-custom-connection.png"/>
    <figcaption>自定义连接</figcaption>
  </figure>
</div>

## 数据库、模式和表的自动发现

marimo 会检查连接并在数据源面板中显示数据库、模式、表和列。此面板让你能够快速导航模式，将表和列拉入你的 SQL 查询中。

<div align="center">
  <figure>
    <img src="/images/guides/marimo/marimo-datasource-discovery.png"/>
    <figcaption>数据源面板</figcaption>
  </figure>
</div>

## 引用本地数据框

在 SQL 单元格中通过 Python 变量的名称引用本地数据框。如果你有一个数据库连接并包含同名的表，则会使用数据库表。

```python
import polars as pl
df = pl.DataFrame({"column": [1, 2, 3]})
```

```sql
SELECT * FROM df WHERE column > 2
```

## 引用 SQL 单元格的输出

在 SQL 单元格中定义一个非私有（非下划线）输出变量，允许你引用结果数据框在其他 Python 和 SQL 单元格中。

<div align="center">
  <figure>
    <img src="/images/guides/marimo/marimo-sql-result.png"/>
    <figcaption>在 Python 中引用 SQL 结果</figcaption>
  </figure>
</div>

## 反应式 SQL 单元格

marimo 允许你创建反应式 SQL 单元格，当其依赖项发生变化时会自动更新。**处理昂贵的查询或大型数据集？** 你可以配置 marimo 的运行时为“懒惰”模式。通过这样做，依赖单元格只会被标记为过时，让用户决定何时重新运行。

```python
digits = mo.ui.slider(label="Digits", start=100, stop=10000, step=200)
digits
```

```sql
CREATE TABLE random_data AS
    SELECT i AS id, random() AS random_value,
    FROM range({digits.value}) AS t(i);

SELECT * FROM random_data;
```

与 UI 元素（如滑块）的交互使你的数据更具可视化效果。

<div align="center">
  <img src="/images/guides/marimo/marimo-reactive-sql.gif"/>
</div>

## marimo 中的 DuckDB 驱动的 OLAP 分析

marimo 提供了与 DuckDB 一起使用的多个功能，适用于分析工作流：

* Python 与 SQL 之间无缝集成
* 反应式执行，当查询更改时自动更新依赖单元格
* 可用于参数化 SQL 查询的交互式 UI 元素
* 能够将笔记本导出为独立应用程序或 Python 脚本，甚至完全在浏览器中运行 [通过 WebAssembly](https://docs.marimo.io/guides/wasm/)。

## 下一步

* 阅读 [marimo 文档](https://docs.marimo.io/)。
* 尝试 SQL 教程：`marimo tutorial sql`。
* 本指南的代码 [可在 GitHub 上获取](https://github.com/marimo-team/marimo/blob/main/examples/sql/duckdb_example.py)。使用 `marimo edit ⟨github_url⟩` 运行它。