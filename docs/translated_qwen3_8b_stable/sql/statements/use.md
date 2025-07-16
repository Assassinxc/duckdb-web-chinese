---
---
layout: docu
railroad: statements/use.js
redirect_from:
- /docs/sql/statements/use
title: USE 语句
---

`USE` 语句选择一个数据库和可选的模式，或仅选择一个模式作为默认模式。

## 示例

```sql
--- 设置 'memory' 数据库为默认数据库。如果不存在，则隐式使用 'main' 模式或报错
--- 如果不存在，则隐式使用 'main' 模式或报错
USE memory;
--- 设置 'duck.main' 数据库和模式为默认
USE duck.main;
-- 设置当前所选数据库的 `main` 模式为默认模式，此时为 'duck.main'
USE main;
```

## 语法

<div id="rrdiagram1"></div>

`USE` 语句为未来的操作设置一个默认数据库、模式或数据库/模式组合。例如，如果没有提供完全限定的表名创建表，表将被创建在默认数据库中。