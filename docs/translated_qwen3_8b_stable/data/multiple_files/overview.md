---
---
layout: docu
redirect_from:
- /docs/data/csv/multiple_files
- /docs/data/csv/multiple_files/
- /docs/data/multiple_files/overview
title: 读取多个文件
---

DuckDB 可以同时读取多种类型的多个文件（CSV、Parquet、JSON 文件），使用 glob 语法或提供要读取的文件列表即可。
查看 [组合模式]({% link docs/stable/data/multiple_files/combining_schemas.md %}) 页面，了解如何读取具有不同模式的文件的技巧。

## CSV

读取 `dir` 文件夹中所有以 `.csv` 结尾的文件：

```sql
SELECT *
FROM 'dir/*.csv';
```

读取所有以 `.csv` 结尾的文件，且嵌套两层目录：

```sql
SELECT *
FROM '*/*/*.csv';
```

读取所有以 `.csv` 结尾的文件，且在 `dir` 文件夹中任意深度：

```sql
SELECT *
FROM 'dir/**/*.csv';
```

读取 CSV 文件 `flights1.csv` 和 `flights2.csv`：

```sql
SELECT *
FROM read_csv(['flights1.csv', 'flights2.csv']);
```

读取 CSV 文件 `flights1.csv` 和 `flights2.csv`，通过名称统一模式并输出一个 `filename` 列：

```sql
SELECT *
FROM read_csv(['flights1.csv', 'flights2.csv'], union_by_name = true, filename = true);
```

## Parquet

读取所有匹配 glob 模式的文件：

```sql
SELECT *
FROM 'test/*.parquet';
```

读取三个 Parquet 文件并将其视为一个表：

```sql
SELECT *
FROM read_parquet(['file1.parquet', 'file2.parquet', 'file3.parquet']);
```

读取两个特定文件夹中的所有 Parquet 文件：

```sql
SELECT *
FROM read_parquet(['folder1/*.parquet', 'folder2/*.parquet']);
```

读取所有匹配 glob 模式的 Parquet 文件，无论深度如何：

```sql
SELECT *
FROM read_parquet('dir/**/*.parquet');
```

## 多文件读取与 glob

DuckDB 也可以读取一系列 Parquet 文件并将其视为一个表。请注意，这仅在 Parquet 文件具有相同模式时才有效。您可以使用列表参数、glob 模式匹配语法，或两者的组合来指定要读取的 Parquet 文件。

### 列表参数

`read_parquet` 函数可以接受一个文件名列表作为输入参数。

读取三个 Parquet 文件并将其视为一个表：

```sql
SELECT *
FROM read_parquet(['file1.parquet', 'file2.parquet', 'file3.parquet']);
```

### glob 语法

传递给 `read_parquet` 函数的任何文件名输入可以是精确的文件名，也可以使用 glob 语法来读取符合模式的多个文件。

| 通配符  |                        描述                        |
|------------|-----------------------------------------------------------|
| `*`        | 匹配任意数量的任意字符（包括无字符）     |
| `**`       | 匹配任意数量的子目录（包括无子目录）     |
| `?`        | 匹配任意单个字符                              |
| `[abc]`    | 匹配括号中给出的任意一个字符                |
| `[a-z]`    | 匹配括号中给出的范围内的任意一个字符 |

请注意，由于 HTTP 编码问题，glob 中的 `?` 通配符在从 S3 读取时不受支持。

以下示例读取位于 `test` 文件夹中所有以 `.parquet` 结尾的文件：

读取所有匹配 glob 模式的文件：

```sql
SELECT *
FROM read_parquet('test/*.parquet');
```

### glob 列表

可以将 glob 语法和列表输入参数结合使用，以扫描符合多个模式之一的文件。

读取两个特定文件夹中的所有 Parquet 文件。

```sql
SELECT *
FROM read_parquet(['folder1/*.parquet', 'folder2/*.parquet']);
```

DuckDB 可以使用 glob 语法或提供要读取的文件列表，同时读取多个 CSV 文件。

## 文件名

`filename` 参数可用于在结果中添加一个额外的 `filename` 列，以指示哪一行来自哪个文件。例如：

```sql
SELECT *
FROM read_csv(['flights1.csv', 'flights2.csv'], union_by_name = true, filename = true);
```

| FlightDate | OriginCityName |  DestCityName   | UniqueCarrier |   filename   |
|------------|----------------|-----------------|---------------|--------------|
| 1988-01-01 | New York, NY   | Los Angeles, CA | NULL          | flights1.csv |
| 1988-01-02 | New York, NY   | Los Angeles, CA | NULL          | flights1.csv |
| 1988-01-03 | New York, NY   | Los Angeles, CA | AA            | flights2.csv |

## 使用 glob 函数查找文件名

glob 模式匹配语法也可以用于通过 `glob` 表函数搜索文件名。
它接受一个参数：要搜索的路径（可能包含 glob 模式）。

搜索当前目录下的所有文件。

```sql
SELECT *
FROM glob('*');
```

|     file      |
|---------------|
| test.csv      |
| test.json     |
| test.parquet  |
| test2.csv     |
| test2.parquet |
| todos.json    |