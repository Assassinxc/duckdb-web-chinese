---
---
layout: docu
railroad: query_syntax/with.js
redirect_from:
- /docs/sql/query_syntax/with
title: WITH 子句
---

`WITH` 子句允许您指定公共表表达式（CTE）。
常规（非递归）公共表表达式本质上是作用域仅限于特定查询的视图。
CTE 可以相互引用，并且可以嵌套。[递归 CTE](#recursive-ctes) 可以引用自身。

## 基本 CTE 示例

创建一个名为 `cte` 的 CTE 并在主查询中使用它：

```sql
WITH cte AS (SELECT 42 AS x)
SELECT * FROM cte;
```

| x  |
|---:|
| 42 |

创建两个 CTE `cte1` 和 `cte2`，其中第二个 CTE 引用了第一个 CTE：

```sql
WITH
    cte1 AS (SELECT 42 AS i),
    cte2 AS (SELECT i * 100 AS x FROM cte1)
SELECT * FROM cte2;
```

|  x   |
|-----:|
| 4200 |

您可以为 CTE 指定列名：

```sql
WITH cte(j) AS (SELECT 42 AS i)
FROM cte;
```

## CTE 物化

DuckDB 可以使用 CTE 物化，而不是将 CTE 内联到主查询中。
这是通过启发式方法实现的：如果 CTE 进行了分组聚合并且被查询多次，则会进行物化。
可以通过使用 `AS MATERIALIZED` 显式激活物化，并通过使用 `AS NOT MATERIALIZED` 禁用物化。

以下是一个示例查询，该查询调用了同一个 CTE 三次：

```sql
WITH t(x) AS (⟨complex_query⟩)
SELECT *
FROM
    t AS t1,
    t AS t2,
    t AS t3;
```

内联会为每个引用重复定义 `t`，从而产生以下查询：

```sql
SELECT *
FROM
    (⟨complex_query⟩) AS t1(x),
    (⟨complex_query⟩) AS t2(x),
    (⟨complex_query⟩) AS t3(x);
```

如果 `complex_query` 很昂贵，使用 `MATERIALIZED` 关键字进行物化可以提高性能。在这种情况下，`complex_query` 仅评估一次。

```sql
WITH t(x) AS MATERIALIZED (⟨complex_query⟩)
SELECT *
FROM
    t AS t1,
    t AS t2,
    t AS t3;
```

如果要禁用物化，请使用 `NOT MATERIALIZED`：

```sql
WITH t(x) AS NOT MATERIALIZED (⟨complex_query⟩)
SELECT *
FROM
    t AS t1,
    t AS t2,
    t AS t3;
```

## 递归 CTE

`WITH RECURSIVE` 允许定义可以引用自身的 CTE。请注意，查询必须以确保终止的方式编写，否则可能会陷入无限循环。

### 示例：斐波那契数列

`WITH RECURSIVE` 可用于进行递归计算。例如，下面是使用 `WITH RECURSIVE` 计算前十个斐波那契数的方法：

```sql
WITH RECURSIVE FibonacciNumbers (
    RecursionDepth, FibonacciNumber, NextNumber
) AS (
        -- 基础情况
        SELECT
            0 AS RecursionDepth,
            0 AS FibonacciNumber,
            1 AS NextNumber
        UNION ALL
        -- 递归步骤
        SELECT
            fib.RecursionDepth + 1 AS RecursionDepth,
            fib.NextNumber AS FibonacciNumber,
            fib.FibonacciNumber + fib.NextNumber AS NextNumber
        FROM
            FibonacciNumbers fib
        WHERE
            fib.RecursionDepth + 1 < 10
    )
SELECT
    fn.RecursionDepth AS FibonacciNumberIndex,
    fn.FibonacciNumber
FROM
    FibonacciNumbers fn;
```

| FibonacciNumberIndex | FibonacciNumber |
|---------------------:|----------------:|
| 0                    | 0               |
| 1                    | 1               |
| 2                    | 1               |
| 3                    | 2               |
| 4                    | 3               |
| 5                    | 5               |
| 6                    | 8               |
| 7                    | 13              |
| 8                    | 21              |
| 9                    | 34              |

### 示例：树遍历

`WITH RECURSIVE` 可用于遍历树。例如，考虑一个标签的层次结构：

<img id="tree-example" alt="示例树" style="width: 700px; text-align: center">

```sql
CREATE TABLE tag (id INTEGER, name VARCHAR, subclassof INTEGER);
INSERT INTO tag VALUES
    (1, 'U2',     5),
    (2, 'Blur',   5),
    (3, 'Oasis',  5),
    (4, '2Pac',   6),
    (5, 'Rock',   7),
    (6, 'Rap',    7),
    (7, 'Music',  9),
    (8, 'Movies', 9),
    (9, 'Art', NULL);
```

以下查询返回从节点 `Oasis` 到树根节点 `Art` 的路径。

```sql
WITH RECURSIVE tag_hierarchy(id, source, path) AS (
        SELECT id, name, [name] AS path
        FROM tag
        WHERE subclassof IS NULL
    UNION ALL
        SELECT tag.id, tag.name, list_prepend(tag.name, tag_hierarchy.path)
        FROM tag, tag_hierarchy
        WHERE tag.subclassof = tag_hierarchy.id
    )
SELECT path
FROM tag_hierarchy
WHERE source = 'Oasis';
```

|           path            |
|---------------------------|
| [Oasis, Rock, Music, Art] |

### 图遍历

`WITH RECURSIVE` 子句可用于表达任意图上的图遍历。然而，如果图中存在环，查询必须执行环检测以防止无限循环。
实现这一目标的一种方法是将遍历路径存储在 [列表]({% link docs/stable/sql/data_types/list.md %}) 中，并在扩展路径时检查端点是否已被访问（请参见后面的示例）。

以下是从 [LDBC Graphalytics 基准](https://arxiv.org/pdf/2011.15028.pdf) 中的有向图：

<img id="graph-example" alt="示例图" style="width: 700px; text-align: center">

```sql
CREATE TABLE edge (node1id INTEGER, node2id INTEGER);
INSERT INTO edge VALUES
    (1, 3), (1, 5), (2, 4), (2, 5), (2, 10), (3, 1),
    (3, 5), (3, 8), (3, 10), (5, 3), (5, 4), (5, 8),
    (6, 3), (6, 4), (7, 4), (8, 1), (9, 4);
```

请注意，该图包含有向环，例如在节点 1、5 和 8 之间。

#### 枚举从某个节点的所有路径

以下查询返回从节点 1 开始的所有路径：

```sql
WITH RECURSIVE paths(startNode, endNode, path) AS (
        SELECT -- 定义路径为遍历的第一个边
            node1id AS startNode,
            node2id AS endNode,
            [node1id, node2id] AS path
        FROM edge
        WHERE startNode = 1
        UNION ALL
        SELECT -- 将新边添加到路径中
            paths.startNode AS startNode,
            node2id AS endNode,
            array_append(path, node2id) AS path
        FROM paths
        JOIN edge ON paths.endNode = node1id
        -- 防止将重复的节点添加到路径中。
        -- 这确保不会出现循环。
        WHERE list_position(paths.path, node2id) IS NULL
    )
SELECT startNode, endNode, path
FROM paths
ORDER BY length(path), path;
```

| startNode | endNode |     path      |
|----------:|--------:|---------------|
| 1         | 3       | [1, 3]        |
| 1         | 5       | [1, 5]        |
| 1         | 5       | [1, 3, 5]     |
| 1         | 8       | [1, 3, 8]     |
| 1         | 10      | [1, 3, 10]    |
| 1         | 3       | [1, 5, 3]     |
| 1         | 4       | [1, 5, 4]     |
| 1         | 8       | [1, 5, 8]     |
| 1         | 4       | [1, 3, 5, 4]  |
| 1         | 8       | [1, 3, 5, 8]  |
| 1         | 8       | [1, 5, 3, 8]  |
| 1         | 10      | [1, 5, 3, 10] |

请注意，此查询的结果不限于最短路径。例如，对于节点 5，结果包括路径 `[1, 5]` 和 `[1, 3, 5]`。

#### 枚举从某个节点的无权最短路径

在大多数情况下，枚举所有路径是不实际或不可行的。相反，我们只关心 **(无权) 最短路径**。为了找到这些路径，应调整 `WITH RECURSIVE` 查询的后半部分，使得仅包含尚未访问过的节点。这通过使用一个子查询来检查之前的路径是否包含该节点来实现：

```sql
WITH RECURSIVE paths(startNode, endNode, path) AS (
        SELECT -- 定义路径为遍历的第一个边
            node1id AS startNode,
            node2id AS endNode,
            [node1id, node2id] AS path
        FROM edge
        WHERE startNode = 1
        UNION ALL
        SELECT -- 将新边添加到路径中
            paths.startNode AS startNode,
            node2id AS endNode,
            array_append(path, node2id) AS path
        FROM paths
        JOIN edge ON paths.endNode = node1id
        -- 防止添加之前任何路径中已经访问过的节点。
        -- 这确保 (1) 不出现循环，并且 (2) 仅添加未被之前（较短）路径访问过的节点。
        WHERE NOT EXISTS (
                FROM paths previous_paths
                WHERE list_contains(previous_paths.path, node2id)
              )
    )
SELECT startNode, endNode, path
FROM paths
ORDER BY length(path), path;
```

| startNode | endNode |    path    |
|----------:|--------:|------------|
| 1         | 3       | [1, 3]     |
| 1         | 5       | [1, 5]     |
| 1         | 8       | [1, 3, 8]  |
| 1         | 10      | [1, 3, 10] |
| 1         | 4       | [1, 5, 4]  |
| 1         | 8       | [1, 5, 8]  |

#### 枚举两个节点之间的无权最短路径

`WITH RECURSIVE` 也可以用于查找 **两个节点之间的所有无权最短路径**。为了确保在到达终点时立即停止递归查询，我们使用 [窗口函数]({% link docs/stable/sql/functions/window_functions.md %}) 来检查终点是否在新添加的节点中。

以下查询返回节点 1（起点）和节点 8（终点）之间的所有无权最短路径：

```sql
WITH RECURSIVE paths(startNode, endNode, path, endReached) AS (
   SELECT -- 定义路径为遍历的第一个边
        node1id AS startNode,
        node2id AS endNode,
        [node1id, node2id] AS path,
        (node2id = 8) AS endReached
     FROM edge
     WHERE startNode = 1
   UNION ALL
   SELECT -- 将新边添加到路径中
        paths.startNode AS startNode,
        node2id AS endNode,
        array_append(path, node2id) AS path,
        max(CASE WHEN node2id = 8 THEN 1 ELSE 0 END)
            OVER (ROWS BETWEEN UNBOUNDED PRECEDING
                           AND UNBOUNDED FOLLOWING) AS endReached
     FROM paths
     JOIN edge ON paths.endNode = node1id
    WHERE NOT EXISTS (
            FROM paths previous_paths
            WHERE list_contains(previous_paths.path, node2id)
          )
      AND paths.endReached = 0
)
SELECT startNode, endNode, path
FROM paths
WHERE endNode = 8
ORDER BY length(path), path;
```

| startNode | endNode |   path    |
|----------:|--------:|-----------|
| 1         | 8       | [1, 3, 8] |
| 1         | 8       | [1, 5, 8] |

## 使用 `USING KEY` 的递归 CTE

`USING KEY` 会改变常规递归 CTE 的行为。

在每次迭代中，常规递归 CTE 会将结果行追加到联合表中，最终定义 CTE 的整体结果。相反，带有 `USING KEY` 的 CTE 能够更新在早期迭代中放入联合表中的行：如果当前迭代生成一个键为 `k` 的行，则会替换联合表中相同键 `k` 的行（类似于字典）。如果联合表中尚不存在该键，则新行会像往常一样追加到联合表中。

这允许 CTE 对联合表的内容进行细粒度控制。避免仅追加行为可以显著减小联合表的大小。这有助于查询运行时间、内存消耗，并使在迭代过程中访问联合表成为可能（这在常规递归 CTE 中是不可能的）：在 CTE `WITH RECURSIVE T(...) USING KEY ...` 中，表 `T` 表示最后一次迭代中添加的行（与常规递归 CTE 一样），而表 `recurring.T` 表示到目前为止构建的联合表。对 `recurring.T` 的引用允许将较为复杂的算法优雅地转换为可读的 SQL 代码。

### 示例：`USING KEY`

这是一个使用 `USING KEY` 的递归 CTE，其中 `USING KEY` 有一个键列 (`a`) 和一个负载列 (`b`)。
负载列对应于要覆盖的列。
在第一次迭代中，我们有两个不同的键，`1` 和 `2`。
这两个键将生成两行新数据，`(1, 3)` 和 `(2, 4)`。
在下一次迭代中，我们生成一个新的键 `3`，生成一行新数据。
我们还会生成一行 `(2, 3)`，其中 `2` 是一个已存在于前一次迭代中的键。
这将覆盖旧的负载 `4` 为新的负载 `3`。

```sql
WITH RECURSIVE tbl(a, b) USING KEY (a) AS (
    SELECT a, b
    FROM (VALUES (1, 3), (2, 4)) t(a, b)
        UNION
    SELECT a + 1, b
    FROM tbl
    WHERE a < 3
)
SELECT *
FROM tbl;
```

| a | b |
|--:|--:|
| 1 | 3 |
| 2 | 3 |
| 3 | 3 |

## 使用 `VALUES`

您可以使用 `VALUES` 子句用于 CTE 的初始（锚定）部分：

```sql
WITH RECURSIVE tbl(a, b) USING KEY (a) AS (
    VALUES (1, 3), (2, 4)
        UNION
    SELECT a + 1, b
    FROM tbl
    WHERE a < 3
)
SELECT *
FROM tbl;
```

### 示例：`USING KEY` 引用联合表

除了将联合表作为字典使用，我们还可以在查询中引用它。这允许您使用不仅限于上一次迭代，还包括更早的迭代的结果。这一新功能使得某些算法更容易实现。

一个例子是连通分量算法。对于每个节点，该算法确定它连接的具有最低 ID 的节点。为了实现这一点，我们使用联合表中的条目来跟踪每个节点找到的最低 ID。如果新传入的行包含更低的 ID，我们将更新此值。

<img id="uk-example" alt="示例图" style="width: 700px; text-align: center">

```sql
CREATE TABLE nodes (id INTEGER);
INSERT INTO nodes VALUES (1), (2), (3), (4), (5), (6), (7), (8);
CREATE TABLE edges (node1id INTEGER, node2id INTEGER);
INSERT INTO edges VALUES
    (1, 3), (2, 3), (3, 7), (7, 8), (5, 4),
    (6, 4);
```

```sql
WITH RECURSIVE cc(id, comp) USING KEY (id) AS (
    SELECT n.id, n.id AS comp
    FROM nodes AS n
        UNION
    (SELECT DISTINCT ON (u.id) u.id, v.comp
    FROM recurring.cc AS u, cc AS v, edges AS e
    WHERE ((e.node1id, e.node2id) = (u.id, v.id)
       OR (e.node2id, e.node1id) = (u.id, v.id))
      AND v.comp < u.comp
    ORDER BY u.id ASC, v.comp ASC)
)
TABLE cc
ORDER BY id;
```

| id | comp |
|---:|-----:|
| 1  | 1    |
| 2  | 1    |
| 3  | 1    |
| 4  | 4    |
| 5  | 4    |
| 6  | 4    |
| 7  | 1    |
| 8  | 1    |

## 局限性

DuckDB 不支持相互递归的 CTE。请参阅 DuckDB 仓库中 [相关的 issue 和讨论](https://github.com/duckdb/duckdb/issues/14716#issuecomment-2467952456)。

## 语法

<div id="rrdiagram"></div>

---