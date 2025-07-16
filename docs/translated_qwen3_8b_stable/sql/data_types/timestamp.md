---
---
blurb: 时间戳表示时间点。
layout: docu
redirect_from:
- /docs/sql/data_types/timestamp
title: 时间戳类型
---

时间戳表示时间点。因此，它们结合了 [`DATE`]({% link docs/stable/sql/data_types/date.md %}) 和 [`TIME`]({% link docs/stable/sql/data_types/time.md %}) 的信息。
它们可以通过使用符合 ISO 8601 格式 `YYYY-MM-DD hh:mm:ss[.zzzzzzzzz][+-TT[:tt]]` 的字符串和类型名来创建，这也是我们在此文档中使用的格式。超出支持精度的小数位将被忽略。

## 时间戳类型

| 名称 | 别名 | 描述 |
|:---|:---|:---|
| `TIMESTAMP_NS` |                                           | 无时区信息的时间戳，精度为纳秒 |
| `TIMESTAMP`    | `DATETIME`, `TIMESTAMP WITHOUT TIME ZONE` | 无时区信息的时间戳，精度为微秒 |
| `TIMESTAMP_MS` |                                           | 无时区信息的时间戳，精度为毫秒 |
| `TIMESTAMP_S`  |                                           | 无时区信息的时间戳，精度为秒 |
| `TIMESTAMPTZ`  | `TIMESTAMP WITH TIME ZONE`                | 时区感知时间戳，精度为微秒 |

> 警告：目前没有 `TIMESTAMP_NS WITH TIME ZONE` 数据类型，因此具有纳秒精度和 `WITH TIME ZONE` 语义的外部列（例如 [具有 `isAdjustedToUTC=true` 的 Parquet 时间戳列](https://github.com/apache/parquet-format/blob/master/LogicalTypes.md#instant-semantics-timestamps-normalized-to-utc)）会被转换为 `TIMESTAMP WITH TIME ZONE`，从而在使用 DuckDB 读取时丢失精度。

```sql
SELECT TIMESTAMP_NS '1992-09-20 11:30:00.123456789';
```

```text
1992-09-20 11:30:00.123456789
```

```sql
SELECT TIMESTAMP '1992-09-20 11:30:00.123456789';
```

```text
1992-09-20 11:30:00.123456
```

```sql
SELECT TIMESTAMP_MS '1992-09-20 11:30:00.123456789';
```

```text
1992-09-20 11:30:00.123
```

```sql
SELECT TIMESTAMP_S '1992-09-20 11:30:00.123456789';
```

```text
1992-09-20 11:30:00
```

```sql
SELECT TIMESTAMPTZ '1992-09-20 11:30:00.123456789';
```

```text
1992-09-20 11:30:00.123456+00
```

```sql
SELECT TIMESTAMPTZ '1992-09-20 12:30:00.123456789+01:00';
```

```text
1992-09-20 11:30:00.123456+00
```

DuckDB 区分 `WITHOUT TIME ZONE` 和 `WITH TIME ZONE` 的时间戳（当前唯一代表是 `TIMESTAMP WITH TIME ZONE`）。

尽管名字中包含“时区”，但 `TIMESTAMP WITH TIME ZONE` 并不存储时区信息。相反，它仅存储自 Unix 时间点 `1970-01-01 00:00:00+00` 开始的非闰秒的 `INT64` 数值，因此可以无歧义地表示一个绝对时间点，或 [*instant*]({% link docs/stable/sql/data_types/timestamp.md %}#instants)。之所以使用 *time zone aware* 和 `WITH TIME ZONE` 的标签，是因为该类型的时间戳算术、[*binning*]({% link docs/stable/sql/data_types/timestamp.md %}#temporal-binning) 和字符串格式化操作是基于一个[配置时区]({% link docs/stable/sql/data_types/timestamp.md %}#time-zone-support) 进行的，默认是系统时区，如上面示例所示是 `UTC+00:00`。

对应的 `TIMESTAMP WITHOUT TIME ZONE` 存储相同的 `INT64` 值，但算术、binning 和字符串格式化遵循协调世界时（UTC）的简单规则，不考虑偏移量或时区。因此，`TIMESTAMP` 可以被解释为 UTC 时间戳，但更常见的是用于表示在未指定时区中记录的 *本地* 时间观察值，对这些类型的操作可以被解释为按照名义时间逻辑简单操作元组字段。将此类观察值进行区分是常见的数据清洗问题，这些观察值可能以没有时区说明或 UTC 偏移量的原始字符串形式存储，可以转换为无歧义的 `TIMESTAMP WITH TIME ZONE` 时间点。一种可能的解决方案是向字符串追加 UTC 偏移量，然后显式转换为 `TIMESTAMP WITH TIME ZONE`。另一种方法是首先创建 `TIMESTAMP WITHOUT TIME ZONE`，然后将其与时区说明结合以获得时区感知的 `TIMESTAMP WITH TIME ZONE`。

## 字符串与朴素/时区感知时间戳之间的转换

字符串 *无* UTC 偏移量或 IANA 时区名称和 `WITHOUT TIME ZONE` 类型之间的转换是无歧义且直接的。
字符串 *有* UTC 偏移量或时区名称和 `WITH TIME ZONE` 类型之间的转换也是无歧义的，但需要 `ICU` 扩展来处理时区名称。

当字符串 *无* UTC 偏移量或时区名称被转换为 `WITH TIME ZONE` 类型时，字符串将在配置的时区中解释。相反，当字符串 *有* UTC 偏移量传递给 `WITHOUT TIME ZONE` 类型时，会存储配置时区中指定时间点的本地时间。

最后，当 `WITH TIME ZONE` 和 `WITHOUT TIME ZONE` 类型通过显式或隐式转换相互转换时，转换使用配置的时区。若要使用其他时区，可以使用 `ICU` 扩展提供的 `timezone` 函数：

```sql
SELECT
    timezone('America/Denver', TIMESTAMP '2001-02-16 20:38:40') AS aware1,
    timezone('America/Denver', TIMESTAMPTZ '2001-02-16 04:38:40') AS naive1,
    timezone('UTC', TIMESTAMP '2001-02-16 20:38:40+00:00') AS aware2,
    timezone('UTC', TIMESTAMPTZ '2001-02-16 04:38:40 Europe/Berlin') AS naive2;
```

<div class="monospace_table"></div>

|         aware1         |       naive1        |         aware2         |       naive2        |
|------------------------|---------------------|------------------------|---------------------|
| 2001-02-17 04:38:40+01 | 2001-02-15 20:38:40 | 2001-02-16 21:38:40+01 | 2001-02-16 03:38:40 |

请注意，`TIMESTAMP` 在结果中不包含时区说明，遵循 ISO 8601 对本地时间的规则，而时区感知的 `TIMESTAMPTZ` 会显示配置时区的 UTC 偏移量，如示例中所示为 `'Europe/Berlin'`。`'America/Denver'` 和 `'Europe/Berlin'` 在所有涉及的时刻的 UTC 偏移量分别为 `-07:00` 和 `+01:00`。

## 特殊值

可以使用三个特殊字符串来创建时间戳：

| 输入字符串 | 描述                                      |
|:-----------|:------------------------------------------|
| `epoch`    | 1970-01-01 00:00:00[+00]（Unix 系统时间零） |
| `infinity` | 比所有其他时间戳都晚                       |
| `-infinity`| 比所有其他时间戳都早                       |

`infinity` 和 `-infinity` 是特殊值，在显示时保持不变，而 `epoch` 是一个记号，读取时会转换为对应的日期时间值。

```sql
SELECT '-infinity'::TIMESTAMP, 'epoch'::TIMESTAMP, 'infinity'::TIMESTAMP;
```

| Negative  | Epoch               | Positive |
|:----------|:--------------------|:---------|
| -infinity | 1970-01-01 00:00:00 | infinity |

## 函数

参见 [时间戳函数]({% link docs/stable/sql/functions/timestamp.md %}).

## 时区

要理解时区和 `WITH TIME ZONE` 类型，从两个概念开始会很有帮助：*instant*（时间点）和 *temporal binning*（时间分桶）。

### 时间点

时间点是绝对时间的一个点，通常以某个固定时间点（称为 *epoch*）的计数表示。这类似于通过纬度和经度相对于赤道和格林威治子午线来表示地球表面的位置。在 DuckDB 中，固定时间点是 Unix 时间点 `1970-01-01 00:00:00+00:00`，计数单位可以是秒、毫秒、微秒或纳秒，具体取决于数据类型。

### 时间分桶

分桶是连续数据的一种常见做法：将可能的值范围划分为连续的子集，分桶操作将实际值映射到它们所属的 *桶*。*时间分桶* 就是将这种做法应用于时间点；例如，将时间点分桶为年、月和日。

<img src="/images/blog/timezones/tz-instants.svg"
     alt="时区时间点在纪元时"
     width=600
     />

时间分桶规则较为复杂，通常分为两组：*时区* 和 *日历*。
对于大多数任务，日历将只是广泛使用的格里高利历，
但时区应用本地化规则，差异可能很大。
例如，下面是 `'America/Los_Angeles'` 时区在纪元附近的时间分桶示例：

<img src="/images/blog/timezones/tz-timezone.svg"
     alt="纪元时的两个时区"
     width=600
     />

最常见的时间分桶问题发生在夏令时变更期间。
下面的示例包含一个夏令时变更，其中“小时”桶为两小时长。
为了区分这两个小时，需要另一个包含与 UTC 偏移量的分桶范围：

<img src="/images/blog/timezones/tz-daylight.svg"
     alt="夏令时过渡时的两个时区"
     width=600
     />

### 时区支持

`TIMESTAMPTZ` 类型可以通过合适的扩展进行分桶，以使用日历和时钟分桶。
内置的 [ICU 扩展]({% link docs/stable/core_extensions/icu.md %}) 使用 [Unicode 国际组件](https://icu.unicode.org) 的时区和日历函数实现所有分桶和算术操作。

要设置使用的时区，首先加载 ICU 扩展。ICU 扩展已预装在多个 DuckDB 客户端中（包括 Python、R、JDBC 和 ODBC），因此在这些情况下可以跳过此步骤。在其他情况下，您可能需要首先安装并加载 ICU 扩展。

```sql
INSTALL icu;
LOAD icu;
```

接下来，使用 `SET TimeZone` 命令：

```sql
SET TimeZone = 'America/Los_Angeles';
```

`TIMESTAMPTZ` 的时间分桶操作将使用指定的时区进行。

可以从 `pg_timezone_names()` 表函数中获取可用时区列表：

```sql
SELECT
    name,
    abbrev,
    utc_offset
FROM pg_timezone_names()
ORDER BY
    name;
```

您还可以从 [可用时区列表]({% link docs/stable/sql/data_types/timezones.md %}) 获取参考表。

## 日历支持

[ICU 扩展]({% link docs/stable/core_extensions/icu.md %}) 也支持非格里高利历，使用 `SET Calendar` 命令。
请注意，如果 DuckDB 客户端未捆绑 ICU 扩展，则需要执行 `INSTALL` 和 `LOAD` 步骤。

```sql
INSTALL icu;
LOAD icu;
SET Calendar = 'japanese';
```

`TIMESTAMPTZ` 的时间分桶操作将使用指定的日历进行。
在此示例中，`era` 部分现在将报告日本帝国纪年。

可以从 `icu_calendar_names()` 表函数中获取可用日历列表：

```sql
SELECT name
FROM icu_calendar_names()
ORDER BY 1;
```

## 设置

`TimeZone` 和 `Calendar` 设置的当前值由 ICU 在启动时确定。
它们可以从 `duckdb_settings()` 表函数中查询：

```sql
SELECT *
FROM duckdb_settings()
WHERE name = 'TimeZone';
```

|   name   |      value       |      description      | input_type |
|----------|------------------|-----------------------|------------|
| TimeZone | Europe/Amsterdam | 当前时区              | VARCHAR    |

```sql
SELECT *
FROM duckdb_settings()
WHERE name = 'Calendar';
```

|   name   |   value   |     description      | input_type |
|----------|-----------|----------------------|------------|
| Calendar | gregorian | 当前日历             | VARCHAR    |

> 如果您发现分桶操作没有按照预期进行，请检查 `TimeZone` 和 `Calendar` 值，并在需要时进行调整。