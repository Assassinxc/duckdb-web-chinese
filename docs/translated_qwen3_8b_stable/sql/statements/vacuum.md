---
---
layout: docu
railroad: statements/vacuum.js
redirect_from:
- /docs/sql/statements/vacuum
title: VACUUM 语句
---

DuckDB 中的 `VACUUM` 语句仅具有基本支持，主要用于 PostgreSQL 兼容性。

某些变体（例如在指定某一列时调用），如果由于更新导致统计信息过时，会重新计算不同的统计信息（不同实体的数量）。

> 警告 `VACUUM` 的行为与 PostgreSQL 的语义不一致，未来可能会发生变化。

## 示例

无操作：

```sql
VACUUM;
```

无操作：

```sql
VACUUM ANALYZE;
```

对给定的表-列对调用 `VACUUM` 会重建表和列的统计信息：

```sql
VACUUM my_table(my_column);
```

重建表和列的统计信息：

```sql
VACUUM ANALYZE my_table(my_column);
```

以下操作不被支持：

```sql
VAC
```