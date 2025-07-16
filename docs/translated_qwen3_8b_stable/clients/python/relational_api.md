# DuckDB Python API 说明

## 操作

此部分包含用于创建和修改关系对象的操作。

| 名称 | 描述 |
|:--|:-------|
| [`aggregate`](#aggregate) | 聚合关系对象 |
| [`append`](#append) | 将关系对象附加到另一个关系对象 |
| [`as_arrow`](#as_arrow) | 将关系对象转换为 Arrow 表 |
| [`as_df`](#as_df) | 将关系对象转换为 pandas DataFrame |
| [`as_pl`](#as_pl) | 将关系对象转换为 Polars DataFrame |
| [`as_tensor`](#as_tensor) | 将关系对象转换为 TensorFlow 张量 |
| [`as_torch`](#as_torch) | 将关系对象转换为 PyTorch 张量 |
| [`as_vet`](#as_vet) | 将关系对象转换为 VET |
| [`collect`](#collect) | 收集关系对象 |
| [`create`](#create) | 创建一个新表 |
| [`create_view`](#create_view) | 创建一个视图 |
| [`delete`](#delete) | 从关系对象中删除指定列 |
| [`distinct`](#distinct) | 获取关系对象的唯一值 |
| [`drop`](#drop) | 从关系对象中删除指定列 |
| [`filter`](#filter) | 过滤关系对象 |
| [`from_arrow`](#from_arrow) | 从 Arrow 表创建关系对象 |
| [`from_df`](#from_df) | 从 pandas DataFrame 创建关系对象 |
| [`from_pl`](#from_pl) | 从 Polars DataFrame 创建关系对象 |
| [`from_tensor`](#from_tensor) | 从 TensorFlow 张量创建关系对象 |
| [`from_torch`](#from_torch) | 从 PyTorch 张量创建关系对象 |
| [`from_vet`](#from_vet) | 从 VET 创建关系对象 |
| [`head`](#head) | 获取关系对象的前几行 |
| [`join`](#join) | 将两个关系对象连接 |
| [`limit`](#limit) | 限制关系对象的行数 |
| [`mutate`](#mutate) | 修改关系对象的列 |
| [`order_by`](#order_by) | 按照指定列排序关系对象 |
| [`rename`](#rename) | 重命名关系对象的列 |
| [`select`](#select) | 选择关系对象的列 |
| [`set`](#set) | 设置关系对象的列 |
| [`show`](#show) | 显示关系对象的前几行 |
| [`sort`](#sort) | 按照指定列排序关系对象 |
| [`tail`](#tail) | 获取关系对象的最后几行 |
| [`union`](#union) | 将两个关系对象合并 |
| [`unique`](#unique) | 获取关系对象的唯一值 |

#### `aggregate`

##### 签名

```python
aggregate(self: duckdb.duckdb.DuckDBPyRelation) -> duckdb.duckdb.DuckDBPyRelation
```

##### 描述

聚合关系对象

##### 示例

```python
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

agg_rel = rel.aggregate()
```

##### 结果

```text
The relation object is aggregated.
```

#### `append`

##### 签名

```python
append(self: duckdb.duckdb.DuckDBPyRelation, other: duckdb.duckdb.DuckDBPyRelation) -> duckdb.duckdb.DuckDBPyRelation
```

##### 描述

将关系对象附加到另一个关系对象

##### 示例

```python
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

other_rel = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

new_rel = rel.append(other_rel)
```

##### 结果

```text
The relation object is appended with another relation object.
```

#### `as_arrow`

##### 签名

```python
as_arrow(self: duckdb.duckdb.DuckDBPyRelation) -> pyarrow.lib.Table
```

##### 描述

将关系对象转换为 Arrow 表

##### 示例

```python
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

pa_table = rel.as_arrow()
```

##### 结果

```text
The relation object is converted to an Arrow table.
```

#### `as_df`

##### 签名

```python
as_df(self: duckdb.duckdb.DuckDBPyRelation) -> pandas.DataFrame
```

##### 描述

将关系对象转换为 pandas DataFrame

##### 示例

```python
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

df = rel.as_df()
```

##### 结果

```text
The relation object is converted to a pandas DataFrame.
```

#### `as_pl`

##### 签名

```python
as_pl(self: duckdb.duckdb.DuckDBPyRelation) -> duckdb::PolarsDataFrame
```

##### 描述

将关系对象转换为 Polars DataFrame

##### 示例

```python
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

pl_df = rel.as_pl()
```

##### 结果

```text
The relation object is converted to a Polars DataFrame.
```

#### `as_tensor`

##### 签名

```python
as_tensor(self: duckdb.duckdb.DuckDBPyRelation) -> dict
```

##### 描述

将关系对象转换为 TensorFlow 张量

##### 示例

```python
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

tensor_dict = rel.as_tensor()
```

##### 结果

```text
The relation object is converted to a dictionary of TensorFlow tensors.
```

#### `as_torch`

##### 签名

```python
as_torch(self: duckdb.duckdb.DuckDBPyRelation) -> dict
```

##### 描述

将关系对象转换为 PyTorch 张量

##### 示例

```python
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

torch_dict = rel.as_torch()
```

##### 结果

```text
The relation object is converted to a dictionary of PyTorch tensors.
```

#### `as_vet`

##### 签名

```python
as_vet(self: duckdb.duckdb.DuckDBPyRelation) -> dict
```

##### 描述

将关系对象转换为 VET

##### 示例

```python
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

vet_dict = rel.as_vet()
```

##### 结果

```text
The relation object is converted to a dictionary of VETs.
```

#### `collect`

##### 签名

```python
collect(self: duckdb.duckdb.DuckDBPyRelation) -> duckdb.duckdb.DuckDBPyRelation
```

##### 描述

收集关系对象

##### 示例

```python
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

collected_rel = rel.collect()
```

##### 结果

```text
The relation object is collected.
```

#### `create`

##### 签名

```python
create(self: duckdb.duckdb.DuckDBPyRelation, table_name: str) -> None
```

##### 描述

创建一个新表

##### 示例

```python
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

rel.create("new_table")
```

##### 结果

```text
A new table named "new_table" is created with the contents of the relation object.
```

#### `create_view`

##### 签名

```python
create_view(self: duckdb.duckdb.DuckDBPyRelation, view_name: str, replace: bool = True) -> duckdb.duckdb.DuckDBPyRelation
```

##### 描述

创建一个视图

##### 示例

```python
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

rel.create_view("new_view", replace=True)
```

##### 结果

```text
A new view named "new_view" is created with the query definition of the relation object.
```

#### `delete`

##### 签名

```python
delete(self: duckdb.duckdb.DuckDBPyRelation, columns: list[str]) -> duckdb.duckdb.DuckDBPyRelation
```

##### 描述

从关系对象中删除指定列

##### 示例

```python
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

new_rel = rel.delete(["id", "created_timestamp"])
```

##### 结果

```text
The relation object has the specified columns deleted.
```

#### `distinct`

##### 签名

```python
distinct(self: duckdb.duckdb.DuckDBPyRelation) -> duckdb.duckdb.DuckDBPyRelation
```

##### 描述

获取关系对象的唯一值

##### 示例

```python
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created
        from range(1, 10)
    """
)

distinct_rel = rel.distinct()
```

##### 结果

```text
The relation object is filtered to contain only distinct values.
```

#### `drop`

##### 签名

```python
drop(self: duckdb.duckdb.DuckDBPyRelation, columns: list[str]) -> duckdb.duckdb.DuckDBPyRelation
```

##### 描述

从关系对象中删除指定列

##### 示例

```python
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

new_rel = rel.drop(["id", "created_timestamp"])
```

##### 结果

```text
The relation object has the specified columns deleted.
```

#### `filter`

##### 签名

```python
filter(self: duckdb.duckdb.DuckDBPyRelation, condition: str) -> duckdb.duckdb.DuckDBPyRelation
```

##### 描述

过滤关系对象

##### 示例

```python
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

filtered_rel = rel.filter("value > 5")
```

##### 结果

```text
The relation object is filtered to contain only rows where the value is greater than 5.
```

#### `from_arrow`

##### 签名

```python
from_arrow(self: duckdb.duckdb.DuckDBPyRelation, table: pyarrow.lib.Table) -> duckdb.duckdb.DuckDBPyRelation
```

##### 描述

从 Arrow 表创建关系对象

##### 示例

```python
import duckdb
import pyarrow as pa

duckdb_conn = duckdb.connect()

pa_table = pa.table({"id": ["1", "2"], "value": [1, 2]})

rel = duckdb.from_arrow(pa_table)
```

##### 结果

```text
A relation object is created from the Arrow table.
```

#### `from_df`

##### 签名

```python
from_df(self: duckdb.duckdb.DuckDBPyRelation, df: pandas.DataFrame) -> duckdb.duckdb.DuckDBPyRelation
```

##### 描述

从 pandas DataFrame 创建关系对象

##### 示例

```python
import duckdb
import pandas as pd

duckdb_conn = duckdb.connect()

df = pd.DataFrame({"id": ["1", "2"], "value": [1, 2]})

rel = duckdb.from_df(df)
```

##### 结果

```text
A relation object is created from the pandas DataFrame.
```

#### `from_pl`

##### 签名

```python
from_pl(self: duckdb.duckdb.DuckDBPyRelation, df: duckdb::PolarsDataFrame) -> duckdb.duckdb.DuckDBPyRelation
```

##### 描述

从 Polars DataFrame 创建关系对象

##### 示例

```python
import duckdb
import polars as pl

duckdb_conn = duckdb.connect()

df = pl.DataFrame({"id": ["1", "2"], "value": [1, 2]})

rel = duckdb.from_pl(df)
```

##### 结果

```text
A relation object is created from the Polars DataFrame.
```

#### `from_tensor`

##### 签名

```python
from_tensor(self: duckdb.duckdb.DuckDBPyRelation, tensor_dict: dict) -> duckdb.duckdb.DuckDBPyRelation
```

##### 描述

从 TensorFlow 张量创建关系对象

##### 示例

```python
import duckdb
import tensorflow as tf

duckdb_conn = duckdb.connect()

tensor_dict = {"id": tf.constant(["1", "2"]), "value": tf.constant([1, 2])}

rel = duckdb.from_tensor(tensor_dict)
```

##### 结果

```text
A relation object is created from the TensorFlow tensors.
```

#### `from_torch`

##### 签名

```python
from_torch(self: duckdb.duckdb.DuckDBPyRelation, tensor_dict: dict) -> duckdb.duckdb.DuckDBPyRelation
```

##### 描述

从 PyTorch 张量创建关系对象

##### 示例

```python
import duckdb
import torch

duckdb_conn = duckdb.connect()

tensor_dict = {"id": torch.tensor(["1", "2"]), "value": torch.tensor([1, 2])}

rel = duckdb.from_torch(tensor_dict)
```

##### 结果

```text
A relation object is created from the PyTorch tensors.
```

#### `from_vet`

##### 签名

```python
from_vet(self: duckdb.duckdb.DuckDBPyRelation, vet_dict: dict) -> duckdb.duckdb.DuckDBPyRelation
```

##### 描述

从 VET 创建关系对象

##### 示例

```python
import duckdb

duckdb_conn = duckdb.connect()

vet_dict = {"id": "1", "value": 1}

rel = duckdb.from_vet(vet_dict)
```

##### 结果

```text
A relation object is created from the VET.
```

#### `head`

##### 签名

```python
head(self: duckdb.duckdb.DuckDBPyRelation, n: int = 5) -> duckdb.duckdb.DuckDBPyRelation
```

##### 描述

获取关系对象的前几行

##### 示例

```python
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

head_rel = rel.head(3)
```

##### 结果

```text
The relation object is limited to the first 3 rows.
```

#### `join`

##### 签名

```python
join(self: duckdb.duckdb.DuckDBPyRelation, other: duckdb.duckdb.DuckDBPyRelation, on: list[str]) -> duckdb.duckdb.DuckDBPyRelation
```

##### 描述

将两个关系对象连接

##### 示例

```python
import duckdb

duckdb_conn = duckdb.connect()

rel1 = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

rel2 = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

joined_rel = rel1.join(rel2, on=["id", "description"])
```

##### 结果

```text
The two relation objects are joined on the specified columns.
```

#### `limit`

##### 签名

```python
limit(self: duckdb.duckdb.DuckDBPyRelation, n: int) -> duckdb.duckdb.DuckDBPyRelation
```

##### 描述

限制关系对象的行数

##### 示例

```python
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

limited_rel = rel.limit(3)
```

##### 结果

```text
The relation object is limited to the first 3 rows.
```

#### `mutate`

##### 签名

```python
mutate(self: duckdb.duckdb.DuckDBPyRelation, new_columns: dict) -> duckdb.duckdb.DuckDBPyRelation
```

##### 描述

修改关系对象的列

##### 示例

```python
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

new_rel = rel.mutate({"new_column": "value * 2"})
```

##### 结果

```text
The relation object has a new column added.
```

#### `order_by`

##### 签名

```python
order_by(self: duckdb.duckdb.DuckDBPyRelation, columns: list[str]) -> duckdb.duckdb.DuckDBPyRelation
```

##### 描述

按照指定列排序关系对象

##### 示例

```python
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

ordered_rel = rel.order_by(["value", "description"])
```

##### 结果

```text
The relation object is sorted by the specified columns.
```

#### `rename`

##### 签名

```python
rename(self: duckdb.duckdb.DuckDBPyRelation, columns: dict) -> duckdb.duckdb.DuckDBPyRelation
```

##### 描述

重命名关系对象的列

##### 示例

```python
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

renamed_rel = rel.rename({"id": "new_id", "description": "new_description"})
```

##### 结果

```text
The relation object has its columns renamed.
```

#### `select`

##### 签名

```python
select(self: duckdb.duckdb.DuckDBPyRelation, columns: list[str]) -> duckdb.duckdb.DuckDBPyRelation
```

##### 描述

选择关系对象的列

##### 示例

```python
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

selected_rel = rel.select(["id", "value"])
```

##### 结果

```text
The relation object is filtered to contain only the specified columns.
```

#### `set`

##### 签名

```python
set(self: duckdb.duckdb.DuckDBPyRelation, columns: dict) -> duckdb.duckdb.DuckDBPyRelation
```

##### 描述

设置关系对象的列

##### 示例

```python
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

set_rel = rel.set({"new_column": "value * 2"})
```

##### 结果

```text
The relation object has a new column added.
```

#### `show`

##### 签名

```python
show(self: duckdb.duckdb.DuckDBPyRelation, n: int = 5) -> duckdb.duckdb.DuckDBPyRelation
```

##### 描述

显示关系对象的前几行

##### 示例

```python
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

show_rel = rel.show(3)
```

##### 结果

```text
The relation object is displayed with the first 3 rows.
```

#### `sort`

##### 签名

```python
sort(self: duckdb.duckdb.DuckDBPyRelation, columns: list[str]) -> duckdb.duckdb.DuckDBPyRelation
```

##### 描述

按照指定列排序关系对象

##### 示例

```python
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

sorted_rel = rel.sort(["value", "description"])
```

##### 结果

```text
The relation object is sorted by the specified columns.
```

#### `tail`

##### 签名

```python
tail(self: duckdb.duckdb.DuckDBPyRelation, n: int = 5) -> duckdb.duckdb.DuckDBPyRelation
```

##### 描述

获取关系对象的最后几行

##### 示例

```python
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

tail_rel = rel.tail(3)
```

##### 结果

```text
The relation object is displayed with the last 3 rows.
```

#### `union`

##### 签名

```python
union(self: duckdb.duckdb.DuckDBPyRelation, other: duckdb.duckdb.DuckDBPyRelation) -> duckdb.duckdb.DuckDBPyRelation
```

##### 描述

将两个关系对象合并

##### 示例

```python
import duckdb

duckdb_conn = duckdb.connect()

rel1 = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

rel2 = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

union_rel = rel1.union(rel2)
```

##### 结果

```text
The two relation objects are merged.
```

#### `unique`

##### 签名

```python
unique(self: duckdb.duckdb.DuckDBPyRelation) -> duckdb.duckdb.DuckDBPyRelation
```

##### 描述

获取关系对象的唯一值

##### 示例

```python
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

unique_rel = rel.unique()
```

##### 结果

```text
The relation object is filtered to contain only distinct values.
```

## 函数

此部分包含用于执行 SQL 查询并获取数据的函数。

| 名称 | 描述 |
|:--|:-------|
| [`arrow`](#arrow) | 执行并获取所有行作为 Arrow 表 |
| [`close`](#close) | 关闭结果 |
| [`create`](#create) | 创建一个新表 |
| [`create_view`](#create_view) | 创建一个视图 |
| [`df`](#df) | 执行并获取所有行作为 pandas DataFrame |
| [`execute`](#execute) | 将关系对象转换为结果集 |
| [`fetch_arrow_reader`](#fetch_arrow_reader) | 执行并返回一个 Arrow Record Batch Reader |
| [`fetch_arrow_table`](#fetch_arrow_table) | 执行并获取所有行作为 Arrow 表 |
| [`fetch_df_chunk`](#fetch_df_chunk) | 执行并获取一个数据块 |
| [`fetchall`](#fetchall) | 执行并获取所有行作为元组列表 |
| [`fetchdf`](#fetchdf) | 执行并获取所有行作为 pandas DataFrame |
| [`fetchmany`](#fetchmany) | 执行并获取下一批行 |
| [`fetchnumpy`](#fetchnumpy) | 执行并获取所有行作为 numpy 数组 |
| [`fetchone`](#fetchone) | 执行并获取一行作为元组 |
| [`pl`](#pl) | 执行并获取所有行作为 Polars DataFrame |
| [`record_batch`](#record_batch) | 执行并返回一个 Arrow Record Batch Reader |
| [`tf`](#tf) | 获取结果作为 TensorFlow 张量 |
| [`to_arrow_table`](#to_arrow_table) | 执行并获取所有行作为 Arrow 表 |
| [`to_csv`](#to_csv) | 将关系对象写入 CSV 文件 |
| [`to_df`](#to_df) | 执行并获取所有行作为 pandas DataFrame |
| [`to_parquet`](#to_parquet) | 将关系对象写入 Parquet 文件 |
| [`to_table`](#to_table) | 创建一个新表 |
| [`to_view`](#to_view) | 创建一个视图 |
| [`torch`](#torch) | 获取结果作为 PyTorch 张量 |
| [`write_csv`](#write_csv) | 将关系对象写入 CSV 文件 |
| [`write_parquet`](#write_parquet) | 将关系对象写入 Parquet 文件 |

#### `arrow`

##### 签名

```python
arrow(self: duckdb.duckdb.DuckDBPyRelation, batch_size: int = 1000000) -> pyarrow.lib.Table
```

##### 描述

执行并获取所有行作为 Arrow 表

##### 示例

```python
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

pa_table = rel.arrow()
```

##### 结果

```text
The relation object is converted to an Arrow table.
```

#### `close`

##### 签名

```python
close(self: duckdb.duckdb.DuckDBPyRelation) -> None
```

##### 描述

关闭结果

#### `create`

##### 签名

```python
create(self: duckdb.duckdb.DuckDBPyRelation, table_name: str) -> None
```

##### 描述

创建一个新表

##### 示例

```python
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

rel.create("new_table")
```

##### 结果

```text
A new table named "new_table" is created with the contents of the relation object.
```

#### `create_view`

##### 签名

```python
create_view(self: duckdb.duckdb.DuckDBPyRelation, view_name: str, replace: bool = True) -> duckdb.duckdb.DuckDBPyRelation
```

##### 描述

创建一个视图

##### 示例

```python
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

rel.create_view("new_view", replace=True)
```

##### 结果

```text
A new view named "new_view" is created with the query definition of the relation object.
```

#### `df`

##### 签名

```python
df(self: duckdb.duckdb.DuckDBPyRelation, *, date_as_object: bool = False) -> pandas.DataFrame
```

##### 描述

执行并获取所有行作为 pandas DataFrame

##### 示例

```python
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

df = rel.df()
```

##### 结果

```text
The relation object is converted to a pandas DataFrame.
```

#### `execute`

##### 签名

```python
execute(self: duckdb.duckdb.DuckDBPyRelation) -> duckdb.duckdb.DuckDBPy
```

##### 描述

将关系对象转换为结果集

#### `fetch_arrow_reader`

##### 签名

```python
fetch_arrow_reader(self: duckdb.duckdb.DuckDBPyRelation, batch_size: int = 1000000) -> pyarrow.lib.RecordBatchReader
```

##### 描述

执行并返回一个 Arrow Record Batch Reader

#### `fetch_arrow_table`

##### 签名

```python
fetch_arrow_table(self: duckdb.duckdb.DuckDBPyRelation, batch_size: int = 1000000) -> pyarrow.lib.Table
```

##### 描述

执行并获取所有行作为 Arrow 表

#### `fetch_df_chunk`

##### 签名

```python
fetch_df_chunk(self: duckdb.duckdb.DuckDBPyRelation, vectors_per_chunk: int = 1, *, date_as_object: bool = False) -> pandas.DataFrame
```

##### 描述

执行并获取一个数据块

#### `fetchall`

##### 签名

```python
fetchall(self: duckdb.duckdb.DuckDBPyRelation) -> list
```

##### 描述

执行并获取所有行作为元组列表

#### `fetchdf`

##### 签名

```python
fetchdf(self: duckdb.duckdb.DuckDBPyRelation, *, date_as_object: bool = False) -> pandas.DataFrame
```

##### 描述

执行并获取所有行作为 pandas DataFrame

#### `fetchmany`

##### 签名

```python
fetchmany(self: duckdb.duckdb.DuckDBPyRelation, size: int = 1) -> list
```

##### 描述

执行并获取下一批行

#### `fetchnumpy`

##### 签名

```python
fetchnumpy(self: duckdb.duckdb.DuckDBPyRelation) -> dict
```

##### 描述

执行并获取所有行作为 numpy 数组

#### `fetchone`

##### 签名

```python
fetchone(self: duckdb.duckdb.DuckDBPyRelation) -> typing.Optional[tuple]
```

##### 描述

执行并获取一行作为元组

#### `pl`

##### 签名

```python
pl(self: duckdb.duckdb.DuckDBPyRelation, batch_size: int = 1000000) -> duckdb::PolarsDataFrame
```

##### 描述

执行并获取所有行作为 Polars DataFrame

#### `record_batch`

##### 签名

```python
record_batch(self: duckdb.duckdb.DuckDBPyRelation, batch_size: int = 1000000) -> pyarrow.lib.RecordBatchReader
```

##### 描述

执行并返回一个 Arrow Record Batch Reader

#### `tf`

##### 签名

```python
tf(self: duckdb.duckdb.DuckDBPyRelation) -> dict
```

##### 描述

获取结果作为 TensorFlow 张量

#### `to_arrow_table`

##### 签名

```python
to_arrow_table(self: duckdb.duckdb.DuckDBPyRelation, batch_size: int = 1000000) -> pyarrow.lib.Table
```

##### 描述

执行并获取所有行作为 Arrow 表

#### `to_csv`

##### 签名

```python
to_csv(self: duckdb.duckdb.DuckDBPyRelation, file_name: str, *, sep: object = None, na_rep: object = None, header: object = None, quotechar: object = None, escapechar: object = None, date_format: object = None, timestamp_format: object = None, quoting: object = None, encoding: object = None, compression: object = None, overwrite: object = None, per_thread_output: object = None, use_tmp_file: object = None, partition_by: object = None, write_partition_columns: object = None) -> None
```

##### 描述

将关系对象写入 CSV 文件

#### `to_df`

##### 签名

```python
to_df(self: duckdb.duckdb.DuckDBPyRelation, *, date_as_object: bool = False) -> pandas.DataFrame
```

##### 描述

执行并获取所有行作为 pandas DataFrame

#### `to_parquet`

##### 签名

```python
to_parquet(self: duckdb.duckdb.DuckDBPyRelation, file_name: str, *, compression: object = None, field_ids: object = None, row_group_size_bytes: object = None, row_group_size: object = None, overwrite: object = None, per_thread_output: object = None, use_tmp_file: object = None, partition_by: object = None, write_partition_columns: object = None, append: object = None) -> None
```

##### 描述

将关系对象写入 Parquet 文件

#### `to_table`

##### 签名

```python
to_table(self: duckdb.duckdb.DuckDBPyRelation, table_name: str) -> None
```

##### 描述

创建一个新表

#### `to_view`

##### 签名

```python
to_view(self: duckdb.duckdb.DuckDBPyRelation, view_name: str, replace: bool = True) -> duckdb.duckdb.DuckDBPyRelation
```

##### 描述

创建一个视图

#### `torch`

##### 签名

```python
torch(self: duckdb.duckdb.DuckDBPyRelation) -> dict
```

##### 描述

获取结果作为 PyTorch 张量

#### `write_csv`

##### 签名

```python
write_csv(self: duckdb.duckdb.DuckDBPyRelation, file_name: str, *, sep: object = None, na_rep: object = None, header: object = None, quotechar: object = None, escapechar: object = None, date_format: object = None, timestamp_format: object = None, quoting: object = None, encoding: object = None, compression: object = None, overwrite: object = None, per_thread_output: object = None, use_tmp_file: object = None, partition_by: object = None, write_partition_columns: object = None) -> None
```

##### 描述

将关系对象写入 CSV 文件

#### `write_parquet`

##### 签名

```python
write_parquet(self: duckdb.duckdb.DuckDBPyRelation, file_name: str, *, compression: object = None, field_ids: object = None, row_group_size_bytes: object = None, row_group_size: object = None, overwrite: object = None, per_thread_output: object = None, use_tmp_file: object = None, partition_by: object = None, write_partition_columns: object = None, append: object = None) -> None
```

##### 描述

将关系对象写入 Parquet 文件