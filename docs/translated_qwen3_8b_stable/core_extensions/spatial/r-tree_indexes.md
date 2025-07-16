---
---
layout: docu
title: R-Tree 索引
redirect_from:
- /docs/stable/extensions/spatial/r-tree_indexes
- /docs/stable/extensions/spatial/r-tree_indexes/
- /docs/extensions/spatial/r-tree_indexes
- /docs/extensions/spatial/r-tree_indexes/
---

从 DuckDB v1.1.0 开始，[`spatial` 扩展]({% link docs/stable/core_extensions/spatial/overview.md %}) 通过 R-tree 扩展索引类型提供了对空间索引的基本支持。

## 为什么使用 R-Tree 索引？

在处理地理空间数据集时，你经常会希望根据特定感兴趣区域的空间关系来筛选行。不幸的是，尽管 DuckDB 的向量化执行引擎相当快，但这种操作在处理大型数据集时并不具备很好的可扩展性，因为它总是需要进行完整的表扫描以检查表中的每一行。然而，通过使用 R-tree 索引对表进行索引，可以显著加速这些类型的查询。

## R-Tree 索引是如何工作的？

R-tree 是一种平衡树数据结构，它在叶节点中存储每种几何体的近似 _最小包围矩形_（以及对应行的内部 ID），并在每个内部节点中存储包含所有子节点的包围矩形。

> 几何体的 _最小包围矩形_（MBR）是能够完全包含该几何体的最小矩形。通常当我们谈论几何体的包围矩形（或在二维几何上下文中的包围“框”）时，我们指的是最小包围矩形。此外，我们通常假设包围框/矩形是 _轴对齐_ 的，即矩形 **不** 旋转 —— 矩形的边始终与坐标轴平行。点的 MBR 就是该点本身。

通过从上到下遍历 R-tree，可以在 R-tree 索引的表中快速找到那些索引几何列与特定感兴趣区域相交的行。因为如果父节点的包围矩形完全不与查询区域相交，就可以跳过整个子树的搜索。一旦到达叶节点，只需要从磁盘中获取那些几何体与查询区域相交的特定行，而往往更昂贵的精确空间谓词检查（以及任何其他过滤器）只需对这些行执行。

## DuckDB 中 R-Tree 索引的限制有哪些？

在开始使用 R-tree 索引之前，有一些限制需要注意：

- R-tree 索引仅支持 `GEOMETRY` 数据类型。
- R-tree 索引仅在使用以下空间谓词函数（因为它们都暗示了相交）进行表筛选（使用 `WHERE` 子句）时用于执行“索引扫描”：`ST_Equals`, `ST_Intersects`, `ST_Touches`, `ST_Crosses`, `ST_Within`, `ST_Contains`, `ST_Overlaps`, `ST_Covers`, `ST_CoveredBy`, `ST_ContainsProperly`。
- 空间谓词函数的一个参数必须是“常量”（即一个在查询计划阶段其结果已知的表达式）。这是因为查询规划器需要在查询实际执行之前知道查询区域的包围框，以便使用 R-tree 索引扫描。

未来我们希望启用 R-tree 索引以加速更多谓词函数和更复杂的查询，例如空间连接。

## 如何在 DuckDB 中使用 R-Tree 索引？

要创建 R-tree 索引，只需使用 `CREATE INDEX` 语句并使用 `USING RTREE` 子句，将要索引的几何列放在括号中。例如：

```sql
-- 创建一个包含几何列的表
CREATE TABLE my_table (geom GEOMETRY);

-- 在几何列上创建 R-tree 索引
CREATE INDEX my_idx ON my_table USING RTREE (geom);
```

在创建 R-tree 索引时，还可以使用 `WITH` 子句传递额外的选项以控制 R-tree 索引的行为。例如，要指定 R-tree 中每个节点的最大条目数，可以使用 `max_node_capacity` 选项：

```sql
CREATE INDEX my_idx ON my_table USING RTREE (geom) WITH (max_node_capacity = 16);
```

调整这些选项对性能的影响高度依赖于 DuckDB 运行的系统配置、数据集的空间分布以及特定工作负载的查询模式。默认值通常足够好，但如果你想尝试不同的参数，可以查看 [此处的完整选项列表](#options)。

## 示例

以下是一个示例，展示了如何在几何列上创建 R-tree 索引，以及在使用空间谓词过滤表时可以看到 `RTREE_INDEX_SCAN` 操作符的使用：

```sql
INSTALL spatial;
LOAD spatial;

-- 创建一个包含 10_000_000 个随机点的表
CREATE TABLE t1 AS SELECT point::GEOMETRY AS geom
FROM st_generatepoints({min_x: 0, min_y: 0, max_x: 100, max_y: 100}::BOX_2D, 10_000, 1337);

-- 在表上创建索引。
CREATE INDEX my_idx ON t1 USING RTREE (geom);

-- 对索引的几何列执行带有“空间谓词”的查询
-- 注意，此处的第二个参数，ST_MakeEnvelope 调用是一个“常量”
SELECT count(*) FROM t1 WHERE ST_Within(geom, ST_MakeEnvelope(45, 45, 65, 65));
```

```text
390
```

我们可以使用 `EXPLAIN` 语句来验证是否使用了 R-tree 索引扫描：

```sql
EXPLAIN SELECT count(*) FROM t1 WHERE ST_Within(geom, ST_MakeEnvelope(45, 45, 65, 65));
```

```text
┌───────────────────────────┐
│    UNGROUPED_AGGREGATE    │
│    ────────────────────   │
│        Aggregates:        │
│        count_star()       │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│           FILTER          │
│    ────────────────────   │
│ ST_Within(geom, '...')    │ 
│                           │
│         ~2000 Rows        │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│     RTREE_INDEX_SCAN      │
│    ────────────────────   │
│   t1 (RTREE INDEX SCAN :  │
│           my_idx)         │
│                           │
│     Projections: geom     │
│                           │
│        ~10000 Rows        │
└───────────────────────────┘
```

## 性能考虑

### 批量加载与维护

在已经填充数据的表上创建 R-tree 会比先创建索引再插入数据要快得多。这是因为 R-tree 会在插入后达到最大容量时定期重新平衡自己，并执行代价较高的分割操作，这可能导致额外的分割操作向上级树级传播。然而，当在已经填充的表上创建 R-tree 索引时，会使用一种特殊的自底向上的“批量加载算法”（Sort-Tile-Recursive），该算法将所有条目分成一个已经平衡的树，因为所需的节点总数可以从一开始就计算出来。

此外，使用批量加载算法通常会创建一个结构更好的 R-tree（包围框之间重叠较少），这通常会导致更好的查询性能。如果你发现查询 R-tree 的性能在大量更新或删除后开始下降，删除并重新创建索引可能会生成一个质量更高的 R-tree。

### 内存使用

与 DuckDB 的内置 ART 索引类似，所有与 R-tree 相关的缓冲区都会在运行 DuckDB 时以磁盘后端模式懒加载（即在需要时从磁盘加载），但它们在索引被删除之前永远不会卸载。这意味着如果你最终扫描整个索引，整个索引将被加载到内存中并持续保留到数据库连接结束。然而，DuckDB 会跟踪 R-tree 索引（即使在批量加载期间）所使用的内存，并且这些内存会计入由 `memory_limit` 配置参数设置的内存限制。

### 调优

根据你的具体工作负载，你可能需要尝试 `max_node_capacity` 和 `min_node_capacity` 选项来改变 R-tree 的结构以及它对插入和删除的响应，查看 [此处的完整选项列表](#options)。一般来说，节点总数更高的树（即 `max_node_capacity` 更低）_可能_ 会产生更细粒度的结构，从而在查询执行期间实现更激进的子树剪枝，但也会需要更多内存来存储树本身，并在查询较大区域时需要遍历更多的内部节点，这会更耗费性能。

## 选项

在创建 R-tree 索引时，可以将以下选项传递给 `WITH` 子句：（例如，`CREATE INDEX my_idx ON my_table USING RTREE (geom) WITH (⟨option⟩ = ⟨value⟩);`{:.language-sql .highlight}）

| 选项              | 描述                                          | 默认值                  |
|-------------------|------------------------------------------------|---------------------------|
| `max_node_capacity` | R-tree 中每个节点的最大条目数                 | `128`                     |
| `min_node_capacity` | R-tree 中每个节点的最小条目数                 | `0.4 * max_node_capacity` |

*如果在删除后节点的条目数低于最小值，该节点将被溶解，所有条目将从树的顶部重新插入。这是 R-tree 实现中常见的操作，以防止树变得过于不平衡。

## R-Tree 表函数

`rtree_index_dump(VARCHAR)` 表函数可用于返回 R-tree 索引中所有可能的节点，这在调试、分析或简单查看索引结构时可能会很有帮助。该函数接受 R-tree 索引的名称作为参数，并返回一个具有以下列的表：

| 列名 | 类型       | 描述                                                                   |
|------|------------|------------------------------------------------------------------------|
| `level`     | `INTEGER`  | 节点在 R-tree 中的层级。根节点的层级为 0                              |
| `bounds`    | `BOX_2DF`  | 节点的包围框                                                           |
| `row_id`    | `ROW_TYPE` | 如果是叶节点，`rowid` 是表中行的 `rowid`，否则为 `NULL`               |

示例：

```sql
-- 创建一个包含 64 个随机点的表
CREATE TABLE t1 AS SELECT point::GEOMETRY AS geom
FROM st_generatepoints({min_x: 0, min_y: 0, max_x: 100, max_y: 100}::BOX_2D, 64, 1337);

-- 在几何列上创建 R-tree 索引（为了演示目的使用较低的 max_node_capacity）
CREATE INDEX my_idx ON t1 USING RTREE (geom) WITH (max_node_capacity = 4);

-- 检查 R-tree 索引。请注意，随着我们深入树的层级，分支节点的包围框的面积会减少。
SELECT 
  level, 
  bounds::GEOMETRY AS geom, 
  CASE WHEN row_id IS NULL THEN st_area(geom) ELSE NULL END AS area, 
  row_id, 
  CASE WHEN row_id IS NULL THEN 'branch' ELSE 'leaf' END AS kind 
FROM rtree_index_dump('my_idx') 
ORDER BY area DESC;
```

```text
┌───────┬──────────────────────────────┬────────────────────┬────────┬─────────┐
│ level │             geom             │        area        │ row_id │  kind   │
│ int32 │           geometry           │       double       │ int64  │ varchar │
├───────┼──────────────────────────────┼────────────────────┼────────┼─────────┤
│     0 │ POLYGON ((2.17285037040710…  │  3286.396482226409 │        │ branch  │
│     0 │ POLYGON ((6.00962591171264…  │  3193.725100864862 │        │ branch  │
│     0 │ POLYGON ((0.74995160102844…  │  3099.921458393704 │        │ branch  │
│     0 │ POLYGON ((14.6168870925903…  │ 2322.2760491675654 │        │ branch  │
│     1 │ POLYGON ((2.17285037040710…  │  604.1520104388514 │        │ branch  │
│     1 │ POLYGON ((26.6022186279296…  │  569.1665467030252 │        │ branch  │
│     1 │ POLYGON ((35.7942314147949…  │ 435.24662436250037 │        │ branch  │
│     1 │ POLYGON ((62.2643051147460…  │ 396.39027683023596 │        │ branch  │
│     1 │ POLYGON ((59.5225715637207…  │ 386.09153403820187 │        │ branch  │
│     1 │ POLYGON ((82.3060836791992…  │ 369.15115640929434 │        │ branch  │
│     · │              ·               │          ·         │      · │  ·      │
│     · │              ·               │          ·         │      · │  ·      │
│     · │              ·               │          ·         │      · │  ·      │
│     2 │ POLYGON ((20.5411434173584…  │                    │     35 │ leaf    │
│     2 │ POLYGON ((14.6168870925903…  │                    │     36 │ leaf    │
│     2 │ POLYGON ((43.7271652221679…  │                    │     39 │ leaf    │
│     2 │ POLYGON ((53.4629211425781…  │                    │     44 │ leaf    │
│     2 │ POLYGON ((26.6022186279296…  │                    │     62 │ leaf    │
│     2 │ POLYGON ((53.1732063293457…  │                    │     63 │ leaf    │
│     2 │ POLYGON ((78.1427154541015…  │                    │     10 │ leaf    │
│     2 │ POLYGON ((75.1728591918945…  │                    │     15 │ leaf    │
│     2 │ POLYGON ((62.2643051147460…  │                    │     42 │ leaf    │
│     2 │ POLYGON ((80.5032577514648…  │                    │     49 │ leaf    │
├───────┴──────────────────────────────┴────────────────────┴────────┴─────────┤
│ 84 rows (20 shown)                                                 5 columns │
└──────────────────────────────────────────────────────────────────────────────┘
```