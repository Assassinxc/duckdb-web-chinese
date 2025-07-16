---
---
layout: docu
railroad: statements/comment.js
redirect_from:
- /docs/sql/statements/comment_on
title: COMMENT ON 语句
---

`COMMENT ON` 语句允许向目录条目（表、列等）添加元数据。
它遵循 [PostgreSQL 语法](https://www.postgresql.org/docs/16/sql-comment.html)。

## 示例

在 `TABLE` 上创建注释：

```sql
COMMENT ON TABLE test_table IS 'very nice table';
```

在 `COLUMN` 上创建注释：

```sql
COMMENT ON COLUMN test_table.test_table_column IS 'very nice column';
```

在 `VIEW` 上创建注释：

```sql
COMMENT ON VIEW test_view IS 'very nice view';
```

在 `INDEX` 上创建注释：

```sql
COMMENT ON INDEX test_index IS 'very nice index';
```

在 `SEQUENCE` 上创建注释：

```sql
COMMENT ON SEQUENCE test_sequence IS 'very nice sequence';
```

在 `TYPE` 上创建注释：

```sql
COMMENT ON TYPE test_type IS 'very nice type';
```

在 `MACRO` 上创建注释：

```sql
COMMENT ON MACRO test_macro IS 'very nice macro';
```

在 `MACRO TABLE` 上创建注释：

```sql
COMMENT ON MACRO TABLE test_table_macro IS 'very nice table macro';
```

要取消注释，将其设置为 `NULL`，例如：

```sql
COMMENT ON TABLE test_table IS NULL;
```

## 读取注释

可以通过查询相应 [元数据函数]({% link docs/stable/sql/meta/duckdb_table_functions.md %}) 的 `comment` 列来读取注释：

列出 `TABLE` 的注释：

```sql
SELECT comment FROM duckdb_tables();
```

列出 `COLUMN` 的注释：

```sql
SELECT comment FROM duckdb_columns();
```

列出 `VIEW` 的注释：

```sql
SELECT comment FROM duckdb_views();
```

列出 `INDEX` 的注释：

```sql
SELECT comment FROM duckdb_indexes();
```

列出 `SEQUENCE` 的注释：

```sql
SELECT comment FROM duckdb_sequences();
```

列出 `TYPE` 的注释：

```sql
SELECT comment FROM duckdb_types();
```

列出 `MACRO` 的注释：

```sql
SELECT comment FROM duckdb_functions();
```

列出 `MACRO TABLE` 的注释：

```sql
SELECT comment FROM duckdb_functions();
```

## 局限性

`COMMENT ON` 语句目前有以下限制：

* 无法对模式或数据库进行注释。
* 无法对具有依赖关系的项目进行注释（例如，带有索引的表）。

## 语法

<div id="rrdiagram1"></div>