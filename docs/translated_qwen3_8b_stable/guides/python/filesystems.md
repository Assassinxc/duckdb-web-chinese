---
---
layout: docu
redirect_from:
- /docs/guides/python/filesystems
title: 使用 fsspec 文件系统
---

DuckDB 对 [`fsspec`](https://filesystem-spec.readthedocs.io) 文件系统的支持，允许查询 DuckDB 的 [`httpfs` 扩展]({% link docs/stable/core_extensions/httpfs/overview.md %}) 不支持的文件系统。`fsspec` 具有大量的 [内置文件系统](https://filesystem-spec.readthedocs.io/en/latest/api.html#built-in-implementations)，并且也有许多 [外部实现](https://filesystem-spec.readthedocs.io/en/latest/api.html#other-known-implementations)。此功能仅在 DuckDB 的 Python 客户端中可用，因为 `fsspec` 是一个 Python 库，而 `httpfs` 扩展在许多 DuckDB 客户端中都可用。

## 示例

以下是一个使用 `fsspec` 查询 Google Cloud Storage 中文件（而不是使用其 S3 兼容 API）的示例。

首先，您必须安装 `duckdb`、`fsspec`，以及您选择的文件系统接口。

```bash
pip install duckdb fsspec gcsfs
```

然后，您可以注册您想要查询的任何文件系统：

```python
import duckdb
from fsspec import filesystem

# 如果未安装相应的文件系统接口，此行将引发异常
duckdb.register_filesystem(filesystem('gcs'))

duckdb.sql("SELECT * FROM read_csv('gcs:///bucket/file.csv')")
```

> 这些文件系统不是用 C++ 实现的，因此它们的性能可能无法与 `httpfs` 扩展提供的文件系统相媲美。
> 此外，还需注意，由于它们是第三方库，可能会包含我们无法控制的错误。