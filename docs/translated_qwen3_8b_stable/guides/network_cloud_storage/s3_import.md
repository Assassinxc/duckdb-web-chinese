---
---
layout: docu
redirect_from:
- /docs/guides/import/s3_import
- /docs/guides/import/s3_import/
- /docs/guides/network_cloud_storage/s3_import
title: S3 Parquet 导入
---

## 前提条件

要从 S3 导入 Parquet 文件，需要使用 [`httpfs` 扩展]({% link docs/stable/core_extensions/httpfs/overview.md %})。可以通过 `INSTALL` SQL 命令安装此扩展。只需运行一次。

```sql
INSTALL httpfs;
```

要使用 `httpfs` 扩展，使用 `LOAD` SQL 命令加载：

```sql
LOAD httpfs;
```

## 凭证和配置

加载 `httpfs` 扩展后，设置凭证和 S3 区域以读取数据：

```sql
CREATE SECRET (
    TYPE s3,
    KEY_ID '⟨AKIAIOSFODNN7EXAMPLE⟩',
    SECRET '⟨wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY⟩',
    REGION '⟨us-east-1⟩'
);
```

> 提示 如果出现 IO 错误（`Connection error for HTTP HEAD`），请通过 `ENDPOINT 's3.⟨your_region⟩.amazonaws.com'`{:.language-sql .highlight} 显式配置端点。

或者，使用 [`aws` 扩展]({% link docs/stable/core_extensions/aws.md %}) 自动获取凭证：

```sql
CREATE SECRET (
    TYPE s3,
    PROVIDER credential_chain
);
```

## 查询

在设置好 `httpfs` 扩展并正确配置 S3 后，可以使用以下命令从 S3 读取 Parquet 文件：

```sql
SELECT * FROM read_parquet('s3://⟨bucket⟩/⟨file⟩');
```

## Google Cloud Storage (GCS) 和 Cloudflare R2

DuckDB 也可以通过 S3 API 处理 [Google Cloud Storage (GCS)]({% link docs/stable/guides/network_cloud_storage/gcs_import.md %}) 和 [Cloudflare R2]({% link docs/stable/guides/network_cloud_storage/cloudflare_r2_import.md %})。
请参阅相关指南以获取详细信息。