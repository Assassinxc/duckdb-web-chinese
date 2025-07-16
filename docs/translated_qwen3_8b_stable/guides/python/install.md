---
---
layout: docu
redirect_from:
- /docs/guides/python/install
title: 安装 Python 客户端
---

## 通过 Pip 安装

可以使用 `pip` 安装 Python 客户端的最新版本。

```bash
pip install duckdb
```

可以使用 `--pre` 安装 Python 客户端的预发布版本。

```bash
pip install duckdb --upgrade --pre
```

## 从源代码安装

可以从 [DuckDB GitHub 仓库的 `tools/pythonpkg` 目录](https://github.com/duckdb/duckdb/tree/main/tools/pythonpkg) 从源代码安装最新的 Python 客户端。

```batch
BUILD_PYTHON=1 GEN=ninja make
cd tools/pythonpkg
python setup.py install
```

如需详细了解如何从源代码编译 DuckDB，请参阅 [构建指南]({% link docs/stable/dev/building/python.md %})。