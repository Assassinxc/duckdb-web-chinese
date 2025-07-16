---
---
github_repository: https://github.com/duckdb/duckdb-wasm
layout: docu
redirect_from:
- /docs/api/wasm
- /docs/api/wasm/
- /docs/api/wasm/overview
- /docs/api/wasm/overview/
- /docs/clients/wasm/overview
title: DuckDB Wasm
---

> DuckDB WebAssembly 客户端的最新版本是 {{ site.current_duckdb_wasm_version }}。

DuckDB 已经被编译为 WebAssembly，因此可以在任何设备上的任何浏览器中运行。

<!-- markdownlint-disable-next-line -->
{% include iframe.html src="https://shell.duckdb.org" %}

DuckDB-Wasm 提供了一个分层的 API，您可以根据需要将其嵌入为 [JavaScript + WebAssembly 库](https://www.npmjs.com/package/@duckdb/duckdb-wasm)，作为 [Web 命令行工具](https://www.npmjs.com/package/@duckdb/duckdb-wasm-shell)，或者从 [源代码构建](https://github.com/duckdb/duckdb-wasm)。

## 开始使用 DuckDB-Wasm

一个很好的起点是阅读 [DuckDB-Wasm 发布博客文章]({% post_url 2021-10-29-duckdb-wasm %})！

另一个宝贵资源是 [GitHub 仓库](https://github.com/duckdb/duckdb-wasm)。

如需详细信息，请参阅完整的 [DuckDB-Wasm API 文档](https://shell.duckdb.org/docs/modules/index.html)。

## 限制

* 默认情况下，WebAssembly 客户端仅使用单个线程。
* WebAssembly 客户端可用内存有限。[WebAssembly 将可用内存限制为 4 GB](https://v8.dev/blog/4gb-wasm-memory)，而浏览器可能会施加更严格的限制。