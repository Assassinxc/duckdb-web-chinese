---
---
layout: docu
railroad: statements/createtable.js
redirect_from:
- /docs/sql/statements/create_table
title: CREATE TABLE 语句
---

`CREATE TABLE` 语句用于在目录中创建表。

## 示例

创建一个包含两个整数列（`i` 和 `j`）的表：

```sql
CREATE TABLE t1 (i INTEGER, j INTEGER);
```

创建一个带有主键的表：

```sql
CREATE TABLE t1 (id INTEGER PRIMARY KEY, j VARCHAR);
```

创建一个带有复合主键的表：

```sql
CREATE TABLE t1 (id INTEGER, j VARCHAR, PRIMARY KEY (id, j));
```

创建一个包含各种不同类型和约束的表：

```sql
CREATE TABLE t1 (
    i INTEGER NOT NULL,
    decimalnr DOUBLE CHECK (decimalnr < 10),
    date DATE UNIQUE,
    time TIMESTAMP
);
```

使用 `CREATE TABLE ... AS SELECT`（CTAS）创建表：

```sql
CREATE TABLE t1 AS
    SELECT 42 AS i, 84 AS j;
```

从 CSV 文件创建表（自动检测列名和类型）：

```sql
CREATE TABLE t1 AS
    SELECT *
    FROM read_csv('path/file.csv');
```

我们可以使用 `FROM`-first 语法省略 `SELECT *`：

```sql
CREATE TABLE t1 AS
    FROM read_csv('path/file.csv');
```

将 `t2` 的模式复制到 `t1`：

```sql
CREATE TABLE t1 AS
    FROM t2
    LIMIT 0;
```

请注意，只有列名和类型会被复制到 `t2`，其他信息（索引、约束、默认值等）不会被复制。

## 临时表

可以使用 `CREATE TEMP TABLE` 或 `CREATE TEMPORARY TABLE` 语句创建临时表（见下图）。
临时表是会话作用域的（例如类似于 PostgreSQL），这意味着只有创建它们的特定连接可以访问它们，一旦与 DuckDB 的连接关闭，它们将被自动删除。
临时表驻留在内存中而非磁盘上（即使连接到持久化 DuckDB 也是如此），但如果在连接时设置了 `temp_directory` [配置]({% link docs/stable/configuration/overview.md %}) 或使用 `SET` 命令设置，当内存受限时，数据会溢出到磁盘上。

从 CSV 文件创建一个临时表（自动检测列名和类型）：

```sql
CREATE TEMP TABLE t1 AS
    SELECT *
    FROM read_csv('path/file.csv');
```

允许临时表将多余内存转储到磁盘：

```sql
SET temp_directory = '/path/to/directory/';
```

临时表属于 `temp.main` 模式。虽然不建议，但它们的名称可以与常规数据库表的名称重叠。在这种情况下，请使用其完全限定名称，例如 `temp.main.t1` 进行区分。

## `CREATE OR REPLACE`

`CREATE OR REPLACE` 语法允许创建新表或用新表覆盖现有表。这相当于先删除现有表，然后再创建新表。

即使 `t1` 已经存在，也可以创建一个包含两个整数列（`i` 和 `j`）的表：

```sql
CREATE OR REPLACE TABLE t1 (i INTEGER, j INTEGER);
```

## `IF NOT EXISTS`

`IF NOT EXISTS` 语法只有在表不存在时才会执行创建操作。如果表已经存在，则不会执行任何操作，现有表将保留在数据库中。

仅在 `t1` 不存在时创建包含两个整数列（`i` 和 `j`）的表：

```sql
CREATE TABLE IF NOT EXISTS t1 (i INTEGER, j INTEGER);
```

## `CREATE TABLE ... AS SELECT` (CTAS)

DuckDB 支持 `CREATE TABLE ... AS SELECT` 语法，也称为“CTAS”：

```sql
CREATE TABLE nums AS
    SELECT i
    FROM range(0, 3) t(i);
```

此语法可以与 [CSV 读取器]({% link docs/stable/data/csv/overview.md %})、直接从 CSV 文件读取的简写方式、[`FROM`-first 语法]({% link docs/stable/sql/query_syntax/from.md %}) 以及 [HTTP(S) 支持]({% link docs/stable/core_extensions/httpfs/https.md %}) 结合使用，从而产生如下简洁的 SQL 命令：

```sql
CREATE TABLE flights AS
    FROM 'https://duckdb.org/data/flights.csv';
```

CTAS 构造也可以与 `OR REPLACE` 修饰符结合使用，产生 `CREATE OR REPLACE TABLE ... AS` 语句：

```sql
CREATE OR REPLACE TABLE flights AS
    FROM 'https://duckdb.org/data/flights.csv';
```

### 复制模式

您可以按照以下方式创建表的模式副本（仅列名和类型）：

```sql
CREATE TABLE t1 AS
    FROM t2
    WITH NO DATA;
```

或者：

```sql
CREATE TABLE t1 AS
    FROM t2
    LIMIT 0;
```

无法使用 CTAS 语句创建带有约束（主键、检查约束等）的表。

## 检查约束

`CHECK` 约束是必须由表中每一行的值满足的表达式。

```sql
CREATE TABLE t1 (
    id INTEGER PRIMARY KEY,
    percentage INTEGER CHECK (0 <= percentage AND percentage <= 100)
);
INSERT INTO t1 VALUES (1, 5);
INSERT INTO t1 VALUES (2, -1);
```

```console
约束错误：
CHECK 约束失败: t1
```

```sql
INSERT INTO t1 VALUES (3, 101);
```

```console
约束错误：
CHECK 约束失败: t1
```

```sql
CREATE TABLE t2 (id INTEGER PRIMARY KEY, x INTEGER, y INTEGER CHECK (x < y));
INSERT INTO t2 VALUES (1, 5, 10);
INSERT INTO t2 VALUES (2, 5, 3);
```

```console
约束错误：
CHECK 约束失败: t2
```

`CHECK` 约束也可以作为 `CONSTRAINTS` 子句的一部分添加：

```sql
CREATE TABLE t3 (
    id INTEGER PRIMARY KEY,
    x INTEGER,
    y INTEGER,
    CONSTRAINT x_smaller_than_y CHECK (x < y)
);
INSERT INTO t3 VALUES (1, 5, 10);
INSERT INTO t3 VALUES (2, 5, 3);
```

```console
约束错误：
CHECK 约束失败: t3
```

## 外键约束

`FOREIGN KEY` 是一个列（或一组列），它引用另一个表的主键。外键检查参照完整性，即在插入时，被引用的主键必须存在于其他表中。

```sql
CREATE TABLE t1 (id INTEGER PRIMARY KEY, j VARCHAR);
CREATE TABLE t2 (
    id INTEGER PRIMARY KEY,
    t1_id INTEGER,
    FOREIGN KEY (t1_id) REFERENCES t1 (id)
);
```

示例：

```sql
INSERT INTO t1 VALUES (1, 'a');
INSERT INTO t2 VALUES (1, 1);
INSERT INTO t2 VALUES (2, 2);
```

```console
约束错误：
违反外键约束，因为键 "id: 2" 不存在于被引用的表中
```

外键可以定义在复合主键上：

```sql
CREATE TABLE t3 (id INTEGER, j VARCHAR, PRIMARY KEY (id, j));
CREATE TABLE t4 (
    id INTEGER PRIMARY KEY, t3_id INTEGER, t3_j VARCHAR,
    FOREIGN KEY (t3_id, t3_j) REFERENCES t3(id, j)
);
```

示例：

```sql
INSERT INTO t3 VALUES (1, 'a');
INSERT INTO t4 VALUES (1, 1, 'a');
INSERT INTO t4 VALUES (2, 1, 'b');
```

```console
约束错误：
违反外键约束，因为键 "id: 1, j: b" 不存在于被引用的表中
```

外键也可以定义在唯一列上：

```sql
CREATE TABLE t5 (id INTEGER UNIQUE, j VARCHAR);
CREATE TABLE t6 (
    id INTEGER PRIMARY KEY,
    t5_id INTEGER,
    FOREIGN KEY (t5_id) REFERENCES t5(id)
);
```

### 限制

外键有以下限制。

不支持带有级联删除的外键（`FOREIGN KEY ... REFERENCES ... ON DELETE CASCADE`）。

向具有自引用外键的表中插入数据目前不被支持，并会产生以下错误：

```console
约束错误：
违反外键约束，因为键 "..." 不存在于被引用的表中。
```

## 生成列

`[type] [GENERATED ALWAYS] AS (expr) [VIRTUAL|STORED]` 语法会创建一个生成列。这种列中的数据由其表达式生成，该表达式可以引用表中的其他（常规或生成）列。由于它们是通过计算生成的，这些列不能直接插入数据。

DuckDB 可以根据表达式的返回类型推断生成列的类型。这允许你在声明生成列时省略类型。虽然可以显式设置类型，但如果引用列的类型无法转换为生成列的类型，插入操作可能会失败。

生成列有两种类型：`VIRTUAL` 和 `STORED`。
虚拟生成列的数据不会存储在磁盘上，而是每次引用该列时（通过 SELECT 语句）从表达式中重新计算。

存储生成列的数据会存储在磁盘上，并在其依赖数据发生变化时（通过 INSERT / UPDATE / DROP 语句）重新计算。

目前仅支持 `VIRTUAL` 类型，并且如果最后一个字段未填写，它也是默认选项。

生成列的最简单语法：

类型由表达式推断，变体默认为 `VIRTUAL`：

```sql
CREATE TABLE t1 (x FLOAT, two_x AS (2 * x));
```

完整指定相同的生成列：

```sql
CREATE TABLE t1 (x FLOAT, two_x FLOAT GENERATED ALWAYS AS (2 * x) VIRTUAL);
```

## 语法

<div id="rrdiagram"></div>

---