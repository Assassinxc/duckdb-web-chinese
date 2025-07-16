---
---
layout: docu
railroad: statements/createsequence.js
redirect_from:
- /docs/sql/statements/create_sequence
title: CREATE SEQUENCE 语句
---

`CREATE SEQUENCE` 语句用于创建一个新的序列号生成器。

### 示例

生成一个从 1 开始递增的序列：

```sql
CREATE SEQUENCE serial;
```

从指定的起始数字生成序列：

```sql
CREATE SEQUENCE serial START 101;
```

使用 `INCREMENT BY` 生成奇数：

```sql
CREATE SEQUENCE serial START WITH 1 INCREMENT BY 2;
```

生成一个从 99 开始递减的序列：

```sql
CREATE SEQUENCE serial START WITH 99 INCREMENT BY -1 MAXVALUE 99;
```

默认情况下，不允许循环，否则会报错，例如：

```console
序列错误：
nextval: 序列 "serial" 的最大值已达到 (10)
```

```sql
CREATE SEQUENCE serial START WITH 1 MAXVALUE 10;
```

`CYCLE` 允许序列在同一个序列中重复循环：

```sql
CREATE SEQUENCE serial START WITH 1 MAXVALUE 10 CYCLE;
```

### 创建和删除序列

序列可以像其他目录项一样创建和删除。

覆盖现有的序列：

```sql
CREATE OR REPLACE SEQUENCE serial;
```

如果序列尚未存在才创建序列：

```sql
CREATE SEQUENCE IF NOT EXISTS serial;
```

删除序列：

```sql
DROP SEQUENCE serial;
```

如果存在则删除序列：

```sql
DROP SEQUENCE IF EXISTS serial;
```

### 使用序列作为主键

序列可以为表提供一个整数主键。例如：

```sql
CREATE SEQUENCE id_sequence START 1;
CREATE TABLE tbl (id INTEGER DEFAULT nextval('id_sequence'), s VARCHAR);
INSERT INTO tbl (s) VALUES ('hello'), ('world');
SELECT * FROM tbl;
```

该脚本生成以下表：

| id |   s   |
|---:|-------|
| 1  | hello |
| 2  | world |

也可以使用 [`ALTER TABLE` 语句]({% link docs/stable/sql/statements/alter_table.md %}) 添加序列。以下示例添加了一个 `id` 列，并使用序列生成的值填充该列：

```sql
CREATE TABLE tbl (s VARCHAR);
INSERT INTO tbl VALUES ('hello'), ('world');
CREATE SEQUENCE id_sequence START 1;
ALTER TABLE tbl ADD COLUMN id INTEGER DEFAULT nextval('id_sequence');
SELECT * FROM tbl;
```

此脚本生成与前一个示例相同的表。

### 选择下一个值

要从序列中选择下一个数字，请使用 `nextval`：

```sql
CREATE SEQUENCE serial START 1;
SELECT nextval('serial') AS nextval;
```

| nextval |
|--------:|
| 1       |

在 `INSERT` 命令中使用此序列：

```sql
INSERT INTO distributors VALUES (nextval('serial'), 'nothing');
```

### 选择当前值

您也可以查看序列的当前值。请注意，在调用 `currval` 之前必须已经调用了 `nextval` 函数，否则会抛出序列化错误（`sequence is not yet defined in this session`）。

```sql
CREATE SEQUENCE serial START 1;
SELECT nextval('serial') AS nextval;
SELECT currval('serial') AS currval;
```

| currval |
|--------:|
| 1       |

### 语法

<div id="rrdiagram"></div>

`CREATE SEQUENCE` 用于创建一个新的序列号生成器。

如果指定了模式名称，则在指定的模式中创建序列。否则，在当前模式中创建序列。临时序列存在于一个特殊的模式中，因此在创建临时序列时不能指定模式名称。序列名称必须与同一模式中的其他任何序列名称不同。

序列创建后，可以使用 `nextval` 函数对其进行操作。

## 参数

| 名称 | 描述 |
|:--|:-----|
| `CYCLE` 或 `NO CYCLE` | `CYCLE` 选项允许序列在升序或降序达到 `maxvalue` 或 `minvalue` 时循环。如果达到限制，生成的下一个数字将是 `minvalue` 或 `maxvalue`。如果指定了 `NO CYCLE`，则在序列达到最大值后，任何对 `nextval` 的调用都会返回错误。如果未指定 `CYCLE` 或 `NO CYCLE`，则默认为 `NO CYCLE`。 |
| `increment` | 可选子句 `INCREMENT BY increment` 指定当前序列值加上多少以生成新值。正数会生成升序序列，负数会生成降序序列。默认值为 1。 |
| `maxvalue` | 可选子句 `MAXVALUE maxvalue` 确定序列的最大值。如果未提供此子句或指定了 `NO MAXVALUE`，则使用默认值。升序序列的默认值为 `2^63 - 1`，降序序列的默认值为 `-1`。 |
| `minvalue` | 可选子句 `MINVALUE minvalue` 确定序列可以生成的最小值。如果未提供此子句或指定了 `NO MINVALUE`，则使用默认值。升序序列的默认值为 `1`，降序序列的默认值为 `-(2^63 - 1)`。 |
| `name` | 要创建的序列的名称（可选模式限定）。 |
| `start` | 可选子句 `START WITH start` 允许序列从任何位置开始。升序序列的默认起始值为 `minvalue`，降序序列的默认起始值为 `maxvalue`。 |
| `TEMPORARY` 或 `TEMP` | 如果指定了该选项，则序列对象仅在当前会话中存在，并在会话退出时自动删除。临时序列存在时，具有相同名称的现有永久序列在此会话中不可见，除非使用模式限定名称引用。 |

> 序列基于 `BIGINT` 算术，因此范围不能超过八字节整数的范围（-9223372036854775808 到 9223372036854775807）。

## 局限性

由于 DuckDB 依赖管理器的限制，在某些边缘情况下 `DROP SEQUENCE` 会失败。
例如，删除使用序列的列应允许删除序列，但目前会返回错误：

```sql
CREATE SEQUENCE id_sequence START 1;
CREATE TABLE tbl (id INTEGER DEFAULT nextval('id_sequence'), s VARCHAR);

ALTER TABLE tbl DROP COLUMN id;
DROP SEQUENCE id_sequence;
```

```console
依赖错误：
无法删除条目 "id_sequence"，因为有依赖它的条目。
表 "tbl" 依赖于索引 "id_sequence"。
使用 DROP...CASCADE 删除所有依赖项。
```

可以通过使用 `CASCADE` 修饰符来解决此问题。
以下命令删除序列：

```sql
DROP SEQUENCE id_sequence CASCADE;
```