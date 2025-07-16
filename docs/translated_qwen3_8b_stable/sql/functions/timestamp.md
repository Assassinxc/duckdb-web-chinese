---
---
layout: docu
redirect_from:
- /docs/sql/functions/timestamp
title: 时间戳函数
---

<!-- markdownlint-disable MD001 -->

本节描述了用于检查和操作 [`TIMESTAMP` 值]({% link docs/stable/sql/data_types/timestamp.md %}) 的函数和运算符。
另请参阅相关的 [`TIMESTAMPTZ` 函数]({% link docs/stable/sql/functions/timestamptz.md %}).

## 时间戳运算符

下表显示了 `TIMESTAMP` 类型可用的数学运算符。

| 运算符 | 描述 | 示例 | 结果 |
|:-|:--|:----|:--|
| `+` | 添加 `INTERVAL` | `TIMESTAMP '1992-03-22 01:02:03' + INTERVAL 5 DAY` | `1992-03-27 01:02:03` |
| `-` | 减去 `TIMESTAMP` | `TIMESTAMP '1992-03-27' - TIMESTAMP '1992-03-22'` | `5 days` |
| `-` | 减去 `INTERVAL` | `TIMESTAMP '1992-03-27 01:02:03' - INTERVAL 5 DAY` | `1992-03-22 01:02:03` |

对 [无限值]({% link docs/stable/sql/data_types/timestamp.md %}#special-values) 进行加减运算会得到相同的无限值。

## 标量时间戳函数

下表显示了 `TIMESTAMP` 值可用的标量函数。

| 名称 | 描述 |
|:--|:-------|
| [`age(timestamp, timestamp)`](#agetimestamp-timestamp) | 用两个时间戳相减，得到两个时间戳之间的时间差。 |
| [`age(timestamp)`](#agetimestamp) | 用当前日期减去时间戳。 |
| [`century(timestamp)`](#centurytimestamp) | 提取时间戳的世纪。 |
| [`current_localtimestamp()`](#current_localtimestamp) | 返回当前时间戳（事务开始时）。 |
| [`date_diff(part, startdate, enddate)`](#date_diffpart-startdate-enddate) | 两个时间戳之间的 [分区]({% link docs/stable/sql/functions/datepart.md %}) 边界数量。 |
| [`date_part([part, ...], timestamp)`](#date_partpart--timestamp) | 获取列出的 [子字段]({% link docs/stable/sql/functions/datepart.md %}) 作为 `struct`。列表必须是常量。 |
| [`date_part(part, timestamp)`](#date_partpart-timestamp) | 获取 [子字段]({% link docs/stable/sql/functions/datepart.md %})（等同于 `extract`）。 |
| [`date_sub(part, startdate, enddate)`](#date_subpart-startdate-enddate) | 两个时间戳之间的完整 [分区]({% link docs/stable/sql/functions/datepart.md %}) 数量。 |
| [`date_trunc(part, timestamp)`](#date_truncpart-timestamp) | 截断到指定的 [精度]({% link docs/stable/sql/functions/datepart.md %})。 |
| [`datediff(part, startdate, enddate)`](#datediffpart-startdate-enddate) | `date_diff` 的别名。两个时间戳之间的 [分区]({% link docs/stable/sql/functions/datepart.md %}) 边界数量。 |
| [`datepart([part, ...], timestamp)`](#datepartpart--timestamp) | `date_part` 的别名。获取列出的 [子字段]({% link docs/stable/sql/functions/datepart.md %}) 作为 `struct`。列表必须是常量。 |
| [`datepart(part, timestamp)`](#datepartpart-timestamp) | `date_part` 的别名。获取 [子字段]({% link docs/stable/sql/functions/datepart.md %})（等同于 `extract`）。 |
| [`datesub(part, startdate, enddate)`](#datesubpart-startdate-enddate) | `date_sub` 的别名。两个时间戳之间的完整 [分区]({% link docs/stable/sql/functions/datepart.md %}) 数量。 |
| [`datetrunc(part, timestamp)`](#datetruncpart-timestamp) | `date_trunc` 的别名。截断到指定的 [精度]({% link docs/stable/sql/functions/datepart.md %})。 |
| [`dayname(timestamp)`](#daynametimestamp) | 星期的英文名称。 |
| [`epoch_ms(ms)`](#epoch_msms) | 将自纪元以来的毫秒数转换为时间戳。 |
| [`epoch_ms(timestamp)`](#epoch_mstimestamp) | 返回自纪元以来的总毫秒数。 |
| [`epoch_ns(timestamp)`](#epoch_nstimestamp) | 返回自纪元以来的总纳秒数。 |
| [`epoch_us(timestamp)`](#epoch_ustimestamp) | 返回自纪元以来的总微秒数。 |
| [`epoch(timestamp)`](#epochtimestamp) | 返回自纪元以来的总秒数。 |
| [`extract(field FROM timestamp)`](#extractfield-from-timestamp) | 从时间戳中获取 [子字段]({% link docs/stable/sql/functions/datepart.md %})。 |
| [`greatest(timestamp, timestamp)`](#greatesttimestamp-timestamp) | 两个时间戳中较晚的那个。 |
| [`isfinite(timestamp)`](#isfinitetimestamp) | 如果时间戳是有限的则返回 true，否则返回 false。 |
| [`isinf(timestamp)`](#isinftimestamp) | 如果时间戳是无限的则返回 true，否则返回 false。 |
| [`julian(timestamp)`](#juliantimestamp) | 从时间戳中提取儒略日数。 |
| [`last_day(timestamp)`](#last_daytimestamp) | 月份的最后一天。 |
| [`least(timestamp, timestamp)`](#leasttimestamp-timestamp) | 两个时间戳中较早的那个。 |
| [`make_timestamp(bigint, bigint, bigint, bigint, bigint, double)`](#make_timestampbigint-bigint-bigint-bigint-bigint-double) | 给定部分的时间戳。 |
| [`make_timestamp(microseconds)`](#make_timestampmicroseconds) | 将自纪元以来的微秒数转换为时间戳。 |
| [`make_timestamp_ns(nanoseconds)`](#make_timestamp_nsnanoseconds) | 将自纪元以来的纳秒数转换为时间戳。 |
| [`monthname(timestamp)`](#monthnametimestamp) | 月份的英文名称。 |
| [`strftime(timestamp, format)`](#strftimetimestamp-format) | 根据 [格式字符串]({% link docs/stable/sql/functions/dateformat.md %}#format-specifiers) 将时间戳转换为字符串。 |
| [`strptime(text, format-list)`](#strptimetext-format-list) | 将字符串 `text` 转换为时间戳，应用 [格式字符串]({% link docs/stable/sql/functions/dateformat.md %}) 列表中的格式，直到其中一个成功。失败时抛出错误。要返回 `NULL`，请使用 [`try_strptime`](#try_strptimetext-format-list)。 |
| [`strptime(text, format)`](#strptimetext-format) | 根据 [格式字符串]({% link docs/stable/sql/functions/dateformat.md %}#format-specifiers) 将字符串 `text` 转换为时间戳。失败时抛出错误。要返回 `NULL`，请使用 [`try_strptime`](#try_strptimetext-format)。 |
| [`time_bucket(bucket_width, timestamp[, offset])`](#time_bucketbucket_width-timestamp-offset) | 将 `timestamp` 截断到宽度为 `bucket_width` 的网格。当 `bucket_width` 是月数或更粗的单位时，网格锚定在 `2000-01-01 00:00:00[ + offset]`，否则锚定在 `2000-01-03 00:00:00[ + offset]`。注意 `2000-01-03` 是星期一。 |
| [`time_bucket(bucket_width, timestamp[, origin])`](#time_bucketbucket_width-timestamp-origin) | 将 `timestamp` 截断到宽度为 `bucket_width` 的网格。网格锚定在 `origin` 时间戳，当 `bucket_width` 是月数或更粗的单位时，默认为 `2000-01-01 00:00:00`，否则为 `2000-01-03 00:00:00`。注意 `2000-01-03` 是星期一。 |
| [`try_strptime(text, format-list)`](#try_strptimetext-format-list) | 将字符串 `text` 转换为时间戳，应用 [格式字符串]({% link docs/stable/sql/functions/dateformat.md %}) 列表中的格式，直到其中一个成功。失败时返回 `NULL`。 |
| [`try_strptime(text, format)`](#try_strptimetext-format) | 根据 [格式字符串]({% link docs/stable/sql/functions/dateformat.md %}#format-specifiers) 将字符串 `text` 转换为时间戳。失败时返回 `NULL`。 |

还有专门的提取函数来获取 [子字段]({% link docs/stable/sql/functions/datepart.md %}).

对无限日期应用的函数将返回相同的无限日期（例如 `greatest`）或 `NULL`（例如 `date_part`），具体取决于什么“有意义”。通常，如果函数需要检查无限日期的各个部分，结果将是 `NULL`。

#### `age(timestamp, timestamp)`

<div class="nostroke_table"></div>

| **描述** | 用两个时间戳相减，得到两个时间戳之间的时间差。 |
| **示例** | `age(TIMESTAMP '2001-04-10', TIMESTAMP '1992-09-20')` |
| **结果** | `8 years 6 months 20 days` |

#### `age(timestamp)`

<div class="nostroke_table"></div>

| **描述** | 用当前日期减去时间戳。 |
| **示例** | `age(TIMESTAMP '1992-09-20')` |
| **结果** | `29 years 1 month 27 days 12:39:00.844` |

#### `century(timestamp)`

<div class="nostroke_table"></div>

| **描述** | 提取时间戳的世纪。 |
| **示例** | `century(TIMESTAMP '1992-03-22')` |
| **结果** | `20` |

#### `current_localtimestamp()`

<div class="nostroke_table"></div>

| **描述** | 返回当前时间戳（事务开始时）。 |
| **示例** | `current_localtimestamp()` |
| **结果** | `2024-11-30 13:28:48.895` |

#### `date_diff(part, startdate, enddate)`

<div class="nostroke_table"></div>

| **描述** | 两个时间戳之间的 [分区]({% link docs/stable/sql/functions/datepart.md %}) 边界数量。 |
| **示例** | `date_diff('hour', TIMESTAMP '1992-09-30 23:59:59', TIMESTAMP '1992-10-01 01:58:00')` |
| **结果** | `2` |

#### `date_part([part, ...], timestamp)`

<div class="nostroke_table"></div>

| **描述** | 获取列出的 [子字段]({% link docs/stable/sql/functions/datepart.md %}) 作为 `struct`。列表必须是常量。 |
| **示例** | `date_part(['year', 'month', 'day'], TIMESTAMP '1992-09-20 20:38:40')` |
| **结果** | `{year: 1992, month: 9, day: 20}` |

#### `date_part(part, timestamp)`

<div class="nostroke_table"></div>

| **描述** | 获取 [子字段]({% link docs/stable/sql/functions/datepart.md %})（等同于 `extract`）。 |
| **示例** | `date_part('minute', TIMESTAMP '1992-09-20 20:38:40')` |
| **结果** | `38` |

#### `date_sub(part, startdate, enddate)`

<div class="nostroke_table"></div>

| **描述** | 两个时间戳之间的完整 [分区]({% link docs/stable/sql/functions/datepart.md %}) 数量。 |
| **示例** | `date_sub('hour', TIMESTAMP '1992-09-30 23:59:59', TIMESTAMP '1992-10-01 01:58:00')` |
| **结果** | `1` |

#### `date_trunc(part, timestamp)`

<div class="nostroke_table"></div>

| **描述** | 截断到指定的 [精度]({% link docs/stable/sql/functions/datepart.md %})。 |
| **示例** | `date_trunc('hour', TIMESTAMP '1992-09-20 20:38:40')` |
| **结果** | `1992-09-20 20:00:00` |

#### `datediff(part, startdate, enddate)`

<div class="nostroke_table"></div>

| **描述** | `date_diff` 的别名。两个时间戳之间的 [分区]({% link docs/stable/sql/functions/datepart.md %}) 边界数量。 |
| **示例** | `datediff('hour', TIMESTAMP '1992-09-30 23:59:59', TIMESTAMP '1992-10-01 01:58:00')` |
| **结果** | `2` |

#### `datepart([part, ...], timestamp)`

<div class="nostroke_table"></div>

| **描述** | `date_part` 的别名。获取列出的 [子字段]({% link docs/stable/sql/functions/datepart.md %}) 作为 `struct`。列表必须是常量。 |
| **示例** | `datepart(['year', 'month', 'day'], TIMESTAMP '1992-09-20 20:38:40')` |
| **结果** | `{year: 1992, month: 9, day: 20}` |

#### `datepart(part, timestamp)`

<div class="nostroke_table"></div>

| **描述** | `date_part` 的别名。获取 [子字段]({% link docs/stable/sql/functions/datepart.md %})（等同于 `extract`）。 |
| **示例** | `datepart('minute', TIMESTAMP '1992-09-20 20:38:40')` |
| **结果** | `38` |

#### `datesub(part, startdate, enddate)`

<div class="nostroke_table"></div>

| **描述** | `date_sub` 的别名。两个时间戳之间的完整 [分区]({% link docs/stable/sql/functions/datepart.md %}) 数量。 |
| **示例** | `datesub('hour', TIMESTAMP '1992-09-30 23:59:59', TIMESTAMP '1992-10-01 01:58:00')` |
| **结果** | `1` |

#### `datetrunc(part, timestamp)`

<div class="nostroke_table"></div>

| **描述** | `date_trunc` 的别名。截断到指定的 [精度]({% link docs/stable/sql/functions/datepart.md %})。 |
| **示例** | `datetrunc('hour', TIMESTAMP '1992-09-20 20:38:40')` |
| **结果** | `1992-09-20 20:00:00` |

#### `dayname(timestamp)`

<div class="nostroke_table"></div>

| **描述** | 星期的英文名称。 |
| **示例** | `dayname(TIMESTAMP '1992-03-22')` |
| **结果** | `Sunday` |

#### `epoch_ms(ms)`

<div class="nostroke_table"></div>

| **描述** | 将自纪元以来的毫秒数转换为时间戳。 |
| **示例** | `epoch_ms(701222400000)` |
| **结果** | `1992-03-22 00:00:00` |

#### `epoch_ms(timestamp)`

<div class="nostroke_table"></div>

| **描述** | 返回自纪元以来的总毫秒数。 |
| **示例** | `epoch_ms(TIMESTAMP '2021-08-03 11:59:44.123456')` |
| **结果** | `1627991984123` |

#### `epoch_ns(timestamp)`

<div class="nostroke_table"></div>

| **描述** | 返回自纪元以来的总纳秒数。 |
| **示例** | `epoch_ns(TIMESTAMP '2021-08-03 11:59:44.123456')` |
| **结果** | `1627991984123456000` |

#### `epoch_us(timestamp)`

<div class="nostroke_table"></div>

| **描述** | 返回自纪元以来的总微秒数。 |
| **示例** | `epoch_us(TIMESTAMP '2021-08-03 11:59:44.123456')` |
| **结果** | `1627991984123456` |

#### `epoch(timestamp)`

<div class="nostroke_table"></div>

| **描述** | 返回自纪元以来的总秒数。 |
| **示例** | `epoch('2022-11-07 08:43:04'::TIMESTAMP);` |
| **结果** | `1667810584` |

#### `extract(field FROM timestamp)`

<div class="nostroke_table"></div>

| **描述** | 从时间戳中获取 [子字段]({% link docs/stable/sql/functions/datepart.md %})。 |
| **示例** | `extract('hour' FROM TIMESTAMP '1992-09-20 20:38:48')` |
| **结果** | `20` |

#### `greatest(timestamp, timestamp)`

<div class="nostroke_table"></div>

| **描述** | 两个时间戳中较晚的那个。 |
| **示例** | `greatest(TIMESTAMP '1992-09-20 20:38:48', TIMESTAMP '1992-03-22 01:02:03.1234')` |
| **结果** | `1992-09-20 20:38:48` |

#### `isfinite(timestamp)`

<div class="nostroke_table"></div>

| **描述** | 如果时间戳是有限的则返回 true，否则返回 false。 |
| **示例** | `isfinite(TIMESTAMP '1992-03-07')` |
| **结果** | `true` |

#### `isinf(timestamp)`

<div class="nostroke_table"></div>

| **描述** | 如果时间戳是无限的则返回 true，否则返回 false。 |
| **示例** | `isinf(TIMESTAMP '-infinity')` |
| **结果** | `true` |

#### `julian(timestamp)`

<div class="nostroke_table"></div>

| **描述** | 从时间戳中提取儒略日数。 |
| **示例** | `julian(TIMESTAMP '1992-03-22 01:02:03.1234')` |
| **结果** | `2448704.043091706` |

#### `last_day(timestamp)`

<div class="nostroke_table"></div>

| **描述** | 月份的最后一天。 |
| **示例** | `last_day(TIMESTAMP '1992-03-22 01:02:03.1234')` |
| **结果** | `1992-03-31` |

#### `least(timestamp, timestamp)`

<div class="nostroke_table"></div>

| **描述** | 两个时间戳中较早的那个。 |
| **示例** | `least(TIMESTAMP '1992-09-20 20:38:48', TIMESTAMP '1992-03-22 01:02:03.1234')` |
| **结果** | `1992-03-22 01:02:03.1234` |

#### `make_timestamp(bigint, bigint, bigint, bigint, bigint, double)`

<div class="nostroke_table"></div>

| **描述** | 给定部分的时间戳。 |
| **示例** | `make_timestamp(1992, 9, 20, 13, 34, 27.123456)` |
| **结果** | `1992-09-20 13:34:27.123456` |

#### `make_timestamp(microseconds)`

<div class="nostroke_table"></div>

| **描述** | 将自纪元以来的微秒数转换为时间戳。 |
| **示例** | `make_timestamp(1667810584123456)` |
| **结果** | `2022-11-07 08:43:04.123456` |

#### `make_timestamp_ns(nanoseconds)`

<div class="nostroke_table"></div>

| **描述** | 将自纪元以来的纳秒数转换为时间
| **示例** | `make_timestamp_ns(1667810584123456789)` |
| **结果** | `2022-11-07 08:43:04.123456789` |

#### `monthname(timestamp)`

<div class="nostroke_table"></div>

| **描述** | 月份的英文名称。 |
| **示例** | `monthname(TIMESTAMP '1992-09-20')` |
| **结果** | `September` |

#### `strftime(timestamp, format)`

<div class="nostroke_table"></div>

| **描述** | 根据 [格式字符串]({% link docs/stable/sql/functions/dateformat.md %}#format-specifiers) 将时间戳转换为字符串。 |
| **示例** | `strftime(timestamp '1992-01-01 20:38:40', '%a, %-d %B %Y - %I:%M:%S %p')` |
| **结果** | `Wed, 1 January 1992 - 08:38:40 PM` |

#### `strptime(text, format-list)`

<div class="nostroke_table"></div>

| **描述** | 将字符串 `text` 转换为时间戳，应用 [格式字符串]({% link docs/stable/sql/functions/dateformat.md %}) 列表中的格式，直到其中一个成功。失败时抛出错误。要返回 `NULL`，请使用 [`try_strptime`](#try_strptimetext-format-list)。 |
| **示例** | `strptime('4/15/2023 10:56:00', ['%d/%m/%Y %H:%M:%S', '%m/%d/%Y %H:%M:%S'])` |
| **结果** | `2023-04-15 10:56:00` |

#### `strptime(text, format)`

<div class="nostroke_table"></div>

| **描述** | 根据 [格式字符串]({% link docs/stable/sql/functions/dateformat.md %}#format-specifiers) 将字符串 `text` 转换为时间戳。失败时抛出错误。要返回 `NULL`，请使用 [`try_strptime`](#try_strptimetext-format)。 |
| **示例** | `strptime('Wed, 1 January 1992 - 08:38:40 PM', '%a, %-d %B %Y - %I:%M:%S %p')` |
| **结果** | `1992-01-01 20:38:40` |

#### `time_bucket(bucket_width, timestamp[, offset])`

<div class="nostroke_table"></div>

| **描述** | 将 `timestamp` 截断到宽度为 `bucket_width` 的网格。当 `bucket_width` 是月数或更粗的单位时，网格包括 `2000-01-01 00:00:00[ + offset]`，否则包括 `2000-01-03 00:00:00[ + offset]`。注意 `2000-01-03` 是星期一。 |
| **示例** | `time_bucket(INTERVAL '10 minutes', TIMESTAMP '1992-04-20 15:26:00-07', INTERVAL '5 minutes')` |
| **结果** | `1992-04-20 15:25:00` |

#### `time_bucket(bucket_width, timestamp[, origin])`

<div class="nostroke_table"></div>

| **描述** | 将 `timestamp` 截断到宽度为 `bucket_width` 的网格。网格包括 `origin` 时间戳，当 `bucket_width` 是月数或更粗的单位时，默认为 `2000-01-01 00:00:00`，否则为 `2000-01-03 00:00:00`。注意 `2000-01-03` 是星期一。 |
| **示例** | `time_bucket(INTERVAL '2 weeks', TIMESTAMP '1992-04-20 15:26:00', TIMESTAMP '1992-04-01 00:00:00')` |
| **结果** | `1992-04-15 00:00:00` |

#### `try_strptime(text, format-list)`

<div class="nostroke_table"></div>

| **描述** | 将字符串 `text` 转换为时间戳，应用 [格式字符串]({% link docs/stable/sql/functions/dateformat.md %}) 列表中的格式，直到其中一个成功。失败时返回 `NULL`。 |
| **示例** | `try_strptime('4/15/2023 10:56:00', ['%d/%m/%Y %H:%M:%S', '%m/%d/%Y %H:%M:%S'])` |
| **结果** | `2023-04-15 10:56:00` |

#### `try_strptime(text, format)`

<div class="nostroke_table"></div>

| **描述** | 根据 [格式字符串]({% link docs/stable/sql/functions/dateformat.md %}#format-specifiers) 将字符串 `text` 转换为时间戳。失败时返回 `NULL`。 |
| **示例** | `try_strptime('Wed, 1 January 1992 - 08:38:40 PM', '%a, %-d %B %Y - %I:%M:%S %p')` |
| **结果** | `1992-01-01 20:38:40` |

## 时间戳表函数

下表显示了 `TIMESTAMP` 类型可用的表函数。

| 名称 | 描述 |
|:--|:-------|
| [`generate_series(timestamp, timestamp, interval)`](#generate_seriestimestamp-timestamp-interval) | 生成一个闭区间的时间戳表，按间隔递增。 |
| [`range(timestamp, timestamp, interval)`](#rangetimestamp-timestamp-interval) | 生成一个半开区间的时间戳表，按间隔递增。 |

> 表函数的边界不允许使用无限值。

#### `generate_series(timestamp, timestamp, interval)`

<div class="nostroke_table"></div>

| **描述** | 生成一个闭区间的时间戳表，按间隔递增。 |
| **示例** | `generate_series(TIMESTAMP '2001-04-10', TIMESTAMP '2001-04-11', INTERVAL 30 MINUTE)` |

#### `range(timestamp, timestamp, interval)`

<div class="nostroke_table"></div>

| **描述** | 生成一个半开区间的时间戳表，按间隔递增。 |
| **示例** | `range(TIMESTAMP '2001-04-10', TIMESTAMP '2001-04-11', INTERVAL 30 MINUTE)` |