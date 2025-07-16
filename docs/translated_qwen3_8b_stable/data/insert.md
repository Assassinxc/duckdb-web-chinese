---
---
layout: docu
redirect_from:
- /docs/data/insert
title: INSERT 语句
---

`INSERT` 语句是将数据加载到关系型数据库的标准方式。在使用 `INSERT` 语句时，值是逐行提供的。虽然简单，但解析和处理单个 `INSERT` 语句会带来显著的开销。这使得大量逐行插入操作在批量插入时非常低效。

> 最佳实践 一般来说，避免在插入多行数据时使用大量逐行的 `INSERT` 语句（即避免在循环中使用 `INSERT` 语句）。在批量插入数据时，应尽量在单条语句中插入尽可能多的数据。

如果你必须在循环中使用 `INSERT` 语句来加载数据，请避免在自动提交模式下执行这些语句。每次提交后，数据库都需要将所做的更改同步到磁盘以确保数据不会丢失。在自动提交模式下，每个语句都会被封装在单独的事务中，这意味着每个语句都会调用 `fsync`。在批量加载数据时，这通常是不必要的，并会显著降低程序的运行速度。

> 提示 如果你绝对必须在循环中使用 `INSERT` 语句来加载数据，请将它们包裹在 `BEGIN TRANSACTION` 和 `COMMIT` 调用中。

## 语法

使用 `INSERT INTO` 向表中加载数据的示例如下：

```sql
CREATE TABLE people (id INTEGER, name VARCHAR);
INSERT INTO people VALUES (1, 'Mark'), (2, 'Hannes');
```

如需更详细的描述以及语法图，请参见[INSERT 语句页面]({% link docs/stable/sql/statements/insert.md %})。