---
---
layout: docu
redirect_from:
- /docs/sql/functions/timestamptz
title: 带时区的时间戳函数
---

<!-- markdownlint-disable MD001 -->

本节描述了用于检查和操作 [`TIMESTAMP WITH TIME ZONE`（或 `TIMESTAMPTZ`）值]({% link docs/stable/sql/data_types/timestamp.md %}) 的函数和运算符。另请参阅相关的 [`TIMESTAMP` 函数]({% link docs/stable/sql/functions/timestamp.md %}）。

时区支持由内置的 [ICU 扩展]({% link docs/stable/core_extensions/icu.md %}) 提供。

在下面的示例中，假定当前时区为 `America/Los_Angeles`，使用格里高利历。

## 内置带时区的时间戳函数

下表列出了 `TIMESTAMPTZ` 值的可用标量函数。由于这些函数不涉及分组或显示，因此它们始终可用。

| 名称 | 描述 |
|:--|:-------|
| [`current_timestamp`](#current_timestamp) | 当前日期和时间（当前事务的开始）。 |
| [`get_current_timestamp()`](#get_current_timestamp) | 当前日期和时间（当前事务的开始）。 |
| [`greatest(timestamptz, timestamptz)`](#greatesttimestamptz-timestamptz) | 两个时间戳中较晚的一个。 |
| [`isfinite(timestamptz)`](#isfinitetimestamptz) | 如果带时区的时间戳是有限的，返回 true，否则返回 false。 |
| [`isinf(timestamptz)`](#isinftimestamptz) | 如果带时区的时间戳是无限的，返回 true，否则返回 false。 |
| [`least(timestamptz, timestamptz)`](#leasttimestamptz-timestamptz) | 两个时间戳中较早的一个。 |
| [`now()`](#now) | 当前日期和时间（当前事务的开始）。 |
| [`timetz_byte_comparable(timetz)`](#timetz_byte_comparabletimetz) | 将 `TIME WITH TIME ZONE` 转换为 `UBIGINT` 排序键。 |
| [`to_timestamp(double)`](#to_timestampdouble) | 将自纪元以来的秒数转换为带时区的时间戳。 |
| [`transaction_timestamp()`](#transaction_timestamp) | 当前日期和时间（当前事务的开始）。 |

#### `current_timestamp`

<div class="nostroke_table"></div>

| **描述** | 当前日期和时间（当前事务的开始）。 |
| **示例** | `current_timestamp` |
| **结果** | `2022-10-08 12:44:46.122-07` |

#### `get_current_timestamp()`

<div class="nostroke_table"></div>

| **描述** | 当前日期和时间（当前事务的开始）。 |
| **示例** | `get_current_timestamp()` |
| **结果** | `2022-10-08 12:44:46.122-07` |

#### `greatest(timestamptz, timestamptz)`

<div class="nostroke_table"></div>

| **描述** | 两个时间戳中较晚的一个。 |
| **示例** | `greatest(TIMESTAMPTZ '1992-09-20 20:38:48', TIMESTAMPTZ '1992-03-22 01:02:03.1234')` |
| **结果** | `1992-09-20 20:38:48-07` |

#### `isfinite(timestamptz)`

<div class="nostroke_table"></div>

| **描述** | 如果带时区的时间戳是有限的，返回 true，否则返回 false。 |
| **示例** | `isfinite(TIMESTAMPTZ '1992-03-07')` |
| **结果** | `true` |

#### `isinf(timestamptz)`

<div class="nostroke_table"></div>

| **描述** | 如果带时区的时间戳是无限的，返回 true，否则返回 false。 |
| **示例** | `isinf(TIMESTAMPTZ '-infinity')` |
| **结果** | `true` |

#### `least(timestamptz, timestamptz)`

<div class="nostroke_table"></div>

| **描述** | 两个时间戳中较早的一个。 |
| **示例** | `least(TIMESTAMPTZ '1992-09-20 20:38:48', TIMESTAMPTZ '1992-03-22 01:02:03.1234')` |
| **结果** | `1992-03-22 01:02:03.1234-08` |

#### `now()`

<div class="nostroke_table"></div>

| **描述** | 当前日期和时间（当前事务的开始）。 |
| **示例** | `now()` |
| **结果** | `2022-10-08 12:44:46.122-07` |

#### `timetz_byte_comparable(timetz)`

<div class="nostroke_table"></div>

| **描述** | 将 `TIME WITH TIME ZONE` 转换为 `UBIGINT` 排序键。 |
| **示例** | `timetz_byte_comparable('18:18:16.21-07:00'::TIMETZ)` |
| **结果** | `2494691656335442799` |

#### `to_timestamp(double)`

<div class="nostroke_table"></div>

| **描述** | 将自纪元以来的秒数转换为带时区的时间戳。 |
| **示例** | `to_timestamp(1284352323.5)` |
| **结果** | `2010-09-13 04:32:03.5+00` |

#### `transaction_timestamp()`

<div class="nostroke_table"></div>

| **描述** | 当前日期和时间（当前事务的开始）。 |
| **示例** | `transaction_timestamp()` |
| **结果** | `2022-10-08 12:44:46.122-07` |

## 带时区的时间戳字符串

在未加载时区扩展的情况下，`TIMESTAMPTZ` 值将使用偏移表示法进行字符串转换。
这将允许您在没有时区信息的情况下正确指定一个时间点。
为了可移植性，`TIMESTAMPTZ` 值始终使用 GMT 偏移量显示：

```sql
SELECT '2022-10-08 13:13:34-07'::TIMESTAMPTZ;
```

```text
2022-10-08 20:13:34+00
```

如果加载了像 ICU 这样的时区扩展，那么可以从字符串中解析时区并将其转换为本地时区的表示：

```sql
SELECT '2022-10-08 13:13:34 Europe/Amsterdam'::TIMESTAMPTZ::VARCHAR;
```

```text
2022-10-08 04:13:34-07 -- 偏移量将根据您的本地时区而有所不同
```

## ICU 带时区的时间戳运算符

下表显示了由 ICU 扩展提供的 `TIMESTAMP WITH TIME ZONE` 值的可用数学运算符。

| 运算符 | 描述 | 示例 | 结果 |
|:-|:--|:----|:--|
| `+` | 添加一个 `INTERVAL` | `TIMESTAMPTZ '1992-03-22 01:02:03' + INTERVAL 5 DAY` | `1992-03-27 01:02:03` |
| `-` | 减去 `TIMESTAMPTZ` | `TIMESTAMPTZ '1992-03-27' - TIMESTAMPTZ '1992-03-22'` | `5 days` |
| `-` | 减去一个 `INTERVAL` | `TIMESTAMPTZ '1992-03-27 01:02:03' - INTERVAL 5 DAY` | `1992-03-22 01:02:03` |

对无限值进行加减操作将产生相同的无限值。

## ICU 带时区的时间戳函数

下表显示了 ICU 提供的 `TIMESTAMP WITH TIME ZONE` 值的标量函数。

| 名称 | 描述 |
|:--|:-------|
| [`age(timestamptz, timestamptz)`](#agetimestamptz-timestamptz) | 减去参数，得到两个时间戳之间的时间差。 |
| [`age(timestamptz)`](#agetimestamptz) | 从当前日期减去。 |
| [`date_diff(part, startdate, enddate)`](#date_diffpart-startdate-enddate) | 两个时间戳之间的 [分隔]({% link docs/stable/sql/functions/datepart.md %}) 数量。 |
| [`date_part([part, ...], timestamptz)`](#date_partpart--timestamptz) | 获取列出的 [子字段]({% link docs/stable/sql/functions/datepart.md %}) 作为 `struct`。列表必须为常量。 |
| [`date_part(part, timestamptz)`](#date_partpart-timestamptz) | 获取 [子字段]({% link docs/stable/sql/functions/datepart.md %})（等同于 *extract*）。 |
| [`date_sub(part, startdate, enddate)`](#date_subpart-startdate-enddate) | 两个时间戳之间的完整 [分隔]({% link docs/stable/sql/functions/datepart.md %}) 数量。 |
| [`date_trunc(part, timestamptz)`](#date_truncpart-timestamptz) | 截断到指定的 [精度]({% link docs/stable/sql/functions/datepart.md %})。 |
| [`datediff(part, startdate, enddate)`](#datediffpart-startdate-enddate) | `date_diff` 的别名。两个时间戳之间的 [分隔]({% link docs/stable/sql/functions/datepart.md %}) 数量。 |
| [`datepart([part, ...], timestamptz)`](#datepartpart--timestamptz) | `date_part` 的别名。获取列出的 [子字段]({% link docs/stable/sql/functions/datepart.md %}) 作为 `struct`。列表必须为常量。 |
| [`datepart(part, timestamptz)`](#datepartpart-timestamptz) | `date_part` 的别名。获取 [子字段]({% link docs/stable/sql/functions/datepart.md %})（等同于 *extract*）。 |
| [`datesub(part, startdate, enddate)`](#datesubpart-startdate-enddate) | `date_sub` 的别名。两个时间戳之间的完整 [分隔]({% link docs/stable/sql/functions/datepart.md %}) 数量。 |
| [`datetrunc(part, timestamptz)`](#datetruncpart-timestamptz) | `date_trunc` 的别名。截断到指定的 [精度]({% link docs/stable/sql/functions/datepart.md %})。 |
| [`epoch_ms(timestamptz)`](#epoch_mstimestamptz) | 将 `timestamptz` 转换为自纪元以来的毫秒数。 |
| [`epoch_ns(timestamptz)`](#epoch_nstimestamptz) | 将 `timestamptz` 转换为自纪元以来的纳秒数。 |
| [`epoch_us(timestamptz)`](#epoch_ustimestamptz) | 将 `timestamptz` 转换为自纪元以来的微秒数。 |
| [`extract(field FROM timestamptz)`](#extractfield-from-timestamptz) | 从 `TIMESTAMP WITH TIME ZONE` 获取 [子字段]({% link docs/stable/sql/functions/datepart.md %})。 |
| [`last_day(timestamptz)`](#last_daytimestamptz) | 该月的最后一天。 |
| [`make_timestamptz(bigint, bigint, bigint, bigint, bigint, double, string)`](#make_timestamptzbigint-bigint-bigint-bigint-bigint-double-string) | 给定部分和时区的 `TIMESTAMP WITH TIME ZONE`。 |
| [`make_timestamptz(bigint, bigint, bigint, bigint, bigint, double)`](#make_timestamptzbigint-bigint-bigint-bigint-bigint-double) | 给定部分在当前时区的 `TIMESTAMP WITH TIME ZONE`。 |
| [`make_timestamptz(microseconds)`](#make_timestamptzmicroseconds) | 给定自纪元以来的 µs 的 `TIMESTAMP WITH TIME ZONE`。 |
| [`strftime(timestamptz, format)`](#strftimetimestamptz-format) | 将 `TIMESTAMP WITH TIME ZONE` 值根据 [格式字符串]({% link docs/stable/sql/functions/dateformat.md %}#format-specifiers) 转换为字符串。 |
| [`strptime(text, format)`](#strptimetext-format) | 如果指定了 `%Z`，则根据 [格式字符串]({% link docs/stable/sql/functions/dateformat.md %}#format-specifiers) 将字符串转换为 `TIMESTAMP WITH TIME ZONE`。 |
| [`time_bucket(bucket_width, timestamptz[, offset])`](#time_bucketbucket_width-timestamptz-offset) | 将 `timestamptz` 截断到宽度为 `bucket_width` 的网格。网格在 `2000-01-01 00:00:00+00:00[ + offset]` 处锚定，当 `bucket_width` 是月数或更粗的单位时，否则在 `2000-01-03 00:00:00+00:00[ + offset]` 处锚定。注意 `2000-01-03` 是星期一。 |
| [`time_bucket(bucket_width, timestamptz[, origin])`](#time_bucketbucket_width-timestamptz-origin) | 将 `timestamptz` 截断到宽度为 `bucket_width` 的网格。网格锚定在 `origin` 时间戳，当 `bucket_width` 是月数或更粗的单位时，默认值为 `2000-01-01 00:00:00+00:00`，否则为 `2000-01-03 00:00:00+00:00`。注意 `2000-01-03` 是星期一。 |
| [`time_bucket(bucket_width, timestamptz[, timezone])`](#time_bucketbucket_width-timestamptz-origin) | 将 `timestamptz` 截断到宽度为 `bucket_width` 的网格。网格锚定在 `origin` 时间戳，当 `bucket_width` 是月数或更粗的单位时，`origin` 默认为 `2000-01-01 00:00:00` 提供的 `timezone`，否则为 `2000-01-03 00:00:00` 提供的 `timezone`。默认时区是 `'UTC'`。注意 `2000-01-03` 是星期一。 |



#### `age(timestamptz, timestamptz)`

<div class="nostroke_table"></div>

| **描述** | 减去参数，得到两个时间戳之间的时间差。 |
| **示例** | `age(TIMESTAMPTZ '2001-04-10', TIMESTAMPTZ '1992-09-20')` |
| **结果** | `8 years 6 months 20 days` |

#### `age(timestamptz)`

<div class="nostroke_table"></div>

| **描述** | 从当前日期减去。 |
| **示例** | `age(TIMESTAMP '1992-09-20')` |
| **结果** | `29 years 1 month 27 days 12:39:00.844` |

#### `date_diff(part, startdate, enddate)`

<div class="nostroke_table"></div>

| **描述** | 两个时间戳之间的 [分隔]({% link docs/stable/sql/functions/datepart.md %}) 数量。 |
| **示例** | `date_diff('hour', TIMESTAMPTZ '1992-09-30 23:59:59', TIMESTAMPTZ '1992-10-01 01:58:00')` |
| **结果** | `2` |

#### `date_part([part, ...], timestamptz)`

<div class="nostroke_table"></div>

| **描述** | 获取列出的 [子字段]({% link docs/stable/sql/functions/datepart.md %}) 作为 `struct`。列表必须为常量。 |
| **示例** | `date_part(['year', 'month', 'day'], TIMESTAMPTZ '1992-09-20 20:38:40-07')` |
| **结果** | `{year: 1992, month: 9, day: 20}` |

#### `date_part(part, timestamptz)`

<div class="nostroke_table"></div>

| **描述** | 获取 [子字段]({% link docs/stable/sql/functions/datepart.md %})（等同于 *extract*）。 |
| **示例** | `date_part('minute', TIMESTAMPTZ '1992-09-20 20:38:40')` |
| **结果** | `38` |

#### `date_sub(part, startdate, enddate)`

<div class="nostroke_table"></div>

| **描述** | 两个时间戳之间的完整 [分隔]({% link docs/stable/sql/functions/datepart.md %}) 数量。 |
| **示例** | `date_sub('hour', TIMESTAMPTZ '1992-09-30 23:59:59', TIMESTAMPTZ '1992-10-01 01:58:00')` |
| **结果** | `1` |

#### `date_trunc(part, timestamptz)`

<div class="nostroke_table"></div>

| **描述** | 截断到指定的 [精度]({% link docs/stable/sql/functions/datepart.md %})。 |
| **示例** | `date_trunc('hour', TIMESTAMPTZ '1992-09-20 20:38:40')` |
| **结果** | `1992-09-20 20:00:00` |

#### `datediff(part, startdate, enddate)`

<div class="nostroke_table"></div>

| **描述** | `date_diff` 的别名。两个时间戳之间的 [分隔]({% link docs/stable/sql/functions/datepart.md %}) 数量。 |
| **示例** | `datediff('hour', TIMESTAMPTZ '1992-09-30 23:59:59', TIMESTAMPTZ '1992-10-01 01:58:00')` |
| **结果** | `2` |

#### `datepart([part, ...], timestamptz)`

<div class="nostroke_table"></div>

| **描述** | `date_part` 的别名。获取列出的 [子字段]({% link docs/stable/sql/functions/datepart.md %}) 作为 `struct`。列表必须为常量。 |
| **示例** | `datepart(['year', 'month', 'day'], TIMESTAMPTZ '1992-09-20 20:38:40-07')` |
| **结果** | `{year: 1992, month: 9, day: 20}` |

#### `datepart(part, timestamptz)`

<div class="nostroke_table"></div>

| **描述** | `date_part` 的别名。获取 [子字段]({% link docs/stable/sql/functions/datepart.md %})（等同于 *extract*）。 |
| **示例** | `datepart('minute', TIMESTAMPTZ '1992-09-20 20:38:40')` |
| **结果** | `38` |

#### `datesub(part, startdate, enddate)`

<div class="nostroke_table"></div>

| **描述** | `date_sub` 的别名。两个时间戳之间的完整 [分隔]({% link docs/stable/sql/functions/datepart.md %}) 数量。 |
| **示例** | `datesub('hour', TIMESTAMPTZ '1992-09-30 23:59:59', TIMESTAMPTZ '1992-10-01 01:58:00')` |
| **结果** | `1` |

#### `datetrunc(part, timestamptz)`

<div class="nostroke_table"></div>

| **描述** | `date_trunc` 的别名。截断到指定的 [精度]({% link docs/stable/sql/functions/datepart.md %})。 |
| **示例** | `datetrunc('hour', TIMESTAMPTZ '1992-09-20 20:38:40')` |
| **结果** | `1992-09-20 20:00:00` |

#### `epoch_ms(timestamptz)`

<div class="nostroke_table"></div>

| **描述** | 将 `timestamptz` 转换为自纪元以来的毫秒数。 |
| **示例** | `epoch_ms('2022-11-07 08:43:04.123456+00'::TIMESTAMPTZ);` |
| **结果** | `1667810584123` |

#### `epoch_ns(timestamptz)`

<div class="nostroke_table"></div>

| **描述** | 将 `timestamptz` 转换为自纪元以来的纳秒数。 |
| **示例** | `epoch_ns('2022-11-07 08:43:04.123456+00'::TIMESTAMPTZ);` |
| **结果** | `1667810584123456000` |

#### `epoch_us(timestamptz)`

<div class="nostroke_table"></div>

| **描述** | 将 `timestamptz` 转换为自纪元以来的微秒数。 |
| **示例** | `epoch_us('2022-11-07 08:43:04.123456+00'::TIMESTAMPTZ);` |
| **结果** | `1667810584123456` |

#### `extract(field FROM timestamptz)`

<div class="nostroke_table"></div>

| **描述** | 从 `TIMESTAMP WITH TIME ZONE` 获取 [子字段]({% link docs/stable/sql/functions/datepart.md %})。 |
| **示例** | `extract('hour' FROM TIMESTAMPTZ '1992-09-20 20:38:48')` |
| **结果** | `20` |

#### `last_day(timestamptz)`

<div class="nostroke_table"></div>

| **描述** | 该月的最后一天。 |
| **示例** | `last_day(TIMESTAMPTZ '1992-03-22 01:02:03.1234')` |
| **结果** | `1992-03-31` |

#### `make_timestamptz(bigint, bigint, bigint, bigint, bigint, double, string)`

<div class="nostroke_table"></div>

| **描述** | 给定部分和时区的 `TIMESTAMP WITH TIME ZONE`。 |
| **示例** | `make_timestamptz(1992, 9, 20, 15, 34, 27.123456, 'CET')` |
| **结果** | `1992-09-20 06:34:27.123456-07` |

#### `make_timestamptz(bigint, bigint, bigint, bigint, bigint, double)`

<div class="nostroke_table"></div>

| **描述** | 给定部分在当前时区的 `TIMESTAMP WITH TIME ZONE`。 |
| **示例** | `make_timestamptz(1992, 9, 20, 13, 34, 27.123456)` |
| **结果** | `1992-09-20 13:34:27.123456-07` |

#### `make_timestamptz(microseconds)`

<div class="nostroke_table"></div>

| **描述** | 给定自纪元以来的 µs 的 `TIMESTAMP WITH TIME ZONE`。 |
| **示例** | `make_timestamptz(1667810584123456)` |
| **结果** | `2022-11-07 16:43:04.123456-08` |

#### `strftime(timestamptz, format)`

<div class="nostroke_table"></div>

| **描述** | 将 `TIMESTAMP WITH TIME ZONE` 值根据 [格式字符串]({% link docs/stable/sql/functions/dateformat.md %}#format-specifiers) 转换为字符串。 |
| **示例** | `strftime(timestamptz '1992-01-01 20:38:40', '%a, %-d %B %Y - %I:%M:%S %p')` |
| **结果** | `Wed, 1 January 1992 - 08:38:40 PM` |

#### `strptime(text, format)`

<div class="nostroke_table"></div>

| **描述** | 如果指定了 `%Z`，则根据 [格式字符串]({% link docs/stable/sql/functions/dateformat.md %}#format-specifiers) 将字符串转换为 `TIMESTAMP WITH TIME ZONE`。 |
| **示例** | `strptime('Wed, 1 January 1992 - 08:38:40 PST', '%a, %-d %B %Y - %H:%M:%S %Z')` |
| **结果** | `1992-01-01 08:38:40-08` |

#### `time_bucket(bucket_width, timestamptz[, offset])`

<div class="nostroke_table"></div>

| **描述** | 将 `timestamptz` 截断到宽度为 `bucket_width` 的网格。网格在 `2000-01-01 00:00:00+00:00[ + offset]` 处锚定，当 `bucket_width` 是月数或更粗的单位时，否则在 `2000-01-03 00:00:00+00:00[ + offset]` 处锚定。注意 `2000-01-03` 是星期一。 |
| **示例** | `time_bucket(INTERVAL '10 minutes', TIMESTAMPTZ '1992-04-20 15:26:00-07', INTERVAL '5 minutes')` |
| **结果** | `1992-04-20 15:25:00-07` |

#### `time_bucket(bucket_width, timestamptz[, origin])`

<div class="nostroke_table"></div>

| **描述** | 将 `timestamptz` 截断到宽度为 `bucket_width` 的网格。网格锚定在 `origin` 时间戳，当 `bucket_width` 是月数或更粗的单位时，默认值为 `2000-01-01 00:00:00+00:00`，否则为 `2000-01-03 00:00:00+00:00`。注意 `2000-01-03` 是星期一。 |
| **示例** | `time_bucket(INTERVAL '2 weeks', TIMESTAMPTZ '1992-04-20 15:26:00-07', TIMESTAMPTZ '1992-04-01 00:00:00-07')` |
| **结果** | `1992-04-15 00:00:00-07` |

#### `time_bucket(bucket_width, timestamptz[, timezone])`

<div class="nostroke_table"></div>

| **描述** | 将 `timestamptz` 截断到宽度为 `bucket_width` 的网格。网格锚定在 `origin` 时间戳，当 `bucket_width` 是月数或更粗的单位时，`origin` 默认为 `2000-01-01 00:00:00` 提供的 `timezone`，否则为 `2000-01-03 00:00:00` 提供的 `timezone`。默认时区是 `'UTC'`。注意 `2000-01-03` 是星期一。 |
| **示例** | `time_bucket(INTERVAL '2 days', TIMESTAMPTZ '1992-04-20 15:26:00-07', 'Europe/Berlin')` |
| **结果** | `1992-04-19 15:00:00-07` (=`1992-04-20 00:00:00 Europe/Berlin`) |

还有专门的提取函数可以获取 [子字段]({% link docs/stable/sql/functions/datepart.md %}）。

## ICU 带时区的时间戳表函数

下表显示了 `TIMESTAMP WITH TIME ZONE` 类型的可用表函数。

| 名称 | 描述 |
|:--|:-------|
| [`generate_series(timestamptz, timestamptz, interval)`](#generate_seriestimestamptz-timestamptz-interval) | 生成一个包含起始时间戳和结束时间戳（包括两者）的时间戳表，按间隔步进。 |
| [`range(timestamptz, timestamptz, interval)`](#rangetimestamptz-timestamptz-interval) | 生成一个包含起始时间戳但不包括结束时间戳（半开区间）的时间戳表，按间隔步进。 |

> 表函数的边界不允许使用无限值。

#### `generate_series(timestamptz, timestamptz, interval)`

<div class="nostroke_table"></div>

| **描述** | 生成一个包含起始时间戳和结束时间戳（包括两者）的时间戳表，按间隔步进。 |
| **示例** | `generate_series(TIMESTAMPTZ '2001-04-10', TIMESTAMPTZ '2001-04-11', INTERVAL 30 MINUTE)` |

#### `range(timestamptz, timestamptz, interval)`

<div class="nostroke_table"></div>

| **描述** | 生成一个包含起始时间戳但不包括结束时间戳（半开区间）的时间戳表，按间隔步进。 |
| **示例** | `range(TIMESTAMPTZ '2001-04-10', TIMESTAMPTZ '2001-04-11', INTERVAL 30 MINUTE)` |

## ICU 无时区的时间戳函数

下表显示了由 ICU 提供的对普通 `TIMESTAMP` 值进行操作的标量函数。
这些函数假定 `TIMESTAMP` 是一个“本地时间戳”。

本地时间戳实际上是一种将时区的各个部分值编码为单个值的方法。
由于夏令时可能导致生成的值出现间隙和歧义，因此应谨慎使用这些函数。
通常，使用 `date_part` 函数的 `struct` 变体可以更可靠地实现相同的功能。

| 名称 | 描述 |
|:--|:-------|
| [`current_localtime()`](#current_localtime) | 返回一个 `TIME`，其 GMT 分区值对应于当前时区的本地时间。 |
| [`current_localtimestamp()`](#current_localtimestamp) | 返回一个 `TIMESTAMP`，其 GMT 分区值对应于当前时区的本地日期和时间。 |
| [`localtime`](#localtime) | `current_localtime()` 函数调用的同义词。 |
| [`localtimestamp`](#localtimestamp) | `current_localtimestamp()` 函数调用的同义词。 |
| [`timezone(text, timestamp)`](#timezonetext-timestamp) | 使用 GMT 中时间戳的 [日期部分]({% link docs/stable/sql/functions/datepart.md %}) 构造指定时区的时间戳。实际上，参数是一个“本地”时间。 |
| [`timezone(text, timestamptz)`](#timezonetext-timestamptz) | 使用指定时区中时间戳的 [日期部分]({% link docs/stable/sql/functions/datepart.md %}) 构造时间戳。实际上，结果是一个“本地”时间。 |

#### `current_localtime()`

<div class="nostroke_table"></div>

| **描述** | 返回一个 `TIME`，其 GMT 分区值对应于当前时区的本地时间。 |
| **示例** | `current_localtime()` |
| **结果** | `08:47:56.497` |

#### `current_localtimestamp()`

<div class="nostroke_table"></div>

| **描述** | 返回一个 `TIMESTAMP`，其 GMT 分区值对应于当前时区的本地日期和时间。 |
| **示例** | `current_localtimestamp()` |
| **结果** | `2022-12-17 08:47:56.497` |

#### `localtime`

<div class="nostroke_table"></div>

| **描述** | `current_localtime()` 函数调用的同义词。 |
| **示例** | `localtime` |
| **结果** | `08:47:56.497` |

#### `localtimestamp`

<div class="nostroke_table"></div>

| **描述** | `current_localtimestamp()` 函数调用的同义词。 |
| **示例** | `localtimestamp` |
| **结果** | `2022-12-17 08:47:56.497` |

#### `timezone(text, timestamp)`

<div class="nostroke_table"></div>

| **描述** | 使用 GMT 中时间戳的 [日期部分]({% link docs/stable/sql/functions/datepart.md %}) 构造指定时区的时间戳。实际上，参数是一个“本地”时间。 |
| **示例** | `timezone('America/Denver', TIMESTAMP '2001-02-16 20:38:40')` |
| **结果** | `2001-02-16 19:38:40-08` |

#### `timezone(text, timestamptz)`

<div class="nostroke_table"></div>

| **描述** | 使用指定时区中时间戳的 [日期部分]({% link docs/stable/sql/functions/date
| **示例** | `timezone('America/Denver', TIMESTAMPTZ '2001-02-16 20:38:40-05')` |
| **结果** | `2001-02-16 18:38:40` |

## AT TIME ZONE

`AT TIME ZONE` 语法是上述（两个参数）`timezone` 函数的语法糖：

```sql
SELECT TIMESTAMP '2001-02-16 20:38:40' AT TIME ZONE 'America/Denver' AS ts;
```

```text
2001-02-16 19:38:40-08
```

```sql
SELECT TIMESTAMP WITH TIME ZONE '2001-02-16 20:38:40-05' AT TIME ZONE 'America/Denver' AS ts;
```

```text
2001-02-16 18:38:40
```

请注意，不允许使用数字时区：

```sql
SELECT TIMESTAMP '2001-02-16 20:38:40-05' AT TIME ZONE '0200' AS ts;
```

```console
Not implemented Error: Unknown TimeZone '0200'
```

## 无穷大

对无穷大日期应用的函数将返回相同的无穷大日期（例如 `greatest`）或 `NULL`（例如 `date_part`），具体取决于“什么是有意义的”。
通常，如果函数需要检查无穷大时间值的各个部分，结果将是 `NULL`。

## 历法

ICU 扩展还支持 [非格里高利历]({% link docs/stable/sql/data_types/timestamp.md %}#calendar-support)。
如果当前使用的是这样的历法，那么显示和分组操作将使用该历法。