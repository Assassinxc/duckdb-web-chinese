---
---
layout: docu
redirect_from:
- /docs/sql/functions/time
title: 时间函数
---

<!-- markdownlint-disable MD001 -->

本节描述了用于检查和操作 [`TIME` 值]({% link docs/stable/sql/data_types/time.md %}) 的函数和运算符。

## 时间运算符

下表显示了 `TIME` 类型可用的数学运算符。

| 运算符 | 描述 | 示例 | 结果 |
|:-|:---|:----|:--|
| `+` | 添加一个 `INTERVAL` | `TIME '01:02:03' + INTERVAL 5 HOUR` | `06:02:03` |
| `-` | 减去一个 `INTERVAL` | `TIME '06:02:03' - INTERVAL 5 HOUR` | `01:02:03` |

## 时间函数

下表显示了 `TIME` 类型可用的标量函数。

| 名称 | 描述 |
|:--|:-------|
| [`current_time`](#current_time) | 本地时区中的当前时间（当前事务的开始时间）。请注意，函数调用时应省略括号。 |
| [`date_diff(part, starttime, endtime)`](#date_diffpart-starttime-endtime) | 两个时间之间的 [分区]({% link docs/stable/sql/functions/datepart.md %}) 边界数量。 |
| [`date_part(part, time)`](#date_partpart-time) | 获取 [子字段]({% link docs/stable/sql/functions/datepart.md %})（等同于 `extract`）。 |
| [`date_sub(part, starttime, endtime)`](#date_subpart-starttime-endtime) | 两个时间之间的完整 [分区]({% link docs/stable/sql/functions/datepart.md %}) 数量。 |
| [`datediff(part, starttime, endtime)`](#datediffpart-starttime-endtime) | `date_diff` 的别名。两个时间之间的 [分区]({% link docs/stable/sql/functions/datepart.md %}) 边界数量。 |
| [`datepart(part, time)`](#datepartpart-time) | `date_part` 的别名。获取 [子字段]({% link docs/stable/sql/functions/datepart.md %})（等同于 `extract`）。 |
| [`datesub(part, starttime, endtime)`](#datesubpart-starttime-endtime) | `date_sub` 的别名。两个时间之间的完整 [分区]({% link docs/stable/sql/functions/datepart.md %}) 数量。 |
| [`extract(part FROM time)`](#extractpart-from-time) | 从时间中获取子字段。 |
| [`get_current_time()`](#get_current_time) | UTC 时区中的当前时间（当前事务的开始时间）。 |
| [`make_time(bigint, bigint, double)`](#make_timebigint-bigint-double) | 给定部分对应的时间。 |

对于时间而言，唯一定义的 [日期部分]({% link docs/stable/sql/functions/datepart.md %}) 是 `epoch`、`hours`、`minutes`、`seconds`、`milliseconds` 和 `microseconds`。

#### `current_time`

<div class="nostroke_table"></div>

| **描述** | 本地时区中的当前时间（当前事务的开始时间）。请注意，函数调用时应省略括号。 |
| **示例** | `current_time` |
| **结果** | `10:31:58.578` |
| **别名** | `get_current_time()` |

#### `date_diff(part, starttime, endtime)`

<div class="nostroke_table"></div>

| **描述** | 两个时间之间的 [分区]({% link docs/stable/sql/functions/datepart.md %}) 边界数量。 |
| **示例** | `date_diff('hour', TIME '01:02:03', TIME '06:01:03')` |
| **结果** | `5` |

#### `date_part(part, time)`

<div class="nostroke_table"></div>

| **描述** | 获取 [子字段]({% link docs/stable/sql/functions/datepart.md %})（等同于 `extract`）。 |
| **示例** | `date_part('minute', TIME '14:21:13')` |
| **结果** | `21` |

#### `date_sub(part, starttime, endtime)`

<div class="nostroke_table"></div>

| **描述** | 两个时间之间的完整 [分区]({% link docs/stable/sql/functions/datepart.md %}) 数量。 |
| **示例** | `date_sub('hour', TIME '01:02:03', TIME '06:01:03')` |
| **结果** | `4` |

#### `datediff(part, starttime, endtime)`

<div class="nostroke_table"></div>

| **描述** | `date_diff` 的别名。两个时间之间的 [分区]({% link docs/stable/sql/functions/datepart.md %}) 边界数量。 |
| **示例** | `datediff('hour', TIME '01:02:03', TIME '06:01:03')` |
| **结果** | `5` |

#### `datepart(part, time)`

<div class="nostroke_table"></div>

| **描述** | `date_part` 的别名。获取 [子字段]({% link docs/stable/sql/functions/datepart.md %})（等同于 `extract`）。 |
| **示例** | `datepart('minute', TIME '14:21:13')` |
| **结果** | `21` |

#### `datesub(part, starttime, endtime)`

<div class="nostroke_table"></div>

| **描述** | `date_sub` 的别名。两个时间之间的完整 [分区]({% link docs/stable/sql/functions/datepart.md %}) 数量。 |
| **示例** | `datesub('hour', TIME '01:02:03', TIME '06:01:03')` |
| **结果** | `4` |

#### `extract(part FROM time)`

<div class="nostroke_table"></div>

| **描述** | 从时间中获取子字段。 |
| **示例** | `extract('hour' FROM TIME '14:21:13')` |
| **结果** | `14` |

#### `get_current_time()`

<div class="nostroke_table"></div>

| **描述** | UTC 时区中的当前时间（当前事务的开始时间）。 |
| **示例** | `get_current_time()` |
| **结果** | `10:31:58.578` |
| **别名** | `current_time` |

#### `make_time(bigint, bigint, double)`

<div class="nostroke_table"></div>

| **描述** | 给定部分对应的时间。 |
| **示例** | `make_time(13, 34, 27.123456)` |
| **结果** | `13:34:27.123456` |