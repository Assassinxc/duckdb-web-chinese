---
---
layout: docu
redirect_from:
- /docs/guides/sql_features/asof_join
title: AsOf Join
---

## 什么是AsOf Join？

时间序列数据并不总是完全对齐。
时钟可能会有轻微偏差，或者因果之间可能存在延迟。
这使得连接两个有序数据集变得具有挑战性。
AsOf Join 是解决此类问题及其他类似问题的工具之一。

AsOf Join 用于解决的问题之一是
在特定时间点查找一个变化属性的值。
这个用例非常常见，因此名称也由此而来：

_给我这个时间点的属性值_。

更一般而言，AsOf Join 体现了一些常见的时态分析语义，
这些语义在标准 SQL 中实现起来可能繁琐且效率低下。

## 投资组合示例数据集

让我们从一个具体示例开始。
假设我们有一个股票 [`prices`](/data/prices.csv) 表，包含时间戳：

| ticker | when | price |
| :----- | :--- | ----: |
| APPL   | 2001-01-01 00:00:00 | 1 |
| APPL   | 2001-01-01 00:01:00 | 2 |
| APPL   | 2001-01-01 00:02:00 | 3 |
| MSFT   | 2001-01-01 00:00:00 | 1 |
| MSFT   | 2001-01-01 00:01:00 | 2 |
| MSFT   | 2001-01-01 00:02:00 | 3 |
| GOOG   | 2001-01-01 00:00:00 | 1 |
| GOOG   | 2001-01-01 00:01:00 | 2 |
| GOOG   | 2001-01-01 00:02:00 | 3 |

我们还有另一个表，包含投资组合 [`holdings`](/data/holdings.csv) 在不同时间点的数据：

| ticker | when | shares |
| :----- | :--- | -----: |
| APPL   | 2000-12-31 23:59:30 | 5.16   |
| APPL   | 2001-01-01 00:00:30 | 2.94   |
| APPL   | 2001-01-01 00:01:30 | 24.13  |
| GOOG   | 2000-12-31 23:59:30 | 9.33   |
| GOOG   | 2001-01-01 00:00:30 | 23.45  |
| GOOG   | 2001-01-01 00:01:30 | 10.58  |
| DATA   | 2000-12-31 23:59:30 | 6.65   |
| DATA   | 2001-01-01 00:00:30 | 17.95  |
| DATA   | 2001-01-01 00:01:30 | 18.37  |

要将这些表加载到 DuckDB 中，运行以下 SQL：

```sql
CREATE TABLE prices AS FROM 'https://duckdb.org/data/prices.csv';
CREATE TABLE holdings AS FROM 'https://duckdb.org/data/holdings.csv';
```

## 内部 AsOf Join

我们可以通过查找持有时间戳之前的最近价格来计算每个持有资产在该时间点的值，使用 AsOf Join：

```sql
SELECT h.ticker, h.when, price * shares AS value
FROM holdings h
ASOF JOIN prices p
       ON h.ticker = p.ticker
      AND h.when >= p.when;
```

这将把每个行在该时间点的持有资产价值附加：

| ticker | when | value |
| :----- | :--- | ----: |
| APPL   | 2001-01-01 00:00:30 | 2.94  |
| APPL   | 2001-01-01 00:01:30 | 48.26 |
| GOOG   | 2001-01-01 00:00:30 | 23.45 |
| GOOG   | 2001-01-01 00:01:30 | 21.16 |

它本质上是通过在 `prices` 表中查找附近的值来执行一个函数。
请注意，缺失的 `ticker` 值没有匹配项，也不会出现在输出中。

## 外部 AsOf Join

因为 AsOf 从右侧最多产生一个匹配项，
因此左侧表不会因为连接而增大，
但如果右侧有缺失时间，左侧表可能会变小。
为了处理这种情况，可以使用 *外部* AsOf Join：

```sql
SELECT h.ticker, h.when, price * shares AS value
FROM holdings h
ASOF LEFT JOIN prices p
            ON h.ticker = p.ticker
           AND h.when >= p.when
ORDER BY ALL;
```

正如你可能预期的那样，当没有 ticker 或时间早于价格开始时，
它将产生 `NULL` 的价格和值，而不是删除左侧行。

| ticker | when | value |
| :----- | :--- | ----: |
| APPL   | 2000-12-31 23:59:30 |       |
| APPL   | 2001-01-01 00:00:30 | 2.94  |
| APPL   | 2001-01-01 00:01:30 | 48.26 |
| GOOG   | 2000-12-31 23:59:30 |       |
| GOOG   | 2001-01-01 00:00:30 | 23.45 |
| GOOG   | 2001-01-01 00:01:30 | 21.16 |
| DATA   | 2000-12-31 23:59:30 |       |
| DATA   | 2001-01-01 00:00:30 |       |
| DATA   | 2001-01-01 00:01:30 |       |

## 使用 `USING` 关键字的 AsOf Join

到目前为止，我们已经明确地指定了 AsOf 的条件，
但 SQL 也有一个简化连接条件的语法，
用于列名在两个表中相同的情况。
该语法使用 `USING` 关键字列出应比较相等的字段。
AsOf 也支持此语法，但有两个限制：

* 最后一个字段是不等式
* 不等式是 `>=`（最常见的用例）

因此，我们的第一个查询可以写成：

```sql
SELECT ticker, h.when, price * shares AS value
FROM holdings h
ASOF JOIN prices p USING (ticker, "when");
```

### 关于 `USING` 在 AsOf Join 中列选择的说明

在连接中使用 `USING` 关键字时，`USING` 子句中指定的列会被合并到结果集中。这意味着如果你运行：

```sql
SELECT *
FROM holdings h
ASOF JOIN prices p USING (ticker, "when");
```

你将只得到列 `h.ticker, h.when, h.shares, p.price`。列 `ticker` 和 `when` 会只出现一次，其中 `ticker` 和 `when` 来自左侧表（holdings）。

这种行为对于 `ticker` 列来说是合适的，因为两个表中的值是相同的。然而，对于 `when` 列，由于 AsOf Join 使用了 `>=` 条件，两个表中的值可能会不同。AsOf Join 的设计是为了根据 `when` 列将左侧表（holdings）中的每一行与右侧表（prices）中最近的前一行进行匹配。

如果你想从两个表中获取 `when` 列以查看两个时间戳，你需要显式列出列，而不是依赖 `*`，如下所示：

```sql
SELECT h.ticker, h.when AS holdings_when, p.when AS prices_when, h.shares, p.price
FROM holdings h
ASOF JOIN prices p USING (ticker, "when");
```

这可以确保你获得两个表的完整信息，避免 `USING` 关键字默认行为可能引起的任何混淆。

## 参见

有关实现细节，请参阅 [博客文章“DuckDB 的 AsOf Join：模糊时间查找”]({% post_url 2023-09-15-asof-joins-fuzzy-temporal-lookups %})。