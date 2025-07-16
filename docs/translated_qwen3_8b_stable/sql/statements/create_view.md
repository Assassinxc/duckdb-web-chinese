---
---
layout: docu
railroad: statements/createview.js
redirect_from:
- /docs/sql/statements/create_view
title: CREATE VIEW 语句
---

`CREATE VIEW` 语句在目录中定义一个新的视图。

## 示例

创建一个简单的视图：

```sql
CREATE VIEW v1 AS SELECT * FROM tbl;
```

创建一个视图，如果同名的视图已经存在则替换它：

```sql
CREATE OR REPLACE VIEW v1 AS SELECT 42;
```

创建一个视图并替换列名：

```sql
CREATE VIEW v1(a) AS SELECT 42;
```

可以使用 [`duckdb_views()` 函数]({% link docs/stable/sql/meta/duckdb_table_functions.md %}#duckdb_views) 读取现有视图的 SQL 查询，如下所示：

```sql
SELECT sql FROM duckdb_views() WHERE view_name = 'v1';
```

## 语法

<div id="rrdiagram"></div>

`CREATE VIEW` 定义一个查询的视图。该视图不会物理上进行物化。相反，每次在查询中引用该视图时都会执行该查询。

`CREATE OR REPLACE VIEW` 类似，但如果同名的视图已经存在，它将被替换。

如果指定了模式名，则在指定的模式中创建视图。否则，在当前模式中创建视图。临时视图存在于一个特殊的模式中，因此在创建临时视图时不能指定模式名。视图的名称必须与同一模式中的任何其他视图或表的名称不同。