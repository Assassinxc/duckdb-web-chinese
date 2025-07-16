---
---
layout: docu
redirect_from:
- /docs/guides/import/excel_import
- /docs/guides/import/excel_import/
- /docs/guides/file_formats/excel_import
title: Excel 导入
---

DuckDB 支持读取 Excel `.xlsx` 文件，但是不支持 `.xls` 文件。

## 导入 Excel 工作表

在查询的 `FROM` 子句中使用 `read_xlsx` 函数：

```sql
SELECT * FROM read_xlsx('test_excel.xlsx');
```

或者，您可以省略 `read_xlsx` 函数，让 DuckDB 从扩展中推断：

```sql
SELECT * FROM 'test_excel.xlsx';
```

然而，如果您希望能够传递选项以控制导入行为，应使用 `read_xlsx` 函数。

一个这样的选项是 `sheet` 参数，它允许指定 Excel 工作表的名称：

```sql
SELECT * FROM read_xlsx('test_excel.xlsx', sheet = 'Sheet1');
```

如果未指定工作表，则默认加载第一个工作表。

## 导入特定范围

要选择特定的单元格范围，使用格式为 `A1:B2` 的字符串作为 `range` 参数，其中 `A1` 是左上角单元格，`B2` 是右下角单元格：

```sql
SELECT * FROM read_xlsx('test_excel.xlsx', range = 'A1:B2');
```

这也可以用于跳过前 5 行：

```sql
SELECT * FROM read_xlsx('test_excel.xlsx', range = 'A5:Z');
```

或者跳过前 5 列：

```sql
SELECT * FROM read_xlsx('test_excel.xlsx', range = 'E:Z');
```

如果未提供 `range` 参数，则范围将自动推断为从连续非空单元格的第一行到相同列的第一个空行之间的矩形区域。

默认情况下，如果未提供范围，DuckDB 在遇到空行时将停止读取 Excel 文件。但当提供了范围时，默认行为是读取到范围的末尾。此行为可以通过 `stop_at_empty` 参数进行控制：

```sql
-- 读取前 100 行，或直到第一个空行，以先到达者为准
SELECT * FROM read_xlsx('test_excel.xlsx', range = '1:100', stop_at_empty = true);

-- 始终读取整个工作表，即使包含空行
SELECT * FROM read_xlsx('test_excel.xlsx', stop_at_empty = false);
```

## 创建新表

要使用查询结果创建新表，请使用 `CREATE TABLE ... AS` 从 `SELECT` 语句：

```sql
CREATE TABLE new_tbl AS
    SELECT * FROM read_xlsx('test_excel.xlsx', sheet = 'Sheet1');
```

## 加载到现有表

要从查询将数据加载到现有表中，请使用 `INSERT INTO` 从 `SELECT` 语句：

```sql
INSERT INTO tbl
    SELECT * FROM read_xlsx('test_excel.xlsx', sheet = 'Sheet1');
```

或者，您可以使用带有 `XLSX` 格式选项的 `COPY` 语句，将 Excel 文件导入现有表中：

```sql
COPY tbl FROM 'test_excel.xlsx' (FORMAT xlsx, SHEET 'Sheet1');
```

当使用 `COPY` 语句将 Excel 文件加载到现有表中时，目标表的列类型将用于强制 Excel 工作表中单元格的类型。

## 导入带有/不带标题的工作表

要将第一行视为结果列的名称，请使用 `header` 参数：

```sql
SELECT * FROM read_xlsx('test_excel.xlsx', header = true);
```

默认情况下，如果第一行中的所有单元格（在推断或提供的范围内）都是非空字符串，则会将第一行视为标题。要禁用此行为，请将 `header` 设置为 `false`。

## 类型检测

当不导入到现有表时，DuckDB 将尝试根据单元格内容和/或“数字格式”推断 Excel 工作表中列的类型。

- `TIMESTAMP`、`TIME`、`DATE` 和 `BOOLEAN` 类型将根据应用于单元格的“数字格式”进行推断。
- 包含 `TRUE` 和 `FALSE` 的文本单元格将被推断为 `BOOLEAN`。
- 空单元格默认被视为 `DOUBLE` 类型。
- 否则，根据内容将单元格推断为 `VARCHAR` 或 `DOUBLE`。

此行为可以通过以下方式调整。

要将所有空单元格视为 `VARCHAR` 而不是 `DOUBLE`，请将 `empty_as_varchar` 设置为 `true`：

```sql
SELECT * FROM read_xlsx('test_excel.xlsx', empty_as_varchar = true);
```

要完全禁用类型推断并把所有单元格视为 `VARCHAR`，请将 `all_varchar` 设置为 `true`：

```sql
SELECT * FROM read_xlsx('test_excel.xlsx', all_varchar = true);
```

此外，如果将 `ignore_errors` 参数设置为 `true`，DuckDB 将静默地将无法转换为相应推断列类型的单元格替换为 `NULL`。

```sql
SELECT * FROM read_xlsx('test_excel.xlsx', ignore_errors = true);
```

## 参见

DuckDB 还可以 [导出 Excel 文件]({% link docs/stable/guides/file_formats/excel_export.md %}).
如需更多关于 Excel 支持的详细信息，请参见 [Excel 扩展页面]({% link docs/stable/core_extensions/excel.md %})。