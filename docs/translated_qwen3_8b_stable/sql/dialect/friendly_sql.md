---
---
layout: docu
redirect_from:
- /docs/guides/sql_features/friendly_sql
- /docs/guides/sql_features/friendly_sql/
- /docs/sql/dialect/friendly_sql
title: 友好 SQL
---

DuckDB 提供了多种高级 SQL 特性以及语法糖，使 SQL 查询更加简洁。我们通常称这些特性为“友好 SQL”。

> 其中一些功能也支持其他系统，而有些功能（目前）仅限于 DuckDB。

## 子句

* 创建表和插入数据：
    * [`CREATE OR REPLACE TABLE`]({% link docs/stable/sql/statements/create_table.md %}#create-or-replace)：避免在脚本中使用 `DROP TABLE IF EXISTS` 语句。
    * [`CREATE TABLE ... AS SELECT` (CTAS)]({% link docs/stable/sql/statements/create_table.md %}#create-table--as-select-ctas)：从表的输出创建一个新表，无需手动定义模式。
    * [`INSERT INTO ... BY NAME`]({% link docs/stable/sql/statements/insert.md %}#insert-into--by-name)：此 `INSERT` 变体允许使用列名而不是位置。
    * [`INSERT OR IGNORE INTO ...`]({% link docs/stable/sql/statements/insert.md %}#insert-or-ignore-into)：插入不会导致由于 `UNIQUE` 或 `PRIMARY KEY` 约束冲突的行。
    * [`INSERT OR REPLACE INTO ...`]({% link docs/stable/sql/statements/insert.md %}#insert-or-replace-into)：插入不会导致由于 `UNIQUE` 或 `PRIMARY KEY` 约束冲突的行。对于那些导致冲突的行，将现有行的列替换为新插入行的新值。
* 描述表和计算统计信息：
    * [`DESCRIBE`]({% link docs/stable/guides/meta/describe.md %})：提供表或查询模式的简洁摘要。
    * [`SUMMARIZE`]({% link docs/stable/guides/meta/summarize.md %})：返回表或查询的摘要统计信息。
* 使 SQL 子句更紧凑和可读：
    * [`FROM`-first 语法，可选 `SELECT` 子句]({% link docs/stable/sql/query_syntax/from.md %}#from-first-syntax)：DuckDB 允许使用 `FROM tbl` 形式查询，选择所有列（执行 `SELECT *` 语句）。
    * [`GROUP BY ALL`]({% link docs/stable/sql/query_syntax/groupby.md %}#group-by-all)：通过从 `SELECT` 子句中列出的属性推断来省略分组列。
    * [`ORDER BY ALL`]({% link docs/stable/sql/query_syntax/orderby.md %}#order-by-all)：对所有列进行排序的简写（例如，以确保确定性结果）。
    * [`SELECT * EXCLUDE`]({% link docs/stable/sql/expressions/star.md %}#exclude-clause)：`EXCLUDE` 选项允许从 `*` 表达式中排除特定列。
    * [`SELECT * REPLACE`]({% link docs/stable/sql/expressions/star.md %}#replace-clause)：`REPLACE` 选项允许在 `*` 表达式中用不同的表达式替换特定列。
    * [`UNION BY NAME`]({% link docs/stable/sql/query_syntax/setops.md %}#union-all-by-name)：按列名执行 `UNION` 操作（而不是依赖位置）。
    * [`SELECT` 和 `FROM` 子句中的前缀别名]({% link docs/stable/sql/query_syntax/select.md %})：用 `x: 42` 替代 `42 AS x` 以提高可读性。
* 转换表：
    * [`PIVOT`]({% link docs/stable/sql/statements/pivot.md %})：将长表转换为宽表。
    * [`UNPIVOT`]({% link docs/stable/sql/statements/unpivot.md %})：将宽表转换为长表。
* 定义 SQL 级别变量：
    * [`SET VARIABLE`]({% link docs/stable/sql/statements/set.md %}#set-variable)
    * [`RESET VARIABLE`]({% link docs/stable/sql/statements/set.md %}#reset-variable)

## 查询特性

* [`WHERE`、`GROUP BY` 和 `HAVING` 中的列别名]({% post_url 2022-05-04-friendlier-sql %}#column-aliases-in-where--group-by--having)。（注意，列别名不能在 [`JOIN` 子句]({% link docs/stable/sql/query_syntax/from.md %}#joins) 的 `ON` 子句中使用。）
* [`COLUMNS()` 表达式]({% link docs/stable/sql/expressions/star.md %}#columns-expression) 可用于对多个列执行相同的表达式：
    * [使用正则表达式]({% post_url 2023-08-23-even-friendlier-sql %}#columns-with-regular-expressions)
    * [使用 `EXCLUDE` 和 `REPLACE`]({% post_url 2023-08-23-even-friendlier-sql %}#columns-with-exclude-and-replace)
    * [使用 lambda 函数]({% post_url 2023-08-23-even-friendlier-sql %}#columns-with-lambda-functions)
* 可重用的列别名（也称为“横向列别名”），例如：`SELECT i + 1 AS j, j + 2 AS k FROM range(0, 3) t(i)`
* 高级聚合功能用于分析（OLAP）查询：
    * [`FILTER` 子句]({% link docs/stable/sql/query_syntax/filter.md %})
    * [`GROUPING SETS`、`GROUP BY CUBE`、`GROUP BY ROLLUP` 子句]({% link docs/stable/sql/query_syntax/grouping_sets.md %})
* [`count()` 简写]({% link docs/stable/sql/functions/aggregates.md %}) 用于 `count(*)`
* [`IN` 操作符用于列表和映射]({% link docs/stable/sql/expressions/in.md %})
* [为公共表表达式 (`WITH`) 指定列名]({% link docs/stable/sql/query_syntax/with.md %}#basic-cte-examples)
* [在 `JOIN` 子句中指定列名]({% link docs/stable/sql/query_syntax/from.md %}#shorthands-in-the-join-clause)
* [在 `JOIN` 子句中使用 `VALUES`]({% link docs/stable/sql/query_syntax/from.md %}#shorthands-in-the-join-clause)
* [在公共表表达式的锚点部分使用 `VALUES`]({% link docs/stable/sql/query_syntax/with.md %}#using-values)

## 字面量和标识符

* [在目录中保持实体大小写的同时忽略大小写]({% link docs/stable/sql/dialect/keywords_and_identifiers.md %}#case-sensitivity-of-identifiers)
* [去重标识符]({% link docs/stable/sql/dialect/keywords_and_identifiers.md %}#deduplicating-identifiers)
* [在数字字面量中使用下划线作为数字分隔符]({% link docs/stable/sql/dialect/keywords_and_identifiers.md %}#numeric-literals)

## 数据类型

* [`MAP` 数据类型]({% link docs/stable/sql/data_types/map.md %})
* [`UNION` 数据类型]({% link docs/stable/sql/data_types/union.md %})

## 数据导入

* [自动检测 CSV 文件的标题和模式]({% link docs/stable/data/csv/auto_detection.md %})
* 直接查询 [CSV 文件]({% link docs/stable/data/csv/overview.md %}) 和 [Parquet 文件]({% link docs/stable/data/parquet/overview.md %})
* [替换扫描]({% link docs/stable/guides/glossary.md %})：
    * 可以使用 `FROM 'my.csv'`、`FROM 'my.csv.gz'`、`FROM 'my.parquet'` 等语法从文件加载数据。
    * 在 Python 中，可以使用 `FROM df` [访问 Pandas 数据框]({% link docs/stable/guides/python/export_pandas.md %}).
* [文件名扩展（globbing）]({% link docs/stable/sql/functions/pattern_matching.md %}#globbing)，例如：`FROM 'my-data/part-*.parquet'`

## 函数和表达式

* [函数链的点操作符]({% link docs/stable/sql/functions/overview.md %}#function-chaining-via-the-dot-operator)：`SELECT ('hello').upper()`
* 字符串格式化器：
    * [`fmt` 语法的 `format()` 函数]({% link docs/stable/sql/functions/text.md %}#fmt-syntax)
    * [`printf()` 函数]({% link docs/stable/sql/functions/text.md %}#printf-syntax)
* [列表推导]({% post_url 2023-08-23-even-friendlier-sql %}#list-comprehensions)
* [列表切片]({% post_url 2022-05-04-friendlier-sql %}#string-slicing) 和从后索引（`[-1]`）
* [字符串切片]({% post_url 2022-05-04-friendlier-sql %}#string-slicing)
* [`STRUCT.*` 符号]({% post_url 2022-05-04-friendlier-sql %}#struct-dot-notation)
* [使用方括号创建 `LIST`]({% link docs/stable/sql/data_types/list.md %}#creating-lists)
* [简单的 `LIST` 和 `STRUCT` 创建]({% post_url 2022-05-04-friendlier-sql %}#simple-list-and-struct-creation)
* [更新 `STRUCT` 的模式]({% link docs/stable/sql/data_types/struct.md %}#updating-the-schema)

## 连接类型

* [`ASOF` 连接]({% link docs/stable/sql/query_syntax/from.md %}#as-of-joins)
* [`LATERAL` 连接]({% link docs/stable/sql/query_syntax/from.md %}#lateral-joins)
* [`POSITIONAL` 连接]({% link docs/stable/sql/query_syntax/from.md %}#positional-joins)

## 尾随逗号

DuckDB 允许 [尾随逗号](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Trailing_commas)，
无论是在列举实体（例如列名和表名）时，还是在构建 [`LIST` 项]({% link docs/stable/sql/data_types/list.md %}#creating-lists) 时。
例如，以下查询有效：

```sql
SELECT
    42 AS x,
    ['a', 'b', 'c',] AS y,
    'hello world' AS z,
;
```

## “组内前 N” 查询

在 SQL 中，计算“组内前 N 行”根据某些标准排序是一个常见任务，但不幸的是，这通常需要使用窗口函数和/或子查询的复杂查询。

为了帮助完成这个任务，DuckDB 提供了聚合函数 [`max(arg, n)`]({% link docs/stable/sql/functions/aggregates.md %}#maxarg-n)、[`min(arg, n)`]({% link docs/stable/sql/functions/aggregates.md %}#minarg-n)、[`arg_max(arg, val, n)`]({% link docs/stable/sql/functions/aggregates.md %}#arg_maxarg-val-n)、[`arg_min(arg, val, n)`]({% link docs/stable/sql/functions/aggregates.md %}#arg_minarg-val-n)、[`max_by(arg, val, n)`]({% link docs/stable/sql/functions/aggregates.md %}#max_byarg-val-n) 和 [`min_by(arg, val, n)`]({% link docs/stable/sql/functions/aggregates.md %}#min_byarg-val-n)，以高效地根据组内特定列的升序或降序返回“前”`n` 行。

例如，使用以下表：

```sql
SELECT * FROM t1;
```

```text
┌─────────┬───────┐
│   grp   │  val  │
│ varchar │ int32 │
├─────────┼───────┤
│ a       │     2 │
│ a       │     1 │
│ b       │     5 │
│ b       │     4 │
│ a       │     3 │
│ b       │     6 │
└─────────┴───────┘
```

我们希望获取每个组 `grp` 中的前 3 个 `val` 值。传统方法是使用子查询中的窗口函数：

```sql
SELECT array_agg(rs.val), rs.grp
FROM
    (SELECT val, grp, row_number() OVER (PARTITION BY grp ORDER BY val DESC) AS rid
    FROM t1 ORDER BY val DESC) AS rs
WHERE rid < 4
GROUP BY rs.grp;
```

```text
┌───────────────────┬─────────┐
│ array_agg(rs.val) │   grp   │
│      int32[]      │ varchar │
├───────────────────┼─────────┤
│ [3, 2, 1]         │ a       │
│ [6, 5, 4]         │ b       │
└───────────────────┴─────────┘
```

但在 DuckDB 中，我们可以更简洁（且更高效）地完成：

```sql
SELECT max(val, 3) FROM t1 GROUP BY grp;
```

```text
┌─────────────┐
│ max(val, 3) │
│   int32[]   │
├─────────────┤
│ [3, 2, 1]   │
│ [6, 5, 4]   │
└─────────────┘
```

## 相关博客文章

* [“DuckDB 中更友好的 SQL”]({% post_url 2022-05-04-friendlier-sql %}) 博客文章
* [“DuckDB 中更加友好的 SQL”]({% post_url 2023-08-23-even-friendlier-sql %}) 博客文章
* [“SQL 炼金术：将 SQL 弯曲成灵活的新形状”]({% post_url 2024-03-01-sql-gymnastics %}) 博客文章
---