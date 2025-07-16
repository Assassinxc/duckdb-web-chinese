---
---
blurb: QUALIFY 子句用于过滤 WINDOW 函数的结果。
layout: docu
railroad: query_syntax/qualify.js
redirect_from:
- /docs/sql/query_syntax/qualify
title: QUALIFY 子句
---

`QUALIFY` 子句用于过滤 [`WINDOW` 函数]({% link docs/stable/sql/functions/window_functions.md %}) 的结果。这种结果过滤方式类似于 [`HAVING` 子句]({% link docs/stable/sql/query_syntax/having.md %}) 对基于 [`GROUP BY` 子句]({% link docs/stable/sql/query_syntax/groupby.md %}) 应用的聚合函数进行结果过滤的方式。

`QUALIFY` 子句避免了使用子查询或 [`WITH` 子句]({% link docs/stable/sql/query_syntax/with.md %}) 来执行这种过滤（与 `HAVING` 类似，它也避免使用子查询）。下面的 `QUALIFY` 示例中包含了一个使用 `WITH` 子句而不是 `QUALIFY` 的示例。

请注意，这里是基于 [`WINDOW` 函数]({% link docs/stable/sql/functions/window_functions.md %}) 的过滤，而不一定是基于 [`WINDOW` 子句]({% link docs/stable/sql/query_syntax/window.md %})。`WINDOW` 子句是可选的，可以用来简化创建多个 `WINDOW` 函数表达式。

`QUALIFY` 子句的指定位置在 `SELECT` 语句中的 [`WINDOW` 子句]({% link docs/stable/sql/query_syntax/window.md %}) 之后（`WINDOW` 子句不需要指定），并在 [`ORDER BY`]({% link docs/stable/sql/query_syntax/orderby.md %}) 之前。

## 示例

以下每个示例都产生相同的输出，位于下方。

基于 `QUALIFY` 子句中定义的窗口函数进行过滤：

```sql
SELECT
    schema_name,
    function_name,
    -- 在此示例中，select 子句中的 function_rank 列仅用于参考
    row_number() OVER (PARTITION BY schema_name ORDER BY function_name) AS function_rank
FROM duckdb_functions()
QUALIFY
    row_number() OVER (PARTITION BY schema_name ORDER BY function_name) < 3;
```

基于 `SELECT` 子句中定义的窗口函数进行过滤：

```sql
SELECT
    schema_name,
    function_name,
    row_number() OVER (PARTITION BY schema_name ORDER BY function_name) AS function_rank
FROM duckdb_functions()
QUALIFY
    function_rank < 3;
```

基于 `QUALIFY` 子句中定义的窗口函数进行过滤，但使用 `WINDOW` 子句：

```sql
SELECT
    schema_name,
    function_name,
    -- 在此示例中，select 子句中的 function_rank 列仅用于参考
    row_number() OVER my_window AS function_rank
FROM duckdb_functions()
WINDOW
    my_window AS (PARTITION BY schema_name ORDER BY function_name)
QUALIFY
    row_number() OVER my_window < 3;
```

基于 `SELECT` 子句中定义的窗口函数进行过滤，但使用 `WINDOW` 子句：

```sql
SELECT
    schema_name,
    function_name,
    row_number() OVER my_window AS function_rank
FROM duckdb_functions()
WINDOW
    my_window AS (PARTITION BY schema_name ORDER BY function_name)
QUALIFY
    function_rank < 3;
```

基于 `WITH` 子句的等效查询（不使用 `QUALIFY` 子句）：

```sql
WITH ranked_functions AS (
    SELECT
        schema_name,
        function_name,
        row_number() OVER (PARTITION BY schema_name ORDER BY function_name) AS function_rank
    FROM duckdb_functions()
)
SELECT
    *
FROM ranked_functions
WHERE
    function_rank < 3;
```

| schema_name |  function_name  | function_rank |
|:---|:---|:---|
| main        | !__postfix      | 1             |
| main        | !~~             | 2             |
| pg_catalog  | col_description | 1             |
| pg_catalog  | format_pg_type  | 2             |

## 语法

<div id="rrdiagram"></div>