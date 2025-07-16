---
---
layout: docu
title: Amazon SageMaker Lakehouse (AWS Glue)
redirect_from:
- /docs/stable/extensions/iceberg/amazon_sagemaker_lakehouse
- /docs/stable/extensions/iceberg/amazon_sagemaker_lakehouse/
---

> 目前对 Amazon SageMaker Lakehouse (AWS Glue) 的支持仍处于实验阶段。

`iceberg` 扩展支持通过 [Amazon SageMaker Lakehouse（即 AWS Glue）](https://aws.amazon.com/sagemaker/lakehouse/) 目录读取 Iceberg 表。请按照 [安装和加载]({% link docs/stable/core_extensions/iceberg/overview.md %}) 中的步骤安装 Iceberg 扩展。

## 连接到 Amazon SageMaker Lakehouse

使用 [Secrets Manager]({% link docs/stable/configuration/secrets_manager.md %}) 配置您的角色、区域和凭证提供者（或显式凭证）：

```sql
CREATE SECRET (
    TYPE s3,
    PROVIDER credential_chain,
    CHAIN sts,
    ASSUME_ROLE_ARN 'arn:aws:iam::⟨account_id⟩:role/⟨role⟩',
    REGION 'us-east-2'
);
```

然后，使用 `ENDPOINT_TYPE glue` 选项连接到目录：

```sql
ATTACH '⟨account_id⟩:s3tablescatalog/⟨namespace_name⟩' AS glue_catalog (
    TYPE iceberg,
    ENDNOTYPE glue
);
```

要检查连接是否成功，请列出所有表：

```sql
SHOW ALL TABLES;
```

您可以按以下方式查询表：

```sql
SELECT count(*)
FROM glue_catalog.⟨namespace_name⟩.⟨table_name⟩;
```