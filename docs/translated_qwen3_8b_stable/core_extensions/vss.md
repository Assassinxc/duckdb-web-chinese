---
---
github_repository: https://github.com/duckdb/duckdb-vss
layout: docu
title: 向量相似性搜索扩展
redirect_from:
- /docs/stable/extensions/vss
- /docs/stable/extensions/vss/
- /docs/extensions/vss
- /docs/extensions/vss/
---

`vss` 扩展是 DuckDB 的一个实验性扩展，它通过 DuckDB 的新固定大小 `ARRAY` 类型，为加速向量相似性搜索查询提供索引支持。

请参见 [公告博客文章]({% post_url 2024-05-03-vector-similarity-search-vss %}) 和 [“向量相似性搜索扩展的新功能”文章]({% post_url 2024-10-23-whats-new-in-the-vss-extension %}).

## 使用方法

要在一个具有 `ARRAY` 列的表上创建新的 HNSW（Hierarchical Navigable Small Worlds）索引，请使用带有 `USING HNSW` 子句的 `CREATE INDEX` 语句。例如：

```sql
INSTALL vss;
LOAD vss;

CREATE TABLE my_vector_table (vec FLOAT[3]);
INSERT INTO my_vector_table
    SELECT array_value(a, b, c)
    FROM range(1, 10) ra(a), range(1, 10) rb(b), range(1, 10) rc(c);
CREATE INDEX my_hnsw_index ON my_vector_table USING HNSW (vec);
```

该索引将用于加速使用 `ORDER BY` 子句对索引列和常量向量进行评估的受支持距离度量函数的查询，随后使用 `LIMIT` 子句。例如：

```sql
SELECT *
FROM my_vector_table
ORDER BY array_distance(vec, [1, 2, 3]::FLOAT[3])
LIMIT 3;
```

此外，如果 `arg` 参数是匹配的距离度量函数，也可以使用重载的 `min_by(col, arg, n)` 来加速 `HNSW` 索引。这可用于快速执行单次最近邻搜索。例如，要获取与 `[1, 2, 3]` 最接近的向量的前 3 行：

```sql
SELECT min_by(my_vector_table, array_distance(vec, [1, 2, 3]::FLOAT[3]), 3 ORDER BY vec) AS result
FROM my_vector_table;
```

```text
[{'vec': [1.0, 2.0, 3.0]}, {'vec': [2.0, 2.0, 3.0]}, {'vec': [1.0, 2.0, 4.0]}]
```

请注意，我们如何将表名作为第一个参数传递给 [`min_by`]({% link docs/stable/sql/functions/aggregates.md %}#min_byarg-val-n)，以返回包含整个匹配行的结构。

我们可以通过检查 `EXPLAIN` 输出并查找计划中的 `HNSW_INDEX_SCAN` 节点来验证索引是否正在使用：

```sql
EXPLAIN
SELECT *
FROM my_vector_table
ORDER BY array_distance(vec, [1, 2, 3]::FLOAT[3])
LIMIT 3;
```

```text
┌───────────────────────────┐
│         PROJECTION        │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│             #0            │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         PROJECTION        │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│            vec            │
│array_distance(vec, [1.0, 2│
│         .0, 3.0])         │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│      HNSW_INDEX_SCAN      │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│   t1 (HNSW INDEX SCAN :   │
│           my_idx)         │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│            vec            │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│           EC: 3           │
└───────────────────────────┘
```

默认情况下，HNSW 索引将使用欧几里得距离 `l2sq`（L2-norm squared）度量，与 DuckDB 的 `array_distance` 函数匹配，但可以通过在创建索引时指定 `metric` 选项使用其他距离度量。例如：

```sql
CREATE INDEX my_hnsw_cosine_index
ON my_vector_table
USING HNSW (vec)
WITH (metric = 'cosine');
```

下表显示了支持的距离度量及其对应的 DuckDB 函数：

| 度量 | 函数 | 描述 |
|------|------|------|
| `l2sq` | `array_distance` | 欧几里得距离 |
| `cosine` | `array_cosine_distance` | 余弦相似度距离 |
| `ip` | `array_negative_inner_product` | 负的内积 |

请注意，虽然每个 `HNSW` 索引仅适用于单个列，但你可以在同一张表上创建多个 `HNSW` 索引，每个索引分别针对不同的列。此外，你还可以在同一个列上创建多个 `HNSW` 索引，每个索引支持不同的距离度量。

## 索引选项

除了 `metric` 选项，`HNSW` 索引创建语句还支持以下选项，用于控制索引构建和搜索过程的超参数：

| 选项 | 默认值 | 描述 |
|------|--------|------|
| `ef_construction` | 128 | 在构建索引过程中考虑的候选顶点数量。较高的值将导致更准确的索引，但也会增加构建索引所需的时间。 |
| `ef_search` | 64 | 在索引搜索阶段考虑的候选顶点数量。较高的值将导致更准确的索引，但也会增加搜索所需的时间。 |
| `M` | 16 | 图中每个顶点保留的最大邻居数。较高的值将导致更准确的索引，但也会增加构建索引所需的时间。 |
| `M0` | 2 * `M` | 图中零级的基连接性，即每个顶点保留的邻居数。较高的值将导致更准确的索引，但也会增加构建索引所需的时间。 |

此外，你还可以在运行时通过设置 `SET hnsw_ef_search = ⟨int⟩`{:.language-sql .highlight} 配置选项来覆盖在索引构建时设置的 `ef_search` 参数。这在你想在每连接基础上权衡搜索性能和准确性时可能很有用。你也可以通过调用 `RESET hnsw_ef_search`{:.language-sql .highlight} 来取消该覆盖。

## 持久化

由于一些已知的与自定义扩展索引持久化相关的问题，`HNSW` 索引默认只能在内存数据库的表上创建，除非将 `SET hnsw_enable_experimental_persistence = ⟨bool⟩`{:.language-sql .highlight} 配置选项设置为 `true`。

将此功能锁定在实验性标志背后的理由是，“WAL”（Write-Ahead Logging）恢复尚未完全实现对于自定义索引，这意味着如果发生崩溃或数据库在有未提交更改的 `HNSW` 索引表的情况下意外关闭，你可能会遇到**数据丢失或索引损坏**的问题。

如果你启用了此选项并遇到意外关闭，你可以尝试通过首先单独启动 DuckDB，加载 `vss` 扩展，然后 `ATTACH` 数据库文件来恢复索引，这确保了在 WAL 播放期间 `HNSW` 索引功能可用，允许 DuckDB 的恢复过程顺利进行。但仍然建议你不要在生产环境中使用此功能。

启用 `hnsw_enable_experimental_persistence` 选项后，索引将被持久化到 DuckDB 数据库文件中（如果你使用的是基于磁盘的数据库文件），这意味着在数据库重启后，索引可以从磁盘重新加载到内存中，而无需重新创建。考虑到这一点，持久化索引存储没有增量更新，因此每次 DuckDB 执行检查点时，整个索引将被序列化到磁盘并覆盖自身。同样，在数据库重启后，索引将被完全反序列化回主内存。尽管如此，反序列化过程将在你首次访问与索引相关的表时进行。根据索引的大小，反序列化过程可能需要一些时间，但应该比简单地删除并重新创建索引要快得多。

## 插入、更新、删除和重新压缩

HNSW 索引在索引创建后支持对表进行插入、更新和删除行。不过，有两点需要注意：

* 在表填充数据后创建索引会更快，因为初始批量加载可以更好地利用大表的并行性。
* 删除操作不会立即反映在索引中，而是被“标记”为已删除，这可能导致索引逐渐变得过时，进而影响查询质量和性能。

为了解决最后一点，你可以调用 `PRAGMA hnsw_compact_index('⟨index_name⟩')`{:.language-sql .highlight} 语法函数来触发索引的重新压缩，以修剪已删除的条目，或者在大量更新后重新创建索引。

## 额外功能：向量相似性搜索连接

`vss` 扩展还提供了一些表宏，用于简化多个向量之间的匹配，这些被称为“模糊连接”。它们是：

* `vss_join(left_table, right_table, left_col, right_col, k, metric := 'l2sq')`
* `vss_match(right_table", left_col, right_col, k, metric := 'l2sq')`

> `k` 是从 `right_table` 中为每个 `left_table` 记录选择的记录数，按得分排序。

这些 **目前** 并未使用 `HNSW` 索引，而是作为便利的实用函数提供给那些可以接受不编写连接逻辑本身而执行暴力向量相似性搜索的用户。在未来，这些可能会成为基于索引优化的目标。

这些函数可以这样使用：

```sql
CREATE TABLE haystack (id int, vec FLOAT[3]);
CREATE TABLE needle (search_vec FLOAT[3]);

INSERT INTO haystack
    SELECT row_number() OVER (), array_value(a, b, c)
    FROM range(1, 10) ra(a), range(1, 10) rb(b), range(1, 10) rc(c);

INSERT INTO needle
    VALUES ([5, 5, 5]), ([1, 1, 1]);

SELECT *
FROM vss_join(needle, haystack, search_vec, vec, 2) res;
```

```text
┌───────┬─────────────────────────────────┬─────────────────────────────────────┐
│ score │            left_tbl             │              right_tbl              │
│ float │   struct(search_vec float[3])   │  struct(id integer, vec float[3])   │
├───────┼─────────────────────────────────┼─────────────────────────────────────┤
│   0.0 │ {'search_vec': [5.0, 5.0, 5.0]} │ {'id': 365, 'vec': [5.0, 5.0, 5.0]} │
│   1.0 │ {'search_vec': [5.0, 5.0, 5.0]} │ {'id': 356, 'vec': [5.0, 5.0, 4.0]} │
│   0.0 │ {'search_vec': [1.0, 1.0, 1.0]} │ {'id': 1, 'vec': [1.0, 1.0, 1.0]}   │
│   1.0 │ {'search_vec': [1.0, 1.0, 1.0]} │ {'id': 2, 'vec': [1.0, 2.0, 1.0]}   │
└───────┴─────────────────────────────────┴─────────────────────────────────────┘
```

或者，我们可以使用 `vss_match` 宏作为“横向连接”来获取已经按左表分组的匹配项。请注意，这需要我们首先指定左表，然后是引用左表搜索列的 `vss_match` 宏（在这种情况下是 `search_vec`）：

```sql
SELECT *
FROM needle, vss_match(haystack, search_vec, vec, 2) res;
```

```text
┌─────────────────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│   search_vec    │                                                         matches                                                          │
│    float[3]     │                              struct(score float, "row" struct(id integer, vec float[3]))[]                               │
├─────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ [5.0, 5.0, 5.0] │ [{'score': 0.0, 'row': {'id': 365, 'vec': [5.0, 5.0, 5.0]}}, {'score': 1.0, 'row': {'id': 356, 'vec': [5.0, 5.0, 4.0]}}] │
│ [1.0, 1.0, 1.0] │ [{'score': 0.0, 'row': {'id': 1, 'vec': [1.0, 1.0, 1.0]}}, {'score': 1.0, 'row': {'id': 2, 'vec': [1.0, 2.0, 1.0]}}]     │
└─────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## 局限性

* 目前仅支持由 `FLOAT`（32 位，单精度）组成的向量。
* 索引本身不是缓冲管理的，必须能够完全放入 RAM 内存。
* 索引在内存中的大小不计入 DuckDB 的 `memory_limit` 配置参数。
* `HNSW` 索引只能在内存数据库的表上创建，除非将 `SET hnsw_enable_experimental_persistence = ⟨bool⟩` 配置选项设置为 `true`，更多信息请参见 [持久化](#persistence)。
* 向量连接表宏（`vss_join` 和 `vss_match`）不需要或使用 `HNSW` 索引。