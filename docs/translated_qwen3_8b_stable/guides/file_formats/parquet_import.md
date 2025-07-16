---
---
layout: docu
redirect_from:
- /docs/guides/import/parquet_import
- /docs/guides/import/parquet_import/
- /docs/guides/file_formats/parquet_import
title: Parquet 导入
---

要从 Parquet 文件读取数据，可以在查询的 `FROM` 子句中使用 `read_parquet` 函数：

```sql
SELECT * FROM read_parquet('input.parquet');
```

或者，可以省略 `read_parquet` 函数，让 DuckDB 从扩展中推断：

```sql
SELECT * FROM 'input.parquet';
```

要使用查询结果创建一个新表，可以使用 [`CREATE TABLE ... AS SELECT` 语句]({% link docs/stable/sql/statements/create_table.md %}#create-table--as-select-ctas)：

```sql
CREATE TABLE new_tbl AS
    SELECT * FROM read_parquet('input.parquet');
```

要从查询结果将数据加载到现有表中，可以使用 `INSERT INTO` 从 `SELECT` 语句：

```sql
INSERT INTO tbl
    SELECT * FROM read_parquet('input.parquet');
```

或者，也可以使用 `COPY` 语句将 Parquet 文件中的数据加载到现有表中：

```sql
COPY tbl FROM 'input.parquet' (FORMAT parquet);
```

## 动态调整模式

你可以使用以下技巧将 Parquet 文件加载到一个略有不同的模式中（例如，不同的列数、更宽松的类型）。

假设我们有一个包含两个列 `c1` 和 `c2` 的 Parquet 文件：

```sql
COPY (FROM (VALUES (42, 43)) t(c1, c2))
TO 'f.parquet';
```

如果我们想要添加一个文件中不存在的列 `c3`，可以运行：

```sql
FROM (VALUES(NULL::VARCHAR, NULL, NULL)) t(c1, c2, c3)
WHERE false
UNION ALL BY NAME
FROM 'f.parquet';
```

第一个 `FROM` 子句生成一个包含 *三个* 列的空表，其中 `c1` 是 `VARCHAR` 类型。然后，我们使用 `UNION ALL BY NAME` 来合并 Parquet 文件。结果如下：

```text
┌─────────┬───────┬───────┐
│   c1    │  c2   │  c3   │
│ varchar │ int32 │ int32 │
├─────────┼───────┼───────┤
│ 42      │  43   │ NULL  │
└─────────┴───────┴───────┘
```

如需更多选项，请参阅 [Parquet 加载参考]({% link docs/stable/data/parquet/overview.md %})。