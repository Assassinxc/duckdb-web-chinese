---
---
blurb: 日期表示年、月和日的组合。
layout: docu
redirect_from:
- /docs/sql/data_types/date
title: 日期类型
---

| 名称   | 别名 | 描述                     |
|:-------|:-----|:--------------------------|
| `DATE` |      | 日历日期（年、月、日）   |

日期表示年、月和日的组合。DuckDB遵循SQL标准，仅使用公历计算日期，即使是在该历法投入使用之前。日期可以通过`DATE`关键字创建，数据必须按照ISO 8601格式（`YYYY-MM-DD`）进行格式化。

```sql
SELECT DATE '1992-09-20';
```

## 特殊值

输入时还可以使用三个特殊日期值：

| 输入字符串 | 描述                         |
|:-----------|:-----------------------------|
| epoch      | 1970-01-01（Unix系统零日）   |
| infinity   | 比所有其他日期都晚           |
| -infinity  | 比所有其他日期都早           |

`infinity`和`-infinity`在系统内部有特殊表示，并且在显示时保持不变；而`epoch`只是一个符号表示，在读取时会被转换为对应的日期值。

```sql
SELECT
    '-infinity'::DATE AS negative,
    'epoch'::DATE AS epoch,
    'infinity'::DATE AS positive;
```

| negative  |   epoch    | positive |
|-----------|------------|----------|
| -infinity | 1970-01-01 | infinity |

## 函数

参见 [日期函数]({% link docs/stable/sql/functions/date.md %})。