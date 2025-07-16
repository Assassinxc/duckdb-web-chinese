---
---
layout: docu
redirect_from:
- /docs/guides/network_cloud_storage/duckdb_over_https_or_s3
title: 通过 HTTPS 或 S3 连接到 DuckDB 数据库
---

您可以通过 HTTPS 或 S3 API 建立到 DuckDB 实例的只读连接。

## 先决条件

本指南需要 [`httpfs` 扩展]({% link docs/stable/core_extensions/httpfs/overview.md %})，可以通过 `INSTALL httpfs` SQL 命令进行安装。只需运行一次即可。

## 通过 HTTPS 连接到数据库

要通过 HTTPS 连接到 DuckDB 数据库，请使用 [`ATTACH` 语句]({% link docs/stable/sql/statements/attach.md %})，如下所示：

```sql
ATTACH 'https://blobs.duckdb.org/databases/stations.duckdb' AS stations_db;
```

> 自 DuckDB 1.1 版本起，`ATTACH` 语句会创建到 HTTP 端点的只读连接。
> 在之前的版本中，需要使用 `READ_ONLY` 标志。

然后，可以使用以下语句查询数据库：

```sql
SELECT count(*) AS num_stations
FROM stations_db.stations;
```

| num_stations |
|-------------:|
| 578          |

## 通过 S3 API 连接到数据库

要通过 S3 API 连接到 DuckDB 数据库，请先[配置认证信息]({% link docs/stable/guides/network_cloud_storage/s3_import.md %}#credentials-and-configuration)（如果需要的话）。
然后，使用 [`ATTACH` 语句]({% link docs/stable/sql/statements/attach.md %})，如下所示：

```sql
ATTACH 's3://duckdb-blobs/databases/stations.duckdb' AS stations_db;
```

> 自 DuckDB 1.1 版本起，`ATTACH` 语句会创建到 HTTP 端点的只读连接。
> 在之前的版本中，需要使用 `READ_ONLY` 标志。

可以使用以下语句查询数据库：

```sql
SELECT count(*) AS num_stations
FROM stations_db.stations;
```

| num_stations |
|-------------:|
| 578          |

> 也支持连接到诸如 [Google Cloud Storage (`gs://`)]({% link docs/stable/guides/network_cloud_storage/gcs_import.md %}#attaching-to-a-database) 等 S3 兼容 API。

## 限制

* 仅允许只读连接，无法通过 HTTPS 协议或 S3 API 写入数据库。