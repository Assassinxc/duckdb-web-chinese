---
---
layout: docu
redirect_from:
- /dev/profiling
- /dev/profiling/
- /docs/dev/profiling
title: 性能分析
---

性能分析对于理解为什么某些查询表现出特定的性能特征至关重要。
DuckDB 包含多个内置功能以启用查询性能分析，本文档将介绍这些功能。
如需使用 `EXPLAIN` 的高级示例，请参阅[“检查查询计划”页面]({% link docs/stable/guides/meta/explain.md %}).
如需深入了解，请参阅[“性能分析”页面]({% link docs/stable/dev/profiling.md %})中的开发者文档。

## 语句

### `EXPLAIN` 语句

分析查询的第一步可以包括检查查询计划。
`EXPLAIN` 语句显示查询计划并描述其底层发生的情况。

### `EXPLAIN ANALYZE` 语句

查询计划帮助开发者了解查询的性能特征。
然而，有时还需要检查各个操作符的性能数据以及通过它们的基数。
`EXPLAIN ANALYZE` 语句可获取这些数据，因为它以美观的格式打印查询计划并执行查询。
因此，它提供了实际的运行时性能数据。

### `FORMAT` 选项

`EXPLAIN [ANALYZE]` 语句允许导出到多种格式：

* `text` – 默认 ASCII 艺术风格输出
* `graphviz` – 生成 DOT 输出，可以用 [Graphviz](https://graphviz.org/) 渲染
* `html` – 生成 HTML 输出，可以用 [treeflex](https://dumptyd.github.io/treeflex/) 渲染
* `json` – 生成 JSON 输出

要指定格式，请使用 `FORMAT` 标签：

```sql
EXPLAIN (FORMAT html) SELECT 42 AS x;
```

## 预处理指令

DuckDB 支持多个预处理指令，用于开启和关闭性能分析以及控制性能分析输出的详细程度。

以下预处理指令可用，可以通过 `PRAGMA` 或 `SET` 设置。
它们也可以通过 `RESET` 重置，后跟设置名称。
如需更多信息，请参阅预处理指令页面的[“性能分析”]({% link docs/stable/configuration/pragmas.md %}#profiling)部分。

| 设置                                                                                                                                                            | 描述                                      | 默认值                                                   | 选项                                                                                                                 |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------|-----------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|
| [`enable_profiling`]({% link docs/stable/configuration/pragmas.md %}#enable_profiling), [`enable_profile`]({% link docs/stable/configuration/pragmas.md %}#enable_profiling)     | 启用性能分析                                | `query_tree`                                              | `query_tree`, `json`, `query_tree_optimizer`, `no_output`                                                               |
| [`profiling_output`]({% link docs/stable/configuration/pragmas.md %}#profiling_output)                                                                                    | 设置性能分析输出文件                      | 控制台                                                   | 文件路径                                                                                                              |
| [`profiling_mode`]({% link docs/stable/configuration/pragmas.md %}#profiling_mode)                                                                                        | 切换额外的优化器和规划器指标  | `standard`                                                | `standard`, `detailed`                                                                                                  |
| [`custom_profiling_settings`]({% link docs/stable/configuration/pragmas.md %}#custom_profiling_metrics)                                                                   | 启用或禁用特定指标               | 所有指标，除了那些由详细性能分析激活的指标  | 与以下内容匹配的 JSON 对象：`{"METRIC_NAME": "boolean", ...}`。请参阅下面的[指标](#metrics)部分。 |
| [`disable_profiling`]({% link docs/stable/configuration/pragmas.md %}#disable_profiling), [`disable_profile`]({% link docs/stable/configuration/pragmas.md %}#disable_profiling) | 禁用性能分析                               |                                                           |                                                                                                                         |

## 指标

查询树有两种类型的节点：`QUERY_ROOT` 和 `OPERATOR` 节点。
`QUERY_ROOT` 仅指顶层节点，其包含的指标是在整个查询中测量的。
`OPERATOR` 节点指查询计划中的各个操作符。
一些指标仅适用于 `QUERY_ROOT` 节点，而另一些仅适用于 `OPERATOR` 节点。
下表描述了每个指标及其可用的节点。

除了 `QUERY_NAME` 和 `OPERATOR_TYPE`，还可以开启或关闭所有指标。

| 指标                      | 返回类型 | 单位   | 查询 | 操作符 | 描述                                                                                                                   |
|-----------------------------|-------------|----------|:-----:|:--------:|-------------------------------------------------------------------------------------------------------------------------------|
| `BLOCKED_THREAD_TIME`       | `double`    | 秒  |   ✅  |          | 线程被阻塞的总时间                                                                                              |
| `EXTRA_INFO`                | `string`    |          |   ✅  |    ✅    | 独特的操作符指标                                                                                                       |
| `LATENCY`                   | `double`    | 秒  |   ✅  |          | 查询执行的总耗时                                                                                              |
| `OPERATOR_CARDINALITY`      | `uint64`    | 绝对值 |       |    ✅    | 每个操作符的基数，即其返回给父级的行数。操作符等价于 `ROWS_RETURNED`   |
| `OPERATOR_ROWS_SCANNED`     | `uint64`    | 绝对值 |       |    ✅    | 每个操作符扫描的总行数                                                                                       |
| `OPERATOR_TIMING`           | `double`    | 秒  |       |    ✅    | 每个操作符所花费的时间。操作符等价于 `LATENCY`                                                             |
| `OPERATOR_TYPE`             | `string`    |          |       |    ✅    | 每个操作符的名称                                                                                                     |
| `QUERY_NAME`                | `string`    |          |   ✅  |          | 查询字符串                                                                                                              |
| `RESULT_SET_SIZE`           | `uint64`    | 字节    |   ✅  |    ✅    | 结果集的大小                                                                                                        |
| `ROWS_RETURNED`             | `uint64`    | 绝对值 |   ✅  |          | 查询返回的行数                                                                                      |
| `SYSTEM_PEAK_BUFFER_MEMORY` | `uint64`    | 字节    |   ✅  |          | 查询期间系统所有分配缓冲区的峰值内存使用量                                                     |
| `SYSTEM_PEAK_TEMP_DIR_SIZE` | `uint64`    | 字节    |   ✅  |          | 查询期间系统临时目录的峰值大小                                                                |

### 累计指标

DuckDB 也支持几种在所有节点中可用的累计指标。
在 `QUERY_ROOT` 节点中，这些指标代表查询中所有操作符的相应指标的总和。
`OPERATOR` 节点表示操作符特定指标及其所有子节点的递归总和。

即使底层特定指标被禁用，这些累计指标也可以独立启用。
下表显示了累计指标。
它还描绘了 DuckDB 计算累计指标所依据的指标。

| 指标                    | 单位     | 累计计算的指标 |
|---------------------------|----------|--------------------------------|
| `CPU_TIME`                | 秒  | `OPERATOR_TIMING`              |
| `CUMULATIVE_CARDINALITY`  | 绝对值 | `OPERATOR_CARDINALITY`         |
| `CUMULATIVE_ROWS_SCANNED` | 绝对值 | `OPERATOR_ROWS_SCANN,`        |

`CPU_TIME` 测量累计操作符时间。
它不包括在其他阶段（如解析、查询规划等）所花费的时间。
因此，对于某些查询，`QUERY_ROOT` 中的 `LATENCY` 可能大于 `CPU_TIME`。

## 详细性能分析

当 `profiling_mode` 设置为 `detailed` 时，会启用一组额外的指标，这些指标仅在 `QUERY_ROOT` 节点中可用。
这些包括 [`OPTIMIZER`](#optimizer-metrics)、[`PLANNER`](#planner-metrics) 和 [`PHYSICAL_PLANNER`](#physical-planner-metrics) 指标。
它们以秒为单位，返回为 `double`。
可以单独切换这些额外指标。

### 优化器指标

在 `QUERY_ROOT` 节点中，有指标用于测量每个 [优化器]({% link docs/stable/internals/overview.md %}#optimizer) 所耗费的时间。
这些指标仅在启用特定优化器时可用。
可以使用 [`duckdb_optimizers()`{:.language-sql .highlight} 表函数]({% link docs/stable/sql/meta/duckdb_table_functions.md %}#duckdb_optimizers) 查询可用的优化。

每个优化器都有一个对应的指标，格式为：`OPTIMIZER_⟨OPTIMIZER_NAME⟩`{:.language-sql .highlight}。
例如，`OPTIMIZER_JOIN_ORDER` 指标对应 `JOIN_ORDER` 优化器。

此外，以下指标可用于支持优化器指标：

* `ALL_OPTIMIZERS`: 启用所有优化器指标并测量优化器父节点的耗时。
* `CUMULATIVE_OPTIMIZER_TIMING`: 所有优化器指标的累计总和。无需启用所有优化器指标即可使用。

### 规划器指标

规划器负责生成逻辑计划。目前，DuckDB 在规划器中测量两个指标：

* `PLANNER`: 从解析的 SQL 节点生成逻辑计划所花费的时间。
* `PLANNER_BINDING`: 绑定逻辑计划所花费的时间。

### 物理规划器指标

物理规划器负责从逻辑计划生成物理计划。
以下是物理规划器支持的指标：

* `PHYSICAL_PLANNER`: 生成物理计划所花费的时间。
* `PHYSICAL_PLANNER_COLUMN_BINDING`: 将逻辑计划中的列绑定到物理列所花费的时间。
* `PHYSICAL_PLANNER_RESOLVE_TYPES`: 将逻辑计划中的类型解析为物理类型所花费的时间。
* `PHYSICAL_PLANNER_CREATE_PLAN`: 创建物理计划所花费的时间。

## 自定义指标示例

以下示例演示了如何启用自定义性能分析并设置输出格式为 `json`。
在第一个示例中，我们启用了性能分析并将输出设置为文件。
我们仅启用了 `EXTRA_INFO`、`OPERATOR_CARDINALITY` 和 `OPERATOR_TIMING`。

```sql
CREATE TABLE students (name VARCHAR, sid INTEGER);
CREATE TABLE exams (eid INTEGER, subject VARCHAR, sid INTEGER);
INSERT INTO students VALUES ('Mark', 1), ('Joe', 2), ('Matthew', 3);
INSERT INTO exams VALUES (10, 'Physics', 1), (20, 'Chemistry', 2), (30, 'Literature', 3);

PRAGMA enable_profiling = 'json';
PRAGMA profiling_output = '/path/to/file.json';

PRAGMA custom_profiling_settings = '{"CPU_TIME": "false", "EXTRA_INFO": "true", "OPERATOR_CARDINALITY": "true", "OPERATOR_TIMING": "true"}';

SELECT name
FROM students
JOIN exams USING (sid)
WHERE name LIKE 'Ma%';
```

执行查询后，文件的内容如下：

```json
{
    "extra_info": {},
    "query_name": "SELECT name\nFROM students\nJOIN exams USING (sid)\nWHERE name LIKE 'Ma%';",
    "children": [
        {
            "operator_timing": 0.000001,
            "operator_cardinality": 2,
            "operator_type": "PROJECTION",
            "extra_info": {
                "Projections": "name",
                "Estimated Cardinality": "1"
            },
            "children": [
                {
                    "extra_info": {
                        "Join Type": "INNER",
                        "Conditions": "sid = sid",
                        "Build Min": "1",
                        "Build Max": "3",
                        "Estimated Cardinality": "1"
                    },
                    "operator_cardinality": 2,
                    "operator_type": "HASH_JOIN",
                    "operator_timing": 0.00023899999999999998,
                    "children": [
...
```

第二个示例在输出中添加了详细指标。

```sql
PRAGMA profiling_mode = 'detailed';

SELECT name
FROM students
JOIN exams USING (sid)
WHERE name LIKE 'Ma%';
```

输出文件的内容如下：

```json
{
  "all_optimizers": 0.001413,
  "cumulative_optimizer_timing": 0.0014120000000000003,
  "planner": 0.000873,
  "planner_binding": 0.000869,
  "physical_planner": 0.000236,
  "physical_planner_column_binding": 0.000005,
  "physical_planner_resolve_types": 0.000001,
  "physical_planner_create_plan": 0.000226,
  "optimizer_expression_rewriter": 0.000029,
  "optimizer_filter_pullup": 0.000002,
  "optimizer_filter_pushdown": 0.000102,
...
  "optimizer_column_lifetime": 0.000009999999999999999,
  "rows_returned": 2,
  "latency": 0.003708,
  "cumulative_rows_scanned": 6,
  "cumulative_cardinality": 11,
  "extra_info": {},
  "cpu_time": 0.000095,
  "optimizer_build_side_probe_side": 0.000017,
  "result_set_size": 32,
  "blocked_thread_time": 0.0,
  "query_name": "SELECT name\nFROM students\nJOIN exams USING (sid)\nWHERE name LIKE 'Ma%';",
  "children": [
    {
      "operator_timing": 0.000001,
      "operator_rows_scanned": 0,
      "cumulative_rows_scanned": 6,
      "operator_cardinality": 2,
      "operator_type": "PROJECTION",
      "cumulative_cardinality": 11,
      "extra_info": {
        "Projections": "name",
        "Estimated Cardinality": "1"
      },
      "result_set_size": 32,
      "cpu_time": 0.000095,
      "children": [
...
```

## 查询图

也可以将性能分析输出渲染为查询图。
查询图以视觉方式表示查询计划，显示操作符及其关系。
查询计划必须以 `json` 格式输出并存储在文件中。
在将性能分析输出写入指定文件后，Python 脚本可以将其渲染为查询图。
该脚本需要安装 `duckdb` Python 模块。
它生成一个 HTML 文件并在您的网络浏览器中打开它。

```bash
python -m duckdb.query_graph /path/to/file.json
```

## 查询计划中的符号

在查询计划中，[哈希连接](https://en.wikipedia.org/wiki/Hash_join) 操作符遵循以下约定：
连接的 _探测侧_ 是左侧操作数，而 _构建侧_ 是右侧操作数。

查询计划中的连接操作符显示使用的连接类型：

* 内连接表示为 `INNER`。
* 左外连接和右外连接分别表示为 `LEFT` 和 `RIGHT`。
* 全外连接表示为 `FULL`。

> 提示 要可视化查询计划，请考虑使用由[图宾根大学数据库系统研究组](https://github.com/DBatUTuebingen)开发的[DuckDB 执行计划可视化器](https://db.cs.uni-tuebingen.de/explain/)。