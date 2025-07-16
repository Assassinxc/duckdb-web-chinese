---
---
blurb: UNPIVOT 语句允许将列堆叠成行，这些行表示先前列的名称和值。
layout: docu
railroad: statements/unpivot.js
redirect_from:
- /docs/sql/statements/unpivot
title: UNPIVOT 语句
---

`UNPIVOT` 语句允许将多个列堆叠成更少的列。
在基本情况下，多个列会被堆叠成两列：一个 `NAME` 列（包含源列的名称）和一个 `VALUE` 列（包含源列的值）。

DuckDB 实现了 SQL 标准的 `UNPIVOT` 语法和一种简化的 `UNPIVOT` 语法。
两者都可以使用 [`COLUMNS` 表达式]({% link docs/stable/sql/expressions/star.md %}#columns) 自动检测要解堆叠的列。
`PIVOT_LONGER` 可以用于替代 `UNPIVOT` 关键字。

有关 `UNPIVOT` 语句的实现细节，请参阅 [Pivot 内部机制页面]({% link docs/stable/internals/pivot.md %}#unpivot)。

> [`PIVOT` 语句]({% link docs/stable/sql/statements/pivot.md %}) 是 `UNPIVOT` 语句的逆操作。

## 简化版 `UNPIVOT` 语法

完整的语法图如下，但简化版的 `UNPIVOT` 语法可以使用电子表格透视表命名约定总结为：

```sql
UNPIVOT ⟨dataset⟩
ON ⟨column(s)⟩
INTO
    NAME ⟨name_column_name⟩
    VALUE ⟨value_column_name(s)⟩
ORDER BY ⟨column(s)_with_order_direction(s)⟩
LIMIT ⟨number_of_rows⟩;
```

### 示例数据

所有示例均使用以下查询生成的数据集：

```sql
CREATE OR REPLACE TABLE monthly_sales
    (empid INTEGER, dept TEXT, Jan INTEGER, Feb INTEGER, Mar INTEGER, Apr INTEGER, May INTEGER, Jun INTEGER);
INSERT INTO monthly_sales VALUES
    (1, 'electronics', 1, 2, 3, 4, 5, 6),
    (2, 'clothes', 10, 20, 30, 40, 50, 60),
    (3, 'cars', 100, 200, 300, 400, 500, 600);
```

```sql
FROM monthly_sales;
```

| empid |    dept     | Jan | Feb | Mar | Apr | May | Jun |
|------:|-------------|----:|----:|----:|----:|----:|----:|
| 1     | electronics | 1   | 2   | 3   | 4   | 5   | 6   |
| 2     | clothes     | 10  | 20  | 30  | 40  | 50  | 60  |
| 3     | cars        | 100 | 200 | 300 | 400 | 500 | 600 |

<!--
    Easiest is to just unpivot all months into their own name/value pair manually.
    Then show the columns-expr version.
    Can also show the quarterly example. -->

### 手动使用 `UNPIVOT`

最常见的 `UNPIVOT` 转换是将已经透视的数据重新堆叠成每列一个名称和值。
在这种情况下，所有月份将被堆叠成 `month` 列和 `sales` 列。

```sql
UNPIVOT monthly_sales
ON jan, feb, mar, apr, may, jun
INTO
    NAME month
    VALUE sales;
```

| empid |    dept     | month | sales |
|------:|-------------|-------|------:|
| 1     | electronics | Jan   | 1     |
| 1     | electronics | Feb   | 2     |
| 1     | electronics | Mar   | 3     |
| 1     | electronics | Apr   | 4     |
| 1     | electronics | May   | 5     |
| 1     | electronics | Jun   | 6     |
| 2     | clothes     | Jan   | 10    |
| 2     | clothes     | Feb   | 20    |
| 2     | clothes     | Mar   | 30    |
| 2     | clothes     | Apr   | 40    |
| 2     | clothes     | May   | 50    |
| 2     | clothes     | Jun   | 60    |
| 3     | cars        | Jan   | 100   |
| 3     | cars        | Feb   | 200   |
| 3     | cars        | Mar   | 300   |
| 3     | cars        | Apr   | 400   |
| 3     | cars        | May   | 500   |
| 3     | cars        | Jun   | 600   |

### 使用列表达式动态执行 `UNPIVOT`

在许多情况下，要解堆叠的列数无法提前确定。
在这个数据集的情况下，每次新增一个月份，上面的查询都需要进行更改。
可以使用 [`COLUMNS` 表达式]({% link docs/stable/sql/expressions/star.md %}#columns-expression) 选择所有不是 `empid` 或 `dept` 的列。
这使得动态解堆叠成为可能，无论添加多少个月份都可以正常工作。
下面的查询返回与上面相同的输出结果。

```sql
UNPIVOT monthly_sales
ON COLUMNS(* EXCLUDE (empid, dept))
INTO
    NAME month
    VALUE sales;
```

| empid |    dept     | month | sales |
|------:|-------------|-------|------:|
| 1     | electronics | Jan   | 1     |
| 1     | electronics | Feb   | 2     |
| 1     | electronics | Mar   | 3     |
| 1     | electronics | Apr   | 4     |
| 1     | electronics | May   | 5     |
| 1     | electronics | Jun   | 6     |
| 2     | clothes     | Jan   | 10    |
| 2     | clothes     | Feb   | 20    |
| 2     | clothes     | Mar   | 30    |
| 2     | clothes     | Apr   | 40    |
| 2     | clothes     | May   | 50    |
| 2     | clothes     | Jun   | 60    |
| 3     | cars        | Jan   | 100   |
| 3     | cars        | Feb   | 200   |
| 3     | cars        | Mar   | 300   |
| 3     | cars        | Apr   | 400   |
| 3     | cars        | May   | 500   |
| 3     | cars        | Jun   | 600   |

### `UNPIVOT` 映射到多个值列

`UNPIVOT` 语句还有额外的灵活性：支持超过 2 个目标列。
这在希望减少数据集的透视程度但不完全堆叠所有透视列时非常有用。
为了演示这一点，下面的查询将生成一个数据集，其中每个季度内各个月份的编号（月份 1、2 或 3）有单独的列，每个季度有单独的行。
由于季度数量少于月份，这使数据集变长，但不如上面的长。

为了实现这一点，`ON` 子句中包含多个列组。
`q1` 和 `q2` 别名是可选的。
`ON` 子句中每个列组的列数必须与 `VALUE` 子句中的列数匹配。

```sql
UNPIVOT monthly_sales
    ON (jan, feb, mar) AS q1, (apr, may, jun) AS q2
    INTO
        NAME quarter
        VALUE month_1_sales, month_2_sales, month_3_sales;
```

| empid |    dept     | quarter | month_1_sales | month_2_sales | month_3_sales |
|------:|-------------|---------|--------------:|--------------:|--------------:|
| 1     | electronics | q1      | 1             | 2             | 3             |
| 1     | electronics | q2      | 4             | 5             | 6             |
| 2     | clothes     | q1      | 10            | 20            | 30            |
| 2     | clothes     | q2      | 40            | 50            | 60            |
| 3     | cars        | q1      | 100           | 200           | 300           |
| 3     | cars        | q2      | 400           | 500           | 600           |

### 在 `SELECT` 语句中使用 `UNPIVOT`

`UNPIVOT` 语句可以作为 CTE（[公共表表达式，或 WITH 子句]({% link docs/stable/sql/query_syntax/with.md %})) 或子查询包含在 `SELECT` 语句中。
这允许 `UNPIVOT` 与其它 SQL 逻辑一起使用，以及在一个查询中使用多个 `UNPIVOT`。

CTE 中不需要 `SELECT`，`UNPIVOT` 关键字可以被认为取而代之。

```sql
WITH unpivot_alias AS (
    UNPIVOT monthly_sales
    ON COLUMNS(* EXCLUDE (empid, dept))
    INTO
        NAME month
        VALUE sales
)
SELECT * FROM unpivot_alias;
```

`UNPIVOT` 可以在子查询中使用，必须用括号括起来。
请注意，这种行为与 SQL 标准的 Unpivot 不同，如后续示例所示。

```sql
SELECT *
FROM (
    UNPIVOT monthly_sales
    ON COLUMNS(* EXCLUDE (empid, dept))
    INTO
        NAME month
        VALUE sales
) unpivot_alias;
```

### 在 `UNPIVOT` 语句中使用表达式

DuckDB 允许在 `UNPIVOT` 语句中使用表达式，前提是它们只涉及一列。这些可以用于执行计算以及 [显式转换]({% link docs/stable/sql/data_types/typecasting.md %}#explicit-casting)。例如：

```sql
UNPIVOT
    (SELECT 42 AS col1, 'woot' AS col2)
    ON
        (col1 * 2)::VARCHAR,
        col2;
```

| name | value |
|------|-------|
| col1 | 84    |
| col2 | woot  |

### 简化版 `UNPIVOT` 完整语法图

下面是 `UNPIVOT` 语句的完整语法图。

<div id="rrdiagram"></div>

## SQL 标准 `UNPIVOT` 语法

完整的语法图如下，但 SQL 标准的 `UNPIVOT` 语法可以总结为：

```sql
FROM [dataset]
UNPIVOT [INCLUDE NULLS] (
    [value-column-name(s)]
    FOR [name-column-name] IN [column(s)]
);
```

请注意，`name-column-name` 表达式中只能包含一个列。

### 使用 SQL 标准 `UNPIVOT` 手动操作

使用 SQL 标准语法完成基本的 `UNPIVOT` 操作，只需做一些简单的添加。

```sql
FROM monthly_sales UNPIVOT (
    sales
    FOR month IN (jan, feb, mar, apr, may, jun)
);
```

| empid |    dept     | month | sales |
|------:|-------------|-------|------:|
| 1     | electronics | Jan   | 1     |
| 1     | electronics | Feb   | 2     |
| 1     | electronics | Mar   | 3     |
| 1     | electronics | Apr   | 4     |
| 1     | electronics | May   | 5     |
| 1     | electronics | Jun   | 6     |
| 2     | clothes     | Jan   | 10    |
| 2     | clothes     | Feb   | 20    |
| 2     | clothes     | Mar   | 30    |
| 2     | clothes     | Apr   | 40    |
| 2     | clothes     | May   | 50    |
| 2     | clothes     | Jun   | 60    |
| 3     | cars        | Jan   | 100   |
| 3     | cars        | Feb   | 200   |
| 3     | cars        | Mar   | 300   |
| 3     | cars        | Apr   | 400   |
| 3     | cars        | May   | 500   |
| 3     | cars        | Jun   | 600   |

### 使用 `COLUMNS` 表达式动态执行 SQL 标准 `UNPIVOT`

[`COLUMNS` 表达式]({% link docs/stable/sql/expressions/star.md %}#columns) 可以用于动态确定 `IN` 列表。
即使在数据集中添加了额外的 `month` 列，它仍然可以正常工作。
它产生的结果与上面的查询相同。

```sql
FROM monthly_sales UNPIVOT (
    sales
    FOR month IN (columns(* EXCLUDE (empid, dept)))
);
```

### SQL 标准 `UNPIVOT` 映射到多个值列

`UNPIVOT` 语句有额外的灵活性：支持超过 2 个目标列。
这在希望减少数据集的透视程度但不完全堆叠所有透视列时非常有用。
为了演示这一点，下面的查询将生成一个数据集，其中每个季度内各个月份的编号（月份 1、2 或 3）有单独的列，每个季度有单独的行。
由于季度数量少于月份，这使数据集变长，但不如上面的长。

为了实现这一点，`UNPIVOT` 语句的 `value-column-name` 部分包含多个列。
`IN` 子句中包含多个列组。
`q1` 和 `q2` 别名是可选的。
`IN` 子句中每个列组的列数必须与 `value-column-name` 部分的列数匹配。

```sql
FROM monthly_sales
UNPIVOT (
    (month_1_sales, month_2_sales, month_3_sales)
    FOR quarter IN (
        (jan, feb, mar) AS q1,
        (apr, may, jun) AS q2
    )
);
```

| empid |    dept     | quarter | month_1_sales | month_2_sales | month_3_sales |
|------:|-------------|---------|--------------:|--------------:|--------------:|
| 1     | electronics | q1      | 1             | 2             | 3             |
| 1     | electronics | q2      | 4             | 5             | 6             |
| 2     | clothes     | q1      | 10            | 20            | 30            |
| 2     | clothes     | q2      | 40            | 50            | 60            |
| 3     | cars        | q1      | 100           | 200           | 300           |
| 3     | cars        | q2      | 400           | 500           | 600           |

### SQL 标准 `UNPIVOT` 完整语法图

下面是 SQL 标准版本的 `UNPIVOT` 语句的完整语法图。

<div id="rrdiagram2"></div>