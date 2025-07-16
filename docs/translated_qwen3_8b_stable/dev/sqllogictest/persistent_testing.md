---
---
layout: docu
redirect_from:
- /dev/sqllogictest/persistent_testing
- /dev/sqllogictest/persistent_testing/
- /docs/dev/sqllogictest/persistent_testing
title: 持久化测试
---

默认情况下，所有测试均在内存模式下运行（除非启用了`--force-storage`）。在某些情况下，我们希望强制使用持久化数据库。我们可以通过`load`命令启动一个持久化数据库，并通过`restart`命令触发数据库的重新加载。

```sql
# 从磁盘加载数据库
load __TEST_DIR__/storage_scan.db

statement ok
CREATE TABLE test (a INTEGER);

statement ok
INSERT INTO test VALUES (11), (12), (13), (14), (15), (NULL)

# ...

restart

query I
SELECT * FROM test ORDER BY a
----
NULL
11
12
13
14
15
```

请注意，默认情况下测试会使用`SET wal_autocheckpoint = '0KB'`进行运行 – 表示每次语句后都会触发检查点。WAL测试通常使用以下设置来禁用此行为：

```sql
statement ok
PRAGMA disable_checkpoint_on_shutdown

statement ok
PRAGMA wal_autocheckpoint = '1TB'
```