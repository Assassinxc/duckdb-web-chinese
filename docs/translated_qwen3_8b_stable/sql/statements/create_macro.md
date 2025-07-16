---
---
layout: docu
railroad: statements/createmacro.js
redirect_from:
- /docs/sql/statements/create_macro
title: CREATE MACRO 语句
---

`CREATE MACRO` 语句可以在目录中创建标量或表宏（函数）。
宏只能是单个 `SELECT` 语句（类似于 `VIEW`），但它具有接受参数的优势。

对于标量宏，`CREATE MACRO` 后面是宏的名称，可选参数在括号中。接下来是关键字 `AS`，然后是宏的文本。按设计，标量宏只能返回一个值。
对于表宏，语法与标量宏类似，只是 `AS` 被替换为 `AS TABLE`。表宏可以返回任意大小和形状的表。

> 如果宏是临时的，它只能在同一个数据库连接中使用，并在连接关闭时被删除。

## 示例

### 标量宏

创建一个宏，将两个表达式（`a` 和 `b`）相加：

```sql
CREATE MACRO add(a, b) AS a + b;
```

创建一个宏，替换可能存在的定义：

```sql
CREATE OR REPLACE MACRO add(a, b) AS a + b;
```

如果宏不存在则创建，否则不做任何操作：

```sql
CREATE MACRO IF NOT EXISTS add(a, b) AS a + b;
```

创建一个用于 `CASE` 表达式的宏：

```sql
CREATE MACRO ifelse(a, b, c) AS CASE WHEN a THEN b ELSE c END;
```

创建一个执行子查询的宏：

```sql
CREATE MACRO one() AS (SELECT 1);
```

宏依赖于模式，并具有别名 `FUNCTION`：

```sql
CREATE FUNCTION main.my_avg(x) AS sum(x) / count(x);
```

创建一个带有默认常量参数的宏：

```sql
CREATE MACRO add_default(a, b := 5) AS a + b;
```

创建一个名为 `arr_append` 的宏（功能等同于 `array_append`）：

```sql
CREATE MACRO arr_append(l, e) AS list_concat(l, list_value(e));
```

### 表宏

创建一个没有参数的表宏：

```sql
CREATE MACRO static_table() AS TABLE
    SELECT 'Hello' AS column1, 'World' AS column2;
```

创建一个带有参数的表宏（参数可以是任意类型）：

```sql
CREATE MACRO dynamic_table(col1_value, col2_value) AS TABLE
    SELECT col1_value AS column1, col2_value AS column2;
```

创建一个返回多行的表宏。如果它已经存在，它将被替换，并且它是临时的（连接结束时会自动删除）：

```sql
CREATE OR REPLACE TEMP MACRO dynamic_table(col1_value, col2_value) AS TABLE
    SELECT col1_value AS column1, col2_value AS column2
    UNION ALL
    SELECT 'Hello' AS col1_value, 456 AS col2_value;
```

传递一个列表作为参数：

```sql
CREATE MACRO get_users(i) AS TABLE
    SELECT * FROM users WHERE uid IN (SELECT unnest(i));
```

使用 `get_users` 表宏的一个示例如下：

```sql
CREATE TABLE users AS
    SELECT *
    FROM (VALUES (1, 'Ada'), (2, 'Bob'), (3, 'Carl'), (4, 'Dan'), (5, 'Eve')) t(uid, name);
SELECT * FROM get_users([1, 5]);
```

要在任意表上定义宏，请使用 [`query_table` 函数]({% link docs/stable/guides/sql_features/query_and_query_table_functions.md %})。例如，以下宏计算表的列级校验和：

```sql
CREATE MACRO checksum(table_name) AS TABLE
    SELECT bit_xor(md5_number(COLUMNS(*)::VARCHAR))
    FROM query_table(table_name);

CREATE TABLE tbl AS SELECT unnest([42, 43]) AS x, 100 AS y;
SELECT * FROM checksum('tbl');
```

## 重载

可以根据宏所接受的参数数量对宏进行重载，这适用于标量宏和表宏。

通过提供重载，我们可以同时拥有 `add_x(a, b)` 和 `add_x(a, b, c)` 两个不同的函数体。

```sql
CREATE MACRO add_x
    (a, b) AS a + b,
    (a, b, c) AS a + b + c;
```

```sql
SELECT
    add_x(21, 42) AS two_args,
    add_x(21, 42, 21) AS three_args;
```

| two_args | three_args |
|----------|------------|
|    63    |     84     |

## 语法

<div id="rrdiagram"></div>

宏允许您为表达式的组合创建快捷方式。

```sql
CREATE MACRO add(a) AS a + b;
```

```console
Binder Error:
在 FROM 子句中找不到引用的列 "b"!
```

这可以工作：

```sql
CREATE MACRO add(a, b) AS a + b;
```

使用示例：

```sql
SELECT add(1, 2) AS x;
```

| x |
|--:|
| 3 |

然而，这会失败：

```sql
SELECT add('hello', 3);
```

```console
Binder Error:
无法选择函数调用 "add(STRING_LITERAL, INTEGER_LITERAL)" 的最佳候选函数。为了选择一个，请添加显式的类型转换。
	候选函数：
	add(DATE, INTEGER) -> DATE
	add(INTEGER, INTEGER) -> INTEGER
```

宏可以有默认参数。
与一些语言不同，默认参数在调用宏时必须显式命名。

`b` 是一个默认参数：

```sql
CREATE MACRO add_default(a, b := 5) AS a + b;
```

以下将返回 42：

```sql
SELECT add_default(37);
```

以下将引发错误：

```sql
SELECT add_default(40, 2);
```

```console
Binder Error:
宏函数 'add_default(a)' 需要一个位置参数，但提供了 2 个位置参数。
```

默认参数必须按如下方式使用：

```sql
SELECT add_default(40, b := 2) AS x;
```

| x  |
|---:|
| 42 |

然而，以下会失败：

```sql
SELECT add_default(b := 2, 40);
```

```console
Binder Error:
位置参数不能出现在带有默认值的参数之后!
```

默认参数的顺序无关紧要：

```sql
CREATE MACRO triple_add(a, b := 5, c := 10) AS a + b + c;
```

```sql
SELECT triple_add(40, c := 1, b := 1) AS x;
```

| x  |
|---:|
| 42 |

当使用宏时，它们会被展开（即，用原始表达式替换），并且展开后的表达式中的参数会被替换为提供的参数。逐步说明：

我们上面定义的 `add` 宏用于查询中：

```sql
SELECT add(40, 2) AS x;
```

内部，`add` 会被替换为其定义的 `a + b`：

```sql
SELECT a + b; AS x
```

然后，参数会被替换为提供的参数：

```sql
SELECT 40 + 2 AS x;
```

## 局限性

### 使用命名参数

目前，位置参数只能按位置使用，命名参数只能通过提供其名称来使用。因此，以下操作不会成功：

```sql
CREATE MACRO my_macro(a, b := 42) AS (a + b);
SELECT my_macro(32, 52);
```

```console
Binder Error:
宏函数 'my_macro(a)' 需要一个位置参数，但提供了 2 个位置参数。
```

### 使用子查询宏

如果宏定义为子查询，它不能在表函数中调用。DuckDB 将返回以下错误：

```console
Binder Error:
表函数不能包含子查询
```

### 重载

宏函数的重载必须在创建时设置，不能在不删除原有定义的情况下重复定义同名的宏。

### 递归函数

不支持定义递归函数。
例如，以下宏（旨在计算斐波那契数列的第 *n* 项）会失败：

```sql
CREATE OR REPLACE FUNCTION fibo(n) AS (SELECT 1);
CREATE OR REPLACE FUNCTION fibo(n) AS (
    CASE
        WHEN n <= 1 THEN 1
        ELSE fibo(n - 1)
    END
);
SELECT fibo(3);
```

```console
Binder Error:
最大表达式深度限制为 1000。使用 "SET max_expression_depth TO x" 来增加最大表达式深度。
```