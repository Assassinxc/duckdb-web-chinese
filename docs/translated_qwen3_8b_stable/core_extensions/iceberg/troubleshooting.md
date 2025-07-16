---
---
layout: docu
title: 故障排除
redirect_from:
- /docs/stable/extensions/iceberg/troubleshooting
- /docs/stable/extensions/iceberg/troubleshooting/
---

## 局限性

* 目前不支持写入 Iceberg 表。
* 读取带有删除操作的表尚未支持。

## Curl 请求失败

### 问题

尝试连接到 Iceberg REST 目录端点时，DuckDB 返回以下错误：

```console
IO 错误：
Curl 请求到 '/v1/oauth/tokens' 失败，错误为：'URL 使用了不良/非法格式或缺少 URL'
```

### 解决方案

确保您已安装最新版本的 Iceberg 扩展：

```bash
duckdb
```

```plsql
FORCE INSTALL iceberg FROM core_nightly;
```

退出 DuckDB 并启动一个新的会话：

```bash
duckdb
```

```plsql
LOAD iceberg;
```

## HTTP 错误 403

### 问题

尝试在远程连接目录中列出表时，DuckDB 返回以下错误：

```sql
SHOW ALL TABLES;
```

```console
查询 https://s3tables.us-east-2.amazonaws.com/iceberg/v1/arn:aws:s3tables:... 失败，抛出 HTTP 错误 403。
消息：{"message":"请求中包含的安全令牌无效。"}
```

### 解决方案

使用 `duckdb_secrets()` 函数检查 DuckDB 是否已加载所需的凭据：

```sql
.mode line
FROM duckdb_secrets();
```

如果您未看到您的凭据，请手动设置以下秘密：

```sql
CREATE SECRET (
    TYPE s3,
    KEY_ID '⟨AKIAIOSFODNN7EXAMPLE⟩',
    SECRET '⟨wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY⟩',
    REGION '⟨us-east-1⟩'
);
```