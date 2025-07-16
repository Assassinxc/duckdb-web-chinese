---
---
layout: docu
railroad: statements/checkpoint.js
redirect_from:
- /docs/sql/statements/checkpoint
title: CHECKPOINT 语句
---

`CHECKPOINT` 语句将写前日志（WAL）中的数据同步到数据库数据文件。对于内存数据库，该语句将成功但无任何效果。

## 示例

同步默认数据库中的数据：

```sql
CHECKPOINT;
```

同步指定数据库中的数据：

```sql
CHECKPOINT file_db;
```

中止任何正在进行的事务以同步数据：

```sql
FORCE CHECKPOINT;
```

## 语法

<div id="rrdiagram1"></div>

根据 WAL 大小，检查点操作会自动执行（详见 [配置]({% link docs/stable/configuration/overview.md %} ))。此语句用于手动执行检查点操作。

## 行为

默认的 `CHECKPOINT` 命令如果存在运行中的事务将失败。包含 `FORCE` 将中止所有事务并执行检查点操作。

另请参阅相关的 [`PRAGMA` 选项]({% link docs/stable/configuration/pragmas.md %}#force-checkpoint) 以进一步修改行为。

### 回收空间

在执行检查点（无论是自动还是手动）时，被删除行所占用的空间将部分回收。请注意，这不会删除所有被删除的行，而是将具有大量删除操作的行组合并。在当前实现中，这要求相邻行组中大约有 25% 的行被删除。

在内存模式下运行时，检查点操作不会产生任何效果，因此不会回收内存数据库中删除操作后产生的空间。

> 警告 [`VACUUM` 语句]({% link docs/stable/sql/statements/vacuum.md %}) 不会触发真空操作，因此不会回收空间。