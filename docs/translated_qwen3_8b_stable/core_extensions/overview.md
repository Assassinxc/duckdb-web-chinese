---
---
layout: docu
title: 核心扩展
redirect_from:
- /docs/extensions/official_extensions
- /docs/extensions/official_extensions/
---

## 核心扩展列表

| 名称                                                                    | GitHub                                                                           | 描述                                                                        | 阶段        | 别名                 |
| :---------------------------------------------------------------------- | -------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------- | :----------- | :---------------------- |
| [autocomplete]({% link docs/stable/core_extensions/autocomplete.md %}) |                                                                                  | 在 shell 中添加自动补全支持                                         | 稳定       |                         |
| [avro]({% link docs/stable/core_extensions/avro.md %})                 | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-avro)      | 添加对 Avro 文件的读取支持                                                 | 稳定       |                         |
| [aws]({% link docs/stable/core_extensions/aws.md %})                   | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-aws)       | 提供依赖 AWS SDK 的功能                                       | 稳定       |                         |
| [azure]({% link docs/stable/core_extensions/azure.md %})               | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-azure)     | 为 Azure blob 存储添加文件系统抽象到 DuckDB                     | 稳定       |                         |
| [delta]({% link docs/stable/core_extensions/delta.md %})               | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-delta)     | 添加对 Delta Lake 的支持                                                        | 实验性 |                         |
| [ducklake]({% link docs/stable/core_extensions/ducklake.md %})         | [<span class="github">GitHub</span>](https://github.com/duckdb/ducklake)         | 添加对 DuckLake 的支持                                                          | 实验性 |                         |
| [encodings]({% link docs/stable/core_extensions/encodings.md %})       | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-encodings) | 添加对 ICU 数据库中可用编码的支持                    | 实验性 |                         |
| [excel]({% link docs/stable/core_extensions/excel.md %})               | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-excel)     | 添加对 Excel 文件的读写支持                                   | 实验性 |                         |
| [fts]({% link docs/stable/core_extensions/full_text_search.md %})      | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-fts)       | 添加对全文搜索索引的支持                                          | 实验性 |                         |
| [httpfs]({% link docs/stable/core_extensions/httpfs/overview.md %})    | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-httpfs)    | 添加对通过 HTTP(S) 或 S3 连接读写文件的支持        | 稳定       | http, https, s3         |
| [iceberg]({% link docs/stable/core_extensions/iceberg/overview.md %})  | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-iceberg)   | 添加对 Apache Iceberg 的支持                                                    | 实验性 |                         |
| [icu]({% link docs/stable/core_extensions/icu.md %})                   |                                                                                  | 使用 ICU 库添加对时区和排序规则的支持                   | 稳定       |                         |
| [inet]({% link docs/stable/core_extensions/inet.md %})                 | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-inet)      | 添加对 IP 相关数据类型和函数的支持                               | 实验性 |                         |
| [jemalloc]({% link docs/stable/core_extensions/jemalloc.md %})         |                                                                                  | 使用 jemalloc 替代系统内存分配器                                      | 稳定       |                         |
| [json]({% link docs/stable/data/json/overview.md %})                   |                                                                                  | 添加对 JSON 操作的支持                                                   | 稳定       |                         |
| [mysql]({% link docs/stable/core_extensions/mysql.md %})               | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-mysql)     | 添加对 MySQL 数据库的读写支持                      | 稳定       | mysql_scanner           |
| [parquet]({% link docs/stable/data/parquet/overview.md %})             |                                                                                  | 添加对 Parquet 文件的读写支持                                 | 稳定       |                         |
| [postgres]({% link docs/stable/core_extensions/postgres.md %})         | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-postgres)  | 添加对 PostgreSQL 数据库的读写支持                 | 稳定       | postgres_scanner        |
| [spatial]({% link docs/stable/core_extensions/spatial/overview.md %})  | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-spatial)   | 地理空间扩展，添加对空间数据和函数的支持 | 实验性 |                         |
| [sqlite]({% link docs/stable/core_extensions/sqlite.md %})             | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-sqlite)    | 添加对 SQLite 数据库文件的读写支持                 | 稳定       | sqlite_scanner, sqlite3 |
| [tpcds]({% link docs/stable/core_extensions/tpcds.md %})               |                                                                                  | 添加 TPC-DS 数据生成和查询支持                                      | 实验性 |                         |
| [tpch]({% link docs/stable/core_extensions/tpch.md %})                 |                                                                                  | 添加 TPC-H 数据生成和查询支持                                       | 稳定       |                         |
| [ui]({% link docs/stable/core_extensions/ui.md %})                     | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-ui)        | 添加 DuckDB 的本地 UI                                                           | 实验性 |                         |
| [vss]({% link docs/stable/core_extensions/vss.md %})                   | [<span class="github">GitHub</span>](https://github.com/duckdb/duckdb-vss)       | 添加对向量相似性搜索查询的支持                                  | 实验性 |                         |

**阶段** 列显示了扩展的生命周期阶段，遵循 [tidyverse](https://lifecycle.r-lib.org/articles/stages.html) 所使用的生命周期阶段的约定。

## 默认扩展

不同的 DuckDB 客户端包含的扩展集合也不同。
下面的表格总结了主要的发行版本。

| 名称                                                                    | CLI | Python | R   | Java | Node.js |
| ----------------------------------------------------------------------- | --- | ------ | --- | ---- | ------- |
| [autocomplete]({% link docs/stable/core_extensions/autocomplete.md %}) | yes |        |     |      |         |
| [icu]({% link docs/stable/core_extensions/icu.md %})                   | yes | yes    |     | yes  | yes     |
| [json]({% link docs/stable/data/json/overview.md %})                   | yes | yes    |     | yes  | yes     |
| [parquet]({% link docs/stable/data/parquet/overview.md %})             | yes | yes    | yes | yes  | yes     |

jemalloc 扩展的可用性取决于操作系统。
请查看 [jemalloc 页面]({% link docs/stable/core_extensions/jemalloc.md %}) 获取详细信息。