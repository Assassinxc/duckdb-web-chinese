---
---
layout: docu
redirect_from:
- /docs/guides/performance/schema
title: 模式
---

## 类型

在编码列时，使用正确的类型（例如 `BIGINT`、`DATE`、`DATETIME`）非常重要。虽然始终可以使用字符串类型（如 `VARCHAR` 等）来编码更具体的值，但这不被推荐。字符串会占用更多空间，并且在过滤、连接和聚合等操作中处理速度更慢。

在加载 CSV 文件时，您可以利用 CSV 读取器的 [自动检测机制]({% link docs/stable/data/csv/auto_detection.md %}) 来获取 CSV 输入的正确类型。

如果在内存受限的环境中运行，使用较小的数据类型（例如 `TINYINT`）可以减少完成查询所需的内存和磁盘空间。DuckDB 的 [位打包压缩]({% post_url 2022-10-28-lightweight-compression %}#bit-packing) 表示，即使在较大的数据类型中存储的小值，也不会在磁盘上占用更大的空间，但在处理期间会占用更多内存。

> 最佳实践 在创建列时使用尽可能严格的类型。避免使用字符串来编码更具体的数据显示。

### 微基准测试：使用时间戳

我们通过 [LDBC Comment 表的 `creationDate` 列（scale factor 300）](https://blobs.duckdb.org/data/ldbc-sf300-comments-creationDate.parquet) 来展示聚合速度的差异。该表包含约 5.54 亿个无序时间戳值。我们运行一个简单的聚合查询，从时间戳中返回平均的月份中的天数，使用两种配置进行比较。

首先，我们使用 `DATETIME` 来编码值，并使用 [`extract` datetime 函数]({% link docs/stable/sql/functions/timestamp.md %}) 运行查询：

```sql
SELECT avg(extract('day' FROM creationDate)) FROM Comment;
```

其次，我们使用 `VARCHAR` 类型并使用字符串操作：

```sql
SELECT avg(CAST(creationDate[9:10] AS INTEGER)) FROM Comment;
```

微基准测试的结果如下：

| 列类型 | 存储大小 | 查询时间 |
| ----------- | -----------: | ---------: |
| `DATETIME`  |       3.3 GB |      0.9 s |
| `VARCHAR`   |       5.2 GB |      3.9 s |

结果表明，使用 `DATETIME` 值可以得到更小的存储大小和更快的处理速度。

### 微基准测试：基于字符串的连接

我们通过 [LDBC Comment 表（scale factor 100）](https://blobs.duckdb.org/data/ldbc-sf100-comments.tar.zst) 来展示基于不同类型的连接差异。该表使用 64 位整数标识符作为每行的 `id` 属性。我们执行以下连接操作：

```sql
SELECT count(*) AS count
FROM Comment c1
JOIN Comment c2 ON c1.ParentCommentId = c2.id;
```

在第一个实验中，我们使用正确的（最严格的）类型，即 `id` 和 `ParentCommentId` 列都被定义为 `BIGINT`。
在第二个实验中，我们定义所有列的类型为 `VARCHAR`。
虽然两个实验的查询结果相同，但它们的运行时间差异显著。
以下结果表明，基于 `BIGINT` 列的连接比基于 `VARCHAR` 类型列（编码相同值）的连接快约 1.8 倍。

| 连接列数据类型 | 连接列模式类型 | 示例值      | 查询时间 |
| ------------------------ | ----------------------- | ------------------ | ---------: |
| `BIGINT`                 | `BIGINT`                | `70368755640078`   |      1.2 s |
| `BIGINT`                 | `VARCHAR`               | `'70368755640078'` |      2.1 s |

> 最佳实践 避免将数值表示为字符串，尤其是如果您打算对它们执行连接等操作。

## 约束

DuckDB 允许定义 [约束]({% link docs/stable/sql/constraints.md %})，如 `UNIQUE`、`PRIMARY KEY` 和 `FOREIGN KEY`。这些约束有助于确保数据完整性，但它们会对加载性能产生负面影响，因为它们需要建立索引并执行检查。此外，它们_很少能提升查询性能_，因为 DuckDB 不依赖这些索引来执行连接和聚合操作（有关详细信息，请参阅 [索引]({% link docs/stable/guides/performance/indexing.md %})）。

> 最佳实践 除非您的目标是确保数据完整性，否则不要定义约束。

### 微基准测试：主键的影响

我们通过 [LDBC Comment 表（scale factor 300）](https://blobs.duckdb.org/data/ldbc-sf300-comments.tar.zst) 来展示主键的使用效果。该表包含约 5.54 亿条记录。
在第一个实验中，我们创建模式时不包含主键，然后加载数据。
在第二个实验中，我们创建模式时包含主键，然后加载数据。
在第三个情况下，我们创建模式时不包含主键，加载数据后添加主键约束。
在所有情况下，我们从 `.csv.gz` 文件中获取数据，并测量加载所需的时间。

|                  操作                    | 执行时间 |
|-----------------------------------------------|---------------:|
| 带主键加载                         |        461.6 s |
| 不带主键加载                      |        121.0 s |
| 不带主键加载后添加主键 |        242.0 s |

对于这个数据集，主键仅在高度选择性的查询中（例如按单个标识符过滤）会产生（轻微）正面影响。
定义主键（或索引）不会对连接和聚合操作产生影响。

> 最佳实践 为了获得最佳批量加载性能，请避免使用主键约束。
> 如果必须使用，请在批量加载步骤之后定义它们。