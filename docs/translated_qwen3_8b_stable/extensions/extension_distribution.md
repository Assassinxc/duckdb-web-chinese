---
---
layout: docu
title：扩展分发
---

## 平台

扩展二进制文件为多个平台提供分发（见下文）。
对于某些扩展没有可用包的平台，用户可以从源代码构建它们，并通过 [手动安装生成的二进制文件]({% link docs/stable/extensions/advanced_installation_methods.md %}#installing-an-extension-from-an-explicit-path)。

所有官方扩展都为以下平台提供分发。

| 平台名称         | 操作系统 | 架构             | CPU类型                         | 用于                     |
|------------------|----------|------------------|----------------------------------|--------------------------|
| `linux_amd64`    | Linux    | x86_64 (AMD64)   |                                  | Node.js包等              |
| `linux_arm64`    | Linux    | AArch64 (ARM64)  | AWS Graviton，Snapdragon等       | 所有包                   |
| `osx_amd64`      | macOS    | x86_64 (AMD64)   | Intel                            | 所有包                   |
| `osx_arm64`      | macOS    | AArch64 (ARM64)  | Apple Silicon M1，M2等           | 所有包                   |
| `windows_amd64`  | Windows  | x86_64 (AMD64)   | Intel，AMD等                     | 所有包                   |

一些扩展为以下平台提供分发：

* `windows_amd64_mingw`
* `wasm_eh` 和 `wasm_mvp`（参见 [DuckDB-Wasm 的扩展]({% link docs/stable/clients/wasm/extensions.md %})）

对于上述列表以外的平台，我们不正式分发扩展（例如 `linux_arm64_android`）。

## 扩展签名

### 已签名的扩展

扩展可以使用加密密钥进行签名。
默认情况下，DuckDB 使用其内置的公钥来验证加载扩展前的完整性。
所有核心和社区扩展均由 DuckDB 团队签名。

对扩展进行签名简化了它们的分发，这就是为什么它们可以通过 HTTP 而无需 HTTPS 分发，
HTTPS 本身通过一个扩展支持（[`httpfs`]({% link docs/stable/core_extensions/httpfs/overview.md %})）。

### 未签名的扩展

> 警告
> 仅从你信任的来源加载未签名的扩展。
> 避免通过 HTTP 加载未签名的扩展。
> 请参阅 [Securing DuckDB 页面]({% link docs/stable/operations_manual/securing_duckdb/securing_extensions.md %}) 获取如何以安全方式设置 DuckDB 的指南。

如果你希望加载你自己的扩展或第三方扩展，你需要启用 `allow_unsigned_extensions` 标志。
使用 [CLI 客户端]({% link docs/stable/clients/cli/overview.md %}) 加载未签名的扩展时，在启动时传递 `-unsigned` 标志：

```bash
duckdb -unsigned
```

现在可以加载任何扩展，无论是否签名：

```sql
LOAD './some/local/ext.duckdb_extension';
```

对于客户端 API，需要设置 `allow_unsigned_extensions` 数据库配置选项，详见相应的 [客户端 API 文档]({% link docs/stable/clients/overview.md %})。
例如，对于 Python 客户端，请参阅 [Python API 文档中的“加载和安装扩展”部分]({% link docs/stable/clients/python/overview.md %}#loading-and-installing-extensions)。

## 二进制兼容性

为了避免二进制兼容性问题，DuckDB 分发的二进制扩展同时绑定到特定的 DuckDB 版本和一个 [平台](#platforms)。
这意味着 DuckDB 可以自动检测它与可加载扩展之间的二进制兼容性。
当尝试加载为不同版本或平台编译的扩展时，DuckDB 会抛出错误并拒绝加载该扩展。

## 创建自定义仓库

你可以创建自定义的 DuckDB 扩展仓库。
一个 DuckDB 仓库是一个基于 HTTP、HTTPS、S3 或本地文件的目录，用于提供特定结构的扩展文件。
这种结构在 [“从 S3 直接下载扩展”部分]({% link docs/stable/extensions/advanced_installation_methods.md %}#downloading-extensions-directly-from-s3) 中描述，并且对于本地路径和远程服务器来说是相同的，例如：

```text
base_repository_path_or_url
└── v1.0.0
    └── osx_arm64
        ├── autocomplete.duckdb_extension
        ├── httpfs.duckdb_extension
        ├── icu.duckdb_extension
        ├── inet.duckdb_extension
        ├── json.duckdb_extension
        ├── parquet.duckdb_extension
        ├── tpcds.duckdb_extension
        ├── tpcds.duckdb_extension
        └── tpch.duckdb_extension
```

请查看 [`extension-template` 仓库](https://github.com/duckdb/extension-template/) 以获取设置仓库所需的所有代码和脚本。

当从自定义仓库安装扩展时，DuckDB 会同时查找压缩和未压缩的版本。例如：

```sql
INSTALL icu FROM '⟨custom_repository⟩';
```

执行此语句时，DuckDB 会首先查找 `icu.duckdb_extension.gz`，然后查找 `icu.duckdb_extension`。

如果自定义仓库通过 HTTPS 或 S3 提供服务，需要 [`httpfs` 扩展]({% link docs/stable/core_extensions/httpfs/overview.md %})。DuckDB 会在尝试通过 HTTPS 或 S3 安装时自动加载 `httpfs` 扩展。