---
---
layout: docu
redirect_from:
- /docs/guides/import/s3_export
- /docs/guides/import/s3_export/
- /docs/guides/network_cloud_storage/s3_export
title: S3 Parquet 导出
---

要将 Parquet 文件写入 S3，需要使用 [`httpfs` 扩展]({% link docs/stable/core_extensions/httpfs/overview.md %})。可以通过 `INSTALL` SQL 命令安装此扩展。只需运行一次即可。

```sql
INSTALL httpfs;
```

要使用 `httpfs` 扩展，使用 `LOAD` SQL 命令加载扩展：

```sql
LOAD httpfs;
```

加载 `httpfs` 扩展后，设置用于写入数据的凭据。注意，`region` 参数应与您要访问的存储桶的区域匹配。

```sql
CREATE SECRET (
    TYPE s3,
    KEY_ID '⟨AKIAIOSFODNN7EXAMPLE⟩',
    SECRET '⟨wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY⟩',
    REGION '⟨us-east-1⟩'
);
```

> 提示 如果出现 IO 错误（`Connection error for HTTP HEAD`），请通过 `ENDPOINT 's3.⟨your_region⟩.amazonaws.com'`{:.language-sql .highlight} 显式配置端点。

或者，使用 [`aws` 扩展]({% link docs/stable/core_extensions/aws.md %}) 自动获取凭据：

```sql
CREATE SECRET (
    TYPE s3,
    PROVIDER credential_chain
);
```

在 `httpfs` 扩展配置完成且 S3 凭据正确设置后，可以使用以下命令将 Parquet 文件写入 S3：

```sql
COPY ⟨table_name⟩ TO 's3://⟨s3-bucket⟩/⟨filename⟩.parquet';
```

同样，通过互操作性 API 支持 Google Cloud Storage (GCS)。
您需要创建 [HMAC 密钥](https://console.cloud.google.com/storage/settings;tab=interoperability)，并按照以下方式提供凭据：

```sql
CREATE SECRET (
    TYPE gcs,
    KEY_ID '⟨AKIAIOSFODNN7EXAMPLE⟩',
    SECRET '⟨wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY⟩'
);
```

在设置好 GCS 凭据后，可以使用以下命令进行导出：

```sql
COPY ⟨table_name⟩ TO 'gs://⟨gcs_bucket⟩/⟨filename⟩.parquet';
```