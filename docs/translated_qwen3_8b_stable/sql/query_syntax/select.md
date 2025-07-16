---
---
blurb: SELECT 子句指定了查询将返回的列列表。
layout: docu
railroad: query_syntax/select.js
redirect_from:
- /docs/sql/query_syntax/select
title: SELECT 子句
---

`SELECT` 子句指定了查询将返回的列列表。虽然它在子句中首先出现，但从逻辑上讲，这里的表达式只在最后执行。`SELECT` 子句可以包含任意的表达式，这些表达式可以转换输出，也可以包含聚合函数和窗口函数。

## 示例

从名为 `table_name` 的表中选择所有列：

```sql
SELECT * FROM table_name;
```

对表中的列进行算术运算，并提供别名：

```sql
SELECT col1 + col2 AS res, sqrt(col1) AS root FROM table_name;
```

使用前缀别名：

```sql
SELECT
    res: col1 + col2,
    root: sqrt(col1)
FROM table_name;
```

从 `addresses` 表中选择所有唯一的城市：

```sql
SELECT DISTINCT city FROM addresses;
```

返回 `addresses` 表中行的总数：

```sql
SELECT count(*) FROM addresses;
```

从 `addresses` 表中选择所有列，但排除 `city` 列：

```sql
SELECT * EXCLUDE (city) FROM addresses;
```

从 `addresses` 表中选择所有列，但将 `city` 替换为 `lower(city)`：

```sql
SELECT * REPLACE (lower(city) AS city) FROM addresses;
```

从表中选择所有匹配给定正则表达式的列：

```sql
SELECT COLUMNS('number\d+') FROM addresses;
```

对表中所有给定列计算一个函数：

```sql
SELECT min(COLUMNS(*)) FROM addresses;
```

要选择包含空格或特殊字符的列，请使用双引号 (`"`)：

```sql
SELECT "Some Column Name" FROM tbl;
```

## 语法

<div id="rrdiagram"></div>

## `SELECT` 列表

`SELECT` 子句包含一组表达式，用于指定查询的结果。select 列表可以引用 `FROM` 子句中的任何列，并通过表达式将它们组合起来。由于 SQL 查询的输出是一个表，因此 `SELECT` 子句中的每个表达式都有一个名称。可以使用 `AS` 子句显式地为表达式命名（例如 `expr AS name`）。如果用户没有提供名称，系统会自动为表达式命名。

> 列名是大小写不敏感的。有关大小写敏感性的规则，请参阅 [大小写敏感性规则]({% link docs/stable/sql/dialect/keywords_and_identifiers.md %}#rules-for-case-sensitivity)。

### 星号表达式

从名为 `table_name` 的表中选择所有列：

```sql
SELECT *
FROM table_name;
```

从表中选择所有匹配给定正则表达式的列：

```sql
SELECT COLUMNS('number\d+')
FROM addresses;
```

[星号表达式]({% link docs/stable/sql/expressions/star.md %}) 是一种特殊的表达式，它会根据 `FROM` 子句的内容扩展为多个表达式。在最简单的情况下，`*` 会扩展为 `FROM` 子句中的所有表达式。还可以使用正则表达式或 lambda 函数来选择列。有关更多信息，请参阅 [星号表达式页面]({% link docs/stable/sql/expressions/star.md %})。

### `DISTINCT` 子句

从 `addresses` 表中选择所有唯一的城市：

```sql
SELECT DISTINCT city
FROM addresses;
```

`DISTINCT` 子句可以用来只返回结果中的唯一行，这样任何重复的行都会被过滤掉。

> 以 `SELECT DISTINCT` 开头的查询会执行去重操作，这是一个耗时的操作。因此，只有在必要时才使用 `DISTINCT`。

### `DISTINCT ON` 子句

选择每个国家中人口最高的城市：

```sql
SELECT DISTINCT ON(country) city, population
FROM cities
ORDER BY population DESC;
```

`DISTINCT ON` 子句会根据 `ON` 子句中定义的表达式集合中的每个唯一值返回一行。如果存在 `ORDER BY` 子句，返回的行是根据 `ORDER BY` 条件遇到的第一个行。如果没有 `ORDER BY` 子句，遇到的第一个行未定义，可以是表中的任何行。

> 在查询大型数据集时，对所有列使用 `DISTINCT` 可能很昂贵。因此，考虑在某一列（或一组列）上使用 `DISTINCT ON`，这可以保证结果具有足够的唯一性。例如，在表的关键列（或一组列）上使用 `DISTINCT ON` 可以保证完全的唯一性。

### 聚合函数

返回 `addresses` 表中行的总数：

```sql
SELECT count(*)
FROM addresses;
```

返回按城市分组的 `addresses` 表中行的总数：

```sql
SELECT city, count(*)
FROM addresses
GROUP BY city;
```

[聚合函数]({% link docs/stable/sql/functions/aggregates.md %}) 是一种特殊的函数，它可以将多行组合成一个值。当 `SELECT` 子句中存在聚合函数时，查询将变成聚合查询。在聚合查询中，**所有**表达式必须是聚合函数的一部分，或者属于一个组（如由 [`GROUP BY 子句`]({% link docs/stable/sql/query_syntax/groupby.md %}) 指定的组）。

### 窗口函数

生成一个 `row_number` 列，包含每行的递增标识符：

```sql
SELECT row_number() OVER ()
FROM sales;
```

按时间顺序计算当前金额与前一个金额之间的差值：

```sql
SELECT amount - lag(amount) OVER (ORDER BY time)
FROM sales;
```

[窗口函数]({% link docs/stable/sql/functions/window_functions.md %}) 是一种特殊的函数，允许在结果的 *其他行* 上计算值。窗口函数由 `OVER` 子句标记，该子句包含 *窗口规范*。窗口规范定义了窗口函数计算的框架或上下文。有关更多信息，请参阅 [窗口函数页面]({% link docs/stable/sql/functions/window_functions.md %})。

### `unnest` 函数

将数组展开一层：

```sql
SELECT unnest([1, 2, 3]);
```

将结构展开一层：

```sql
SELECT unnest({'a': 42, 'b': 84});
```

[`unnest`]({% link docs/stable/sql/query_syntax/unnest.md %}) 函数是一种特殊的函数，可以与 [数组]({% link docs/stable/sql/data_types/array.md %})、[列表]({% link docs/stable/sql/data_types/list.md %}) 或 [结构]({% link docs/stable/sql/data_types/struct.md %}) 一起使用。`unnest` 函数会移除类型的一层嵌套。例如，`INTEGER[]` 会转换为 `INTEGER`。`STRUCT(a INTEGER, b INTEGER)` 会转换为 `a INTEGER, b INTEGER`。`unnest` 函数可以将嵌套类型转换为常规的标量类型，这使得它们更容易进行操作。