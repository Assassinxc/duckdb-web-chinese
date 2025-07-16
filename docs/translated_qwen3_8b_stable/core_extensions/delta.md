---
---
github_repository: https://github.com/duckdb/duckdb-delta
layout: docu
title: Delta 扩展
redirect_from:
- /docs/stable/extensions/delta
- /docs/stable/extensions/delta/
- /docs/extensions/delta
- /docs/extensions/delta/
---

`delta` 扩展为 [Delta Lake 开源存储格式](https://delta.io/) 提供了支持。它使用 [Delta Kernel](https://github.com/delta-incubator/delta-kernel-rs) 构建。该扩展为 Delta 表（本地和远程）提供 **读取支持**。

有关实现细节，请参阅 [公告博客文章]({% post_url 2024-06-10-delta %}).

> 警告 `delta` 扩展目前处于实验阶段，且仅支持 [特定平台](#supported-duckdb-versions-and-platforms)。

## 安装和加载

`delta` 扩展将在首次使用时从官方扩展仓库中透明地 [自动加载]({% link docs/stable/core_extensions/overview.md %}#autoloading-extensions)。
如果你想手动安装和加载它，请运行：

```sql
INSTALL delta;
LOAD delta;
```

## 使用

要扫描本地 Delta 表，请运行：

```sql
SELECT *
FROM delta_scan('file:///some/path/on/local/machine');
```

### 从 S3 存储桶读取

要扫描位于 [S3 存储桶]({% link docs/stable/core_extensions/httpfs/s3api.md %}) 中的 Delta 表，请运行：

```sql
SELECT *
FROM delta_scan('s3://some/delta/table');
```

对于 S3 存储桶的认证，DuckDB 支持 [Secrets]({% link docs/stable/configuration/secrets_manager.md %})：

```sql
CREATE SECRET (
    TYPE s3,
    PROVIDER credential_chain
);
SELECT *
FROM delta_scan('s3://some/delta/table/with/auth');
```

要扫描 S3 上的公共存储桶，你可能需要通过创建包含你的公共 S3 存储桶区域的 secret 来传递正确的区域：

```sql
CREATE SECRET (
    TYPE s3,
    REGION 'my-region'
);
SELECT *
FROM delta_scan('s3://some/public/table/in/my-region');
```

### 从 Azure Blob 存储读取

要扫描位于 [Azure Blob 存储桶]({% link docs/stable/core_extensions/azure.md %}#azure-blob-storage) 中的 Delta 表，请运行：

```sql
SELECT *
FROM delta_scan('az://my-container/my-table');
```

对于 Azure Blob 存储的认证，DuckDB 支持 [Secrets]({% link docs/stable/configuration/secrets_manager.md %})：

```sql
CREATE SECRET (
    TYPE azure,
    PROVIDER credential_chain
);
SELECT *
FROM delta_scan('az://my-container/my-table-with-auth');
```

## 功能

虽然 `delta` 扩展仍处于实验阶段，但许多（扫描）功能和优化已经支持：

* 多线程扫描和 Parquet 元数据读取
* 数据跳过/过滤下推
    * 基于 Parquet 元数据跳过文件中的行组
    * 基于 Delta 分区信息跳过整个文件
* 投影下推
* 扫描带有删除向量的表
* 所有原始类型
* 结构体
* 带 secrets 的 S3 支持

未来将发布更多优化。

## 支持的 DuckDB 版本和平台

`delta` 扩展要求 DuckDB 版本 0.10.3 或更高版本。

目前 `delta` 扩展仅支持以下平台：

* Linux AMD64（x86_64 和 ARM64）：`linux_amd64` 和 `linux_arm64`
* macOS Intel 和 Apple Silicon：`osx_amd64` 和 `osx_arm64`
* Windows AMD64：`windows_amd64`

对 [其他 DuckDB 平台]({% link docs/stable/extensions/extension_distribution.md %}#platforms) 的支持正在开发中。