---
---
layout: docu
redirect_from:
- /docs/data/json/caveats
title: 注意事项
---

## 等值比较

> 警告 当前，JSON 文件的等值比较可能根据上下文有所不同。在某些情况下，它是基于原始文本的比较，而在其他情况下，则使用逻辑内容的比较。

以下查询对于所有字段均返回 true：

```sql
SELECT
    a != b, -- 空格是物理 JSON 内容的一部分。尽管逻辑内容相等，但值被视为不相等。
    c != d, -- 同上。
    c[0] = d[0], -- 等值，因为字段的物理内容中的空格已被移除：
    a = c[0], -- 实际上，字段等于没有空格的空列表...
    b != c[0], -- ...但与带有空格的空列表不同。
FROM (
    SELECT
        '[]'::JSON AS a,
        '[ ]'::JSON AS b,
        '[[]]'::JSON AS c,
        '[[ ]]'::JSON AS d
    );
```

<div class="monospace_table"></div>

| (a != b) | (c != d) | (c[0] = d[0]) | (a = c[0]) | (b != c[0]) |
|----------|----------|---------------|------------|-------------|
| true     | true     | true          | true       | true        |