---
---
layout: docu
redirect_from:
- /docs/guides/meta/explain_analyze
title: 'EXPLAIN ANALYZE: 查询分析'
---

在查询前添加 `EXPLAIN ANALYZE`，可以对查询计划进行格式化显示，并执行该查询，为每个操作符提供运行时性能数据，以及估计的基数 (`EC`) 和实际的基数。

```sql
EXPLAIN ANALYZE SELECT * FROM tbl;
```

请注意，**每个操作符**所花费的累计实际运行时间都会显示。当多个线程并行处理查询时，整个查询的总处理时间可能低于所有操作符所花费时间的总和。

以下是运行 `EXPLAIN ANALYZE` 的一个示例：

```sql
CREATE TABLE students (name VARCHAR, sid INTEGER);
CREATE TABLE exams (eid INTEGER, subject VARCHAR, sid INTEGER);
INSERT INTO students VALUES ('Mark', 1), ('Joe', 2), ('Matthew', 3);
INSERT INTO exams VALUES (10, 'Physics', 1), (20, 'Chemistry', 2), (30, 'Literature', 3);

EXPLAIN ANALYZE
    SELECT name
    FROM students
    JOIN exams USING (sid)
    WHERE name LIKE 'Ma%';
```

```text
┌─────────────────────────────────────┐
│┌───────────────────────────────────┐│
││        Total Time: 0.0008s        ││
│└───────────────────────────────────┘│
└─────────────────────────────────────┘
┌───────────────────────────┐
│      EXPLAIN_ANALYZE      │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│             0             │
│          (0.00s)          │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         PROJECTION        │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│            name           │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│             2             │
│          (0.00s)          │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         HASH_JOIN         │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│           INNER           │
│         sid = sid         │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ├──────────────┐
│           EC: 1           │              │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │              │
│             2             │              │
│          (0.00s)          │              │
└─────────────┬─────────────┘              │
┌─────────────┴─────────────┐┌─────────────┴─────────────┐
│         SEQ_SCAN          ││           FILTER          │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ││   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│           exams           ││     prefix(name, 'Ma')    │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ││   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│            sid            ││           EC: 1           │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ││   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│           EC: 3           ││             2             │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ││          (0.00s)          │
│             3             ││                           │
│          (0.00s)          ││                           │
└───────────────────────────┘└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         SEQ_SCAN          │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│          students         │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│            sid            │
│            name           │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│ Filters: name>=Ma AND name│
│  <Mb AND name IS NOT NULL │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│           EC: 1           │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│             2             │
│          (0.00s)          │
└───────────────────────────┘
```

## 参见

如需更多信息，请参阅[“分析”页面]({% link docs/stable/dev/profiling.md %})。