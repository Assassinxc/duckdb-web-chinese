---
---
layout: docu
redirect_from:
- /docs/guides/import/s3_iceberg_import
- /docs/guides/import/s3_iceberg_import/
- /docs/guides/network_cloud_storage/s3_iceberg_import
selected: S3 Iceberg 导入
title: S3 Iceberg 导入
---

## 前提条件

从 S3 导入 Iceberg 文件，需要同时安装 [`httpfs`]({% link docs/stable/core_extensions/httpfs/overview.md %}) 和 [`iceberg`]({% link docs/stable/core_extensions/iceberg/overview.md %}) 扩展。它们可以通过 `INSTALL` SQL 命令进行安装。扩展只需安装一次。

```sql
INSTALL httpfs;
INSTALL iceberg;
```

要使用这些扩展，使用 `LOAD` 命令：

```sql
LOAD httpfs;
LOAD iceberg;
```

## 凭证

安装扩展后，设置凭证和 S3 区域以读取数据。您可以使用访问密钥和秘密密钥，或者使用令牌。

```sql
CREATE SECRET (
    TYPE s3,
    KEY_ID '⟨AKIAIOSFODNN7EXAMPLE⟩',
    SECRET '⟨wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY⟩',
    REGION '⟨us-east-1⟩'
);
```

或者，使用 [`aws` 扩展]({% link docs/stable/core_extensions/aws.md %}) 自动获取凭证：

```sql
CREATE SECRET (
    TYPE s3,
    PROVIDER credential_chain
);
```

## 从 S3 导入 Iceberg 表

在扩展配置完成且 S3 凭证正确设置后，可以使用以下命令从 S3 读取 Iceberg 表：

```sql
SELECT *
FROM iceberg_scan('s3://⟨bucket⟩/⟨iceberg_table_folder⟩/metadata/⟨id⟩.metadata.json');
```

请注意，您需要直接链接到清单文件。否则会报错如下：

```console
IO 错误：
无法打开文件 "s3://bucket/iceberg_table_folder/metadata/version-hint.text": 没有此文件或目录
```