---
---
layout: docu
title: Amazon S3 表
redirect_from:
- /docs/stable/extensions/iceberg/amazon_s3_tables
- /docs/stable/extensions/iceberg/amazon_s3_tables/
---

> 对 S3 表的支持目前仍处于实验阶段。

`iceberg` 扩展支持读取存储在 [Amazon S3 表](https://aws.amazon.com/s3/features/tables/) 中的 Iceberg 表。

## 要求

安装以下扩展：

```sql
INSTALL aws;
INSTALL httpfs;
INSTALL iceberg;
```

## 连接 Amazon S3 表

您可以通过创建以下密钥，让 DuckDB 基于 `~/.aws` 目录中的默认配置文件检测您的 AWS 凭证和配置，使用 [Secrets Manager]({% link docs/stable/configuration/secrets_manager.md %})：

```sql
CREATE SECRET (
    TYPE s3,
    PROVIDER credential_chain
);
```

或者，您可以手动设置值：

```sql
CREATE SECRET (
    TYPE s3,
    KEY_ID '⟨AKIAIOSFODNN7EXAMPLE⟩',
    SECRET '⟨wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY⟩',
    REGION '⟨us-east-1⟩'
);
```

然后，使用 S3 表的 ARN（可在 AWS 管理控制台中获取）和 `ENDPOINT_TYPE s3_tables` 选项连接到目录：

```sql
ATTACH '⟨s3_tables_arn⟩' AS s3_tables (
   TYPE iceberg,
   ENDPOINT_TYPE s3_tables
);
```

要检查连接是否成功，请列出所有表：

```sql
SHOW ALL TABLES;
```

您可以按如下方式查询表：

```sql
SELECT count(*)
FROM s3_tables.⟨namespace_name⟩.⟨table_name⟩;
```