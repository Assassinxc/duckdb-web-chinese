---
---
layout: docu
redirect_from:
  - /docs/configuration/secrets_manager
title: 密钥管理器
---

**密钥管理器**为所有使用密钥的后端提供统一的用户界面。密钥可以被作用域限定，因此不同的存储前缀可以拥有不同的密钥，例如允许在一个查询中跨组织合并数据。密钥也可以被持久化存储，这样在每次启动DuckDB时就无需每次都指定。

> 警告 持久化密钥以未加密的二进制格式存储在磁盘上。

## 密钥类型

密钥是有类型的，其类型标识了该密钥对应的服务。
大多数密钥并不包含在DuckDB默认配置中，而是由扩展注册。
目前，以下密钥类型是可用的：

| 密钥类型   | 服务 / 协议   | 扩展                                                                         |
| ------------- | -------------------- | --------------------------------------------------------------------------------- |
| `azure`       | Azure Blob Storage   | [`azure`]({% link docs/stable/core_extensions/azure.md %})                        |
| `ducklake`    | DuckLake             | [`ducklake`](https://ducklake.select/docs/stable/duckdb/usage/connecting#secrets) |
| `gcs`         | Google Cloud Storage | [`httpfs`]({% link docs/stable/core_extensions/httpfs/s3api.md %})                |
| `http`        | HTTP and HTTPS       | [`httpfs`]({% link docs/stable/core_extensions/httpfs/https.md %})                |
| `huggingface` | Hugging Face         | [`httpfs`]({% link docs/stable/core_extensions/httpfs/hugging_face.md %})         |
| `mysql`       | MySQL                | [`mysql`]({% link docs/stable/core_extensions/mysql.md %})                        |
| `postgres`    | PostgreSQL           | [`postgres`]({% link docs/stable/core_extensions/postgres.md %})                  |
| `r2`          | Cloudflare R2        | [`httpfs`]({% link docs/stable/core_extensions/httpfs/s3api.md %})                |
| `s3`          | AWS S3               | [`httpfs`]({% link docs/stable/core_extensions/httpfs/s3api.md %})                |

对于每种类型，都有一个或多个“密钥提供者”来指定密钥是如何创建的。密钥还可以有一个可选的作用域，该作用域是一个密钥适用的文件路径前缀。在根据路径获取密钥时，密钥的作用域将与路径进行比较，返回与路径匹配的密钥。在存在多个匹配密钥时，会选择最长的前缀。

## 创建密钥

可以使用 [`CREATE SECRET` SQL语句]({% link docs/stable/sql/statements/create_secret.md %}) 创建密钥。
密钥可以是 **临时** 或 **持久化**。默认情况下使用临时密钥，它们在DuckDB实例的生命周期内存储在内存中，类似于以前的设置方式。持久化密钥以 **未加密的二进制格式** 存储在 `~/.duckdb/stored_secrets` 目录中。在DuckDB启动时，会从该目录读取持久化密钥并自动加载。

### 密钥提供者

为了创建一个密钥，需要使用一个 **密钥提供者**。密钥提供者是生成密钥的机制。为了说明这一点，对于 `S3`、`GCS`、`R2` 和 `AZURE` 密钥类型，DuckDB目前支持两种提供者：`CONFIG` 和 `credential_chain`。`CONFIG` 提供者要求用户将所有配置信息传递给 `CREATE SECRET`，而 `credential_chain` 提供者将自动尝试获取凭据。如果没有指定密钥提供者，默认使用 `CONFIG` 提供者。如需了解如何使用不同提供者创建密钥，请查看 [httpfs]({% link docs/stable/core_extensions/httpfs/overview.md %}#configuration-and-authentication-using-secrets) 和 [azure]({% link docs/stable/core_extensions/azure.md %}#authentication-with-secret) 页面的相关信息。

### 临时密钥

要创建一个临时未作用域的密钥以访问S3，我们现在可以使用以下语句：

```sql
CREATE SECRET my_secret (
    TYPE s3,
    KEY_ID 'my_secret_key',
    SECRET 'my_secret_value',
    REGION 'my_region'
);
```

请注意，这里隐式使用了默认的 `CONFIG` 密钥提供者。

### 持久化密钥

为了在DuckDB数据库实例之间持久化密钥，我们现在可以使用 `CREATE PERSISTENT SECRET` 命令，例如：

```sql
CREATE PERSISTENT SECRET my_persistent_secret (
    TYPE s3,
    KEY_ID 'my_secret_key',
    SECRET 'my_secret_value'
);
```

默认情况下，这将把密钥（未加密）写入 `~/.duckdb/stored_secrets` 目录。要更改密钥目录，请执行：

```sql
SET secret_directory = 'path/to/my_secrets_dir';
```

请注意，设置 `home_directory` 配置选项的值不会影响密钥的位置。

## 删除密钥

可以使用 [`DROP SECRET` 语句]({% link docs/stable/sql/statements/create_secret.md %}#syntax-for-drop-secret) 删除密钥，例如：

```sql
DROP PERSISTENT SECRET my_persistent_secret;
```

## 为同一服务类型创建多个密钥

如果存在两个相同服务类型的密钥，可以使用作用域来决定使用哪一个。例如：

```sql
CREATE SECRET secret1 (
    TYPE s3,
    KEY_ID 'my_secret_key1',
    SECRET 'my_secret_value1',
    SCOPE 's3://⟨my-bucket⟩'
);
```

```sql
CREATE SECRET secret2 (
    TYPE s3,
    KEY_ID 'my_secret_key2',
    SECRET 'my_secret_value2',
    SCOPE 's3://⟨my-other-bucket⟩'
);
```

现在，如果用户查询 `s3://⟨my-other-bucket⟩/something` 的内容，系统会自动选择 `secret2` 作为该请求的密钥。要查看使用了哪个密钥，可以使用 `which_secret` 标量函数，它接受一个路径和一个密钥类型作为参数：

```sql
FROM which_secret('s3://⟨my-other-bucket⟩/file.parquet', 's3');
```

## 列出密钥

可以使用内置的生成表函数列出密钥，例如使用 [`duckdb_secrets()` 表函数]({% link docs/stable/sql/meta/duckdb_table_functions.md %}#duckdb_secrets)：

```sql
FROM duckdb_secrets();
```

敏感信息将被屏蔽。