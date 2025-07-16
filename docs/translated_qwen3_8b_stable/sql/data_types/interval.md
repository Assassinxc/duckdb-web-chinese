---
---
blurb: Intervals 表示以月、日、微秒，或这些单位的组合形式度量的时间段。
layout: docu
redirect_from:
- /docs/sql/data_types/interval
title: Interval 类型
---

`INTERVAL` 表示可以加到或减去 `DATE`、`TIMESTAMP`、`TIMESTAMPTZ` 或 `TIME` 值的时间段。

| 名称 | 描述 |
|:---|:---|
| `INTERVAL` | 时间段 |

可以通过提供数值和单位来构造一个 `INTERVAL`。不是 *月*、*日* 或 *微秒* 的单位会转换为这三个基础单位中更小的单位的等效数值。

```sql
SELECT
    INTERVAL 1 YEAR, -- 使用 YEAR 关键字的单个单位；存储为 12 个月
    INTERVAL (random() * 10) YEAR, -- 需要括号用于变量数值；
                                   -- 存储为整数月数
    INTERVAL '1 month 1 day', -- 需要字符串类型用于多个单位；存储为 (1 个月, 1 天)
    '16 months'::INTERVAL, -- 支持字符串类型转换；存储为 16 个月
    '48:00:00'::INTERVAL, -- 支持 HH::MM::SS 字符串；存储为 (48 * 60 * 60 * 1e6 微秒)
;
```

> 警告：使用单位关键字时，十进制值会被截断为整数（除非单位是 `SECONDS` 或 `MILLISECONDS`）。
>
> ```sql
> SELECT INTERVAL '1.5' YEARS;
> -- 返回 12 个月；等同于 `to_years(CAST(trunc(1.5) AS INTEGER))`
> ```
>
> 为了更精确，可以在字符串中包含单位或使用更细粒度的单位；例如：`INTERVAL '1.5 years'` 或 `INTERVAL 18 MONTHS`。

需要三个基础单位，因为一个月不对应固定的天数（二月的天数比三月少），而一天也不对应固定的微秒数。将时间间隔分解为这些部分使 `INTERVAL` 类型适合于向日期添加或减去特定的时间单位。例如，我们可以使用以下 SQL 查询生成一个包含每个月第一天的表：

```sql
SELECT DATE '2000-01-01' + INTERVAL (i) MONTH
FROM range(12) t(i);
```

当通过 `datepart` 函数分解 `INTERVAL` 时，*months* 组件会被进一步拆分为年和月，*microseconds* 组件会被拆分为小时、分钟和微秒。*days* 组件不会被拆分为其他单位。为了演示这一点，以下查询通过将三个基础单位的随机值相加生成一个名为 `period` 的 `INTERVAL`。然后从 `period` 中提取上述六个部分，将它们加回去，并确认结果总是等于原始的 `period`。

```sql
SELECT
    period = list_reduce(
        [INTERVAL (datepart(part, period) || part) FOR part IN
             ['year', 'month', 'day', 'hour', 'minute', 'microsecond']
        ],
        (i1, i2) -> i1 + i2
    ) -- 总是成立
FROM (
    VALUES (
        INTERVAL (random() * 123_456_789_123) MICROSECONDS
        + INTERVAL (random() * 12_345) DAYS
        + INTERVAL (random() * 12_345) MONTHS
    )
) _(period);
```

> 警告：*microseconds* 组件仅被拆分为小时、分钟和微秒，而不是小时、分钟、*秒* 和微秒。

此外，`INTERVAL` 中的世纪、十年、季度、秒和毫秒的数量，可以通过 `datepart` 函数提取，且向下取整到最近的整数。然而，这些组件并不需要重新组合原始 `INTERVAL`。实际上，如果之前的查询还提取了十年或秒，那么提取的各个部分的总和通常会比原始的 `period` 大，因为这会分别重复计算月和微秒的部分。

> 所有单位使用 0 基索引，除了季度，使用 1 基索引。

例如：

```sql
SELECT
    datepart('decade', INTERVAL 12 YEARS), -- 返回 1
    datepart('year', INTERVAL 12 YEARS), -- 返回 12
    datepart('second', INTERVAL 1_234 MILLISECONDS), -- 返回 1
    datepart('microsecond', INTERVAL 1_234 MILLISECONDS), -- 返回 1_234_000
;
```

## 与时间戳、日期和间隔的运算

可以使用 `+` 和 `-` 运算符将 `INTERVAL` 加到或减去 `TIMESTAMP`、`TIMESTAMPTZ`、`DATE` 和 `TIME`。

```sql
SELECT
    DATE '2000-01-01' + INTERVAL 1 YEAR,
    TIMESTAMP '2000-01-01 01:33:30' - INTERVAL '1 month 13 hours',
    TIME '02:00:00' - INTERVAL '3 days 23 hours', -- 循环；等于 TIME '03:00:00'
;
```

> 将 `INTERVAL` 加到 `DATE` 返回一个 `TIMESTAMP`，即使 `INTERVAL` 没有微秒组件。结果等同于将 `DATE` 转换为 `TIMESTAMP`（将时间部分设置为 `00:00:00`）后再加 `INTERVAL`。

相反，从一个 `TIMESTAMP` 或 `TIMESTAMPTZ` 中减去另一个 `TIMESTAMP` 或 `TIMESTAMPTZ` 会创建一个描述两个时间戳之间差异的 `INTERVAL`，仅包含 *天数和微秒* 组件。例如：

```sql
SELECT
    TIMESTAMP '2000-02-06 12:00:00' - TIMESTAMP '2000-01-01 11:00:00', -- 36 天 1 小时
    TIMESTAMP '2000-02-01' + (TIMESTAMP '2000-02-01' - TIMESTAMP '2000-01-01'), -- '2000-03-03'，不是 '2000-03-01'
;
```

从一个 `DATE` 中减去另一个 `DATE` 不会创建一个 `INTERVAL`，而是返回两个日期之间的天数（作为整数值）。

> 警告：从两个 `TIMESTAMP` 之间提取 `INTERVAL` 的组件并不等同于使用 `datediff` 函数计算对应单位的分区边界数量：
>
> ```sql
> SELECT
>     datediff('day', TIMESTAMP '2020-01-01 01:00:00', TIMESTAMP '2020-01-02 00:00:00'), -- 1
>     datepart('day', TIMESTAMP '2020-01-02 00:00:00' - TIMESTAMP '2020-01-01 01:00:00'), -- 0
> ;
> ```

## 等式与比较

仅用于等式和排序比较时，`INTERVAL` 的总微秒数是通过将天数基础单位转换为 `24 * 60 * 60 * 1e6` 微秒，将月数基础单位转换为 30 天，或 `30 * 24 * 60 * 60 * 1e6` 微秒来计算的。

因此，即使 `INTERVAL` 在功能上不同，它们也可以比较相等，且当它们被加到日期或时间戳上时，`INTERVAL` 的顺序并不总是被保留。

例如：

* `INTERVAL 30 DAYS = INTERVAL 1 MONTH`
* 但 `DATE '2020-01-01' + INTERVAL 30 DAYS != DATE '2020-01-01' + INTERVAL 1 MONTH`。

和

* `INTERVAL '30 days 12 hours' > INTERVAL 1 MONTH`
* 但 `DATE '2020-01-01' + INTERVAL '30 days 12 hours' < DATE '2020-01-01' + INTERVAL 1 MONTH`。

## 函数

查看 [日期部分函数页面]({% link docs/stable/sql/functions/datepart.md %}) 以获取可用于 `INTERVAL` 的可用日期部分列表。

查看 [间隔运算符页面]({% link docs/stable/sql/functions/interval.md %}) 以获取用于间隔的函数。