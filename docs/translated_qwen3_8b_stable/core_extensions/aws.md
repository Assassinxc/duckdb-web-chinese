---
---
github_repository: https://github.com/duckdb/duckdb-aws
layout: docu
title: AWS 扩展
redirect_from:
- /docs/stable/extensions/aws
- /docs/stable/extensions/aws/
- /docs/extensions/aws
- /docs/extensions/aws/
---

`aws` 扩展在 `httpfs` 扩展的 [S3 功能]({% link docs/stable/core_extensions/httpfs/overview.md %}#s3-api) 基础上增加了功能（例如认证），使用 AWS SDK。

## 安装和加载

`aws` 扩展将在首次使用时从官方扩展仓库中透明地[自动加载]({% link docs/stable/core_extensions/overview.md %}#autoloading-extensions)。
如果希望手动安装和加载它，请运行：

```sql
INSTALL aws;
LOAD aws;
```

> 在大多数情况下，`aws` 扩展与 [`httpfs` 扩展]({% link docs/stable/core_extensions/httpfs/overview.md %} 配合使用。

## 配置和认证

推荐使用 [secrets]({% link docs/stable/sql/statements/create_secret.md %} 来配置和认证 AWS S3 端点。

### `config` 提供者

默认提供者 `config`（即用户配置的）允许通过手动提供密钥访问 S3 存储桶。例如：

```sql
CREATE OR REPLACE SECRET secret (
    TYPE s3,
    PROVIDER config,
    KEY_ID '⟨AKIAIOSFODNN7EXAMPLE⟩',
    SECRET '⟨wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY⟩',
    REGION '⟨us-east-1⟩'
);
```

> 提示 如果出现 IO 错误（`Connection error for HTTP HEAD`），请通过 `ENDPOINT 's3.⟨your_region⟩.amazonaws.com'`{:.language-sql .highlight} 显式配置端点。

现在，使用上述密钥查询，只需查询任何以 `s3://` 开头的文件：

```sql
SELECT *
FROM 's3://⟨your-bucket⟩/⟨your_file⟩.parquet';
```

### `credential_chain` 提供者

`credential_chain` 提供者允许通过 AWS SDK 提供的机制自动获取凭据。例如，使用 AWS SDK 默认提供者：

```sql
CREATE OR REPLACE SECRET secret (
    TYPE s3,
    PROVIDER credential_chain
);
```

同样，使用上述密钥查询文件时，只需查询任何以 `s3://` 开头的文件。

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

`credential_chain` 提供者还允许覆盖自动获取的配置。例如，要自动加载凭据，然后覆盖区域，请运行：

```sql
CREATE OR REPLACE SECRET secret (
    TYPE s3,
    PROVIDER credential_chain,
    CHAIN config,
    REGION '⟨eu-west-1⟩'
);
```

### 自动刷新

某些 AWS 端点需要定期刷新凭据。
可以通过 `REFRESH auto` 选项指定：

```sql
CREATE SECRET env_test (
    TYPE s3,
    PROVIDER credential_chain,
    REFRESH auto
);
```

## 旧功能

> 已弃用 `load_aws_credentials` 函数已弃用。

在 0.10.0 版本之前，DuckDB 没有 [Secrets manager]({% link docs/stable/sql/statements/create_secret.md %} 来自动加载凭据，AWS 扩展提供了特殊函数来在 [旧版认证方法]({% link docs/stable/core_extensions/httpfs/s3api_legacy_authentication.md %} 中加载 AWS 凭据。

| 函数 | 类型 | 描述 |
|---|---|-------|
| `load_aws_credentials` | `PRAGMA` 函数 | 通过 [AWS 默认凭据提供者链](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/credentials-chain.html) 加载 AWS 凭据 |

### 加载 AWS 凭据（旧版）

要加载 AWS 凭据，请运行：

```sql
CALL load_aws_credentials();
```

<div class="monospace_table"></div>

| loaded_access_key_id | loaded_secret_access_key | loaded_session_token | loaded_region |
|----------------------|--------------------------|----------------------|---------------|
| AKIAIOSFODNN7EXAMPLE | `<redacted>`             | NULL                 | us-east-2     |

该函数接受一个字符串参数以指定特定的配置文件：

```sql
CALL load_aws_credentials('minio-testing-2');
```

<div class="monospace_table"></div>

| loaded_access_key_id | loaded_secret_access_key | loaded_session
|----------------------|--------------------------|----------------------|---------------|
| minio_duckdb_user_2  | `<redacted>`             | NULL                 | NULL          |

调用该函数有多个参数可以调整其行为：

```sql
CALL load_aws_credentials('minio-testing-2', set_region = false, redact_secret = false);
```

<div class="monospace_table"></div>

| loaded_access_key_id | loaded_secret_access_key     | loaded_session_token | loaded_region |
|----------------------|------------------------------|----------------------|---------------|
| minio_duckdb_user_2  | minio_duckdb_user_password_2 | NULL                 | NULL          |