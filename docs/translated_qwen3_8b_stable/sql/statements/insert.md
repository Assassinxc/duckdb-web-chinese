---
---
layout: docu
railroad: statements/insert.js
redirect_from:
- /docs/sql/statements/insert
title: INSERT 语句
---

`INSERT` 语句将新数据插入到表中。

### 示例

将值 1、2、3 插入到 `tbl` 中：

```sql
INSERT INTO tbl
    VALUES (1), (2), (3);
```

将查询结果插入到表中：

```sql
INSERT INTO tbl
    SELECT * FROM other_tbl;
```

将值插入到 `i` 列中，其他列插入默认值：

```sql
INSERT INTO tbl (i)
    VALUES (1), (2), (3);
```

显式地将默认值插入到列中：

```sql
INSERT INTO tbl (i)
    VALUES (1), (DEFAULT), (3);
```

假设 `tbl` 有主键/唯一约束，在冲突时不做任何操作：

```sql
INSERT OR IGNORE INTO tbl (i)
    VALUES (1);
```

或者用新值更新表：

```sql
INSERT OR REPLACE INTO tbl (i)
    VALUES (1);
```

### 语法

<div id="rrdiagram"></div>

`INSERT INTO` 将新行插入到表中。可以插入一个或多个由值表达式指定的行，或零个或多个由查询结果生成的行。

## 插入列顺序

可以提供一个可选的插入列顺序，该顺序可以是 `BY POSITION`（默认）或 `BY NAME`。
每个未在显式或隐式列列表中出现的列将被填充默认值，即其声明的默认值或如果没有则为 `NULL`。

如果任何列的表达式数据类型不正确，将尝试自动类型转换。

### `INSERT INTO ... [BY POSITION]`

表中列的值插入顺序由列声明的顺序决定。
也就是说，`VALUES` 子句或查询提供的值将按照列列表从左到右进行关联。
这是默认选项，可以使用 `BY POSITION` 显式指定。
例如：

```sql
CREATE TABLE tbl (a INTEGER, b INTEGER);
INSERT INTO tbl
    VALUES (5, 42);
```

指定 `BY POSITION` 是可选的，等同于默认行为：

```sql
INSERT INTO tbl
    BY POSITION
    VALUES (5, 42);
```

要使用不同的顺序，可以在目标中提供列名，例如：

```sql
CREATE TABLE tbl (a INTEGER, b INTEGER);
INSERT INTO tbl (b, a)
    VALUES (5, 42);
```

添加 `BY POSITION` 会得到相同的行为：

```sql
INSERT INTO tbl
    BY POSITION (b, a)
    VALUES (5, 42);
```

这会将 `5` 插入到 `b`，`42` 插入到 `a`。

### `INSERT INTO ... BY NAME`

使用 `BY NAME` 修饰符，将 `SELECT` 语句的列列表名称与表的列名称进行匹配，以确定插入表的值顺序。这允许在列顺序与 `SELECT` 语句中的值顺序不同时，甚至某些列缺失时进行插入。

例如：

```sql
CREATE TABLE tbl (a INTEGER, b INTEGER);
INSERT INTO tbl BY NAME (SELECT 42 AS b, 32 AS a);
INSERT INTO tbl BY NAME (SELECT 22 AS b);
SELECT * FROM tbl;
```

|  a   | b  |
|-----:|---:|
| 32   | 42 |
| NULL | 22 |

需要注意的是，使用 `INSERT INTO ... BY NAME` 时，`SELECT` 语句中指定的列名必须与表中的列名匹配。如果列名拼写错误或不存在于表中，将引发错误。`SELECT` 语句中缺失的列将被填充默认值。

## `ON CONFLICT` 子句

可以使用 `ON CONFLICT` 子句来处理由于 `UNIQUE` 或 `PRIMARY KEY` 约束引发的冲突。
以下示例展示了一个这样的冲突：

```sql
CREATE TABLE tbl (i INTEGER PRIMARY KEY, j INTEGER);
INSERT INTO tbl
    VALUES (1, 42);
INSERT INTO tbl
    VALUES (1, 84);
```

这将引发错误：

```console
约束错误：
重复键 "i: 1" 违反主键约束。
```

表中将保留首次插入的行：

```sql
SELECT * FROM tbl;
```

| i | j  |
|--:|---:|
| 1 | 42 |

可以通过显式处理冲突来避免这些错误消息。
DuckDB 支持两种这样的子句： [`ON CONFLICT DO NOTHING`](#do-nothing-clause) 和 [`ON CONFLICT DO UPDATE SET ...`](#do-update-clause-upsert)。

### `DO NOTHING` 子句

`DO NOTHING` 子句将忽略错误，并且不插入或更新值。
例如：

```sql
CREATE TABLE tbl (i INTEGER PRIMARY KEY, j INTEGER);
INSERT INTO tbl
    VALUES (1, 42);
INSERT INTO tbl
    VALUES (1, 84)
    ON CONFLICT DO NOTHING;
```

这些语句成功完成，并且表中保留行 `<i: 1, j: 42>`。

#### `INSERT OR IGNORE INTO`

`INSERT OR IGNORE INTO ...` 是 `INSERT INTO ... ON CONFLICT DO NOTHING` 的简写语法。
例如，以下语句是等价的：

```sql
INSERT OR IGNORE INTO tbl
    VALUES (1, 84);
INSERT INTO tbl
    VALUES (1, 84) ON CONFLICT DO NOTHING;
```

### `DO UPDATE` 子句（Upsert）

`DO UPDATE` 子句会将 `INSERT` 转换为对冲突行的 `UPDATE` 操作。
`SET` 表达式决定了这些行如何被更新。表达式可以使用特殊的虚拟表 `EXCLUDED`，其中包含行的冲突值。
可选地，您可以提供一个额外的 `WHERE` 子句，以排除某些行的更新。
不满足此条件的冲突将被忽略。

由于我们需要一种方法来引用 **待插入** 的元组和 **现有** 的元组，我们引入了特殊的 `EXCLUDED` 限定符。
当提供 `EXCLUDED` 限定符时，引用指的是 **待插入** 的元组，否则指的是 **现有** 的元组。
此特殊限定符可以在 `ON CONFLICT` 子句的 `WHERE` 子句和 `SET` 表达式中使用。

```sql
CREATE TABLE tbl (i INTEGER PRIMARY KEY, j INTEGER);
INSERT INTO tbl VALUES (1, 42);
INSERT INTO tbl VALUES (1, 52), (1, 62) ON CONFLICT DO UPDATE SET j = EXCLUDED.j;
```

#### 示例

使用 `DO UPDATE` 的一个示例如下：

```sql
CREATE TABLE tbl (i INTEGER PRIMARY KEY, j INTEGER);
INSERT INTO tbl
    VALUES (1, 42);
INSERT INTO tbl
    VALUES (1, 84)
    ON CONFLICT DO UPDATE SET j = EXCLUDED.j;
SELECT * FROM tbl;
```

| i | j  |
|--:|---:|
| 1 | 84 |

重新排列列并使用 `BY NAME` 也是可能的：

```sql
CREATE TABLE tbl (i INTEGER PRIMARY KEY, j INTEGER);
INSERT INTO tbl
    VALUES (1, 42);
INSERT INTO tbl (j, i)
    VALUES (168, 1)
    ON CONFLICT DO UPDATE SET j = EXCLUDED.j;
INSERT INTO tbl
    BY NAME (SELECT 1 AS i, 336 AS j)
    ON CONFLICT DO UPDATE SET j = EXCLUDED.j;
SELECT * FROM tbl;
```

| i |  j  |
|--:|----:|
| 1 | 336 |

#### `INSERT OR REPLACE INTO`

`INSERT OR REPLACE INTO ...` 是 `INSERT INTO ... DO UPDATE SET c1 = EXCLUDED.c1, c2 = EXCLUDED.c2, ...` 的简写语法。
即，它会将 **现有** 行的每一列更新为 **待插入** 行的新值。
例如，给定以下输入表：

```sql
CREATE TABLE tbl (i INTEGER PRIMARY KEY, j INTEGER);
INSERT INTO tbl
    VALUES (1, 42);
```

这些语句是等价的：

```sql
INSERT OR REPLACE INTO tbl
    VALUES (1, 84);
INSERT INTO tbl
    VALUES (1, 84)
    ON CONFLICT DO UPDATE SET j = EXCLUDED.j;
INSERT INTO tbl (j, i)
    VALUES (84, 1)
    ON CONFLICT DO UPDATE SET j = EXCLUDED.j;
INSERT INTO tbl BY NAME
    (SELECT 84 AS j, 1 AS i)
    ON CONFLICT DO UPDATE SET j = EXCLUDED.j;
```

#### 限制

当使用 `ON CONFLICT ... DO UPDATE` 子句并且发生冲突时，DuckDB 会将未受冲突影响的行的列值设置为 `NULL`，然后重新分配它们的值。如果受影响的列使用了 `NOT NULL` 约束，这将触发 `NOT NULL constraint failed` 错误。例如：

```sql
CREATE TABLE t1 (id INTEGER PRIMARY KEY, val1 DOUBLE, val2 DOUBLE NOT NULL);
CREATE TABLE t2 (id INTEGER PRIMARY KEY, val1 DOUBLE);
INSERT INTO t1
    VALUES (1, 2, 3);
INSERT INTO t2
    VALUES (1, 5);

INSERT INTO t1 BY NAME (SELECT id, val1 FROM t2)
    ON CONFLICT DO UPDATE
    SET val1 = EXCLUDED.val1;
```

这将失败并抛出以下错误：

```console
约束错误：
NOT NULL 约束失败：t1.val2
```

#### 复合主键

当需要多个列作为唯一性约束的一部分时，使用一个包含所有相关列的 `PRIMARY KEY` 子句：

```sql
CREATE TABLE t1 (id1 INTEGER, id2 INTEGER, val1 DOUBLE, PRIMARY KEY(id1, id2));
INSERT OR REPLACE INTO t1
    VALUES (1, 2, 3);
INSERT OR REPLACE INTO t1
    VALUES (1, 2, 4);
```

### 定义冲突目标

可以提供一个冲突目标作为 `ON CONFLICT (conflict_target)`。这是一组列，索引或唯一性/主键约束定义在其上。如果省略冲突目标，或目标表的主键约束。

除非使用 [`DO UPDATE`](#do-update-clause-upsert) 并且表上有多个唯一/主键约束，否则指定冲突目标是可选的。

```sql
CREATE TABLE tbl (i INTEGER PRIMARY KEY, j INTEGER UNIQUE, k INTEGER);
INSERT INTO tbl
    VALUES (1, 20, 300);
SELECT * FROM tbl;
```

| i | j  |  k  |
|--:|---:|----:|
| 1 | 20 | 300 |

```sql
INSERT INTO tbl
    VALUES (1, 40, 700)
    ON CONFLICT (i) DO UPDATE SET k = 2 * EXCLUDED.k;
```

| i | j  |  k   |
|--:|---:|-----:|
| 1 | 20 | 1400 |

```sql
INSERT INTO tbl
    VALUES (1, 20, 900)
    ON CONFLICT (j) DO UPDATE SET k = 5 * EXCLUDED.k;
```

| i | j  |  k   |
|--:|---:|-----:|
| 1 | 20 | 4500 |

当提供冲突目标时，可以进一步使用 `WHERE` 子句来过滤，该子句应适用于所有冲突。

```sql
INSERT INTO tbl
    VALUES (1, 40, 700)
    ON CONFLICT (i) DO UPDATE SET k = 2 * EXCLUDED.k WHERE k < 100;
```

## `RETURNING` 子句

`RETURNING` 子句可用于返回插入的行内容。这在某些列在插入时需要计算时非常有用。例如，如果表包含一个自动递增的主键，则 `RETURNING` 子句将包含自动创建的主键。这在生成列的情况下也很有用。

可以选择返回某些或所有列，并且可以使用别名来重命名它们。也可以返回任意非聚合表达式，而不是仅仅返回列。使用 `*` 表达式可以返回所有列，也可以在 `*` 返回的所有列之外返回列或表达式。

例如：

```sql
CREATE TABLE t1 (i INTEGER);
INSERT INTO t1
    SELECT 42
    RETURNING *;
```

| i  |
|---:|
| 42 |

一个更复杂的示例，包含 `RETURNING` 子句中的表达式：

```sql
CREATE TABLE t2 (i INTEGER, j INTEGER);
INSERT INTO t2
    SELECT 2 AS i, 3 AS j
    RETURNING *, i * j AS i_times_j;
```

| i | j | i_times_j |
|--:|--:|----------:|
| 2 | 3 | 6         |

下一个示例展示了 `RETURNING` 子句更有帮助的情况。首先创建一个带有主键列的表。然后创建一个序列，以允许主键在插入新行时递增。当我们插入表时，我们并不知道序列生成的值，因此返回这些值很有价值。有关更多信息，请参阅 [`CREATE SEQUENCE` 页面]({% link docs/stable/sql/statements/create_sequence.md %}).

```sql
CREATE TABLE t3 (i INTEGER PRIMARY KEY, j INTEGER);
CREATE SEQUENCE 't3_key';
INSERT INTO t3
    SELECT nextval('t3_key') AS i, 42 AS j
    UNION ALL
    SELECT nextval('t3_key') AS i, 43 AS j
    RETURNING *;
```

| i | j  |
|--:|---:|
| 1 | 42 |
| 2 | 43 |