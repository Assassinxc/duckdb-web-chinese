---
---
layout: docu
railroad: expressions/aggregate.js
redirect_from:
- /docs/sql/aggregates
- /docs/sql/aggregates/
- /docs/sql/functions/aggregates
title: 聚合函数
---

<!-- markdownlint-disable MD001 -->

## 示例

生成一个包含 `amount` 列总和的单行：

```sql
SELECT sum(amount)
FROM sales;
```

为每个唯一的地区生成一行，包含每个组的 `amount` 总和：

```sql
SELECT region, sum(amount)
FROM sales
GROUP BY region;
```

只返回 `amount` 总和高于 100 的地区：

```sql
SELECT region
FROM sales
GROUP BY region
HAVING sum(amount) > 100;
```

返回 `region` 列中的唯一值数量：

```sql
SELECT count(DISTINCT region)
FROM sales;
```

返回两个值，`amount` 的总和以及 `amount` 减去地区为 `north` 的列的总和，使用 [`FILTER` 子句]({% link docs/stable/sql/query_syntax/filter.md %})：

```sql
SELECT sum(amount), sum(amount) FILTER (region != 'north')
FROM sales;
```

返回按 `amount` 列排序的所有地区列表：

```sql
SELECT list(region ORDER BY amount DESC)
FROM sales;
```

返回使用 `first()` 聚合函数的第一个销售金额：

```sql
SELECT first(amount ORDER BY date ASC)
FROM sales;
```

## 语法

<div id="rrdiagram"></div>

聚合函数是将多行 *组合* 成一个值的函数。聚合函数不同于标量函数和窗口函数，因为它们会改变结果的基数。因此，聚合函数只能在 SQL 查询的 `SELECT` 和 `HAVING` 子句中使用。

### 聚合函数中的 `DISTINCT` 子句

当提供 `DISTINCT` 子句时，计算聚合时只考虑不同的值。这通常与 `count` 聚合函数一起使用以获取不同元素的数量；但可以与系统中的任何聚合函数一起使用。
有一些聚合函数对重复值不敏感（例如 `min` 和 `max`），对于这些函数，该子句会被解析并忽略。

### 聚合函数中的 `ORDER BY` 子句

可以在函数调用的最后一个参数之后提供 `ORDER BY` 子句。注意子句前缺少逗号分隔符。

```sql
SELECT ⟨aggregate_function⟩(⟨arg⟩, ⟨sep⟩ ORDER BY ⟨ordering_criteria⟩);
```

此子句确保在应用函数之前对聚合值进行排序。
大多数聚合函数是顺序无关的，对于它们，此子句会被解析并丢弃。
然而，有一些顺序敏感的聚合函数在没有排序的情况下可能会产生非确定性结果，例如 `first`、`last`、`list` 和 `string_agg` / `group_concat` / `listagg`。
通过排序参数可以使这些函数变得确定。

例如：

```sql
CREATE TABLE tbl AS
    SELECT s FROM range(1, 4) r(s);

SELECT string_agg(s, ', ' ORDER BY s DESC) AS countdown
FROM tbl;
```

| countdown |
|-----------|
| 3, 2, 1   |

### 处理 `NULL` 值

所有通用聚合函数忽略 `NULL` 值，除了 [`list`](#listarg) ([`array_agg`](#array_aggarg))、[`first`](#firstarg) ([`arbitrary`](#arbitraryarg)) 和 [`last`](#lastarg)。
要从 `list` 中排除 `NULL` 值，可以使用 [`FILTER` 子句]({% link docs/stable/sql/query_syntax/filter.md %}).
要忽略 `first` 中的 `NULL` 值，可以使用 [`any_value` 聚合函数](#any_valuearg)。

所有通用聚合函数（除 [`count`](#countarg) 外）在空组中返回 `NULL`。
特别是，[`list`](#listarg) 不返回空列表，`sum` 不返回零，`string_agg` 不在这种情况返回空字符串。

## 通用聚合函数

下表显示了可用的通用聚合函数。

| 函数 | 描述 |
|:--|:--------|
| [`any_value(arg)`](#any_valuearg) | 返回 `arg` 中的第一个非 `NULL` 值。此函数 [受排序影响](#order-by-clause-in-aggregate-functions)。 |
| [`arbitrary(arg)`](#arbitraryarg) | 返回 `arg` 中的第一个值（`NULL` 或非 `NULL`）。此函数 [受排序影响](#order-by-clause-in-aggregate-functions)。 |
| [`arg_max(arg, val)`](#arg_maxarg-val) | 查找具有最大 `val` 的行，并计算该行的 `arg` 表达式。`arg` 或 `val` 表达式值为 `NULL` 的行将被忽略。此函数 [受排序影响](#order-by-clause-in-aggregate-functions)。 |
| [`arg_max(arg, val, n)`](#arg_maxarg-val-n) | `arg_max` 的通用情况，用于 `n` 值：返回一个 `LIST`，包含按 `val` 降序排列的前 `n` 行的 `arg` 表达式。此函数 [受排序影响](#order-by-clause-in-aggregate-functions)。 |
| [`arg_max_null(arg, val)`](#arg_max_nullarg-val) | 查找具有最大 `val` 的行，并计算该行的 `arg` 表达式。`val` 表达式评估为 `NULL` 的行将被忽略。此函数 [受排序影响](#order-by-clause-in-aggregate-functions)。 |
| [`arg_min(arg, val)`](#arg_minarg-val) | 查找具有最小 `val` 的行，并计算该行的 `arg` 表达式。`arg` 或 `val` 表达式值为 `NULL` 的行将被忽略。此函数 [受排序影响](#order-by-clause-in-aggregate-functions)。 |
| [`arg_min(arg, val, n)`](#arg_minarg-val-n) | 返回一个 `LIST`，包含按 `val` 升序排列的前 `n` 行的 `arg` 表达式。此函数 [受排序影响](#order-by-clause-in-aggregate-functions)。 |
| [`arg_min_null(arg, val)`](#arg_min_nullarg-val) | 查找具有最小 `val` 的行，并计算该行的 `arg` 表达式。`val` 表达式评估为 `NULL` 的行将被忽略。此函数 [受排序影响](#order-by-clause-in-aggregate-functions)。 |
| [`array_agg(arg)`](#array_aggarg) | 返回包含一列所有值的 `LIST`。此函数 [受排序影响](#order-by-clause-in-aggregate-functions)。 |
| [`avg(arg)`](#avgarg) | 计算 `arg` 中所有非 `NULL` 值的平均值。 |
| [`bit_and(arg)`](#bit_andarg) | 返回给定表达式中所有位的按位与。 |
| [`bit_or(arg)`](#bit_orarg) | 返回给定表达式中所有位的按位或。 |
| [`bit_xor(arg)`](#bit_xorarg) | 返回给定表达式中所有位的按位异或。 |
| [`bitstring_agg(arg)`](#bitstring_aggarg) | 返回一个位字符串，其长度对应于非 `NULL`（整数）值的范围，每个（不同的）值的位置设置为 1。 |
| [`bool_and(arg)`](#bool_andarg) | 如果所有输入值都为 `true`，返回 `true`，否则返回 `false`。 |
| [`bool_or(arg)`](#bool_orarg) | 如果任何输入值为 `true`，返回 `true`，否则返回 `false`。 |
| [`count()`](#count) | 返回组中的行数。 |
| [`count(arg)`](#countarg) | 返回 `arg` 中非 `NULL` 值的数量。 |
| [`countif(arg)`](#countifarg) | 返回组中 `arg` 为 `true` 的行数。 |
| [`favg(arg)`](#favgarg) | 使用更精确的浮点求和（Kahan Sum）计算平均值。 |
| [`first(arg)`](#firstarg) | 返回 `arg` 中的第一个值（`NULL` 或非 `NULL`）。此函数 [受排序影响](#order-by-clause-in-aggregate-functions)。 |
| [`fsum(arg)`](#fsumarg) | 使用更精确的浮点求和（Kahan Sum）计算总和。 |
| [`geomean(arg)`](#geomeanarg) | 计算 `arg` 中所有非 `NULL` 值的几何平均值。 |
| [`histogram(arg)`](#histogramarg) | 返回一个 `MAP`，表示桶和计数的键值对。 |
| [`histogram(arg, boundaries)`](#histogramarg-boundaries) | 返回一个 `MAP`，表示提供的上界 `boundaries` 和对应分桶（左开右闭）中的元素计数。如果元素大于所有提供的 `boundaries`，会自动添加一个位于数据类型最大值的边界。边界可以通过 [`equi_width_bins`]({% link docs/stable/sql/functions/utility.md %}#equi_width_binsminmaxbincountnice) 提供。 |
| [`histogram_exact(arg, elements)`](#histogram_exactarg-elements) | 返回一个 `MAP`，表示请求的元素及其计数。会自动添加一个特定于数据类型的通配符元素以计数其他元素。 |
| [`histogram_values(source, boundaries)`](#histogram_valuessource-col_name-technique-bin_count) | 返回分桶的上边界及其计数。 |
| [`kahan_sum(arg)`](#fsumarg) | 使用更精确的浮点求和（K,ahan Sum）计算总和。 |
| [`last(arg)`](#lastarg) | 返回列的最后一个值。此函数 [受排序影响](#order-by-clause-in-aggregate-functions)。 |
| [`list(arg)`](#listarg) | 返回包含一列所有值的 `LIST`。此函数 [受排序影响](#order-by-clause-in-aggregate-functions)。 |
| [`max(arg)`](#maxarg) | 返回 `arg` 中的最大值。此函数 [不受唯一性影响](#distinct-clause-in-aggregate-functions)。 |
| [`max(arg, n)`](#maxarg-n) | 返回一个 `LIST`，包含按 `arg` 降序排列的前 `n` 行的 `arg` 值。 |
| [`max_by(arg, val)`](#max_byarg-val) | 查找具有最大 `val` 的行，并计算该行的 `arg` 表达式。此函数 [受排序影响](#order-by-clause-in-aggregate-functions)。 |
| [`max_by(arg, val, n)`](#max_byarg-val-n) | 返回一个 `LIST`，包含按 `val` 降序排列的前 `n` 行的 `arg` 表达式。 |
| [`min(arg)`](#minarg) | 返回 `arg` 中的最小值。此函数 [不受唯一性影响](#distinct-clause-in-aggregate-functions)。 |
| [`min(arg, n)`](#minarg-n) | 返回一个 `LIST`，包含按 `arg` 升序排列的前 `n` 行的 `arg` 值。 |
| [`min_by(arg, val)`](#min_byarg-val) | 查找具有最小 `val` 的行，并计算该行的 `arg` 表达, 此函数 [受排序影响](#order-by-clause-in-aggregate-functions)。 |
| [`min_by(arg, val, n)`](#min_byarg-val-n) | 返回一个 `LIST`，包含按 `val` 升序排列的前 `n` 行的 `arg` 表达式。 |
| [`product(arg)`](#productarg) | 计算 `arg` 中所有非 `NULL` 值的乘积。 |
| [`string_agg(arg)`](#string_aggarg-sep) | 用逗号分隔符（`,`）连接列字符串值。此函数 [受排序影响](#order-by-clause-in-aggregate-functions)。 |
| [`string_agg(arg, sep)`](#string_aggarg-sep) | 用分隔符连接列字符串值。此函数 [受排序影响](#order-by-clause-in-aggregate-functions)。 |
| [`sum(arg)`](#sumarg) | 计算 `arg` 中所有非 `NULL` 值的总和 / 当 `arg` 是布尔值时计数 `true` 值。 |
| [`sumkahan(arg)`](#fsumarg) | 使用更精确的浮点求和（Kahan Sum）计算总和。 |
| [`weighted_avg(arg, weight)`](#weighted_avgarg-weight) | 计算 `arg` 中所有非 `NULL` 值的加权平均值，其中每个值根据其对应的 `weight` 进行缩放。如果 `weight` 为 `NULL`，则对应的 `arg` 值会被跳过。 |

#### `any_value(arg)`

<div class="nostroke_table"></div>

| **描述** | 返回 `arg` 中的第一个非 `NULL` 值。此函数 [受排序影响](#order-by-clause-in-aggregate-functions)。 |
| **示例** | `any_value(A)` |
| **别名** | - |

#### `arbitrary(arg)`

<div class="nostroke_table"></div>

| **描述** | 返回 `arg` 中的第一个值（`NULL` 或非 `NULL`）。此函数 [受排序影响](#order-by-clause-in-aggregate-functions)。 |
| **示例** | `arbitrary(A)` |
| **别名** | `first(A)` |

#### `arg_max(arg, val)`

<div class="nostroke_table"></div>

| **描述** | 查找具有最大 `val` 的行，并计算该行的 `arg` 表达式。`arg` 或 `val` 表达式值为 `NULL` 的行将被忽略。此函数 [受排序影响](#order-by-clause-in-aggregate-functions)。 |
| **示例** | `arg_max(A, B)` |
| **别名** | `argmax(arg, val)`, `max_by(arg, val)` |

#### `arg_max(arg, val, n)`

<div class="nostroke_table"></div>

| **描述** | `arg_max` 的通用情况，用于 `n` 值：返回一个 `LIST`，包含按 `val` 降序排列的前 `n` 行的 `arg` 表达式。此函数 [受排序影响](#order-by-clause-in-aggregate-functions)。 |
| **示例** | `arg_max(A, B, 2)` |
| **别名** | `argmax(arg, val, n)`, `max_by(arg, val, n)` |

#### `arg_max_null(arg, val)`

<div class="nostroke_table"></div>

| **描述** | 查找具有最大 `val` 的行，并计算该行的 `arg` 表达式。`val` 表达式评估为 `NULL` 的行将被忽略。此函数 [受排序影响](#order-by-clause-in-aggregate-functions)。 |
| **示例** | `arg_max_null(A, B)` |
| **别名** | - |

#### `arg_min(arg, val)`

<div class="nostroke_table"></div>

| **描述** | 查找具有最小 `val` 的行，并计算该行的 `arg` 表达式。`arg` 或 `val` 表达式值为 `NULL` 的行将被忽略。此函数 [受排序影响](#order-by-clause-in-aggregate-functions)。 |
| **示例** | `arg_min(A, B)` |
| **别名** | `argmin(arg, val)`, `min_by(arg, val)` |

#### `arg_min(arg, val, n)`

<div class="nostroke_table"></div>

| **描述** | `arg_min` 的通用情况，用于 `n` 值：返回一个 `LIST`，包含按 `val` 降序排列的前 `n` 行的 `arg` 表达式。此函数 [受排序影响](#order-by-clause-in-aggregate-functions)。 |
| **示例** | `arg_min(A, B, 2)` |
| **别名** | `argmin(arg, val, n)`, `min_by(arg, val, n)` |

#### `arg_min_null(arg, val)`

<div class="nostroke_table"></div>

| **描述** | 查找具有最小 `val` 的行，并计算该行的 `arg` 表达式。`val` 表达式评估为 `NULL` 的行将被忽略。此函数 [受排序影响](#order-by-clause-in-aggregate-functions)。 |
| **示例** | `arg_min_null(A, B)` |
| **别名** | - |

#### `array_agg(arg)`

<div class="nostroke_table"></div>

| **描述** | 返回包含一列所有值的 `LIST`。此函数 [受排序影响](#order-by-clause-in-aggregate-functions)。 |
| **示例** | `array_agg(A)` |
| **别名** | `list` |

#### `avg(arg)`

<div class="nostroke_table"></div>

| **描述** | 计算 `arg` 中所有非 `NULL` 值的平均值。 |
| **示例** | `avg(A)` |
| **别名** | `mean` |

#### `bit_and(arg)`

<div class="nostroke_table"></div>

| **描述** | 返回给定表达式中所有位的按位 `AND`。 |
| **示例** | `bit_and(A)` |
| **别名** | - |

#### `bit_or(arg)`

<div class="nostroke_table"></div>

| **描述** | 返回给定表达式中所有位的按位 `OR`。 |
| **示例** | `bit_or(A)` |
| **别名** | - |

#### `bit_xor(arg)`

<div class="nostroke_table"></div>

| **描述** | 返回给定表达式中所有位的按位 `XOR`。 |
| **示例** | `bit_xor(A)` |
| **别名** | - |

#### `bitstring_agg(arg)`

<div class="nostroke_table"></div>

| **描述** | 返回一个位字符串，其长度对应于非 `NULL`（整数）值的范围，每个（不同的）值的位置设置为 1。 |
| **示例** | `bitstring_agg(A)` |
| **别名** | - |

#### `bool_and(arg)`

<div class="nostroke_table"></div>

| **描述** | 如果所有输入值都为 `true`，返回 `true`，否则返回 `false`。 |
| **示例** | `bool_and(A)` |
| **别名** | - |

#### `bool_or(arg)`

<div class="nostroke_table"></div>

| **描述** | 如果任何输入值为 `true`，返回 `true`，否则返回 `false`。 |
| **示例** | `bool_or(A)` |
| **别名** | - |

#### `count()`

<div class="nostroke_table"></div>

| **描述** | 返回组中的行数。 |
| **示例** | `count()` |
| **别名** | `count(*)` |

#### `count(arg)`

<div class="nostroke_table"></div>

| **描述** | 返回 `arg` 中非 `NULL` 值的数量。 |
| **示例** | `count(A)` |
| **别名** | - |

#### `countif(arg)`

<div class="nostroke_table"></div>

| **描述** | 返回组中 `arg` 为 `true` 的行数。 |
| **示例** | `countif(A)` |
| **别名** | - |

#### `favg(arg)`

<div class="nostroke_table"></div>

| **描述** | 使用更精确的浮点求和（Kahan Sum）计算平均值。 |
| **示例** | `favg(A)` |
| **别名** | - |

#### `first(arg)`

<div class="nostroke_table"></div>

| **描述** | 返回 `arg` 中的第一个值（`NULL` 或非 `NULL`）。此函数 [受排序影响](#order-by-clause-in-aggregate-functions)。 |
| **示例** | `first(A)` |
| **别名** | `arbitrary(A)` |

#### `fsum(arg)`

<div class="nostroke_table"></div>

| **描述** | 使用更精确的浮点求和（Kahan Sum）计算总和。 |
| **示例** | `fsum(A)` |
| **别名** | `sumkahan`, `kahan_sum` |

#### `geomean(arg)`

<div class="nostroke_table"></div>

| **描述** | 计算 `arg` 中所有非 `NULL` 值的几何平均值。 |
| **示例** | `geomean(A)` |
| **别名** | `geometric_mean(A)` |

#### `histogram(arg)`

<div class="nostroke_table"></div>

| **描述** | 返回一个 `MAP`，表示桶和计数的键值对。 |
| **示例** | `histogram(A)` |
| **别名** | - |

#### `histogram(arg, boundaries)`

<div class="nostroke_table"></div>

| **描述** | 返回一个 `MAP`，表示提供的上界 `boundaries` 和对应分桶（左开右闭）中的元素计数。如果元素大于所有提供的 `boundaries`，会自动添加一个位于数据类型最大值的边界。边界可以通过 [`equi_width_bins`]({% link docs/stable/sql/functions/utility.md %}#equi_width_binsminmaxbincountnice) 提供。 |
| **示例** | `histogram(A, [0, 1, 10])` |
| **别名** | - |

#### `histogram_exact(arg, elements)`

<div class="nostroke_table"></div>

| **描述** | 返回一个 `MAP`，表示请求的元素及其计数。会自动添加一个特定于数据类型的通配符元素以计数其他元素。 |
| **示例** | `histogram_exact(A, [0, 1, 10])` |
| **别名** | - |

#### `histogram_values(source, col_name, technique, bin_count)`

<div class="nostroke_table"></div>

| **描述** | 返回分桶的上边界及其计数。 |
| **示例** | `histogram_values(integers, i, bin_count := 2)` |
| **别名** | - |

#### `last(arg)`

<div class="nostroke_table"></div>

| **描述** | 返回列的最后一个值。此函数 [受排序影响](#order-by-clause-in-aggregate-functions)。 |
| **示例** | `last(A)` |
| **别名** | - |

#### `list(arg)`

<div class="nostroke_table"></div>

| **描述** | 返回包含一列所有值的 `LIST`。此函数 [受排序影响](#order-by-clause-in-aggregate-functions)。 |
| **示例** | `list(A)` |
| **别名** | `array_agg` |

#### `max(arg)`

<div class="nostroke_table"></div>

| **描述** | 返回 `arg` 中的最大值。此函数 [不受唯一性影响](#distinct-clause-in-aggregate-functions)。 |
| **示例** | `max(A)` |
| **别名** | - |

#### `max(arg, n)`

<div class="nostroke_table"></div>

| **描述** | 返回一个 `LIST`，包含按 `arg` 降序排列的前 `n` 行的 `arg` 值。 |
| **示例** | `max(A, 2)` |
| **别名** | - |

#### `max_by(arg, val)`

<div class="nostroke_table"></div>

| **描述** | 查找具有最大 `val` 的行，并计算该行的 `arg` 表达式。此函数 [受排序影响](#order-by-clause-in-aggregate-functions)。 |
| **示例** | `max_by(A, B)` |
| **别名** | `argmax(arg, val)`, `arg_max(arg, val)` |

#### `max_by(arg, val, n)`

<div class="nostroke_table"></div>

| **描述** | 返回一个 `LIST`，包含按 `val` 降序排列的前 `n` 行的 `arg` 表达式。 |
| **示例** | `max_by(A, B, 2)` |
| **别名** | `argmax(arg, val, n)`, `arg_max(arg, val, n)` |

#### `min(arg)`

<div class="nostroke_table"></div>

| **描述** | 返回 `arg` 中的最小值。此函数 [不受唯一性影响](#distinct-clause-in-aggregate-functions)。 |
| **示例** | `min(A)` |
| **别名** | - |

#### `min(arg, n)`

<div class="nostroke_table"></div>

| **描述** | 返回一个 `LIST`，包含按 `arg` 升序排列的前 `n` 行的 `arg` 值。 |
| **示例** | `min(A, 2)` |
| **别名** | - |

#### `min_by(arg, val)`

<div class="nostroke_table"></div>

| **描述** | 查找具有最小 `val` 的行，并计算该行的 `arg` 表达式。此函数 [受排序影响](#order-by-clause-in-aggregate-functions)。 |
| **示例** | `min_by(A, B)` |
| **别名** | `argMin(arg, val)`, `arg_min(arg, val)` |

#### `min_by(arg, val, n)`

<div class="nostroke_table"></div>

| **描述** | 返回一个 `LIST`，包含按 `val` 升序排列的前 `n` 行的 `arg` 表达式。 |
| **示例** | `min_by(A, B, 2)` |
| **别名** | `argMin(arg, val, n)`, `arg_min(arg, val, n)` |

#### `product(arg)`

<div class="nostroke_table"></div>

| **描述** | 计算 `arg` 中所有非 `NULL` 值的乘积。 |
| **示例** | `product(A)` |
| **别名** | - |

#### `string_agg(arg)`

<div class="nostroke_table"></div>

| **描述** | 使用逗号分隔符（`,`）连接列字符串值。此函数 [受排序影响](#order-by-clause-in-aggregate-functions)。 |
| **示例** | `string_agg(S, ',')` |
| **别名** | `group_concat(arg, sep)`, `listagg(arg, sep)` |

#### `string_agg(arg, sep)`

<div class="nostroke_table"></div>

| **描述** | 使用分隔符连接列字符串值。此函数 [受排序影响](#order-by-clause-in-aggregate-functions)。 |
| **示例** | `string_agg(S, ',')` |
| **别名** | `group_concat(arg, sep)`, `listagg(arg, sep)` |

#### `sum(arg)`

<div class="nostroke_table"></div>

| **描述** | 计算 `arg` 中所有非 `NULL` 值的总和 / 当 `arg` 是布尔值时计数 `true` 值。 |
| **示例** | `sum(A)` |
| **别名** | - |

#### `weighted_avg(arg, weight)`

<div class="nostroke_table"></div>

| **描述** | 计算 `arg` 中所有非 `NULL` 值的加权平均值，其中每个值根据其对应的 `weight` 进行缩放。如果 `weight` 为 `NULL`，则对应的 `arg` 值会被跳过。 |
| **示例** | `weighted_avg(A, W)` |
| **别名** | `wavg(arg, weight)` |

## 近似聚合函数

下表显示了可用的近似聚合函数。

| 函数 | 描述 | 示例 |
|:---|:---|:---|
| `approx_count_distinct(x)` | 使用 HyperLogLog 计算近似不同元素的数量。 | `approx_count_distinct(A)` |
| `approx_quantile(x, pos)` | 使用 T-Digest 计算近似分位数。 | `approx_quantile(A, 0.5)` |
| `approx_top_k(arg, k)` | 使用 Filtered Space-Saving 计算 `arg` 的 `k` 个最频繁值的 `LIST`。 | |
| `reservoir_quantile(x, quantile, sample_size = 8192)` | 使用水库抽样计算近似分位数，样本大小是可选的，默认使用 8192。 | `reservoir_quantile(A, 0.5, 1024)` |

## 统计聚合函数

下表显示了可用的统计聚合函数。
它们忽略 `NULL` 值（在单个输入列 `x` 的情况下）或成对的 `NULL` 值（在两个输入列 `y` 和 `x` 的情况下）。

| 函数 | 描述 |
|:--|:--------|
| [`corr(y, x)`](#corry-x) | 相关系数。 |
| [`covar_pop(y, x)`](#covar_popy-x) | 总体协方差，不包含偏差校正。 |
| [`covar_samp(y, x)`](#covar_sampy-x) | 样本协方差，包含贝塞尔偏差校正。 |
| [`entropy(x)`](#entropyx) | 以 2 为底的熵。 |
| [`kurtosis_pop(x)`](#kurtosis_popx) | 超峰度（Fisher 的定义）无偏差校正。 |
| [`kurtosis(x)`](#kurtosisx) | 超峰度（Fisher 的定义）根据样本大小进行偏差校正。 |
| [`mad(x)`](#madx) | 中位数绝对偏差。时间类型返回一个正的 `INTERVAL`。 |
| [`median(x)`](#medianx) | 数据集的中间值。偶数个值时，定量值取平均，顺序值返回较小的值。 |
| [`mode(x)`](#modex)| 最频繁的值。此函数 [受排序影响](#order-by-clause-in-aggregate-functions)。 |
| [`quantile_cont(x, pos)`](#quantile_contx-pos) | `x` 的 `pos`-分位数的插值，其中 `0 <= pos <= 1`。返回 `pos * (n_nonnull_values - 1)`th（零索引，按指定顺序）的 `x` 值或在索引不是整数时返回相邻值之间的插值。直观地，将 `x` 的值排列为线上的等距 *点*，从 0 开始，到 1 结束，并返回 `pos` 处的（插值）值。如果 `pos` 是 `FLOAT` 的 `LIST`，则结果是一个对应的插值分位数的 `LIST`。 |
| [`quantile_disc(x, pos)`](#quantile_discx-pos) | `x` 的 `pos`-分位数的离散值，其中 `0 <= pos <= 1`。返回 `greatest(ceil(pos * n_nonnull_values) - 1, 0)`th（零索引，按指定顺序）的 `x` 值。直观地，为 `x` 的每个值分配一个等大的 *子区间*（左开右闭，除了初始区间），并选择包含 `pos` 的子区间的值。如果 `pos` 是 `FLOAT` 的 `LIST`，则结果是对应离散分位数的 `LIST`。 |
| [`regr_avgx(y, x)`](#regr_avgxy-x) | 非 `NULL` 对的独立变量的平均值，其中 `x` 是独立变量，`y` 是依赖变量。 |
| [`regr_avgy(y, x)`](#regr_avgyy-x) | 非 `NULL` 对的依赖变量的平均值，其中 `x` 是独立变量，`y` 是依赖变量。 |
| [`regr_count(y, x)`](#regr_county-x) | 非 `NULL` 对的数量。 |
| [`regr_intercept(y, x)`](#regr_intercepty-x) | 独立变量 `x` 和依赖变量 `y` 的单变量线性回归的截距。 |
| [`regr_r2(y, x)`](#regr_r2y-x) | `y` 和 `x` 之间的平方皮尔逊相关系数。此外：线性回归中的决定系数，其中 `x` 是独立变量，`y` 是依赖变量。 |
| [`regr_slope(y, x)`](#regr_slopey-x) | 独立变量 `x` 和依赖变量 `y` 的线性回归的斜率。 |
| [`regr_sxx(y, x)`](#regr_sxxy-x) | 独立变量 `x` 和依赖变量 `y` 的非 `NULL` 对的总体方差，包含贝塞尔偏差校正。 |
| [`regr_sxy(y, x)`](#regr_sxyy-x) | 总体协方差，包含贝塞尔偏差校正。 |
| [`regr_syy(y, x)`](#regr_syyy-x) | 依赖变量 `y` 和独立变量 `x` 的非 `NULL` 对的总体方差，包含贝塞尔偏差校正。 |
| [`skewness(x)`](#skewnessx) | 偏度。 |
| [`sem(x)`](#semx) | 平均值的标准误差。 |
| [`stddev_pop(x)`](#stddev_popx) | 总体标准差。 |
| [`stddev_samp(x)`](#stddev_sampx) | 样本标准差。 |
| [`var_pop(x)`](#var_popx) | 总体方差，不包含偏差校正。 |
| [`var_samp(x)`](#var_sampx) | 样本方差，包含贝塞尔偏差校正。 |

#### `corr(y, x)`

<div class="nostroke_table"></div>

| **描述** | 相关系数。
| **公式** | `covar_pop(y, x) / (stddev_pop(x) * stddev_pop(y))` |
| **别名** | - |

#### `covar_pop(y, x)`

<div class="nostroke_table"></div>

| **描述** | 总体协方差，不包含偏差校正。
| **公式** | `(sum(x*y) - sum(x) * sum(y) / regr_count(y, x)) / regr_count(y, x)`, `covar_samp(y, x) * (1 - 1 / regr_count(y, x))`
| **别名** | - |

#### `covar_samp(y, x)`

<div class="nostroke_table"></div>

| **描述** | 样本协方差，包含贝塞尔偏差校正。
| **公式** | `(sum(x*y) - sum(x) * sum(y) / regr_count(y, x)) / (regr_count(y, x) - 1)`, `covar_pop(y, x) / (1 - 1 / regr_count(y, x))`
| **别名** | `regr_sxy(y, x)`

#### `entropy(x)`

<div class="nostroke_table"></div>

| **描述** | 以 2 为底的熵。
| **公式** | -
| **别名** | -

#### `kurtosis_pop(x)`

<div class="nostroke_table"></div>

| **描述** | 超峰度（Fisher 的定义）无偏差校正。
| **公式** | -
| **别名** | -

#### `kurtosis(x)`

<div class="nostroke_table"></div>

| **描述** | 超峰度（Fisher 的定义）根据样本大小进行偏差校正。
| **公式** | -
| **别名** | -

#### `mad(x)`

<div class="nostroke_table"></div>

| **描述** | 中位数绝对偏差。时间类型返回一个正的 `INTERVAL`。
| **公式** | `median(abs(x - median(x)))`
| **别名** | -

#### `median(x)`

<div class="nostroke_table"></div>

| **描述** | 数据集的中间值。偶数个值时，定量值取平均，顺序值返回较小的值。
| **公式** | `quantile_cont(x, 0.5)`
| **别名** | -

#### `mode(x)`

<div class="nostroke_table"></div>

| **描述** | 最频繁的值。此函数 [受排序影响](#order-by-clause-in-aggregate-functions)。
| **公式** | -
| **别名** | -

#### `quantile_cont(x, pos)`

<div class="nostroke_table"></div>

| **描述** | `x` 的 `pos`-分位数的插值，其中 `0 <= pos <= 1`。返回 `pos * (n_nonnull_values - 1)`th（零索引，按指定顺序）的 `x` 值或在索引不是整数时返回相邻值之间的插值。直观地，将 `x` 的值排列为线上的等距 *点*，从 0 开始，到 1 结束，并返回 `pos` 处的（插值）值。如果 `pos` 是 `FLOAT` 的 `LIST`，则结果是一个对应的插值分位数的 `LIST`。
| **公式** | -
| **别名** | -

#### `quantile_disc(x, pos)`

<div class="nostroke_table"></div>

| **描述** | `x` 的 `pos`-分位数的离散值，其中 `0 <= pos <= 1`。返回 `greatest(ceil(pos * n_nonnull_values) - 1, 0)`th（零索引，按指定顺序）的 `x` 值。直观地，为 `x` 的每个值分配一个等大的 *子区间*（左开右闭，除了初始区间），并选择包含 `pos` 的子区间的值。如果 `pos` 是 `FLOAT` 的 `LIST`，则结果是对应离散分位数的 `LIST`。
| **公式** | -
| **别名** | `quantile`

#### `regr_avgx(y, x)`

<div class="nostroke_table"></div>

| **描述** | 非 `NULL` 对的独立变量的平均值，其中 `x` 是独立变量，`y` 是依赖变量。
| **公式** | -
| **别名** | -

#### `regr_avgy(y, x)`

<div class="nostroke_table"></div>

| **描述** | 非 `NULL` 对的依赖变量的平均值，其中 `x` 是独立变量，`y` 是依赖变量。
| **公式** | -
| **别名** | -

#### `regr_count(y, x)`

<div class="nostroke_table"></div>

| **描述** | 非 `NULL` 对的数量。
| **公式** | -
| **别名** | -

#### `regr_intercept(y, x)`

<div class="nostroke_table"></div>

| **描述** | 独立变量 `x` 和依赖变量 `y` 的单变量线性回归的截距。
| **公式** | `regr_avgy(y, x) - regr_slope(y, x) * regr_avgx(y, x)`
| **别名** | -

#### `regr_r2(y, x)`

<div class="nostroke_table"></div>

| **描述** | `y` 和 `x` 之间的平方皮尔逊相关系数。此外：线性回归中的决定系数，其中 `x` 是独立变量，`y` 是依赖变量。
| **公式** | -
| **别名** | -

#### `regr_slope(y, x)`

<div class="nostroke_table"></div>

| **描述** | 独立变量 `x` 和依赖变量 `y` 的线性回归的斜率。
| **公式** | `regr_sxy(y, x) / regr_sxx(y, x)`
| **别名** | -

#### `regr_sxx(y, x)`

<div class="nostroke_table"></div>

| **描述** | 独立变量 `x` 和依赖变量 `y` 的非 `NULL` 对的总体方差，包含贝塞尔偏差校正。
| **公式** | -
| **别名** | -

#### `regr_sxy(y, x)`

<div class="nostroke_table"></div>

| **描述** | 总体协方差，包含贝塞尔偏差校正。
| **公式** | -
| **别名** | -

#### `regr_syy(y, x)`

<div class="nostroke_table"></div>

| **描述** | 依赖变量 `y` 和独立变量 `x` 的非 `NULL` 对的总体方差，包含贝塞尔偏差校正。
| **公式** | -
| **别名** | -

#### `sem(x)`

<div class="nostroke_table"></div>

| **描述** | 平均值的标准误差。
| **公式** | -
| **别名** | -

#### `skewness(x)`

<div class="nostroke_table"></div>

| **描述** | 偏度。
| **公式** | -
| **别名** | -

#### `stddev_pop(x)`

<div class="nostroke_table"></div>

| **描述** | 总体标准差。
| **公式** | `sqrt(var_pop(x))`
| **别名** | -

#### `stddev_samp(x)`

<div class="nostroke_table"></div>

| **描述** | 样本标准差。
| **公式** | `sqrt(var_samp(x))`
| **别名** | `stddev(x)`

#### `var_pop(x)`

<div class="nostroke_table"></div>

| **描述** | 总体方差，不包含偏差校正。
| **公式** | `(sum(x^2) - sum(x)^2 / count(x)) / count(x)`, `var_samp(y, x) * (1 - 1 / count(x))`
| **别名** | -

#### `var_samp(x)`

<div class="nostroke_table"></div>

| **描述** | 样本方差，包含贝塞尔偏差校正。
| **公式** | `(sum(x^2) - sum(x)^2 / count(x)) / (count(x) - 1)`, `var_pop(y, x) / (1 - 1 / count(x))`
| **别名** | `variance(arg, val)`

## 有序集合聚合函数

下表显示了可用的“有序集合”聚合函数。
这些函数使用 `WITHIN GROUP (ORDER BY sort_expression)` 语法指定，
并将其转换为等效的聚合函数，该函数将排序表达式作为第一个参数。

| 函数 | 等效函数 |
|:---|:---|
| <code>mode() WITHIN GROUP (ORDER BY column [(ASC&#124;DESC)])</code> | <code>mode(column ORDER BY column [(ASC&#124;DESC)])</code> |
| <code>percentile_cont(fraction) WITHIN GROUP (ORDER BY column [(ASC&#124;DESC)])</code> | <code>quantile_cont(column, fraction ORDER BY column [(ASC&#124;DESC)])</code> |
| <code>percentile_cont(fractions) WITHIN GROUP (ORDER BY column [(ASC&#124;DESC)])</code> | <code>quantile_cont(column, fractions ORDER BY column [(ASC&#124;DESC)])</code> |
| <code>percentile_disc(fraction) WITHIN GROUP (ORDER BY column [(ASC&#124;DESC)])</code> | <code>quantile_disc(column, fraction ORDER BY column [(ASC&#124;DESC)])</code> |
| <code>percentile_disc(fractions) WITHIN GROUP (ORDER BY column [(ASC&#124;DESC)])</code> | <code>quantile_disc(column, fractions ORDER BY column [(ASC&#124;DESC)])</code> |

## 其他聚合函数

| 函数 | 描述 | 别名 |
|:--|:---|:--|
| `grouping()` | 对于使用 `GROUP BY` 且包含 [`ROLLUP` 或 `GROUPING SETS`]({% link docs/stable/sql/query_syntax/grouping_sets.md %}#identifying-grouping-sets-with-grouping_id) 的查询：返回一个整数，标识用于创建当前超级聚合行的参数表达式。 | `grouping_id()` |