---
---
layout: docu
redirect_from:
- /docs/sql/statements/profiling
title: 查询剖析
---

DuckDB 通过 `EXPLAIN` 和 `EXPLAIN ANALYZE` 语句支持查询剖析。

## `EXPLAIN`

要查看查询的查询计划而不执行查询，请运行：

```sql
EXPLAIN ⟨query⟩;
```

`EXPLAIN` 的输出包含每个操作符的预估基数。

## `EXPLAIN ANALYZE`

要剖析查询，请运行：

```sql
EXPLAIN ANALYZE ⟨query⟩;
```

`EXPLAIN ANALYZE` 语句会执行查询，并显示每个操作符的实际基数，以及在每个操作符上累计的墙上时间。