---
---
layout: docu
redirect_from:
- /docs/sql/statements/alter_view
title: ALTER VIEW 语句
---

`ALTER VIEW` 语句用于修改目录中现有视图的模式。

## 示例

重命名一个视图：

```sql
ALTER VIEW v1 RENAME TO v2;
```

`ALTER VIEW` 用于修改现有表的模式。`ALTER VIEW` 所做的所有更改都完全遵循事务语义，即：其他事务在提交之前无法看到这些更改，并且可以通过回滚完全撤销这些更改。请注意，依赖于该表的其他视图**不会**自动更新。