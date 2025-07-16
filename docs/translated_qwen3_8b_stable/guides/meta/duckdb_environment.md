---
---
layout: docu
redirect_from:
- /docs/guides/meta/duckdb_environment
title: DuckDB 环境
---

DuckDB 提供了一系列函数和 `PRAGMA` 选项，用于获取正在运行的 DuckDB 实例及其环境的信息。

## 版本

`version()` 函数返回 DuckDB 的版本号。

```sql
SELECT version() AS version;
```

<div class="monospace_table"></div>

| version |
|-----------|
| v{{ site.current_duckdb_version }} |

使用 `PRAGMA`：

```sql
PRAGMA version;
```

<div class="monospace_table"></div>

| library_version | source_id  |
|-----------------|------------|
| v{{ site.current_duckdb_version }} | {{ site.current_duckdb_hash }} |

## 平台

平台信息包括操作系统、系统架构以及可选的编译器。
平台信息在[安装扩展]({% link docs/stable/extensions/extension_distribution.md %}#platforms)时使用。
要获取平台信息，可以使用以下 `PRAGMA`：

```sql
PRAGMA platform;
```

在 macOS 上，运行在 Apple Silicon 架构上，结果为：

| platform  |
|-----------|
| osx_arm64 |

在 Windows 上，运行在 AMD64 架构上，平台为 `windows_amd64`。
在 Ubuntu Linux 上，运行在 ARM64 架构上，平台为 `linux_arm64`。

## 扩展

要获取 DuckDB 扩展及其状态（例如 `loaded`、`installed`）的列表，可以使用 [`duckdb_extensions()` 函数]({% link docs/stable/core_extensions/overview.md %}#listing-extensions)：

```sql
SELECT *
FROM duckdb_extensions();
```

## 元数据表函数

DuckDB 提供了以下内置的表函数，用于获取可用目录对象的元数据：

* [`duckdb_columns()`]({% link docs/stable/sql/meta/duckdb_table_functions.md %}#duckdb_columns): 列
* [`duckdb_constraints()`]({% link docs/stable/sql/meta/duckdb_table_functions.md %}#duckdb_constraints): 约束
* [`duckdb_databases()`]({% link docs/stable/sql/meta/duckdb_table_functions.md %}#duckdb_databases): 列出当前 DuckDB 进程可访问的数据库
* [`duckdb_dependencies()`]({% link docs/stable/sql/meta/duckdb_table_functions.md %}#duckdb_dependencies): 对象之间的依赖关系
* [`duckdb_extensions()`]({% link docs/stable/sql/meta/duckdb_table_functions.md %}#duckdb_extensions): 扩展
* [`duckdb_functions()`]({% link docs/stable/sql/meta/duckdb_table_functions.md %}#duckdb_functions): 函数
* [`duckdb_indexes()`]({% link docs/stable/sql/meta/duckdb_table_functions.md %}#duckdb_indexes): 二级索引
* [`duckdb_keywords()`]({% link docs/stable/sql/meta/duckdb_table_functions.md %}#duckdb_keywords): DuckDB 的关键字和保留字
* [`duckdb_optimizers()`]({% link docs/stable/sql/meta/duckdb_table_functions.md %}#duckdb_optimizers): DuckDB 实例中可用的优化规则
* [`duckdb_schemas()`]({% link docs/stable/sql/meta/duckdb_table_functions.md %}#duckdb_schemas): 架构
* [`duckdb_sequences()`]({% link docs/stable/sql/meta/duckdb_table_functions.md %}#duckdb_sequences): 序列
* [`duckdb_settings()`]({% link docs/stable/sql/meta/duckdb_table_functions.md %}#duckdb_settings): 设置
* [`duckdb_tables()`]({% link docs/stable/sql/meta/duckdb_table_functions.md %}#duckdb_tables): 基础表
* [`duckdb_temporary_files()`]({% link docs/stable/sql/meta/duckdb_table_functions.md %}#duckdb_temporary_files): DuckDB 写入磁盘的临时文件，用于将数据从内存中卸载
* [`duckdb_types()`]({% link docs/stable/sql/meta/duckdb_table_functions.md %}#duckdb_types): 数据类型
* [`duckdb_views()`]({% link docs/stable/sql/meta/duckdb_table_functions.md %}#duckdb_views): 视图