---
---
layout: docu
redirect_from:
- /docs/data/csv/tips
title: CSV 导入技巧
---

以下是一些在尝试导入复杂 CSV 文件时的技巧。在示例中，我们使用 [`flights.csv`](/data/flights.csv) 文件。

## 如果表头未被正确检测，请覆盖表头标志

如果文件中仅包含字符串列，`header` 自动检测可能会失败。可以通过提供 `header` 选项来覆盖此行为。

```sql
SELECT * FROM read_csv('flights.csv', header = true);
```

## 如果文件中不包含表头，请提供列名

如果文件中不包含表头，列名将默认自动生成。您可以使用 `names` 选项提供自己的列名。

```sql
SELECT * FROM read_csv('flights.csv', names = ['DateOfFlight', 'CarrierName']);
```

## 覆盖特定列的类型

`types` 标志可用于通过提供 `name` → `type` 映射的结构来覆盖特定列的类型。

```sql
SELECT * FROM read_csv('fl
```