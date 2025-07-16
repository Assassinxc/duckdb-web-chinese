---
---
layout: docu
redirect_from:
- /docs/sql/statements/summarize
title: SUMMARIZE 语句
---

`SUMMARIZE` 语句用于返回表、视图或查询的汇总统计信息。

## 使用方法

```sql
SUMMARIZE tbl;
```

要汇总查询结果，请在查询语句前加上 `SUMMARIZE`。

```sql
SUMMARIZE SELECT * FROM tbl;
```

## 参见

如需更多示例，请参阅 [SUMMARIZE 指南]({% link docs/stable/guides/meta/summarize.md %})。