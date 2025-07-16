---
---
layout: docu
redirect_from:
- /docs/internals/pivot
title: Pivot 内部机制
---

## `PIVOT`

[Pivoting]({% link docs/stable/sql/statements/pivot.md %}) 是通过 SQL 查询重写和专用的 `PhysicalPivot` 操作符实现的，以提高性能。
每个 `PIVOT` 都是一组聚合操作，然后通过专用的 `PhysicalPivot` 操作符将这些列表转换为列名和值。
如果在 pivoting 时动态检测要创建的列（这发生在未使用 `IN` 子句时），则需要额外的预处理步骤。

DuckDB 与大多数 SQL 引擎一样，要求在查询开始时就知道所有列名和类型。
为了自动检测由 `PIVOT` 语句创建的列，必须将其转换为多个查询。
[`ENUM` 类型]({% link docs/stable/sql/data_types/enum.md %}) 用于查找应成为列的唯一值。
然后将每个 `ENUM` 注入到 `PIVOT` 语句的 `IN` 子句中。

在 `IN` 子句中填充 `ENUM` 之后，查询将再次重写为一组聚合操作到列表中。

例如：

```sql
PIVOT cities
ON year
USING sum(population);
```

最初会被翻译为：

```sql
CREATE TEMPORARY TYPE __pivot_enum_0_0 AS ENUM (
    SELECT DISTINCT
        year::VARCHAR
    FROM cities
    ORDER BY
        year
    );
PIVOT cities
ON year IN __pivot_enum_0_0
USING sum(population);
```

最后被翻译为：

```sql
SELECT country, name, list(year), list(population_sum)
FROM (
    SELECT country, name, year, sum(population) AS population_sum
    FROM cities
    GROUP BY ALL
)
GROUP BY ALL;
```

这会生成以下结果：

| country |     name      |    list("year")    | list(population_sum) |
|---------|---------------|--------------------|----------------------|
| NL      | Amsterdam     | [2000, 2010, 2020] | [1005, 1065, 1158]   |
| US      | Seattle       | [2000, 2010, 2020] | [564, 608, 738]      |
| US      | New York City | [2000, 2010, 2020] | [8015, 8175, 8772]   |

`PhysicalPivot` 操作符将这些列表转换为列名和值，以返回以下结果：

| country |     name      | 2000 | 2010 | 2020 |
|---------|---------------|-----:|-----:|-----:|
| NL      | Amsterdam     | 1005 | 1065 | 1158 |
| US      | Seattle       | 564  | 608  | 738  |
| US      | New York City | 8015 | 8175 | 8772 |

## `UNPIVOT`

### 内部机制

Unpivoting 完全通过 SQL 查询重写实现。
每个 `UNPIVOT` 都是一组 `unnest` 函数，作用于列名列表和列值列表。
如果进行动态 unpivoting，首先会评估 `COLUMNS` 表达式以计算列列表。

例如：

```sql
UNPIVOT monthly_sales
ON jan, feb, mar, apr, may, jun
INTO
    NAME month
    VALUE sales;
```

会被翻译为：

```sql
SELECT
    empid,
    dept,
    unnest(['jan', 'feb', 'mar', 'apr', 'may', 'jun']) AS month,
    unnest(["jan", "feb", "mar", 'apr', 'may', 'jun']) AS sales
FROM monthly_sales;
```

注意使用单引号来构建文本字符串列表以填充 `month`，并使用双引号来获取列值以用于 `sales`。
这会生成与初始示例相同的结果：

| empid |    dept     | month | sales |
|------:|-------------|-------|------:|
| 1     | electronics | jan   | 1     |
| 1     | electronics | feb   | 2     |
| 1     | electronics | mar   | 3     |
| 1     | electronics | apr   | 4     |
| 1     | electronics | may   | 5     |
| 1     | electronics | jun   | 6     |
| 2     | clothes     | jan   | 10    |
| 2     | clothes     | feb   | 20    |
| 2     | clothes     | mar   | 30    |
| 2     | clothes     | apr   | 40    |
| 2     | clothes     | may   | 50    |
| 2     | clothes     | jun   | 60    |
| 3     | cars        | jan   | 100   |
| 3     | cars        | feb   | 200   |
| 3     | cars        | mar   | 300   |
| 3     | cars        | apr   | 400   |
| 3     | cars        | may   | 500   |
| 3     | cars        | jun   | 600   |