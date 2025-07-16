---
---
layout: docu
redirect_from:
- /docs/sql/dialect/indexing
title: 索引
---

DuckDB 使用 1-based 索引，除了 [JSON 对象]({% link docs/stable/data/json/overview.md %})，它们使用 0-based 索引。

## 示例

对于字符串、列表等，索引起始值为 1。

```sql
SELECT list[1] AS element
FROM (SELECT ['first', 'second', 'third'] AS list);
```

```text
┌─────────┐
│ element │
│ varchar │
├─────────┤
│ first   │
└─────────┘
```

对于 JSON 对象，索引起始值为 0。

```sql
SELECT json[1] AS element
FROM (SELECT '["first", "second", "third"]'::JSON AS json);
```

```text
┌──────────┐
│ element  │
│   json   │
├──────────┤
│ "second" │
└──────────┘
```