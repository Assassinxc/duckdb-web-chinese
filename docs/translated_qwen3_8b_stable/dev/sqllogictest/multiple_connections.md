---
---
layout: docu
redirect_from:
- /dev/sqllogictest/multiple_connections
- /dev/sqllogictest/multiple_connections/
- /docs/dev/sqllogictest/multiple_connections
title: 多连接
---

对于旨在验证事务管理或数据版本控制是否正确的测试，通常需要使用多个连接。例如，如果我们想验证表的创建是否正确地具有事务性，我们可能希望在 `con1` 中启动一个事务并创建表，然后在 `con2` 中执行一个查询，检查该表在提交之前是否不可访问。

我们可以在 sqllogictests 中使用 `连接标签` 来使用多个连接。连接标签可以可选地附加到任何 `语句` 或 `查询`。具有相同连接标签的所有查询将在同一个连接中执行。验证上述特性的测试可能如下所示：

```sql
statement ok con1
BEGIN TRANSACTION

statement ok con1
CREATE TABLE integers (i INTEGER);

statement error con2
SELECT * FROM integers;
```

## 并发连接

在语句和查询上使用连接修饰符将测试多个连接，但所有查询仍将按顺序在单个线程上运行。如果我们希望在多个线程上并发地从多个连接运行代码，可以使用 `concurrentloop` 构造。`concurrentloop` 中的查询将在同一时间在不同的线程上并发运行。

```sql
concurrentloop i 0 10

statement ok
CREATE TEMP TABLE t2 AS (SELECT 1);

statement ok
INSERT INTO t2 VALUES (42);

statement ok
DELETE FROM t2

endloop
```

`concurrentloop` 的一个注意事项是，结果通常不可预测 – 当多个客户端同时对数据库进行操作时，可能会出现（预期的）事务冲突。`statement maybe` 可用于处理这些情况。`statement maybe` 基本上接受成功和带有特定错误信息的失败。

```sql
concurrentloop i 1 10

statement maybe
CREATE OR REPLACE TABLE t2 AS (SELECT -54124033386577348004002656426531535114 FROM t2 LIMIT 70%);
----
write-write conflict

endloop
```