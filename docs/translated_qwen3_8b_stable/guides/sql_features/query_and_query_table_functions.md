---
---
layout: docu
redirect_from:
- /docs/guides/sql_features/query_and_query_table_functions
title: query 和 query_table 函数
---

[`query`]({% link docs/stable/sql/functions/utility.md %}#queryquery_string_literal)
和 [`query_table`]({% link docs/stable/sql/functions/utility.md %}#query_tabletbl_name)
函数接受一个字符串字面量，并分别将其转换为 `SELECT` 子查询和表引用。
请注意，这些函数仅接受字面量字符串。
因此，它们不如通用的 `eval` 函数强大（或危险）。

这些函数在概念上很简单，但可以实现强大且更动态的 SQL。例如，它们允许将表名作为预编译语句参数传递：

```sql
CREATE TABLE my_table (i INTEGER);
INSERT INTO my_table VALUES (42);

PREPARE select_from_table AS SELECT * FROM query_table($1);
EXECUTE select_from_table('my_table');
```

| i  |
|---:|
| 42 |

当与 [`COLUMNS` 表达式]({% link docs/stable/sql/expressions/star.md %}#columns) 结合使用时，我们可以编写非常通用的 SQL 宏。例如，下面是一个自定义的 `SUMMARIZE` 函数，它会计算表中每一列的 `min` 和 `max`：

```sql
CREATE OR REPLACE MACRO my_summarize(table_name) AS TABLE
SELECT
    unnest([*COLUMNS('alias_.*')]) AS column_name,
    unnest([*COLUMNS('min_.*')]) AS min_value,
    unnest([*COLUMNS('max_.*')]) AS max_value
FROM (
    SELECT
        any_value(alias(COLUMNS(*))) AS "alias_\0",
        min(COLUMNS(*))::VARCHAR AS "min_\0",
        max(COLUMNS(*))::VARCHAR AS "max_\0"
    FROM query_table(table_name::VARCHAR)
);

SELECT *
FROM my_summarize('https://blobs.duckdb.org/data/ontime.parquet')
LIMIT 3;
```

| column_name | min_value | max_value |
|-------------|----------:|----------:|
| year        | 2017      | 2017      |
| quarter     | 1         | 3         |
| month       | 1         | 9         |