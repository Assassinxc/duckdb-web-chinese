---
---
layout: docu
redirect_from:
- /docs/data/parquet
- /docs/data/parquet/
- /docs/extensions/parquet
- /docs/extensions/parquet/
- /docs/data/parquet/overview
title: 读取和写入 Parquet 文件
---

## 示例

读取单个 Parquet 文件：

```sql
SELECT * FROM 'test.parquet';
```

确定 Parquet 文件中的列/类型：

```sql
DESCRIBE SELECT * FROM 'test.parquet';
```

从 Parquet 文件创建表：

```sql
CREATE TABLE test AS
    SELECT * FROM 'test.parquet';
```

如果文件不以 `.parquet` 结尾，请使用 `read_parquet` 函数：

```sql
SELECT *
FROM read_parquet('test.parq');
```

使用列表参数读取三个 Parquet 文件，并将它们视为一个表：

```sql
SELECT *
FROM read_parquet(['file1.parquet', 'file2.parquet', 'file3.parquet']);
```

读取所有匹配通配符模式的文件：

```sql
SELECT *
FROM 'test/*.parquet';
```

读取所有匹配通配符模式的文件，并包含指定每行来源文件的 `filename` 虚拟列（自 DuckDB v1.3.0 起，该列默认可用无需配置选项）：

```sql
SELECT *, filename
FROM read_parquet('test/*.parquet');
```

使用通配符列表读取两个特定文件夹中的所有 Parquet 文件：

```sql
SELECT *
FROM read_parquet(['folder1/*.parquet', 'folder2/*.parquet']);
```

通过 HTTPS 读取：

```sql
SELECT *
FROM read_parquet('https://some.url/some_file.parquet');
```

查询 [Parquet 文件的元数据]({% link docs/stable/data/parquet/metadata.md %}#parquet-metadata)：

```sql
SELECT *
FROM parquet_metadata('test.parquet');
```

查询 [Parquet 文件的文件元数据]({% link docs/stable/data/parquet/metadata.md %}#parquet-file-metadata)：

```sql
SELECT *
FROM parquet_file_metadata('test.parquet');
```

查询 [Parquet 文件的键值元数据]({% link docs/stable/data/parquet/metadata.md %}#parquet-key-value-metadata)：

```sql
SELECT *
FROM parquet_kv_metadata('test.parquet');
```

查询 [Parquet 文件的模式]({% link docs/stable/data/parquet/metadata.md %}#parquet-schema)：

```sql
SELECT *
FROM parquet_schema('test.parquet');
```

使用默认压缩（Snappy）将查询结果写入 Parquet 文件：

```sql
COPY
    (SELECT * FROM tbl)
    TO 'result-snappy.parquet'
    (FORMAT parquet);
```

使用指定压缩和行组大小将查询结果写入 Parquet 文件：

```sql
COPY
    (FROM generate_series(100_000))
    TO 'test.parquet'
    (FORMAT parquet, COMPRESSION zstd, ROW_GROUP_SIZE 100_000);
```

将整个数据库的表内容导出为 parquet：

```sql
EXPORT DATABASE 'target_directory' (FORMAT parquet);
```

## Parquet 文件

Parquet 文件是压缩的列式文件，加载和处理效率高。DuckDB 提供了高效的读取和写入 Parquet 文件的支持，还支持将过滤器和投影推送到 Parquet 文件扫描中。

> Parquet 数据集会根据文件数量、单个文件大小、使用的压缩算法、行组大小等因素有所不同。这些因素对性能有显著影响。请参阅 [性能指南]({% link docs/stable/guides/performance/file_formats.md %}) 了解详细信息。

## `read_parquet` 函数

| 函数 | 描述 | 示例 |
|:--|:--|:-----|
| `read_parquet(path_or_list_of_paths)` | 读取 Parquet 文件 | `SELECT * FROM read_parquet('test.parquet');` |
| `parquet_scan(path_or_list_of_paths)` | `read_parquet` 的别名 | `SELECT * FROM parquet_scan('test.parquet');` |

如果文件以 `.parquet` 结尾，函数语法是可选的。系统会自动推断你正在读取 Parquet 文件：

```sql
SELECT * FROM 'test.parquet';
```

可以通过提供通配符或文件列表一次性读取多个文件。有关更多信息，请参阅 [多个文件部分]({% link docs/stable/data/multiple_files/overview.md %})。

### 参数

有多个选项可以传递给 `read_parquet` 函数或 [`COPY` 语句]({% link docs/stable/sql/statements/copy.md %})。

| 名称 | 描述 | 类型 | 默认 |
|:--|:-----|:-|:-|
| `binary_as_string` | 由旧版写入器生成的 Parquet 文件不会正确设置字符串的 `UTF8` 标志，导致字符串列被加载为 `BLOB`。将此设置为 true 可以将二进制列加载为字符串。 | `BOOL` | `false` |
| `encryption_config` | [Parquet 加密]({% link docs/stable/data/parquet/encryption.md %}) 的配置。 | `STRUCT` | - |
| `filename` | 是否在结果中包含额外的 `filename` 列。自 DuckDB v1.3.0 起，`filename` 列会自动作为虚拟列添加，此选项仅保留兼容性原因。 | `BOOL` | `false` |
| `file_row_number` | 是否包含 `file_row_number` 列。 | `BOOL` | `false` |
| `hive_partitioning` | 是否将路径解释为 [Hive 分区路径]({% link docs/stable/data/partitioning/hive_partitioning.md %})。 | `BOOL` | (自动检测) |
| `union_by_name` | 是否按名称 [统一多个模式]({% link docs/stable/data/multiple_files/combining_schemas.md %})，而不是按位置。 | `BOOL` | `false` |

## 部分读取

DuckDB 支持将投影推送到 Parquet 文件本身。也就是说，在查询 Parquet 文件时，只会读取查询所需的列。这允许你只读取感兴趣的 Parquet 文件部分。DuckDB 会自动完成此操作。

DuckDB 还支持将过滤器推送到 Parquet 读取器。当你对从 Parquet 文件扫描的列应用过滤器时，过滤器会被推送到扫描中，甚至可以使用内置的 zonemaps 跳过文件的部分内容。请注意，这取决于你的 Parquet 文件是否包含 zonemaps。

过滤器和投影推送到可提供显著的性能优势。更多信息请参见 [我们的博客文章“使用 DuckDB 精确查询 Parquet”]({% post_url 2021-06-25-querying-parquet %})。

## 插入和视图

你还可以将数据插入表中或直接从 Parquet 文件创建表。这将从 Parquet 文件加载数据并插入到数据库中：

将 Parquet 文件中的数据插入表中：

```sql
INSERT INTO people
    SELECT * FROM read_parquet('test.parquet');
```

直接从 Parquet 文件创建表：

```sql
CREATE TABLE people AS
    SELECT * FROM read_parquet('test.parquet');
```

如果你想保留 Parquet 文件中的数据，但想直接查询 Parquet 文件，可以创建一个覆盖 `read_parquet` 函数的视图。然后你可以像查询内置表一样查询 Parquet 文件：

创建一个覆盖 Parquet 文件的视图：

```sql
CREATE VIEW people AS
    SELECT * FROM read_parquet('test.parquet');
```

查询 Parquet 文件：

```sql
SELECT * FROM people;
```

## 写入 Parquet 文件

DuckDB 还支持使用 `COPY` 语句语法将数据写入 Parquet 文件。有关详细信息，请参阅 [`COPY` 语句页面]({% link docs/stable/sql/statements/copy.md %})，包括 `COPY` 语句的所有可能参数。

将查询写入 Snappy 压缩的 Parquet 文件：

```sql
COPY
    (SELECT * FROM tbl)
    TO 'result-snappy.parquet'
    (FORMAT parquet);
```

将 `tbl` 写入 zstd 压缩的 Parquet 文件：

```sql
COPY tbl
    TO 'result-zstd.parquet'
    (FORMAT parquet, COMPRESSION zstd);
```

将 `tbl` 写入 zstd 压缩的 Parquet 文件，使用最低压缩级别以获得最快压缩速度：

```sql
COPY tbl
    TO 'result-zstd.parquet'
    (FORMAT parquet, COMPRESSION zstd, COMPRESSION_LEVEL 1);
```

写入带有 [键值元数据]({% link docs/stable/data/parquet/metadata.md %}) 的 Parquet 文件：

```sql
COPY (
    SELECT
        42 AS number,
        true AS is_even
) TO 'kv_metadata.parquet' (
    FORMAT parquet,
    KV_METADATA {
        number: 'Answer to life, universe, and everything',
        is_even: 'not ''odd''' -- 值中的单引号必须转义
    }
);
```

将 CSV 文件写入未压缩的 Parquet 文件：

```sql
COPY
    'test.csv'
    TO 'result-uncompressed.parquet'
    (FORMAT parquet, COMPRESSION uncompressed);
```

将查询写入带有 zstd 压缩和行组大小的 Parquet 文件：

```sql
COPY
    (FROM generate_series(100_000))
    TO 'row-groups-zstd.parquet'
    (FORMAT parquet, COMPRESSION zstd, ROW_GROUP_SIZE 100_000);
```

将数据写入 LZ4 压缩的 Parquet 文件：

```sql
COPY
    (FROM generate_series(100_000))
    TO 'result-lz4.parquet'
    (FORMAT parquet, COMPRESSION lz4);
```

或者等效地：

```sql
COPY
    (FROM generate_series(100_000))
    TO 'result-lz4.parquet'
    (FORMAT parquet, COMPRESSION lz4_raw);
```

将数据写入 Brotli 压缩的 Parquet 文件：

```sql
COPY
    (FROM generate_series(100_000))
    TO 'result-brotli.parquet'
    (FORMAT parquet, COMPRESSION brotli);
```

要配置 Parquet 文件字典页的页面大小，请使用 `STRING_DICTIONARY_PAGE_SIZE_LIMIT` 选项（默认：1 MB）：

```sql
COPY
    lineitem
    TO 'lineitem-with-custom-dictionary-size.parquet'
    (FORMAT parquet, STRING_DICTIONARY_PAGE_SIZE_LIMIT 100_000);
```

DuckDB 的 `EXPORT` 命令可用于将整个数据库导出为一系列 Parquet 文件。有关详细信息，请参阅 [“`EXPORT` 语句”页面]({% link docs/stable/sql/statements/export.md %})：

将整个数据库的表内容导出为 Parquet：

```sql
EXPORT DATABASE 'target_directory' (FORMAT parquet);
```

## 加密

DuckDB 支持读取和写入 [加密的 Parquet 文件]({% link docs/stable/data/parquet/encryption.md %}).

## 支持的特性

支持的 Parquet 特性列表可在 [Parquet 文档的“实现状态”页面](https://parquet.apache.org/docs/file-format/implementationstatus/) 中找到。

## 安装和加载 Parquet 扩展

对 Parquet 文件的支持通过扩展启用。`parquet` 扩展几乎包含在所有客户端中。但是，如果您的客户端未捆绑 `parquet` 扩展，则必须单独安装扩展：

```sql
INSTALL parquet;
```