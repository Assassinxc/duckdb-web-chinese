---
---
layout: docu
railroad: expressions/window.js
redirect_from:
- /docs/sql/window_functions
- /docs/sql/window_functions/
- /docs/sql/functions/window_functions
title: 窗口函数
---

<!-- markdownlint-disable MD001 -->

DuckDB 支持 [窗口函数](https://en.wikipedia.org/wiki/Window_function_(SQL))，这些函数可以使用多行来为每一行计算一个值。
窗口函数是 [阻塞操作符]({% link docs/stable/guides/performance/how_to_tune_workloads.md %}#blocking-operators)，即它们需要对其整个输入进行缓冲，因此是 SQL 中最耗内存的操作符之一。

窗口函数自 [SQL:2003](https://en.wikipedia.org/wiki/SQL:2003) 起在 SQL 中可用，并且被主要的 SQL 数据库系统所支持。

## 示例

生成一个 `row_number` 列以枚举行：

```sql
SELECT row_number() OVER ()
FROM sales;
```

> 提示 如果您只需要为表中的每一行生成一个数字，可以使用 [`rowid` 虚拟列]({% link docs/stable/sql/statements/select.md %}#row-ids)。

生成一个 `row_number` 列以枚举行，按 `time` 排序：

```sql
SELECT row_number() OVER (ORDER BY time)
FROM sales;
```

生成一个 `row_number` 列以枚举行，按 `time` 排序并按 `region` 分区：

```sql
SELECT row_number() OVER (PARTITION BY region ORDER BY time)
FROM sales;
```

计算当前行与前一行（按 `time` 排序）的 `amount` 之间的差值：

```sql
SELECT amount - lag(amount) OVER (ORDER BY time)
FROM sales;
```

计算每行 `region` 的 `amount` 总额的百分比：

```sql
SELECT amount / sum(amount) OVER (PARTITION BY region)
FROM sales;
```

## 语法

<div id="rrdiagram"></div>

窗口函数只能在 `SELECT` 子句中使用。要共享 `OVER` 规范，使用语句的 [`WINDOW` 子句]({% link docs/stable/sql/query_syntax/window.md %}) 并使用 `OVER ⟨window_name⟩`{:.language-sql .highlight} 语法。

## 通用窗口函数

下表显示了可用的通用窗口函数。

| 名称 | 描述 |
|:--|:-------|
| [`cume_dist([ORDER BY ordering])`](#cume_distorder-by-ordering) | 累计分布：(分区中当前行之前的行数或与当前行相同行数) / 分区总行数。 |
| [`dense_rank()`](#dense_rank) | 当前行的排名 *无间隔*；此函数统计同组行。 |
| [`first_value(expr[ ORDER BY ordering][ IGNORE NULLS])`](#first_valueexpr-order-by-ordering-ignore-nulls) | 返回 `expr` 在窗口框架中第一行的值（如果设置了 `IGNORE NULLS`，则为 `expr` 非空值的第一行）。 |
| [`lag(expr[, offset[, default]][ ORDER BY ordering][ IGNORE NULLS])`](#lagexpr-offset-default-order-by-ordering-ignore-nulls) | 返回 `expr` 在窗口框架中 `offset` 行（如果设置了 `IGNORE NULLS`，则为 `expr` 非空值的行）前的值；如果没有这样的行，则返回 `default`（`expr` 必须与 `default` 类型相同）。`offset` 和 `default` 都是相对于当前行计算的。如果省略，`offset` 默认为 `1`，`default` 默认为 `NULL`。 |
| [`last_value(expr[ ORDER BY ordering][ IGNORE NULLS])`](#last_valueexpr-order-by-ordering-ignore-nulls) | 返回 `expr` 在窗口框架中最后一行的值（如果设置了 `IGNORE NULLS`，则为 `expr` 非空值的最后一行）。 |
| [`lead(expr[, offset[, default]][ ORDER BY ordering][ IGNORE NULLS])`](#leadexpr-offset-default-order-by-ordering-ignore-nulls) | 返回 `expr` 在窗口框架中 `offset` 行后（如果设置了 `IGNORE NULLS`，则为 `expr` 非空值的行）的值；如果没有这样的行，则返回 `default`（`expr` 必须与 `default` 类型相同）。`offset` 和 `default` 都是相对于当前行计算的。如果省略，`offset` 默认为 `1`，`default` 默认为 `NULL`。 |
| [`nth_value(expr, nth[ ORDER BY ordering][ IGNORE NULLS])`](#nth_valueexpr-nth-order-by-ordering-ignore-nulls) | 返回 `expr` 在窗口框架中第 `nth` 行（如果设置了 `IGNORE NULLS`，则为 `expr` 非空值的行）的值（从 1 开始计数）；如果没有这样的行，则返回 `NULL`。 |
| [`ntile(num_buckets[ ORDER BY ordering])`](#ntilenum_buckets-order-by-ordering) | 一个整数，从 1 到 `num_buckets`，尽可能均匀地划分分区。 |
| [`percent_rank([ORDER BY ordering])`](#percent_rankorder-by-ordering) | 当前行的相对排名：`(rank() - 1) / (总分区行数 - 1)`。 |
| [`rank_dense()`](#rank_dense) | 当前行的排名 *无间隔*。 |
| [`rank([ORDER BY ordering])`](#rankorder-by-ordering) | 当前行的排名 *有间隔*；与它的第一个同组行的 `row_number` 相同。 |
| [`row_number([ORDER BY ordering])`](#row_numberorder-by-ordering) | 当前行在分区中的编号，从 1 开始计数。 |

#### `cume_dist([ORDER BY ordering])`

<div class="nostroke_table"></div>

| **描述** | 累计分布：(分区中当前行之前或相同行数) / 分区总行数。如果指定了 `ORDER BY` 子句，则使用提供的排序来计算分布，而不是框架排序。 |
| **返回类型** | `DOUBLE` |
| **示例** | `cume_dist()` |

#### `dense_rank()`

<div class="nostroke_table"></div>

| **描述** | 当前行的排名 *无间隔*；此函数统计同组行。 |
| **返回类型** | `BIGINT` |
| **示例** | `dense_rank()` |
| **别名** | `rank_dense()` |

#### `first_value(expr[ ORDER BY ordering][ IGNORE NULLS])`

<div class="nostroke_table"></div>

| **描述** | 返回 `expr` 在窗口框架中的第一行的值（如果设置了 `IGNORE NULLS`，则为 `expr` 非空值的第一行）。如果指定了 `ORDER BY` 子句，则使用提供的排序来计算第一行编号，而不是框架排序。 |
| **返回类型** | 与 `expr` 相同的类型 |
| **示例** | `first_value(column)` |

#### `lag(expr[, offset[, default]][ ORDER BY ordering][ IGNORE NULLS])`

<div class="nostroke_table"></div>

| **描述** | 返回 `expr` 在窗口框架中 `offset` 行（如果设置了 `IGNORE NULLS`，则为 `expr` 非空值的行）前的值；如果没有这样的行，则返回 `default`（`expr` 必须与 `default` 类型相同）。`offset` 和 `default` 都是相对于当前行计算的。如果省略，`offset` 默认为 `1`，`default` 默认为 `NULL`。如果指定了 `ORDER BY` 子句，则使用提供的排序来计算滞后行编号，而不是框架排序。 |
| **返回类型** | 与 `expr` 相同的类型 |
| **别名** | `lag(column, 3, 0)` |

#### `last_value(expr[ ORDER BY ordering][ IGNORE NULLS])`

<div class="nostroke_table"></div>

| **描述** | 返回 `expr` 在窗口框架中的最后一行的值（如果设置了 `IGNORE NULLS`，则为 `expr` 非空值的最后一行）。如果省略，`offset` 默认为 `1`，`default` 默认为 `NULL`。如果指定了 `ORDER BY` 子句，则使用提供的排序来计算最后一行，而不是框架排序。 |
| **返回类型** | 与 `expr` 相同的类型 |
| **示例** | `last_value(column)` |

#### `lead(expr[, offset[, default]][ ORDER BY ordering][ IGNORE NULLS])`

<div class="nostroke_table"></div>

| **描述** | 返回 `expr` 在窗口框架中 `offset` 行后（如果设置了 `IGNORE NULLS`，则为 `expr` 非空值的行）的值；如果没有这样的行，则返回 `default`（`expr` 必须与 `default` 类型相同）。`offset` 和 `default` 都是相对于当前行计算的。如果省略，`offset` 默认为 `1`，`default` 默认为 `NULL`。如果指定了 `ORDER BY` 子句，则使用提供的排序来计算领先行编号，而不是框架排序。 |
| **返回类型** | 与 `expr` 相同的类型 |
| **别名** | `lead(column, 3, 0)` |

#### `nth_value(expr, nth[ ORDER BY ordering][ IGNORE NULLS])`

<div class="nostroke_table"></div>

| **描述** | 返回 `expr` 在窗口框架中第 `nth` 行（如果设置了 `IGNORE NULLS`，则为 `expr` 非空值的行）的值（从 1 开始计数）；如果没有这样的行，则返回 `NULL`。如果指定了 `ORDER BY` 子句，则使用提供的排序来计算第 `nth` 行编号，而不是框架排序。 |
| **返回类型** | 与 `expr` 相同的类型 |
| **别名** | `nth_value(column, 2)` |

#### `ntile(num_buckets[ ORDER BY ordering])`

<div class="nostroke_table"></div>

| **描述** | 一个整数，从 1 到 `num_buckets`，尽可能均匀地划分分区。如果指定了 `ORDER BY` 子句，则使用提供的排序来计算 ntile，而不是框架排序。 |
| **返回类型** | `BIGINT` |
| **示例** | `ntile(4)` |

#### `percent_rank([ORDER BY ordering])`

<div class="nostroke_table"></div>

| **描述** | 当前行的相对排名：`(rank() - 1) / (总分区行数 - 1)`。如果指定了 `ORDER BY` 子句，则使用提供的排序来计算相对排名，而不是框架排序。 |
| **返回类型** | `DOUBLE` |
| **示例** | `percent_rank()` |

#### `rank_dense()`

<div class="nostroke_table"></div>

| **描述** | 当前行的排名 *无间隔*。 |
| **返回类型** | `BIGINT` |
| **示例** | `rank_dense()` |
| **别名** | `dense_rank()` |

#### `rank([ORDER BY ordering])`

<div class="nostroke_table"></div>

| **描述** | 当前行的排名 *有间隔*；与它的第一个同组行的 `row_number` 相同。如果指定了 `ORDER BY` 子句，则使用提供的排序来计算排名，而不是框架排序。 |
| **返回类型** | `BIGINT` |
| **示例** | `rank()` |

#### `row_number([ORDER BY ordering])`

<div class="nostroke_table"></div>

| **描述** | 当前行在分区中的编号，从 1 开始计数。如果指定了 `ORDER BY` 子句，则使用提供的排序来计算行号，而不是框架排序。 |
| **返回类型** | `BIGINT` |
| **示例** | `row_number()` |

## 聚合窗口函数

所有 [聚合函数]({% link docs/stable/sql/functions/aggregates.md %}) 都可以用于窗口上下文中，包括可选的 [`FILTER` 子句]({% link docs/stable/sql/query_syntax/filter.md %}).
`first` 和 `last` 聚合函数被相应的通用窗口函数所覆盖，其较小的后果是这些函数不支持 `FILTER` 子句，但支持 `IGNORE NULLS`。

## DISTINCT 参数

所有聚合窗口函数都支持使用 `DISTINCT` 子句来处理参数。当 `DISTINCT` 子句提供时，仅考虑不同的值进行聚合计算。这通常与 `COUNT` 聚合函数一起使用以获取不同元素的数量；但也可以与系统中的任何聚合函数一起使用。有些聚合函数对重复值不敏感（例如 `min`、`max`），对于这些函数，该子句会被解析但忽略。

```sql
-- 计算某一时间点的唯一用户数量
SELECT count(DISTINCT name) OVER (ORDER BY time) FROM sales;
-- 将这些唯一用户合并成一个列表
SELECT list(DISTINCT name) OVER (ORDER BY time) FROM sales;
```

## ORDER BY 参数

所有聚合窗口函数都支持使用一个 *不同于* 窗口排序的 `ORDER BY` 参数子句。当 `ORDER BY` 参数子句提供时，在应用函数之前会先对聚合值进行排序。通常这不是很重要，但有些对排序敏感的聚合函数可能会产生不确定的结果（例如，`mode`、`list` 和 `string_agg`）。这些可以通过对参数进行排序使其变得确定。对于对排序不敏感的聚合函数，该子句会被解析并忽略。

```sql
-- 计算每个时间点的众值，打破平局以最近的值为优
SELECT mode(value ORDER BY time DESC) OVER (ORDER BY time) FROM sales;
```

SQL 标准没有提供使用 `ORDER BY` 与通用窗口函数结合的方法，但我们已经扩展了所有这些函数（除了 `dense_rank`），以接受此语法并使用框架来限制次要排序的应用范围。

```sql
-- 比较每位运动员在比赛中的时间与目前的最好成绩
SELECT event, date, athlete, time
    first_value(time ORDER BY time DESC) OVER w AS record_time,
    first_value(athlete ORDER BY time DESC) OVER w AS record_athlete,
FROM meet_results
WINDOW w AS (PARTITION BY event ORDER BY datetime)
ORDER BY ALL
```

请注意，参数和 `ORDER BY` 子句之间没有逗号分隔。

## 空值

所有 [通用窗口函数](#general-purpose-window-functions)（接受 `IGNORE NULLS` 的）默认尊重空值。这种默认行为可以通过 `RESPECT NULLS` 显式声明。

相反，所有 [聚合窗口函数](#aggregate-window-functions)（除了 `list` 及其别名，可以通过 `FILTER` 忽略空值）忽略空值，并且不接受 `RESPECT NULLS`。例如，`sum(column) OVER (ORDER BY time) AS cumulativeColumn` 计算一个累积和，其中 `column` 为 `NULL` 的行具有与前一行相同的 `cumulativeColumn` 值。

## 评估

窗口操作通过将关系分成独立的 *分区*，
*对这些分区进行排序*，
然后为每一行计算一个新列，该列是附近值的函数。
一些窗口函数仅依赖于分区边界和排序，
但一些（包括所有聚合函数）还使用 *框架*。
框架是定义为当前行两侧（*preceding* 或 *following*）的行数。
距离可以指定为行数，
或使用分区排序值和距离的值范围，
或指定为组数（具有相同排序值的行集）。

完整的语法在页面顶部的图表中显示，
并且该图表视觉上展示了计算环境：

<img src="/images/framing.png" alt="窗口计算环境" title="图 1: 窗口计算环境" style="max-width:90%;width:90%;height:auto"/>

### 分区和排序

分区将关系分成独立、无关的部分。
分区是可选的，如果未指定，则将整个关系视为一个分区。
窗口函数无法访问包含当前行的分区以外的值。

排序也是可选的，但没有排序时，[通用窗口函数](#general-purpose-window-functions) 和 [排序敏感的聚合函数]({% link docs/stable/sql/functions/aggregates.md %}#order-by-clause-in-aggregate-functions) 以及 [框架](#framing) 的顺序是不明确的。
每个分区都使用相同的排序子句。

以下是可用作 CSV 文件的发电数据表（[`power-plant-generation-history.csv`](/data/power-plant-generation-history.csv)）。要加载数据，请运行：

```sql
CREATE TABLE "Generation History" AS
    FROM 'power-plant-generation-history.csv';
```

在按电厂和按日期排序后，它将具有如下布局：

| 电厂 | 日期 | MWh |
|:---|:---|---:|
| 波士顿 | 2019-01-02 | 564337 |
| 波士顿 | 2019-01-03 | 507405 |
| 波士顿 | 2019-01-04 | 528523 |
| 波士顿 | 2019-01-05 | 469538 |
| 波士顿 | 2019-01-06 | 474163 |
| 波士顿 | 2019-01-07 | 507213 |
| 波士顿 | 2019-01-08 | 613040 |
| 波士顿 | 2019-01-09 | 582588 |
| 波士顿 | 2019-01-10 | 499506 |
| 波士顿 | 2019-01-11 | 482014 |
| 波士顿 | 2019-01-12 | 486134 |
| 波士顿 | 2019-01-13 | 531518 |
| 罗斯福 | 2019-01-02 | 118860 |
| 罗斯福 | 2019-01-03 | 101977 |
| 罗斯福 | 2019-01-04 | 106054 |
| 罗斯福 | 2019-01-05 | 92182 |
| 罗斯福 | 2019-01-06 | 94492 |
| 罗斯福 | 2019-01-07 | 99932 |
| 罗斯福 | 2019-01-08 | 118854 |
| 罗斯福 | 2019-01-09 | 113506 |
| 罗斯福 | 2019-01-10 | 96644 |
| 罗斯福 | 2019-01-11 | 93806 |
| 罗斯福 | 2019-01-12 | 98963 |
| 罗斯,福 | 2019-01-13 | 107170 |

在接下来的内容中，
我们将使用这个表（或其中的小部分）来说明窗口函数评估的不同方面。

最简单的窗口函数是 `row_number()`。
该函数仅使用查询计算分区中的 1 基行号：

```sql
SELECT
    "Plant",
    "Date",
    row_number() OVER (PARTITION BY "Plant" ORDER BY "Date") AS "Row"
FROM "Generation History"
ORDER BY 1, 2;
```

结果将如下所示：

| 电厂 | 日期 | 行 |
|:---|:---|---:|
| 波士顿 | 2019-01-02 | 1 |
| 波士顿 | 2019-01-03 | 2 |
| 波士顿 | 2019-01-04 | 3 |
| ... | ... | ... |
| 罗斯福 | 2019-01-02 | 1 |
| 罗斯福 | 2019-01-03 | 2 |
| 罗斯福 | 2019-01-04 | 3 |
| ... | ... | ... |

请注意，尽管函数使用了 `ORDER BY` 子句进行计算，
但结果不一定需要排序，
所以如果希望排序，`SELECT` 也需要显式排序。

### 框架

框架指定了每个行的相对行集，这些行用于评估函数。
距离从当前行出发，以 `PRECEDING` 或 `FOLLOWING` 的方式给出，这取决于 `ORDER BY` 子句在 `OVER` 规范中定义的顺序。
该距离可以指定为整数的 `ROWS` 或 `GROUPS`，
或作为 `RANGE` 的 delta 表达式。框架不能在开始后结束。
对于 `RANGE` 规范，必须只有一个排序表达式，并且它必须支持减法，除非仅使用哨兵边界值 `UNBOUNDED PRECEDING` / `UNBOUNDED FOLLOWING` / `CURRENT ROW`。
使用 [`EXCLUDE` 子句](#exclude-clause)，可以排除在指定排序表达式中与当前行相等的行（所谓的同组行）。

默认框架是无限制的（即整个分区），当没有 `ORDER BY` 子句时，且当存在 `ORDER BY` 子句时，是 `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`。默认情况下，`CURRENT ROW` 边界值（但不是 `EXCLUDE` 子句中的 `CURRENT ROW`）意味着在使用 `RANGE` 或 `GROUP` 框架时的当前行和所有同组行，但在使用 `ROWS` 框架时仅指当前行。

#### `ROWS` 框架

这是一个简单的 `ROW` 框架查询，使用聚合函数：

```sql
SELECT points,
    sum(points) OVER (
        ROWS BETWEEN 1 PRECEDING
                 AND 1 FOLLOWING) AS we
FROM results;
```

此查询计算每个点及其两侧点的 `sum`：

<img src="/images/blog/windowing/moving-sum.jpg" alt="三个值的移动 SUM" title="图 2: 三个值的移动 SUM" style="max-width:90%;width:90%;height:auto"/>

请注意，在分区的边缘，只有两个值被相加。
这是因为框架被裁剪到分区的边缘。

#### `RANGE` 框架

回到发电数据，假设数据是嘈杂的。
我们可能希望计算每个电厂的 7 天移动平均值以平滑噪声。
为此，我们可以使用这个窗口查询：

```sql
SELECT "Plant", "Date",
    avg("MWh") OVER (
        PARTITION BY "Plant"
        ORDER BY "Date" ASC
        RANGE BETWEEN INTERVAL 3 DAYS PRECEDING
                  AND INTERVAL 3 DAYS FOLLOWING)
        AS "MWh 7-day Moving Average"
FROM "Generation History"
ORDER BY 1, 2;
```

此查询按 `Plant` 分区数据（以保持不同电厂的数据分开），
按 `Date` 排序每个电厂的分区（以将能量测量值放在一起），
并使用 `RANGE` 框架，在每天的两侧使用 3 天的范围来计算 `avg`
（以处理任何缺失的天数）。
这是结果：

| 电厂 | 日期 | MWh 7-day Moving Average |
|:---|:---|---:|
| 波士顿 | 2019-01-02 | 517450.75 |
| 波士顿 | 2019-01-03 | 508793.20 |
| 波士顿 | 2019-01-04 | 508529.83 |
| ... | ... | ... |
| 波士顿 | 2019-01-13 | 499793.00 |
| 罗斯福 | 2019-01-02 | 104768.25 |
| 罗斯福 | 2019-01-03 | 102713.00 |
| 罗斯福 | 2019-01-04 | 102249.50 |
| ... | ... | ... |

#### `GROUPS` 框架

第三种框架类型按当前行的相对组数进行计数。
一个 *组* 在这种框架中是具有相同 `ORDER BY` 值的一组值。
如果我们假设每天都在发电，
我们可以使用 `GROUPS` 框架来计算系统中所有发电的移动平均值，
而无需使用日期运算：

```sql
SELECT "Date", "Plant",
    avg("MWh") OVER (
        ORDER BY "Date" ASC
        GROUPS BETWEEN 3 PRECEDING
                   AND 3 FOLLOWING)
        AS "MWh 7-day Moving Average"
FROM "Generation History"
ORDER BY 1, 2;
```

|    日期    |   电厂   | MWh 7-day Moving Average |
|------------|-----------|-------------------------:|
| 2019-01-02 | 波士顿    | 311109.500               |
| 2019-01-02 | 罗斯福 | 311109.500               |
| 2019-01-03 | 波士顿    | 305753.100               |
| 2019-01-03 | 罗斯福 | 305753.100               |
| 2019-01-04 | 波士顿    | 305389.667               |
| 2019-01-04 | 罗斯福 | 305389.667               |
| ... | ... | ... |
| 2019-01-12 | 波士顿    | 309184.900               |
| 2019-01-12 | 罗斯福 | 309184.900               |
| 2019-01-13 | 波士顿    | 299469.375               |
| 2019-01-13 | 罗斯福 | 299469.375               |

请注意，每个日期的值是相同的。

#### `EXCLUDE` 子句

`EXCLUDE` 是一个可选的框架子句修饰符，用于排除当前行周围的行。
这在您想计算附近行的某些聚合值以查看当前行与其比较时非常有用。

在以下示例中，我们想知道运动员在比赛中的时间与他们在事件中记录的 ±10 天内的平均时间相比：

```sql
SELECT
    event,
    date,
    athlete,
    avg(time) OVER w AS recent,
FROM results
WINDOW w AS (
    PARTITION BY event
    ORDER BY date
    RANGE BETWEEN INTERVAL 10 DAYS PRECEDING AND INTERVAL 10 DAYS FOLLOWING
        EXCLUDE CURRENT ROW
)
ORDER BY event, date, athlete;
```

`EXCLUDE` 子句有四个选项，用于指定如何处理当前行：

* `CURRENT ROW` – 仅排除当前行
* `GROUP` – 排除当前行及其所有“同组”行（具有相同 `ORDER BY` 值的行）
* `TIES` – 排除所有同组行，但 _不_ 排除当前行（这会在两侧形成一个空洞）
* `NO OTHERS` – 不排除任何内容（默认）

排除适用于窗口聚合函数以及 `first`、`last` 和 `nth_value` 函数。

### `WINDOW` 子句

可以在同一个 `SELECT` 中指定多个不同的 `OVER` 子句，并且每个子句将分别计算。
通常，我们希望多个窗口函数使用相同的布局。
`WINDOW` 子句可以用来定义一个 *命名的* 窗口，可以在多个窗口函数之间共享：

```sql
SELECT "Plant", "Date",
    min("MWh") OVER seven AS "MWh 7-day Moving Minimum",
    avg("MWh") OVER seven AS "MWh 7-day Moving Average",
    max("MWh") OVER seven AS "MWh 7-day Moving Maximum"
FROM "Generation History"
WINDOW seven AS (
    PARTITION BY "Plant"
    ORDER BY "Date" ASC
    RANGE BETWEEN INTERVAL 3 DAYS PRECEDING
              AND INTERVAL 3 DAYS FOLLOWING)
ORDER BY 1, 2;
```

这三个窗口函数也将共享数据布局，这将提高性能。

可以在同一个 `WINDOW` 子句中通过逗号分隔定义多个窗口：

```sql
SELECT "Plant", "Date",
    min("MWh") OVER seven AS "MWh 7-day Moving Minimum",
    avg("MWh") OVER seven AS "MWh 7-day Moving Average",
    max("MWh") OVER seven AS "MWh 7-day Moving Maximum",
    min("MWh") OVER three AS "MWh 3-day Moving Minimum",
    avg("MWh") OVER three AS "MWh 3-day Moving Average",
    max("MWh") OVER three AS "MWh 3-day Moving Maximum"
FROM "Generation History"
WINDOW
    seven AS (
        PARTITION BY "Plant"
        ORDER BY "Date" ASC
        RANGE BETWEEN INTERVAL 3 DAYS PRECEDING
                  AND INTERVAL 3 DAYS FOLLOWING),
    three AS (
        PARTITION BY "Plant"
        ORDER BY "Date" ASC
        RANGE BETWEEN INTERVAL 1 DAYS PRECEDING
        AND INTERVAL 1 DAYS FOLLOWING)
ORDER BY 1, 2;
```

上面的查询没有使用常见的选择语句中的子句，如 `WHERE`、`GROUP BY` 等。对于更复杂的查询，您可以在 [`SELECT 语句`]({% link docs/stable/sql/statements/select.md %}) 的规范顺序中找到 `WINDOW` 子句的位置。

### 使用 `QUALIFY` 过滤窗口函数的结果

窗口函数在 [`WHERE`]({% link docs/stable/sql/query_syntax/where.md %}) 和 [`HAVING`]({% link docs/stable/sql/query_syntax/having.md %}) 子句已经评估之后执行，因此无法使用这些子句来过滤窗口函数的结果。
[`QUALIFY` 子句]({% link docs/stable/sql/query_syntax/qualify.md %}) 可以避免使用子查询或 [`WITH` 子句]({% link docs/stable/sql/query_syntax/with.md %}) 来执行此过滤。

### 箱形图查询

所有聚合函数都可以作为窗口函数使用，包括复杂的统计函数。
这些函数的实现已经针对窗口进行了优化，
我们可以通过窗口语法编写查询以生成移动箱形图的数据：

```sql
SELECT "Plant", "Date",
    min("MWh") OVER seven AS "MWh 7-day Moving Minimum",
    quantile_cont("MWh", [0.25, 0.5, 0.75]) OVER seven
        AS "MWh 7-day Moving IQR",
    max("MWh") OVER seven AS "MWh 7-day Moving Maximum",
FROM "Generation History"
WINDOW seven AS (
    PARTITION BY "Plant"
    ORDER BY "Date" ASC
    RANGE BETWEEN INTERVAL 3 DAYS PRECEDING
              AND INTERVAL 3 DAYS FOLLOWING)
ORDER BY 1, 2;
```

---