---
---
layout: docu
title: S3 API 旧版认证方案
redirect_from:
- /docs/extensions/httpfs/s3api_legacy_authentication
- /docs/extensions/httpfs/s3api_legacy_authentication/
- /docs/stable/extensions/httpfs/s3api_legacy_authentication
- /docs/stable/extensions/httpfs/s3api_legacy_authentication/
---

在 0.10.0 版本之前，DuckDB 没有 [Secrets manager]({% link docs/stable/sql/statements/create_secret.md %})。因此，S3 端点的配置和认证是通过变量进行的。本页面文档记录了 S3 API 的旧版认证方案。

> 警告 本页面描述了一种旧版的存储密钥的方式，即通过 DuckDB 设置。
> 这会增加密钥意外泄露的风险（例如，通过打印其值）。
> 因此，应避免使用这些方法来存储密钥。
> 推荐的 S3 端点配置和认证方式是使用 [secrets]({% link docs/stable/core_extensions/httpfs/s3api.md %}#configuration-and-authentication)。

## 旧版认证方案

为了能够从 S3 读取或写入数据，应设置正确的区域：

```sql
SET s3_region = 'us-east-1';
```

可选地，如果使用的是非 AWS 的对象存储服务器，还可以配置端点：

```sql
SET s3_endpoint = '⟨domain⟩.⟨tld⟩:⟨port⟩';
```

如果端点未启用 SSL，则运行：

```sql
SET s3_use_ssl = false;
```

可以通过以下方式在 [path-style](https://docs.aws.amazon.com/AmazonS3/latest/userguide/VirtualHosting.html#path-style-access) 和 [vhost-style](https://docs.aws.amazon.com/AmazonS3/latest/userguide/VirtualHosting.html#virtual-hosted-style-access) URL 之间切换：

```sql
SET s3_url_style = 'path';
```

但请注意，这可能还需要更新端点。例如，对于 AWS S3，需要将端点更改为 `s3.⟨region⟩.amazonaws.com`{:.language-sql .highlight}。

在配置好正确的端点和区域后，可以读取公共文件。要读取私有文件，可以添加认证凭据：

```sql
SET s3_access_key_id = '⟨aws_access_key_id⟩';
SET s3_secret_access_key = '⟨aws_secret_access_key⟩';
```

或者，也支持临时 S3 凭据。它们需要设置一个额外的会话令牌：

```sql
SET s3_session_token = '⟨aws_session_token⟩';
```

[`aws` 扩展]({% link docs/stable/core_extensions/aws.md %}) 允许加载 AWS 凭据。

## 每个请求的配置

除了上述全局的 S3 配置，还可以在每个请求的基础上使用特定的配置值。这允许使用多个凭据集、区域等。这些配置值可以通过在 S3 URI 中作为查询参数来使用。上述所有单独的配置值都可以设置为查询参数。例如：

```sql
SELECT *
FROM 's3://bucket/file.parquet?s3_access_key_id=accessKey&s3_secret_access_key=secretKey';
```

每个查询也可以使用多个配置：

```sql
SELECT *
FROM 's3://bucket/file.parquet?s3_access_key_id=accessKey1&s3_secret_access_key=secretKey1' t1
INNER JOIN 's3://bucket/file.csv?s3_access_key_id=accessKey2&s3_secret_access_key=secretKey2' t2;
```

## 配置

对于 S3 上传，还有一些额外的配置选项，但默认值对于大多数使用场景来说已经足够。

此外，大多数配置选项也可以通过环境变量设置：

| DuckDB 设置         | 环境变量            | 说明                                     |
|:---------------------|:--------------------|:-----------------------------------------|
| `s3_region`          | `AWS_REGION`        | 优先于 `AWS_DEFAULT_REGION`              |
| `s3_region`          | `AWS_DEFAULT_REGION`|                                         |
| `s3_access_key_id`   | `AWS_ACCESS_KEY_ID` |                                         |
| `s3_secret_access_key`| `AWS_SECRET_ACCESS_KEY`|                                         |
| `s3_session_token`   | `AWS_SESSION_TOKEN` |                                         |
| `s3_endpoint`        | `DUCKDB_S3_ENDPOINT`|                                         |
| `s3_use_ssl`         | `DUCKDB_S3_USE_SSL` |                                         |