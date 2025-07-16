---
---
layout: docu
redirect_from:
- /docs/sql/statements/analyze
title: ANALYZE 语句
---

`ANALYZE` 语句会重新计算 DuckDB 表的统计信息。

## 使用方式

`ANALYZE` 语句重新计算的统计信息仅用于 [连接顺序优化](https://blobs.duckdb.org/papers/tom-ebergen-msc-thesis-join-order-optimization-with-almost-no-statistics.pdf)。因此，建议在执行大量更新（插入和/或删除操作）后重新计算这些统计信息，以提高连接顺序。

要重新计算统计信息，请运行：

```sql
ANALYZE;
```