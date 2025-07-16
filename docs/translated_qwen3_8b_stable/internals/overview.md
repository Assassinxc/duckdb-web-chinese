---
---
layout: docu
redirect_from:
- /internals/overview
- /internals/overview/
- /docs/internals/overview
title: DuckDB 内部结构概述
---

本页面简要描述了 DuckDB 引擎的内部结构。

## 解析器

解析器将查询字符串转换为以下标记：

* [`SQLStatement`](https://github.com/duckdb/duckdb/blob/main/src/include/duckdb/parser/sql_statement.hpp)
* [`QueryNode`](https://github.com/duckdb/duckdb/blob/main/src/include/duckdb/parser/query_node.hpp)
* [`TableRef`](https://github.com/duckdb/duckdb/blob/main/src/include/duckdb/parser/tableref.hpp)
* [`ParsedExpression`](https://github.com/duckdb/duckdb/blob/main/src/include/duckdb/parser/parsed_expression.hpp)

解析器并不了解目录或数据库的其他任何方面。如果表不存在，它不会抛出错误，也不会解析任何类型的列。它仅将查询字符串转换为指定的标记集合。

### ParsedExpression

ParsedExpression 表示 SQL 语句中的表达式。例如，它可以是列的引用、加法运算符或常量值。ParsedExpression 的类型表示其含义，例如比较操作符表示为 [`ComparisonExpression`](https://github.com/duckdb/duckdb/blob/main/src/include/duckdb/parser/expression/comparison_expression.hpp)。

ParsedExpressions 本身**不具有类型**，除非是具有显式类型的节点，例如 `CAST` 语句。表达式类型是在绑定器中解析的，而不是在解析器中。

### TableRef

TableRef 表示任意的表源。它可以是基表的引用，也可以是连接、生成表的函数或子查询。

### QueryNode

QueryNode 表示 (1) 一个 `SELECT` 语句，或 (2) 一个集合操作（即 `UNION`、`INTERSECT` 或 `DIFFERENCE`）。

### SQL 语句

SQLStatement 表示完整的 SQL 语句。SQL 语句的类型表示其种类（例如，`StatementType::SELECT` 表示一个 `SELECT` 语句）。如果原始查询字符串包含多个查询，一个 SQL 字符串可以被转换为多个 SQL 语句。

## 绑定器

绑定器将所有节点转换为它们的**绑定**等价形式。在绑定阶段：

* 使用目录解析表和列
* 解析类型
* 提取聚合/窗口函数

以下转换会进行：

* SQLStatement → [`BoundStatement`](https://github.com/duckdb/duckdb/blob/main/src/include/duckdb/planner/bound_statement.hpp)
* QueryNode → [`BoundQueryNode`](https://github.com/duckdb/duckdb/blob/main/src/include/duckdb/planner/bound_query_node.hpp)
* TableRef → [`BoundTableRef`](https://github.com/duckdb/duckdb/blob/main/src/include/duckdb/planner/bound_tableref.hpp)
* ParsedExpression → [`Expression`](https://github.com/duckdb/duckdb/blob/main/src/include/duckdb/planner/expression.hpp)

## 逻辑计划器

逻辑计划器从绑定语句创建 [`LogicalOperator`](https://github.com/duckdb/duckdb/blob/main/src/include/duckdb/planner/logical_operator.hpp) 节点。在此阶段，实际的逻辑查询树被创建。

## 优化器

在逻辑计划器创建了逻辑查询树之后，优化器会在该查询树上运行以创建优化的查询计划。以下查询优化器会被运行：

* **表达式重写器**：简化表达式，执行常量折叠
* **过滤下推**：将过滤条件下推到查询计划中，并在等价集上复制过滤条件。同时，会剪枝那些肯定为空的子树（由于过滤条件静态评估为假）。
* **连接顺序优化器**：使用动态规划重新排序连接。具体来说，使用了论文 [Dynamic Programming Strikes Back](https://15721.courses.cs.cmu.edu/spring2017/papers/14-optimizer1/p539-moerkotte.pdf) 中的 `DPccp` 算法。
* **公共子表达式**：从投影和过滤节点中提取公共子表达式以避免不必要的重复执行。
* **IN 子句重写器**：将大型静态 IN 子句重写为 MARK 连接或 INNER 连接。

## 列绑定解析器

列绑定解析器将逻辑 [`BoundColumnRefExpresion`](https://github.com/duckdb/duckdb/blob/main/src/include/duckdb/planner/expression/bound_columnref_expression.hpp) 节点（指向特定表的列）转换为 [`BoundReferenceExpression`](https://github.com/duckdb/duckdb/blob/main/src/include/duckdb/planner/expression/bound_reference_expression.hpp) 节点（指向执行引擎中传递的 DataChunks 的特定索引）。

## 物理计划生成器

物理计划生成器将生成的逻辑操作符树转换为 [`PhysicalOperator`](https://github.com/duckdb/duckdb/blob/main/src/include/duckdb/execution/physical_operator.hpp) 树。

## 执行

在执行阶段，物理操作符会被执行以生成查询结果。
DuckDB 使用基于推送的向量化模型，其中 [`DataChunks`](https://github.com/duckdb/duckdb/blob/main/src/include/duckdb/common/types/data_chunk.hpp) 会通过操作符树进行推送。
如需更多信息，请参见演讲 [Push-Based Execution in DuckDB](https://www.youtube.com/watch?v=1kDrPgRUuEI)。