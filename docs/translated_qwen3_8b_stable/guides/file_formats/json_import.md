---
---
layout: docu
redirect_from:
- /docs/guides/import/json_import
- /docs/guides/import/json_import/
- /docs/guides/file_formats/json_import
title: JSON 导入
---

要从 JSON 文件读取数据，请在查询的 `FROM` 子句中使用 `read_json_auto` 函数：

```sql
SELECT *
FROM read_json_auto('input.json');
```

要使用查询结果创建新表，请从 `SELECT` 语句使用 `CREATE TABLE AS`：

```sql
CREATE TABLE new_tbl AS
    SELECT *
    FROM read_json_auto('input.json');
```

要将数据从查询加载到现有表中，请从 `SELECT` 语句使用 `INSERT INTO`：

```sql
INSERT INTO tbl
    SELECT *
    FROM read_json_auto('input.json');
```

或者，也可以使用 `COPY` 语句将数据从 JSON 文件加载到现有表中：

```sql
COPY tbl FROM 'input.json';
```

如需更多选项，请参阅 [JSON 加载参考]({% link docs/stable/data/json/overview.md %}) 和 [`COPY` 语句文档]({% link docs/stable/sql/statements/copy.md %})。