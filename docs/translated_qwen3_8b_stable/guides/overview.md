---
---
layout: docu
redirect_from:
- /docs/guides
- /docs/guides/
- /docs/guides/index
- /docs/guides/index/
- /docs/guides/overview
title: 指南
---

指南部分包含简明的如何操作指南，专注于实现单个目标。
如需查看 API 参考和示例，请查看文档的其余部分。

请注意，有许多使用 DuckDB 的工具并未包含在官方指南中。
要查找这些工具列表，请查看 [Awesome DuckDB 仓库](https://github.com/davidgasquez/awesome-duckdb)。

> 提示：如需一个简短的入门教程，请查看 [“荷兰铁路交通分析”]({% post_url 2024-05-31-analyzing-railway-traffic-in-the-netherlands %}) 教程。

## 数据导入和导出

* [数据导入概述]({% link docs/stable/guides/file_formats/overview.md %})
* [使用 `file:` 协议访问文件]({% link docs/stable/guides/file_formats/file_access.md %})

### CSV 文件

* [如何将 CSV 文件加载到表中]({% link docs/stable/guides/file_formats/csv_import.md %})
* [如何将表导出为 CSV 文件]({% link docs/stable/guides/file_formats/csv_export.md %})

### Parquet 文件

* [如何将 Parquet 文件加载到表中]({% link docs/stable/guides/file_formats/parquet_import.md %})
* [如何将表导出为 Parquet 文件]({% link docs/stable/guides/file_formats/parquet_export.md %})
* [如何直接在 Parquet 文件上运行查询]({% link docs/stable/guides/file_formats/query_parquet.md %})

### HTTP(S)、S3 和 GCP

* [如何直接从 HTTP(S) 加载 Parquet 文件]({% link docs/stable/guides/network_cloud_storage/http_import.md %})
* [如何直接从 S3 加载 Parquet 文件]({% link docs/stable/guides/network_cloud_storage/s3_import.md %})
* [如何将 Parquet 文件导出到 S3]({% link docs/stable/guides/network_cloud_storage/s3_export.md %})
* [如何从 S3 Express One 加载 Parquet 文件]({% link docs/stable/guides/network_cloud_storage/s3_express_one.md %})
* [如何直接从 GCS 加载 Parquet 文件]({% link docs/stable/guides/network_cloud_storage/gcs_import.md %})
* [如何直接从 Cloudflare R2 加载 Parquet 文件]({% link docs/stable/guides/network_cloud_storage/cloudflare_r2_import.md %})
* [如何直接从 S3 加载 Iceberg 表]({% link docs/stable/guides/network_cloud_storage/s3_iceberg_import.md %})

### JSON 文件

* [如何将 JSON 文件加载到表中]({% link docs/stable/guides/file_formats/json_import.md %})
* [如何将表导出为 JSON 文件]({% link docs/stable/guides/file_formats/json_export.md %})

### 使用空间扩展的 Excel 文件

* [如何将 Excel 文件加载到表中]({% link docs/stable/guides/file_formats/excel_import.md %})
* [如何将表导出为 Excel 文件]({% link docs/stable/guides/file_formats/excel_export.md %})

### 查询其他数据库系统

* [如何直接查询 MySQL 数据库]({% link docs/stable/guides/database_integration/mysql.md %})
* [如何直接查询 PostgreSQL 数据库]({% link docs/stable/guides/database_integration/postgres.md %})
* [如何直接查询 SQLite 数据库]({% link docs/stable/guides/database_integration/sqlite.md %})

### 直接读取文件

* [如何直接读取二进制文件]({% link docs/stable/guides/file_formats/read_file.md %}#read_blob)
* [如何直接读取文本文件]({% link docs/stable/guides/file_formats/read_file.md %}#read_text)

## 性能

* [我的工作负载很慢（故障排除指南）]({% link docs/stable/guides/performance/my_workload_is_slow.md %})
* [如何设计用于最佳性能的模式]({% link docs/stable/guides/performance/schema.md %})
* [DuckDB 的理想硬件环境是什么]({% link docs/stable/guides/performance/environment.md %})
* [Parquet 文件和（压缩）CSV 文件对性能有何影响]({% link docs/stable/guides/performance/file_formats.md %})
* [如何调优工作负载]({% link docs/stable/guides/performance/how_to_tune_workloads.md %})
* [基准测试]({% link docs/stable/guides/performance/benchmarks.md %})

## 元查询

* [如何列出所有表]({% link docs/stable/guides/meta/list_tables.md %})
* [如何查看查询结果的模式]({% link docs/stable/guides/meta/describe.md %})
* [如何使用 summarize 快速了解数据集]({% link docs/stable/guides/meta/summarize.md %})
* [如何查看查询的查询计划]({% link docs/stable/guides/meta/explain.md %})
* [如何分析查询]({% link docs/stable/guides/meta/explain_analyze.md %})

## ODBC

* [如何设置 ODBC 应用程序（以及更多！）]({% link docs/stable/guides/odbc/general.md %})

## Python 客户端

* [如何安装 Python 客户端]({% link docs/stable/guides/python/install.md %})
* [如何执行 SQL 查询]({% link docs/stable/guides/python/execute_sql.md %})
* [如何在 Jupyter 笔记本中轻松查询 DuckDB]({% link docs/stable/guides/python/jupyter.md %})
* [如何在 marimo 笔记本中轻松查询 DuckDB]({% link docs/stable/guides/python/marimo.md %})
* [如何在 DuckDB 中使用多个 Python 线程]({% link docs/stable/guides/python/multiple_threads.md %})
* [如何在 DuckDB 中使用 fsspec 文件系统]({% link docs/stable/guides/python/filesystems.md %})

### Pandas

* [如何在 Pandas DataFrame 上执行 SQL]({% link docs/stable/guides/python/sql_on_pandas.md %})
* [如何从 Pandas DataFrame 创建表]({% link docs/stable/guides/python/import_pandas.md %})
* [如何将数据导出到 Pandas DataFrame]({% link docs/stable/guides/python/export_pandas.md %})

### Apache Arrow

* [如何在 Apache Arrow 上执行 SQL]({% link docs/stable/guides/python/sql_on_arrow.md %})
* [如何从 Apache Arrow 创建 DuckDB 表]({% link docs/stable/guides/python/import_arrow.md %})
* [如何将数据导出到 Apache Arrow]({% link docs/stable/guides/python/export_arrow.md %})

### 关系型 API

* [如何使用关系型 API 查询 Pandas DataFrame]({% link docs/stable/guides/python/relational_api_pandas.md %})

### Python 库集成

* [如何使用 Ibis 通过 SQL 或不通过 SQL 查询 DuckDB]({% link docs/stable/guides/python/ibis.md %})
* [如何通过 Apache Arrow 使用 DuckDB 与 Polars DataFrame 集成]({% link docs/stable/guides/python/polars.md %})

## SQL 特性

* [友好的 SQL]({% link docs/stable/sql/dialect/friendly_sql.md %})
* [As-of 连接]({% link docs/stable/guides/sql_features/asof_join.md %})
* [全文搜索]({% link docs/stable/guides/sql_features/full_text_search.md %})
* [`query` 和 `query_table` 函数]({% link docs/stable/guides/sql_features/query_and_query_table_functions.md %})

## SQL 编辑器和 IDE

* [如何设置 DBeaver SQL IDE]({% link docs/stable/guides/sql_editors/dbeaver.md %})

## 数据查看器

* [如何使用 Tableau 可视化 DuckDB 数据库]({% link docs/stable/guides/data_viewers/tableau.md %})
* [如何使用 DuckDB 和 YouPlot 在命令行中绘制图表]({% link docs/stable/guides/data_viewers/youplot.md %})