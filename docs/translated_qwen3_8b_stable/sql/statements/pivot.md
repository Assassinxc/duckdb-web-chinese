---
---
blurb: PIVOT 语句允许将某一列中的值拆分成各自的列。
layout: docu
railroad: statements/pivot.js
redirect_from:
- /docs/sql/statements/pivot
title: PIVOT 语句
---

`PIVOT` 语句允许将某一列中的不同值拆分成各自的列。
这些新列中的值是通过在匹配每个不同值的行子集上使用聚合函数计算得出的。

DuckDB 实现了 SQL 标准的 `PIVOT` 语法以及一种简化版的 `PIVOT` 语法，该语法在进行透视时会自动检测要创建的列。
`PIVOT_WIDER` 可以用于替代 `PIVOT` 关键字。

有关 `PIVOT` 语句实现的详细信息，请参阅 [Pivot 内部机制页面]({% link docs/stable/internals/pivot.md %}#pivot)。

> [`UNPIVOT` 语句]({% link docs/stable/sql/statements/unpivot.md %}) 是 `PIVOT` 语句的逆操作。

## 简化版 `PIVOT` 语法

完整的语法图如下所示，但简化版的 `PIVOT` 语法可以使用电子表格透视表的命名约定进行总结：

```sql
PIVOT ⟨dataset⟩
ON ⟨columns⟩
USING ⟨values⟩
GROUP BY ⟨rows⟩
ORDER BY ⟨columns_with_order_directions⟩
LIMIT ⟨number_of_rows⟩;
```

`ON`、`USING` 和 `GROUP BY` 子句都是可选的，但它们不能全部省略。

### 示例数据

所有示例都使用以下查询生成的数据集：

```sql
CREATE TABLE cities (
    country VARCHAR, name VARCHAR, year INTEGER, population INTEGER
);
INSERT INTO cities VALUES
    ('NL', 'Amsterdam', 2000, 1005),
    ('NL', 'Amsterdam', 2010, 1065),
    ('NL', 'Amsterdam', 2020, 1158),
    ('US', 'Seattle', 2000, 564),
    ('US', 'Seattle', 2010, 608),
    ('US', 'Seattle', 2020, 738),
    ('US', 'New York City', 2000, 8015),
    ('US', 'New York City', 2010, 8175),
    ('US', 'New York City', 2020, 8772);
```

```sql
SELECT *
FROM cities;
```

| country |     name      | year | population |
|---------|---------------|-----:|-----------:|
| NL      | Amsterdam     | 2000 | 1005       |
| NL      | Amsterdam     | 2010 | 1065       |
| NL      | Amsterdam     | 2020 | 1158       |
| US      | Seattle       | 2000 | 564        |
| US      | Seattle       | 2010 | 608        |
| US      | Seattle       | 2020 | 738        |
| US      | New York City | 2000 | 8015       |
| US      | New York City | 2010 | 8175       |
| US      | New York City | 2020 | 8772       |

### `PIVOT ON` 和 `USING`

使用以下 `PIVOT` 语句为每个年份创建一个单独的列，并计算每个年份的总人口。
`ON` 子句指定要拆分成单独列的列。
它等同于电子表格透视表中的列参数。

`USING` 子句决定了如何对拆分成单独列的值进行聚合。
这等同于电子表格透视表中的值参数。
如果未包含 `USING` 子句，默认为 `count(*)`。

```sql
PIVOT cities
ON year
USING sum(population);
```

| country |     name      | 2000 | 2010 | 2020 |
|---------|---------------|-----:|-----:|-----:|
| NL      | Amsterdam     | 1005 | 1065 | 1158 |
| US      | Seattle       | 564  | 608  | 738  |
| US      | New York City | 8015 | 8175 | 8772 |

在上面的示例中，`sum` 聚合函数始终作用于单个值。
如果我们只是想改变数据的显示方向而不进行聚合，可以使用 `first` 聚合函数。
在本例中，我们对数值进行透视，但 `first` 函数在对文本列进行透视时也非常有效。
（这是在电子表格透视表中难以实现的操作，但在 DuckDB 中却非常容易！）

此查询生成的结果与上面相同：

```sql
PIVOT cities
ON year
USING first(population);
```

> 注意 SQL 语法允许在 `USING` 子句中使用 [`FILTER` 子句]({% link docs/stable/sql/query_syntax/filter.md %}) 与聚合函数。
> 在 DuckDB 中，`PIVOT` 语句目前不支持这些子句，它们会被静默忽略。

### `PIVOT ON`、`USING` 和 `GROUP BY`

默认情况下，`PIVOT` 语句保留未在 `ON` 或 `USING` 子句中指定的列。
若要仅包含某些列并进一步聚合，请在 `GROUP BY` 子句中指定列。
这等同于电子表格透视表中的行参数。

在下面的示例中，`name` 列不再包含在输出中，数据被聚合到 `country` 层级。

```sql
PIVOT cities
ON year
USING sum(population)
GROUP BY country;
```

| country | 2000 | 2010 | 2020 |
|---------|-----:|-----:|-----:|
| NL      | 1005 | 1065 | 1158 |
| US      | 8579 | 8783 | 9510 |

### `ON` 子句的 `IN` 过滤器

要只为 `ON` 子句中某一列中的特定值创建单独的列，使用可选的 `IN` 表达式。
例如，假设我们想出于某种原因忽略 2020 年的数据...

```sql
PIVOT cities
ON year IN (2000, 2010)
USING sum(population)
GROUP BY country;
```

| country | 2000 | 2010 |
|---------|-----:|-----:|
| NL      | 1005 | 1065 |
| US      | 8579 | 8783 |

### 每个子句的多个表达式

可以在 `ON` 和 `GROUP BY` 子句中指定多个列，并且可以在 `USING` 子句中包含多个聚合表达式。

#### 多个 `ON` 列和 `ON` 表达式

可以将多个列透视为各自的列。
DuckDB 会在每个 `ON` 子句的列中查找不同的值，并为这些值的所有组合（笛卡尔积）创建一个新列。

在下面的示例中，所有唯一的国家和城市的组合都获得各自的列。
某些组合可能不在底层数据中，因此这些列会被填充为 `NULL` 值。

```sql
PIVOT cities
ON country, name
USING sum(population);
```

| year | NL_Amsterdam | NL_New York City | NL_Seattle | US_Amsterdam | US_New York City | US_Seattle |
|-----:|-------------:|------------------|------------|--------------|-----------------:|-----------:|
| 2000 | 1005         | NULL             | NULL       | NULL         | 8015             | 564        |
| 2010 | 1065         | NULL             | NULL       | NULL         | 8175             | 608        |
| 2020 | 1158         | NULL             | NULL       | NULL         | 8772             | 738        |

要仅对底层数据中存在的值的组合进行透视，使用 `ON` 子句中的表达式。
可以提供多个表达式和/或列。

在此示例中，`country` 和 `name` 被连接在一起，每个连接结果都会获得自己的列。
任何非聚合的任意表达式都可以使用。
在此情况下，使用下划线连接以模仿 `PIVOT` 子句在提供多个 `ON` 列时使用的命名约定（如前面的示例所示）。

```sql
PIVOT cities
ON country || '_' || name
USING sum(population);
```

| year | NL_Amsterdam | US_New York City | US_Seattle |
|-----:|-------------:|-----------------:|-----------:|
| 2000 | 1005         | 8015             | 564        |
| 2010 | 1065         | 8175             | 608        |
| 2020 | 1158         | 8772             | 738        |

#### 多个 `USING` 表达式

可以在 `USING` 子句中的每个表达式中包含别名。
它将被附加到生成的列名后，用下划线 (`_`) 分隔。
当 `USING` 子句中包含多个表达式时，这会使列命名约定更加清晰。

在下面的示例中，对人口列的 `sum` 和 `max` 都被计算，并拆分成各自的列。

```sql
PIVOT cities
ON year
USING sum(population) AS total, max(population) AS max
GROUP BY country;
```

| country | 2000_total | 2000_max | 2010_total | 2010_max | 2020_total | 2020_max |
|---------|-----------:|---------:|-----------:|---------:|-----------:|---------:|
| US      | 8579       | 8015     | 8783       | 8175     | 9510       | 8772     |
| NL      | 1005       | 1005     | 1065       | 1065     | 1158       | 1158     |

#### 多个 `GROUP BY` 列

也可以提供多个 `GROUP BY` 列。
请注意，必须使用列名而非列位置（1, 2 等），并且 `GROUP BY` 子句不支持表达式。

```sql
PIVOT cities
ON year
USING sum(population)
GROUP BY country, name;
```

| country |     name      | 2000 | 2010 | 2020 |
|---------|---------------|-----:|-----:|-----:|
| NL      | Amsterdam     | 1005 | 1065 | 1158 |
| US      | Seattle       | 564  | 608  | 738  |
| US      | New York City | 8015 | 8175 | 8772 |

### 在 `SELECT` 语句中使用 `PIVOT`

`PIVOT` 语句可以作为 CTE（[公共表表达式，或 `WITH` 子句]({% link docs/stable/sql/query_syntax/with.md %}）或子查询包含在 `SELECT` 语句中。
这允许在 `PIVOT` 与其它 SQL 逻辑一起使用，以及在一个查询中使用多个 `PIVOT`。

CTE 中不需要 `SELECT`，`PIVOT` 关键字可以被视为取其位置。

```sql
WITH pivot_alias AS (
    PIVOT cities
    ON year
    USING sum(population)
    GROUP BY country
)
SELECT * FROM pivot_alias;
```

`PIVOT` 可以用在子查询中，并且必须用括号括起来。
请注意，这种行为与 SQL 标准的 `PIVOT` 不同，如后续示例所示。

```sql
SELECT *
FROM (
    PIVOT cities
    ON year
    USING sum(population)
    GROUP BY country
) pivot_alias;
```

### 多个 `PIVOT` 语句

每个 `PIVOT` 都可以被视为 `SELECT` 节点，因此它们可以被连接在一起或以其他方式操作。

例如，如果两个 `PIVOT` 语句共享相同的 `GROUP BY` 表达式，可以使用 `GROUP BY` 子句中的列进行连接，生成一个更宽的透视。

```sql
SELECT *
FROM (PIVOT cities ON year USING sum(population) GROUP BY country) year_pivot
JOIN (PIVOT cities ON name USING sum(population) GROUP BY country) name_pivot
USING (country);
```

| country | 2000 | 2010 | 2020 | Amsterdam | New York City | Seattle |
|---------|-----:|-----:|-----:|----------:|--------------:|--------:|
| NL      | 1005 | 1065 | 1158 | 3228      | NULL          | NULL    |
| US      | 8579 | 8783 | 9510 | NULL      | 24962         | 1910    |

## 简化版 `PIVOT` 完整语法图

下面是 `PIVOT` 语句的完整语法图。

<div id="rrdiagram"></div>

## SQL 标准 `PIVOT` 语法

完整的语法图如下所示，但 SQL 标准的 `PIVOT` 语法可以总结为：

```sql
SELECT *
FROM ⟨dataset⟩
PIVOT (
    ⟨values⟩
    FOR
        ⟨column_1⟩ IN (⟨in_list⟩)
        ⟨column_2⟩ IN (⟨in_list⟩)
        ...
    GROUP BY ⟨rows⟩
);
```

与简化语法不同，每个被透视的列必须指定 `IN` 子句。
如果您对动态透视感兴趣，推荐使用简化语法。

请注意，在 `FOR` 子句中，表达式之间没有逗号分隔，但 `value` 和 `GROUP BY` 表达式必须用逗号分隔！

## 示例

此示例使用一个值表达式、一个列表达式和一个行表达式：

```sql
SELECT *
FROM cities
PIVOT (
    sum(population)
    FOR
        year IN (2000, 2010, 2020)
    GROUP BY country
);
```

| country | 2000 | 2010 | 2020 |
|---------|-----:|-----:|-----:|
| NL      | 1005 | 1065 | 1158 |
| US      | 8579 | 8783 | 9510 |

此示例有些牵强，但展示了如何在 `FOR` 子句中使用多个值表达式和多个列。

```sql
SELECT *
FROM cities
PIVOT (
    sum(population) AS total,
    count(population) AS count
    FOR
        year IN (2000, 2010)
        country IN ('NL', 'US')
);
```

|     name      | 2000_NL_total | 2000_NL_count | 2000_US_total | 2000_US_count | 2010_NL_total | 2010_NL_count | 2010_US_total | 2010_US_count |
|--|-:|-:|-:|-:|-:|-:|-:|-:|
| Amsterdam     | 1005          | 1             | NULL          | 0             | 1065          | 1             | NULL          | 0             |
| Seattle       | NULL          | 0             | 564           | 1             | NULL          | 0             | 608           | 1             |
| New York City | NULL          | 0             | 8015          | 1             | NULL          | 0             | 8175          | 1             |

### SQL 标准 `PIVOT` 完整语法图

下面是 SQL 标准版本的 `PIVOT` 语句的完整语法图。

<div id="rrdiagram2"></div>

## 局限性

`PIVOT` 目前仅接受聚合函数，表达式是不允许的。
例如，以下查询试图将人口表示为人数而不是千人（即，而不是 564，得到 564000）：

```sql
PIVOT cities
ON year
USING sum(population) * 1000;
```

然而，它会报错：

```console
Catalog Error:
* is not an aggregate function
```

要解决这个限制，首先仅使用聚合函数进行 `PIVOT`，然后使用 [`COLUMNS` 表达式]({% link docs/stable/sql/expressions/star.md %}#columns-expression)：

```sql
SELECT country, name, 1000 * COLUMNS(* EXCLUDE (country, name))
FROM (
    PIVOT cities
    ON year
    USING sum(population)
);
```