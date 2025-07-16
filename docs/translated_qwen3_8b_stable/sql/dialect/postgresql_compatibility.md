---
---
layout: docu
redirect_from:
- /docs/sql/postgresl_compatibility
- /docs/sql/postgresl_compatibility/
- /docs/sql/dialect/postgresql_compatibility
title: PostgreSQL 兼容性
---

DuckDB 的 SQL 方言紧密遵循 PostgreSQL 方言的惯例。
以下是一些例外情况，这些例外情况在本页面中列出。

## 浮点数运算

DuckDB 和 PostgreSQL 在处理除以零的浮点数运算时有所不同。DuckDB 遵循 [IEEE 浮点数运算标准（IEEE 754）](https://en.wikipedia.org/wiki/IEEE_754) 来处理除以零和涉及无穷值的操作。PostgreSQL 在除以零时返回错误，但在处理无穷值时与 IEEE 754 保持一致。为了显示这些差异，请运行以下 SQL 查询：

```sql
SELECT 1.0 / 0.0 AS x;
SELECT 0.0 / 0.0 AS x;
SELECT -1.0 / 0.0 AS x;
SELECT 'Infinity'::FLOAT / 'Infinity'::FLOAT AS x;
SELECT 1.0 / 'Infinity'::FLOAT AS x;
SELECT 'Infinity'::FLOAT - 'Infinity'::FLOAT AS x;
SELECT 'Infinity'::FLOAT - 1.0 AS x;
```

<div class="monospace_table"></div>

| 表达式              | PostgreSQL |    DuckDB |  IEEE 754 |
| :------------------ | ---------: | --------: | --------: |
| 1.0 / 0.0           |      error |  Infinity |  Infinity |
| 0.0 / 0.0           |      error |       NaN |       NaN |
| -1.0 / 0.0          |      error | -Infinity | -Infinity |
| 'Infinity' / 'Infinity' |        NaN |       NaN |       NaN |
| 1.0 / 'Infinity'    |        0.0 |       0.0 |       0.0 |
| 'Infinity' - 'Infinity' |        NaN |       NaN |       NaN |
| 'Infinity' - 1.0    |   Infinity |  Infinity |  Infinity |

## 整数除法

在计算整数除法时，PostgreSQL 执行整数除法，而 DuckDB 执行浮点除法：

```sql
SELECT 1 / 2 AS x;
```

PostgreSQL 返回 `0`，而 DuckDB 返回 `0.5`。

要在 DuckDB 中执行整数除法，请使用 `//` 运算符：

```sql
SELECT 1 // 2 AS x;
```

这将返回 `0`。

## 布尔值和整数的 `UNION`

以下查询在 PostgreSQL 中会失败，但在 DuckDB 中可以成功执行：

```sql
SELECT true AS x
UNION
SELECT 2;
```

PostgreSQL 返回错误：

```console
ERROR:  UNION types boolean and integer cannot be matched
```

DuckDB 会执行强制转换，因此可以完成查询并返回以下结果：

|    x |
| ---: |
|    1 |
|    2 |

## 等值检查的隐式转换

DuckDB 在等值检查时会执行隐式转换，例如将字符串转换为数值和布尔值。
因此，有若干实例，PostgreSQL 会抛出错误，而 DuckDB 能够成功计算结果：

<div class="monospace_table"></div>

| 表达式    | PostgreSQL | DuckDB |
| :-------- | ---------- | ------ |
| '1.1' = 1 | error      | true   |
| '1.1' = 1.1 | true       | true   |
| 1 = 1.1 | false      | false  |
| true = 'true' | true       | true   |
| true = 1 | error      | true   |
| 'true' = 1 | error      | error  |

## 引号标识符的大小写敏感性

PostgreSQL 是不区分大小写的。PostgreSQL 通过将未引号的标识符转换为小写来实现不区分大小写，而引号可以保留大小写，例如，以下命令创建了一个名为 `mytable` 的表，但尝试查询 `MyTaBLe`，因为引号保留了大小写。

```sql
CREATE TABLE MyTaBLe (x INTEGER);
SELECT * FROM "MyTaBLe";
```

```console
ERROR:  relation "MyTaBLe" does not exist
```

PostgreSQL 不仅将引号标识符视为大小写敏感，还将其视为大小写敏感，例如，以下命令也不工作：

```sql
CREATE TABLE "PreservedCase" (x INTEGER);
SELECT * FROM PreservedCase;
```

```console
ERROR:  relation "preservedcase" does not exist
```

因此，PostgreSQL 中的不区分大小写仅在不使用不同大小写的引号标识符时才有效。

对于 DuckDB，当与默认大小写敏感的其他工具（如 Parquet、Pandas）交互时，这种行为存在问题——因为所有标识符都会始终被转换为小写。
因此，DuckDB 通过在整个系统中实现完全不区分大小写的标识符，但 [_保留其大小写_]({% link docs/stable/sql/dialect/keywords_and_identifiers.md %}#rules-for-case-sensitivity) 来实现不区分大小写。

在 DuckDB 中，上述脚本可以成功执行：

```sql
CREATE TABLE MyTaBLe (x INTEGER);
SELECT * FROM "MyTaBLe";
CREATE TABLE "PreservedCase" (x INTEGER);
SELECT * FROM PreservedCase;
SELECT table_name FROM duckdb_tables();
```

<div class="monospace_table"></div>

| table_name    |
| ------------- |
| MyTaBLe       |
| PreservedCase |

PostgreSQL 的标识符小写行为可以通过 [`preserve_identifier_case` 选项]({% link docs/stable/configuration/overview.md %}#local-configuration-options) 访问：

```sql
SET preserve_identifier_case = false;
CREATE TABLE MyTaBLe (x INTEGER);
SELECT table_name FROM duckdb_tables();
```

<div class="monospace_table"></div>

| table_name |
| ---------- |
| mytable    |

然而，系统中标识符的不区分大小写匹配无法关闭。

## 使用双等号进行比较

DuckDB 支持 `=` 和 `==` 进行相等性比较，而 PostgreSQL 仅支持 `=`。

```sql
SELECT 1 == 1 AS t;
```

DuckDB 返回 `true`，而 PostgreSQL 返回：

```console
postgres=# SELECT 1 == 1 AS t;
ERROR:  operator does not exist: integer == integer
LINE 1: SELECT 1 == 1 AS t;
```

请注意，使用 `==` 不被推荐，因为其可移植性有限。

## 清理表

在 PostgreSQL 中，`VACUUM` 语句用于清理表并分析表。
在 DuckDB 中，[`VACUUM` 语句]({% link docs/stable/sql/statements/vacuum.md %}) 仅用于重建统计信息。
如需回收空间，请参阅 [“回收空间”页面]({% link docs/stable/operations_manual/footprint_of_duckdb/reclaiming_space.md %}).

## 字符串

自版本 1.3.0 起，DuckDB 在嵌套数据结构中序列化的字符串中转义字符（如 `'`）。
PostgreSQL 不执行此操作。

例如，运行以下命令：

```sql
SELECT ARRAY[''''];
```

PostgreSQL 返回：

```text
{'}
```

DuckDB 返回：

```text
['\'']
```

## 函数

### `regexp_extract` 函数

与 PostgreSQL 的 `regexp_substr` 函数不同，DuckDB 的 `regexp_extract` 在没有匹配时返回空字符串，而不是 `NULL`。

### `to_date` 函数

DuckDB 不支持 [`to_date` PostgreSQL 日期格式化函数](https://www.postgresql.org/docs/17/functions-formatting.html)。
请改用 [`strptime` 函数]({% link docs/stable/sql/functions/dateformat.md %}#strptime-examples)。

## 架构中的类型名称解析

对于 [`CREATE TABLE` 语句]({% link docs/stable/sql/statements/create_table.md %})，DuckDB 会在创建表时尝试解析架构中的类型名称。例如：

```sql
CREATE SCHEMA myschema;
CREATE TYPE myschema.mytype AS ENUM ('as', 'df');
CREATE TABLE myschema.mytable (v mytype);
```

PostgreSQL 在最后一行语句返回错误：

```console
ERROR:  type "mytype" does not exist
LINE 1: CREATE TABLE myschema.mytable (v mytype);
```

DuckDB 执行该语句并成功创建表，通过以下查询可以确认：

```sql
DESCRIBE myschema.mytable;
```

<div class="monospace_table"></div>

| column_name | column_type      | null | key  | default | extra |
| ----------- | ---------------- | ---- | ---- | ------- | ----- |
| v           | ENUM('as', 'df') | YES  | NULL | NULL    | NULL  |

## 利用函数依赖进行 `GROUP BY`

PostgreSQL 可以利用函数依赖，例如在以下查询中 `i -> j`：

```sql
CREATE TABLE tbl (i INTEGER, j INTEGER, PRIMARY KEY (i));
SELECT j
FROM tbl
GROUP BY i;
```

PostgreSQL 运行该查询。

DuckDB 失败：

```console
Binder Error:
column "j" must appear in the GROUP BY clause or must be part of an aggregate function.
Either add it to the GROUP BY list, or use "ANY_VALUE(j)" if the exact value of "j" is not important.
```

为了解决这个问题，请添加其他属性或使用 [`GROUP BY ALL` 子句](https://duckdb.org/docs/sql/query_syntax/groupby#group-by-all)。

## 正则表达式匹配运算符的行为

PostgreSQL 支持 [POSIX 正则表达式匹配运算符]({% link docs/stable/sql/functions/pattern_matching.md %}) `~`（区分大小写的部分正则匹配）和 `~*`（不区分大小写的部分正则匹配），以及它们的否定变体 `!~` 和 `!~*`。

在 DuckDB 中，`~` 等价于 [`regexp_full_match`]({% link docs/stable/sql/functions/text.md %}#regexp_full_matchstring-regex)，而 `!~` 等价于 `NOT regexp_full_match`。运算符 `~*` 和 `!~*` 不被支持。

下表显示了 PostgreSQL 和 DuckDB 中这些函数之间的对应关系几乎不存在。
我们建议在 DuckDB 中避免使用 POSIX 正则表达式匹配运算符。

<div class="monospace_table"></div>

<!-- markdownlint-disable MD056 -->

| 表达式          | PostgreSQL | DuckDB |
| :-------------- | ---------- | ------ |
| `'aaa' ~ '(a|b)'` | true       | false  |
| `'AAA' ~* '(a|b)'` | true       | error  |
| `'aaa' !~ '(a|b)'` | false      | true   |
| `'AAA' !~* '(a|b)'` | false      | error  |

<!-- markdownlint-enable MD056 -->