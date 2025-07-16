---
---
layout: docu
redirect_from:
- /docs/data/partitioning/partitioned_writes
title: 分区写入
---

## 示例

将表写入 Parquet 文件的 Hive 分区数据集：

```sql
COPY orders TO 'orders'
(FORMAT parquet, PARTITION_BY (year, month));
```

将表写入 CSV 文件的 Hive 分区数据集，并允许覆盖：

```sql
COPY orders TO 'orders'
(FORMAT csv, PARTITION_BY (year, month), OVERWRITE_OR_IGNORE);
```

将表写入 GZIP 压缩的 CSV 文件的 Hive 分区数据集，并设置数据文件的显式扩展名：

```sql
COPY orders TO 'orders'
(FORMAT csv, PARTITION_BY (year, month), COMPRESSION gzip, FILE_EXTENSION 'csv.gz');
```

## 分区写入

当在 [`COPY` 语句]({% link docs/stable/sql/statements/copy.md %}) 中指定了 `PARTITION_BY` 子句时，文件将按照 [Hive 分区]({% link docs/stable/data/partitioning/hive_partitioning.md %}) 的文件夹结构进行写入。目标目录是根目录的名称（在上面的例子中为 `orders`）。文件按照文件夹结构顺序写入。目前，每个线程会向每个目录写入一个文件。

```text
orders
├── year=2021
│    ├── month=1
│    │   ├── data_1.parquet
│    │   └── data_2.parquet
│    └── month=2
│        └── data_1.parquet
└── year=2022
     ├── month=11
     │   ├── data_1.parquet
     │   └── data_2.parquet
     └── month=12
         └── data_1.parquet
```

分区的值会自动从数据中提取。请注意，写入大量分区可能会非常耗时，因为会创建很多文件。理想的分区数量取决于你的数据集的大小。

为了限制系统在使用 `PARTITION_BY` 写入时在刷新到磁盘前可以保持打开的文件的最大数量，使用 `partitioned_write_max_open_files` 配置选项（默认值：100）：

```bash
SET partitioned_write_max_open_files = 10;
```

> 最佳实践 将数据写入许多小分区非常昂贵。通常建议每个分区至少有 `100 MB` 的数据。

### 文件名模式

默认情况下，文件将被命名为 `data_0.parquet` 或 `data_0.csv`。通过 `FILENAME_PATTERN` 标志，可以定义一个包含 `{i}` 或 `{uuid}` 的模式以创建特定的文件名：

* `{i}` 将被替换为一个索引
* `{uuid}` 将被替换为一个 128 位的 UUID

将表写入 .parquet 文件的 Hive 分区数据集，并在文件名中包含索引：

```sql
COPY orders TO 'orders'
(FORMAT parquet, PARTITION_BY (year, month), OVERWRITE_OR_IGNORE, FILENAME_PATTERN 'orders_{i}');
```

将表写入 .parquet 文件的 Hive 分区数据集，并使用唯一文件名：

```sql
COPY orders TO 'orders'
(FORMAT parquet, PARTITION_BY (year, month), OVERWRITE_OR_IGNORE, FILENAME_PATTERN 'file_{uuid}');
```

### 覆盖

默认情况下，分区写入不允许覆盖现有目录。
在本地文件系统中，`OVERWRITE` 和 `OVERWRITE_OR_IGNORE` 选项会删除现有目录。
在远程文件系统中，不支持覆盖。

### 追加

要向现有的 Hive 分区目录结构追加数据，使用 `APPEND` 选项：

```sql
COPY orders TO 'orders'
(FORMAT parquet, PARTITION_BY (year, month), APPEND);
```

使用 `APPEND` 选项将产生与 `OVERWRITE_OR_IGNORE, FILENAME_PATTERN '{uuid}'` 选项类似的行为，
但 DuckDB 会额外检查文件是否已存在，并在极少数情况下重新生成 UUID 以避免冲突。

### 处理列名中的斜杠

要处理列名中的斜杠，请使用 [`url_encode` 函数]({% link docs/stable/sql/functions/text.md %}#url_encodestring) 实现的百分比编码。