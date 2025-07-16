---
---
layout: docu
redirect_from:
- /docs/guides/import/excel_export
- /docs/guides/import/excel_export/
- /docs/guides/file_formats/excel_export
title: Excel 导出
---

DuckDB 支持将数据导出为 Excel `.xlsx` 文件。然而，`.xls` 文件不被支持。

## 导出 Excel 工作表

要将表导出为 Excel 文件，可以使用带有 `FORMAT xlsx` 选项的 `COPY` 语句：

```sql
COPY tbl TO 'output.xlsx' WITH (FORMAT xlsx);
```

查询结果也可以直接导出为 Excel 文件：

```sql
COPY (SELECT * FROM tbl) TO 'output.xlsx' WITH (FORMAT xlsx);
```

若要将列名作为 Excel 文件的第一行，可以使用 `HEADER` 选项：

```sql
COPY tbl TO 'output.xlsx' WITH (FORMAT xlsx, HEADER true);
```

若要为生成的 Excel 文件中的工作表指定名称，可以使用 `SHEET` 选项：

```sql
COPY tbl TO 'output.xlsx' WITH (FORMAT xlsx, SHEET 'Sheet1');
```

## 类型转换

由于 Excel 仅真正支持存储数字或字符串（相当于 `VARCHAR` 和 `DOUBLE`），在写入 XLSX 文件时会自动应用以下类型转换：

* 数字类型会被转换为 `DOUBLE`。
* 时间类型（`TIMESTAMP`, `DATE`, `TIME` 等）会被转换为 Excel 的“序列”数字，即从 1900-01-01 开始的天数，以及时间的分数部分。这些数字随后会被设置为“数字格式”，以便在 Excel 中打开时显示为日期或时间。
* `TIMESTAMP_TZ` 和 `TIME_TZ` 会被转换为 UTC 的 `TIMESTAMP` 和 `TIME`，时区信息将被丢弃。
* `BOOLEAN` 会被转换为 `1` 和 `0`，并应用“数字格式”以在 Excel 中显示为 `TRUE` 和 `FALSE`。
* 所有其他类型会被转换为 `VARCHAR`，然后以文本单元格的形式写入。

当然，你也可以在导出到 Excel 前显式地将列转换为其他类型：

```sql
COPY (SELECT CAST(a AS VARCHAR), b FROM tbl) TO 'output.xlsx' WITH (FORMAT xlsx);
```

## 参见

DuckDB 还可以 [导入 Excel 文件]({% link docs/stable/guides/file_formats/excel_import.md %}).
如需更多关于 Excel 支持的详细信息，请参阅 [Excel 扩展页面]({% link docs/stable/core_extensions/excel.md %})。