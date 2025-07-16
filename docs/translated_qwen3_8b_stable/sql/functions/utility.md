---
---
layout: docu
redirect_from:
- /docs/test/functions/utility
- /docs/test/functions/utility/
- /docs/sql/functions/utility
title: 工具函数
---

<!-- markdownlint-disable MD001 -->

## 标量工具函数

以下函数难以归类到特定的函数类型中，且具有广泛用途。

| 名称 | 描述 |
|:--|:-------|
| [`alias(column)`](#aliascolumn) | 返回列的名称。 |
| [`can_cast_implicitly(source_value, target_value)`](#can_cast_implicitlysource_value-target_value) | 是否可以将源值的类型隐式转换为目标值的类型。 |
| [`checkpoint(database)`](#checkpointdatabase) | 将 WAL 与文件同步，用于（可选）数据库，不中断事务。 |
| [`coalesce(expr, ...)`](#coalesceexpr-) | 返回第一个评估为非 `NULL` 值的表达式。接受 1 个或多个参数。每个表达式可以是列、字面值、函数结果或其他许多内容。 |
| [`constant_or_null(arg1, arg2)`](#constant_or_nullarg1-arg2) | 如果 `arg2` 是 `NULL`，返回 `NULL`。否则返回 `arg1`。 |
| [`count_if(x)`](#count_ifx) | 聚合函数；如果 `x` 是 `true` 或非零数字，行贡献 1，否则贡献 0。 |
| [`create_sort_key(parameters...)`](#create_sort_keyparameters) | 根据一组输入参数和排序限定符构造一个二进制可比较的排序键。 |
| [`current_catalog()`](#current_catalog) | 返回当前活动的目录名称。默认是 memory。 |
| [`current_database()`](#current_database) | 返回当前活动的数据库名称。 |
| [`current_query()`](#current_query) | 返回当前查询作为字符串。 |
| [`current_schema()`](#current_schema) | 返回当前活动的模式名称。默认是 main。 |
| [`current_schemas(boolean)`](#current_schemasboolean) | 返回模式列表。传递参数 `true` 以包含隐式模式。 |
| [`current_setting('setting_name')`](#current_settingsetting_name) | 返回配置设置的当前值。 |
| [`currval('sequence_name')`](#currvalsequence_name) | 返回序列的当前值。注意，`nextval` 必须至少调用一次才能调用 `currval`。 |
| [`error(message)`](#errormessage) | 抛出指定的错误 `message`。 |
| [`equi_width_bins(min, max, bincount, nice := false)`](#equi_width_binsmin-max-bincount-nice--false) | 返回将区间 `[min, max]` 分成 `bin_count` 个等大小子区间的上边界（用于例如 [`histogram`]({% link docs/stable/sql/functions/aggregates.md %}#histogramargboundaries)）。如果 `nice = true`，则可能调整 `min`、`max` 和 `bincount` 以产生更美观的结果。 |
| [`force_checkpoint(database)`](#force_checkpointdatabase) | 将 WAL 与文件同步，用于（可选）数据库，中断事务。 |
| [`gen_random_uuid()`](#gen_random_uuid) | 返回一个随机 UUID，类似于 `eeccb8c5-9943-b2bb-bb5e-222f4e14b687`。 |
| [`getenv(var)`](#getenvvar) | 返回环境变量 `var` 的值。仅在 [命令行客户端]({% link docs/stable/clients/cli/overview.md %}) 中可用。 |
| [`hash(value)`](#hashvalue) | 返回 `value` 的哈希值作为 `UBIGINT`。 |
| [`icu_sort_key(string, collator)`](#icu_sort_keystring-collator) | 用于根据特定区域设置对特殊字符进行排序的代理排序键。Collator 参数是可选的。仅在安装了 ICU 扩展时可用。 |
| [`if(a, b, c)`](#ifa-b-c) | 三元条件运算符。 |
| [`ifnull(expr, other)`](#ifnullexpr-other) | `coalesce` 的双参数版本。 |
| [`is_histogram_other_bin(arg)`](#is_histogram_other_binarg) | 当 `arg` 是 `histogram_exact` 函数中数据类型的“捕获所有元素”时返回 `true`，该元素等于 `histogram` 函数中数据类型的“最右边边界”。 |
| [`md5(string)`](#md5string) | 返回 `string` 的 MD5 哈希值作为 `VARCHAR`。 |
| [`md5_number(string)`](#md5_numberstring) | 返回 `string` 的 MD5 哈希值作为 `UHUGEINT`。 |
| [`md5_number_lower(string)`](#md5_number_lowerstring) | 返回 `string` 的 MD5 哈希值的低 64 位部分作为 `UBIGINT`。 |
| [`md5_number_upper(string)`](#md5_number_upperstring) | 返回 `string` 的 MD5 哈希值的高 6 位部分作为 `UBIGINT`。 |
| [`nextval('sequence_name')`](#nextvalsequence_name) | 返回序列的下一个值。 |
| [`nullif(a, b)`](#nullifa-b) | 如果 `a = b`，返回 `NULL`，否则返回 `a`。等同于 `CASE WHEN a = b THEN NULL ELSE a END`。 |
| [`pg_typeof(expression)`](#pg_typeofexpression) | 返回表达式结果的数据类型的名称（小写）。用于 PostgreSQL 兼容性。 |
| [`query(`*`query_string_literal`*`)`](#queryquery_string_literal) | 解析并执行定义在 *`query_string_literal`* 中的查询的表函数。仅允许字面字符串。警告：此函数允许调用任意查询，可能会更改数据库状态。 |
| [`query_table(`*`tbl_name`*`)`](#query_tabletbl_name) | 返回指定 *`tbl_name`* 表的表函数。 |
| [`query_table(`*`tbl_names`*`, [`*`by_name`*`])`](#query_tabletbl_names-by_name) | 返回指定 *`tbl_names`* 中表的联合的表函数。如果可选参数 *`by_name`* 设置为 `true`，则使用 [`UNION ALL BY NAME`]({% link docs/stable/sql/query_syntax/setops.md %}#union-all-by-name) 语义。 |
| [`read_blob(source)`](#read_blobsource) | 从 `source`（文件名、文件名列表或通配符模式）返回内容作为 `BLOB`。更多信息请参阅 [`read_blob` 指南]({% link docs/stable/guides/file_formats/read_file.md %}#read_blob)。 |
| [`read_text(source)`](#read_textsource) | 从 `source`（文件名、文件名列表或通配符模式）返回内容作为 `VARCHAR`。文件内容首先验证是否为有效的 UTF-8。如果 `read_text` 尝试读取无效 UTF-8 的文件，则会抛出错误，建议改用 `read_blob`。更多信息请参阅 [`read_text` 指南]({% link docs/stable/guides/file_formats/read_file.md %}#read_text)。 |
| [`sha1(string)`](#sha1string) | 返回 `string` 的 SHA-1 哈希值作为 `VARCHAR`。 |
| [`sha256(string)`](#sha256string) | 返回 `string` 的 SHA-256 哈希值作为 `VARCHAR`。 |
| [`stats(expression)`](#statsexpression) | 返回关于表达式的统计信息字符串。表达式可以是列、常量或 SQL 表达式。 |
| [`txid_current()`](#txid_current) | 返回当前事务的标识符，一个 `BIGINT` 值。如果当前事务尚未分配，则会分配一个新的标识符。 |
| [`typeof(expression)`](#typeofexpression) | 返回表达式结果的数据类型名称。 |
| [`uuid()`](#uuid) | 返回一个随机 UUID（UUIDv4），类似于 `eeccb8c5-9943-b2bb-bb5e-222f4e14b687`。 |
| [`uuidv4()`](#uuidv4) | 返回一个随机 UUID（UUIDv4），类似于 `eeccb8c5-9943-b2bb-bb5e-222f4e14b687`。 |
| [`uuidv7()`](#uuidv7) | 返回一个随机 UUIDv7，类似于 `81964ebe-00b1-7e1d-b0f9-43c29b6fb8f5`。 |
| [`uuid_extract_timestamp(uuidv7)`](#uuid_extract_timestampuuidv7) | 从 UUIDv7 值中提取时间戳。 |
| [`uuid_extract_version(uuid)`](#uuid_extract_versionuuid) | 提取 UUID 版本（`4` 或 `7`）。 |
| [`version()`](#version) | 返回当前活动的 DuckDB 版本，格式如下。 |

#### `alias(column)`

<div class="nostroke_table"></div>

| **描述** | 返回列的名称。 |
| **示例** | `alias(column1)` |
| **结果** | `column1` |

#### `can_cast_implicitly(source_value, target_value)`

<div class="nostroke_table"></div>

| **描述** | 是否可以将源值的类型隐式转换为目标值的类型。 |
| **示例** | `can_cast_implicitly(1::BIGINT, 1::SMALLINT)` |
| **结果** | `false` |

#### `checkpoint(database)`

<div class="nostroke_table"></div>

| **描述** | 将 WAL 与文件同步，用于（可选）数据库，不中断事务。 |
| **示例** | `checkpoint(my_db)` |
| **结果** | success Boolean |

#### `coalesce(expr, ...)`

<div class="nostroke_table"></div>

| **描述** | 返回第一个评估为非 `NULL` 值的表达式。接受 1 个或多个参数。每个表达式可以是列、字面值、函数结果或其他许多内容。 |
| **示例** | `coalesce(NULL, NULL, 'default_string')` |
| **结果** | `default_string` |

#### `constant_or_null(arg1, arg2)`

<div class="nostroke_table"></div>

| **描述** | 如果 `arg2` 是 `NULL`，返回 `NULL`。否则返回 `arg1`。 |
| **示例** | `constant_or_null(42, NULL)` |
| **结果** | `NULL` |

#### `count_if(x)`

<div class="nostroke_table"></div>

| **描述** | 聚合函数；如果 `x` 是 `true` 或非零数字，行贡献 1，否则贡献 0。 |
| **示例** | `count_if(42)` |
| **结果** | 1 |

#### `create_sort_key(parameters...)`

<div class="nostroke_table"></div>

| **描述** | 根据一组输入参数和排序限定符构造一个二进制可比较的排序键。 |
| **示例** | `create_sort_key('abc', 'ASC NULLS FIRST');` |
| **结果** | `\x02bcd\x00` |

#### `current_catalog()`

<div class="nostroke_table"></div>

| **描述** | 返回当前活动的目录名称。默认是 memory。 |
| **示例** | `current_catalog()` |
| **结果** | `memory` |

#### `current_database()`

<div class="nostroke_table"></div>

| **描述** | 返回当前活动的数据库名称。 |
| **示例** | `current_database()` |
| **结果** | `memory` |

#### `current_query()`

<div class="nostroke_table"></div>

| **描述** | 返回当前查询作为字符串。 |
| **示例** | `current_query()` |
| **结果** | `SELECT current_query();` |

#### `current_schema()`

<div class="nostroke_table"></div>

| **描述** | 返回当前活动的模式名称。默认是 main。 |
| **示例** | `current_schema()` |
| **结果** | `main` |

#### `current_schemas(boolean)`

<div class="nostroke_table"></div>

| **描述** | 返回模式列表。传递参数 `true` 以包含隐式模式。 |
| **示例** | `current_schemas(true)` |
| **结果** | `['temp', 'main', 'pg_catalog']` |

#### `current_setting('setting_name')`

<div class="nostroke_table"></div>

| **描述** | 返回配置设置的当前值。 |
| **示例** | `current_setting('access_mode')` |
| **结果** | `automatic` |

#### `currval('sequence_name')`

<div class="nostroke_table"></div>

| **描述** | 返回序列的当前值。注意，`nextval` 必须至少调用一次才能调用 `currval`。 |
| **示例** | `currval('my_sequence_name')` |
| **结果** | `1` |

#### `error(message)`

<div class="nostroke_table"></div>

| **描述** | 抛出指定的错误 `message`。 |
| **示例** | `error('access_mode')` |

#### `equi_width_bins(min, max, bincount, nice := false)`

<div class="nostroke_table"></div>

| **描述** | 返回将区间 `[min, max]` 分成 `bin_count` 个等大小子区间的上边界（用于例如 [`histogram`]({% link docs/stable/sql/functions/aggregates.md %}#histogramargboundaries)）。如果 `nice = true`，则可能调整 `min`、`max` 和 `bincount` 以产生更美观的结果。 |
| **示例** | `equi_width_bins(0.1, 2.7, 4, true)` |
| **结果** | `[0.5, 1.0, 1.5, 2.0, 2.5, 3.0]` |

#### `force_checkpoint(database)`

<div class="nostroke_table"></div>

| **描述** | 将 WAL 与文件同步，用于（可选）数据库，中断事务。 |
| **示例** | `force_checkpoint(my_db)` |
| **结果** | success Boolean |

#### `gen_random_uuid()`

<div class="nostroke_table"></div>

| **描述** | 返回一个随机 UUID（UUIDv4），类似于 `eeccb8c5-9943-b2bb-bb5e-222f4e14b687`。 |
| **示例** | `gen_random_uuid()` |
| **结果** | various |

#### `getenv(var)`

| **描述** | 返回环境变量 `var` 的值。仅在 [命令行客户端]({% link docs/stable/clients/cli/overview.md %}) 中可用。 |
| **示例** | `getenv('HOME')` |
| **结果** | `/path/to/user/home` |

#### `hash(value)`

<div class="nostroke_table"></div>

| **描述** | 返回 `value` 的哈希值作为 `UBIGINT`。 |
| **示例** | `hash('🦆')` |
| **结果** | `2595805878642663834` |

#### `icu_sort_key(string, collator)`

<div class="nostroke_table"></div>

| **描述** | 用于根据特定区域设置对特殊字符进行排序的代理排序键。Collator 参数是可选的。仅在安装了 ICU 扩展时可用。 |
| **示例** | `icu_sort_key('ö', 'DE')` |
| **结果** | `460145960106` |

#### `if(a, b, c)`

<div class="nostroke_table"></div>

| **描述** | 三元条件运算符；如果 a 为真，返回 b，否则返回 c。等同于 `CASE WHEN a THEN b ELSE c END`。 |
| **示例** | `if(2 > 1, 3, 4)` |
| **结果** | `3` |

#### `ifnull(expr, other)`

<div class="nostroke_table"></div>

| **描述** | `coalesce` 的双参数版本。 |
| **示例** | `ifnull(NULL, 'default_string')` |
| **结果** | `default_string` |

#### `is_histogram_other_bin(arg)`

<div class="nostroke_table"></div>

| **描述** | 当 `arg` 是 `histogram_exact` 函数中数据类型的“捕获所有元素”时返回 `true`，该元素等于 `histogram` 函数中数据类型的“最右边边界”。 |
| **示例** | `is_histogram_other_bin('')` |
| **结果** | `true` |

#### `md5(string)`

<div class="nostroke_table"></div>

| **描述** | 返回 `string` 的 MD5 哈希值作为 `VARCHAR`。 |
| **示例** | `md5('abc')` |
| **结果** | `900150983cd24fb0d6963f7d28e17f72` |

#### `md5_number(string)`

<div class="nostroke_table"></div>

| **描述** | 返回 `string` 的 MD5 哈希值作为 `UHUGEINT`。 |
| **示例** | `md5_number('abc')` |
| **结果** | `152195979970564155685860391459828531600` |

#### `md5_number_lower(string)`

<div class="nostroke_table"></div>

| **描述** | 返回 `string` 的 MD5 哈希值的低 8 字节作为 `UBIGINT`。 |
| **示例** | `md5_number_lower('abc')` |
| **结果** | `8250560606382298838` |

#### `md5_number_upper(string)`

<div class="nostroke_table"></div>

| **描述** | 返回 `string` 的 MD5 哈希值的高 8 字节作为 `UBIGINT`。 |
| **示例** | `md5_number_upper('abc')` |
| **结果** | `12704604231530709392` |

#### `nextval('sequence_name')`

<div class="nostroke_table"></div>

| **描述** | 返回序列的下一个值。 |
| **示例** | `nextval('my_sequence_name')` |
| **结果** | `2` |

#### `nullif(a, b)`

<div class="nostroke_table"></div>

| **描述** | 如果 a = b，返回 `NULL`，否则返回 a。等同于 `CASE WHEN a = b THEN NULL ELSE a END`。 |
| **示例** | `nullif(1+1, 2)` |
| **结果** | `NULL` |

#### `pg_typeof(expression)`

<div class="nostroke_table"></div>

| **描述** | 返回表达式结果的数据类型的名称（小写）。用于 PostgreSQL 兼容性。 |
| **示例** | `pg_typeof('abc')` |
| **结果** | `varchar` |

#### `query(query_string_literal)`

<div class="nostroke_table"></div>

| **描述** | 解析并执行定义在 `query_string_literal` 中的查询的表函数。仅允许字面字符串。警告：此函数允许调用任意查询，可能会更改数据库状态。 |
| **示例** | `query('SELECT 42 AS x')` |
| **结果** | `42` |

#### `query_table(tbl_name)`

<div class="nostroke_table"></div>

| **描述** | 返回指定 `tbl_name` 表的表函数。 |
| **示例** | `query_table('t1')` |
| **结果** | (`t1` 的行) |

#### `query_table(tbl_names, [by_name])`

<div class="nostroke_table"></div>

| **描述** | 返回指定 `tbl_names` 中表的联合的表函数。如果可选参数 `by_name` 设置为 `true`，则使用 [`UNION ALL BY NAME`]({% link docs/stable/sql/query_syntax/setops.md %}#union-all-by-name) 语义。 |
| **示例** | `query_table(['t1', 't2'])` |
| **结果** | (`t1` 和 `t2` 的联合) |

#### `read_blob(source)`

<div class="nostroke_table"></div>

| **描述** | 从 `source`（文件名、文件名列表或通配符模式）返回内容作为 `BLOB`。更多信息请参阅 [`read_blob` 指南]({% link docs/stable/guides/file_formats/read_file.md %}#read_blob)。 |
| **示例** | `read_blob('hello.bin')` |
| **结果** | `hello\x0A` |

#### `read_text(source)`

<div class="nostroke_table"></div>

| **描述** | 从 `source`（文件名、文件名列表或通配符模式）返回内容作为 `VARCHAR`。文件内容首先验证是否为有效的 UTF-8。如果 `read_text` 尝试读取无效 UTF-8 的文件，则会抛出错误，建议改用 `read_blob`。更多信息请参阅 [`read_text` 指南]({% link docs/stable/guides/file_formats/read_file.md %}#read_text)。 |
| **示例** | `read_text('hello.txt')` |
| **结果** | `hello\n` |

#### `sha1(string)`

<div class="nostroke_table"></div>

| **描述** | 返回 `string` 的 SHA-1 哈希值作为 `VARCHAR`。 |
| **示例** | `sha1('🦆')` |
| **结果** | `949bf843dc338be348fb9525d1eb535d31241d76` |

#### `sha256(string)`

<div class="nostroke_table"></div>

| **描述** | 返回 `string` 的 SHA-256 哈希值作为 `VARCHAR`。 |
| **示例** | `sha256('🦆')` |
| **结果** | `d7a5c5e0d1d94c32218539e7e47d4ba9c3c7b77d61332fb60d633dde89e473fb` |

#### `stats(expression)`

<div class="nostroke_table"></div>

| **描述** | 返回关于表达式的统计信息字符串。表达式可以是列、常量或 SQL 表达式。 |
| **示例** | `stats(5)` |
| **结果** | `'[Min: 5, Max: 5][Has Null: false]'` |

#### `txid_current()`

<div class="nostroke_table"></div>

| **描述** | 返回当前事务的标识符，一个 `BIGINT` 值。如果当前事务尚未分配，则会分配一个新的标识符。 |
| **示例** | `txid_current()` |
| **结果** | various |

#### `typeof(expression)`

<div class="nostroke_table"></div>

| **描述** | 返回表达式结果的数据类型名称。 |
| **示例** | `typeof('abc')` |
| **结果** | `VARCHAR` |

#### `uuid()`

<div class="nostroke_table"></div>

| **描述** | 返回一个随机 UUID（UUIDv4），类似于 `eeccb8c5-9943-b2bb-bb5e-222f4e14b687`。 |
| **示例** | `uuid()` |
| **结果** | various |

#### `uuidv4()`

| **描述** | 返回一个随机 UUID（UUIDv4），类似于 `eeccb8c5-9943-b2bb-bb5e-222f4e14b687`。 |
| **示例** | `uuidv4()` |
| **结果** | various |

#### `uuidv7()`

| **描述** | 返回一个随机 UUIDv7，类似于 `81964ebe-00b1-7e1d-b0f9-43c29b6fb8f5`。 |
| **示例** | `uuidv7()` |
| **结果** | various |

#### `uuid_extract_timestamp(uuidv7)`

| **描述** | 从 UUIDv7 值中提取时间戳。 |
| **示例** | `uuid_extract_timestamp(uuidv7())` |
| **结果** | `2025-04-19 15:51:20.07+00` |

#### `uuid_extract_version(uuid)`

| **描述** | 提取 UUID 版本（`4` 或 `7`）。 |
| **示例** | `uuid_extract_version(uuidv7())` |
| **结果** | `7` |

#### `version()`

<div class="nostroke_table"></div>

| **描述** | 返回当前活动的 DuckDB 版本，格式如下。 |
| **示例** | `version()` |
| **结果** | various |

## 工具表函数

表函数用于在 `FROM` 子句中替换表。

| 名称 | 描述 |
|:--|:-------|
| [`glob(search_path)`](#globsearch_path) | 返回在 *search_path* 指示的位置找到的文件名，作为单列 `file`。*search_path* 可能包含 [通配符模式匹配语法]({% link docs/stable/sql/functions/pattern_matching.md %})。 |
| [`repeat_row(varargs, num_rows)`](#repeat_rowvarargs-num_rows) | 返回一个包含 `num_rows` 行的表，每行包含 `varargs` 中定义的字段。 |

#### `glob(search_path)`

<div class="nostroke_table"></div>

| **描述** | 返回在 *search_path* 指示的位置找到的文件名，作为单列 `file`。*search
| **示例** | `glob('*')` |
| **结果** | （文件名表） |

#### `repeat_row(varargs, num_rows)`

<div class="nostroke_table"></div>

| **描述** | 返回一个包含 `num_rows` 行的表，每行包含 `varargs` 中定义的字段。 |
| **示例** | `repeat_row(1, 2, 'foo', num_rows = 3)` |
| **结果** | 3 行的 `1, 2, 'foo'` |