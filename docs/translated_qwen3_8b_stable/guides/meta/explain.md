---
---
layout: docu
redirect_from:
- /docs/guides/meta/explain
title: 'EXPLAIN: 检查查询计划'
---

```sql
EXPLAIN SELECT * FROM tbl;
```

`EXPLAIN` 语句会显示物理计划，即即将执行的查询计划，并通过在查询前添加 `EXPLAIN` 来启用。物理计划是一棵树状结构的操作符，以特定顺序执行以生成查询结果。为了生成高效的物理计划，查询优化器会将现有的物理计划转换为更优的物理计划。

为了演示，参见以下示例：

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
┌─────────────────────────────┐
│┌───────────────────────────┐│
││       物理计划       ││
│└───────────────────────────┘│
└─────────────────────────────┘
┌───────────────────────────┐
│         投影        │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│            name           │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         哈希连接         │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│           内连接           │
│         sid = sid         ├──────────────┐
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │              │
│           EC: 1           │              │
└─────────────┬─────────────┘              │
┌─────────────┴─────────────┐┌─────────────┴─────────────┐
│         序列扫描          ││           过滤器          │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ││   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│           exams           ││     前缀(name, 'Ma')    │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ││   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│            sid            ││           EC: 1           │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ││                           │
│           EC: 3           ││                           │
└───────────────────────────┘└─────────────┬─────────────┘
                             ┌─────────────┴─────────────┐
                             │         序列扫描          │
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
                             └───────────────────────────┘
```

请注意，查询实际上并未执行，因此我们只能看到每个操作符的估计基数（`EC`），它通过使用基础表的统计信息并应用每个操作符的启发式方法计算得出。

## 其他 EXPLAIN 设置

`EXPLAIN` 语句支持一些额外的设置，可用于控制输出。以下设置可用：

默认设置。仅显示物理计划。

```sql
PRAGMA explain_output = 'physical_only';
```

仅显示优化后的计划。

```sql
PRAGMA explain_output = 'optimized_only';
```

同时显示物理计划和优化后的计划。

```sql
PRAGMA explain_output = 'all';
```

## 参见

如需更多信息，请参阅 [“剖析”页面]({% link docs/stable/dev/profiling.md %})。