---
---
layout: docu
redirect_from:
  - /clients
  - /docs/clients
  - /docs/clients/
  - /docs/api/overview
  - /docs/api/overview/
  - /docs/clients/overview
title: 客户端概览
---

DuckDB 是一个进程内数据库系统，为多种语言提供了客户端 API（也称为“驱动程序”）。

| 客户端 API                                                                     | 维护者                                                                              | 支持层级 | 版本                                                                                                                     |
| ------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------- | ------------ | --------------------------------------------------------------------------------------------------------------------------- |
| [C]({% link docs/stable/clients/c/overview.md %})                              | DuckDB 团队                                                                         | 一级      | [{{ site.current_duckdb_version }}]({% link docs/installation/index.html %}?version=stable&environment=cplusplus)           |
| [命令行界面 (CLI)]({% link docs/stable/clients/cli/overview.md %}) | DuckDB 团队                                                                         | 一级      | [{{ site.current_duckdb_version }}]({% link docs/installation/index.html %}?version=stable&environment=cli)                 |
| [Java (JDBC)]({% link docs/stable/clients/java.md %})                          | DuckDB 团队                                                                         | 一级      | [{{ site.current_duckdb_java_short_version }}](https://central.sonatype.com/artifact/org.duckdb/duckdb_jdbc)                |
| [Go]({% link docs/stable/clients/go.md %})                                     | [Marc Boeker](https://github.com/marcboeker) 和 DuckDB 团队                        | 一级      | [{{ site.current_duckdb_go_version }}](https://github.com/marcboeker/go-duckdb?tab=readme-ov-file#go-sql-driver-for-duckdb) |
| [Node.js (node-neo)]({% link docs/stable/clients/node_neo/overview.md %})      | [Jeff Raymakers](https://github.com/jraymakers) ([MotherDuck](https://motherduck.com/)) | 一级      | [{{ site.current_duckdb_node_neo_version }}](https://www.npmjs.com/package/@duckdb/node-api)                                |
| [ODBC]({% link docs/stable/clients/odbc/overview.md %})                        | DuckDB 团队                                                                         | 一级      | [{{ site.current_duckdb_odbc_short_version }}]({% link docs/installation/index.html %}?version=stable&environment=odbc)     |
| [Python]({% link docs/stable/clients/python/overview.md %})                    | DuckDB 团队                                                                         | 一级      | [{{ site.current_duckdb_version }}](https://pypi.org/project/duckdb/)                                                       |
| [R]({% link docs/stable/clients/r.md %})                                       | [Kirill Müller](https://github.com/krlmlr) 和 DuckDB 团队                          | 一级      | [{{ site.current_duckdb_r_version }}](https://cran.r-project.org/web/packages/duckdb/index.html)                            |
| [Rust]({% link docs/stable/clients/rust.md %})                                 | DuckDB 团队                                                                         | 一级      | [{{ site.current_duckdb_rust_version }}](https://crates.io/crates/duckdb)                                                   |
| [WebAssembly (Wasm)]({% link docs/stable/clients/wasm/overview.md %})          | DuckDB 团队                                                                         | 一级      | [{{ site.current_duckdb_wasm_version }}](https://github.com/duckdb/duckdb-wasm?tab=readme-ov-file#duckdb-and-duckdb-wasm)   |
| [ADBC (Arrow)]({% link docs/stable/clients/adbc.md %})                         | DuckDB 团队                                                                         | 二级      | [{{ site.current_duckdb_version }}]({% link docs/stable/clients/adbc.md %})                                                 |
| [C# (.NET)](https://duckdb.net/)                                               | [Giorgi](https://github.com/Giorgi)                                                     | 二级      | [{{ site.current_duckdb_csharp_version}}](https://www.nuget.org/packages/DuckDB.NET.Bindings.Full)                          |
| [C++]({% link docs/stable/clients/cpp.md %})                                   | DuckDB 团队                                                                         | 二级      | [{{ site.current_duckdb_version }}]({% link docs/installation/index.html %}?version=stable&environment=cplusplus)           |
| [Dart]({% link docs/stable/clients/dart.md %})                                 | [TigerEye](https://www.tigereye.com/)                                                   | 二级      | [{{ site.current_duckdb_dart_version }}](https://pub.dev/packages/dart_duckdb)                                              |
| [Node.js (弃用)]({% link docs/stable/clients/nodejs/overview.md %})      | DuckDB 团队                                                                         | 二级      | [{{ site.current_duckdb_nodejs_version }}](https://www.npmjs.com/package/duckdb)                                            |
| [Common Lisp](https://github.com/ak-coram/cl-duckdb)                           | [ak-coram](https://github.com/ak-coram)                                                 | 三级      |                                                                                                                             |
| [Crystal](https://github.com/amauryt/crystal-duckdb)                           | [amauryt](https://github.com/amauryt)                                                   | 三级      |                                                                                                                             |
| [Elixir](https://github.com/AlexR2D2/duckdbex)                                 | [AlexR2D2](https://github.com/AlexR2D2/duckdbex)                                        | 三级      |                                                                                                                             |
| [Erlang](https://github.com/mmzeeman/educkdb)                                  | [MM Zeeman](https://github.com/mmzeeman)                                                | 三级      |                                                                                                                             |
| [Julia]({% link docs/stable/clients/julia.md %})                               | DuckDB 团队                                                                         | 三级      |                                                                                                                             |
| [PHP](https://github.com/satur-io/duckdb-php)                                  | [satur-io](https://github.com/satur-io)                                                 | 三级      |                                                                                                                             |
| [Pyodide](https://github.com/duckdb/duckdb-pyodide)                            | DuckDB 团队                                                                         | 三级      |                                                                                                                             |
| [Ruby](https://suketa.github.io/ruby-duckdb/)                                  | [suketa](https://github.com/suketa)                                                     | 三级      |                                                                                                                             |
| [Scala](https://www.duck4s.com/docs/index.html)                                | [Salar Rahmanian](https://www.softinio.com)                                             | 三级      |                                                                                                                             |
| [Swift]({% link docs/stable/clients/swift.md %})                               | DuckDB 团队                                                                         | 三级      |                                                                                                                             |
| [Zig](https://github.com/karlseguin/zuckdb.zig)                                | [karlseguin](https://github.com/karlseguin)                                             | 三级      |                                                                                                                             |

## 支持层级

由于客户类型众多，DuckDB 团队将开发资源集中在最流行的客户端上。
为了反映这一点，我们对客户端支持进行了三个层级的区分。
一级客户端率先获得新功能，并由 [社区支持](https://duckdblabs.com/community_support_policy) 支持。
二级客户端可以获得新功能，但不包含社区支持。
最后，三级客户端没有功能或支持的保证。

> 上述 DuckDB 客户端均为开源，我们欢迎社区为这些库做出贡献。
> 所有的一级和二级客户端均适用于 MIT 许可证。
> 对于三级客户端，请查看对应仓库的许可证信息。

我们报告了一级和二级支持层级客户端的最新稳定版本。

## 兼容性

所有 DuckDB 客户端均支持相同的 DuckDB SQL 语法，并使用相同的磁盘 [数据库格式]({% link docs/stable/internals/storage.md %}).
[DuckDB 扩展]({% link docs/stable/core_extensions/overview.md %}) 在客户端之间也具有可移植性，但有一些例外（请参见 [Wasm 扩展]({% link docs/stable/clients/wasm/extensions.md %}#list-of-officially-available-extensions)）。