---
---
layout: docu
railroad: statements/export.js
redirect_from:
- /docs/sql/statements/export
title: EXPORT 和 IMPORT DATABASE 语句
---

`EXPORT DATABASE` 命令允许您将数据库内容导出到特定目录。`IMPORT DATABASE` 命令则允许您再次读取这些内容。

## 示例

将数据库导出到目标目录 'target_directory' 作为 CSV 文件：

```sql
EXPORT DATABASE 'target_directory';
```

导出到目录 'target_directory'，使用给定选项进行 CSV 序列化：

```sql
EXPORT DATABASE 'target_directory' (FORMAT csv, DELIMITER '|');
```

导出到目录 'target_directory'，表以 Parquet 格式序列化：

```sql
EXPORT DATABASE 'target_directory' (FORMAT parquet);
```

导出到目录 'target, directory'，表以 Parquet 格式序列化，使用 ZSTD 压缩，行组大小为 100,000：

```sql
EXPORT DATABASE 'target_directory' (
    FORMAT parquet,
    COMPRESSION zstd,
    ROW_GROUP_SIZE 100_000
);
```

重新加载数据库：

```sql
IMPORT DATABASE 'source_directory';
```

或者使用 `PRAGMA`：

```sql
PRAGMA import_database('source_directory');
```

有关 Parquet 文件写入的详细信息，请参阅 [数据导入部分的 Parquet 文件页面]({% link docs/stable/data/parquet/overview.md %}#writing-to-parquet-files) 和 [`COPY` 语句页面]({% link docs/stable/sql/statements/copy.md %}).

## `EXPORT DATABASE`

`EXPORT DATABASE` 命令将数据库的全部内容 – 包括模式信息、表、视图和序列 – 导出到特定目录，该目录之后可以再次加载。创建的目录结构如下：

```text
target_directory/schema.sql
target_directory/load.sql
target_directory/t_1.csv
...
target_directory/t_n.csv
```

`schema.sql` 文件包含数据库中找到的模式语句。它包含任何 `CREATE SCHEMA`、`CREATE TABLE`、`CREATE VIEW` 和 `CREATE SEQUENCE` 命令，这些命令用于重新构建数据库。

`load.sql` 文件包含一组 `COPY` 语句，可用于再次从 CSV 文件中读取数据。该文件对模式中发现的每个表都包含一个 `COPY` 语句。

### 语法

<div id="rrdiagram1"></div>

## `IMPORT DATABASE`

可以使用 `IMPORT DATABASE` 命令重新加载数据库，也可以手动运行 `schema.sql` 然后 `load.sql` 重新加载数据。

### 语法

<div id="rrdiagram2"></div>