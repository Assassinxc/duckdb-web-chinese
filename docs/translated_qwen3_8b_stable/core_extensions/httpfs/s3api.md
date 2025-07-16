---
---
layout: docu
title: S3 API 支持
redirect_from:
- /docs/extensions/httpfs/s3api
- /docs/extensions/httpfs/s3api/
- /docs/stable/extensions/httpfs/s3api
- /docs/stable/extensions/httpfs/s3api/
---

`httpfs` 扩展支持通过 S3 API 读取/写入/[globbing](#globbing) 对象存储服务器上的文件。S3 提供了标准 API 来读取和写入远程文件（而早期的常规 http 服务器并未提供统一的写入 API）。DuckDB 遵循 S3 API，该 API 现在在行业存储提供商中广泛使用。

## 平台

`httpfs` 文件系统已与 [AWS S3](https://aws.amazon.com/s3/), [Minio](https://min.io/), [Google Cloud](https://cloud.google.com/storage/docs/interoperability), 和 [lakeFS](https://docs.lakefs.io/integrations/duckdb.html) 进行了测试。其他实现 S3 API 的服务（如 [Cloudflare R2](https://www.cloudflare.com/en-gb/developer-platform/r2/)）也应该可以使用，但可能不支持所有功能。

以下表格显示了每个 `httpfs` 功能所需的 S3 API 部分。

| 功能 | 所需的 S3 API 功能 |
|:---|:---|
| 公开文件读取 | HTTP 范围请求 |
| 私有文件读取 | 密钥或会话令牌认证 |
| 文件 glob | [ListObjectsV2](https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListObjectsV2.html) |
| 文件写入 | [分段上传](https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html) |

## 配置和认证

推荐使用 [secrets]({% link docs/stable/sql/statements/create_secret.md %}) 来配置和认证 S3 端点。多种秘密提供者可用。

要从 [弃用的 S3 API]({% link docs/stable/core_extensions/httpfs/s3api_legacy_authentication.md %}) 迁移，使用带有配置文件的定义秘密。
请参阅 [“基于配置文件加载秘密”部分](#loading-a-secret-based-on-a-profile)。

### `config` 提供者

默认提供者 `config`（即用户配置），允许手动提供密钥访问 S3 存储桶。例如：

```sql
CREATE OR REPLACE SECRET secret (
    TYPE s3,
    PROVIDER config,
    KEY_ID '⟨AKIAIOSFODNN7EXAMPLE⟩',
    SECRET '⟨wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY⟩',
    REGION '⟨us-east-1⟩'
);
```

> 提示 如果您遇到 IO 错误（`Connection error for HTTP HEAD`），请通过 `ENDPOINT 's3.⟨your_region⟩.amazonaws.com'`{:.language-sql .highlight} 显式配置端点。

现在，使用上述秘密查询，只需查询任何 `s3://` 前缀的文件：

```sql
SELECT *
FROM 's3://⟨your-bucket⟩/⟨your_file⟩.parquet';
```

### `credential_chain` 提供者

`credential_chain` 提供者允许使用 AWS SDK 提供的机制自动获取凭证。例如，使用 AWS SDK 默认提供者：

```sql
CREATE OR REPLACE SECRET secret (
    TYPE s3,
    PROVIDER credential_chain
);
```

同样，使用上述秘密查询文件，只需查询任何 `s3://` 前缀的文件。

DuckDB 还允许使用 `CHAIN` 关键字指定特定的链。这接受一个分号分隔的列表（`a;b;c`），按顺序尝试这些提供者。例如：

```sql
CREATE OR REPLACE SECRET secret (
    TYPE s3,
    PROVIDER credential_chain,
    CHAIN 'env;config'
);
```

`CHAIN` 的可能值如下：

* [`config`](https://sdk.amazonaws.com/cpp/api/LATEST/aws-cpp-sdk-core/html/class_aws_1_1_auth_1_1_profile_config_file_a_w_s_credentials_provider.html)
* [`sts`](https://sdk.amazonaws.com/cpp/api/LATEST/aws-cpp-sdk-core/html/class_aws_1_1_auth_1_1_s_t_s_assume_role_web_identity_credentials_provider.html)
* [`sso`](https://aws.amazon.com/what-is/sso/)
* [`env`](https://sdk.amazonaws.com/cpp/api/LATEST/aws-cpp-sdk-core/html/class_aws_1_1_auth_1_1_environment_a_w_s_credentials_provider.html)
* [`instance`](https://sdk.amazonaws.com/cpp/api/LATEST/aws-cpp-sdk-core/html/class_aws_1_1_auth_1_1_instance_profile_credentials_provider.html)
* [`process`](https://sdk.amazonaws.com/cpp/api/LATEST/aws-cpp-sdk-core/html/class_aws_1_1_auth_1_1_process_credentials_provider.html)

`credential_chain` 提供者还可以覆盖自动获取的配置。例如，要自动加载凭证，然后覆盖区域，运行：

```sql
CREATE OR REPLACE SECRET secret (
    TYPE s3,
    PROVIDER credential_chain,
    CHAIN config,
    REGION '⟨eu-west-1⟩'
);
```

#### 基于配置文件加载秘密

要加载基于未定义为默认的配置文件的凭证（来自 `AWS_PROFILE` 环境变量或 AWS SDK 优先级的默认配置文件），运行：

```sql
CREATE OR REPLACE SECRET secret (
    TYPE s3,
    PROVIDER credential_chain,
    CHAIN config,
    PROFILE '⟨my_profile⟩'
);
```

这种方法等同于 [弃用的 S3 API]({% link docs/stable/core_extensions/httpfs/s3api_legacy_authentication.md %}) 的方法 `load_aws_credentials('⟨my_profile⟩')`。

### S3 密钥参数概览

下面是可用于 `config` 和 `credential_chain` 提供者的支持参数完整列表：

| 名称                          | 描述                                                                           | 密钥            | 类型      | 默认值                                     |
|:------------------------------|:----------------------------------------------------------------------------------|:------------------|:----------|:--------------------------------------------|
| `ENDPOINT`                    | 指定自定义的 S3 端点                                                          | `S3`, `GCS`, `R2` | `STRING`  | `s3.amazonaws.com` 对于 `S3`,                |
| `KEY_ID`                      | 要使用的密钥 ID                                                              | `S3`, `GCS`, `R2` | `STRING`  | -                                           |
| `REGION`                      | 用于认证的区域（应与查询的存储桶的区域匹配）                                 | `S3`, `GCS`, `R2` | `STRING`  | `us-east-1`                                 |
| `SECRET`                      | 要使用的密钥的密钥                                                           | `S3`, `GCS`, `R2` | `STRING`  | -                                           |
| `SESSION_TOKEN`               | 可选，可以传递会话令牌以使用临时凭证                                           | `S3`, `GCS`, `R2` | `STRING`  | -                                           |
| `URL_COMPATIBILITY_MODE`      | 在 URL 包含有问题的字符时可以提供帮助                                         | `S3`, `GCS`, `R2` | `BOOLEAN` | `true`                                      |
| `URL_STYLE`                   | `vhost` 或 `path`                                                              | `S3`, `GCS`, `R2` | `STRING`  | `vhost` 对于 `S3`, `path` 对于 `R2` 和 `GCS` |
| `USE_SSL`                     | 是否使用 HTTPS 或 HTTP                                                        | `S3`, `GCS`, `R2` | `BOOLEAN` | `true`                                      |
| `ACCOUNT_ID`                  | 用于生成端点 URL 的 R2 账户 ID                                                | `R2`              | `STRING`  | -                                           |
| `KMS_KEY_ID`                  | AWS KMS（密钥管理服务）密钥用于 S3 的服务器端加密                             | `S3`              | `STRING`  | -                                           |

### 平台特定的秘密类型

#### S3 密钥

`httpfs` 扩展支持使用 `KMS_KEY_ID` 选项通过 [AWS Key Management Service (KMS) 在 S3 上的服务器端加密](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html)：

```sql
CREATE OR REPLACE SECRET secret (
    TYPE s3,
    PROVIDER credential_chain,
    CHAIN config,
    REGION '⟨eu-west-1⟩',
    KMS_KEY_ID 'arn:aws:kms:⟨region⟩:⟨account_id⟩:⟨key⟩/⟨key_id⟩',
    SCOPE 's3://⟨bucket-sub-path⟩'
);
```

#### R2 密钥

虽然 [Cloudflare R2](https://www.cloudflare.com/developer-platform/r2) 使用常规的 S3 API，DuckDB 有一个特殊的 Secret 类型 `R2` 以简化配置：

```sql
CREATE OR REPLACE SECRET secret (
    TYPE r2,
    KEY_ID '⟨AKIAIOSFODNN7EXAMPLE⟩',
    SECRET '⟨wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY⟩',
    ACCOUNT_ID '⟨my_account_id⟩'
);
```

请注意添加了 `ACCOUNT_ID`，它用于为您生成正确的端点 URL。此外，`R2` 密钥也可以使用 `CONFIG` 和 `credential_chain` 提供者。然而，由于 DuckDB 内部使用 AWS 客户端，当使用 `credential_chain` 时，客户端将在标准的 AWS 凭证位置（环境变量、凭证文件等）中查找 AWS 凭证。因此，您的 R2 凭证必须作为 AWS 环境变量（`AWS_ACCESS_KEY_ID` 和 `AWS_SECRET_ACCESS_KEY`）提供，以便凭证链正常工作。最后，`R2` 密钥仅在使用以 `r2://` 开头的 URL 时可用，例如：

```sql
SELECT *
FROM read_parquet('r2://⟨some-file-that-uses-an-r2-secret⟩.parquet');
```

#### GCS 密钥

虽然 [Google Cloud Storage](https://cloud.google.com/storage) 通过 S3 API 由 DuckDB 访问，DuckDB 有一个特殊的 Secret 类型 `GCS` 来简化配置：

```sql
CREATE OR REPLACE SECRET secret (
    TYPE gcs,
    KEY_ID '⟨my_hmac_access_id⟩',
    SECRET '⟨my_hmac_secret_key⟩'
);
```

**重要**：`KEY_ID` 和 `SECRET` 值必须是为 Google Cloud Storage 兼容性生成的 HMAC 密钥。这些与常规的 GCP 服务账户密钥或访问令牌不同。您可以按照 [Google Cloud 文档管理 HMAC 密钥](https://cloud.google.com/storage/docs/authentication/managing-hmackeys) 创建 HMAC 密钥。

请注意，上述密钥将自动配置正确的 Google Cloud Storage 端点。此外，`GCS` 密钥也可以使用 `CONFIG` 和 `credential_chain` 提供者。然而，由于 DuckDB 内部使用 AWS 客户端，当使用 `credential_chain` 时，客户端将在标准的 AWS 凭证位置（环境变量、凭证文件等）中查找 AWS 凭证。因此，您的 GCS HMAC 密钥必须作为 AWS 环境变量（`AWS_ACCESS_KEY_ID` 和 `AWS_SECRET_ACCESS_KEY`）提供，以便凭证链正常工作。最后，`GCS` 密钥仅在使用以 `gcs://` 或 `gs://` 开头的 URL 时可用，例如：

```sql
SELECT *
FROM read_parquet('gcs://⟨some/file/that/uses/a/gcs/secret⟩.parquet');
```

## 读取

从 S3 读取文件现在就像这样简单：

```sql
SELECT *
FROM 's3://⟨your-bucket⟩/⟨filename⟩.⟨extension⟩';
```

### 部分读取

`httpfs` 扩展支持从 S3 存储桶进行 [部分读取]({% link docs/stable/core_extensions/httpfs/https.md %}#partial-reading)。

### 读取多个文件

也可以读取多个文件，例如：

```sql
SELECT *
FROM read_parquet([
    's3://⟨your-bucket⟩/⟨filename-1⟩.parquet',
    's3://⟨your-bucket⟩/⟨filename-2⟩.parquet'
]);
```

### Globbing

文件 [globbing]({% link docs/stable/sql/functions/pattern_matching.md %}#globbing) 使用 ListObjectsV2 API 调用实现，并允许使用文件系统类似的 glob 模式匹配多个文件，例如：

```sql
SELECT *
FROM read_parquet('s3://⟨your-bucket⟩/*.parquet');
```

此查询匹配存储桶根目录中所有以 [Parquet 扩展]({% link docs/stable/data/parquet/overview.md %}) 结尾的文件。

支持多种匹配功能，例如 `*` 可以匹配任意数量的任意字符，`?` 用于匹配任意单个字符或 `[0-9]` 用于匹配字符范围中的单个字符：

```sql
SELECT count(*) FROM read_parquet('s3://⟨your-bucket⟩/folder*/100?/t[0-9].parquet');
```

在使用 glob 时，一个有用的功能是 `filename` 选项，它会添加一个名为 `filename` 的列，记录每一行的原始文件：

```sql
SELECT *
FROM read_parquet('s3://⟨your-bucket⟩/*.parquet', filename = true);
```

这可能会导致以下结果：

| column_a | column_b | filename |
|:---|:---|:---|
| 1 | examplevalue1 | s3://bucket-name/file1.parquet |
| 2 | examplevalue1 | s3://bucket-name/file2.parquet |

### Hive 分区

DuckDB 还支持 [Hive 分区方案]({% link docs/stable/data/partitioning/hive_partitioning.md %})，当使用 HTTP(S) 和 S3 端点时可用。

## 写入

写入 S3 使用分段上传 API。这使 DuckDB 能够高速可靠地上传文件。写入 S3 对 CSV 和 Parquet 都有效：

```sql
COPY table_name TO 's3://⟨your-bucket⟩/⟨filename⟩.⟨extension⟩';
```

分片写入 S3 也有效：

```sql
COPY table TO 's3://⟨your-bucket⟩/partitioned' (
    FORMAT parquet,
    PARTITION_BY (⟨part_col_a⟩, ⟨part_col_b⟩)
);
```

会自动检查现有文件/目录，目前非常保守（在 S3 上会增加一点延迟）。要禁用此检查并强制写入，添加 `OVERWRITE_OR_IGNORE` 标志：

```sql
COPY table TO 's3://⟨your-bucket⟩/partitioned' (
    FORMAT parquet,
    PARTITION_BY (⟨part_col_a⟩, ⟨part_col_b⟩),
    OVERWRITE_OR_IGNORE true
);
```

写入的文件命名方案如下：

```sql
s3://⟨your-bucket⟩/partitioned/part_col_a=⟨val⟩/part_col_b=⟨val⟩/data_⟨thread_number⟩.parquet
```

### 配置

S3 上传还有一些额外的配置选项，但默认值对于大多数使用情况已经足够。

| 名称 | 描述 |
|:---|:---|
| `s3_uploader_max_parts_per_file` | 用于分片大小计算，详见 [AWS 文档](https://docs.aws.amazon.com/AmazonS3/latest/userguide/qfacts.html) |
| `s3_uploader_max_filesize` | 用于分片大小计算，详见 [AWS 文档](https://docs.aws.amazon.com/AmazonS3/latest/userguide/qfacts.html) |
| `s3_uploader_thread_limit` | 最大上传线程数 |