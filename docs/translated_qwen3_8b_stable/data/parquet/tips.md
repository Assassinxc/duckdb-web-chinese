---
---
layout: docu
redirect_from:
- /docs/data/parquet/tips
title: Parquet 提示
---

以下是一些在处理 Parquet 文件时的提示。

## 读取 Parquet 文件的提示

### 使用 `union_by_name` 读取具有不同模式的文件

`union_by_name` 选项可以用于统一具有不同或缺失列的文件的模式。对于缺少某些列的文件，会用 `NULL` 值填充：

```sql
SELECT *
FROM read_parquet('flights*.parquet', union_by_name = true);
```

## 写入 Parquet 文件的提示

使用 [glob 模式]({% link docs/stable/data/multiple_files/overview.md %}#glob-syntax) 或 [Hive 分区]({% link docs/stable/data/partitioning/hive_partitioning.md %}) 结构是透明处理多个文件的好方法。

### 启用 `PER_THREAD_OUTPUT`

如果最终 Parquet 文件的数量并不重要，按线程写入单个文件可以显著提高性能：

```sql
COPY
    (FROM generate_series(10_000_000))
    TO 'test.parquet'
    (FORMAT parquet, PER_THREAD_OUTPUT);
```

### 选择 `ROW_GROUP_SIZE`

`ROW_GROUP_SIZE` 参数指定 Parquet 行组的最小行数，最小值等于 DuckDB 的向量大小 2,048，默认值为 122,880。
Parquet 行组是行的分区，包含数据集中每个列的列块。

压缩算法仅在行组级别应用，因此行组越大，压缩数据的机会越多。
DuckDB 即使在同一个文件中也可以并行读取 Parquet 行组，并使用谓词下推只扫描与查询 `WHERE` 子句匹配的行组元数据。
不过，读取每个组的元数据会有一些开销。
一种好的方法是确保每个文件中的行组总数至少等于查询该文件所使用的 CPU 线程数。
超过线程数的行组会提高高度选择性查询的速度，但会降低必须扫描整个文件的查询（如聚合）的速度。

要写入具有不同行组大小的 Parquet 文件，请运行：

```sql
COPY
    (FROM generate_series(100_000))
    TO 'row-groups.parquet'
    (FORMAT parquet, ROW_GROUP_SIZE 100_000);
```

### `ROW_GROUPS_PER_FILE` 选项

`ROW_GROUPS_PER_FILE` 参数会在当前文件达到指定的行组数时创建一个新的 Parquet 文件。

```sql
COPY
    (FROM generate_series(100_000))
    TO 'output-directory'
    (FORMAT parquet, ROW_GROUP_SIZE 20_000, ROW_GROUPS_PER_FILE 2);
```

> 如果有多个线程正在运行，文件中的行组数可能会略微超过指定的行组数，以限制锁的使用量——类似于 [`FILE_SIZE_BYTES`](../../sql/statements/copy#copy--to-options) 的行为。
> 然而，如果设置了 `PER_THREAD_OUTPUT`，每个文件只由一个线程写入，因此会变得准确。

有关更多提示，请参阅 [“文件格式”性能指南]({% link docs/stable/guides/performance/file_formats.md %}#parquet-file-sizes)。