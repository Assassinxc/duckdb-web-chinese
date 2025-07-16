---
---
layout: docu
redirect_from:
- /docs/data/overview
title: 数据导入
---

使用数据库系统的第一个步骤是将数据插入到该系统中。
DuckDB 可以直接连接到 [许多流行的数据源]({% link docs/stable/data/data_sources.md %})，并提供了几种数据摄入方法，使您可以轻松高效地填充数据库。
在本页中，我们提供了这些方法的概述，以便您可以选择最适合您使用场景的方法。

## `INSERT` 语句

`INSERT` 语句是将数据加载到数据库系统中的标准方法。它们适用于快速原型开发，但应避免用于批量加载，因为它们具有显著的每行开销。

```sql
INSERT INTO people VALUES (1, 'Mark');
```

如需更详细的描述，请参阅 [关于 `INSERT` 语句的页面]({% link docs/stable/data/insert.md %}).

## 文件加载：相对路径

使用配置选项 [`file_search_path`]({% link docs/stable/configuration/overview.md %}#local-configuration-options) 来配置相对路径扩展到哪些“根目录”。
如果未设置 `file_search_path`，则使用工作目录作为相对路径的基础。

## 文件格式

### CSV 加载

可以使用几种方法从 CSV 文件高效加载数据。最简单的是使用 CSV 文件的名称：

```sql
SELECT * FROM 'test.csv';
```

或者使用 [`read_csv` 函数]({% link docs/stable/data/csv/overview.md %}) 来传递选项：

```sql
SELECT * FROM read_csv('test.csv', header = false);
```

或者使用 [`COPY` 语句]({% link docs/stable/sql/statements/copy.md %}#copy--from):

```sql
COPY tbl FROM 'test.csv' (HEADER false);
```

也可以直接从 **压缩的 CSV 文件** 中读取数据（例如，使用 [gzip](https://www.gzip.org/) 压缩）：

```sql
SELECT * FROM 'test.csv.gz';
```

DuckDB 可以使用 [`CREATE TABLE ... AS SELECT` 语句]({% link docs/stable/sql/statements/create_table.md %}#create-table--as-select-ctas) 从加载的数据创建表：

```sql
CREATE TABLE test AS
    SELECT * FROM 'test.csv';
```

如需更多详情，请参阅 [CSV 加载页面]({% link docs/stable/data/csv/overview.md %}).

### Parquet 加载

可以使用文件名高效加载和查询 Parquet 文件：

```sql
SELECT * FROM 'test.parquet';
```

或者使用 [`read_parquet` 函数]({% link docs/stable/data/parquet/overview.md %})：

```sql
SELECT * FROM read_parquet('test.parquet');
```

或者使用 [`COPY` 语句]({% link docs/stable/sql/statements/copy.md %}#copy--from):

```sql
COPY tbl FROM 'test.parquet';
```

如需更多详情，请参阅 [Parquet 加载页面]({% link docs/stable/data/parquet/overview.md %}).

### JSON 加载

可以使用文件名高效加载和查询 JSON 文件：

```sql
SELECT * FROM 'test.json';
```

或者使用 [`read_json_auto` 函数]({% link docs/stable/data/json/overview.md %})：

```sql
SELECT * FROM read_json_auto('test.json');
```

或者使用 [`COPY` 语句]({% link docs/stable/sql/statements/copy.md %}#copy--from):

```sql
COPY tbl FROM 'test.json';
```

如需更多详情，请参阅 [JSON 加载页面]({% link docs/stable/data/json/overview.md %}).

### 返回文件名

自 DuckDB v1.3.0 起，CSV、JSON 和 Parquet 读取器支持 `filename` 虚拟列：

```sql
COPY (FROM (VALUES (42), (43)) t(x)) TO 'test.parquet';
SELECT *, filename FROM 'test.parquet';
```

## Appender

在多个 API（C、C++、Go、Java 和 Rust）中，[Appender]({% link docs/stable/data/appender.md %}) 可作为批量数据加载的替代方案。
该类可用于在不使用 SQL 语句的情况下高效地将行添加到数据库系统中。