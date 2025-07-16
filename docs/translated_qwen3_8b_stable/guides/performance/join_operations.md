---
---
layout: docu
redirect_from:
- /docs/guides/performance/join_operations
title: 连接操作
---

## 如何强制指定连接顺序

DuckDB 拥有一个基于成本的查询优化器，它使用基础表中的统计信息（存储在 DuckDB 数据库或 Parquet 文件中）来估计操作的基数。

### 关闭连接顺序优化器

要关闭连接顺序优化器，请设置以下 [`PRAGMA`s]({% link docs/stable/configuration/pragmas.md %})：

```sql
SET disabled_optimizers = 'join_order,build_side_probe_side';
```

这将禁用连接顺序优化器以及连接的左右交换功能。
这样，DuckDB 将按照 `JOIN` 子句的顺序构建一个左深连接树。

```sql
SELECT ...
FROM ...
JOIN ...  -- 此连接首先执行
JOIN ...; -- 此连接其次执行
```

一旦执行了相关查询，请使用以下命令重新启用优化器：

```sql
SET disabled_optimizers = '';
```

### 创建临时表

要强制特定的连接顺序，您可以将查询拆分为多个查询，每个查询创建一个临时表：

```sql
CREATE OR REPLACE TEMPORARY TABLE t1 AS
    ...;

-- 在第一个查询的结果 t1 上进行连接
CREATE OR REPLACE TEMPORARY TABLE t2 AS
    SELECT * FROM t1 ...;

-- 使用 t2 计算最终结果
SELECT * FROM t1 ...
```

清理时，请删除中间表：

```sql
DROP TABLE IF EXISTS t1;
DROP TABLE IF EXISTS t2;
```