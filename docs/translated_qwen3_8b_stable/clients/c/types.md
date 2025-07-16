---
layout: docu
redirect_from:
- /docs/api/c/types
- /docs/api/c/types/
- /docs/clients/c/types
title: 类型
---

DuckDB 是一个强类型数据库系统。因此，每个列都有一个指定的单一类型。该类型在整个列中保持不变。也就是说，被标记为 `INTEGER` 列的列只会包含 `INTEGER` 值。

DuckDB 还支持复合类型的列。例如，可以定义一个整数数组 (`INTEGER[]`)。也可以定义任意结构类型的类型 (`ROW(i INTEGER, j VARCHAR)`）。因此，原生的 DuckDB 类型对象不仅仅是枚举，而是一个可以嵌套的类。

在 C API 中，类型使用枚举 (`duckdb_type`) 和一个复杂类 (`duckdb_logical_type`) 来建模。对于大多数原始类型，例如整数或变长字符串，枚举就足够了。对于更复杂的类型，如列表、结构或十进制数，必须使用逻辑类型。

```c
typedef enum DUCKDB_TYPE {
  DUCKDB_TYPE_INVALID = 0,
  DUCKDB_TYPE_BOOLEAN = 1,
  DUCKDB_TYPE_TINYINT = 2,
  DUCKDB_TYPE_SMALLINT = 3,
  DUCKDB_TYPE_INTEGER = 4,
  DUCKDB_TYPE_BIGINT = 5,
  DUCKDB_TYPE_UTINYINT = 6,
  DUCKDB_TYPE_USMALLINT = 7,
  DUCKDB_TYPE_UINTEGER = 8,
  DUCKDB_TYPE_UBIGINT = 9,
  DUCKDB_TYPE_FLOAT = 10,
  DUCKDB_TYPE_DOUBLE = 11,
  DUCKDB_TYPE_TIMESTAMP = 12,
  DUCKDB_TYPE_DATE = 13,
  DUCKDB_TYPE_TIME = 14,
  DUCKDB_TYPE_INTERVAL = 15,
  DUCKDB_TYPE_HUGEINT = 16,
  DUCKDB_TYPE_UHUGEINT = 32,
  DUCKDB_TYPE_VARCHAR = 17,
  DUCKDB_TYPE_BLOB = 18,
  DUCKDB_TYPE_DECIMAL = 19,
  DUCKDB_TYPE_TIMESTAMP_S = 20,
  DUCKDB_TYPE_TIMESTAMP_MS = 21,
  DUCKDB_TYPE_TIMESTAMP_NS = 22,
  DUCKDB_TYPE_ENUM = 23,
  DUCKDB_TYPE_LIST = 24,
  DUCKDB_TYPE_STRUCT = 25,
  DUCKDB_TYPE_MAP = 26,
  DUCKDB_TYPE_ARRAY = 33,
  DUCKDB_TYPE_UUID = 27,
  DUCKDB_TYPE_UNION = 28,
  DUCKDB_TYPE_BIT = 29,
  DUCKDB_TYPE_TIME_TZ = 30,
  DUCKDB_TYPE_TIMESTAMP_TZ = 31,
} duckdb_type;
```

## 函数

可以使用 `duckdb_column_type` 函数来获取结果列的枚举类型。可以使用 `duckdb_column_logical_type` 函数来获取列的逻辑类型。

### `duckdb_value`

`duckdb_value` 函数会自动进行类型转换。例如，使用 `duckdb_value_double` 函数处理 `duckdb_value_int32` 类型的列是没有问题的。值会被自动转换并返回为双精度浮点数。需要注意的是，在某些情况下类型转换可能会失败。例如，当请求 `duckdb_value_int8` 但值无法适应 `int8` 时。在这种情况下，将返回默认值（通常是 `0` 或 `nullptr`）。如果对应值为 `NULL`，也会返回相同的默认值。

可以使用 `duckdb_value_is_null` 函数来检查特定值是否为 `NULL`。

`duckdb_value_varchar_internal` 函数是唯一不进行自动类型转换的例外。该函数仅适用于 `VARCHAR` 列。该函数存在的原因在于结果不需要被释放。

> `duckdb_value_varchar` 和 `duckdb_value_blob` 需要使用 `duckdb_free` 来释放结果。

### `duckdb_fetch_chunk`

`duckdb_fetch_chunk` 函数可以用于从 DuckDB 结果集中读取数据块，是使用 C API 从 DuckDB 结果集中读取数据最有效的方式。它也是读取某些类型数据的唯一方式。例如，`duckdb_value` 函数不支持复合类型（列表或结构）或更复杂的类型（如枚举和十进制数）的结构化读取。

有关数据块的更多信息，请参阅 [数据块文档]({% link docs/stable/clients/c/data_chunk.md %}).

## API 参考概述

<!-- 本部分由 scripts/generate_c_api_docs.py 脚本生成 -->

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_data_chunk</span> <a href="#duckdb_result_get_chunk"><span class="nf">duckdb_result_get_chunk</span></a>(<span class="kt">duckdb_result</span> <span class="nv">result</span>, <span class="kt">idx_t</span> <span class="nv">chunk_index</span>);
<span class="kt">bool</span> <a href="#duckdb_result_is_streaming"><span class="nf">duckdb_result_is_streaming</span></a>(<span class="kt">duckdb_result</span> <span class="nv">result</span>);
<span class="kt">idx_t</span> <a href="#duckdb_result_chunk_count"><span class="nf">duckdb_result_chunk_count</span></a>(<span class="kt">duckdb_result</span> <span class="nv">result</span>);
<span class="kt">duckdb_result_type</span> <a href="#duckdb_result_return_type"><span class="nf">duckdb_result_return_type</span></a>(<span class="kt">duckdb_result</span> <span class="nv">result</span>);
</code></pre></div></div>

### 日期时间时间戳辅助函数

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_date_struct</span> <a href="#duckdb_from_date"><span class="nf">duckdb_from_date</span></a>(<span class="kt">duckdb_date</span> <span class="nv">date</span>);
<span class="kt">duckdb_date</span> <a href="#duckdb_to_date"><span class="nf">duckdb_to_date</span></a>(<span class="kt">duckdb_date_struct</span> <span class="nv">date</span>);
<span class="kt">bool</span> <a href="#duckdb_is_finite_date"><span class="nf">duckdb_is_finite_date</span></a>(<span class="kt">duckdb_date</span> <span class="nv">date</span>);
<span class="kt">duckdb_time_struct</span> <a href="#duckdb_from_time"><span class="nf">duckdb_from_time</span></a>(<span class="kt">duckdb_time</span> <span class="nv">time</span>);
<span class="kt">duckdb_time_tz</span> <a href="#duckdb_create_time_tz"><span class="nf">duckdb_create_time_tz</span></a>(<span class="kt">int64_t</span> <span class="nv">micros</span>, <span class="kt">int32_t</span> <span class="nv">offset</span>);
<span class="kt">duckdb_time_tz_struct</span> <a href="#duckdb_from_time_tz"><span class="nf">duckdb_from_time_tz</span></a>(<span class="kt">duckdb_time_tz</span> <span class="nv">micros</span>);
<span class="kt">duckdb_time</span> <a href="#duckdb_to_time"><span class="nf">duckdb_to_time</span></a>(<span class="kt">duckdb_time_struct</span> <span class="nv">time</span>);
<span class="kt">duckdb_timestamp_struct</span> <a href="#duckdb_from_timestamp"><span class="nf">duckdb_from_timestamp</span></a>(<span class="kt">duckdb_timestamp</span> <span class="nv">ts</span>);
<span class="kt">duckdb_timestamp</span> <a href="#duckdb_to_timestamp"><span class="nf">duckdb_to_timestamp</span></a>(<span class="kt">duckdb_timestamp_struct</span> <span class="nv">ts</span>);
<span class="kt">bool</span> <a href="#duckdb_is_finite_timestamp"><span class="nf">duckdb_is_finite_timestamp</span></a>(<span class="kt">duckdb_timestamp</span> <span class="nv">ts</span>);
<span class="kt">bool</span> <a href="#duckdb_is_finite_timestamp_s"><span class="nf">duckdb_is_finite_timestamp_s</span></a>(<span class="nv">duckdb_timestamp_s</span> <span class="nv">ts</span>);
<span class="kt">bool</span> <a href="#duckdb_is_finite_timestamp_ms"><span class="nf">duckdb_is_finite_timestamp_ms</span></a>(<span class="nv">duckdb_timestamp_ms</span> <span class="nv">ts</span>);
<span class="kt">bool</span> <a href="#duckdb_is_finite_timestamp_ns"><span class="nf">duckdb_is_finite_timestamp_ns</span></a>(<span class="nv">duckdb_timestamp_ns</span> <span class="nv">ts</span>);
</code></pre></div></div>

### 巨大整数辅助函数

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">double</span> <a href="#duckdb_hugeint_to_double"><span class="nf">duckdb_hugeint_to_double</span></a>(<span class="kt">duckdb_hugeint</span> <span class="nv">val</span>);
<span class="kt">duckdb_hugeint</span> <a href="#duckdb_double_to_hugeint"><span class="nf">duckdb_double_to_hugeint</span></a>(<span class="kt">double</span> <span class="nv">val</span>);
</code></pre></div></div>

### 十进制辅助函数

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_decimal</span> <a href="#duckdb_double_to_decimal"><span class="nf">duckdb_double_to_decimal</span></a>(<span class="kt">double</span> <span class="nv">val</span>, <span class="kt">uint8_t</span> <span class="nv">width</span>, <span class="kt">uint8_t</span> <span class="nv">scale</span>);
<span class="kt">double</span> <a href="#duckdb_decimal_to_double"><span class="nf">duckdb_decimal_to_double</span></a>(<span class="kt">duckdb_decimal</span> <span class="nv">val</span>);
</code></pre></div></div>

### 逻辑类型接口

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_logical_type</span> <a href="#duckdb_create_logical_type"><span class="nf">duckdb_create_logical_type</span></a>(<span class="kt">duckdb_type</span> <span class="nv">type</span>);
<span class="kt">char</span> *<a href="#duckdb_logical_type_get_alias"><span class="nf">duckdb_logical_type_get_alias</span></a>(<span class="kt">duckdb_logical_type</span> <span class="nv">type</span>);
<span class="kt">void</span> <a href="#duckdb_logical_type_set_alias"><span class="nf">duckdb_logical_type_set_alias</span></a>(<span class="kt">duckdb_logical_type</span> <span class="nv">type</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">alias</span>);
<span class="kt">duckdb_logical_type</span> <a href="#duckdb_create_list_type"><span class="nf">duckdb_create_list_type</span></a>(<span class="kt">duckdb_logical_type</span> <span class="nv">type</span>);
<span class="kt">duckdb_logical_type</span> <a href="#duckdb_create_array_type"><span class="nf">duckdb_create_array_type</span></a>(<span class="kt">duckdb_logical_type</span> <span class="nv">type</span>, <span class="kt">idx_t</span> <span class="nv">array_size</span>);
<span class="kt">duckdb_logical_type</span> <a href="#duckdb_create_map_type"><span class="nf">duckdb_create_map_type</span></a>(<span class="kt">duckdb_logical_type</span> <span class="nv">key_type</span>, <span class="kt">duckdb_logical_type</span> <span class="nv">value_type</span>);
<span class="kt">duckdb_logical_type</span> <a href="#duckdb_create_union_type"><span class="nf">duckdb_create_union_type</span></a>(<span class="kt">duckdb_logical_type</span> *<span class="nv">member_types</span>, <span class="kt">const</span> <span class="kt">char</span> **<span class="nv">member_names</span>, <span class="kt">idx_t</span> <span class="nv">member_count</span>);
<span class="kt">duckdb_logical_type</span> <a href="#duckdb_create_struct_type"><span class="nf">duckdb_create_struct_type</span></a>(<span class="kt">duckdb_logical_type</span> *<span class="nv">member_types</span>, <span class="kt">const</span> <span class="kt">char</span> **<span class="nv">member_names</span>, <span class="kt">idx_t</span> <span class="nv">member_count</span>);
<span class="kt">duckdb_logical_type</span> <a href="#duckdb_create_enum_type"><span class="nf">duckdb_create_enum_type</span></a>(<span class="kt">const</span> <span class="kt">char</span> **<span class="nv">member_names</span>, <span class="kt">idx_t</span> <span class="nv">member_count</span>);
<span class="kt">duckdb_logical_type</span> <a href="#duckdb_create_decimal_type"><span class="nf">duckdb_create_decimal_type</span></a>(<span class="kt">uint8_t</span> <span class="nv">width</span>, <span class="kt">uint8_t</span> <span class="nv">scale</span>);
<span class="kt">duckdb_type</span> <a href="#duckdb_get_type_id"><span class="nf">duckdb_get_type_id</span></a>(<span class="kt">duckdb_logical_type</span> <span class="nv">type</span>);
<span class="kt">uint8_t</span> <a href="#duckdb_decimal_width"><span class="nf">duckdb_decimal_width</span></a>(<span class="kt">duckdb_logical_type</span> <span class="nv">type</span>);
<span class="kt">uint8_t</span> <a href="#duckdb_decimal_scale"><span class="nf">duckdb_decimal_scale</span></a>(<span class="kt">duckdb_logical_type</span> <span class="nv">type</span>);
<span class="kt">duckdb_type</span> <a href="#duckdb_decimal_internal_type"><span class="nf">duckdb_decimal_internal_type</span></a>(<span class="kt">duckdb_logical_type</span> <span class="nv">type</span>);
<span class="kt">duckdb_type</span> <a href="#duckdb_enum_internal_type"><span class="nf">duckdb_enum_internal_type</span></a>(<span class="kt">duckdb_logical_type</span> <span class="nv">type</span>);
<span class="kt">uint32_t</span> <a href="#duckdb_enum_dictionary_size"><span class="nf">duckdb_enum_dictionary_size</span></a>(<span class="kt">duckdb_logical_type</span> <span class="nv">type</span>);
<span class="kt">char</span> *<a href="#duckdb_enum_dictionary_value"><span class="nf">duckdb_enum_dictionary_value</span></a>(<span class="kt">duckdb_logical_type</span> <span class="nv">type</span>, <span class="kt">idx_t</span> <span class="nv">index</span>);
<span class="kt">duckdb_logical_type</span> <a href="#duckdb_list_type_child_type"><span class="nf">duckdb_list_type_child_type</span></a>(<span class="kt">duckdb_logical_type</span> <span class="nv">type</span>);
<span class="kt">duckdb_logical_type</span> <a href="#duckdb_array_type_child_type"><span class="nf">duckdb_array_type_child_type</span></a>(<span class="kt">duckdb_logical_type</span> <span class="nv">type</span>);
<span class="kt">idx_t</span> <a href="#duckdb_array_type_array_size"><span class="nf">duckdb_array_type_array_size</span></a>(<span class="kt">duckdb_logical_type</span> <span class="nv">type</span>);
<span class="kt">duckdb_logical_type</span> <a href="#duckdb_map_type_key_type"><span class="nf">duckdb_map_type_key_type</span></a>(<span class="kt">duckdb_logical_type</span> <span class="nv">type</span>);
<span class="kt">duckdb_logical_type</span> <a href="#duckdb_map_type_value_type"><span class="nf">duckdb_map_type_value_type</span></a>(<span class="kt">duckdb_logical_type</span> <span class="nv">type</span>);
<span class="kt">idx_t</span> <a href="#duckdb_struct_type_child_count"><span class="nf">duckdb_struct_type_child_count</span></a>(<span class="kt">duckdb_logical_type</span> <span class="nv">type</span>);
<span class="kt">char</span> *<a href="#duckdb_struct_type_child_name"><span class="nf">duckdb_struct_type_child_name</span></a>(<span class="kt">duckdb_logical_type</span> <span class="nv">type</span>, <span class="kt">idx_t</span> <span class="nv">index</span>);
<span class="kt">duckdb_logical_type</span> <a href="#duckdb_struct_type_child_type"><span class="nf">duckdb_struct_type_child_type</span></a>(<span class="kt">duckdb_logical_type</span> <span class="nv">type</span>, <span class="kt">idx_t</span> <span class="nv">index</span>);
<span class="kt">idx_t</span> <a href="#duckdb_union_type_member_count"><span class="nf">duckdb_union_type_member_count</span></a>(<span class="kt">duckdb_logical_type</span> <span class="nv">type</span>);
<span class="kt">char</span> *<a href="#duckdb_union_type_member_name"><span class="nf">duckdb_union_type_member_name</span></a>(<span class="kt">duckdb_logical_type</span> <span class="nv">type</span>, <span class="kt">idx_t</span> <span class="nv">index</span>);
<span class="kt">duckdb_logical_type</span> <a href="#duckdb_union_type_member_type"><span class="nf">duckdb_union_type_member_type</span></a>(<span class="kt">duckdb_logical_type</span> <span class="nv">type</span>, <span class="kt">idx_t</span> <span class="nv">index</span>);
<span class="kt">void</span> <a href="#duckdb_destroy_logical_type"><span class="nf">duckdb_destroy_logical_type</span></a>(<span class="kt">duckdb_logical_type</span> *<span class="nv">type</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_register_logical_type"><span class="nf">duckdb_register_logical_type</span></a>(<span class="kt">duckdb_connection</span> <span class="nv">con</span>, <span class="kt">duckdb_logical_type</span> <span class="nv">type</span>, <span class="nv">duckdb_create_type_info</span> <span class="nv">info</span>);
</code></pre></div></div>

#### `duckdb_result_get_chunk`

> 警告：弃用通知。此方法将在未来版本中被移除。

从 duckdb_result 中获取一个数据块。此函数应被重复调用，直到结果被完全读取。

结果必须使用 `duckdb_destroy_data_chunk` 进行销毁。

此函数取代了所有的 `duckdb_value` 函数，以及 `duckdb_column_data` 和 `duckdb_nullmask_data` 函数。它在性能上显著提升，应优先在新代码库中使用。

如果使用此函数，则不能使用其他任何结果函数，反之亦然（即，此函数不能与旧的结果函数混合使用）。

使用 `duckdb_result_chunk_count` 来确定结果中有多少个数据块。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_data_chunk</span> <span class="nv">duckdb_result_get_chunk</span>(<span class="nv">
</span>  <span class="kt">duckdb_result</span> <span class="nv">result</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">chunk_index
</span>);
</code></pre></div></div>

##### 参数

* `result`: 要从中获取数据块的结果对象。
* `chunk_index`: 要获取的数据块索引。

##### 返回值

结果数据块。如果数据块索引超出范围，则返回 `NULL`。

<br>

#### `duckdb_result_is_streaming`

> 警告：弃用通知。此方法将在未来版本中被移除。

检查内部结果的类型是否为 StreamQueryResult。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">bool</span> <span class="nv">duckdb_result_is_streaming</span>(<span class="nv">
</span>  <span class="kt">duckdb_result</span> <span class="nv">result
</span>);
</code></pre></div></div>

##### 参数

* `result`: 要检查的结果对象。

##### 返回值

结果对象是否为 StreamQueryResult 类型。

<br>

#### `duckdb_result_chunk_count`

> 警告：弃用通知。此方法将在未来版本中被移除。

返回结果中数据块的数量。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="nv">duckdb_result_chunk_count</span>(<span class="nv">
</span>  <span class="kt">duckdb_result</span> <span class="nv">result
</span>);
</code></pre></div></div>

##### 参数

* `result`: 结果对象

##### 返回值

结果中数据块的数量。

<br>

#### `duckdb_result_return_type`

返回给定结果的返回类型，或在出错时返回 DUCKDB_RETURN_TYPE_INVALID

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_result_type</span> <span class="nv">duckdb_result_return_type</span>(<span class="nv">
</span>  <span class="kt">duckdb_result</span> <span class="nv">result
</span>);
</code></pre></div></div>

##### 参数

* `result`: 结果对象

##### 返回值

返回类型

<br>

#### `duckdb_from_date`

将 `duckdb_date` 对象分解为年、月和日（存储为 `duckdb_date_struct`）。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_date_struct</span> <span class="nv">duckdb_from_date</span>(<span class="nv">
</span>  <span class="kt">duckdb_date</span> <span class="nv">date
</span>);
</code></pre></div></div>

##### 参数

* `date`: 从 `DUCKDB_TYPE_DATE` 列中获得的日期对象。

##### 返回值

包含分解元素的 `duckdb_date_struct`。

<br>

#### `duckdb_to_date`

从年、月和日（`duckdb_date_struct`）重新组合 `duckdb_date`。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_date</span> <span class="nv">duckdb_to_date</span>(<span class="nv">
</span>  <span class="kt">duckdb_date_struct</span> <span class="nv">date
</span>);
</code></pre></div></div>

##### 参数

* `date`: 存储在 `duckdb_date_struct` 中的年、月和日。

##### 返回值

`duckdb_date` 元素。

<br>

#### `duckdb_is_finite_date`

测试 `duckdb_date` 是否为有限值。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">bool</span> <span class="nv">duckdb_is_finite_date</span>(<span class="nv">
</span>  <span class="kt">duckdb_date</span> <span class="nv">date
</span>);
</code></pre></div></div>

##### 参数

* `date`: 从 `DUCKDB_TYPE_DATE` 列中获得的日期对象。

##### 返回值

如果日期是有限值，返回 `true`，否则返回 `false`（表示 ±infinity）。

<br>

#### `duckdb_from_time`

将 `duckdb_time` 对象分解为小时、分钟、秒和微秒（存储为 `duckdb_time_struct`）。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_time_struct</span> <span class="nv">duckdb_from_time</span>(<span class="nv">
</span>  <span class="kt">duckdb_time</span> <span class="nv">time
</span>);
</code></pre></div></div>

##### 参数

* `time`: 从 `DUCKDB_TYPE_TIME` 列中获得的时间对象。

##### 返回值

包含分解元素的 `duckdb_time_struct`。

<br>

#### `duckdb_create_time_tz`

从微秒和时区偏移量创建 `duckdb_time_tz` 对象。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_time_tz</span> <span class="nv">duckdb_create_time_tz</span>(<span class="nv">
</span>  <span class="kt">int64_t</span> <span class="nv">micros</span>,<span class="nv">
</span>  <span class="kt">int32_t</span> <span class="nv">offset
</span>);
</code></pre></div></div>

##### 参数

* `micros`: 时间的微秒部分。
* `offset`: 时间的时区偏移部分。

##### 返回值

`duckdb_time_tz` 元素。

<br>

#### `duckdb_from_time_tz`

将 TIME_TZ 对象分解为微秒和时区偏移量。

使用 `duckdb_from_time` 将微秒进一步分解为小时、分钟、秒和微秒。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_time_tz_struct</span> <span class="nv">duckdb_from_time_tz</span>(<span class="nv">
</span>  <span class="kt">duckdb_time_tz</span> <span class="nv">micros
</span>);
</code></pre></div></div>

##### 参数

* `micros`: 从 `DUCKDB_TYPE_TIME_TZ` 列中获得的时间对象。

<br>

#### `duckdb_to_time`

从小时、分钟、秒和微秒（`duckdb_time_struct`）重新组合 `duckdb_time`。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_time</span> <span class="nv">duckdb_to_time</span>(<span class="nv">
</span>  <span class="kt">duckdb_time_struct</span> <span class="nv">time
</span>);
</code></pre></div></div>

##### 参数

* `time`: 存储在 `duckdb_time_struct` 中的小时、分钟、秒和微秒。

##### 返回值

`duckdb_time` 元素。

<br>

#### `duckdb_from_timestamp`

将 `duckdb_timestamp` 对象分解为 `duckdb_timestamp_struct`。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_timestamp_struct</span> <span class="nv">duckdb_from_timestamp</span>(<span class="nv">
</span>  <span class="kt">duckdb_timestamp</span> <span class="nv">ts
</span>);
</code></pre></div></div>

##### 参数

* `ts`: 从 `DUCKDB_TYPE_TIMESTAMP` 列中获得的 ts 对象。

##### 返回值

包含分解元素的 `duckdb_timestamp_struct`。

<br>

#### `duckdb_to_timestamp`

从 `duckdb_timestamp_struct` 重新组合 `duckdb_timestamp`。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_timestamp</span> <span class="nv">duckdb_to_timestamp</span>(<span class="nv">
</span>  <span class="kt">duckdb_timestamp_struct</span> <span class="nv">ts
</span>);
</code></pre></div></div>

##### 参数

* `ts`: 存储在 `duckdb_timestamp_struct` 中的分解元素。

##### 返回值

`duckdb_timestamp` 元素。

<br>

#### `duckdb_is_finite_timestamp`

测试 `duckdb_timestamp` 是否为有限值。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">bool</span> <span class="nv">duckdb_is_finite_timestamp</span>(<span class="nv">
</span>  <span class="kt">duckdb_timestamp</span> <span class="nv">ts
</span>);
</code></pre></div></div>

##### 参数

* `ts`: 从 `DUCKDB_TYPE_TIMESTAMP` 列中获得的 `duckdb_timestamp` 对象。

##### 返回值

如果时间戳是有限值，返回 `true`，否则返回 `false`（表示 ±infinity）。

<br>

#### `duckdb_is_finite_timestamp_s`

测试 `duckdb_timestamp_s` 是否为有限值。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">bool</span> <span class="nv">duckdb_is_finite_timestamp_s</span>(<span class="nv">
</span>  <span class="nv">duckdb_timestamp_s</span> <span class="nv">ts
</span>);
</code></pre></div></div>

##### 参数

* `ts`: 从 `DUCKDB_TYPE_TIMESTAMP_S` 列中获得的 `duckdb_timestamp_s` 对象。

##### 返回值

如果时间戳是有限值，返回 `true`，否则返回 `false`（表示 ±infinity）。

<br>

#### `duckdb_is_finite_timestamp_ms`

测试 `duckdb_timestamp_ms` 是否为有限值。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">bool</span> <span class="nv">duckdb_is_finite_timestamp_ms</span>(<span class="nv">
</span>  <span class="nv">duckdb_timestamp_ms</span> <span class="nv">ts
</span>);
</code></pre></div></div>

##### 参数

* `ts`: 从 `DUCKDB_TYPE_TIMESTAMP_MS` 列中获得的 `duckdb_timestamp_ms` 对象。

##### 返回值

如果时间戳是有限值，返回 `true`，否则返回 `false`（表示 ±infinity）。

<br>

#### `duckdb_is_finite_timestamp_ns`

测试 `duckdb_timestamp_ns` 是否为有限值。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">bool</span> <span class="nv">duckdb_is_finite_timestamp_ns</span>(<span class="nv">
</span>  <span class="nv">duckdb_timestamp_ns</span> <span class="nv">ts
</span>);
</code></pre></div></div>

##### 参数

* `ts`: 从 `DUCKDB_TYPE_TIMESTAMP_NS` 列中获得的 `duckdb_timestamp_ns` 对象。

##### 返回值

如果时间戳是有限值，返回 `true`，否则返回 `false`（表示 ±infinity）。

<br>

#### `duckdb_hugeint_to_double`

将 `duckdb_hugeint` 对象（从 `DUCKDB_TYPE_HUGEINT` 列中获得）转换为双精度浮点数。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">double</span> <span class="nv">duckdb_hugeint_to_double</span>(<span class="nv">
</span>  <span class="kt">duckdb_hugeint</span> <span class="nv">val
</span>);
</code></pre></div></div>

##### 参数

* `val`: 巨大整数值。

##### 返回值

转换后的 `double` 元素。

<br>

#### `duckdb_double_to_hugeint`

将双精度值转换为 `duckdb_hugeint` 对象。

如果转换失败，因为双精度值太大，结果将为 0。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_hugeint</span> <span class="nv">duckdb_double_to_hugeint</span>(<span class="nv">
</span>  <span class="kt">double</span> <span class="nv">val
</span>);
</code></pre></div></div>

##### 参数

* `val`: 双精度值。

##### 返回值

转换后的 `duckdb_hugeint` 元素。

<br>

#### `duckdb_double_to_decimal`

将双精度值转换为 `duckdb_decimal` 对象。

如果转换失败，因为双精度值太大，或者宽度/比例无效，结果将为 0。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_decimal</span> <span class="nv">duckdb_double_to_decimal</span>(<span class="nv">
</span>  <span class="kt">double</span> <span class="nv">val</span>,<span class="nv">
</span>  <span class="kt">uint8_t</span> <span class="nv">width</span>,<span class="nv">
</span>  <span class="kt">uint8_t</span> <span class="nv">scale
</span>);
</code></pre></div></div>

##### 参数

* `val`: 双精度值。

##### 返回值

转换后的 `duckdb_decimal` 元素。

<br>

#### `duckdb_decimal_to_double`

将 `duckdb_decimal` 对象（从 `DUCKDB_TYPE_DECIMAL` 列中获得）转换为双精度浮点数。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">double</span> <span class="nv">duckdb_decimal_to_double</span>(<span class="nv">
</span>  <span class="kt">duckdb_decimal</span> <span class="nv">val
</span>);
</code></pre></div></div>

##### 参数

* `val`: 十进制值。

##### 返回值

转换后的 `double` 元素。

<br>

#### `duckdb_create_logical_type`

从原始类型创建 `duckdb_logical_type`。
生成的逻辑类型必须使用 `duckdb_destroy_logical_type` 进行销毁。

如果类型是 `DUCKDB_TYPE_INVALID`、`DUCKDB_TYPE_DECIMAL`、`DUCKDB_TYPE_ENUM`、`DUCKDB_TYPE_LIST`、`DUCKDB_TYPE_STRUCT`、`DUCKDB_TYPE_MAP`、`DUCKDB_TYPE_ARRAY` 或 `DUCKDB_TYPE_UNION`，则返回无效的逻辑类型。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_logical_type</span> <span class="nv">duckdb_create_logical_type</span>(<span class="nv">
</span>  <span class="kt">duckdb_type</span> <span class="nv">type
</span>);
</code></pre></div></div>

##### 参数

* `type`: 要创建的原始类型。

##### 返回值

逻辑类型。

<br>

#### `duckdb_logical_type_get_alias`

返回 `duckdb_logical_type` 的别名（如果设置的话），否则返回 `nullptr`。
结果必须使用 `duckdb_free` 进行释放。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">char</span> *<span class="nv">duckdb_logical_type_get_alias</span>(<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> <span class="nv">type
</span>);
</code></pre></div></div>

##### 参数

* `type`: 逻辑类型

##### 返回值

别名或 `nullptr`

<br>

#### `duckdb_logical_type_set_alias`

设置 `duckdb_logical_type` 的别名。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nv">duckdb_logical_type_set_alias</span>(<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> <span class="nv">type</span>,<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">alias
</span>);
</code></pre></div></div>

##### 参数

* `type`: 逻辑类型
* `alias`: 要设置的别名

<br>

#### `duckdb_create_list_type`

从子类型创建 LIST 类型。
返回类型必须使用 `duckdb_destroy_logical_type` 进行销毁。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_logical_type</span> <span class="nv">duckdb_create_list_type</span>(<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> <span class="nv">type
</span>);
</code></pre></div></div>

##### 参数

* `type`: 列表的子类型

##### 返回值

逻辑类型。

<br>

#### `duckdb_create_array_type`

从子类型创建 ARRAY 类型。
返回类型必须使用 `duckdb_destroy_logical_type` 进行销毁。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_logical_type</span> <span class="nv">duckdb_create_array_type</span>(<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> <span class="nv">type</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">array_size
</span>);
</code></pre></div></div>

##### 参数

* `type`: 数组的子类型。
* `array_size`: 数组中的元素数量。

##### 返回值

逻辑类型。

<br>

#### `duckdb_create_map_type`

从键类型和值类型创建 MAP 类型。
返回类型必须使用 `duckdb_destroy_logical_type` 进行销毁。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_logical_type</span> <span class="nv">duckdb_create_map_type</span>(<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> <span class="nv">key_type</span>,<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> <span class="nv">value_type
</span>);
</code></pre></div></div>

##### 参数

* `key_type`: MAP 的键类型。
* `value_type`: MAP 的值类型。

##### 返回值

逻辑类型。

<br>

#### `duckdb_create_union_type`

从传入的数组创建 UNION 类型。
返回类型必须使用 `duckdb_destroy_logical_type` 进行销毁。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_logical_type</span> <span class="nv">duckdb_create_union_type</span>(<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> *<span class="nv">member_types</span>,<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> **<span class="nv">member_names</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">member_count
</span>);
</code></pre></div></div>

##### 参数

* `member_types`: 联合成员类型的数组。
* `member_names`: 联合成员名称。
* `member_count`: 联合成员数量。

##### 返回值

逻辑类型。

<br>

#### `duckdb_create_struct_type`

根据成员类型和名称创建 STRUCT 类型。
生成的类型必须使用 `duckdb_destroy_logical_type` 进行销毁。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_logical_type</span> <span class="nv">duckdb_create_struct_type</span>(<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> *<span class="nv">member_types</span>,<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> **<span class="nv">member_names</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">member_count
</span>);
</code></pre></div></div>

##### 参数

* `member_types`: 结构成员类型的数组。
* `member_names`: 结构成员名称的数组。
* `member_count`: 结构成员的数量。

##### 返回值

逻辑类型。

<br>

#### `duckdb_create_enum_type`

从传入的成员名称数组创建 ENUM 类型。
生成的类型应使用 `duckdb_destroy_logical_type` 进行销毁。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_logical_type</span> <span class="nv">duckdb_create_enum_type</span>(<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> **<span class="nv">member_names</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">member_count
</span>);
</code></pre></div></div>

##### 参数

* `member_names`: 枚举应包含的名称数组。
* `member_count`: 数组中指定的元素数量。

##### 返回值

逻辑类型。

<br>

#### `duckdb_create_decimal_type`

创建具有指定宽度和比例的 DECIMAL 类型。
生成的类型应使用 `duckdb_destroy_logical_type` 进行销毁。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_logical_type</span> <span class="nv">duckdb_create_decimal_type</span>(<span class="nv">
</span>  <span class="kt">uint8_t</span> <span class="nv">width</span>,<span class="nv">
</span>  <span class="kt">uint8_t</span> <span class="nv">scale
</span>);
</code></pre></div></div>

##### 参数

* `width`: 十进制类型的宽度
* `scale`: 十进制类型的比例

##### 返回值

逻辑类型。

<br>

#### `duckdb_get_type_id`

获取 `duckdb_logical_type` 的 `duckdb_type` 枚举。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_type</span> <span class="nv">duckdb_get_type_id</span>(<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> <span class="nv">type
</span>);
</code></pre></div></div>

##### 参数

* `type`: 逻辑类型。

##### 返回值

`duckdb_type` id。

<br>

#### `duckdb_decimal_width`

获取十进制类型的宽度。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">uint8_t</span> <span class="nv">duckdb_decimal_width</span>(<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> <span class="nv">type
</span>);
</code></pre></div></div>

##### 参数

* `type`: 逻辑类型对象

##### 返回值

十进制类型的宽度

<br>

#### `duckdb_decimal_scale`

获取十进制类型的比例。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">uint8_t</span> <span class="nv">duckdb_decimal_scale</span>(<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> <span class="nv">type
</span>);
</code></pre></div></div>

##### 参数

* `type`: 逻辑类型对象

##### 返回值

十进制类型的比例

<br>

#### `duckdb_decimal_internal_type`

获取十进制类型的内部存储类型。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_type</span> <span class="nv">duckdb_decimal_internal_type</span>(<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> <span class="nv">type
</span>);
</code></pre></div></div>

##### 参数

* `type`: 逻辑类型对象

##### 返回值

十进制类型的内部类型

<br>

#### `duckdb_enum_internal_type`

获取枚举类型的内部存储类型。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_type</span> <span class="nv">duckdb_enum_internal_type</span>(<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> <span class="nv">type
</span>);
</code></pre></div></div>

##### 参数

* `type`: 逻辑类型对象

##### 返回值

枚举类型的内部类型

<br>

#### `duckdb_enum_dictionary_size`

获取枚举类型的字典大小。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">uint32_t</span> <span class="nv">duckdb_enum_dictionary_size</span>(<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> <span class="nv">type
</span>);
</code></pre></div></div>

##### 参数

* `type`: 逻辑类型对象

##### 返回值

枚举类型的字典大小

<br>

#### `duckdb_enum_dictionary_value`

获取枚举类型中指定位置的字典值。

结果必须使用 `duckdb_free` 进行释放。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">char</span> *<span class="nv">duckdb_enum_dictionary_value</span>(<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> <span class="nv">type</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">index
</span>);
</code></pre></div></div>

##### 参数

* `type`: 逻辑类型对象
* `index`: 字典中的索引

##### 返回值

枚举类型的字符串值。必须使用 `duckdb_free` 进行释放。

<br>

#### `duckdb_list_type_child_type`

获取给定 LIST 类型的子类型。也接受 MAP 类型。
结果必须使用 `duckdb_destroy_logical_type` 进行释放。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_logical_type</span> <span class="nv">duckdb_list_type_child_type</span>(<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> <span class="nv">type
</span>);
</code></pre></div></div>

##### 参数

* `type`: 逻辑类型，可以是 LIST 或 MAP。

##### 返回值

LIST 或 MAP 类型的子类型。

<br>

#### `duckdb_array_type_child_type`

获取给定 ARRAY 类型的子类型。

结果必须使用 `duckdb_destroy_logical_type` 进行释放。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_logical_type</span> <span class="nv">duck

</span>  <span class="kt">duckdb_logical_type</span> <span class="nv">type
</span>);
</code></pre></div></div>

##### 参数

* `type`: 逻辑类型。必须为 ARRAY。

##### 返回值

ARRAY 类型的子类型。

<br>

#### `duckdb_array_type_array_size`

获取给定数组类型中的数组大小。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="nv">duckdb_array_type_array_size</span>(<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> <span class="nv">type
</span>);
</code></pre></div></div>

##### 参数

* `type`: 逻辑类型对象

##### 返回值

该数组类型值可以存储的固定元素数量。

<br>

#### `duckdb_map_type_key_type`

获取给定映射类型中的键类型。

结果必须使用 `duckdb_destroy_logical_type` 进行释放。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_logical_type</span> <span class="nv">duckdb_map_type_key_type</span>(<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> <span class="nv">type
</span>);
</code></pre></div></div>

##### 参数

* `type`: 逻辑类型对象

##### 返回值

映射类型的键类型。必须使用 `duckdb_destroy_logical_type` 进行释放。

<br>

#### `duckdb_map_type_value_type`

获取给定映射类型中的值类型。

结果必须使用 `duckdb_destroy_logical_type` 进行释放。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_logical_type</span> <span class="nv">duckdb_map_type_value_type</span>(<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> <span class="nv">type
</span>);
</code></pre></div></div>

##### 参数

* `type`: 逻辑类型对象

##### 返回值

映射类型的值类型。必须使用 `duckdb_destroy_logical_type` 进行释放。

<br>

#### `duckdb_struct_type_child_count`

返回结构类型子项的数量。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="nv">duckdb_struct_type_child_count</span>(<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> <span class="nv">type
</span>);
</code></pre></div></div>

##### 参数

* `type`: 逻辑类型对象

##### 返回值

结构类型子项的数量。

<br>

#### `duckdb_struct_type_child_name`

获取结构子项的名称。

结果必须使用 `duckdb_free` 进行释放。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">char</span> *<span class="nv">duckdb_struct_type_child_name</span>(<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> <span class="nv">type</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">index
</span>);
</code></pre></div></div>

##### 参数

* `type`: 逻辑类型对象
* `index`: 子项索引

##### 返回值

结构类型的名称。必须使用 `duckdb_free` 进行释放。

<br>

#### `duckdb_struct_type_child_type`

获取给定结构类型在指定索引处的子类型。

结果必须使用 `duckdb_destroy_logical_type` 进行释放。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_logical_type</span> <span class="nv">duckdb_struct_type_child_type</span>(<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> <span class="nv">type</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">index
</span>);
</code></pre></div></div>

##### 参数

* `type`: 逻辑类型对象
* `index`: 子项索引

##### 返回值

结构类型的子类型。必须使用 `duckdb_destroy_logical_type` 进行释放。

<br>

#### `duckdb_union_type_member_count`

返回联合类型成员的数量。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="nv">duckdb_union_type_member_count</span>(<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> <span class="nv">type
</span>);
</code></pre></div></div>

##### 参数

* `type`: 逻辑类型（联合）对象

##### 返回值

联合类型成员的数量。

<br>

#### `duckdb_union_type_member_name`

获取联合成员的名称。

结果必须使用 `duckdb_free` 进行释放。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">char</span> *<span class="nv">duckdb_union_type_member_name</span>(<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> <span class="nv">type</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">index
</span>);
</code></pre></div></div>

##### 参数

* `type`: 逻辑类型对象
* `index`: 子项索引

##### 返回值

联合成员的名称。必须使用 `duckdb_free` 进行释放。

<br>

#### `duckdb_union_type_member_type`

获取给定联合成员在指定索引处的子类型。

结果必须使用 `duckdb_destroy_logical_type` 进行释放。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_logical_type</span> <span class="nv">duckdb_union_type_member_type</span>(<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> <span class="nv">type</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">index
</span>);
</code></pre></div></div>

##### 参数

* `type`: 逻辑类型对象
* `index`: 子项索引

##### 返回值

联合成员的子类型。必须使用 `duckdb_destroy_logical_type` 进行释放。

<br>

#### `duckdb_destroy_logical_type`

销毁逻辑类型并释放为其分配的所有内存。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nv">duckdb_destroy_logical_type</span>(<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> *<span class="nv">type
</span>);
</code></pre></div></div>

##### 参数

* `type`: 要销毁的逻辑类型。

<br>

#### `duckdb_register_logical_type`

在指定的连接中注册自定义类型。
类型必须具有别名

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_register_logical_type</span>(<span class="nv">
</span>  <span class="kt">duckdb_connection</span> <span class="nv">con</span>,<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> <span class="nv">type</span>,<span class="nv">
</span>  <span class="nv">duckdb_create_type_info</span> <span class="nv">info
</span>);
</code></pre></div></div>

##### 参数

* `con`: 要使用的连接
* `type`: 要注册的自定义类型

##### 返回值

注册是否成功。