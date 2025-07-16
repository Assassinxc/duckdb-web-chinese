---
---
layout: docu
redirect_from:
- /docs/data/multiple_files/combining_schemas
title: 合并模式
---

<!-- markdownlint-disable MD036 -->

## 示例

读取一组CSV文件，按列位置合并列：

```sql
SELECT * FROM read_csv('flights*.csv');
```

读取一组CSV文件，按列名合并列：

```sql
SELECT * FROM read_csv('flights*.csv', union_by_name = true);
```

## 合并模式

在从多个文件中读取数据时，我们必须**合并这些文件的模式**。这是因为每个文件都有自己的模式，可能与其他文件不同。DuckDB提供了两种统一多个文件模式的方法：**按列位置**和**按列名**。

默认情况下，DuckDB读取第一个文件的模式，然后按列位置统一后续文件中的列。只要所有文件的模式相同，这种方法就能正确运行。如果文件的模式不同，您可能希望使用`union_by_name`选项，让DuckDB通过读取所有列名来构建模式。

以下是这两种方法如何工作的示例。

## 按位置合并

默认情况下，DuckDB**按列位置**统一这些不同文件的列。这意味着每个文件中的第一列会被合并，每个文件中的第二列也会被合并，依此类推。例如，考虑以下两个文件。

[`flights1.csv`](/data/flights1.csv):

```csv
FlightDate|UniqueCarrier|OriginCityName|DestCityName
1988-01-01|AA|New York, NY|Los Angeles, CA
1988-01-02|AA|New York, NY|Los Angeles, CA
```

[`flights2.csv`](/data/flights2.csv):

```csv
FlightDate|UniqueCarrier|OriginCityName|DestCityName
1988-01-03|AA|New York, NY|Los Angeles, CA
```

同时读取这两个文件将产生以下结果集：

| FlightDate | UniqueCarrier | OriginCityName |  DestCityName   |
|------------|---------------|----------------|-----------------|
| 1988-01-01 | AA            | New York, NY   | Los Angeles, CA |
| 1988-01-02 | AA            | New York, NY   | Los Angeles, CA |
| 1988-01-03 | AA            | New York, NY   | Los Angeles, CA |

这等同于SQL构造 [`UNION ALL`]({% link docs/stable/sql/query_syntax/setops.md %}#union-all)。

## 按名称合并

如果您正在处理具有不同模式的多个文件，可能是因为列被添加或重命名，那么按**列名**合并不同文件的列可能是更有利的。这可以通过提供`union_by_name`选项来实现。例如，考虑以下两个文件，其中`flights4.csv`包含一个额外的列（`UniqueCarrier`）。

[`flights3.csv`](/data/flights3.csv):

```csv
FlightDate|OriginCityName|DestCityName
1988-01-01|New York, NY|Los Angeles, CA
1988-01-02|New York, NY|Los Angeles, CA
```

[`flights4.csv`](/data/flights4.csv):

```csv
FlightDate|UniqueCarrier|OriginCityName|DestCityName
1988-01-03|AA|New York, NY|Los Angeles, CA
```

按列位置统一列名时读取这些文件会导致错误——因为这两个文件的列数不同。当指定`union_by_name`选项时，列会被正确统一，任何缺失的值将被设置为`NULL`。

```sql
SELECT * FROM read_csv(['flights3.csv', 'flights4.csv'], union_by_name = true);
```

| FlightDate | OriginCityName |  DestCityName   | UniqueCarrier |
|------------|----------------|-----------------|---------------|
| 1988-01-01 | New York, NY   | Los Angeles, CA | NULL          |
| 1988-01-02 | New York, NY   | Los Angeles, CA | NULL          |
| 1988-01-03 | New York, NY   | Los Angeles, CA | AA            |

这等同于SQL构造 [`UNION ALL BY NAME`]({% link docs/stable/sql/query_syntax/setops.md %}#union-all-by-name)。

> 使用`union_by_name`选项会增加内存消耗。