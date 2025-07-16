---
---
layout: docu
redirect_from:
- /docs/guides/import/s3_express_one
- /docs/guides/import/s3_express_one/
- /docs/guides/network_cloud_storage/s3_express_one
title: S3 Express One
---

2023年底，AWS [宣布](https://aws.amazon.com/about-aws/whats-new/2023/11/amazon-s3-express-one-zone-storage-class/) 推出了 [S3 Express One Zone](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-express-one-zone.html)，这是传统 S3 存储桶的高速变体。
DuckDB 可以通过 [`httpfs` 扩展]({% link docs/stable/core_extensions/httpfs/overview.md %}) 读取 S3 Express One 存储桶。

## 凭据和配置

S3 Express One 存储桶的配置与 [常规 S3 存储桶]({% link docs/stable/guides/network_cloud_storage/s3_import.md %}) 相似，唯一的例外是：
我们需要根据以下模式指定端点：

```sql
s3express-⟨availability_zone⟩.⟨region⟩.amazonaws.com
```

其中 `⟨availability_zone⟩`{:.language-sql .highlight}（例如 `use-az5`）可以从 S3 Express One 存储桶的配置页面获取，`⟨region⟩`{:.language-sql .highlight} 是 AWS 区域（例如 `us-east-1`）。

例如，要允许 DuckDB 使用 S3 Express One 存储桶，请按照以下方式配置 [Secrets manager]({% link docs/stable/sql/statements/create_secret.md %})：

```sql
CREATE SECRET (
    TYPE s3,
    KEY_ID '⟨AKIAIOSFODNN7EXAMPLE⟩',
    SECRET '⟨wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY⟩',
    REGION '⟨us-east-1⟩',
    ENDPOINT 's3express-⟨use1-az5⟩.⟨us-east-1⟩.amazonaws.com'
);
```

## 实例位置

为了获得最佳性能，请确保 EC2 实例与您查询的 S3 Express One 存储桶位于同一个可用区。
要确定可用区名称与可用区 ID 之间的映射关系，请使用 `aws ec2 describe-availability-zones` 命令。

* 可用区名称到可用区 ID 映射：

  ```batch
  aws ec2 describe-availability-zones --output json \
      | jq -r '.AvailabilityZones[] | select(.ZoneName == "us-east-1f") | .ZoneId'
  ```

  ```text
  use1-az5
  ```

* 可用区 ID 到可用区名称映射：

  ```batch
  aws ec2 describe-availability-zones --output json \
      | jq -r '.AvailabilityZones[] | select(.ZoneId == "use1-az5") | .ZoneName'
  ```

  ```text
  us-east-1f
  ```

## 查询

您可以像查询其他 S3 存储桶一样查询 S3 Express One 存储桶：

```sql
SELECT *
FROM 's3://express-bucket-name--use1-az5--x-s3/my-file.parquet';
```

## 性能

我们在 `c7gd.12xlarge` 实例上运行了两个实验，使用了 [LDBC SF300 Comments `creationDate` Parquet 文件](https://blobs.duckdb.org/data/ldbc-sf300-comments-creationDate.parquet) 文件（也用于 [性能指南的微基准测试]({% link docs/stable/guides/performance/benchmarks.md %}#data-sets)）。

| 实验 | 文件大小 | 运行时间 |
|:-----|--:|--:|
| 仅从 Parquet 加载 | 4.1 GB | 3.5 s |
| 从 Parquet 创建本地表 | 4.1 GB | 5.1 s |

“仅加载”变体通过 [`EXPLAIN ANALYZE`]({% link docs/stable/guides/meta/explain_analyze.md %}) 语句运行加载，以测量运行时间而不创建本地表；而“创建本地表”变体使用 [`CREATE TABLE ... AS SELECT`]({% link docs/stable/sql/statements/create_table.md %}#create-table--as-select-ctas) 在本地磁盘上创建持久化表。