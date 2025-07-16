---
---
layout: docu
redirect_from:
- /docs/guides/performance/indexing
title: 索引
---

DuckDB 有两种类型的索引：Zonemap 索引和 ART 索引。

## Zonemap 索引

DuckDB 会为所有 [通用数据类型]({% link docs/stable/sql/data_types/overview.md %}#general-purpose-data-types) 的列自动创建 [Zonemap](https://en.wikipedia.org/wiki/Block_Range_Index)（也称为 min-max 索引）。
像谓词下推到扫描操作符和计算聚合这些操作都使用 Zonemap 索引。
如果使用过滤条件（例如 `WHERE column1 = 123`），DuckDB 可以跳过任何其 min-max 范围不包含该过滤值的行组（例如，当比较 `= 123` 或 `< 400` 时，可以跳过 min-max 范围为 1000 到 2000 的块）。

### 数据顺序对 Zonemap 索引的影响

列内的数据越有序，Zonemap 索引的价值就越大。
例如，在最坏情况下，列中的每一行都可能包含随机数字。
此时，DuckDB 很可能无法跳过任何行组。
如果你查询具有选择性过滤条件的特定列，最好在插入数据时按这些列进行预排序。
即使排序不完美，仍然会有所帮助。
有序数据的最佳情况通常出现在 `DATETIME` 列中。

### 微基准测试：顺序的影响

举个例子，我们重复运行 [时间戳微基准测试]({% link docs/stable/guides/performance/schema.md %}#microbenchmark-using-timestamps)，使用升序排列的有序时间戳列与无序时间戳列进行比较。

| 列类型 | 是否有序 | 存储大小 | 查询时间 |
|---|---|--:|--:|
| `DATETIME` | 是 | 1.3 GB | 0.6 秒 |
| `DATETIME` | 否 | 3.3 GB | 0.9 秒 |

结果表明，仅仅保持列的顺序可以改善压缩效果，使存储大小减小了 2.5 倍。
它还可以使计算速度提高 1.5 倍。

### 有序整数

另一种利用顺序的方法是使用 `INTEGER` 类型并采用自动递增，而不是使用 `UUID` 来表示被选择性过滤查询的列。
在一张表中包含无序的 `UUID` 时，DuckDB 必须扫描许多行组才能找到特定的 `UUID` 值。
有序的 `INTEGER` 列允许跳过所有行组，只保留包含该值的行组。

## ART 索引

DuckDB 以两种方式支持定义 [自适应基数树 (ART) 索引](https://db.in.tum.de/~leis/papers/ART.pdf)。
首先，对于具有 `PRIMARY KEY`、`FOREIGN KEY` 和 `UNIQUE` [约束]({% link docs/stable/guides/performance/schema.md %}#constraints) 的列，会隐式创建此类索引。
其次，显式运行 [`CREATE INDEX`]({% link docs/stable/sql/indexes.md %}) 语句会在目标列上创建 ART 索引。

在列上创建 ART 索引的权衡如下：

1. ART 索引可以在更改（插入、更新和删除）时进行约束检查。
2. 对于索引表的更改操作性能不如非索引表。
  这是由于这些操作的索引维护所致。
3. 对于某些使用情况，_单列 ART 索引_ 可以提高对索引列的高选择性查询的性能。

ART 索引不会影响连接、聚合和排序查询的性能。

### ART 索引扫描

ART 索引扫描会通过单列 ART 索引查找所需数据，而不是按顺序扫描表。
查找可以提高某些查询的性能。
DuckDB 会尝试使用索引扫描来处理等值和 `IN(...)` 条件。
它还会将动态过滤条件（如来自哈希连接的过滤条件）推送到扫描中，从而在这些过滤条件上执行动态索引扫描。

只有在索引单列且不带表达式时，索引才适合索引扫描。
例如，以下索引适合索引扫描：

```sql
CREATE INDEX idx ON tbl (col1);
```

以下两个索引 **不适合** 索引扫描：

```sql
CREATE INDEX idx_multi_column ON tbl (col1, col2);
CREATE INDEX idx_expr ON tbl (col1 + 1);
```

索引扫描的默认阈值是 `MAX(2048, 0.001 * table_cardinality)`。
你可以通过 `index_scan_percentage` 和 `index_scan_max_count` 来配置此阈值，或者将这些值设为零以禁用索引扫描。
如有疑问，使用 [`EXPLAIN ANALYZE`]({% link docs/stable/guides/meta/explain_analyze.md %}) 来验证查询计划是否使用了索引扫描。

### 索引和内存

DuckDB 通过其缓冲管理器注册索引内存。
然而，这些索引缓冲区尚未进行缓冲管理。
这意味着如果需要驱逐内存，DuckDB 不会销毁任何索引缓冲区。
因此，索引可能会占用 DuckDB 可用内存的很大一部分，这可能会影响内存密集型查询的性能。
重新附加（`DETACH` + `ATTACH`）包含索引的数据库可以缓解这一影响，因为我们对索引内存进行延迟反序列化。
禁用索引扫描并在更改后重新附加数据库，还可以进一步减少索引对 DuckDB 可用内存的影响。

### 索引和打开数据库

索引会被序列化到磁盘，并在重新打开数据库时进行延迟反序列化。
使用索引的操作只会加载索引所需的部分。
因此，拥有索引在打开现有数据库时不会引起任何性能下降。

> 最佳实践 建议遵循以下指南：
>
> * 仅在需要强制数据约束时使用主键、外键或唯一约束。
> * 除非你有高选择性查询且内存充足，否则不要定义显式索引。
> * 如果你定义了 ART 索引，请在批量加载数据到表之后定义。在加载数据之前定义索引（无论是显式还是通过主键/外键）会 [损害加载性能]({% link docs/stable/guides/performance/schema.md %}#microbenchmark-the-effect-of-primary-keys)。