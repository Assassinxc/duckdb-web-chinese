---
---
layout: docu
redirect_from:
- /docs/api/wasm/extensions
- /docs/api/wasm/extensions/
- /docs/clients/wasm/extensions
title: 扩展
---

DuckDB-Wasm（动态）扩展加载机制与常规 DuckDB 的扩展加载机制类似，但因平台差异而存在一些相关区别。

## 格式

DuckDB 中的扩展是通过 `dlopen` 动态加载的二进制文件。一个密码学签名被附加到该二进制文件中。
DuckDB-Wasm 中的扩展是一个普通的 Wasm 文件，通过 Emscripten 的 `dlopen` 动态加载。一个密码学签名被附加到 Wasm 文件中，作为名为 `duckdb_signature` 的 WebAssembly 自定义节。
这确保了该文件仍然是一个有效的 WebAssembly 文件。

> 目前，我们要求该自定义节必须是最后一个，但未来可能会放宽这一限制。

## `INSTALL` 和 `LOAD`

在原生嵌入的 DuckDB 中，`INSTALL` 的语义是获取、从 `gzip` 解压缩并存储到本地磁盘。
在原生嵌入的 DuckDB 中，`LOAD` 的语义是（可选地）执行签名检查 *和* 使用主 DuckDB 二进制文件动态加载二进制文件。

在 DuckDB-Wasm 中，`INSTALL` 是一个无操作，因为没有跨会话的持久化存储。`LOAD` 操作将获取（并实时解压缩）、执行签名检查 *和* 通过 Emscripten 实现的 `dlopen` 动态加载。

## 自动加载

[自动加载]({% link docs/stable/core_extensions/overview.md %})，即 DuckDB 能够在运行时动态添加扩展功能，是 DuckDB-Wasm 的默认启用功能。

## 官方可用扩展列表

| 扩展名称                                                          | 描述                                                      | 别名         |
| ------------------------------------------------------------------- | --------------------------------------------------------- | ------------ |
| [autocomplete]({% link docs/stable/core_extensions/autocomplete.md %}) | 在 shell 中添加自动补全支持                               |             |
| [excel]({% link docs/stable/core_extensions/excel.md %})           | 添加类似 Excel 的格式字符串支持                           |             |
| [fts]({% link docs/stable/core_extensions/full_text_search.md %})  | 添加全文搜索索引支持                                       |             |
| [icu]({% link docs/stable/core_extensions/icu.md %})               | 使用 ICU 库添加时区和排序支持                              |             |
| [inet]({% link docs/stable/core_extensions/inet.md %})             | 添加 IP 相关的数据类型和函数支持                           |             |
| [json]({% link docs/stable/data/json/overview.md %})               | 添加 JSON 操作支持                                         |             |
| [parquet]({% link docs/stable/data/parquet/overview.md %})         | 添加读写 Parquet 文件的支持                                |             |
| [sqlite]({% link docs/stable/core_extensions/sqlite.md %})         | 添加读取 SQLite 数据库文件的支持                           | sqlite, sqlite3 |
| [sqlsmith]({% link docs/stable/core_extensions/sqlsmith.md %})     |                                                              |             |
| [tpcds]({% link docs/stable/core_extensions/tpcds.md %})           | 添加 TPC-DS 数据生成和查询支持                              |             |
| [tpch]({% link docs/stable/core_extensions/tpch.md %})             | 添加 TPC-H 数据生成和查询支持                               |             |

WebAssembly 基本上是一个额外的平台，可能会有一些平台特定的限制，导致某些扩展无法达到其原生能力或以不同方式执行。我们将在这里记录有关 DuckDB 主机扩展的相关差异。

### HTTPFS

目前，HTTPFS 扩展在 DuckDB-Wasm 中不可用。HTTPS 协议功能需要通过额外的层（浏览器）进行，这添加了差异和一些限制，使某些操作无法从原生代码中执行。

相反，DuckDB-Wasm 有一个独立的实现，对于大多数用途可以互换使用，但不支持所有使用情况（因为它必须遵循浏览器施加的安全规则，如 CORS）。
由于 CORS 限制，使用 HTTPFS 扩展进行的数据请求必须是针对允许（使用 CORS 头）访问该数据的网站。
[MDN 网站](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) 是了解 CORS 的宝贵资源。

## 扩展签名

与常规 DuckDB 扩展一样，DuckDB-Wasm 扩展在 `LOAD` 时默认检查签名以验证扩展未被篡改。
可以通过配置选项禁用扩展签名验证。
签名是二进制文件本身的属性，因此复制 DuckDB 扩展（例如从不同位置提供）仍会保留有效的签名（例如用于本地开发）。

## 获取 DuckDB-Wasm 扩展

官方 DuckDB 扩展提供在 `extensions.duckdb.org`，这也是 `default_extension_repository` 选项的默认值。
安装扩展时，会构建一个相关 URL，格式为 `extensions.duckdb.org/$duckdb_version_hash/$duckdb_platform/$name.duckdb_extension.gz`。

DuckDB-Wasm 扩展仅在加载时获取，URL 格式为：`extensions.duckdb.org/duckdb-wasm/$duckdb_version_hash/$duckdb_platform/$name.duckdb_extension.wasm`。

请注意，文件夹结构中额外添加了 `duckdb-wasm`，并且文件以 `.wasm` 文件形式提供。

DuckDB-Wasm 扩展使用 Brotli 压缩预压缩提供。从浏览器获取扩展时，会透明地进行解压。如果你想手动获取 `duckdb-wasm` 扩展，可以使用 `curl --compress extensions.duckdb.org/<...>/icu.duckdb_extension.wasm`。

## 从第三方仓库提供扩展

与常规 DuckDB 一样，如果你使用 `SET custom_extension_repository = some.url.com`，后续加载将尝试从 `some.url.com/duckdb-wasm/$duckdb_version_hash/$duckdb_platform/$name.duckdb_extension.wasm` 获取。

请注意，对扩展的 GET 请求需要 [启用 CORS](https://www.w3.org/wiki/CORS_Enabled)，以便浏览器允许连接。

## 工具链

DuckDB-Wasm 及其扩展均使用最新的打包 Emscripten 工具链进行编译。

<!-- markdownlint-disable-next-line -->
{% include iframe.html src="https://shell.duckdb.org" %}

---