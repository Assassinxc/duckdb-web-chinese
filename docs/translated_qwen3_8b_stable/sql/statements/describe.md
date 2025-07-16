---
---
layout: docu
redirect_from:
- /docs/sql/statements/describe
title: DESCRIBE 语句
---

`DESCRIBE` 语句显示表、视图或查询的模式。

## 使用方式

```sql
DESCRIBE tbl;
```

为了总结一个查询，可以将 `DESCRIBE` 添加到查询语句前。

```sql
DESCRIBE SELECT * FROM tbl;
```

## 别名

`SHOW` 语句是 `DESCRIBE` 的别名。

## 参见

如需更多示例，请参阅 [DESCRIBE 指南]({% link docs/stable/guides/meta/describe.md %})。