---
---
layout: docu
redirect_from:
- /docs/data/parquet/metadata
title: 查询 Parquet 元数据
---

## Parquet 元数据

`parquet_metadata` 函数可用于查询 Parquet 文件中包含的元数据，这揭示了 Parquet 文件的各种内部细节，例如不同列的统计信息。这在确定 Parquet 文件中可以跳过的数据类型，甚至快速了解各列内容方面非常有用：

```sql
SELECT *
FROM parquet_metadata('test.parquet');
```

以下是 `parquet_metadata` 返回的列表。

<div class="monospace_table"></div>

| 字段                   | 类型            |
| ----------------------- | --------------- |
| file_name               | VARCHAR         |
| row_group_id            | BIGINT          |
| row_group_num_rows      | BIGNT          |
| row_group_num_columns   | BIGINT          |
| row_group_bytes         | BIGINT          |
| column_id               | BIGINT          |
| file_offset             | BIGINT          |
| num_values              | BIGINT          |
| path_in_schema          | VARCHAR         |
| type                    | VARCHAR         |
| stats_min               | VARCHAR         |
| stats_max               | VARCHAR         |
| stats_null_count        | BIGINT          |
| stats_distinct_count    | BIGINT          |
| stats_min_value         | VARCHAR         |
| stats_max_value         | VARCHAR         |
| compression             | VARCHAR         |
| encodings               | VARCHAR         |
| index_page_offset       | BIGINT          |
| dictionary_page_offset  | BIGINT          |
| data_page_offset        | BIGINT          |
| total_compressed_size   | BIGINT          |
| total_uncompressed_size | BIGINT          |
| key_value_metadata      | MAP(BLOB, BLOB) |
| bloom_filter_offset     | BIGINT          |
| bloom_filter_length     | BIGINT          |

## Parquet 架构

`parquet_schema` 函数可用于查询 Parquet 文件中包含的内部架构。请注意，这是 Parquet 文件元数据中包含的架构。如果您想了解 Parquet 文件中包含的列名和类型，使用 `DESCRIBE` 更容易。

获取列名和列类型：

```sql
DESCRIBE SELECT * FROM 'test.parquet';
```

获取 Parquet 文件的内部架构：

```sql
SELECT *
FROM parquet_schema('test.parquet');
```

以下是 `parquet_schema` 返回的列表。

<div class="monospace_table"></div>

| 字段           | 类型    |
| --------------- | ------- |
| file_name       | VARCHAR |
| name            | VARCHAR |
| type            | VARCHAR |
| type_length     | VARCHAR |
| repetition_type | VARCHAR |
| num_children    | BIGINT  |
| converted_type  | VARCHAR |
| scale           | BIGINT  |
| precision       | BIGINT  |
| field_id        | BIGINT  |
| logical_type    | VARCHAR |

## Parquet 文件元数据

`parquet_file_metadata` 函数可用于查询文件级别的元数据，例如格式版本和使用的加密算法：

```sql
SELECT *
FROM parquet_file_metadata('test.parquet');
```

以下是 `parquet_file_metadata` 返回的列表。

<div class="monospace_table"></div>

| 字段                       | 类型    |
| ----------------------------| ------- |
| file_name                   | VARCHAR |
| created_by                  | VARCHAR |
| num_rows                    | BIGINT  |
| num_row_groups              | BIGINT  |
| format_version              | BIGINT  |
| encryption_algorithm        | VARCHAR |
| footer_signing_key_metadata | VARCHAR |

## Parquet 键值元数据

`parquet_kv_metadata` 函数可用于查询作为键值对定义的自定义元数据：

```sql
SELECT *
FROM parquet_kv_metadata('test.parquet');
```

以下是 `parquet_kv_metadata` 返回的列表。

<div class="monospace_table"></div>

| 字段     | 类型    |
| --------- | ------- |
| file_name | VARCHAR |
| key       | BLOB    |
| value     | BLOB    |

## Bloom 过滤器

DuckDB 支持使用 Bloom 过滤器来剪枝需要读取以回答高度选择性查询的行组。
目前，Bloom 过滤器支持以下类型：

* 整数类型：`TINYINT`, `UTINYINT`, `SMALLINT`, `USMALLINT`, `INTEGER`, `UINTEGER`, `BIGINT`, `UBIGINT`
* 浮点类型：`FLOAT`, `DOUBLE`
* `VARCHAR`
* `BLOB`

`parquet_bloom_probe(filename, column_name, value)` 函数可用于使用 Bloom 过滤器筛选特定列特定值时，哪些行组可以被排除。
例如：

```sql
FROM parquet_bloom_probe('my_file.parquet', 'my_col', 500);
```

|   file_name     | row_group_id | bloom_filter_excludes |
|-----------------|-------------:|----------------------:|
| my_file.parquet | 0            | true                  |
| ...             | ...          | ...                   |
| my_file.parquet | 9            | false                 |