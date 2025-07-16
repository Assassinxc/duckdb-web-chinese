---
---
layout: docu
title: 部署 DuckDB-Wasm
---

部署 DuckDB-Wasm 需要访问以下组件：

* DuckDB-Wasm 主库组件，以 TypeScript 形式分发，并编译为 JavaScript 代码
* DuckDB-Wasm Worker 组件，编译为 JavaScript 代码，可能在多线程环境中被多次实例化
* DuckDB-Wasm 模块，编译为 WebAssembly 文件，并由浏览器实例化
* 任何相关的 DuckDB-Wasm 扩展

## 主库组件

该组件以 TypeScript 代码或 CommonJS JavaScript 代码形式分发在 `npm` duckdb-wasm 包中，可以与应用程序一起打包，或在同源（子）域中提供并运行时包含，也可以从第三方 CDN（如 JSDelivery）提供。
此组件需要某种形式的转译，不能直接提供，因为它需要知道后续文件的位置才能正常运行。
具体细节取决于您的部署环境，示例请参见 <https://github.com/duckdb/duckdb-wasm/tree/main/examples>。
例如部署可以是 <https://shell.duckdb.org>，该部署将主库组件与 shell 代码一起转译（第一种方法）。或者参见 <https://github.com/duckdb/duckdb-wasm/tree/main/examples/bare-browser> 的 `bare-browser` 示例。

## JS Worker 组件

该组件以三种不同形式的 JavaScript 文件分发，分别为 `mvp`、`eh` 和 `threads`，需要直接提供，主库组件需要知道实际位置。

有三种变体对应三种不同的 `平台`：

- MVP 面向 WebAssembly 1.0 规范
- EH 面向 WebAssembly 1.0 规范，并增加了 Wasm 级异常处理，提升了性能
- THREADS 面向 WebAssembly 规范，并增加了异常和线程构造

您可以提供所有三种变体并进行特性检测，或者提供一个变体并指导 duckdb-wasm 库使用哪一个。

## Wasm Worker 组件

与 JS Worker 组件相同，有三种不同形式，`mvp`、`eh` 和 `threads`，每种形式都由相应的 JS 组件使用。这些 WebAssembly 模块需要在任意可达的 [子] 域中直接提供。

## DuckDB 扩展

DuckDB-Wasm 的 DuckDB 扩展与原生情况类似，均在默认扩展端点 `https://extensions.duckdb.org` 提供签名。
如果您部署 duckdb-wasm，可以考虑在不同的端点镜像相关扩展，这可能允许在内部网络中进行严格的部署。

```sql
SET custom_extension_repository = '⟨https://some.endpoint.org/path/to/repository⟩';
```

此语句将默认扩展仓库从公共的 `https://extensons.duckdb.org` 更改为指定的仓库。请注意，扩展仍然签名，因此最佳做法是下载并提供与原始仓库结构相似的扩展。更多信息请参见 https://duckdb.org/docs/stable/extensions/extension_distribution#creating-a-custom-repository。

社区扩展在 https://community-extensioions.duckdb.org 提供，它们使用不同的密钥进行签名，因此可以通过单向 SQL 语句禁用：

```sql
SET allow_community_extensions = false;
```

此语句将仅允许加载核心 DuckDB 扩展。请注意，错误发生在 `LOAD` 时，而不是 `INSTALL` 时。

请参阅 <https://duckdb.org/docs/stable/extensions/extension_distribution> 以获取有关扩展的一般信息。

## 安全考虑

> 警告：使用对您数据的访问权限部署 DuckDB-Wasm 意味着任何拥有 SQL 访问权限的人都可以访问 DuckDB-Wasm 可以访问的数据。此外，DuckDB-Wasm 在默认设置下可以访问远程端点，因此对沙箱内外的外部世界都有明显影响。