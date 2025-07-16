---
---
layout: docu
redirect_from:
- /docs/guides/import/csv_import
- /docs/guides/import/csv_import/
- /docs/guides/file_formats/csv_import
title: CSV 导入
---

要从 CSV 文件读取数据，可以在查询的 `FROM` 子句中使用 `read_csv` 函数：

```sql
SELECT * FROM read_csv('input.csv');
```

或者，可以省略 `read_csv` 函数，让 DuckDB 从扩展中推断：

```sql
SELECT * FROM 'input.csv';
```

要使用查询结果创建一个新表，可以使用 [`CREATE TABLE ... AS SELECT` 语句]({% link docs/stable/sql/statements/create_table.md %}#create-table--as-select-ctas)：

```sql
CREATE TABLE new_tbl AS
    SELECT * FROM read_csv('input.csv');
```

我们可以使用 DuckDB 的 [可选的 `FROM`-first 语法]({% link docs/stable/sql/query_syntax/from.md %}) 来省略 `SELECT *`：

```sql
CREATE TABLE new_tbl AS
    FROM read_csv('input.csv');
```

要将数据从查询导入现有表，可以使用 `INSERT INTO` 从 `SELECT` 语句中：

```sql
INSERT INTO tbl
    SELECT * FROM read_csv('input.csv');
```

或者，也可以使用 `COPY` 语句将 CSV 文件中的数据导入现有表：

```sql
COPY tbl FROM 'input.csv';
```

如需更多选项，请参阅 [CSV 导入参考]({% link docs/stable/data/csv/overview.md %}) 和 [`COPY` 语句文档]({% link docs/stable/sql/statements/copy.md %})。