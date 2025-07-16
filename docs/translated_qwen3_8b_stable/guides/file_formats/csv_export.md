---
---
layout: docu
redirect_from:
- /docs/guides/import/csv_export
- /docs/guides/import/csv_export/
- /docs/guides/file_formats/csv_export
title: CSV 导出
---

要将表中的数据导出到 CSV 文件，可以使用 `COPY` 语句：

```sql
COPY tbl TO 'output.csv' (HEADER, DELIMITER ',');
```

查询结果也可以直接导出到 CSV 文件：

```sql
COPY (SELECT * FROM tbl) TO 'output.csv' (HEADER, DELIMITER ',');
```

如需了解其他选项，请参阅 [`COPY` 语句文档]({% link docs/stable/sql/statements/copy.md %}#csv-options)。