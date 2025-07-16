---
---
github_repository: https://github.com/duckdb/duckdb-excel
layout: docu
title: Excel 扩展
redirect_from:
- /docs/stable/extensions/excel
- /docs/stable/extensions/excel/
- /docs/extensions/excel
- /docs/extensions/excel/
---

`excel` 扩展通过封装 [i18npool 库](https://www.openoffice.org/l10n/i18n_framework/index.html) 提供了按 Excel 格式规则格式化数字的函数，但从 DuckDB 1.2 开始，也提供了读取和写入 Excel（`.xlsx`）文件的功能。但是，`.xls` 文件不被支持。

此前，读取和写入 Excel 文件是通过 [`spatial` 扩展]({% link docs/stable/core_extensions/spatial/overview.md %}) 来处理的，巧合的是，它通过其中一个依赖项包含了对 XLSX 文件的支持，但此功能可能在未来从 spatial 扩展中移除。此外，`excel` 扩展更高效，并且提供了对导入/导出过程的更多控制。请参阅 [Excel 导入]({% link docs/stable/guides/file_formats/excel_import.md %}) 和 [Excel 导出]({% link docs/stable/guides/file_formats/excel_export.md %}) 页面以获取说明。

## 安装和加载

`excel` 扩展将在首次使用时从官方扩展仓库中透明地[自动加载]({% link docs/stable/core_extensions/overview.md %}#autoloading-extensions)。
如果您想手动安装和加载它，请运行：

```sql
INSTALL excel;
LOAD excel;
```

## Excel 标量函数

| 函数                            | 描述                                                          |
| :---------------------------------- | :------------------------------------------------------------------- |
| `excel_text(number, format_string)` | 根据 `format_string` 中的规则格式化给定的 `number` |
| `text(number, format_string)`       | `excel_text` 的别名                                               |

## 示例

```sql
SELECT excel_text(1_234_567.897, 'h:mm AM/PM') AS timestamp;
```

| timestamp |
| --------- |
| 9:31 PM   |

```sql
SELECT excel_text(1_234_567.897, 'h AM/PM') AS timestamp;
```

| timestamp |
| --------- |
| 9 PM      |

## 读取 XLSX 文件

读取 `.xlsx` 文件就像立即从文件中进行 `SELECT` 一样简单，例如：

```sql
SELECT *
FROM 'test.xlsx';
```

|   a |   b |
| --: | --: |
| 1.0 | 2.0 |
| 3.0 | 4.0 |

不过，如果您想设置额外的选项以控制导入过程，可以使用 `read_xlsx` 函数。以下支持的命名参数。

| 选项             | 类型      | 默认值                  | 描述                                                                                                                                                                                                                                                                                           |
| ------------------ | --------- | ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `header`           | `BOOLEAN` | _自动推断_              | 是否将第一行视为结果列的名称。                                                                                                                                                                                                                                               |
| `sheet`            | `VARCHAR` | _自动推断_              | 要读取的 xlsx 文件中的工作表名称。默认是第一个工作表。                                                                                                                                                                                                                           |
| `all_varchar`      | `BOOLEAN` | `false`                  | 是否将所有单元格视为包含 `VARCHAR`。                                                                                                                                                                                                                                                   |
| `ignore_errors`    | `BOOLEAN` | `false`                  | 是否忽略错误并静默地将无法转换为相应推断列类型的单元格替换为 `NULL`。                                                                                                                                                                                                                                        |
| `range`            | `VARCHAR` | _自动推断_              | 要读取的单元格范围，使用电子表格表示法。例如，`A1:B2` 读取 A1 到 B2 的单元格。如果没有指定，则推断结果范围为连续非空单元格的第一行和相同列的第一个空行之间的矩形区域。 |
| `stop_at_empty`    | `BOOLEAN` | _自动推断_              | 是否在遇到空行时停止读取文件。如果提供了显式的 `range` 选项，则默认为 `false`，否则为 `true`。                                                                                                                                                                                                           |
| `empty_as_varchar` | `BOOLEAN` | `false`                  | 是否将空单元格视为 `VARCHAR` 而不是 `DOUBLE`，在尝试自动推断列类型时。                                                                                                                                                                                        |

```sql
SELECT *
FROM read_xlsx('test.xlsx', header = true);
```

|   a |   b |
| --: | --: |
| 1.0 | 2.0 |
| 3.0 | 4.0 |

或者，可以使用带有 `XLSX` 格式选项的 `COPY` 语句，将 Excel 文件导入现有表中，此时目标表的列类型将用于强制转换 Excel 文件中的单元格类型。

```sql
CREATE TABLE test (a DOUBLE, b DOUBLE);
COPY test FROM 'test.xlsx' WITH (FORMAT xlsx, HEADER);
SELECT * FROM test;
```

### 类型和范围推断

由于 Excel 本身只在单元格中真正存储数字或字符串，并不限制列中所有单元格的类型相同，因此 `excel` 扩展必须做一些猜测工作，以“推断”并决定在导入 Excel 表时列的类型。虽然几乎所有的列都被推断为 `DOUBLE` 或 `VARCHAR`，但有一些注意事项：

* `TIMESTAMP`、`TIME`、`DATE` 和 `BOOLEAN` 类型会根据单元格应用的格式进行推断。
* 包含 `TRUE` 和 `FALSE` 的文本单元格被推断为 `BOOLEAN`。
* 空单元格默认被视为 `DOUBLE`，除非将 `empty_as_varchar` 选项设置为 `true`，在这种情况下它们被类型化为 `VARCHAR`。

如果将 `all_varchar` 选项设置为 `true`，则以上所有情况都不适用，所有单元格都被读取为 `VARCHAR`。

当没有显式指定类型时（例如，使用 `read_xlsx` 函数而不是 `COPY TO ... FROM '⟨file⟩.xlsx'`{:.language-sql .highlight}），结果列的类型将基于工作表中的第一个“数据”行进行推断，即：

* 如果没有指定显式范围
  * 如果找到或由 `header` 选项强制的标题，则第一行在标题之后
  * 如果没有找到或强制标题，则第一个非空行
* 如果指定了显式范围
  * 如果在第一行找到标题或由 `header` 选项强制，则范围的第二行
  * 如果没有找到或强制标题，则范围的第一行

如果第一个“数据行”不代表其余部分（例如，包含空单元格），这可能会导致问题，此时可以使用 `ignore_errors` 或 `empty_as_varchar` 选项来解决。

然而，当使用 `COPY TO ... FROM '⟨file⟩.xlsx'` 语法时，不会进行类型推断，结果列的类型由目标表的列类型决定。所有单元格将简单地通过将 `DOUBLE` 或 `VARCHAR` 转换为目标列类型进行转换。

## 写入 XLSX 文件

使用带有 `XLSX` 格式的 `COPY` 语句支持写入 `.xlsx` 文件。以下支持额外的参数。

| 选项            | 类型      | 默认值   | 描述                                                                          |
| ----------------- | --------- | --------- | ------------------------------------------------------------------------------------ |
| `header`          | `BOOLEAN` | `false`   | 是否将列名作为工作表中的第一行写入                      |
| `sheet`           | `VARCHAR` | `Sheet1`  | 要写入的 xlsx 文件中的工作表名称。                                     |
| `sheet_row_limit` | `INTEGER` | `1048576` | 工作表中的最大行数。如果超出此限制会抛出错误。 |

> 警告 许多工具只支持工作表最多 1,048,576 行，因此增加 `sheet_row_limit` 可能会使生成的文件无法被其他软件读取。

这些参数在 `FORMAT` 之后传递给 `COPY` 语句，例如：

```sql
CREATE TABLE test AS
    SELECT *
    FROM (VALUES (1, 2), (3, 4)) AS t(a, b);
COPY test TO 'test.xlsx' WITH (FORMAT xlsx, HEADER true);
```

### 类型转换

由于 XLSX 文件只真正支持存储数字或字符串，即 `VARCHAR` 和 `DOUBLE` 的等效类型，因此在写入 XLSX 文件时应用以下类型转换。

* 数值类型写入 XLSX 文件时会被转换为 `DOUBLE`。
* 时间类型（`TIMESTAMP`、`DATE`、`TIME` 等）会被转换为 Excel 的“序列”数字，即从 1900-01-01 开始的天数，以及时间的天部分分数。然后会应用“数字格式”样式，使其在 Excel 中显示为日期或时间。
* `TIMESTAMP_TZ` 和 `TIME_TZ` 会被转换为 UTC 的 `TIMESTAMP` 和 `TIME`，时区信息将被丢失。
* `BOOLEAN` 会被转换为 `1` 和 `0`，并应用“数字格式”使其在 Excel 中显示为 `TRUE` 和 `FALSE`。
* 所有其他类型都会被转换为 `VARCHAR`，然后作为文本单元格写入。