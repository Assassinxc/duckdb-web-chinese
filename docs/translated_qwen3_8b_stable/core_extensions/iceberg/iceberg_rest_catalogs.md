---
---
layout: docu
title: Iceberg REST 目录
---

`iceberg` 扩展支持附加 Iceberg REST 目录。在附加 Iceberg REST 目录之前，必须按照 [概述]({% link docs/stable/core_extensions/iceberg/overview.md %}) 中的说明安装 `iceberg` 扩展。

如果您要附加由 Amazon 管理的 Iceberg REST 目录，请参阅附加 [Amazon S3 表]({% link docs/stable/core_extensions/iceberg/amazon_s3_tables.md %}) 或 [Amazon Sagemaker Lakehouse]({% link docs/stable/core_extensions/iceberg/amazon_sagemaker_lakehouse.md %}) 的说明。

对于所有其他 Iceberg REST 目录，您可以按照以下说明进行操作。如有关于特定目录的问题，请参阅 [示例](#specific-catalog-examples) 部分。

大多数 Iceberg REST 目录通过 OAuth2 进行身份验证。您可以使用现有的 DuckDB 密码工作流程来存储 OAuth2 服务的登录凭据。

```sql
CREATE SECRET iceberg_secret (
    TYPE ICEBERG,
    CLIENT_ID '⟨admin⟩',
    CLIENT_SECRET '⟨password⟩',
    OAUTH2_SERVER_URI '⟨http://irc_host_url.com/v1/oauth/tokens⟩'
);
```

如果您已经有 Bearer 令牌，可以直接将其传递给您的 `CREATE SECRET` 语句。

```sql
CREATE SECRET iceberg_secret (
    TYPE ICEBERG,
    TOKEN '⟨bearer_token⟩'
);
```

您可以使用以下 [`ATTACH`]({% link docs/stable/sql/statements/attach.md %}) 语句附加 Iceberg 目录。

```sql
ATTACH '⟨warehouse⟩' AS iceberg_catalog (
   TYPE iceberg,
   SECRET iceberg_secret, -- 传递特定的密钥名称以避免歧义
   ENDPOINT ⟨https://rest_endpoint.com⟩
);
```

要查看可用的表，请运行
```sql
SHOW ALL TABLES;
```

### ATTACH 选项

使用 OAuth2 授权的 REST 目录也可以仅通过 `ATTACH` 语句附加。以下是 REST 目录的完整 `ATTACH` 选项列表。

| 参数                    | 类型       | 默认值  | 描述                                                |
| ------------------------ | ---------- | -------- | ---------------------------------------------------- |
| `ENDPOINT_TYPE`          | `VARCHAR`  | `NULL`   | 用于附加 S3Tables 或 Glue 目录。允许的值为 'GLUE' 和 'S3_TABLES' |
| `ENDPOINT`               | `VARCHAR`  | `NULL`   | 与 REST 目录通信的 URL 端点。不能与 `ENDPOINT_TYPE` 一起使用 |
| `SECRET`                 | `VARCHAR`  | `NULL`   | 用于与 REST 目录通信的密钥名称 |
| `CLIENT_ID`              | `VARCHAR`  | `NULL`   | 用于密钥的 CLIENT_ID |
| `CLIENT_SECRET`          | `VARCHAR`  | `NULL`   | 密钥所需的 CLIENT_SECRET |
| `DEFAULT_REGION`         | `VARCHAR`  | `NULL`   | 与存储层通信时使用的默认区域 |
| `OAUTH2_SERVER_URI`      | `VARCHAR`  | `NULL`   | 获取 Bearer 令牌的 OAuth2 服务器 URL |
| `AUTHORIZATION_TYPE`     | `VARCHAR`  | `OAUTH2` | 传递 `SigV4` 用于需要 SigV4 授权的目录 |

以下选项只能传递给 `CREATE SECRET` 语句，并且要求 `AUTHORIZATION_TYPE` 为 `OAUTH2`

| 参数                    | 类型       | 默认值  | 描述                                                |
| ------------------------ | ---------- | -------- | ---------------------------------------------------- |
| `OAUTH2_GRANT_TYPE`      | `VARCHAR`  | `NULL` | 请求 OAuth 令牌时的授权类型 |
| `OAUTH2_SCOPE`           | `VARCHAR`  | `NULL` | 返回的 OAuth 访问令牌的请求范围 |

## 特定目录示例

### R2 目录

要附加到 [R2 cloudflare](https://developers.cloudflare.com/r2/data-catalog/) 管理的目录，请按照以下附加步骤进行操作。

```sql
CREATE SECRET r2_secret (
    TYPE ICEBERG,
    TOKEN '⟨r2_token⟩'
);
```

您可以通过 [创建 API 令牌](https://developers.cloudflare.com/r2/data-catalog/get-started/#3-create-an-api-token) 的步骤来创建令牌。

然后，使用以下命令附加目录。

```sql
ATTACH '⟨warehouse⟩' AS my_r2_catalog (
    TYPE ICEBERG,
    ENDPOINT '⟨catalog-uri⟩'
);
```

`warehouse` 和 `catalog-uri` 的变量将在所选 R2 对象存储目录（R2 对象存储 > 目录名称 > 设置）的设置中可用。

### Polaris

要附加到 [Polaris](https://polaris.apache.org) 目录，请使用以下命令。

```sql
CREATE SECRET polaris_secret (
    TYPE ICEBERG,
    CLIENT_ID '⟨admin⟩',
    CLIENT_SECRET '⟨password⟩',
);
```

```sql
ATTACH 'quickstart_catalog' as polaris_catalog (
    TYPE ICEBERG,
    ENDPOINT '⟨polaris_rest_catalog_endpoint⟩'
);
```

### Lakekeeper

要附加到 [Lakekeeper](https://docs.lakekeeper.io) 目录，请使用以下命令。

```sql
CREATE SECRET lakekeeper_secret (
    TYPE ICEBERG,
    CLIENT_ID '⟨admin⟩',
    CLIENT_SECRET '⟨password⟩',
    OAUTH2_SCOPE '⟨scope⟩',
    OAUTH2_SERVER_URI '⟨lakekeeper_oauth_url⟩'
);
```

```sql
ATTACH '⟨warehouse⟩' as lakekeeper_catalog (
    TYPE ICEBERG,
    ENDPOINT '⟨lakekeeper_irc_url⟩',
    SECRET lakekeeper_secret
);
```

## 限制

目前尚不支持从基于非 S3 或 S3Tables 的远程存储的 Iceberg REST 目录中读取数据。