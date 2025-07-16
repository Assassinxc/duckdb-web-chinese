---
---
layout: docu
redirect_from:
- /docs/configuration
- /docs/configuration/
- /docs/sql/configuration
- /docs/sql/configuration/
- /docs/configuration/overview
title: 配置
---

DuckDB 有许多配置选项可用于更改系统的运行行为。

配置选项可以通过 [`SET` 语句]({% link docs/stable/sql/statements/set.md %}) 或 [`PRAGMA` 语句]({% link docs/stable/configuration/pragmas.md %}) 来设置。
可以通过 [`RESET` 语句]({% link docs/stable/sql/statements/set.md %}#reset) 将其重置为原始值。

可以通过 [`current_setting()` 标量函数]({% link docs/stable/sql/functions/utility.md %}) 或 [`duckdb_settings()` 表函数]({% link docs/stable/sql/meta/duckdb_table_functions.md %}#duckdb_settings) 查询配置选项的值。例如：

```sql
SELECT current_setting('memory_limit') AS memlimit;
```

或者：

```sql
SELECT value AS memlimit
FROM duckdb_settings()
WHERE name = 'memory_limit';
```

## 示例

将系统的内存限制设置为 10 GB。

```sql
SET memory_limit = '10GB';
```

配置系统使用 1 个线程。

```sql
SET threads TO 1;
```

启用在长时间查询中打印进度条。

```sql
SET enable_progress_bar = true;
```

将默认的空值顺序设置为 `NULLS LAST`。

```sql
SET default_null_order = 'nulls_last';
```

返回特定设置的当前值。

```sql
SELECT current_setting('threads') AS threads;
```

| threads |
|--------:|
| 10      |

查询特定设置。

```sql
SELECT *
FROM duckdb_settings()
WHERE name = 'threads';
```

|  name   | value |                   description                   | input_type | scope  |
|---------|-------|-------------------------------------------------|------------|--------|
| threads | 1     | 系统使用的线程总数。                            | BIGINT     | GLOBAL |

显示所有可用设置的列表。

```sql
SELECT *
FROM duckdb_settings();
```

将系统的内存限制重置为默认值。

```sql
RESET memory_limit;
```

## 密钥管理器

DuckDB 具有一个 [密钥管理器]({% link docs/stable/sql/statements/create_secret.md %})，它为所有使用密钥的后端（例如 AWS S3）提供统一的用户界面。

## 配置参考

<!-- 本节由 scripts/generate_config_docs.py 脚本生成 -->

配置选项具有不同的默认 [作用域]({% link docs/stable/sql/statements/set.md %}#scopes)：`GLOBAL` 和 `LOCAL`。以下是按作用域列出的所有可用配置选项。

### 全局配置选项

|                     Name                      |                                                                                                  Description                                                                                                  |    Type     |                    Default value                    |
|----|--------|--|---|
| `access_mode`                                 | 数据库的访问模式 (`AUTOMATIC`, `READ_ONLY` 或 `READ_WRITE`)                                                                                                                                        | `VARCHAR`   | `automatic`                                         |
| `allocator_background_threads`                | 是否启用分配器后台线程。                                                                                                                                                            | `BOOLEAN`   | `false`                                             |
| `allocator_bulk_deallocation_flush_threshold` | 如果发生大于此值的批量释放，则刷新待处理的分配。                                                                                                                                | `VARCHAR`   | `512.0 MiB`                                         |
| `allocator_flush_threshold`                   | 在完成任务后，达到峰值分配阈值时刷新分配器。                                                                                                                            | `VARCHAR`   | `128.0 MiB`                                         |
| `allow_community_extensions`                  | 允许加载社区构建的扩展                                                                                                                                                                      | `BOOLEAN`   | `true`                                              |
| `allow_extensions_metadata_mismatch`          | 允许加载元数据不兼容的扩展                                                                                                                                                         | `BOOLEAN`   | `false`                                             |
| `allow_persistent_secrets`                    | 允许创建持久密钥，这些密钥在重启时会被存储和加载                                                                                                                              | `BOOLEAN`   | `true`                                              |
| `allow_unredacted_secrets`                    | 允许打印未脱敏的密钥                                                                                                                                                                             | `BOOLEAN`   | `false`                                             |
| `allow_unsigned_extensions`                   | 允许加载签名无效或缺失的扩展                                                                                                                                                   | `BOOLEAN`   | `false`                                             |
| `allowed_directories`                         | 始终允许查询的目录/前缀列表 - 即使在 enable_external_access 为 false 时                                                                                                        | `VARCHAR[]` | `[]`                                                |
| `allowed_paths`                               | 始终允许查询的文件列表 - 即使在 enable_external_access 为 false 时                                                                                                               | `VARCHAR[]` | `[]`                                                |
| `arrow_large_buffer_size`                     | 是否使用大缓冲区导出字符串、二进制、UUID 和位的 Arrow 缓冲区                                                                                                               | `BOOLEAN`   | `false`                                             |
| `arrow_lossless_conversion`                   | 如果 DuckDB 类型在 Arrow 中没有明确的原生或规范扩展匹配，则导出类型时使用 duckdb.type_name 扩展名称。                                                           | `BOOLEAN`   | `false`                                             |
| `arrow_output_list_view`                      | 导出到 Arrow 格式时是否使用 ListView 作为 LIST 列的物理布局                                                                                                                    | `BOOLEAN`   | `false`                                             |
| `autoinstall_extension_repository`            | 覆盖扩展安装的自定义端点                                                                                                                                       | `VARCHAR`   |                                                     |
| `autoinstall_known_extensions`                | 是否允许在查询依赖时自动安装已知扩展                                                                                                               | `BOOLEAN`   | `false`                                             |
| `autoload_known_extensions`                   | 是否允许在查询依赖时自动加载已知扩展                                                                                                                  | `BOOLEAN`   | `false`                                             |
| `binary_as_string`                            | 在 Parquet 文件中，将二进制数据解释为字符串。                                                                                                                                                          | `BOOLEAN`   |                                                     |
| `ca_cert_file`                                | 自签名证书的自定义证书文件路径。                                                                                                                                               | `VARCHAR`   |                                                     |
| `catalog_error_max_schemas`                   | 系统在目录中扫描 "did you mean..." 风格错误的最大模式数                                                                                                          | `UBIGINT`   | `100`                                               |
| `checkpoint_threshold`, `wal_autocheckpoint`  | 触发检查点的 WAL 大小阈值（例如，1GB）                                                                                                                             | `VARCHAR`   | `16.0 MiB`                                          |
| `custom_extension_repository`                 | 覆盖远程扩展安装的自定义端点                                                                                                                                               | `VARCHAR`   |                                                     |
| `custom_user_agent`                           | DuckDB 调用者的元数据                                                                                                                                                                                  | `VARCHAR`   |                                                     |
| `default_block_size`                          | 新 duckdb 数据库文件的默认块大小（新创建的文件尚不存在）。                                                                                                                      | `UBIGINT`   | `262144`                                            |
| `default_collation`                           | 未指定时使用的排序设置                                                                                                                                                             | `VARCHAR`   |                                                     |
| `default_null_order`, `null_order`            | 未指定时使用的空值顺序 (`NULLS_FIRST` 或 `NULLS_LAST`)                                                                                                                                     | `VARCHAR`   | `NULLS_LAST`                                        |
| `default_order`                               | 未指定时使用的顺序类型 (`ASC` 或 `DESC`)                                                                                                                                                  | `VARCHAR`   | `ASC`                                               |
| `default_secret_storage`                      | 允许切换密钥的默认存储                                                                                                                                                              | `VARCHAR`   | `local_file`                                        |
| `disable_parquet_prefetching`                 | 禁用 Parquet 的预取机制                                                                                                                                                                  | `BOOLEAN`   | `false`                                             |
| `disabled_compression_methods`                | 禁用特定的压缩方法（逗号分隔）                                                                                                                                               | `VARCHAR`   |                                                     |
| `disabled_filesystems`                        | 禁用特定文件系统以防止访问（例如，LocalFileSystem）                                                                                                                                       | `VARCHAR`   |                                                     |
| `disabled_log_types`                          | 设置禁用的日志记录器列表                                                                                                                                                                             | `VARCHAR`   |                                                     |
| `duckdb_api`                                  | DuckDB API 表面                                                                                                                                                                                            | `VARCHAR`   | `cli`                                               |
| `enable_external_access`                      | 允许数据库访问外部状态（例如，加载/安装模块、COPY TO/FROM、CSV 读取器、pandas 替代扫描等）                                                              | `BOOLEAN`   | `true`                                              |
| `enable_external_file_cache`                  | 允许数据库在内存中缓存外部文件（例如，Parquet）。                                                                                                                                         | `BOOLEAN`   | `true`                                              |
| `enable_fsst_vectors`                         | 允许对 FSST 压缩段进行扫描，以生成压缩向量以利用延迟解压缩                                                                                                              | `BOOLEAN`   | `false`                                             |
| `enable_geoparquet_conversion`                | 如果存在空间扩展，则尝试解码/编码 GeoParquet 文件中的几何数据。                                                                                                            | `BOOLEAN`   | `true`                                              |
| `enable_http_metadata_cache`                  | 是否使用全局 HTTP 元数据缓存 HTTP 元数据                                                                                                                                        | `BOOLEAN`   | `false`                                             |
| `enable_logging`                              | 启用日志记录器                                                                                                                                                                                            | `BOOLEAN`   | `0`                                                 |
| `enable_macro_dependencies`                   | 启用创建的 MACRO 以在引用对象（如表）上创建依赖关系                                                                                                                       | `BOOLEAN`   | `false`                                             |
| `enable_object_cache`                         | [占位符] 旧设置 - 不执行任何操作                                                                                                                                                                   | `BOOLEAN`   | `NULL`                                              |
| `enable_server_cert_verification`             | 启用服务器端证书验证。                                                                                                                                                                  | `BOOLEAN`   | `false`                                             |
| `enable_view_dependencies`                    | 启用创建的 VIEW 以在引用对象（如表）上创建依赖关系                                                                                                                        | `BOOLEAN`   | `false`                                             |
| `enabled_log_types`                           | 设置启用的日志记录器列表                                                                                                                                                                              | `VARCHAR`   |                                                     |
| `extension_directory`                         | 设置存储扩展的目录                                                                                                                                                                      | `VARCHAR`   |                                                     |
| `external_threads`                            | 用于处理 DuckDB 任务的外部线程数量。                                                                                                                                                     | `UBIGINT`   | `1`                                                 |
| `force_download`                              | 强制提前下载文件                                                                                                                                                                               | `BOOLEAN`   | `false`                                             |
| `http_keep_alive`                             | 保持活动连接。将此设置为 false 可以帮助在遇到连接失败时运行                                                                                                                  | `BOOLEAN`   | `true`                                              |
| `http_proxy_password`                         | HTTP 代理的密码                                                                                                                                                                                       | `VARCHAR`   |                                                     |
| `http_proxy_username`                         | HTTP 代理的用户名                                                                                                                                                                                       | `VARCHAR`   |                                                     |
| `http_proxy`                                  | HTTP 代理主机                                                                                                                                                                                               | `VARCHAR`   |                                                     |
| `http_retries`                                | I/O 错误时的 HTTP 重试                                                                                                                                                                                     | `UBIGINT`   | `3`                                                 |
| `http_retry_backoff`                          | 指数增加重试等待时间的回退因子                                                                                                                                                   | `FLOAT`     | `4`                                                 |
| `http_retry_wait_ms`                          | 重试之间的间隔时间                                                                                                                                                                                          | `UB

（由于篇幅限制，翻译内容在此处截断。完整翻译请继续）