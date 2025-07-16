---
---
layout: docu
redirect_from:
- /docs/sql/information_schema
- /docs/sql/information_schema/
- /docs/sql/meta/information_schema
title: Information Schema
---

`information_schema` 中的视图是符合 SQL 标准的视图，用于描述数据库的目录条目。这些视图可以被过滤以获取特定列或表的信息。
DuckDB 的实现基于 [PostgreSQL 的 information schema](https://www.postgresql.org/docs/16/infoschema-columns.html)。

## 表

### `character_sets`: 字符集

| 列 | 描述 | 类型 | 示例 |
|--------|-------------|------|---------|
| `character_set_catalog` | 目前未实现 – 始终为 `NULL`。 | `VARCHAR` | `NULL` |
| `character_set_schema` | 目前未实现 – 始终为 `NULL`。 | `VARCHAR` | `NULL` |
| `character_set_name` | 字符集名称，目前实现为显示数据库编码的名称。 | `VARCHAR` | `'UTF8'` |
| `character_repertoire` | 字符集范围，如果编码为 `UTF8`，则显示 `UCS`，否则仅显示编码名称。 | `VARCHAR` | `'UCS'` |
| `form_of_use` | 字符编码形式，与数据库编码相同。 | `VARCHAR` | `'UTF8'` |
| `default_collate_catalog` | 包含默认排序规则的数据库名称（始终是当前数据库）。 | `VARCHAR` | `'my_db'` |
| `default_collate_schema` | 包含默认排序规则的模式名称。 | `VARCHAR` | `'pg_catalog'` |
| `default_collate_name` | 默认排序规则的名称。 | `VARCHAR` | `'ucs_basic'` |

### `columns`: 列

描述列目录信息的视图是 `information_schema.columns`。它列出数据库中存在的列，并具有以下布局：

| 列 | 描述 | 类型 | 示例 |
|:--|:---|:-|:-|
| `table_catalog` | 包含表的数据库名称（始终是当前数据库）。 | `VARCHAR` | `'my_db'` |
| `table_schema` | 包含表的模式名称。 | `VARCHAR` | `'main'` |
| `table_name` | 表名称。 | `VARCHAR` | `'widgets'` |
| `column_name` | 列名称。 | `VARCHAR` | `'price'` |
| `ordinal_position` | 列在表中的顺序位置（计数从 1 开始）。 | `INTEGER` | `5` |
| `column_default` | 列的默认表达式。 |`VARCHAR`| `1.99` |
| `is_nullable` | 如果列可能为 NULL，则为 `YES`，否则为 `NO`。 |`VARCHAR`| `'YES'` |
| `data_type` | 列的数据类型。 |`VARCHAR`| `'DECIMAL(18, 2)'` |
| `character_maximum_length` | 如果 `data_type` 表示字符或位字符串类型，则为声明的最大长度；对于所有其他数据类型或未声明最大长度的情况为 `NULL`。 |`INTEGER`| `255` |
| `character_octet_length` | 如果 `data_type` 表示字符类型，则为数据值的最大可能字节长度；对于所有其他数据类型为 `NULL`。最大字节长度取决于声明的字符最大长度（见上文）和字符编码。 |`INTEGER`| `1073741824` |
| `numeric_precision` | 如果 `data, type` 表示数值类型，则此列包含该列的（声明或隐式）精度。精度表示有效数字的数量。对于所有其他数据类型，此列为空。 |`INTEGER`| `18` |
| `numeric_scale` | 如果 `data_type` 表示数值类型，则此列包含该列的（声明或隐式）小数位数。精度表示有效数字的数量。对于所有其他数据类型，此列为空。 |`INTEGER`| `2` |
| `datetime_precision` | 如果 `data_type` 表示日期、时间、时间戳或间隔类型，则此列包含该列的（声明或隐式）小数秒精度，即小数点后保留的十进制位数。DuckDB 目前不支持小数秒。对于所有其他数据类型，此列为空。 |`INTEGER`| `0` |

### `constraint_column_usage`: 约束列使用

此视图描述当前数据库中所有被某些约束使用的列。对于检查约束，此视图标识用于检查表达式的列。对于非空约束，此视图标识约束定义的列。对于外键约束，此视图标识外键引用的列。对于唯一或主键约束，此视图标识被约束的列。

| 列 | 描述 | 类型 | 示例 |
|--------|-------------|------|---------|
| `table_catalog` | 包含被某些约束使用的列的表所在的数据库名称（始终是当前数据库） |`VARCHAR`| `'my_db'` |
| `table_schema` | 包含被某些约束使用的列的表所在的模式名称 |`VARCHAR`| `'main'` |
| `table_name` | 包含被某些约束使用的列的表名称 |`VARCHAR`| `'widgets'` |
| `column_name` | 被某些约束使用的列名称 |`VARCHAR`| `'price'` |
| `constraint_catalog` | 包含约束的数据库名称（始终是当前数据库） |`VARCHAR`| `'my_db'` |
| `constraint_schema` | 包含约束的模式名称 |`VARCHAR`| `'main'` |
| `constraint_name` | 约束名称 |`VARCHAR`| `'exam_id_students_id_fkey'` |

### `key_column_usage`: 键列使用

| 列 | 描述 | 类型 | 示例 |
|--------|-------------|------|---------|
| `constraint_catalog` | 包含约束的数据库名称（始终是当前数据库）。 | `VARCHAR` | `'my_db'` |
| `constraint_schema` | 包含约束的模式名称。 | `VARCHAR` | `'main'` |
| `constraint_name` | 约束名称。 | `VARCHAR` | `'exams_exam_id_fkey'` |
| `table_catalog` | 包含被此约束限制的列的表所在的数据库名称（始终是当前数据库）。 | `VARCHAR` | `'my_db'` |
| `table_schema` | 包含被此约束限制的列的表所在的模式名称。 | `VARCHAR` | `'main'` |
| `table_name` | 包含被此约束限制的列的表名称。 | `VARCHAR` | `'exams'` |
| `column_name` | 被此约束限制的列名称。 | `VARCHAR` | `'exam_id'` |
| `ordinal_position` | 列在约束键中的顺序位置（计数从 1 开始）。 | `INTEGER` | `1` |
| `position_in_unique_constraint` | 对于外键约束，引用列在其唯一约束中的顺序位置（计数从 `1` 开始）；否则为 `NULL`。 | `INTEGER` | `1` |

### `referential_constraints`: 引用约束

| 列 | 描述 | 类型 | 示例 |
|--------|-------------|------|---------|
| `constraint_catalog` | 包含约束的数据库名称（始终是当前数据库）。 | `VARCHAR` | `'my_db'` |
| `constraint_schema` | 包含约束的模式名称。 | `VARCHAR` | `main` |
| `constraint_name` | 约束名称。 | `VARCHAR` | `exam_id_students_id_fkey` |
| `unique_constraint_catalog` | 包含外键约束引用的唯一或主键约束的数据库名称。 | `VARCHAR` | `'my_db'` |
| `unique_constraint_schema` | 包含外键约束引用的唯一或主键约束的模式名称。 | `VARCHAR` | `'main'` |
| `unique_constraint_name` | 外键约束引用的唯一或主键约束的名称。 | `VARCHAR` | `'students_id_pkey'` |
| `match_option` | 外键约束的匹配选项。始终为 `NONE`。 | `VARCHAR` | `NONE` |
| `update_rule` | 外键约束的更新规则。始终为 `NO ACTION`。 | `VARCHAR` | `NO ACTION` |
| `delete_rule` | 外键约束的删除规则。始终为 `NO ACTION`。 | `VARCHAR` | `NO ACTION` |

### `schemata`: 数据库、目录和模式

顶层目录视图是 `information_schema.schemata`。它列出数据库中存在的目录和模式，并具有以下布局：

| 列 | 描述 | 类型 | 示例 |
|:--|:---|:-|:-|
| `catalog_name` | 模式所在的数据库名称。 | `VARCHAR` | `'my_db'` |
| `schema_name` | 模式名称。 | `VARCHAR` | `'main'` |
| `schema_owner` | 模式的拥有者名称。尚未实现。 | `VARCHAR` | `'duckdb'` |
| `default_character_set_catalog` | 应用于 DuckDB 中不可用的功能。 | `VARCHAR` | `NULL` |
| `default_character_set_schema` | 应用于 DuckDB 中不可用的功能。 | `VARCHAR` | `NULL` |
| `default_character_set_name` | 应用于 DuckDB 中不可用的功能。 | `VARCHAR` | `NULL` |
| `sql_path` | 应用于 DuckDB 中不可用的功能。 | `VARCHAR` | `NULL` |

### `tables`: 表和视图

描述表和视图目录信息的视图是 `information_schema.tables`。它列出数据库中存在的表，并具有以下布局：

| 列 | 描述 | 类型 | 示例 |
|:--|:---|:-|:-|
| `table_catalog` | 表或视图所属的目录。 | `VARCHAR` | `'my_db'` |
| `table_schema` | 表或视图所属的模式。 | `VARCHAR` | `'main'` |
| `table_name` | 表或视图的名称。 | `VARCHAR` | `'widgets'` |
| `table_type` | 表的类型。可选值为：`BASE TABLE`、`LOCAL TEMPORARY`、`VIEW`。 | `VARCHAR` | `'BASE TABLE'` |
| `self_referencing_column_name` | 应用于 DuckDB 中不可用的功能。 | `VARCHAR` | `NULL` |
| `reference_generation` | 应用于 DuckDB 中不可用的功能。 | `VARCHAR` | `NULL` |
| `user_defined_type_catalog` | 如果表是类型化表，此列是包含底层数据类型的数据库名称（始终是当前数据库），否则为 `NULL`。目前未实现。 | `VARCHAR` | `NULL` |
| `user_defined_type_schema` | 如果表是类型化表，此列是包含底层数据类型的模式名称，否则为 `NULL`。目前未实现。 | `VARCHAR` | `NULL` |
| `user_defined_type_name` | 如果表是类型化表，此列是底层数据类型的名称，否则为 `NULL`。目前未实现。 | `VARCHAR` | `NULL` |
| `is_insertable_into` | 如果表可以插入数据则为 `YES`，否则为 `NO`（基本表始终可以插入，视图则不一定）。| `VARCHAR` | `'YES'` |
| `is_typed` | 如果表是类型化表则为 `YES`，否则为 `NO`。 | `VARCHAR` | `'NO'` |
| `commit_action` | 尚未实现。 | `VARCHAR` | `'NO'` |

### `table_constraints`: 表约束

| 列 | 描述 | 类型 | 示例 |
|--------|-------------|------|---------|
| `constraint_catalog` | 包含约束的数据库名称（始终是当前数据库）。 | `VARCHAR` | `'my_db'` |
| `constraint_schema` | 包含约束的模式名称。 | `VARCHAR` | `'main'` |
| `constraint_name` | 约束名称。 | `VARCHAR` | `'exams_exam_id_fkey'` |
| `table_catalog` | 包含表的数据库名称（始终是当前数据库）。 | `VARCHAR` | `'my_db'` |
| `table_schema` | 包含表的模式名称。 | `VARCHAR` | `'main'` |
| `table_name` | 表名称。 | `VARCHAR` | `'exams'` |
| `constraint_type` | 约束类型：`CHECK`、`FOREIGN KEY`、`PRIMARY KEY` 或 `UNIQUE`。 | `VARCHAR` | `'FOREIGN KEY'` |
| `is_deferrable` | 如果约束可延迟，则为 `YES`，否则为 `NO`。 | `VARCHAR` | `'NO'` |
| `initially_deferred` | 如果约束可延迟且初始延迟，则为 `YES`，否则为 `NO`。 | `VARCHAR` | `'NO'` |
| `enforced` | 始终为 `YES`。 | `VARCHAR` | `'YES'` |
| `nulls_distinct` | 如果约束是唯一约束，则 `YES` 表示约束将 `NULL` 视为不同，`NO` 表示将 `NULL` 视为不不同，其他类型的约束则为 `NULL`。 | `VARCHAR` | `'YES'` |

## 目录函数

还提供了几个函数，用于查看数据库中配置的目录和模式的详细信息。

| 函数 | 描述 | 示例 | 结果 |
|:--|:---|:--|:--|
| `current_catalog()` | 返回当前活动目录的名称。默认是 memory。 | `current_catalog()` | `'memory'` |
| `current_schema()` | 返回当前活动模式的名称。默认是 main。 | `current_schema()` | `'main'` |
| `current_schemas(boolean)` | 返回模式列表。传入 `true` 参数以包含隐式模式。 | `current_schemas(true)` | `['temp', 'main', 'pg_catalog']` |