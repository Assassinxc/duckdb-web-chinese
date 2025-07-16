---
---
layout: docu
railroad: statements/samples.js
redirect_from:
- /docs/sql/samples
title: 示例
---

示例用于从数据集中随机选择一个子集。

### 示例

使用 `reservoir` 抽样从 `tbl` 中选择正好 5 行：

```sql
SELECT *
FROM tbl
USING SAMPLE 5;
```

使用 `system` 抽样从表中选择大约 10% 的数据：

```sql
SELECT *
FROM tbl
USING SAMPLE 10%;
```

> 警告 默认情况下，当您指定一个百分比时，每个 [*向量*]({% link docs/stable/internals/vector.md %}) 会以该概率包含在样本中。如果您的表行数少于约 10,000 行，则建议使用 `bernoulli` 抽样选项，该选项会独立地对每一行应用概率。即使如此，您有时会得到多于或少于指定百分比的行数，但完全得不到任何行的概率会小得多。要精确获取 10% 的行数（四舍五入），您必须使用 `reservoir` 抽样选项。

使用 `bernoulli` 抽样从表中选择大约 10% 的数据：

```sql
SELECT *
FROM tbl
USING SAMPLE 10 PERCENT (bernoulli);
```

使用 `reservoir` 抽样从表中选择正好 10%（四舍五入）的数据：

```sql
SELECT *
FROM tbl
USING SAMPLE 10 PERCENT (reservoir);
```

使用固定种子（100）的 `reservoir` 抽样从表中选择正好 50 行：

```sql
SELECT *
FROM tbl
USING SAMPLE reservoir(50 ROWS)
REPEATABLE (100);
```

使用固定种子（377）的 `system` 抽样从表中选择大约 20% 的数据：

```sql
SELECT *
FROM tbl
USING SAMPLE 20% (system, 377);
```

在与 `tbl2` 进行连接之前，从 `tbl` 中选择大约 20% 的数据：

```sql
SELECT *
FROM tbl TABLESAMPLE reservoir(20%), tbl2
WHERE tbl.i = tbl2.i;
```

在与 `tbl2` 进行连接之后，从 `tbl` 中选择大约 20% 的数据：

```sql
SELECT *
FROM tbl, tbl2
WHERE tbl.i = tbl2.i
USING SAMPLE reservoir(20%);
```

### 语法

<div id="rrdiagram"></div>

样本允许您随机提取数据集的一个子集。样本对于快速探索数据集很有用，因为通常您并不关心查询的精确答案，而只是想知道数据的大致情况和数据内容。样本能够更快地为您提供查询的近似答案，因为它们减少了需要通过查询引擎的数据量。

DuckDB 支持三种不同的抽样方法：`reservoir`、`bernoulli` 和 `system`。默认情况下，DuckDB 在采样精确行数时使用 `reservoir` 抽样，而在指定百分比时使用 `system` 抽样。以下将详细描述这些抽样方法。

样本需要一个 *样本大小*，这表示将从总数据集中抽样的元素数量。样本可以是百分比形式（如 `10%` 或 `10 PERCENT`），也可以是固定行数形式（如 `10` 或 `10 ROWS`）。所有三种抽样方法都支持百分比抽样，但 **只有** `reservoir` 抽样支持固定行数抽样。

样本是概率性的，也就是说，在 *未指定种子* 的情况下，样本在不同运行之间可能会不同。指定种子 *仅* 保证在不启用多线程（即 `SET threads = 1`）时样本相同。在多线程处理样本的情况下，即使使用固定种子，样本也不一定一致。

### `reservoir`

Reservoir 抽样是一种流抽样技术，通过保持一个大小等于样本大小的 *reservoir*，并在更多元素到来时随机替换元素来选择一个随机样本。Reservoir 抽样允许我们指定 *正好* 希望在结果样本中包含多少元素（通过选择 reservoir 的大小）。因此，Reservoir 抽样 *始终* 输出相同数量的元素，这与 system 和 bernoulli 抽样不同。

Reservoir 抽样仅推荐用于小样本大小，不推荐用于百分比抽样。这是因为在 reservoir 抽样中需要将整个样本材料化并随机替换材料化样本中的元组。样本大小越大，这个过程的性能损失就越高。

当使用多处理时，Reservoir 抽样还会产生额外的性能开销，因为 reservoir 需要在不同线程之间共享以确保无偏抽样。当 reservoir 非常小时，这不是大问题，但当样本较大时，这会变得昂贵。

> 最佳实践 如果可能，避免在大样本大小时使用 reservoir 抽样。
> Reservoir 抽样要求整个样本在内存中进行材料化。

### `bernoulli`

Bernoulli 抽样只能在指定抽样百分比时使用。它非常直接：基础表中的每一行都有与指定百分比相等的概率被包含。因此，即使指定相同的百分比，Bernoulli 抽样返回的元组数量也可能不同。*预期* 的行数等于表的指定百分比，但存在一些 *方差*。

由于 Bernoulli 抽样是完全独立的（没有共享状态），因此使用 Bernoulli 抽样与多线程一起使用不会产生任何惩罚。

### `system`

System 抽样是 Bernoulli 抽样的一种变体，有一个关键区别：每个 *向量* 都以抽样百分比的概率被包含。这是一种集群抽样形式。System 抽样比 Bernoulli 抽样更高效，因为不需要对每行进行选择。

*预期* 的行数仍然等于表的指定百分比，但 *方差* 是 `vectorSize` 的 `vectorSize` 倍。因此，System 抽样不适合少于约 10,000 行的数据集，因为在这些数据集中，可能会发生所有行都被过滤或所有数据都被包含，即使您请求的是 `50 PERCENT`。

## 表抽样

`TABLESAMPLE` 和 `USING SAMPLE` 子句在语法和效果上是相同的，有一个重要区别：`TABLESAMPLE` 会直接从指定的表中抽样，而 `SAMPLE` 子句则是在整个 FROM 子句解析之后才进行抽样。这在查询计划中存在连接时非常重要。

`TABLESAMPLE` 子句本质上等同于创建一个带有 `USING SAMPLE` 子句的子查询，即以下两个查询是相同的：

在连接之前抽样 20% 的 `tbl`：

```sql
SELECT *
FROM
    tbl TABLESAMPLE reservoir(20%),
    tbl2
WHERE tbl.i = tbl2.i;
```

在连接之前抽样 20% 的 `tbl`：

```sql
SELECT *
FROM
    (SELECT * FROM tbl USING SAMPLE reservoir(20%)) tbl,
    tbl2
WHERE tbl.i = tbl2.i;
```

在连接之后抽样 20%（即抽样连接结果的 20%）：

```sql
SELECT *
FROM tbl, tbl2
WHERE tbl.i = tbl2.i
USING SAMPLE reservoir(20%);
```