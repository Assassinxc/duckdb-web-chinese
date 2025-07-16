---
---
layout: docu
redirect_from:
- /docs/test/functions/date
- /docs/test/functions/date/
- /docs/sql/functions/date
title: 日期函数
---

<!-- markdownlint-disable MD001 -->

本节描述了用于检查和操作 [`DATE`]({% link docs/stable/sql/data_types/date.md %}) 值的函数和运算符。

## 日期运算符

下表显示了 `DATE` 类型可用的数学运算符。

| 运算符 | 描述 | 示例 | 结果 |
|:-|:--|:---|:--|
| `+` | 添加天数（整数） | `DATE '1992-03-22' + 5` | `1992-03-27` |
| `+` | 添加一个 `INTERVAL` | `DATE '1992-03-22' + INTERVAL 5 DAY` | `1992-03-27 00:00:00` |
| `+` | 添加一个变量 `INTERVAL` | `SELECT DATE '1992-03-22' + INTERVAL (d.days) DAY FROM (VALUES (5), (11)) d(days)` | `1992-03-27 00:00:00` 和 `1992-04-02 00:00:00` |
| `-` | 日期相减 | `DATE '1992-03-27' - DATE '1992-03-22'` | `5` |
| `-` | 减去一个 `INTERVAL` | `DATE '1992-03-27' - INTERVAL 5 DAY` | `1992-03-22 00:00:00` |
| `-` | 减去一个变量 `INTERVAL` | `SELECT DATE '1992-03-27' - INTERVAL (d.days) DAY FROM (VALUES (5), (11)) d(days)` | `1992-03-22 00:00:00` 和 `1992-03-16 00:00:00` |

对无限值 [infinite values]({% link docs/stable/sql/data_types/date.md %}#special-values) 进行加减操作，会得到相同的无限值。

## 日期函数

下表显示了 `DATE` 类型可用的函数。
日期也可以通过类型提升使用 [时间戳函数]({% link docs/stable/sql/functions/timestamp.md %}) 进行操作。

| 名称 | 描述 |
|:--|:-------|
| [`current_date`](#current_date) | 当前事务开始时本地时区的当前日期。注意，函数调用时应省略括号。 |
| [`date_add(date, interval)`](#date_adddate-interval) | 将间隔加到日期上并返回一个 `DATETIME` 值。 |
| [`date_diff(part, startdate, enddate)`](#date_diffpart-startdate-enddate) | 两个日期之间的 [分区]({% link docs/stable/sql/functions/datepart.md %}) 边界数量。 |
| [`date_part(part, date)`](#date_partpart-date) | 获取 [子字段]({% link docs/stable/sql/functions/datepart.md %})（等同于 `extract`）。 |
| [`date_sub(part, startdate, enddate)`](#date_subpart-startdate-enddate) | 两个日期之间的完整 [分区]({% link docs/stable/sql/functions/datepart.md %}) 数量。 |
| [`date_trunc(part, date)`](#date_truncpart-date) | 截断到指定的 [精度]({% link docs/stable/sql/functions/datepart.md %})。 |
| [`datediff(part, startdate, enddate)`](#datediffpart-startdate-enddate) | 两个日期之间的 [分区]({% link docs/stable/sql/functions/datepart.md %}) 边界数量。`date_diff` 的别名。 |
| [`datepart(part, date)`](#datepartpart-date) | 获取 [子字段]({% link docs/stable/sql/functions/datepart.md %})（等同于 `extract`）。`date_part` 的别名。 |
| [`datesub(part, startdate, enddate)`](#datesubpart-startdate-enddate) | 两个日期之间的完整 [分区]({% link docs/stable/sql/functions/datepart.md %}) 数量。`date_sub` 的别名。 |
| [`datetrunc(part, date)`](#datetruncpart-date) | 截断到指定的 [精度]({% link docs/stable/sql/functions/datepart.md %})。`date_trunc` 的别名。 |
| [`dayname(date)`](#daynamedate) | 星期的英文名称。 |
| [`extract(part from date)`](#extractpart-from-date) | 从日期中获取 [子字段]({% link docs/stable/sql/functions/datepart.md %})。 |
| [`greatest(date, date)`](#greatestdate-date) | 两个日期中较晚的一个。 |
| [`isfinite(date)`](#isfinitedate) | 如果日期是有限的则返回 `true`，否则返回 `false`。 |
| [`isinf(date)`](#isinfdate) | 如果日期是无限的则返回 `true`，否则返回 `false`。 |
| [`julian(date)`](#juliandate) | 从日期中提取儒略日数。 |
| [`last_day(date)`](#last_daydate) | 日期对应月份的最后一天。 |
| [`least(date, date)`](#leastdate-date) | 两个日期中较早的一个。 |
| [`make_date(year, month, day)`](#make_dateyear-month-day) | 根据给定的部分生成日期。 |
| [`monthname(date)`](#monthnamedate) | 月份的英文名称。 |
| [`strftime(date, format)`](#strftimedate-format) | 根据 [格式字符串]({% link docs/stable/sql/functions/dateformat.md %}) 将日期转换为字符串。 |
| [`time_bucket(bucket_width, date[, offset])`](#time_bucketbucket_width-date-offset) | 将 `date` 截断到宽度为 `bucket_width` 的网格。网格以 `2000-01-01[ + offset]` 锚定，当 `bucket_width` 是月数或更粗的单位时，否则以 `2000-01-03[ + offset]` 锚定。请注意，`2000-01-03` 是星期一。 |
| [`time_bucket(bucket_width, date[, origin])`](#time_bucketbucket_width-date-origin) | 将 `timestamptz` 截断到宽度为 `bucket_width` 的网格。网格以 `origin` 时间戳锚定，其默认值为 `2000-01-01`，当 `bucket_width` 是月数或更粗的单位时，否则为 `2000-01-03`。请注意，`2000-01-03` 是星期一。 |
| [`today()`](#today) | UTC 时间中当前事务开始时的当前日期。 |

#### `current_date`

<div class="nostroke_table"></div>

| **描述** | 本地时区中当前事务开始时的当前日期。注意，函数调用时应省略括号。 |
| **示例** | `current_date` |
| **结果** | `2022-10-08` |

#### `date_add(date, interval)`

<div class="nostroke_table"></div>

| **描述** | 将间隔加到日期上并返回一个 `DATETIME` 值。 |
| **示例** | `date_add(DATE '1992-09-15', INTERVAL 2 MONTH)` |
| **结果** | `1992-11-15 00:00:00` |

#### `date_diff(part, startdate, enddate)`

<div class="nostroke_table"></div>

| **描述** | 两个日期之间的 [分区]({% link docs/stable/sql/functions/datepart.md %}) 边界数量。 |
| **示例** | `date_diff('month', DATE '1992-09-15', DATE '1992-11-14')` |
| **结果** | `2` |

#### `date_part(part, date)`

<div class="nostroke_table"></div>

| **描述** | 获取 [子字段]({% link docs/stable/sql/functions/datepart.md %})（等同于 `extract`）。 |
| **示例** | `date_part('year', DATE '1992-09-20')` |
| **结果** | `1992` |

#### `date_sub(part, startdate, enddate)`

<div class="nostroke_table"></div>

| **描述** | 两个日期之间的完整 [分区]({% link docs/stable/sql/functions/datepart.md %}) 数量。 |
| **示例** | `date_sub('month', DATE '1992-09-15', DATE '1992-11-14')` |
| **结果** | `1` |

#### `date_trunc(part, date)`

<div class="nostroke_table"></div>

| **描述** | 截断到指定的 [精度]({% link docs/stable/sql/functions/datepart.md %})。 |
| **示例** | `date_trunc('month', DATE '1992-03-07')` |
| **结果** | `1992-03-01` |

#### `datediff(part, startdate, enddate)`

<div class="nostroke_table"></div>

| **描述** | 两个日期之间的 [分区]({% link docs/stable/sql/functions/datepart.md %}) 边界数量。 |
| **示例** | `datediff('month', DATE '1992-09-15', DATE '1992-11-14')` |
| **结果** | `2` |
| **别名** | `date_diff`。 |

#### `datepart(part, date)`

<div class="nostroke_table"></div>

| **描述** | 获取 [子字段]({% link docs/stable/sql/functions/datepart.md %})（等同于 `extract`）。 |
| **示例** | `datepart('year', DATE '1992-09-20')` |
| **结果** | `1992` |
| **别名** | `date_part`。 |

#### `datesub(part, startdate, enddate)`

<div class="nostroke_table"></div>

| **描述** | 两个日期之间的完整 [分区]({% link docs/stable/sql/functions/datepart.md %}) 数量。 |
| **示例** | `datesub('month', DATE '1992-09-15', DATE '1992-11-14')` |
| **结果** | `1` |
| **别名** | `date_sub`。 |

#### `datetrunc(part, date)`

<div class="nostroke_table"></div>

| **描述** | 截断到指定的 [精度]({% link docs/stable/sql/functions/datepart.md %})。 |
| **示例** | `datetrunc('month', DATE '1992-03-07')` |
| **结果** | `1992-03-01` |
| **别名** | `date_trunc`。 |

#### `dayname(date)`

<div class="nostroke_table"></div>

| **描述** | 星期的英文名称。 |
| **示例** | `dayname(DATE '1992-09-20')` |
| **结果** | `Sunday` |

#### `extract(part from date)`

<div class="nostroke_table"></div>

| **描述** | 从日期中获取 [子字段]({% link docs/stable/sql/functions/datepart.md %})。 |
| **示例** | `extract('year' FROM DATE '1992-09-20')` |
| **结果** | `1992` |

#### `greatest(date, date)`

<div class="nostroke_table"></div>

| **描述** | 两个日期中较晚的一个。 |
| **示例** | `greatest(DATE '1992-09-20', DATE '1992-03-07')` |
| **结果** | `1992-09-20` |

#### `isfinite(date)`

<div class="nostroke_table"></div>

| **描述** | 如果日期是有限的则返回 `true`，否则返回 `false`。 |
| **示例** | `isfinite(DATE '1992-03-07')` |
| **结果** | `true` |

#### `isinf(date)`

<div class="nostroke_table"></div>

| **描述** | 如果日期是无限的则返回 `true`，否则返回 `false`。 |
| **示例** | `isinf(DATE '-infinity')` |
| **结果** | `true` |

#### `julian(date)`

<div class="nostroke_table"></div>

| **描述** | 从日期中提取儒略日数。 |
| **示例** | `julian(DATE '1992-09-20')` |
| **结果** | `2448886.0` |

#### `last_day(date)`

<div class="nostroke_table"></div>

| **描述** | 日期对应的月份的最后一天。 |
| **示例** | `last_day(DATE '1992-09-20')` |
| **结果** | `1992-09-30` |

#### `least(date, date)`

<div class="nostroke_table"></div>

| **描述** | 两个日期中较早的一个。 |
| **示例** | `least(DATE '1992-09-20', DATE '1992-03-07')` |
| **结果** | `1992-03-07` |

#### `make_date(year, month, day)`

<div class="nostroke_table"></div>

| **描述** | 根据给定的部分生成日期。 |
| **示例** | `make_date(1992, 9, 20)` |
| **结果** | `1992-09-20` |

#### `monthname(date)`

<div class="nostroke_table"></div>

| **描述** | 月份的英文名称。 |
| **示例** | `monthname(DATE '1992-09-20')` |
| **结果** | `September` |

#### `strftime(date, format)`

<div class="nostroke_table"></div>

| **描述** | 根据 [格式字符串]({% link docs/stable/sql/functions/dateformat.md %}) 将日期转换为字符串。 |
| **示例** | `strftime(DATE '1992-01-01', '%a, %-d %B %Y')` |
| **结果** | `Wed, 1 January 1992` |

#### `time_bucket(bucket_width, date[, offset])`

<div class="nostroke_table"></div>

| **描述** | 将 `date` 截断到宽度为 `bucket_width` 的网格。网格以 `2000-01-01[ + offset]` 锚定，当 `bucket
`bucket_width` 是月数或更粗的单位时，否则以 `2000-01-03[ + offset]` 锚定。请注意，`2000-01-03` 是星期一。 |
| **示例** | `time_bucket(INTERVAL '2 months', DATE '1992-04-20', INTERVAL '1 month')` |
| **结果** | `1992-04-01` |

#### `time_bucket(bucket_width, date[, origin])`

<div class="nostroke_table"></div>

| **描述** | 将 `timestamptz` 截断到宽度为 `bucket_width` 的网格。网格以 `origin` 时间戳锚定，其默认值为 `2000-01-01`，当 `bucket_width` 是月数或更粗的单位时，否则为 `2000-01-03`。请注意，`2000-01-03` 是星期一。 |
| **示例** | `time_bucket(INTERVAL '2 weeks', DATE '1992-04-20', DATE '1992-04-01')` |
| **结果** | `1992-04-15` |

#### `today()`

<div class="nostroke_table"></div>

| **描述** | UTC 时间中当前事务开始时的当前日期。 |
| **示例** | `today()` |
| **结果** | `2022-10-08` |

## 日期子字段提取函数

还有专门的提取函数用于获取 [子字段]({% link docs/stable/sql/functions/datepart.md %}#part-functions)。
一些示例包括从日期中提取日或从日期中提取星期几。

对无限日期应用的函数将返回相同的无限日期（例如 `greatest`）或 `NULL`（例如 `date_part`），具体取决于什么“有意义”。
通常，如果函数需要检查无限日期的各个部分，结果将是 `NULL`。