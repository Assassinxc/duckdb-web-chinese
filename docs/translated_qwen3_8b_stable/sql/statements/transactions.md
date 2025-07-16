---
---
layout: docu
redirect_from:
- /docs/sql/statements/transactions
title: 事务管理
---

DuckDB 支持 [ACID 数据库事务](https://en.wikipedia.org/wiki/Database_transaction)。
事务提供隔离性，即事务所做的更改在提交之前对其他并发事务不可见。
事务也可以被中止，这将丢弃其到目前为止所做的所有更改。

## 语句

DuckDB 提供以下语句用于事务管理。

### 开始事务

要开始一个事务，请运行：

```sql
BEGIN TRANSACTION;
```

### 提交事务

您可以提交事务以使其对其他事务可见，并将其写入持久存储（如果以持久模式使用 DuckDB）。
要提交事务，请运行：

```sql
COMMIT;
```

如果您不在一个活跃的事务中，`COMMIT` 语句将失败。

### 回滚事务

您可以中止一个事务。
此操作也称为回滚，将丢弃事务对数据库所做的任何更改。
要中止事务，请运行：

```sql
ROLLBACK;
```

您也可以使用中止命令，其行为完全相同：

```sql
ABORT;
```

如果您不在一个活跃的事务中，`ROLLBACK` 和 `ABORT` 语句将失败。

### 示例

我们通过一个简单示例来说明事务的使用。

```sql
CREATE TABLE person (name VARCHAR, age BIGINT);

BEGIN TRANSACTION;
INSERT INTO person VALUES ('Ada', 52);
COMMIT;

BEGIN TRANSACTION;
DELETE FROM person WHERE name = 'Ada';
INSERT INTO person VALUES ('Bruce', 39);
ROLLBACK;

SELECT * FROM person;
```

第一个事务（插入“Ada”）被提交，而第二个事务（删除“Ada”并插入“Bruce”）被中止。
因此，最终的表中将只包含 `<'Ada', 52>`。