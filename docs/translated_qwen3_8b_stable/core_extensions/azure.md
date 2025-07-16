---
---
github_repository: https://github.com/duckdb/duckdb-azure
layout: docu
title: Azure 扩展
redirect_from:
- /docs/stable/extensions/azure
- /docs/stable/extensions/azure/
- /docs/extensions/azure
- /docs/extensions/azure/
---

`azure` 扩展是一个可加载扩展，它为 [Azure Blob 存储](https://azure.microsoft.com/en-us/products/storage/blobs) 在 DuckDB 中添加了一个文件系统抽象。

## 安装与加载

`azure` 扩展会在首次使用时从官方扩展仓库中透明地[自动加载]({% link docs/stable/core_extensions/overview.md %}#autoloading-extensions)。
如果您希望手动安装和加载它，请运行：

```sql
INSTALL azure;
LOAD azure;
```

## 使用

一旦[认证](#authentication)设置完成，您可以按照以下方式查询 Azure 存储：

### Azure Blob 存储

允许的 URI 方案：`az` 或 `azure`

```sql
SELECT count(*)
FROM 'az://⟨my_container⟩/⟨path⟩/⟨my_file⟩.⟨parquet_or_csv⟩';
```

也支持通配符：

```sql
SELECT *
FROM 'az://⟨my_container⟩/⟨path⟩/*.csv';
```

```sql
SELECT *
FROM 'az://⟨my_container⟩/⟨path⟩/**';
```

或者使用完整的路径语法：

```sql
SELECT count(*)
FROM 'az://⟨my_storage_account⟩.blob.core.windows.net/⟨my_container⟩/⟨path⟩/⟨my_file⟩.⟨parquet_or_csv⟩';
```

```sql
SELECT *
FROM 'az://⟨my_storage_account⟩.blob.core.windows.net/⟨my_container⟩/⟨path⟩/*.csv';
```

### Azure Data Lake 存储 (ADLS)

允许的 URI 方案：`abfss`

```sql
SELECT count(*)
FROM 'abfss://⟨my_filesystem⟩/⟨path⟩/⟨my_file⟩.⟨parquet_or_csv⟩';
```

也支持通配符：

```sql
SELECT *
FROM 'abfss://⟨my_filesystem⟩/⟨path⟩/*.csv';
```

```sql
SELECT *
FROM 'abfss://⟨my_filesystem⟩/⟨path⟩/**';
```

或者使用完整的路径语法：

```sql
SELECT count(*)
FROM 'abfss://⟨my_storage_account⟩.dfs.core.windows.net/⟨my_filesystem⟩/⟨path⟩/⟨my_file⟩.⟨parquet_or_csv⟩';
```

```sql
SELECT *
FROM 'abfss://⟨my_storage_account⟩.dfs.core.windows.net/⟨my_filesystem⟩/⟨path⟩/*.csv';
```

## 配置

使用以下[配置选项]({% link docs/stable/configuration/overview.md %})来配置扩展如何读取远程文件：

| 名称 | 描述 | 类型 | 默认 |
|:---|:---|:---|:---|
| `azure_http_stats` | 在 [`EXPLAIN ANALYZE` 语句]({% link docs/stable/dev/profiling.md %}) 中包含 Azure 存储的 HTTP 信息。 | `BOOLEAN` | `false` |
| `azure_read_transfer_concurrency` | Azure 客户端用于单次并行读取的最大线程数。如果 `azure_read_transfer_chunk_size` 小于 `azure_read_buffer_size`，则设置此值大于 1 将允许 Azure 客户端进行并发请求以填充缓冲区。 | `BIGINT` | `5` |
| `azure_read_transfer_chunk_size` | Azure 客户端在单个请求中读取的最大字节数。建议此值是 `azure_read_buffer_size` 的倍数。 | `BIGINT` | `1024*1024` |
| `azure_read_buffer_size` | 读取缓冲区的大小。建议此值能被 `azure_read_transfer_chunk_size` 整除。 | `UBIGINT` | `1024*1024` |
| `azure_transport_option_type` | Azure SDK 中使用的底层[适配器](https://github.com/Azure/azure-sdk-for-cpp/blob/main/doc/HttpTransportAdapter.md)。有效值为：`default` 或 `curl`。 | `VARCHAR` | `default` |
| `azure_context_caching` | 启用或禁用在 DuckDB 连接上下文中缓存 Azure SDK 的 HTTP 连接。如果您怀疑这会导致某些副作用，可以通过将其设置为 false 来禁用（不推荐）。 | `BOOLEAN` | `true` |

> 显式设置 `azure_transport_option_type` 为 `curl` 将产生以下效果：
> * 在 Linux 系统中，这可能解决证书问题（`Error: Invalid Error: Fail to get a new connection for: https://storage_account_name.blob.core.windows.net/. Problem with the SSL CA cert (path? access rights?)`），因为当指定扩展时，会尝试在多个路径中查找证书捆绑包（*curl* 默认不会这样做，且可能由于静态链接而错误）。
> * 在 Windows 系统中，这会替换默认适配器（*WinHTTP*），允许您使用所有 *curl* 功能（例如使用 socks 代理）。
> * 在所有操作系统中，它将尊重以下环境变量：
>   * `CURL_CA_INFO`：指向 PEM 编码文件的路径，其中包含发送到 libcurl 的证书颁发机构。请注意，此选项仅在 Linux 上已知有效，如果在其他平台上设置可能会抛出错误。
>   * `CURL_CA_PATH`：指向包含 PEM 编码文件的目录的路径，其中包含发送到 libcurl 的证书颁发机构。

示例：

```sql
SET azure_http_stats = false;
SET azure_read_transfer_concurrency = 5;
SET azure_read_transfer_chunk_size = 1_048_576;
SET azure_read_buffer_size = 1_048_576;
```

## 认证

Azure 扩展有两种方式配置认证。推荐的方式是使用密钥。

### 使用密钥认证

Azure 扩展支持多种[密钥提供者]({% link docs/stable/configuration/secrets_manager.md %}#secret-providers)：

* 如果需要为不同的存储账户定义不同的密钥，请使用 [`SCOPE` 配置]({% link docs/stable/configuration/secrets_manager.md %}#creating-multiple-secrets-for-the-same-service-type)。请注意，`SCOPE` 需要一个尾随斜杠（`SCOPE 'azure://some_container/'`）。
* 如果使用完整路径，则 `ACCOUNT_NAME` 属性是可选的。

#### `CONFIG` 提供者

默认提供者 `CONFIG`（即用户配置），允许使用连接字符串或匿名方式访问存储账户。例如：

```sql
CREATE SECRET secret1 (
    TYPE azure,
    CONNECTION_STRING '⟨value⟩'
);
```

如果不使用认证，您仍然需要指定存储账户名称。例如：

```sql
CREATE SECRET secret2 (
    TYPE azure,
    PROVIDER config,
    ACCOUNT_NAME '⟨storage_account_name⟩'
);
```

默认的 `PROVIDER` 是 `CONFIG`。

#### `credential_chain` 提供者

`credential_chain` 提供者允许通过 Azure SDK 自动获取的凭证连接。默认使用 `DefaultAzureCredential` 链，该链会按照 [Azure 文档](https://learn.microsoft.com/en-us/javascript/api/@azure/identity/defaultazurecredential?view=azure-node-latest#@azure-identity-defaultazurecredential-constructor) 中指定的顺序尝试凭证。例如：

```sql
CREATE SECRET secret3 (
    TYPE azure,
    PROVIDER credential_chain,
    ACCOUNT_NAME '⟨storage_account_name⟩'
);
```

DuckDB 还允许通过 `CHAIN` 关键字指定特定的链。此关键字接受以分号分隔的列表（`a;b;c`），表示按顺序尝试的提供者。例如：

```sql
CREATE SECRET secret4 (
    TYPE azure,
    PROVIDER credential_chain,
    CHAIN 'cli;env',
    ACCOUNT_NAME '⟨storage_account_name⟩'
);
```

可能的值如下：
[`cli`](https://learn.microsoft.com/en-us/cli/azure/authenticate-azure-cli);
[`managed_identity`](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview);
[`env`](https://github.com/Azure/azure-sdk-for-cpp/blob/azure-identity_1.6.0/sdk/identity/azure-identity/README.md#environment-variables);
[`default`](https://github.com/Azure/azure-sdk-for-cpp/blob/azure-identity_1.6.0/sdk/identity/azure-identity/README.md#defaultazurecredential);

如果没有显式指定 `CHAIN`，默认值将是 [`default`](https://github.com/Azure/azure-sdk-for-cpp/blob/azure-identity_1.6.0/sdk/identity/azure-identity/README.md#defaultazurecredential)

#### `SERVICE_PRINCIPAL` 提供者

`SERVICE_PRINCIPAL` 提供者允许使用 [Azure 服务主体 (SPN)](https://learn.microsoft.com/en-us/entra/architecture/service-accounts-principal) 连接。

使用密钥：

```sql
CREATE SECRET azure_spn (
    TYPE azure,
    PROVIDER service_principal,
    TENANT_ID '⟨tenant_id⟩',
    CLIENT_ID '⟨client_id⟩',
    CLIENT_SECRET '⟨client_secret⟩',
    ACCOUNT_NAME '⟨storage_account_name⟩'
);
```

使用证书：

```sql
CREATE SECRET azure_spn_cert (
    TYPE azure,
    PROVIDER service_principal,
    TENANT_ID '⟨tenant_id⟩',
    CLIENT_ID '⟨client_id⟩',
    CLIENT_CERTIFICATE_PATH '⟨client_cert_path⟩',
    ACCOUNT_NAME '⟨storage_account_name⟩'
);
```

#### 配置代理

在使用密钥时，可以通过在密钥定义中添加 `HTTP_PROXY`、`PROXY_USER_NAME` 和 `PROXY_PASSWORD` 来配置代理信息。例如：

```sql
CREATE SECRET secret5 (
    TYPE azure,
    CONNECTION_STRING '⟨value⟩',
    HTTP_PROXY 'http://localhost:3128',
    PROXY_USER_NAME 'john',
    PROXY_PASSWORD 'doe'
);
```

> * 使用密钥时，`HTTP_PROXY` 环境变量仍会被尊重，除非您显式提供该值。
> * 使用密钥时，*使用变量进行认证* 会话中的 `SET` 变量将被忽略。
> * 使用 Azure `credential_chain` 提供者时，实际的令牌在查询时获取，而不是在密钥创建时获取。

### 使用变量进行认证（已弃用）

```sql
SET variable_name = variable_value;
```

其中 `variable_name` 可以是以下之一：

| 名称 | 描述 | 类型 | 默认 |
|:---|:---|:---|:---|
| `azure_storage_connection_string` | Azure 连接字符串，用于认证和配置 Azure 请求。 | `STRING` | - |
| `azure_account_name` | Azure 账户名称，设置后扩展将尝试自动检测凭证（如果提供了连接字符串，则不使用）。 | `STRING` | - |
| `azure_endpoint` | 覆盖 Azure 端点，用于当使用 Azure 凭证提供者时。 | `STRING` | `blob.core.windows.net` |
| `azure_credential_chain`| Azure 凭证提供者的有序列表，以分号分隔的字符串格式。例如：`'cli;managed_identity;env'`。请参阅 [`credential_chain` 提供者部分](#credential_chain-provider) 中的可能值列表。如果提供了连接字符串则不使用。 | `STRING` | - |
| `azure_http_proxy` | 登录和向 Azure 发送请求时使用的代理。 | `STRING` | `HTTP_PROXY` 环境变量（如果设置）。 |
| `azure_proxy_user_name` | HTTP 代理的用户名（如需）。 | `STRING` | - |
| `azure_proxy_password` | HTTP 代理的密码（如需）。 | `STRING` | - |

## 其他信息

### 日志

Azure 扩展依赖 Azure SDK 连接到 Azure Blob 存储，并支持将 SDK 日志打印到控制台。
要控制日志级别，请设置 [`AZURE_LOG_LEVEL`](https://github.com/Azure/azure-sdk-for-cpp/blob/main/sdk/core/azure-core/README.md#sdk-log-messages) 环境变量。

例如，在 Python 中启用详细日志如下：

```python
import os
import duckdb

os.environ["AZURE_LOG_LEVEL"] = "verbose"

duckdb.sql("CREATE SECRET myaccount (TYPE azure, PROVIDER credential_chain, SCOPE 'az://myaccount.blob.core.windows.net/')")
duckdb.sql("SELECT count(*) FROM 'az://myaccount.blob.core.windows.net/path/to/blob.parquet'")
```

### ADLS 与 Blob 存储之间的区别

尽管 ADLS 实现了与 Blob 存储类似的功能，但在使用 ADLS 端点进行通配符匹配时，有一些重要的性能优势，特别是当使用（复杂）通配符模式时。

为了说明这一点，我们来看一个示例，展示如何使用 Blob 和 ADLS 端点分别执行通配符匹配。

使用以下文件系统：

```text
root
├── l_receipmonth=1997-10
│   ├── l_shipmode=AIR
│   │   └── data_0.csv
│   ├── l_shipmode=SHIP
│   │   └── data_0.csv
│   └── l_shipmode=TRUCK
│       └── data_0.csv
├── l_receipmonth=1997-11
│   ├── l_shipmode=AIR
│   │   └── data_0.csv
│   ├── l_ship
│   │   └── data_0.csv
│   └── l_shipmode=TRUCK
│       └── data_0.csv
└── l_receipmonth=1997-12
    ├── l_shipmode=AIR
    │   └── data_0.csv
    ├── l_shipmode=SHIP
    │   └── data_0.csv
    └── l_shipmode=TRUCK
        └── data_0.csv
```

通过 Blob 端点执行以下查询：

```sql
SELECT count(*)
FROM 'az://root/l_receipmonth=1997-*/l_shipmode=SHIP/*.csv';
```

它将执行以下步骤：

* 列出所有以 `root/l_receipmonth=1997-` 为前缀的文件
    * `root/l_receipmonth=1997-10/l_shipmode=SHIP/data_0.csv`
    * `root/l_receipmonth=1997-10/l_shipmode=AIR/data_0.csv`
    * `root/l_receipmonth=1997-10/l_shipmode=TRUCK/data_0.csv`
    * `root/l_receipmonth=1997-11/l_shipmode=SHIP/data_0.csv`
    * `root/l_receipmonth=1997-11/l_shipmode=AIR/data_0.csv`
    * `root/l_receipmonth=1997-11/l_shipmode=TRUCK/data_0.csv`
    * `root/l_receipmonth=1997-12/l_shipmode=SHIP/data_0.csv`
    * `root/l_receipmonth=1997-12/l_shipmode=AIR/data_0.csv`
    * `root/l_receipmonth=1997-12/l_shipmode=TRUCK/data_0.csv`
* 过滤出符合请求模式 `root/l_receipmonth=1997-*/l_shipmode=SHIP/*.csv` 的结果
    * `root/l_receipmonth=1997-10/l_shipmode=SHIP/data_0.csv`
    * `root/l_receipmonth=1997-11/l_shipmode=SHIP/data_0.csv`
    * `root/l_receipmonth=1997-12/l_shipmode=SHIP/data_0.csv`

与此同时，通过 datalake 端点执行相同的查询如下：

```sql
SELECT count(*)
FROM 'abfss://root/l_receipmonth=1997-*/l_shipmode=SHIP/*.csv';
```

这将执行以下步骤：

* 列出 `root/` 下的所有目录
    * `root/l_receipmonth=1997-10`
    * `root/l_receipmonth=1997-11`
    * `root/l_receipmonth=1997-12`
* 过滤并列出子目录：`root/l_receipmonth=1997-10`、`root/l_receipmonth=1997-11`、`root/l_receipmonth=1997-12`
    * `root/l_receipmonth=1997-10/l_shipmode=SHIP`
    * `root/l_receipmonth=1997-10/l_shipmode=AIR`
    * `root/l_receipmonth=1997-10/l_shipmode=TRUCK`
    * `root/l_receipmonth=1997-11/l_shipmode=SHIP`
    * `root/l_receipmonth=1997-11/l_shipmode=AIR`
    * `root/l_receipmonth=1997-11/l_shipmode=TRUCK`
    * `root/l_receipmonth=1997-12/l_shipmode=SHIP`
    * `root/l_receipmonth=1997-12/l_shipmode=AIR`
    * `root/l_receipmonth=1997-12/l_shipmode=TRUCK`
* 过滤并列出子目录：`root/l_receipmonth=1997-10/l_shipmode=SHIP`、`root/l_receipmonth=1997-11/l_shipmode=SHIP`、`root/l_receipmonth=1997-12/l_shipmode=SHIP`
    * `root/l_receipmonth=1997-10/l_shipmode=SHIP/data_0.csv`
    * `root/l_receipmonth=1997-11/l_shipmode=SHIP/data_0.csv`
    * `root/l_receipmonth=1997-12/l_shipmode=SHIP/data_0.csv`

如您所见，由于 Blob 端点不支持目录的概念，因此只能在列表之后进行过滤，而 ADLS 端点会递归列出文件。特别是在分区/目录数量较多的情况下，性能差异可能非常显著。