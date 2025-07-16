---
---
layout: docu
redirect_from:
- /internals/repositories
- /internals/repositories/
- /docs/dev/repositories
title: DuckDB 仓库
---

DuckDB 的多个组件由不同的仓库维护。

## 主仓库

* [`duckdb`](https://github.com/duckdb/duckdb)：核心 DuckDB 项目
* [`duckdb-web`](https://github.com/duckdb/duckdb-web)：文档和博客

## 客户端

* [`duckdb-java`](https://github.com/duckdb/duckdb-java)：Java (JDBC) 客户端
* [`duckdb-node`](https://github.com/duckdb/duckdb-node)：Node.js 客户端，第一版
* [`duckdb-node-neo`](https://github.com/duckdb/duckdb-node-neo)：Node.js 客户端，第二版
* [`duckdb-odbc`](https://github.com/duckdb/duckdb-odbc)：ODBC 客户端
* [`duckdb-pyodide`](https://github.com/duckdb/duckdb-pyodide)：Pyodide 客户端
* [`duckdb-r`](https://github.com/duckdb/duckdb-r)：R 客户端
* [`duckdb-rs`](https://github.com/duckdb/duckdb-rs)：Rust 客户端
* [`duckdb-swift`](https://github.com/duckdb/duckdb-swift)：Swift 客户端
* [`duckdb-wasm`](https://github.com/duckdb/duckdb-wasm)：WebAssembly 客户端
* [`duckplyr`](https://github.com/tidyverse/duckplyr)：R 中 dplyr 的替代品
* [`go-duckdb`](https://github.com/marcboeker/go-duckdb)：Go 客户端

## 连接器

* [`dbt-duckdb`](https://github.com/duckdb/dbt-duckdb)：dbt
* [`duckdb-mysql`](https://github.com/duckdb/duckdb-mysql)：MySQL 连接器
* [`duckdb-postgres`](https://github.com/duckdb/duckdb-postgres)：PostgreSQL 连接器（从 DuckDB 连接到 PostgreSQL）
* [`duckdb-sqlite`](https://github.com/duckdb/duckdb-sqlite)：SQLite 连接器
* [`pg_duckdb`](https://github.com/duckdb/pg_duckdb)：DuckDB 的官方 PostgreSQL 扩展（在 PostgreSQL 中运行 DuckDB）

## 扩展

* 核心扩展仓库在 [官方扩展页面]({% link docs/stable/core_extensions/overview.md %}) 中链接
* 社区扩展由 [社区扩展仓库]({% link community_extensions/index.md %}) 提供

## 规范

* [DuckLake 规范](https://ducklake.select/docs/stable/specification/introduction)