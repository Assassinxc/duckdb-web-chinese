---
---
layout: docu
railroad: expressions/subqueries.js
redirect_from:
- /docs/sql/expressions/subqueries
title: 子查询
---

子查询是括号内的查询表达式，作为更大外层查询的一部分出现。子查询通常基于 `SELECT ... FROM`，但在 DuckDB 中，其他查询构造如 [`PIVOT`]({% link docs/stable/sql/statements/pivot.md %}) 也可以作为子查询出现。

## 标量子查询

<div id="rrdiagram1"></div>

标量子查询是返回单个值的子查询。它们可以在任何可以使用表达式的地方使用。如果标量子查询返回多于一个值，将引发错误（除非将 `scalar_subquery_error_on_multiple_rows` 设置为 `false`，此时会随机选择一行）。

考虑以下表格：

### 成绩

| grade | course |
|---:|:---|
| 7 | Math |
| 9 | Math |
| 8 | CS |

```sql
CREATE TABLE grades (grade INTEGER, course VARCHAR);
INSERT INTO grades VALUES (7, 'Math'), (9, 'Math'), (8, 'CS');
```

我们可以运行以下查询以获取最小成绩：

```sql
SELECT min(grade) FROM grades;
```

| min(grade) |
|-----------:|
| 7          |

通过在 `WHERE` 子句中使用标量子查询，我们可以确定该成绩对应的是哪门课程：

```sql
SELECT course FROM grades WHERE grade = (SELECT min(grade) FROM grades);
```

| course |
|--------|
| Math   |

## 子查询比较：`ALL`、`ANY` 和 `SOME`

在 [标量子查询](#scalar-subquery) 部分，一个标量表达式直接与子查询进行比较，使用了等值 [比较运算符]({% link docs/stable/sql/expressions/comparison_operators.md %}#comparison-operators) (`=`)。
此类直接比较只有在标量子查询中才有意义。

通过指定量词，标量表达式仍可以与返回多行的单列子查询进行比较。可用的量词有 `ALL`、`ANY` 和 `SOME`。`ANY` 和 `SOME` 量词是等价的。

### `ALL`

`ALL` 量词指定当比较表达式左侧的表达式与比较运算符右侧子查询中的每个值进行比较时，所有比较结果都为 `true`，则整体比较结果为 `true`：

```sql
SELECT 6 <= ALL (SELECT grade FROM grades) AS adequate;
```

返回：

| adequate |
|----------|
| true     |

因为 6 小于或等于子查询结果 7、8 和 9 中的每一个。

然而，以下查询

```sql
SELECT 8 >= ALL (SELECT grade FROM grades) AS excellent;
```

返回：

| excellent |
|-----------|
| false     |

因为 8 并不小于或等于子查询结果 7。因此，由于并非所有比较都为 `true`，`>= ALL` 整体上评估为 `false`。

### `ANY`

`ANY` 量词指定只要至少有一个比较结果为 `true`，则整体比较结果为 `true`。
例如：

```sql
SELECT 5 >= ANY (SELECT grade FROM grades) AS fail;
```

返回：

| fail  |
|-------|
| false |

因为子查询中没有结果小于或等于 5。

量词 `SOME` 可以代替 `ANY` 使用：`ANY` 和 `SOME` 是等价的。

## `EXISTS`

<div id="rrdiagram2"></div>

`EXISTS` 运算符用于检测子查询中是否存在任何行。当子查询返回一个或多个记录时返回 `true`，否则返回 `false`。`EXISTS` 运算符通常作为 *相关* 子查询使用，以表达半连接操作。然而，它也可以作为不相关子查询使用。

例如，我们可以使用它来判断某个课程是否有成绩：

```sql
SELECT EXISTS (FROM grades WHERE course = 'Math') AS math_grades_present;
```

| math_grades_present |
|--------------------:|
| true                |

```sql
SELECT EXISTS (FROM grades WHERE course = 'History') AS history_grades_present;
```

| history_grades_present |
|-----------------------:|
| false                  |

> 上述示例中的子查询利用了 DuckDB 中可以省略 `SELECT *` 的 [`FROM`-first 语法]({% link docs/stable/sql/query_syntax/from.md %})。其他 SQL 系统在子查询中需要 `SELECT` 子句，但在 `EXISTS` 和 `NOT EXISTS` 子查询中无法发挥任何作用。

### `NOT EXISTS`

`NOT EXISTS` 运算符用于检测子查询中是否没有任何行。当子查询返回空结果时返回 `true`，否则返回 `false`。`NOT EXISTS` 运算符通常作为 *相关* 子查询使用以表达反连接操作。例如，查找没有兴趣的 Person 节点：

```sql
CREATE TABLE Person (id BIGINT, name VARCHAR);
CREATE TABLE interest (PersonId BIGINT, topic VARCHAR);

INSERT INTO Person VALUES (1, 'Jane'), (2, 'Joe');
INSERT INTO interest VALUES (2, 'Music');

SELECT *
FROM Person
WHERE NOT EXISTS (FROM interest WHERE interest.PersonId = Person.id);
```

| id | name |
|---:|------|
| 1  | Jane |

> DuckDB 会自动检测 `NOT EXISTS` 查询是否表示反连接操作。无需手动将此类查询重写为使用 `LEFT OUTER JOIN ... WHERE ... IS NULL`。

## `IN` 运算符

<div id="rrdiagram3"></div>

`IN` 运算符检查左侧表达式是否包含在由子查询或右侧（RHS）表达式集合定义的结果中。如果表达式存在于 RHS 中，`IN` 运算符返回 `true`；如果表达式不存在于 RHS 中且 RHS 没有 `NULL` 值，则返回 `false`；如果表达式不存在于 RHS 中且 RHS 包含 `NULL` 值，则返回 `NULL`。

我们可以以与使用 `EXISTS` 运算符类似的方式使用 `IN` 运算符：

```sql
SELECT 'Math' IN (SELECT course FROM grades) AS math_grades_present;
```

| math_grades_present |
|--------------------:|
| true                |

## 相关子查询

到目前为止，所有展示的子查询都是 **不相关** 子查询，其中子查询本身是完全自包含的，并且可以在没有父查询的情况下运行。还存在一种称为 **相关** 子查询的第二种类型的子查询。对于相关子查询，子查询使用来自父查询的值。

从概念上讲，子查询会在父查询的每一行上运行一次。或许一个简单的方法是将相关子查询视为应用于源数据集中每一行的 **函数**。

例如，假设我们想要找到每门课程的最低成绩。我们可以这样做：

```sql
SELECT *
FROM grades grades_parent
WHERE grade =
    (SELECT min(grade)
     FROM grades
     WHERE grades.course = grades_parent.course);
```

| grade | course |
|------:|--------|
| 7     | Math   |
| 8     | CS     |

子查询使用了父查询中的一个列（`grades_parent.course`）。从概念上讲，我们可以将子查询视为一个函数，其中相关列是该函数的参数：

```sql
SELECT min(grade)
FROM grades
WHERE course = ?;
```

现在，当我们对每一行执行此函数时，可以看到对于 `Math`，它将返回 `7`，对于 `CS`，它将返回 `8`。我们然后将它与该实际行的成绩进行比较。因此，行 `(Math, 9)` 将被过滤掉，因为 `9 <> 7`。

## 将子查询的每一行返回为结构

在 `SELECT` 子句中使用子查询的名称（不引用特定列）会将子查询的每一行转换为一个结构，其字段对应于子查询的列。例如：

```sql
SELECT t
FROM (SELECT unnest(generate_series(41, 43)) AS x, 'hello' AS y) t;
```

<div class="monospace_table"></div>

|           t           |
|-----------------------|
| {'x': 41, 'y': hello} |
| {'x': 42, 'y': hello} |
| {'x': 43, 'y': hello} |