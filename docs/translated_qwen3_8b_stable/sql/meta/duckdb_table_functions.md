---
---
layout: docu
redirect_from:
- /docs/sql/duckdb_table_functions
- /docs/sql/duckdb_table_functions/
- /docs/sql/meta/duckdb_table_functions
title: DuckDB_% 元数据函数
---

DuckDB 提供了一系列表函数，用于获取当前数据库的元数据信息。这些函数位于 `main` 模式中，并且其名称以 `duckdb_` 为前缀。

`duckdb_` 表函数返回的结果集可以像普通表或视图一样使用。例如，您可以在 `SELECT` 语句的 `FROM` 子句中使用 `duckdb_` 函数调用，并且可以在语句的其他部分（例如 `WHERE` 子句）中引用其返回结果集的列。

表函数仍然是函数，因此您应在函数名后加上括号以调用它并获取其返回的结果集：

```sql
SELECT * FROM duckdb_settings();
```

或者，您也可以使用 `CALL` 语法执行表函数：

```sql
CALL duckdb_settings();
```

在这种情况下，括号也是必需的。

> 对于一些 `duckdb_%` 函数，还存在一个同名的视图，它同样位于 `main` 模式中。通常，这些视图会对 `duckdb_` 表函数执行 `SELECT` 操作，并过滤掉那些被标记为内部的对象。我们在这里提到这一点，是因为如果您在调用 `duckdb_` 表函数时不小心省略了括号，您仍然可能会得到结果，但结果来自同名的视图。

示例：

`duckdb_views()` _表函数_ 返回所有视图，包括那些被标记为内部的视图：

```sql
SELECT * FROM duckdb_views();
```

`duckdb_views` _视图_ 返回那些未被标记为内部的视图：

```sql
SELECT * FROM duckdb_views;
```

## `duckdb_columns`

`duckdb_columns()` 函数提供了 DuckDB 实例中可用列的元数据信息。

| 列 | 描述 | 类型 |
|:-|:---|:-|
| `database_name` | 包含该列对象的数据库名称。 | `VARCHAR` |
| `database_oid` | 包含该列对象的数据库的内部标识符。 | `BIGINT` |
| `schema_name` | 包含定义该列的表对象的模式的 SQL 名称。 | `VARCHAR` |
| `schema_oid` | 包含该列所在表的模式对象的内部标识符。 | `BIGINT` |
| `table_name` | 定义该列的表的 SQL 名称。 | `VARCHAR` |
| `table_oid` | 定义该列的表对象的内部标识符（名称）。 | `BIGINT` |
| `column_name` | 该列的 SQL 名称。 | `VARCHAR` |
| `column_index` | 该列在其表中的唯一位置。 | `INTEGER` |
| `comment` | 由 [`COMMENT ON` 语句]({% link docs/stable/sql/statements/comment_on.md %}) 创建的注释。 | `VARCHAR` |
| `internal` | 如果该列是内置的，则为 `true`，如果它是用户定义的，则为 `false`。 | `BOOLEAN` |
| `column_default` | 该列的默认值（以 SQL 表达）。 | `VARCHAR` |
| `is_nullable` | 如果该列可以存储 `NULL` 值，则为 `true`；如果该列不能存储 `NULL` 值，则为 `false`。 | `BOOLEAN` |
| `data_type` | 该列数据类型的名称。 | `VARCHAR` |
| `data_type_id` | 该列数据类型的内部标识符。 | `BIGINT` |
| `character_maximum_length` | 始终为 `NULL`。DuckDB [文本类型]({% link docs/stable/sql/data_types/text.md %}) 不基于长度类型参数强制执行值长度限制。 | `INTEGER` |
| `numeric_precision` | 存储列值所使用的单位数（以 `numeric_precision_radix` 指示的基数为单位）。对于整数和近似数值类型，这是位数；对于十进制类型，这是数字位数。 | `INTEGER` |
| `numeric_precision_radix` | `numeric_precision` 列中单位的基数。对于整数和近似数值类型，此值为 `2`，表示精度以位数表示。对于 `decimal` 类型，此值为 `10`，表示精度以小数位数表示。 | `INTEGER` |
| `numeric_scale` | 仅适用于 `decimal` 类型。表示最大小数位数（即小数点后可能出现的数字位数）。 | `INTEGER` |

`information_schema.columns` 系统视图提供了获取数据库列元数据的更标准化方式，但 `duckdb_columns` 函数也返回了 DuckDB 内部对象的元数据。（实际上，`information_schema.columns` 是基于 `duckdb_columns()` 的查询实现的）

## `duckdb_constraints`

`duckdb_constraints()` 函数提供了 DuckDB 实例中可用的约束的元数据信息。

| 列 | 描述 | 类型 |
|:-|:---|:-|
| `database_name` | 包含该约束的数据库名称。 | `VARCHAR` |
| `database_oid` | 包含该约束的数据库的内部标识符。 | `BIGNT` |
| `schema_name` | 包含定义该约束的表的模式的 SQL 名称。 | `VARCHAR` |
| `schema_oid` | 包含定义该约束的表的模式对象的内部标识符。 | `BIGINT` |
| `table_name` | 定义该约束的表的 SQL 名称。 | `VARCHAR` |
| `table_oid` | 定义该约束的表对象的内部标识符（名称）。 | `BIGINT` |
| `constraint_index` | 表示约束在其表定义中的位置。 | `BIGINT` |
| `constraint_type` | 表示约束的类型。适用的值为 `CHECK`、`FOREIGN KEY`、`PRIMARY KEY`、`NOT NULL`、`UNIQUE`。 | `VARCHAR` |
| `constraint_text` | 以 SQL 语句形式表达的约束定义。（不一定是完整或语法正确的 DDL 语句） | `VARCHAR` |
| `expression` | 如果约束是检查约束，则为检查条件的定义，否则为 `NULL`。 | `VARCHAR` |
| `constraint_column_indexes` | 指向约束定义中出现的列的表列索引数组。 | `BIGINT[]` |
| `constraint_column_names` | 约束定义中出现的表列名数组。 | `VARCHAR[]` |
| `constraint_name` | 约束的名称。 | `VARCHAR` |
| `referenced_table` | 约束引用的表。 | `VARCHAR` |
| `referenced_column_names` | 约束引用的列名。 | `VARCHAR[]` |

`information_schema.referential_constraints` 和 `information_schema.table_constraints` 系统视图提供了获取约束元数据的更标准化方式，但 `duckdb_constraints` 函数也返回了 DuckDB 内部对象的元数据。（实际上，`information_schema.referential_constraints` 和 `information_schema.table_constraints` 是基于 `duckdb_constraints()` 的查询实现的）

## `duckdb_databases`

`duckdb_databases()` 函数列出当前 DuckDB 进程中可访问的数据库。
除了启动时关联的数据库外，列表还包括之后通过 [附加]({% link docs/stable/sql/statements/attach.md %}) 添加到 DuckDB 进程的数据库。

| 列 | 描述 | 类型 |
|:-|:---|:-|
| `database_name` | 数据库名称，或如果数据库是使用 ALIAS-clause 附加的，则为别名。 | `VARCHAR` |
| `database_oid` | 数据库的内部标识符。 | `VARCHAR` |
| `path` | 与数据库关联的文件路径。 | `VARCHAR` |
| `comment` | 由 [`COMMENT ON` 语句]({% link docs/stable/sql/statements/comment_on.md %}) 创建的注释。 | `VARCHAR` |
| `tags` | 字符串键值对的映射。 | `MAP(VARCHAR, VARCHAR)` |
| `internal` | `true` 表示系统或内置数据库。`false` 表示用户定义的数据库。 | `BOOLEAN` |
| `type` | 表示附加数据库实现的 RDBMS 类型。对于 DuckDB 数据库，该值为 `duckdb`。 | `VARCHAR` |
| `readonly` | 表示数据库是否为只读。 | `BOOLEAN` |

## `duckdb_dependencies`

`duckdb_dependencies()` 函数提供了 DuckDB 实例中可用依赖项的元数据信息。

| 列 | 描述 | 类型 |
|:--|:------|:-|
| `classid` | 始终为 0 | `BIGINT` |
| `objid` | 对象的内部 ID。 | `BIGINT` |
| `objsubid` | 始终为 0 | `INTEGER` |
| `refclassid` | 始终为 0 | `BIGINT` |
| `refobjid` | 依赖对象的内部 ID。 | `BIGINT` |
| `refobjsubid` | 始终为 0 | `INTEGER` |
| `deptype` | 依赖类型。可以是常规 (n) 或自动 (a)。 | `VARCHAR` |

## `duckdb_extensions`

`duckdb_extensions()` 函数提供了 DuckDB 实例中可用扩展的元数据信息。

| 列 | 描述 | 类型 |
|:--|:------|:-|
| `extension_name` | 扩展的名称。 | `VARCHAR` |
| `loaded` | 如果扩展已加载，则为 `true`；如果未加载，则为 `false`。 | `BOOLEAN` |
| `installed` | 如果扩展已安装，则为 `true`；如果未安装，则为 `false`。 | `BOOLEAN` |
| `install_path` | 如果扩展是内置的，则为 `(BUILT-IN)`，否则为实现该扩展的二进制文件所在的文件系统路径。 | `VARCHAR` |
| `description` | 描述扩展功能的人类可读文本。 | `VARCHAR` |
| `aliases` | 该扩展的替代名称列表。 | `VARCHAR[]` |
| `extension_version` | 扩展的版本（稳定版本为 `vX.Y.Z`，不稳定版本为 6 位哈希值）。 | `VARCHAR` |
| `install_mode` | 安装扩展时使用的安装模式：`UNKNOWN`、`REPOSITORY`、`CUSTOM_PATH`、`STATICALLY_LINKED`、`NOT_INSTALLED`、`NULL`。 | `VARCHAR` |
| `installed_from` | 扩展安装的仓库名称，例如 `community` 或 `core_nightly`。空字符串表示 `core` 仓库。 | `VARCHAR` |

## `duckdb_functions`

`duckdb_functions()` 函数提供了 DuckDB 实例中可用函数（包括宏）的元数据信息。

| 列 | 描述 | 类型 |
|:-|:---|:-|
| `database_name` | 包含此函数的数据库名称。 | `VARCHAR` |
| `database_oid` | 包含索引的数据库的内部标识符。 | `BIGINT` |
| `schema_name` | 函数所在的模式的 SQL 名称。 | `VARCHAR` |
| `function_name` | 函数的 SQL 名称。 | `VARCHAR` |
| `function_type` | 函数类型。值为：`table`、`scalar`、`aggregate`、`pragma`、`macro` | `VARCHAR` |
| `description` | 该函数的描述（始终为 `NULL`） | `VARCHAR` |
| `comment` | 由 [`COMMENT ON` 语句]({% link docs/stable/sql/statements/comment_on.md %}) 创建的注释。 | `VARCHAR` |
| `tags` | 字符串键值对的映射。 | `MAP(VARCHAR, VARCHAR)` |
| `return_type` | 返回值的逻辑数据类型名称。适用于标量函数和聚合函数。 | `VARCHAR` |
| `parameters` | 如果函数有参数，则为参数名称的列表。 | `VARCHAR[]` |
| `parameter_types` | 如果函数有参数，则为与参数列表对应的逻辑数据类型名称列表。 | `VARCHAR[]` |
| `varargs` | 如果函数有可变数量的参数，则为数据类型的名称，否则为 `NULL`。 | `VARCHAR` |
| `macro_definition` | 如果这是 [宏]({% link docs/stable/sql/statements/create_macro.md %})，则为定义它的 SQL 表达式。 | `VARCHAR` |
| `has_side_effects` | 如果这是一个纯函数，则为 `false`；如果该函数更改数据库状态（例如序列函数 `nextval()` 和 `curval()`），则为 `true`。 | `BOOLEAN` |
| `internal` | 如果该函数是内置的（由 DuckDB 或扩展定义），则为 `true`；如果使用 [`CREATE MACRO` 语句]({% link docs/stable/sql/statements/create_macro.md %}) 定义的，则为 `false`。 | `BOOLEAN` |
| `function_oid` | 该函数的内部标识符。 | `BIGINT` |
| `examples` | 使用该函数的示例。用于生成文档。 | `VARCHAR[]` |
| `stability` | 函数的稳定性（`CONSISTENT`、`VOLATILE`、`CONSISTENT_WITHIN_QUERY` 或 `NULL`） | `VARCHAR` |

## `duckdb_indexes`

`duckdb_indexes()` 函数提供了 DuckDB 实例中可用的二级索引的元数据信息。

| 列 | 描述 | 类型 |
|:-|:---|:-|
| `database_name` | 包含此索引的数据库名称。 | `VARCHAR` |
| `database_oid` | 包含该索引的数据库的内部标识符。 | `BIGINT` |
| `schema_name` | 包含具有二级索引的表的模式的 SQL 名称。 | `VARCHAR` |
| `schema_oid` | 模式对象的内部标识符。 | `BIGINT` |
| `index_name` | 该二级索引的 SQL 名称。 | `VARCHAR` |
| `index_oid` | 该索引的对象标识符。 | `BIGINT` |
| `table_name` | 具有该索引的表的名称。 | `VARCHAR` |
| `table_oid` | 表对象的内部标识符（名称）。 | `BIGINT` |
| `comment` | 由 [`COMMENT ON` 语句]({% link docs/stable/sql/statements/comment_on.md %}) 创建的注释。 | `VARCHAR` |
| `tags` | 字符串键值对的映射。 | `MAP(VARCHAR, VARCHAR)` |
| `is_unique` | 如果索引是使用 `UNIQUE` 修饰符创建的，则为 `true`；否则为 `false`。 | `BOOLEAN` |
| `is_primary` | 始终为 `false`。 | `BOOLEAN` |
| `expressions` | 始终为 `NULL`。 | `VARCHAR` |
| `sql` | 以 `CREATE INDEX` SQL 语句形式表示的索引定义。 | `VARCHAR` |

请注意，`duckdb_indexes` 仅提供关于二级索引的元数据信息，即那些通过显式的 [`CREATE INDEX`]({% link docs/stable/sql/indexes.md %}#create-index) 语句创建的索引。主键、外键和 `UNIQUE` 约束是通过索引维护的，但其详细信息包含在 `duckdb_constraints()` 函数中。

## `duckdb_keywords`

`duckdb_keywords()` 函数提供了 DuckDB 关键字和保留字的元数据信息。

| 列 | 描述 | 类型 |
|:-|:---|:-|
| `keyword_name` | 关键字。 | `VARCHAR` |
| `keyword_category` | 表示关键字的类别。值为 `column_name`、`reserved`、`type_function` 和 `unreserved`。 | `VARCHAR` |

## `duckdb_log_contexts`

`duckdb_log_contexts()` 函数提供了 DuckDB 日志条目上下文的信息。

| 列 | 描述 | 类型 |
|:-|:---|:-|
| `context_id` | 上下文的标识符。`duckdb_logs` 表中的 `context_id` 列是此列的外键。 | `UBIGINT` |
| `scope` | 上下文的作用域（`connection`、`database` 或 `file_opener` TODO: + more ? <https://github.com/duckdb/duckdb/pull/15119>）。 | `VARCHAR` |
| `connection_id` | 连接的标识符。 | `UBIGINT` |
| `transaction_id` | 事务的标识符。 | `UBIGINT` |
| `query_id` | 查询的标识符。 | `UBIGINT` |
| `thread_id` | 线程的标识符。 | `UBIGINT` |

## `duckdb_logs`

`duckdb_logs()` 函数返回 DuckDB 日志条目的表。

| 列 | 描述 | 类型 |
|:-|:---|:-|
| `context_id` | 日志条目上下文的标识符。外键指向 [`duckdb_log_contexts`](#duckdb_log_contexts) 表。 | `UBIGINT` |
| `timestamp` | 日志条目的时间戳。 | `TIMESTAMP` |
| `type` | 日志条目的类型。 TODO: ?? | `VARCHAR` |
| `log_level` | 日志条目的级别（`TRACE`、`DEBUG`、`INFO`、`WARN`、`ERROR` 或 `FATAL`）。 | `VARCHAR` |
| `message` | 日志条目的消息。 | `VARCHAR` |

## `duckdb_memory`

`duckdb_memory()` 函数提供了关于 DuckDB 缓冲区管理器的元数据信息。

| 列 | 描述 | 类型 |
|:-|:---|:-|
| `tag` | 内存标签。其值为以下之一：`BASE_TABLE`、`HASH_TABLE`、`PARQUET_READER`、`CSV_READER`、`ORDER_BY`、`ART_INDEX`、`COLUMN_DATA`、`METADATA`、`OVERFLOW_STRINGS`、`IN_MEMORY_TABLE`、`ALLOCATOR`、`EXTENSION`。 | `VARCHAR` |
| `memory_usage_bytes` | 使用的内存（以字节为单位）。 | `BIGINT` |
| `temporary_storage_bytes` | 使用的磁盘存储（以字节为单位）。 | `BIGINT` |

## `duckdb_optimizers`

`duckdb_optimizers()` 函数提供了 DuckDB 实例中可用的优化规则（例如 `expression_rewriter`、`filter_pushdown`）的元数据信息。
这些规则可以通过 [`PRAGMA disabled_optimizers`]({% link docs/stable/configuration/pragmas.md %}#selectively-disabling-optimizers) 选择性地禁用。

| 列 | 描述 | 类型 |
|:-|:---|:-|
| `name` | 优化规则的名称。 | `VARCHAR` |

## `duckdb_prepared_statements`

`duckdb_prepared_statements()` 函数提供了当前 DuckDB 会话中可用的 [预编译语句]({% link docs/stable/sql/query_syntax/prepared_statements.md %}) 的元数据信息。

| 列 | 描述 | 类型 |
|:-|:---|:-|
| `name` | 预编译语句的名称。 | `VARCHAR` |
| `statement` | SQL 语句。 | `VARCHAR` |
| `parameter_types` | 语句参数的预期类型。目前对所有参数返回 `UNKNOWN`。 | `VARCHAR[]` |
| `result_types` | 预编译语句返回的表的列类型。 | `VARCHAR[]` |

## `duckdb_schemas`

`duckdb_schemas()` 函数提供了 DuckDB 实例中可用模式的元数据信息。

| 列 | 描述 | 类型 |
|:-|:---|:-|
| `oid` | 模式对象的内部标识符。 | `BIGINT` |
| `database_name` | 包含此模式的数据库名称。 | `VARCHAR` |
| `database_oid` | 包含模式的数据库的内部标识符。 | `BIGINT` |
| `schema_name` | 模式的 SQL 名称。 | `VARCHAR` |
| `comment` | 由 [`COMMENT ON` 语句]({% link docs/stable/sql/statements/comment_on.md %}) 创建的注释。 | `VARCHAR` |
| `tags` | 字符串键值对的映射。 | `MAP(VARCHAR, VARCHAR)` |
| `internal` | 如果是内部（内置）模式，则为 `true`；如果是用户定义的模式，则为 `false`。 | `BOOLEAN` |
| `sql` | 始终为 `NULL` | `VARCHAR` |

`information_schema.schemata` 系统视图提供了获取数据库模式元数据的更标准化方式。

## `duckdb_secret_types`

`duckdb_secret_types()` 列出了当前 DuckDB 会话中支持的密钥类型。

| 列 | 描述 | 类型 |
|:-|:---|:-|
| `type` | 密钥类型的名称，例如 `s3`。 | `VARCHAR` |
| `default_provider` | 默认的密钥提供者，例如 `config`。 | `VARCHAR` |
| `extension` | 注册该密钥类型的扩展，例如 `aws`。 | `VARCHAR` |

## `duckdb_secrets`

`duckdb_secrets()` 函数提供了 DuckDB 实例中可用密钥的元数据信息。

| 列 | 描述 | 类型 |
|:-|:---|:-|
| `name` | 密钥的名称。 | `VARCHAR` |
| `type` | 密钥的类型，例如 `S3`、`GCS`、`R2`、`AZURE`。 | `VARCHAR` |
| `provider` | 密钥的提供者。 | `VARCHAR` |
| `persistent` | 表示密钥是否持久化。 | `BOOLEAN` |
| `storage` | 存储密钥的后端。 | `VARCHAR` |
| `scope` | 密钥的作用域。 | `VARCHAR[]` |
| `secret_string` | 返回密钥的内容作为字符串。敏感信息（例如访问密钥）会被隐藏。 | `VARCHAR` |

## `duckdb_sequences`

`duckdb_sequences()` 函数提供了 DuckDB 实例中可用序列的元数据信息。

| 列 | 描述 | 类型 |
|:-|:---|:-|
| `database_name` | 包含此序列的数据库名称 | `VARCHAR` |
| `database_oid` | 包含序列的数据库的内部标识符。 | `BIGINT` |
| `schema_name` | 包含序列对象的模式的 SQL 名称。 | `VARCHAR` |
| `schema_oid` | 包含序列对象的模式对象的内部标识符。 | `BIGINT` |
| `sequence_name` | 在模式中标识序列的 SQL 名称。 | `VARCHAR` |
| `sequence_oid` | 该序列对象的内部标识符。 | `BIGINT` |
| `comment` | 由 [`COMMENT ON` 语句]({% link docs/stable/sql/statements/comment_on.md %}) 创建的注释。 | `VARCHAR` |
| `tags` | 字符串键值对的映射。 | `MAP(VARCHAR, VARCHAR)` |
| `temporary` | 该序列是否为临时序列。临时序列是临时的，仅在当前连接中可见。 | `BOOLEAN` |
| `start_value` | 序列的初始值。当首次调用 `nextval()` 时，将返回此值。 | `BIGINT` |
| `min_value` | 序列的最小值。 | `BIGINT` |

| `max_value` | 序列的最大值。 | `BIGINT` |
| `increment_by` | 从序列中获取下一个值时，添加到当前值的值。 | `BIGINT` |
| `cycle` | 如果序列在获取下一个值时超出范围，是否重新开始。 | `BOOLEAN` |
| `last_value` | 如果从未从序列中使用 `nextval(...)` 获取值，则为 `NULL`；如果曾经获取过值，则为 `1`。 | `BIGINT` |
| `sql` | 该对象的定义，以 SQL DDL 语句形式表示。 | `VARCHAR` |

如 `temporary`、`start_value` 等属性对应于 [`CREATE SEQUENCE`]({% link docs/stable/sql/statements/create_sequence.md %}) 语句中的各种选项，并在该语句中完整地进行了文档说明。请注意，在 `duckdb_sequences` 的结果集中，这些属性始终会被填充，即使它们在 `CREATE SEQUENCE` 语句中未显式指定。

> 1. 列名 `last_value` 建议它包含从序列中获取的最后一个值，但实际上并非如此。如果从未从序列中获取过值，则为 `NULL`；如果曾经获取过值，则为 `1`。
>
> 2. 如果序列循环，则序列将在其范围的边界重新开始，而不一定是从指定的起始值开始。

## `duckdb_settings`

`duckdb_settings()` 函数提供了 DuckDB 实例中可用设置的元数据信息。

| 列 | 描述 | 类型 |
|:-|:---|:-|
| `name` | 设置的名称。 | `VARCHAR` |
| `value` | 设置的当前值。 | `VARCHAR` |
| `description` | 设置的描述。 | `VARCHAR` |
| `input_type` | 设置值的逻辑数据类型。 | `VARCHAR` |
| `scope` | 设置的作用域（`LOCAL` 或 `GLOBAL`）。 | `VARCHAR` |

各种设置的描述在 [配置页面]({% link docs/stable/configuration/overview.md %}) 中。

## `duckdb_tables`

`duckdb_tables()` 函数提供了 DuckDB 实例中可用基础表的元数据信息。

| 列 | 描述 | 类型 |
|:-|:---|:-|
| `database_name` | 包含此表的数据库名称 | `VARCHAR` |
| `database_oid` | 包含表的数据库的内部标识符。 | `BIGINT` |
| `schema_name` | 包含基础表的模式的 SQL 名称。 | `VARCHAR` |
| `schema_oid` | 包含基础表的模式对象的内部标识符。 | `BIGINT` |
| `table_name` | 基础表的 SQL 名称。 | `VARCHAR` |
| `table_oid` | 基础表对象的内部标识符。 | `BIGINT` |
| `comment` | 由 [`COMMENT ON` 语句]({% link docs/stable/sql/statements/comment_on.md %}) 创建的注释。 | `VARCHAR` |
| `tags` | 字符串键值对的映射。 | `MAP(VARCHAR, VARCHAR)` |
| `internal` | 如果是用户定义的表，则为 `false`。 | `BOOLEAN` |
| `temporary` | 是否为临时表。临时表不会被持久化，仅在当前连接中可见。 | `BOOLEAN` |
| `has_primary_key` | 如果该表对象定义了 `PRIMARY KEY`，则为 `true`。 | `BOOLEAN` |
| `estimated_size` | 表的估计行数。 | `BIGINT` |
| `column_count` | 该对象定义的列数。 | `BIGINT` |
| `index_count` | 与该表关联的索引数。此数字包括所有二级索引，以及为维护 `PRIMARY KEY` 和/或 `UNIQUE` 约束而生成的内部索引。 | `BIGINT` |
| `check_constraint_count` | 该表中列上活动的检查约束数。 | `BIGINT` |
| `sql` | 该对象的定义，以 SQL [`CREATE TABLE`-statement]({% link docs/stable/sql/statements/create_table.md %}) 形式表示。 | `VARCHAR` |

`information_schema.tables` 系统视图提供了获取数据库表元数据的更标准化方式，同时也包括了视图。但 `duckdb_tables` 返回的结果集包含了一些 `information_schema.tables` 中未包含的列。

## `duckdb_temporary_files`

`duckdb_temporary_files()` 函数提供了 DuckDB 写入磁盘的临时文件的元数据信息，用于将数据从内存中卸载。此函数主要用于调试和测试目的。

| 列 | 描述 | 类型 |
|:-|:---|:-|
| `path` | 临时文件的名称。 | `VARCHAR` |
| `size` | 临时文件的大小（以字节为单位）。 | `BIGINT` |

## `duckdb_types`

`duckdb_types()` 函数提供了 DuckDB 实例中可用数据类型的元数据信息。

| 列 | 描述 | 类型 |
|:-|:---|:-|
| `database_name` | 包含此模式的数据库名称。 | `VARCHAR` |
| `database_oid` | 包含数据类型的数据库的内部标识符。 | `BIGINT` |
| `schema_name` | 包含类型定义的模式的 SQL 名称。始终为 `main`。 | `VARCHAR` |
| `schema_oid` | 模式对象的内部标识符。 | `BIGINT` |
| `type_name` | 该数据类型的名称或别名。 | `VARCHAR` |
| `type_oid` | 该数据类型对象的内部标识符。如果为 `NULL`，则表示这是该类型的别名（由 `logical_type` 列中的值标识）。 | `BIGINT` |
| `type_size` | 表示该类型在内存中所需字节数。 | `BIGINT` |
| `logical_type` | 该数据类型的“规范”名称。多个具有不同 `type_name` 的类型可能引用相同的 `logical_type`。 | `VARCHAR` |
| `type_category` | 该类型所属的类别。同一类别中的类型通常在使用该类型值时表现出相似的行为。例如，`NUMERIC` 类别包括整数、十进制数和浮点数。 | `VARCHAR` |
| `comment` | 由 [`COMMENT ON` 语句]({% link docs/stable/sql/statements/comment_on.md %}) 创建的注释。 | `VARCHAR` |
| `tags` | 字符串键值对的映射。 | `MAP(VARCHAR, VARCHAR)` |
| `internal` | 该对象是内部（内置）还是用户定义的。 | `BOOLEAN` |
| `labels` | 用于分类类型的标签。用于生成文档。 | `VARCHAR[]` |

## `duckdb_variables`

`duckdb_variables()` 函数提供了 DuckDB 实例中可用变量的元数据信息。

| 列 | 描述 | 类型 |
|:-|:---|:-|
| `name` | 变量的名称，例如 `x`。 | `VARCHAR` |
| `value` | 变量的值，例如 `12`。 | `VARCHAR` |
| `type` | 变量的类型，例如 `INTEGER`。 | `VARCHAR` |

## `duckdb_views`

`duckdb_views()` 函数提供了 DuckDB 实例中可用视图的元数据信息。

| 列 | 描述 | 类型 |
|:-|:---|:-|
| `database_name` | 包含此视图的数据库名称。 | `VARCHAR` |
| `database_oid` | 包含此视图的数据库的内部标识符。 | `BIGINT` |
| `schema_name` | 视图所在的模式的 SQL 名称。 | `VARCHAR` |
| `schema_oid` | 包含视图的模式对象的内部标识符。 | `BIGINT` |
| `view_name` | 视图对象的 SQL 名称。 | `VARCHAR` |
| `view_oid` | 此视图对象的内部标识符。 | `BIGINT` |
| `comment` | 由 [`COMMENT ON` 语句]({% link docs/stable/sql/statements/comment_on.md %}) 创建的注释。 | `VARCHAR` |
| `tags` | 字符串键值对的映射。 | `MAP(VARCHAR, VARCHAR)` |
| `internal` | 如果是内部（内置）视图，则为 `true`；如果是用户定义的视图，则为 `false`。 | `BOOLEAN` |
| `temporary` | 如果是临时视图，则为 `true`。临时视图不持久化，仅在当前连接中可见。 | `BOOLEAN` |
| `column_count` | 此视图对象定义的列数。 | `BIGINT` |
| `sql` | 该对象的定义，以 SQL DDL 语句形式表示。 | `VARCHAR` |

`information_schema.tables` 系统视图提供了获取数据库视图元数据的更标准化方式，同时也包括了基础表。但 `duckdb_views` 返回的结果集还包含内部视图对象的定义以及 `information_schema.tables` 中未包含的一些列。