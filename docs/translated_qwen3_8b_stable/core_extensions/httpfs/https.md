---
---
layout: docu
title: HTTP(S) 支持
redirect_from:
- /docs/extensions/httpfs/https
- /docs/extensions/httpfs/https/
- /docs/stable/extensions/httpfs/https
- /docs/stable/extensions/httpfs/https/
---

通过 `httpfs` 扩展，可以直接使用 HTTP(S) 协议查询文件。此功能适用于 DuckDB 或其各种扩展所支持的所有文件，并提供只读访问。

```sql
SELECT *
FROM 'https://domain.tld/file.extension';
```

## 部分读取

对于 CSV 文件，由于格式的行基础特性，通常会下载整个文件。
对于 Parquet 文件，DuckDB 支持 [部分读取]({% link docs/stable/data/parquet/overview.md %}#partial-reading)，即可以结合 Parquet 元数据和 [HTTP 范围请求](https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests) 只下载查询实际需要的文件部分。例如，以下查询只会读取 Parquet 元数据和 `column_a` 列的数据：

```sql
SELECT column_a
FROM 'https://domain.tld/file.parquet';
```

在某些情况下，甚至不需要读取任何实际数据，因为只需要读取元数据：

```sql
SELECT count(*)
FROM 'https://domain.tld/file.parquet';
```

## 扫描多个文件

也支持通过 HTTP(S) 扫描多个文件：

```sql
SELECT *
FROM read_parquet([
    'https://domain.tld/file1.parquet',
    'https://domain.tld/file2.parquet'
]);
```

## 认证

要对 HTTP(S) 端点进行认证，使用 [Secrets Manager]({% link docs/stable/configuration/secrets_manager.md %}) 创建一个 `HTTP` 密钥：

```sql
CREATE SECRET http_auth (
    TYPE http,
    BEARER_TOKEN '⟨token⟩'
);
```

或者：

```sql
CREATE SECRET http_auth (
    TYPE http,
    EXTRA_HTTP_HEADERS MAP {
        'Authorization': 'Bearer ⟨token⟩'
    }
);
```

## HTTP 代理

DuckDB 支持 HTTP 代理。

你可以使用 [Secrets Manager]({% link docs/stable/configuration/secrets_manager.md %}) 添加一个 HTTP 代理：

```sql
CREATE SECRET http_proxy (
    TYPE http,
    HTTP_PROXY '⟨http_proxy_url⟩',
    HTTP_PROXY_USERNAME '⟨username⟩',
    HTTP_PROXY_PASSWORD '⟨password⟩'
);
```

或者，可以通过 [配置选项]({% link docs/stable/configuration/pragmas.md %}) 添加：

```sql
SET http_proxy = '⟨http_proxy_url⟩';
SET http_proxy_username = '⟨username⟩';
SET http_proxy_password = '⟨password⟩';
```

## 使用自定义证书文件

要使用自定义证书文件与 `httpfs` 扩展配合使用，请在加载扩展之前设置以下 [配置选项]({% link docs/stable/configuration/pragmas.md %})：

```sql
LOAD httpfs;
SET ca_cert_file = '⟨certificate_file⟩';
SET enable_server_cert_verification = true;
```