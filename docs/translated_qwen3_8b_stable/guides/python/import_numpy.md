---
---
layout: docu
redirect_from:
- /docs/guides/python/import_numpy
title: 从 Numpy 导入
---

可以从 DuckDB 查询 Numpy 数组。
无需手动注册数组 –
由于 [替换扫描]({% link docs/stable/guides/glossary.md %}#replacement-scan)，DuckDB 可以通过名称在 Python 进程中找到它们。
例如：

```python
import duckdb
import numpy as np

my_arr = np.array([(1, 9.0), (2, 8.0), (3, 7.0)])

duckdb.sql("SELECT * FROM my_arr")
```

```text
┌─────────┬─────────┬─────────┐
│ column0 │ column1 │ column2 │
│ double  │ double  │ double  │
├─────────┼─────────┼─────────┤
│     1.0 │     2.0 │     3.0 │
│     9.0 │     8.0 │     7.0 │
└─────────┴─────────┴─────────┘
```

## 参见

DuckDB 也支持 [导出到 Numpy]({% link docs/stable/guides/python/export_numpy.md %})。