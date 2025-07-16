---
---
layout: docu
redirect_from:
- /docs/sql/pragmas
- /docs/sql/pragmas/
- /docs/configuration/pragmas
title: Pragmas
---

<!-- markdownlint-disable MD001 -->

`PRAGMA` 语句是 DUCKDB 从 SQLite 接收的 SQL 扩展。`PRAGMA` 语句可以像普通 SQL 语句一样发出。`PRAGMA` 命令可能会改变数据库引擎的内部状态，并可以影响后续的执行或行为。

`PRAGMA` 语句也可以使用 [`SET` 语句]({% link docs/stable/sql/statements/set.md %}) 来设置选项的值，并且可以使用 `SELECT current_setting(option_name)` 来检索选项的值。

有关 DUCKDB 内置的配置选项，请参阅 [配置参考]({% link docs/stable/configuration/overview.md %}#configuration-reference)。
DUCKDB [扩展]({% link docs/stable/core_extensions/overview.md %}) 可以注册额外的配置选项。
这些在各自扩展的文档页面中进行了说明。

本页面包含支持的 `PRAGMA` 设置。

## 元数据

#### 架构信息

列出所有数据库：

```sql
PRAGMA database_list;
```

列出所有表：

```sql
PRAGMA show_tables;
```

列出所有表，并带有额外信息，类似于 [`DESCRIBE`]({% link docs/stable/guides/meta/describe.md %})：

```sql
PRAGMA show_tables_expanded;
```

列出所有函数：

```sql
PRAGMA functions;
```

对于查询非存在的架构，DUCKDB 会生成“你可能是指...”风格的错误信息。
当有数千个附加的数据库时，这些错误可能需要很长时间才能生成。
为了限制 DUCKDB 搜索的架构数量，使用 `catalog_error_max_schemas` 选项：

```sql
SET catalog_error_max_schemas = 10;
```

#### 表信息

获取特定表的信息：

```sql
PRAGMA table_info('table_name');
CALL pragma_table_info('table_name');
```

`table_info` 返回名为 `table_name` 的表的列信息。返回的表的精确格式如下所示：

```sql
cid INTEGER,        -- 列的 cid
name VARCHAR,       -- 列的名称
type VARCHAR,       -- 列的类型
notnull BOOLEAN,    -- 列是否被标记为 NOT NULL
dflt_value VARCHAR, -- 列的默认值，如果没有指定则为 NULL
pk BOOLEAN          -- 是否是主键的一部分
```

#### 数据库大小

获取每个数据库的文件和内存大小：

```sql
PRAGMA database_size;
CALL pragma_database_size();
```

`database_size` 返回每个数据库的文件和内存大小信息。返回结果的列类型如下所示：

```sql
database_name VARCHAR, -- 数据库名称
database_size VARCHAR, -- 总块数乘以块大小
block_size BIGINT,     -- 数据库块大小
total_blocks BIGINT,   -- 数据库中的总块数
used_blocks BIGINT,    -- 数据库中已使用的块数
free_blocks BIGINT,    -- 数据库中空闲的块数
wal_size VARCHAR,      -- 写前日志大小
memory_usage VARCHAR,  -- 数据库缓冲管理器使用的内存
memory_limit VARCHAR   -- 数据库允许的最大内存
```

#### 存储信息

获取存储信息：

```sql
PRAGMA storage_info('table_name');
CALL pragma_storage_info('table_name');
```

此调用返回指定表的以下信息：

| 名称           | 类型      | 描述                                           |
|----------------|-----------|-------------------------------------------------|
| `row_group_id` | `BIGINT`  |                                                                                                                                                    |
| `column_name`  | `VARCHAR` |                                                                                                                                                    |
| `column_id`    | `BIGINT`  |                                                                                                                                                    |
| `column_path`  | `VARCHAR` |                                                                                                                                                    |
| `segment_id`   | `BIGINT`  |                                                                                                                                                    |
| `segment_type` | `VARCHAR` |                                                                                                                                                    |
| `start`        | `BIGINT`  | 该块的起始行 ID                                                                                                                     |
| `count`        | `BIGINT`  | 该存储块中的条目数量                                                                                                        |
| `compression`  | `VARCHAR` | 该列使用的压缩类型 – 详见 [“DUCKDB 中的轻量级压缩”博客文章]({% post_url 2022-10-28-lightweight-compression %}) |
| `stats`        | `VARCHAR` |                                                                                                                                                    |
| `has_updates`  | `BOOLEAN` |                                                                                                                                                    |
| `persistent`   | `BOOLEAN` | 如果是临时表则为 `false`                                                                                                                         |
| `block_id`     | `BIGINT`  | 除非是持久的，否则为空                                                                                                                            |
| `block_offset` | `BIGINT`  | 除非是持久的，否则为空                                                                                                                            |

更多信息请参见 [存储]({% link docs/stable/internals/storage.md %}).

#### 显示数据库

以下语句等同于 [`SHOW DATABASES` 语句]({% link docs/stable/sql/statements/attach.md %})：

```sql
PRAGMA show_databases;
```

## 资源管理

#### 内存限制

设置缓冲管理器的内存限制：

```sql
SET memory_limit = '1GB';
```

> 警告 指定的内存限制仅适用于缓冲管理器。
> 对于大多数查询，缓冲管理器处理了大部分处理的数据。
> 但是，某些内存数据结构如 [向量]({% link docs/stable/internals/vector.md %}) 和查询结果是在缓冲管理器之外分配的。
> 此外，具有复杂状态的 [聚合函数]({% link docs/stable/sql/functions/aggregates.md %})（例如 `list`、`mode`、`quantile`、`string_agg` 和 `approx` 函数）使用缓冲管理器之外的内存。
> 因此，实际内存使用量可能高于指定的内存限制。

#### 线程

设置并行查询执行的线程数量：

```sql
SET threads = 4;
```

## 排序

列出所有可用的排序规则：

```sql
PRAGMA collations;
```

将默认排序规则设置为可用的排序规则之一：

```sql
SET default_collation = 'nocase';
```

## NULL 的默认排序方式

将 NULL 的默认排序方式设置为 `NULLS_FIRST`、`NULLS_LAST`、`NULLS_FIRST_ON_ASC_LAST_ON_DESC` 或 `NULLS_LAST_ON_ASC_FIRST_ON_DESC`：

```sql
SET default_null_order = 'NULLS_FIRST';
SET default_null_order = 'NULLS_LAST_ON_ASC_FIRST_ON_DESC';
```

将默认结果集排序方向设置为 `ASCENDING` 或 `DESCENDING`：

```sql
SET default_order = 'ASCENDING';
SET default_order = 'DESCENDING';
```

## 按非整数字面量排序

默认情况下，不允许按非整数字面量排序：

```sql
SELECT 42 ORDER BY 'hello world';
```

```console
-- 绑定错误：按非整数字面量排序没有效果。
```

要允许这种行为，请使用 `order_by_non_integer_literal` 选项：

```sql
SET order_by_non_integer_literal = true;
```

## 隐式转换到 VARCHAR

在版本 0.10.0 之前，DUCKDB 会在函数绑定期间自动允许任何类型隐式转换为 `VARCHAR`。因此，可以无需显式转换即可计算整数的子字符串。从版本 v0.10.0 开始，需要显式转换。要恢复到执行隐式转换的旧行为，请将 `old_implicit_casting` 变量设置为 `true`：

```sql
SET old_implicit_casting = true;
```

## Python：扫描所有 DataFrame

在版本 1.1.0 之前，DUCKDB 的 [替换扫描机制]({% link docs/stable/clients/c/replacement_scans.md %}) 在 Python 中扫描全局 Python 命名空间。要恢复到这种旧行为，请使用以下设置：

```sql
SET python_scan_all_frames = true;
```

## DUCKDB 信息

#### 版本

显示 DUCKDB 版本：

```sql
PRAGMA version;
CALL pragma_version();
```

#### 平台

`platform` 返回当前 DUCKDB 可执行文件编译的平台标识符，例如 `osx_arm64`。
此标识符的格式与 [扩展加载说明]({% link docs/stable/extensions/extension_distribution.md %}#platforms) 中描述的平台名称格式匹配：

```sql
PRAGMA platform;
CALL pragma_platform();
```

#### 用户代理

以下语句返回用户代理信息，例如 `duckdb/v0.10.0(osx_arm64)`：

```sql
PRAGMA user_agent;
```

#### 元数据信息

以下语句返回有关元数据存储的信息（`block_id`、`total_blocks`、`free_blocks` 和 `free_list`）：

```sql
PRAGMA metadata_info;
```

## 进度条

运行查询时显示进度条：

```sql
PRAGMA enable_progress_bar;
```

或：

```sql
PRAGMA enable_print_progress_bar;
```

不显示运行查询的进度条：

```sql
PRAGMA disable_progress_bar;
```

或：

```sql
PRAGMA disable_print_progress
```

## EXPLAIN 输出

`EXPLAIN` 的输出可以配置为仅显示物理计划。

`EXPLAIN` 的默认配置：

```sql
SET explain_output = 'physical_only';
```

仅显示优化后的查询计划：

```sql
SET explain_output = 'optimized_only';
```

显示所有查询计划：

```sql
SET explain_output = 'all';
```

## 调试

### 启用调试

以下查询使用默认格式 `query_tree` 启用调试。
无论格式如何，`enable_profiling` 是 **必须的** 来启用调试。

```sql
PRAGMA enable_profiling;
PRAGMA enable_profile;
```

### 调试格式

`enable_profiling` 的格式可以指定为 `query_tree`、`json`、`query_tree_optimizer` 或 `no_output`。
除了 `no_output`，每个格式都会将其输出打印到配置的输出中。

默认格式是 `query_tree`。
它打印物理查询计划和树中每个操作符的指标。

```sql
SET enable_profiling = 'query_tree';
```

或者，`json` 返回物理查询计划作为 JSON：

```sql
SET enable_profiling = 'json';
```

> 提示 要可视化查询计划，可以考虑使用 [DUCKDB 执行计划可视化器](https://db.cs.uni-tuebingen.de/explain/)，由 [图宾根大学数据库系统研究组](https://github.com/DBatUTuebingen) 开发。

要返回包含优化器和规划器指标的物理查询计划：

```sql
SET enable_profiling = 'query_tree_optimizer';
```

数据库驱动程序和其他应用程序也可以通过 API 调用来访问调试信息，在这种情况下用户可以禁用任何其他输出。
尽管参数读取为 `no_output`，但需要注意的是，这**仅**影响打印到可配置的输出。
通过 API 调用来访问调试信息时，仍然需要启用调试：

```sql
SET enable_profiling = 'no_output';
```

### 调试输出

默认情况下，DUCKDB 将调试信息打印到标准输出。
但是，如果您希望将调试信息写入文件，可以使用 `PRAGMA` `profiling_output` 指定文件路径。

> 警告 每次发出新查询时，文件内容都会被覆盖。
> 因此，文件只会包含最后一次运行查询的调试信息：

```sql
SET profiling_output = '/path/to/file.json';
SET profile_output = '/path/to/file.json';
```

### 调试模式

默认情况下，提供有限的调试信息 (`standard`)。

```sql
SET profiling_mode = 'standard';
```

要获取更多细节，请使用 `detailed` 调试模式，将 `profiling_mode` 设置为 `detailed`。
此模式的输出包括规划器和优化器阶段的调试信息。

```sql
SET profiling_mode = 'detailed';
```

### 自定义指标

默认情况下，调试启用所有指标，除了那些由详细调试启用的。

使用 `custom_profiling_settings` `PRAGMA`，可以单独启用或禁用每个指标，包括那些来自详细调试的指标。
此 `PRAGMA` 接受一个 JSON 对象，其中包含指标名称作为键，布尔值用于切换它们的开关。
通过此 `PRAGMA` 指定的设置会覆盖默认行为。

> 注意 此仅在将 `enable_profiling` 设置为 `json` 或 `no_output` 时影响指标。
> `query_tree` 和 `query_tree_optimizer` 始终使用默认的指标集合。

在以下示例中，`CPU_TIME` 指标被禁用。
`EXTRA_INFO`、`OPERATOR_CARDINALITY` 和 `OPERATOR_TIMING` 指标被启用。

```sql
SET custom_profiling_settings = '{"CPU_TIME": "false", "EXTRA_INFO": "true", "OPERATOR_CARDINALITY": "true", "OPERATOR_TIMING": "true"}';
```

调试文档包含有关可用 [指标]({% link docs/stable/dev/profiling.md %}#metrics) 的概述。

### 禁用调试

要禁用调试：

```sql
PRAGMA disable_profiling;
PRAGMA disable_profile;
```

## 查询优化

#### 优化器

要禁用查询优化器：

```sql
PRAGMA disable_optimizer;
```

要启用查询优化器：

```sql
PRAGMA enable_optimizer;
```

#### 选择性禁用优化器

`disabled_optimizers` 选项允许选择性地禁用优化步骤。
例如，要禁用 `filter_pushdown` 和 `statistics_propagation`，请运行：

```sql
SET disabled_optimizers = 'filter_pushdown,statistics_propagation';
```

可以使用 [`duckdb_optimizers()` 表函数]({% link docs/stable/sql/meta/duckdb_table_functions.md %}#duckdb_optimizers) 查询可用的优化。

要重新启用优化器，请运行：

```sql
SET disabled_optimizers = '';
```

> 警告 `disabled_optimizers` 选项仅用于调试性能问题，并且应避免在生产环境中使用。

## 日志

设置查询日志路径：

```sql
SET log_query_path = '/tmp/duckdb_log/';
```

禁用查询日志：

```sql
SET log_query_path = '';
```

## 全文搜索索引

`create_fts_index` 和 `drop_fts_index` 选项仅在加载了 [`fts` 扩展]({% link docs/stable/core_extensions/full_text_search.md %}) 时可用。其使用方法在 [全文搜索扩展页面]({% link docs/stable/core_extensions/full_text_search.md %}) 中有文档说明。

## 验证

#### 验证外部操作符

启用外部操作符的验证：

```sql
PRAGMA verify_external;
```

禁用外部操作符的验证：

```sql
PRAGMA disable_verify_external;
```

#### 验证往返能力

启用对支持的逻辑计划的往返能力验证：

```sql
PRAGMA verify_serializer;
```

禁用往返能力验证：

```sql
PRAGMA disable_verify_serializer;
```

## 对象缓存

启用对象缓存，例如 Parquet 元数据：

```sql
PRAGMA enable_object_cache;
```

禁用对象缓存：

```sql
PRAGMA disable_object_cache;
```

## 检查点

#### 压缩

在检查点期间，现有的列数据 + 任何新更改会被压缩。
存在一些 `PRAGMA` 来影响哪些压缩函数会被考虑。

##### 强制压缩

如果可能，请优先使用此压缩方法：

```sql
PRAGMA force_compression = 'bitpacking';
```

##### 禁用压缩方法

避免使用列表中逗号分隔的压缩方法中的任何方法：

```sql
PRAGMA disabled_compression_methods = 'fsst,rle';
```

#### 强制检查点

当 [`CHECKPOINT`]({% link docs/stable/sql/statements/checkpoint.md %}) 被调用且没有更改时，强制执行检查点：

```sql
PRAGMA force_checkpoint;
```

#### 关闭时检查点

在成功关闭时运行 `CHECKPOINT` 并删除 WAL，以仅留下一个数据库文件：

```sql
PRAGMA enable_checkpoint_on_shutdown;
```

关闭时不运行 `CHECKPOINT`：

```sql
PRAGMA disable_checkpoint_on_shutdown;
```

## 将数据溢出到磁盘的临时目录

默认情况下，DUCKDB 使用一个名为 `⟨database_file_name⟩.tmp`{:.language-sql .highlight} 的临时目录来将数据溢出到磁盘，该目录与数据库文件位于同一目录中。要更改此设置，请使用：

```sql
SET temp_directory = '/path/to/temp_dir.tmp/';
```

## 返回错误为 JSON

可以将 `errors_as_json` 选项设置为以原始 JSON 格式获取错误信息。对于某些错误，会提供额外信息或分解信息，便于机器处理。例如：

```sql
SET errors_as_json = true;
```

然后，运行导致错误的查询将产生 JSON 输出：

```sql
SELECT * FROM nonexistent_tbl;
```

```json
{
   "exception_type":"Catalog",
   "exception_message":"Table with name nonexistent_tbl does not exist!\nDid you mean \"temp.information_schema.tables\"?",
   "name":"nonexistent_tbl",
   "candidates":"temp.information_schema.tables",
   "position":"14",
   "type":"Table",
   "error_subtype":"MISSING_ENTRY"
}
```

## IEEE 浮点运算语义

DUCKDB 遵循 IEEE 浮点运算语义。如果您想关闭此功能，请运行：

```sql
SET ieee_floating_point_ops = false;
```

在这种情况下，浮点除以零（例如 `1.0 / 0.0`、`0.0 / 0.0` 和 `-1.0 / 0.0`）都将返回 `NULL`。

## 查询验证（用于开发）

以下 `PRAGMA` 主要用于开发和内部测试。

启用查询验证：

```sql
PRAGMA enable_verification;
```

禁用查询验证：

```sql
PRAGMA disable_verification;
```

启用强制并行查询处理：

```sql
PRAGMA verify_parallelism;
```

禁用强制并行查询处理：

```sql
PRAGMA disable_verify_parallelism;
```

## 块大小

当将数据库持久化到磁盘时，DUCKDB 会写入一个专用文件，该文件包含存储数据的块列表。
在仅包含很少数据的文件（例如小表）的情况下，默认的 256 kB 块大小可能不理想。
因此，DUCKDB 的存储格式支持不同的块大小。

可能的块大小值有一些限制。

* 必须是 2 的幂。
* 必须大于或等于 16384（16 kB）。
* 必须小于或等于 262144（256 kB）。

您可以设置实例创建的所有新 DUCKDB 文件的默认块大小，如下所示：

```sql
SET default_block_size = '16384';
```

您也可以在文件级别设置块大小，请参见 [`ATTACH`]({% link docs/stable/sql/statements/attach.md %}) 以获取详细信息。