---
---
layout: docu
redirect_from:
- /docs/api/python/known_issues
- /docs/api/python/known_issues/
- /docs/clients/python/known_issues
title: 已知的 Python 问题
---

## 故障排除

### 运行 `EXPLAIN` 会生成换行符

在 Python 中，[`EXPLAIN` 语句]({% link docs/stable/guides/meta/explain.md %}) 的输出包含硬换行符 (`\n`)：

```python
In [1]: import duckdb
   ...: duckdb.sql("EXPLAIN SELECT 42 AS x")
```

```text
Out[1]:
┌───────────────┬───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  explain_key  │                                                   explain_value                                                   │
│    varchar    │                                                      varchar                                                      │
├───────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ physical_plan │ ┌───────────────────────────┐\n│         PROJECTION        │\n│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │\n│             x   …  │
└───────────────┴───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

为了解决这个问题，可以打印 `explain()` 函数的输出：

```python
In [2]: print(duckdb.sql("SELECT 42 AS x").explain())
```

```text
Out[2]:
┌───────────────────────────┐
│         PROJECTION        │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│             x             │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         DUMMY_SCAN        │
└───────────────────────────┘
```

请查看 [Jupyter 指南]({% link docs/stable/guides/python/jupyter.md %}) 以获取在 Jupyter 中使用 JupySQL 的技巧。

### Windows 上的崩溃和错误

在 Windows 上导入 DuckDB 时，Python 运行时可能在导入或首次使用时崩溃或返回错误：

```python
import duckdb

duckdb.sql("...")
```

```console
ImportError: DLL load failed while importing duckdb: The specified module could not be found.
```

```console
Windows fatal exception: access violation

Current thread 0x0000311c (most recent call first):
  File "<stdin>", line 1 in <module>
```

```console
Process finished with exit code -1073741819 (0xC0000005)
```

这个问题很可能是由于使用了过时的 Microsoft Visual C++ (MSVC) 分发包导致的。解决方法是安装 [最新 MSVC 分发包](https://learn.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist)。或者，您可以指示 `pip` 从源代码编译包，如下所示：

```bash
python3 -m pip install duckdb --no-binary duckdb
```

## 已知问题

不幸的是，有些问题要么超出我们的控制范围，要么非常难以追踪。根据您的工作流程，您可能需要了解以下这些问题：

### Numpy 导入多线程

当使用多线程并从 Numpy 数组或通过 Pandas DataFrame 间接获取结果时，可能需要确保 `numpy.core.multiarray` 被导入。如果此模块未从主线程导入，而在执行过程中其他线程尝试导入它，会导致死锁或崩溃。

为了避免这个问题，建议在启动线程之前导入 `numpy.core.multiarray`。

## `DESCRIBE` 和 `SUMMARIZE` 在 Jupyter 中返回空表

`DESCRIBE` 和 `SUMMARIZE` 语句返回空表：

```python
%sql
CREATE OR REPLACE TABLE tbl AS (SELECT 42 AS x);
DESCRIBE tbl;
```

为了解决这个问题，可以将它们包装成子查询：

```python
%sql
CREATE OR REPLACE TABLE tbl AS (SELECT 42 AS x);
FROM (DESCRIBE tbl);
```

### IPython 中 JupySQL 的 Protobuf 错误

在 IPython 中加载 JupySQL 扩展会失败：

```python
In [1]: %load_ext sql
```

```console
ImportError: cannot import name 'builder' from 'google.protobuf.internal' (unknown location)
```

解决方法是修复 `protobuf` 包。这可能需要卸载冲突的包，例如：

```python
%pip uninstall tensorflow
%pip install protobuf
```