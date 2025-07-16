---
---
layout: docu
redirect_from:
- /docs/guides/import/cloudflare_r2_import
- /docs/guides/import/cloudflare_r2_import/
- /docs/guides/network_cloud_storage/cloudflare_r2_import
title: Cloudflare R2 导入
---

## 先决条件

对于 Cloudflare R2，[S3 兼容性 API](https://developers.cloudflare.com/r2/api/s3/api/) 允许您使用 DuckDB 的 S3 支持从 R2 存储桶读取和写入数据。

这需要使用 [`httpfs` 扩展]({% link docs/stable/core_extensions/httpfs/overview.md %})，可以通过 `INSTALL` SQL 命令进行安装。此操作只需运行一次。

## 凭据和配置

您需要[生成 S3 认证令牌](https://developers.cloudflare.com/r2/api/s3/tokens/)，并在 DuckDB 中创建一个 `R2` 秘密：

```sql
CREATE SECRET (
    TYPE r2,
    KEY_ID '⟨AKIAIOSFODNN7EXAMPLE⟩',
    SECRET '⟨wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY⟩',
    ACCOUNT_ID '⟨your-33-character-hexadecimal-account-ID⟩'
);
```

## 查询

在设置好 R2 凭据后，您可以使用 DuckDB 的内置方法查询 R2 数据，例如 `read_csv` 或 `read_parquet`：

```sql
SELECT * FROM read_parquet('r2://⟨r2-bucket-name⟩/⟨file⟩');
```