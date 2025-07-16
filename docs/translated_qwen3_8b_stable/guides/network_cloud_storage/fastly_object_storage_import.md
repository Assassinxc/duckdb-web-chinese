---
---
layout: docu
redirect_from:
- /docs/guides/import/fastly_object_storage_import
- /docs/guides/network_cloud_storage/fastly_object_storage_import
title: Fastly 对象存储导入
---

## 前提条件

对于 Fastly 对象存储，[S3 兼容性 API](https://docs.fastly.com/products/object-storage) 允许您使用 DuckDB 的 S3 支持来读取和写入 Fastly 存储桶。

这需要 [`httpfs` 扩展]({% link docs/stable/core_extensions/httpfs/overview.md %})，可以通过 `INSTALL` SQL 命令进行安装。这只需要运行一次。

## 凭据和配置

您需要 [生成一个 S3 认证令牌](https://docs.fastly.com/en/guides/working-with-object-storage#creating-an-object-storage-access-key)，并在 DuckDB 中创建一个 `S3` 秘密：

```sql
CREATE SECRET my_secret (
    TYPE s3,
    KEY_ID '⟨AKIAIOSFODNN7EXAMPLE⟩',
    SECRET '⟨wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY⟩',
    URL_STYLE 'path',
    REGION '⟨us-east⟩',
    ENDPOINT '⟨us-east⟩.object.fastlystorage.app' -- 请参阅下方说明
);
```

* `ENDPOINT` 需要指向您要使用的 [Fastly 区域的端点](https://docs.fastly.com/en/guides/working-with-object-storage#working-with-the-s3-compatible-api)（例如 `eu-central.object.fast3lystorage.app`）。
* `REGION` 必须使用 `ENDPOINT` 中提到的相同区域。
* `URL_STYLE` 需要使用 `path`。

## 查询

在设置好 Fastly 对象存储凭据后，您可以使用 DuckDB 的内置方法（如 `read_csv` 或 `read_parquet`）查询该数据：

```sql
SELECT * FROM 's3://⟨fastly-bucket-name⟩/(file).csv';
SELECT * FROM read_parquet('s3://⟨fastly-bucket-name⟩/⟨file⟩.parquet');
```