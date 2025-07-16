---
---
layout: docu
redirect_from:
- /docs/guides/import/parquet_export
- /docs/guides/import/parquet_export/
- /docs/guides/file_formats/parquet_export
title: Parquet 导出
---

要将表中的数据导出到 Parquet 文件，可以使用 `COPY` 语句：

```sql
COPY tbl TO 'output.parquet' (FORMAT parquet);
```

查询结果也可以直接导出到 Parquet 文件：

```sql
COPY (SELECT * FROM tbl) TO 'output.parquet' (FORMAT parquet);
```

有关设置压缩、行组大小等标志的详细信息，请参阅[Parquet 文件的读取和写入]({% link docs/stable/data/parquet/overview.md %}) 页面。