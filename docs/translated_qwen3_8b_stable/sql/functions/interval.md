---
---
layout: docu
redirect_from:
- /docs/sql/functions/interval
title: 间隔函数
---

<!-- markdownlint-disable MD001 -->

本节描述了用于检查和操作 [`INTERVAL`]({% link docs/stable/sql/data_types/interval.md %}) 值的函数和运算符。

## 间隔运算符

下表显示了 `INTERVAL` 类型可用的数学运算符。

| 运算符 | 描述 | 示例 | 结果 |
|:-|:--|:----|:--|
| `+` | 将 `INTERVAL` 相加 | `INTERVAL 1 HOUR + INTERVAL 5 HOUR` | `INTERVAL 6 HOUR` |
| `+` | 将 `INTERVAL` 加到 `DATE` | `DATE '1992-03-22' + INTERVAL 5 DAY` | `1992-03-27` |
| `+` | 将 `INTERVAL` 加到 `TIMESTAMP` | `TIMESTAMP '1992-03-22 01:02:03' + INTERVAL 5 DAY` | `1992-03-27 01:02:03` |
| `+` | 将 `INTERVAL` 加到 `TIME` | `TIME '01:02:03' + INTERVAL 5 HOUR` | `06:02:03` |
| `-` | 从 `INTERVAL` 中减去 | `INTERVAL 5 HOUR - INTERVAL 1 HOUR` | `INTERVAL 4 HOUR` |
| `-` | 从 `DATE` 中减去 `INTERVAL` | `DATE '1992-03-27' - INTERVAL 5 DAY` | `1992-03-22` |
| `-` | 从 `TIMESTAMP` 中减去 `INTERVAL` | `TIMESTAMP '1992-03-27 01:02:03' - INTERVAL 5 DAY` | `1992-03-22 01:02:03` |
| `-` | 从 `TIME` 中减去 `INTERVAL` | `TIME '06:02:03' - INTERVAL 5 HOUR` | `01:02:03` |

## 间隔函数

下表显示了 `INTERVAL` 类型可用的标量函数。

| 名称 | 描述 |
|:--|:-------|
| [`date_part(part, interval)`](#date_partpart-interval) | 提取 [日期部分]({% link docs/stable/sql/functions/datepart.md %}) (等同于 `extract`)。参阅 [`INTERVAL`]({% link docs/stable/sql/data_types/interval.md %}) 了解此提取的有时令人惊讶的规则。 |
| [`datepart(part, interval)`](#datepartpart-interval) | `date_part` 的别名。 |
| [`extract(part FROM interval)`](#extractpart-from-interval) | `date_part` 的别名。 |
| [`epoch(interval)`](#epochinterval) | 获取间隔中的总秒数，以双精度浮点数表示。 |
| [`to_centuries(integer)`](#to_centuriesinteger) | 构造一个世纪间隔。 |
| [`to_days(integer)`](#to_daysinteger) | 构造一个天间隔。 |
| [`to_decades(integer)`](#to_decadesinteger) | 构造一个十年间隔。 |
| [`to_hours(integer)`](#to_hoursinteger) | 构造一个小时间隔。 |
| [`to_microseconds(integer)`](#to_microsecondsinteger) | 构造一个微秒间隔。 |
| [`to_millennia(integer)`](#to_millenniainteger) | 构造一个千年间隔。 |
| [`to_milliseconds(integer)`](#to_millisecondsinteger) | 构造一个毫秒间隔。 |
| [`to_minutes(integer)`](#to_minutesinteger) | 构造一个分钟间隔。 |
| [`to_months(integer)`](#to_monthsinteger) | 构造一个月份间隔。 |
| [`to_quarters(integer`)](#to_quartersinteger) | 构造一个 `integer` 个季度的间隔。 |
| [`to_seconds(integer)`](#to_secondsinteger) | 构造一个秒间隔。 |
| [`to_weeks(integer)`](#to_weeksinteger) | 构造一个周间隔。 |
| [`to_years(integer)`](#to_yearsinteger) | 构造一个年份间隔。 |

> 仅定义了文档中列出的 [日期部分组件]({% link docs/stable/sql/functions/datepart.md %})。

#### `date_part(part, interval)`

<div class="nostroke_table"></div>

| **描述** | 提取 [日期部分]({% link docs/stable/sql/functions/datepart.md %}) (等同于 `extract`)。参阅 [`INTERVAL`]({% link docs/stable/sql/data_types/interval.md %}) 了解此提取的有时令人惊讶的规则。 |
| **示例** | `date_part('year', INTERVAL '14 months')` |
| **结果** | `1` |

#### `datepart(part, interval)`

<div class="nostroke_table"></div>

| **描述** | `date_part` 的别名。 |
| **示例** | `datepart('year', INTERVAL '14 months')` |
| **结果** | `1` |

#### `extract(part FROM interval)`

<div class="nostroke_table"></div>

| **描述** | `date_part` 的别名。 |
| **示例** | `extract('month' FROM INTERVAL '14 months')` |
| **结果** | 2 |

#### `epoch(interval)`

<div class="nostroke_table"></div>

| **描述** | 获取间隔中的总秒数，以双精度浮点数表示。 |
| **示例** | `epoch(INTERVAL 5 HOUR)` |
| **结果** | `18000.0` |

#### `to_centuries(integer)`

<div class="nostroke_table"></div>

| **描述** | 构造一个世纪间隔。 |
| **示例** | `to_centuries(5)` |
| **结果** | `INTERVAL 500 YEAR` |

#### `to_days(integer)`

<div class="nostroke_table"></div>

| **描述** | 构造一个天间隔。 |
| **示例** | `to_days(5)` |
| **结果** | `INTERVAL 5 DAY` |

#### `to_decades(integer)`

<div class="nostroke_table"></div>

| **描述** | 构造一个十年间隔。 |
| **示例** | `to_decades(5)` |
| **结果** | `INTERVAL 50 YEAR` |

#### `to_hours(integer)`

<div class="nostroke_table"></div>

| **描述** | 构造一个小时间隔。 |
| **示例** | `to_hours(5)` |
| **结果** | `INTERVAL 5 HOUR` |

#### `to_microseconds(integer)`

<div class="nostroke_table"></div>

| **描述** | 构造一个微秒间隔。 |
| **示例** | `to_microseconds(5)` |
| **结果** | `INTERVAL 5 MICROSECOND` |

#### `to_millennia(integer)`

<div class="nostroke_table"></div>

| **描述** | 构造一个千年间隔。 |
| **示例** | `to_millennia(5)` |
| **结果** | `INTERVAL 5000 YEAR` |

#### `to_milliseconds(integer)`

<div class="nostroke_table"></div>

| **描述** | 构造一个毫秒间隔。 |
| **示例** | `to_milliseconds(5)` |
| **结果** | `INTERVAL 5 MILLISECOND` |

#### `to_minutes(integer)`

<div class="nostroke_table"></div>

| **描述** | 构造一个分钟间隔。 |
| **示例** | `to_minutes(5)` |
| **结果** | `INTERVAL 5 MINUTE` |

#### `to_months(integer)`

<div class="nostroke_table"></div>

| **描述** | 构造一个月份间隔。 |
| **示例** | `to_months(5)` |
| **结果** | `INTERVAL 5 MONTH` |

#### `to_quarters(integer)`

<div class="nostroke_table"></div>

| **描述** | 构造一个 `integer` 个季度的间隔。 |
| **示例** | `to_quarters(5)` |
| **结果** | `INTERVAL 1 YEAR 3 MONTHS` |

#### `to_seconds(integer)`

<div class="nostroke_table"></div>

| **描述** | 构造一个秒间隔。 |
| **示例** | `to_seconds(5)` |
| **结果** | `INTERVAL 5 SECOND` |

#### `to_weeks(integer)`

<div class="nostroke_table"></div>

| **描述** | 构造一个周间隔。 |
| **示例** | `to_weeks(5)` |
| **结果** | `INTERVAL 35 DAY` |

#### `to_years(integer)`

<div class="nostroke_table"></div>

| **描述** | 构造一个年份间隔。 |
| **示例** | `to_years(5)` |
| **结果** | `INTERVAL 5 YEAR` |