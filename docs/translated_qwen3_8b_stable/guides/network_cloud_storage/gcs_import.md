---
---
layout: docu
redirect_from:
- /docs/guides/import/gcs_import
- /docs/guides/import/gcs_import/
- /docs/guides/network_cloud_storage/gcs_import
title: Google Cloud Storage 导入
---

## 先决条件

Google Cloud Storage (GCS) 可以通过 [`httpfs` 扩展]({% link docs/stable/core_extensions/httpfs/overview.md %}) 使用。
可以通过 `INSTALL httpfs` SQL 命令安装此扩展。只需运行一次即可。

## 凭据和配置

您需要创建 [HMAC 密钥](https://console.cloud.google.com/storage/settings;tab=interoperability) 并声明它们：

```sql
CREATE SECRET (
    TYPE gcs,
    KEY_ID '⟨AKIAIOSFODNN7EXAMPLE⟩',
    SECRET '⟨wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY⟩'
);
```

## 查询

在设置好 GCS 凭据后，可以使用以下命令查询 GCS 数据：

```sql
SELECT *
FROM read_parquet('gs://⟨gcs_bucket⟩/⟨file.parquet⟩');
```

## 附加到数据库

您可以以只读模式 [附加到数据库文件]({% link docs/stable/guides/network_cloud_storage/duckdb_over_https_or_s3.md %})：

```sql
LOAD httpfs;
ATTACH 'gs://⟨gcs_bucket⟩/⟨file.duckdb⟩' AS ⟨duckdb_database⟩ (READ_ONLY);
```

> Google Cloud Storage 中的数据库只能以只读模式附加。