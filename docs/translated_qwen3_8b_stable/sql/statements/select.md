---
---
blurb: SELECT 语句从数据库中检索行。
layout: docu
railroad: statements/select.js
redirect_from:
- /docs/sql/statements/select
title: SELECT 语句
---

`SELECT` 语句从数据库中检索行。

### 示例

从表 `tbl` 中选择所有列：

```sql
SELECT * FROM tbl;
```

从 `tbl` 中选择行：

```sql
SELECT j FROM tbl WHERE i = 3;
```

按列 `i` 进行聚合操作：

```sql
SELECT i, sum(j) FROM tbl GROUP BY i;
```

从 `tbl` 中选择前 3 行：

```sql
SELECT * FROM tbl ORDER BY i DESC LIMIT 3;
```

使用 `USING` 子句将两个表连接在一起：

```sql
SELECT * FROM t1 JOIN t2 USING (a, b);
```

使用列索引选择表 `tbl` 中的第一列和第三列：

```sql
SELECT #1, #3 FROM tbl;
```

从地址表中选择所有唯一的城市：

```sql
SELECT DISTINCT city FROM addresses;
```

使用行变量返回一个 `STRUCT`：

```sql
SELECT d
FROM (SELECT 1 AS a, 2 AS b) d;
```

### 语法

`SELECT` 语句从数据库中检索行。`SELECT` 语句的标准顺序如下，不常见的子句会缩进显示：

```sql
SELECT ⟨select_list⟩
FROM ⟨tables⟩
    USING SAMPLE ⟨sample_expression⟩
WHERE ⟨condition⟩
GROUP BY ⟨groups⟩
HAVING ⟨group_filter⟩
    WINDOW ⟨window_expression⟩
    QUALIFY ⟨qualify_filter⟩
ORDER BY ⟨order_expression⟩
LIMIT ⟨n⟩;
```

`SELECT` 语句可选择性地以 [`WITH` 子句]({% link docs/stable/sql/query_syntax/with.md %}) 开头。

由于 `SELECT` 语句非常复杂，我们将语法图拆分为几个部分。完整的语法图可在页面底部找到。

## `SELECT` 子句

<div id="rrdiagram3"></div>

[`SELECT` 子句]({% link docs/stable/sql/query_syntax/select.md %}) 指定查询将返回的列列表。虽然它在子句中首先出现，但从逻辑上讲，此处的表达式只在最后执行。`SELECT` 子句可以包含任意表达式，用于转换输出，以及聚合函数和窗口函数。`DISTINCT` 关键字确保只返回唯一的元组。

> 列名是大小写不敏感的。有关大小写敏感性的详细信息，请参阅 [大小写敏感性规则]({% link docs/stable/sql/dialect/keywords_and_identifiers.md %}#rules-for-case-sensitivity)。

## `FROM` 子句

<div id="rrdiagram4"></div>

[`FROM` 子句]({% link docs/stable/sql/query_syntax/from.md %}) 指定查询其余部分应操作的数据来源。从逻辑上讲，`FROM` 子句是查询开始执行的地方。`FROM` 子句可以包含一个表、多个组合表（这些表被连接在一起），或者一个子查询节点中的另一个 `SELECT` 查询。

## `SAMPLE` 子句

<div id="rrdiagram10"></div>

[`SAMPLE` 子句]({% link docs/stable/sql/query_syntax/sample.md %}) 允许你对基础表的样本运行查询。这可以显著加快查询处理速度，但以牺牲结果的准确性为代价。样本还可以用于快速查看数据集的快照。`SAMPLE` 子句在 `FROM` 子句中的任何内容之后应用（即在任何连接之后，但在 `WHERE` 子句或任何聚合之前）。有关更多信息，请参阅 [样本]({% link docs/stable/sql/samples.md %}) 页面。

## `WHERE` 子句

<div id="rrdiagram5"></div>

[`WHERE` 子句]({% link docs/stable/sql/query_syntax/where.md %}) 指定要应用于数据的任何过滤条件。这允许你只选择感兴趣的数据子集。从逻辑上讲，`WHERE` 子句在 `FROM` 子句之后立即应用。

## `GROUP BY` 和 `HAVING` 子句

<div id="rrdiagram6"></div>

[`GROUP BY` 子句]({% link docs/stable/sql/query_syntax/groupby.md %}) 指定用于在 `SELECT` 子句中进行任何聚合的分组列。如果指定了 `GROUP BY` 子句，查询始终是聚合查询，即使 `SELECT` 子句中没有聚合。

## `WINDOW` 子句

<div id="rrdiagram7"></div>

[`WINDOW` 子句]({% link docs/stable/sql/query_syntax/window.md %}) 允许你指定可在窗口函数中使用的命名窗口。当你有多个窗口函数时，它们非常有用，因为它们可以避免重复相同的窗口子句。

## `QUALIFY` 子句

<div id="rrdiagram11"></div>

[`QUALIFY` 子句]({% link docs/stable/sql/query_syntax/qualify.md %}) 用于过滤 [`WINDOW` 函数]({% link docs/stable/sql/functions/window_functions.md %}) 的结果。

## `ORDER BY`、`LIMIT` 和 `OFFSET` 子句

<div id="rrdiagram8"></div>

[`ORDER BY`]({% link docs/stable/sql/query_syntax/orderby.md %})、[`LIMIT` 和 `OFFSET`]({% link docs/stable/sql/query_syntax/limit.md %}) 是输出修饰符。从逻辑上讲，它们在查询的最后应用。`ORDER BY` 子句根据排序条件对行进行升序或降序排序。`LIMIT` 子句限制获取的行数，而 `OFFSET` 子句指示从哪个位置开始读取值。

## `VALUES` 列表

<div id="rrdiagram9"></div>

[A `VALUES` 列表]({% link docs/stable/sql/query_syntax/values.md %}) 是一个值集合，用于替代 `SELECT` 语句。

## 行 ID

对于每个表，[`rowid` 虚拟列](https://docs.oracle.com/cd/B19306_01/server.102/b14200/pseudocolumns008.htm) 根据物理存储返回行标识符。

```sql
CREATE TABLE t (id INTEGER, content VARCHAR);
INSERT INTO t VALUES (42, 'hello'), (43, 'world');
SELECT rowid, id, content FROM t;
```

| rowid | id | content |
|------:|---:|---------|
| 0     | 42 | hello   |
| 1     | 43 | world   |

在当前存储中，这些标识符是连续的无符号整数（0, 1, ...），如果未删除任何行。删除会引入 rowid 中的间隙，这些间隙可能在以后被重新回收：

```sql
CREATE OR REPLACE TABLE t AS (FROM range(10) r(i));
DELETE FROM t WHERE i % 2 = 0;
SELECT rowid FROM t;
```

| rowid |
|------:|
| 1     |
| 3     |
| 5     |
| 7     |
| 9     |

`rowid` 值在事务内是稳定的。

> 最佳实践 不建议使用 rowid 作为标识符。

> 如果存在一个用户定义的列名为 `rowid`，它会遮蔽 `rowid` 虚拟列。

## 公共表表达式

<div id="rrdiagram2"></div>

## 完整语法图

以下是 `SELECT` 语句的完整语法图：

<div id="rrdiagram"></div>