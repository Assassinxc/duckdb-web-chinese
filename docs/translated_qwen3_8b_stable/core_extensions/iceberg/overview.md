---
---
github_repository: https://github.com/duckdb/duckdb-iceberg
layout: docu
title: Iceberg 扩展
redirect_from:
- /docs/stable/extensions/iceberg
- /docs/stable/extensions/iceberg/
- /docs/stable/extensions/iceberg/overview
- /docs/stable/extensions/iceberg/overview/
- /docs/extensions/iceberg
- /docs/extensions/iceberg/
---

`iceberg` 扩展实现了对 [Apache Iceberg 开源表格式](https://iceberg.apache.org/) 的支持，并且可以连接到 Iceberg REST 目录。有关如何连接到 Iceberg REST 目录的信息，请参阅 [Iceberg REST 目录]({% link docs/stable/core_extensions/iceberg/iceberg_rest_catalogs.md %}) 页面。

## 安装和加载

要安装 `iceberg` 扩展，请运行：

```sql
INSTALL iceberg;
```

请注意，`iceberg` 扩展不是自动加载的。
因此，在使用之前，您需要加载它：

```sql
LOAD iceberg;
```

## 更新扩展

`iceberg` 扩展经常在 DuckDB 发布之间收到更新。
为了确保您拥有最新版本，请[更新您的扩展]({% link docs/stable/sql/statements/update_extensions.md %})：

```sql
UPDATE EXTENSIONS;
```

## 使用

为了测试示例，请下载 [`iceberg_data.zip`](/data/iceberg_data.zip) 文件并解压缩。

### 常用参数

| 参数                    | 类型        | 默认值                                    | 描述                                                |
| ------------------------ | ----------- | ------------------------------------------ | ---------------------------------------------------- |
| `allow_moved_paths`      | `BOOLEAN`   | `false`                                   | 允许扫描被移动的 Iceberg 表                          |
| `metadata_compression_codec` | `VARCHAR`   | `''`                                      | 将元数据文件视为设置为 `'gzip'` 时的处理方式         |
| `snapshot_from_id`       | `UBIGINT`   | `NULL`                                    | 使用特定的 `id` 访问快照                            |
| `snapshot_from_timestamp`| `TIMESTAMP` | `NULL`                                    | 使用特定的 `timestamp` 访问快照                     |
| `version`                | `VARCHAR`   | `'?'`                                     | 提供一个显式的版本字符串、提示文件或猜测             |
| `version_name_format`    | `VARCHAR`   | `'v%s%s.metadata.json,%s%s.metadata.json'` | 控制版本如何转换为元数据文件名                      |

### 查询单个表

```sql
SELECT count(*)
FROM iceberg_scan('data/iceberg/lineitem_iceberg', allow_moved_paths = true);
```

| count_star() |
|-------------:|
| 51793        |

> `allow_moved_paths` 选项确保进行了一些路径解析，
> 这允许扫描被移动的 Iceberg 表。

您还可以直接在查询中指定当前的清单，这可能在查询之前从目录中解析，例如在此示例中，清单版本是一个 UUID。
为此，请导航到 `data/iceberg` 目录并运行：

```sql
SELECT count(*)
FROM iceberg_scan('lineitem_iceberg/metadata/v1.metadata.json');
```

| count_star() |
|-------------:|
| 60175        |

`iceberg` 与 [`httpfs` 扩展]({% link docs/stable/core_extensions/httpfs/overview.md %}) 或 [`azure` 扩展]({% link docs/stable/core_extensions/azure.md %}) 一起工作，以访问 S3 或 Azure Blob 存储等对象存储中的 Iceberg 表。

```sql
SELECT count(*)
FROM iceberg_scan('s3://bucketname/lineitem_iceberg/metadata/v1.metadata.json');
```

### 访问 Iceberg 元数据

要访问 Iceberg 元数据，您可以使用 `iceberg_metadata` 函数：

```sql
SELECT *
FROM iceberg_metadata('data/iceberg/lineitem_iceberg', allow_moved_paths = true);
```

您也可以在通过 REST 目录连接的 Iceberg 表上运行 `iceberg_metadata` 函数：

```sql
SELECT *
FROM iceberg_metadata(iceberg_table);
```

<div class="monospace_table"></div>

|                             manifest_path                              | manifest_sequence_number | manifest_content | status  | content  |                                     file_path                                      | file_format | record_count |
|------------------------------------------------------------------------|--------------------------|------------------|---------|----------|------------------------------------------------------------------------------------|-------------|--------------|
| lineitem_iceberg/metadata/10eaca8a-1e1c-421e-ad6d-b232e5ee23d3-m1.avro | 2                        | DATA             | ADDED   | EXISTING | lineitem_iceberg/data/00041-414-f3c73457-bbd6-4b92-9c15-17b241171b16-00001.parquet | PARQUET     | 51793        |
| lineitem_iceberg/metadata/10eaca8a-1e1c-421e-ad6d-b232e5ee23d3-m0.avro | 2                        | DATA             | DELETED | EXISTING | lineitem_iceberg/data/00000-411-0792dcfe-4e25-4ca3-8ada-175286069a47-00001.parquet | PARQUET     | 60175        |

### 可视化快照

要可视化 Iceberg 表中的快照，请使用 `iceberg_snapshots` 函数：

```sql
SELECT *
FROM iceberg_snapshots('data/iceberg/lineitem_iceberg');
```

您也可以在通过 REST 目录连接的 Iceberg 表上运行 `iceberg_snapshots` 函数：

```sql
SELECT *
FROM iceberg_snapshots(iceberg_table);
```

<div class="monospace_table"></div>

| sequence_number |     snapshot_id     |      timestamp_ms       |                                         manifest_list                                          |
|-----------------|---------------------|-------------------------|------------------------------------------------------------------------------------------------|
| 1               | 3776207205136740581 | 2023-02-15 15:07:54.504 | lineitem_iceberg/metadata/snap-3776207205136740581-1-cf3d0be5-cf70-453d-ad8f-48fdc412e608.avro |
| 2               | 7635660646343998149 | 2023-02-15 15:08:14.73  | lineitem_iceberg/metadata/snap-7635660646343998149-1-10eaca8a-1e1c-421e-ad6d-b232e5ee23d3.avro |

### 选择元数据版本

默认情况下，`iceberg` 扩展会查找 `version-hint.text` 文件以确定要使用的正确元数据版本。可以通过显式提供版本号来覆盖此行为，方法是通过 `iceberg` 扩展函数的 `version` 参数：

```sql
SELECT *
FROM iceberg_snapshots(
    'data/iceberg/lineitem_iceberg',
    version = '1',
    allow_moved_paths = true
);
```

默认情况下，`iceberg` 函数会查找 `v{version}.metadata.json` 和 `{version}.metadata.json` 文件，或者当 `metadata_compression_codec = 'gzip'` 指定时，查找 `v{version}.gz.metadata.json` 和 `{version}.gz.metadata.json`。
其他压缩编解码器不被支持。

如果通过 `version` 参数提供任何文本文件，该文件将被打开并作为版本提示文件处理：

```sql
SELECT *
FROM iceberg_snapshots(
    'data/iceberg/lineitem_iceberg',
    version = 'version-hint.txt',
    allow_moved
```