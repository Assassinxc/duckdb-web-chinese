---
---
layout: docu
redirect_from:
- /docs/sql/functions/datepart
title: 日期部分函数
---

<!-- markdownlint-disable MD001 -->

`date_part`、`date_diff` 和 `date_trunc` 函数可用于操作 [`DATE`]({% link docs/stable/sql/data_types/date.md %}) 和 [`TIMESTAMP`]({% link docs/stable/sql/data_types/timestamp.md %}) 等时间类型字段。
字段通过包含字段名称的字符串进行指定。

以下是所有可用的日期部分指定符的完整列表。
示例是时间戳 `2021-08-03 11:59:44.123456` 对应的部分。

## 可用作日期部分指定符和区间中的部分指定符

| 指定符 | 描述 | 同义词 | 示例 |
|:--|:--|:---|--:|
| `century` | 格里高利世纪 | `cent`, `centuries`, `c` | `21` |
| `day` | 格里高利日 | `days`, `d`, `dayofmonth` | `3` |
| `decade` | 格里高利十年 | `dec`, `decades`, `decs` | `202` |
| `hour` | 小时 | `hr`, `hours`, `hrs`, `h` | `11` |
| `microseconds` | 分钟内的微秒 | `microsecond`, `us`, `usec`, `usecs`, `usecond`, `useconds` | `44123456` |
| `millennium` | 格里高利千禧年 | `mil`, `millenniums`, `millenia`, `mils`, `millenium` | `3` |
| `milliseconds` | 分钟内的毫秒 | `millisecond`, `ms`, `msec`, `msecs`, `msecond`, `mseconds` | `44123` |
| `minute` | 分钟 | `min`, `minutes`, `mins`, `m` | `59` |
| `month` | 格里高利月 | `mon`, `months`, `mons` | `8` |
| `quarter` | 年的季度（1-4） | `quarters` | `3` |
| `second` | 秒 | `sec`, `seconds`, `secs`, `s` | `44` |
| `year` | 格里高利年 | `yr`, `y`, `years`, `yrs` | `2021` |

## 仅可用作日期部分指定符的部分指定符

| 指定符 | 描述 | 同义词 | 示例 |
|:--|:--|:---|--:|
| `dayofweek` | 星期几（周日 = 0，周六 = 6） | `weekday`, `dow` | `2` |
| `dayofyear` | 一年中的第几天（1-365/366） | `doy` | `215` |
| `epoch` | 自 1970-01-01 以来的秒数 | | `1627991984` |
| `era` | 格里高利纪元（公元/AD，公元前/BC） | | `1` |
| `isodow` | ISO 星期几（周一 = 1，周日 = 7） | | `2` |
| `isoyear` | ISO 年份（以包含 1 月 4 日的周周一为起始） | | `2021` |
| `timezone_hour` | 时区偏移小时部分 | | `0` |
| `timezone_minute` | 时区偏移分钟部分 | | `0` |
| `timezone` | 时区偏移秒数 | | `0` |
| `week` | 周数 | `weeks`, `w` | `31` |
| `yearweek` | 以 `YYYYWW` 格式表示的 ISO 年份和周数 | | `202131` |

请注意，时区部分在未安装如 [ICU]({% link docs/stable/core_extensions/icu.md %}) 等扩展以支持 `TIMESTAMP WITH TIME ZONE` 时，均为零。

## 部分函数

有一些专用的提取函数用于获取某些子字段：

| 名称 | 描述 |
|:--|:-------|
| [`century(date)`](#centurydate) | 世纪。 |
| [`day(date)`](#daydate) | 日。 |
| [`dayofmonth(date)`](#dayofmonthdate) | 日（同义词）。 |
| [`dayofweek(date)`](#dayofweekdate) | 数字星期几（周日 = 0，周六 = 6）。 |
| [`dayofyear(date)`](#dayyeardate) | 年中的第几天（从 1 开始，即 1 月 1 日 = 1）。 |
| [`decade(date)`](#decadedate) | 十年（年 / 10）。 |
| [`epoch(date)`](#epochdate) | 自 1970-01-01 以来的秒数。 |
| [`era(date)`](#eradate) | 历法纪元。 |
| [`hour(date)`](#hourdate) | 小时。 |
| [`isodow(date)`](#isodowdate) | 数字 ISO 星期几（周一 = 1，周日 = 7）。 |
| [`isoyear(date)`](#isoyeardate) | ISO 年份（以包含 1 月 4 日的周周一为起始）。 |
| [`microsecond(date)`](#microseconddate) | 分钟内的微秒。 |
| [`millennium(date)`](#millenniumdate) | 千禧年。 |
| [`millisecond(date)`](#milliseconddate) | 分钟内的毫秒。 |
| [`minute(date)`](#minutedate) | 分钟。 |
| [`month(date)`](#monthdate) | 月份。 |
| [`quarter(date)`](#quarterdate) | 季度。 |
| [`second(date)`](#seconddate) | 秒。 |
| [`timezone_hour(date)`](#timezone_hourdate) | 时区偏移小时部分。 |
| [`timezone_minute(date)`](#timezone_minutedate) | 时区偏移分钟部分。 |
| [`timezone(date)`](#timezonedate) | 时区偏移秒数。 |
| [`week(date)`](#weekdate) | ISO 周。 |
| [`weekday(date)`](#weekdaydate) | 数字星期几同义词（周日 = 0，周六 = 6）。 |
| [`weekofyear(date)`](#weekofyeardate) | ISO 周（同义词）。 |
| [`year(date)`](#yeardate) | 年。 |
| [`yearweek(date)`](#yearweekdate) | ISO 年份和 2 位 ISO 周数的组合 `BIGINT`。 |

#### `century(date)`

<div class="nostroke_table"></div>

| **描述** | 世纪。 |
| **示例** | `century(DATE '1992-02-15')` |
| **结果** | `20` |

#### `day(date)`

<div class="nostroke_table"></div>

| **描述** | 日。 |
| **示例** | `day(DATE '1992-02-15')` |
| **结果** | `15` |

#### `dayofmonth(date)`

<div class="nostroke_table"></div>

| **描述** | 日（同义词）。 |
| **示例** | `dayofmonth(DATE '1992-02-15')` |
| **结果** | `15` |

#### `dayofweek(date)`

<div class="nostroke_table"></div>

| **描述** | 数字星期几（周日 = 0，周六 = 6）。 |
| **示例** | `dayofweek(DATE '1992-02-15')` |
| **结果** | `6` |

#### `dayofyear(date)`

<div class="nostroke_table"></div>

| **描述** | 年中的第几天（从 1 开始，即 1 月 1 日 = 1）。 |
| **示例** | `dayofyear(DATE '1992-02-15')` |
| **结果** | `46` |

#### `decade(date)`

<div class="nostroke_table"></div>

| **描述** | 十年（年 / 10）。 |
| **示例** | `decade(DATE '1992-02-15')` |
| **结果** | `199` |

#### `epoch(date)`

<div class="nostroke_table"></div>

| **描述** | 自 1970-01-01 以来的秒数。 |
| **示例** | `epoch(DATE '1992-02-15')` |
| **结果** | `698112000` |

#### `era(date)`

<div class="nostroke_table"></div>

| **描述** | 历法纪元。 |
| **示例** | `era(DATE '0044-03-15 (BC)')` |
| **结果** | `0` |

#### `hour(date)`

<div class="nostroke_table"></div>

| **描述** | 小时。 |
| **示例** | `hour(timestamp '2021-08-03 11:59:44.123456')` |
| **结果** | `11` |

#### `isodow(date)`

<div class="nostroke_table"></div>

| **描述** | 数字 ISO 星期几（周一 = 1，周日 = 7）。 |
| **示例** | `isodow(DATE '1992-02-15')` |
| **结果** | `6` |

#### `isoyear(date)`

<div class="nostroke_table"></div>

| **描述** | ISO 年份（以包含 1 月 4 日的周周一为起始）。 |
| **示例** | `isoyear(DATE '2022-01-01')` |
| **结果** | `2021` |

#### `microsecond(date)`

<div class="nostroke_table"></div>

| **描述** | 分钟内的微秒。 |
| **示例** | `microsecond(timestamp '2021-08-03 11:59:44.123456')` |
| **结果** | `44123456` |

#### `millennium(date)`

<div class="nostroke_table"></div>

| **描述** | 千禧年。 |
| **示例** | `millennium(DATE '1992-02-15')` |
| **结果** | `2` |

#### `millisecond(date)`

<div class="nostroke_table"></div>

| **描述** | 分钟内的毫秒。 |
| **示例** | `millisecond(timestamp '2021-08-03 11:59:44.123456')` |
| **结果** | `44123` |

#### `minute(date)`

<div class="nostroke_table"></div>

| **描述** | 分钟。 |
| **示例** | `minute(timestamp '2021-08-03 11:59:44.123456')` |
| **结果** | `59` |

#### `month(date)`

<div class="nostroke_table"></div>

| **描述** | 月份。 |
| **示例** | `month(DATE '1992-02-15')` |
| **结果** | `2` |

#### `quarter(date)`

<div class="nostroke_table"></div>

| **描述** | 季度。 |
| **示例** | `quarter(DATE '1992-02-15')` |
| **结果** | `1` |

#### `second(date)`

<div class="nostroke_table"></div>

| **描述** | 秒。 |
| **示例** | `second(timestamp '2021-08-03 11:59:44.123456')` |
| **结果** | `44` |

#### `timezone_hour(date)`

<div class="nostroke_table"></div>

| **描述** | 时区偏移小时部分。 |
| **示例** | `timezone_hour(DATE '1992-02-15')` |
| **结果** | `0` |

#### `timezone_minute(date)`

<div class="nostroke_table"></div>

| **描述** | 时区偏移分钟部分。 |
| **示例** | `timezone_minute(DATE '1992-02-15')` |
| **结果** | `0` |

#### `timezone(date)`

<div class="nostroke_table"></div>

| **描述** | 时区偏移秒数。 |
| **示例** | `timezone(DATE '1992-02-15')` |
| **结果** | `0` |

#### `week(date)`

<div class="nostroke_table"></div>

| **描述** | ISO 周。 |
| **示例** | `week(DATE '1992-02-15')` |
| **结果** | `7` |

#### `weekday(date)`

<div class="nostroke_table"></div>

| **描述** | 数字星期几同义词（周日 = 0，周六 = 6）。 |
| **示例** | `weekday(DATE '1992-02-15')` |
| **结果** | `6` |

#### `weekofyear(date)`

<div class="nostroke_table"></div>

| **描述** | ISO 周（同义词）。 |
| **示例** | `weekofyear(DATE '1992-02-15')` |
| **结果** | `7` |

#### `year(date)`

<div class="nostroke_table"></div>

| **描述** | 年。 |
| **示例** | `year(DATE '1992-02-15')` |
| **结果** | `1992` |

#### `yearweek(date)`

<div class="nostroke_table"></div>

| **描述** | ISO 年份和 2 位 ISO 周数的组合 `BIGINT`。 |
| **示例** | `yearweek(DATE '1992-02-15')` |
| **结果** | `199207` |