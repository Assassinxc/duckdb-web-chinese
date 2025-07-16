---
---
layout: docu
redirect_from:
- /docs/sql/functions/dateformat
title: 日期格式函数
---

`strftime` 和 `strptime` 函数可用于在 [`DATE`]({% link docs/stable/sql/data_types/date.md %}) / [`TIMESTAMP`]({% link docs/stable/sql/data_types/timestamp.md %}) 值和字符串之间进行转换。这在解析 CSV 文件、向用户显示输出或在程序之间传输信息时经常需要。由于存在许多可能的日期表示形式，这些函数接受一个 [格式字符串](#format-specifiers)，用于描述日期或时间戳应如何构造。

## `strftime` 示例

[`strftime(timestamp, format)`]({% link docs/stable/sql/functions/timestamp.md %}#strftimetimestamp-format) 根据指定的模式将时间戳或日期转换为字符串。

```sql
SELECT strftime(DATE '1992-03-02', '%d/%m/%Y');
```

```text
02/03/1992
```

```sql
SELECT strftime(TIMESTAMP '1992-03-02 20:32:45', '%A, %-d %B %Y - %I:%M:%S %p');
```

```text
Monday, 2 March 1992 - 08:32:45 PM
```

## `strptime` 示例

[`strptime(text, format)` 函数]({% link docs/stable/sql/functions/timestamp.md %}#strptimetext-format) 根据指定的模式将字符串转换为时间戳。

```sql
SELECT strptime('02/03/1992', '%d/%m/%Y');
```

```text
1992-03-02 00:00:00
```

```sql
SELECT strptime('Monday, 2 March 1992 - 08:32:45 PM', '%A, %-d %B %Y - %I:%M:%S %p');
```

```text
1992-03-02 20:32:45
```

`strptime` 函数在失败时会抛出错误：

```sql
SELECT strptime('02/50/1992', '%d/%m/%Y') AS x;
```

```console
Invalid Input Error: Could not parse string "02/50/1992" according to format specifier "%d/%m/%Y"
02/50/1992
   ^
Error: Month out of range, expected a value between 1 and 12
```

要返回 `NULL`，请使用 [`try_strptime` 函数]({% link docs/stable/sql/functions/timestamp.md %}#try_strptimetext-format)：

```text
NULL
```

## CSV 解析

在 CSV 解析过程中也可以指定日期格式，可以在 [`COPY` 语句]({% link docs/stable/sql/statements/copy.md %}) 或 `read_csv` 函数中指定。可以通过指定 `DATEFORMAT` 或 `TIMESTAMPFORMAT`（或两者）来实现这一点。`DATEFORMAT` 用于转换日期，`TIMESTAMPFORMAT` 用于转换时间戳。以下是使用方法的一些示例。

在 `COPY` 语句中：

```sql
COPY dates FROM 'test.csv' (DATEFORMAT '%d/%m/%Y', TIMESTAMPFORMAT '%A, %-d %B %Y - %I:%M:%S %p');
```

在 `read_csv` 函数中：

```sql
SELECT *
FROM read_csv('test.csv', dateformat = '%m/%d/%Y', timestampformat = '%A, %-d %B %Y - %I:%M:%S %p');
```

## 格式说明符

以下是所有可用格式说明符的完整列表。

| 说明符 | 描述 | 示例 |
|:-|:------|:---|
| `%a` | 缩写星期名称。 | Sun, Mon, ... |
| `%A` | 完整星期名称。 | Sunday, Monday, ... |
| `%b` | 缩写月份名称。 | Jan, Feb, ..., Dec |
| `%B` | 完整月份名称。 | January, February, ... |
| `%c` | ISO 日期和时间表示 | 1992-03-02 10:30:20 |
| `%d` | 月份中的日期，以零填充的十进制数字表示。 | 01, 02, ..., 31 |
| `%-d` | 月份中的日期，以十进制数字表示。 | 1, 2, ..., 30 |
| `%f` | 微秒，以十进制数字表示，左侧补零。 | 000000 - 999999 |
| `%g` | 毫秒，以十进制数字表示，左侧补零。 | 000 - 999 |
| `%G` | ISO 8601 年份，表示包含大部分 ISO 周年的年份（参见 `%V`）。 | 0001, 0002, ..., 2013, 2014, ..., 9998, 9999 |
| `%H` | 24 小时制的小时，以零填充的十进制数字表示。 | 00, 01, ..., 23 |
| `%-H` | 24 小时制的小时，以十进制数字表示。 | 0, 1, ..., 23 |
| `%I` | 12 小时制的小时，以零填充的十进制数字表示。 | 01, 02, ..., 12 |
| `%-I` | 12 小时制的小时，以十进制数字表示。 | 1, 2, ... 12 |
| `%j` | 一年中的第几天，以零填充的十进制数字表示。 | 001, 002, ..., 366 |
| `%-j` | 一年中的第几天，以十进制数字表示。 | 1, 2, ..., 366 |
| `%m` | 月份，以零填充的十进制数字表示。 | 01, 02, ..., 12 |
| `%-m` | 月份，以十进制数字表示。 | 1, 2, ..., 12 |
| `%M` | 分钟，以零填充的十进制数字表示。 | 00, 01, ..., 59 |
| `%-M` | 分钟，以十进制数字表示。 | 0, 1, ..., 59 |
| `%n` | 纳秒，以十进制数字表示，左侧补零。 | 000000000 - 999999999 |
| `%p` | 当地的 AM 或 PM。 | AM, PM |
| `%S` | 秒，以零填充的十进制数字表示。 | 00, 01, ..., 59 |
| `%-S` | 秒，以十进制数字表示。 | 0, 1, ..., 59 |
| `%u` | ISO 8601 星期，以十进制数字表示，其中 1 表示星期一。 | 1, 2, ..., 7 |
| `%U` | 一年中的周数。周 01 从当年的第一个星期日开始，因此可能会有周 00。请注意，这不符合 ISO-8601 的周日期标准。 | 00, 01, ..., 53 |
| `%V` | ISO 8601 周，以十进制数字表示，星期一为一周的第一天。周 01 是包含 1 月 4 日的周。请注意 `%V` 与年指令 `%Y` 不兼容。请改用 ISO 年 `%G`。 | 01, ..., 53 |
| `%w` | 星期，以十进制数字表示。 | 0, 1, ..., 6 |
| `%W` | 一年中的周数。周 01 从当年的第一个星期一开始，因此可能会有周 00。请注意，这不符合 ISO-8601 的周日期标准。 | 00, 01, ..., 53 |
| `%x` | ISO 日期表示 | 1992-03-02 |
| `%X` | ISO 时间表示 | 10:30:20 |
| `%y` | 不带世纪的年份，以零填充的十进制数字表示。 | 00, 01, ..., 99 |
| `%-y` | 不带世纪的年份，以十进制数字表示。 | 0, 1, ..., 99 |
| `%Y` | 带世纪的年份，以十进制数字表示。 | 2013, 2019 等。 |
| `%z` | [UTC 的时间偏移量](https://en.wikipedia.org/wiki/ISO_8601#Time_offsets_from_UTC)，形式为 ±HH:MM、±HHMM 或 ±HH。 | -0700 |
| `%Z` | 时区名称。 | Europe/Amsterdam  |
| `%%` | 字面量 `%` 字符。 | % |