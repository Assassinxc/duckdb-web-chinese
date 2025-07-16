---
---
layout: docu
redirect_from:
- /docs/guides/python/export_numpy
title: 导出为 Numpy
---

可以使用 `fetchnumpy()` 函数将查询结果转换为 Numpy 数组。例如：

```python
import duckdb
import numpy as np

my_arr = duckdb.sql("SELECT unnest([1, 2, 3]) AS x, 5.0 AS y").fetchnumpy()
my_arr
```

```text
{'x': array([1, 2, 3], dtype=int32), 'y': masked_array(data=[5.0, 5.0, 5.0],
             mask=[False, False, False],
       fill_value=1e+20)}
```

然后，可以使用 Numpy 函数对数组进行处理，例如：

```python
np.sum(my_arr['x'])
```

```text
6
```

## 参见

DuckDB 还支持 [从 Numpy 导入]({% link docs/stable/guides/python/import_numpy.md %})。