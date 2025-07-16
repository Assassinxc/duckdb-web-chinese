---
---
layout: docu
redirect_from:
- /docs/guides/python/polars
title: 与 Polars 的集成
---

[Polars](https://github.com/pola-rs/polars) 是一个用 Rust 编写的 DataFrames 库，支持 Python 和 Node.js 的绑定。它使用 [Apache Arrow 的列式格式](https://arrow.apache.org/docs/format/Columnar.html) 作为其内存模型。DuckDB 可以读取 Polars DataFrames 并将查询结果转换为 Polars DataFrames。它通过内部的高效 Apache Arrow 集成实现此功能。请注意，为了使集成正常工作，必须安装 `pyarrow` 库。

## 安装

```bash
pip install -U duckdb 'polars[pyarrow]'
```

## Polars 到 DuckDB

DuckDB 可以通过引用当前作用域中 Polars DataFrames 的名称，原生地查询 Polars DataFrames。

```python
import duckdb
import polars as pl

df = pl.DataFrame(
    {
        "A": [1, 2, 3, 4, 5],
        "fruits": ["banana", "banana", "apple", "apple", "banana"],
        "B": [5, 4, 3, 2, 1],
        "cars": ["beetle", "audi", "beetle", "beetle", "beetle"],
    }
)
duckdb.sql("SELECT * FROM df").show()
```

## DuckDB 到 Polars

DuckDB 可以使用 `.pl()` 结果转换方法将结果输出为 Polars DataFrames。

```python
df = duckdb.sql("""
    SELECT 1 AS id, 'banana' AS fruit
    UNION ALL
    SELECT 2, 'apple'
    UNION ALL
    SELECT 3, 'mango'"""
).pl()
print(df)
```

```text
shape: (3, 2)
┌─────┬────────┐
│ id  ┆ fruit  │
│ --- ┆ ---    │
│ i32 ┆ str    │
╞═════╪════════╡
│ 1   ┆ banana │
│ 2   ┆ apple  │
│ 3   ┆ mango  │
└─────┴────────┘
```

如需了解更多关于 Polars 的信息，可以访问他们的 [Python API 参考文档](https://pola-rs.github.io/polars/py-polars/html/reference/index.html)。