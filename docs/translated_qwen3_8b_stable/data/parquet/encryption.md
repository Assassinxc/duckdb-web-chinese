---
---
layout: docu
redirect_from:
- /docs/data/parquet/encryption
title: Parquet 加密
---

从 0.10.0 版本开始，DuckDB 支持读取和写入加密的 Parquet 文件。
DuckDB 广泛遵循 [Parquet 模块化加密规范](https://github.com/apache/parquet-format/blob/master/Encryption.md)，但有一些 [限制](#limitations)。

## 读取和写入加密文件

使用 `PRAGMA add_parquet_key` 函数，可以将 128、192 或 256 位的命名加密密钥添加到会话中。这些密钥存储在内存中：

```sql
PRAGMA add_parquet_key('key128', '0123456789112345');
PRAGMA add_parquet_key('key192', '012345678911234501234567');
PRAGMA add_parquet_key('key256', '01234567891123450123456789112345');
PRAGMA add_parquet_key('key256base64', 'MDEyMzQ1Njc4OTExMjM0NTAxMjM0NTY3ODkxMTIzNDU=');
```

### 写入加密的 Parquet 文件

在指定密钥（例如 `key256`）后，可以按如下方式加密文件：

```sql
COPY tbl TO 'tbl.parquet' (ENCRYPTION_CONFIG {footer_key: 'key256'});
```

### 读取加密的 Parquet 文件

使用特定密钥（例如 `key256`）加密的 Parquet 文件可以按如下方式读取：

```sql
COPY tbl FROM 'tbl.parquet' (ENCRYPTION_CONFIG {footer_key: 'key256'});
```

或者：

```sql
SELECT *
FROM read_parquet('tbl.parquet', encryption_config = {footer_key: 'key256'});
```

## 限制

DuckDB 的 Parquet 加密目前有以下限制。

1. 目前不兼容例如 PyArrow 的加密，直到缺少的细节被实现。

2. DuckDB 使用 `footer_key` 加密页脚和所有列。Parquet 规范允许使用不同的密钥对单个列进行加密，例如：

   ```sql
   COPY tbl TO 'tbl.parquet'
       (ENCRYPTION_CONFIG {
           footer_key: 'key256',
           column_keys: {key256: ['col0', 'col1']}
       });
   ```

   然而，目前不支持此功能，会抛出错误（目前）：

   ```console
   未实现错误：Parquet 加密配置 column_keys 尚未实现
   ```

## 性能影响

请注意，加密有一些性能影响。
不加密的情况下，从 [`TPC-H`]({% link docs/stable/core_extensions/tpch.md %}) 的 SF1 表（6M 行，15 列）读取/写入到 Parquet 文件分别需要 0.26 和 0.99 秒。
加密后，此操作需要 0.64 和 2.21 秒，分别比未加密版本慢约 2.5 倍。