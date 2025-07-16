---
---
layout: docu
redirect_from:
- /docs/data/partitioning/hive_partitioning
title: Hive 分区
---

## 示例

从 Hive 分区数据集中读取数据：

```sql
SELECT *
FROM read_parquet('orders/*/*/*.parquet', hive_partitioning = true);
```

将表写入 Hive 分区数据集：

```sql
COPY orders
TO 'orders' (FORMAT parquet, PARTITION_BY (year, month));
```

请注意，`PARTITION_BY` 选项不能使用表达式。您可以使用以下语法在运行时生成列：

```sql
COPY (SELECT *, year(timestamp) AS year, month(timestamp) AS month FROM services)
TO 'test' (PARTITION_BY (year, month));
```

在读取时，分区列会从目录结构中读取，并且根据 `hive_partitioning` 参数决定是否包含这些列。

```sql
FROM read_parquet('test/*/*/*.parquet', hive_partitioning = false); -- 不包含 year, month 列
FROM read_parquet('test/*/*/*.parquet', hive_partitioning = true);  -- 包含 year, month 分区列
```

## Hive 分区

Hive 分区是一种 [分区策略](https://en.wikipedia.org/wiki/Partition_(database))，用于根据 **分区键** 将表拆分成多个文件。这些文件被组织成文件夹。在每个文件夹中，**分区键** 的值由文件夹的名称决定。

以下是一个 Hive 分区文件层次结构的示例。文件根据两个键 (`year` 和 `month`) 进行分区。

```text
orders
├── year=2021
│    ├── month=1
│    │   ├── file1.parquet
│    │   └── file2.parquet
│    └── month=2
│        └── file3.parquet
└── year=2022
     ├── month=11
     │   ├── file4.parquet
     │   └── file5.parquet
     └── month=12
         └── file6.parquet
```

存储在这个层次结构中的文件可以通过 `hive_partitioning` 标志进行读取。

```sql
SELECT *
FROM read_parquet('orders/*/*/*.parquet', hive_partitioning = true);
```

当我们指定 `hive_partitioning` 标志时，列的值将从目录中读取。

### 过滤下推

对分区键的过滤条件会自动下推到文件中。这样系统就可以跳过那些对查询无用的文件。例如，考虑以下对上述数据集的查询：

```sql
SELECT *
FROM read_parquet('orders/*/*/*.parquet', hive_partitioning = true)
WHERE year = 2022
  AND month = 11;
```

执行此查询时，只会读取以下文件：

```text
orders
└── year=2022
     └── month=11
         ├── file4.parquet
         └── file5.parquet
```

### 自动检测

默认情况下，系统会尝试推断提供的文件是否处于 Hive 分区层次结构中。如果是，则会自动启用 `hive_partitioning` 标志。自动检测会查看文件夹的名称，并查找 `'key' = 'value'` 的模式。此行为可以通过使用 `hive_partitioning` 配置选项进行覆盖：

```sql
SET hive_partitioning = false;
```

### Hive 类型

`hive_types` 是一种指定 Hive 分区逻辑类型的方式：

```sql
SELECT *
FROM read_parquet(
    'dir/**/*.parquet',
    hive_partitioning = true,
    hive_types = {'release': DATE, 'orders': BIGINT}
);
```

`hive_types` 将自动检测以下类型：`DATE`、`TIMESTAMP` 和 `BIGINT`。要关闭自动检测，可以设置标志 `hive_types_autocast = 0`。

### 写入分区文件

参见 [分区写入]({% link docs/stable/data/partitioning/partitioned_writes.md %}) 部分。