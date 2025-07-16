---
---
layout: docu
redirect_from:
- /docs/guides/import/overview
- /docs/guides/import/overview/
- /docs/guides/performance/import
title: 数据导入
---

## 推荐的导入方法

将数据从其他系统导入到DuckDB时，需要注意一些事项。
我们推荐按照以下顺序进行导入：

1. 对于支持DuckDB扫描器扩展的系统，建议使用扫描器。DuckDB目前提供了对[MySQL]({% link docs/stable/guides/database_integration/mysql.md %})、[PostgreSQL]({% link docs/stable/guides/database_integration/postgres.md %})和[SQLite]({% link docs/stable/guides/database_integration/sqlite.md %})的支持。
2. 如果数据源系统有批量导出功能，可以将数据导出为Parquet或CSV格式，然后使用DuckDB的[Parquet]({% link docs/stable/guides/file_formats/parquet_import.md %})或[CSV加载器]({% link docs/stable/guides/file_formats/csv_import.md %})进行加载。
3. 如果上述方法不适用，可以考虑使用DuckDB的[追加器]({% link docs/stable/data/appender.md %})，目前在C、C++、Go、Java和Rust API中可用。

## 应避免的方法

如果可能，请避免逐行（元组逐个）循环，而应使用批量操作。
逐行插入（即使使用预编译语句）会严重影响性能，并导致加载速度变慢。

> 最佳实践 除非您的数据量很小（<100k行），请避免在循环中使用插入操作。