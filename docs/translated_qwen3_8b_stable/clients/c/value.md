---
layout: docu
redirect_from:
- /docs/api/c/value
- /docs/api/c/value/
- /docs/clients/c/value
title: 值
---

<!-- markdownlint-disable MD001 -->

值类表示任意类型的单个值。

## API 参考概述

<!-- 该部分由 scripts/generate_c_api_docs.py 生成 -->

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <a href="#duckdb_destroy_value"><span class="nf">duckdb_destroy_value</span></a>(<span class="kt">duckdb_value</span> *<span class="nv">value</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_varchar"><span class="nf">duckdb_create_varchar</span></a>(<span class="kt">const</span> <span class="kt">char</span> *<span class="nv">text</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_varchar_length"><span class="nf">duckdb_create_varchar_length</span></a>(<span class="kt">const</span> <span class="kt">char</span> *<span class="nv">text</span>, <span class="kt">idx_t</span> <span class="nv">length</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_bool"><span class="nf">duckdb_create_bool</span></a>(<span class="kt">bool</span> <span class="nv">input</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_int8"><span class="nf">duckdb_create_int8</span></a>(<span class="kt">int8_t</span> <span class="nv">input</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_uint8"><span class="nf">duckdb_create_uint8</span></a>(<span class="kt">uint8_t</span> <span class="nv">input</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_int16"><span class="nf">duckdb_create_int16</span></a>(<span class="kt">int16_t</span> <span class="nv">input</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_uint16"><span class="nf">duckdb_create_uint16</span></a>(<span class="kt">uint16_t</span> <span class="nv">input</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_int32"><span class="nf">duckdb_create_int32</span></a>(<span class="kt">int32_t</span> <span class="nv">input</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_uint32"><span class="nf">duckdb_create_uint32</span></a>(<span class="kt">uint32_t</span> <span class="nv">input</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_uint64"><span class="nf">duckdb_create_uint64</span></a>(<span class="kt">uint64_t</span> <span class="nv">input</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_int64"><span class="nf">duckdb_create_int64</span></a>(<span class="kt">int64_t</span> <span class="nv">val</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_hugeint"><span class="nf">duckdb_create_hugeint</span></a>(<span class="kt">duckdb_hugeint</span> <span class="nv">input</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_uhugeint"><span class="nf">duckdb_create_uhugeint</span></a>(<span class="kt">duckdb_uhugeint</span> <span class="nv">input</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_varint"><span class="nf">duckdb_create_varint</span></a>(<span class="nv">duckdb_varint</span> <span class="nv">input</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_decimal"><span class="nf">duckdb_create_decimal</span></a>(<span class="kt">duckdb_decimal</span> <span class="nv">input</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_float"><span class="nf">duckdb_create_float</span></a>(<span class="kt">float</span> <span class="nv">input</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_double"><span class="nf">duckdb_create_double</span></a>(<span class="kt">double</span> <span class="nv">input</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_date"><span class="nf">duckdb_create_date</span></a>(<span class="kt">duckdb_date</span> <span class="nv">input</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_time"><span class="nf">duckdb_create_time</span></a>(<span class="kt">duckdb_time</span> <span class="nv">input</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_time_tz_value"><span class="nf">duckdb_create_time_tz_value</span></a>(<span class="kt">duckdb_time_tz</span> <span class="nv">value</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_timestamp"><span class="nf">duckdb_create_timestamp</span></a>(<span class="kt">duckdb_timestamp</span> <span class="nv">input</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_timestamp_tz"><span class="nf">duckdb_create_timestamp_tz</span></a>(<span class="kt">duckdb_timestamp</span> <span class="nv">input</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_timestamp_s"><span class="nf">duckdb_create_timestamp_s</span></a>(<span class="nv">duckdb_timestamp_s</span> <span class="nv">input</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_timestamp_ms"><span class="nf">duckdb_create_timestamp_ms</span></a>(<span class="nv">duckdb_timestamp_ms</span> <span class="nv">input</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_timestamp_ns"><span class="nf">duckdb_create_timestamp_ns</span></a>(<span class="nv">duckdb_timestamp_ns</span> <span class="nv">input</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_interval"><span class="nf">duckdb_create_interval</span></a>(<span class="kt">duckdb_interval</span> <span class="nv">input</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_blob"><span class="nf">duckdb_create_blob</span></a>(<span class="kt">const</span> <span class="kt">uint8_t</span> *<span class="nv">data</span>, <span class="kt">idx_t</span> <span class="nv">length</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_bit"><span class="nf">duckdb_create_bit</span></a>(<span class="nv">duckdb_bit</span> <span class="nv">input</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_uuid"><span class="nf">duckdb_create_uuid</span></a>(<span class="kt">duckdb_uhugeint</span> <span class="nv">input</span>);
<span class="kt">bool</span> <a href="#duckdb_get_bool"><span class="nf">duckdb_get_bool</span></a>(<span class="kt">duckdb_value</span> <span class="nv">val</span>);
<span class="kt">int8_t</span> <a href="#duckdb_get_int8"><span class="nf">duckdb_get_int8</span></a>(<span class="kt">duckdb_value</span> <span class="nv">val</span>);
<span class="kt">uint8_t</span> <a href="#duckdb_get_uint8"><span class="nf">duckdb_get_uint8</span></a>(<span class="kt">duckdb_value</span> <span class="nv">val</span>);
<span class="kt">int16_t</span> <a href="#duckdb_get_int16"><span class="nf">duckdb_get_int16</span></a>(<span class="kt">duckdb_value</span> <span class="nv">val</span>);
<span class="kt">uint16_t</span> <a href="#duckdb_get_uint16"><span class="nf">duckdb_get_uint16</span></a>(<span class="kt">duckdb_value</span> <span class="nv">val</span>);
<span class="kt">int32_t</span> <a href="#duckdb_get_int32"><span class="nf">duckdb_get_int32</span></a>(<span class="kt">duckdb_value</span> <span class="nv">val</span>);
<span class="kt">uint32_t</span> <a href="#duckdb_get_uint32"><span class="nf">duckdb_get_uint32</span></a>(<span class="kt">duckdb_value</span> <span class="nv">val</span>);
<span class="kt">int64_t</span> <a href="#duckdb_get_int64"><span class="nf">duckdb_get_int64</span></a>(<span class="kt">duckdb_value</span> <span class="nv">val</span>);
<span class="kt">uint64_t</span> <a href="#duckdb_get_uint64"><span class="nf">duckdb_get_uint64</span></a>(<span class="kt">duckdb_value</span> <span class="nv">val</span>);
<span class="kt">duckdb_hugeint</span> <a href="#duckdb_get_hugeint"><span class="nf">duckdb_get_hugeint</span></a>(<span class="kt">duckdb_value</span> <span class="nv">val</span>);
<span class="kt">duckdb_uhugeint</span> <a href="#duckdb_get_uhugeint"><span class="nf">duckdb_get_uhugeint</span></a>(<span class="kt">duckdb_value</span> <span class="nv">val</span>);
<span class="nv">duckdb_varint</span> <a href="#duckdb_get_varint"><span class="nf">duckdb_get_varint</span></a>(<span class="kt">duckdb_value</span> <span class="nv">val</span>);
<span class="kt">duckdb_decimal</span> <a href="#duckdb_get_decimal"><span class="nf">duckdb_get_decimal</span></a>(<span class="kt">duckdb_value</span> <span class="nv">val</span>);
<span class="kt">float</span> <a href="#duckdb_get_float"><span class="nf">duckdb_get_float</span></a>(<span class="kt">duckdb_value</span> <span class="nv">val</span>);
<span class="kt">double</span> <a href="#duckdb_get_double"><span class="nf">duckdb_get_double</span></a>(<span class="kt">duckdb_value</span> <span class="nv">val</span>);
<span class="kt">duckdb_date</span> <a href="#duckdb_get_date"><span class="nf">duckdb_get_date</span></a>(<span class="kt">duckdb_value</span> <span class="nv">val</span>);
<span class="kt">duckdb_time</span> <a href="#duckdb_get_time"><span class="nf">duckdb_get_time</span></a>(<span class="kt">duckdb_value</span> <span class="nv">val</span>);
<span class="kt">duckdb_time_tz</span> <a href="#duckdb_get_time_tz"><span class="nf">duckdb_get_time_tz</span></a>(<span class="kt">duckdb_value</span> <span class="nv">val</span>);
<span class="kt">duckdb_timestamp</span> <a href="#duckdb_get_timestamp"><span class="nf">duckdb_get_timestamp</span></a>(<span class="kt">duckdb_value</span> <span class="nv">val</span>);
<span class="kt">duckdb_timestamp</span> <a href="#duckdb_get_timestamp_tz"><span class="nf">duckdb_get_timestamp_tz</span></a>(<span class="kt">duckdb_value</span> <span class="nv">val</span>);
<span class="nv">duckdb_timestamp_s</span> <a href="#duckdb_get_timestamp_s"><span class="nf">duckdb_get_timestamp_s</span></a>(<span class="kt">duckdb_value</span> <span class="nv">val</span>);
<span class="nv">duckdb_timestamp_ms</span> <a href="#duckdb_get_timestamp_ms"><span class="nf">duckdb_get_timestamp_ms</span></a>(<span class="kt">duckdb_value</span> <span class="nv">val</span>);
<span class="nv">duckdb_timestamp_ns</span> <a href="#duckdb_get_timestamp_ns"><span class="nf">duckdb_get_timestamp_ns</span></a>(<span class="kt">duckdb_value</span> <span class="nv">val</span>);
<span class="kt">duckdb_interval</span> <a href="#duckdb_get_interval"><span class="nf">duckdb_get_interval</span></a>(<span class="kt">duckdb_value</span> <span class="nv">val</span>);
<span class="kt">duckdb_logical_type</span> <a href="#duckdb_get_value_type"><span class="nf">duckdb_get_value_type</span></a>(<span class="kt">duckdb_value</span> <span class="nv">val</span>);
<span class="kt">duckdb_blob</span> <a href="#duckdb_get_blob"><span class="nf">duckdb_get_blob</span></a>(<span class="kt">duckdb_value</span> <span class="nv">val</span>);
<span class="nv">duckdb_bit</span> <a href="#duckdb_get_bit"><span class="nf">duckdb_get_bit</span></a>(<span class="kt">duckdb_value</span> <span class="nv">val</span>);
<span class="kt">duckdb_uhugeint</span> <a href="#duckdb_get_uuid"><span class="nf">duckdb_get_uuid</span></a>(<span class="kt">duckdb_value</span> <span class="nv">val</span>);
<span class="kt">char</span> *<a href="#duckdb_get_varchar"><span class="nf">duckdb_get_varchar</span></a>(<span class="kt">duckdb_value</span> <span class="nv">value</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_struct_value"><span class="nf">duckdb_create_struct_value</span></a>(<span class="kt">duckdb_logical_type</span> <span class="nv">type</span>, <span class="kt">duckdb_value</span> *<span class="nv">values</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_list_value"><span class="nf">duckdb_create_list_value</span></a>(<span class="kt">duckdb_logical_type</span> <span class="nv">type</span>, <span class="kt">duckdb_value</span> *<span class="nv">values</span>, <span class="kt">idx_t</span> <span class="nv">value_count</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_array_value"><span class="nf">duckdb_create_array_value</span></a>(<span class="kt">duckdb_logical_type</span> <span class="nv">type</span>, <span class="kt">duckdb_value</span> *<span class="nv">values</span>, <span class="kt">idx_t</span> <span class="nv">value_count</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_map_value"><span class="nf">duckdb_create_map_value</span></a>(<span class="kt">duckdb_logical_type</span> <span class="nv">map_type</span>, <span class="kt">duckdb_value</span> *<span class="nv">keys</span>, <span class="kt">duckdb_value</span> *<span class="nv">values</span>, <span class="kt">idx_t</span> <span class="nv">entry_count</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_union_value"><span class="nf">duckdb_create_union_value</span></a>(<span class="kt">duckdb_logical_type</span> <span class="nv">union_type</span>, <span class="kt">idx_t</span> <span class="nv">tag_index</span>, <span class="kt">duckdb_value</span> <span class="nv">value</span>);
<span class="kt">idx_t</span> <a href="#duckdb_get_map_size"><span class="nf">duckdb_get_map_size</span></a>(<span class="kt">duckdb_value</span> <span class="nv">value</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_get_map_key"><span class="nf">duckdb_get_map_key</span></a>(<span class="kt">duckdb_value</span> <span class="nv">value</span>, <span class="kt">idx_t</span> <span class="nv">index</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_get_map_value"><span class="nf">duckdb_get_map_value</span></a>(<span class="kt">duckdb_value</span> <span class="nv">value</span>, <span class="kt">idx_t</span> <span class="nv">index</span>);
<span class="kt">bool</span> <a href="#duckdb_is_null_value"><span class="nf">duckdb_is_null_value</span></a>(<span class="kt">duckdb_value</span> <span class="nv">value</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_null_value"><span class="nf">duckdb_create_null_value</span></a>();
<span class="kt">idx_t</span> <a href="#duckdb_get_list_size"><span class="nf">duckdb_get_list_size</span></a>(<span class="kt">duckdb_value</span> <span class="nv">value</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_get_list_child"><span class="nf">duckdb_get_list_child</span></a>(<span class="kt">duckdb_value</span> <span class="nv">value</span>, <span class="kt">idx_t</span> <span class="nv">index</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_create_enum_value"><span class="nf">duckdb_create_enum_value</span></a>(<span class="kt">duckdb_logical_type</span> <span class="nv">type</span>, <span class="kt">uint64_t</span> <span class="nv">value</span>);
<span class="kt">uint64_t</span> <a href="#duckdb_get_enum_value"><span class="nf">duckdb_get_enum_value</span></a>(<span class="kt">duckdb_value</span> <span class="nv">value</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_get_struct_child"><span class="nf">duckdb_get_struct_child</span></a>(<span class="kt">duckdb_value</span> <span class="nv">value</span>, <span class="kt">idx_t</span> <span class="nv">index</span>);
<span class="kt">char</span> *<a href="#duckdb_value_to_string"><span class="nf">duckdb_value_to_string</span></a>(<span class="kt">duckdb_value</span> <span class="nv">value</span>);
</code></pre></div></div>

#### `duckdb_destroy_value`

销毁值并释放该类型的内存。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nv">duckdb_destroy_value</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> *<span class="nv">value
</span>);
</code></pre></div></div>

##### 参数

* `value`: 要销毁的值。

<br>

#### `duckdb_create_varchar`

从一个空终止字符串创建值

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_varchar</span>(<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">text
</span>);
</code></pre></div></div>

##### 参数

* `text`: 空终止字符串

##### 返回值

值。必须使用 `duckdb_destroy_value` 销毁。

<br>

#### `duckdb_create_varchar_length`

从一个字符串创建值

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_varchar_length</span>(<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">text</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">length
</span>);
</code></pre></div></div>

##### 参数

* `text`: 文本
* `length`: 文本长度

##### 返回值

值。必须使用 `duckdb_destroy_value` 销毁。

<br>

#### `duckdb_create_bool`

从布尔值创建值

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_bool</span>(<span class="nv">
</span>  <span class="kt">bool</span> <span class="nv">input
</span>);
</code></pre></div></div>

##### 参数

* `input`: 布尔值

##### 返回值

值。必须使用 `duckdb_destroy_value` 销毁。

<br>

#### `duckdb_create_int8`

从 int8_t（一个 tinyint）创建值

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_int8</span>(<span class="nv">
</span>  <span class="kt">int8_t</span> <span class="nv">input
</span>);
</code></pre></div></div>

##### 参数

* `input`: tinyint 值

##### 返回值

值。必须使用 `duckdb_destroy_value` 销毁。

<br>

#### `duckdb_create_uint8`

从 uint8_t（一个 utinyint）创建值

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_uint8</span>(<span class="nv">
</span>  <span class="kt">uint8_t</span> <span class="nv">input
</span>);
</code></pre></div></div>

##### 参数

* `input`: utinyint 值

##### 返回值

值。必须使用 `duckdb_destroy_value` 销毁。

<br>

#### `duckdb_create_int16`

从 int16_t（一个 smallint）创建值

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_int16</span>(<span class="nv">
</span>  <span class="kt">int16_t</span> <span class="nv">input
</span>);
</code></pre></div></div>

##### 参数

* `input`: smallint 值

##### 返回值

值。必须使用 `duckdb_destroy_value` 销毁。

<br>

#### `duckdb_create_uint16`

从 uint16_t（一个 usmallint）创建值

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_uint16</span>(<span class="nv">
</span>  <span class="kt">uint16_t</span> <span class="nv">input
</span>);
</code></pre></div></div>

##### 参数

* `input`: usmallint 值

##### 返回值

值。必须使用 `duckdb_destroy_value` 销毁。

<br>

#### `duckdb_create_int32`

从 int32_t（一个 integer）创建值

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_int32</span>(<span class="nv">
</span>  <span class="kt">int32_t</span> <span class="nv">input
</span>);
</code></pre></div></div>

##### 参数

* `input`: integer 值

##### 返回值

值。必须使用 `duckdb_destroy_value` 销毁。

<br>

#### `duckdb_create_uint32`

从 uint32_t（一个 uinteger）创建值

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_uint32</span>(<span class="nv">
</span>  <span class="kt">uint32_t</span> <span class="nv">input
</span>);
</code></pre></div></div>

##### 参数

* `input`: uinteger 值

##### 返回值

值。必须使用 `duckdb_destroy_value` 销毁。

<br>

#### `duckdb_create_uint64`

从 uint64_t（一个 ubigint）创建值

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_uint64</span>(<span class="nv">
</span>  <span class="kt">uint64_t</span> <span class="nv">input
</span>);
</code></pre></div></div>

##### 参数

* `input`: ubigint 值

##### 返回值

值。必须使用 `duckdb_destroy_value` 销毁。

<br>

#### `duckdb_create_int64`

从 int64 创建值


##### 返回值

值。必须使用 `duckdb_destroy_value` 销毁。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_int64</span>(<span class="nv">
</span>  <span class="kt">int64_t</span> <span class="nv">val
</span>);
</code></pre></div></div>
<br>

#### `duckdb_create_hugeint`

从 hugeint 创建值

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_hugeint</span>(<span class="nv">
</span>  <span class="kt">duckdb_hugeint</span> <span class="nv">input
</span>);
</code></pre></div></div>

##### 参数

* `input`: hugeint 值

##### 返回值

值。必须使用 `duckdb_destroy_value` 销毁。

<br>

#### `duckdb_create_uhugeint`

从 uhugeint 创建值

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_uhugeint</span>(<span class="nv">
</span>  <span class="kt">duckdb_uhugeint</span> <span class="nv">input
</span>);
</code></pre></div></div>

##### 参数

* `input`: uhugeint 值

##### 返回值

值。必须使用 `duckdb_destroy_value` 销毁。

<br>

#### `duckdb_create_varint`

从 duckdb_varint 创建 VARINT 值

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_varint</span>(<span class="nv">
</span>  <span class="nv">duckdb_varint</span> <span class="nv">input
</span>);
</code></pre></div></div>

##### 参数

* `input`: duckdb_varint 值

##### 返回值

值。必须使用 `duckdb_destroy_value` 销毁。

<br>

#### `duckdb_create_decimal`

从 duckdb_decimal 创建 DECIMAL 值

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_decimal</span>(<span class="nv">
</span>  <span class="kt">duckdb_decimal</span> <span class="nv">input
</span>);
</code></pre></div></div>

##### 参数

* `input`: duckdb_decimal 值

##### 返回值

值。必须使用 `duckdb_destroy_value` 销毁。

<br>

#### `duckdb_create_float`

从 float 创建值

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_float</span>(<span class="nv">
</span>  <span class="kt">float</span> <span class="nv">input
</span>);
</code></pre></div></div>

##### 参数

* `input`: float 值

##### 返回值

值。必须使用 `duckdb_destroy_value` 销毁。

<br>

#### `duckdb_create_double`

从 double 创建值

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_double</span>(<span class="nv">
</span>  <span class="kt">double</span> <span class="nv">input
</span>);
</code></pre></div></div>

##### 参数

* `input`: double 值

##### 返回值

值。必须使用 `duckdb_destroy_value` 销毁。

<br>

#### `duckdb_create_date`

从 date 创建值

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_date</span>(<span class="nv">
</span>  <span class="kt">duckdb_date</span> <span class="nv">input
</span>);
</code></pre></div></div>

##### 参数

* `input`: date 值

##### 返回值

值。必须使用 `duckdb_destroy_value` 销毁。

<br>

#### `duckdb_create_time`

从 time 创建值

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_time</span>(<span class="nv">
</span>  <span class="kt">duckdb_time</span> <span class="nv">input
</span>);
</code></pre></div></div>

##### 参数

* `input`: time 值

##### 返回值

值。必须使用 `duckdb_destroy_value` 销毁。

<br>

#### `duckdb_create_time_tz_value`

从 time_tz 创建值。不要与 `duckdb_create_time_tz` 混淆，后者创建 duckdb_time_tz_t。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_time_tz_value</span>(<span class="nv">
</span>  <span class="kt">duckdb_time_tz</span> <span class="nv">value
</span>);
</code></pre></div></div>

##### 参数

* `value`: time_tz 值

##### 返回值

值。必须使用 `duckdb_destroy_value` 销毁。

<br>

#### `duckdb_create_timestamp`

从 duckdb_timestamp 创建 TIMESTAMP 值

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_timestamp</span>(<span class="nv">
</span>  <span class="kt">duckdb_timestamp</span> <span class="nv">input
</span>);
</code></pre></div></div>

##### 参数

* `input`: duckdb_timestamp 值

##### 返回值

值。必须使用 `duckdb_destroy_value` 销毁。

<br>

#### `duckdb_create_timestamp_tz`

从 duckdb_timestamp 创建 TIMESTAMP_TZ 值

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_timestamp_tz</span>(<span class="nv">
</span>  <span class="kt">duckdb_timestamp</span> <span class="nv">input
</span>);
</code></pre></div></div>

##### 参数

* `input`: duckdb_timestamp 值

##### 返回值

值。必须使用 `duckdb_destroy_value` 销毁。

<br>

#### `duckdb_create_timestamp_s`

从 duckdb_timestamp_s 创建 TIMESTAMP_S 值

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_timestamp_s</span>(<span class="nv">
</span>  <span class="nv">duckdb_timestamp_s</span> <span class="nv">input
</span>);
</code></pre></div></div>

##### 参数

* `input`: duckdb_timestamp_s 值

##### 返回值

值。必须使用 `duckdb_destroy_value` 销毁。

<br>

#### `duckdb_create_timestamp_ms`

从 duckdb_timestamp_ms 创建 TIMESTAMP_MS 值

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_timestamp_ms</span>(<span class="nv">
</span>  <span class="nv">duckdb_timestamp_ms</span> <span class="nv">input
</span>);
</code></pre></div></div>

##### 参数

* `input`: duckdb_timestamp_ms 值

##### 返回值

值。必须使用 `duckdb_destroy_value` 销毁。

<br>

#### `duckdb_create_timestamp_ns`

从 duckdb_timestamp_ns 创建 TIMESTAMP_NS 值

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_timestamp_ns</span>(<span class="nv">
</span>  <span class="nv">duckdb_timestamp_ns</span> <span class="nv">input
</span>);
</code></pre></div></div>

##### 参数

* `input`: duckdb_timestamp_ns 值

##### 返回值

值。必须使用 `duckdb_destroy_value` 销毁。

<br>

#### `duckdb_create_interval`

从 interval 创建值

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_interval</span>(<span class="nv">
</span>  <span class="kt">duckdb_interval</span> <span class="nv">input
</span>);
</code></pre></div></div>

##### 参数

* `input`: interval 值

##### 返回值

值。必须使用 `duckdb_destroy_value` 销毁。

<br>

#### `duckdb_create_blob`

从 blob 创建值

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_blob</span>(<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">uint8_t</span> *<span class="nv">data</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">length
</span>);
</code></pre></div></div>

##### 参数

* `data`: blob 数据
* `length`: blob 数据长度

##### 返回值

值。必须使用 `duckdb_destroy_value` 销毁。

<br>

#### `duckdb_create_bit`

从 duckdb_bit 创建 BIT 值

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_bit</span>(<span class="nv">
</span>  <span class="nv">duckdb_bit</span> <span class="nv">input
</span>);
</code></pre></div></div>

##### 参数

* `input`: duckdb_bit 值

##### 返回值

值。必须使用 `duckdb_destroy_value` 销毁。

<br>

#### `duckdb_create_uuid`

从 uhugeint 创建 UUID 值

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_uuid</span>(<span class="nv">
</span>  <span class="kt">duckdb_uhugeint</span> <span class="nv">input
</span>);
</code></pre></div></div>

##### 参数

* `input`: 包含 UUID 的 duckdb_uhugeint

##### 返回值

值。必须使用 `duckdb_destroy_value` 销毁。

<br>

#### `duckdb_get_bool`

返回给定值的布尔值。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">bool</span> <span class="nv">duckdb_get_bool</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">val
</span>);
</code></pre></div></div>

##### 参数

* `val`: 包含布尔值的 duckdb_value

##### 返回值

布尔值，如果值无法转换则返回 false

<br>

#### `duckdb_get_int8`

返回给定值的 int8_t 值。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">int8_t</span> <span class="nv">duckdb_get_int8</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">val
</span>);
</code></pre></div></div>

##### 参数

* `val`: 包含 tinyint 的 duckdb_value

##### 返回值

int8_t，如果值无法转换则返回 MinValue<int8>

<br>

#### `duckdb_get_uint8`

返回给定值的 uint8_t 值。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">uint8_t</span> <span class="nv">duckdb_get_uint8</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">val
</span>);
</code></pre></div></div>

##### 参数

* `val`: 包含 utinyint 的 duckdb_value

##### 返回值

uint8_t，如果值无法转换则返回 MinValue<uint8>

<br>

#### `duckdb_get_int16`

返回给定值的 int16_t 值。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">int16_t</span> <span class="nv">duckdb_get_int16</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">val
</span>);
</code></pre></div></div>

##### 参数

* `val`: 包含 smallint 的 duckdb_value

##### 返回值

int16_t，如果值无法转换则返回 MinValue<int16>

<br>

#### `duckdb_get_uint16`

返回给定值的 uint16_t 值。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">uint16_t</span> <span class="nv">duckdb_get_uint16</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">val
</span>);
</code></pre></div></div>

##### 参数

* `val`: 包含 usmallint 的 duckdb_value

##### 返回值

uint16_t，如果值无法转换则返回 MinValue<uint16>

<br>

#### `duckdb_get_int32`

返回给定值的 int32_t 值。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">int32_t</span> <span class="nv">duckdb_get_int32</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">val
</span>);
</code></pre></div></div>

##### 参数

* `val`: 包含整数的 duckdb_value

##### 返回值

int32_t，如果值无法转换则返回 MinValue<int32>

<br>

#### `duckdb_get_uint32`

返回给定值的 uint32_t 值。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">uint32_t</span> <span class="nv">duckdb_get_uint32</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">val
</span>);
</code></pre></div></div>

##### 参数

* `val`: 包含 uinteger 的 duckdb_value

##### 返回值

uint32_t，如果值无法转换则返回 MinValue<uint32>

<br>

#### `duckdb_get_int64`

返回给定值的 int64_t 值。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">int64_t</span> <span class="nv">duckdb_get_int64</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">val
</span>);
</code></pre></div></div>

##### 参数

* `val`: 包含 bigint 的 duckdb_value

##### 返回值

int64_t，如果值无法转换则返回 MinValue<int64>

<br>

#### `duckdb_get_uint64`

返回给定值的 uint64_t 值。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">uint64_t</span> <span class="nv">duckdb_get_uint64</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">val
</span>);
</code></pre></div></div>

##### 参数

* `val`: 包含 ubigint 的 duckdb_value

##### 返回值

uint64_t，如果值无法转换则返回 MinValue<uint64>

<br>

#### `duckdb_get_hugeint`

返回给定值的 hugeint 值。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_hugeint</span> <span class="nv">duckdb_get_hugeint</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">val
</span>);
</code></pre></div></div>

##### 参数

* `val`: 包含 hugeint 的 duckdb_value

##### 返回值

duckdb_hugeint，如果值无法转换则返回 MinValue<hugeint>

<br>

#### `duckdb_get_uhugeint`

返回给定值的 uhugeint 值。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_uhugeint</span> <span class="nv">duckdb_get_uhugeint</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">val
</span>);
</code></pre></div></div>

##### 参数

* `val`: 包含 uhugeint 的 duckdb_value

##### 返回值

duckdb_uhugeint，如果值无法转换则返回 MinValue<uhugeint>

<br>

#### `duckdb_get_varint`

返回给定值的 duckdb_varint 值。`data` 字段必须使用 `duckdb_free` 释放。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">duckdb_varint</span> <span class="nv">duckdb_get_varint</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">val
</span>);
</code></pre></div></div>

##### 参数

* `val`: 包含 VARINT 的 duckdb_value

##### 返回值

duckdb_varint。`data` 字段必须使用 `duckdb_free` 释放。

<br>

#### `duckdb_get_decimal`

返回给定值的 duckdb_decimal 值。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_decimal</span> <span class="nv">duckdb_get_decimal</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">val
</span>);
</code></pre></div></div>

##### 参数

* `val`: 包含 DECIMAL 的 duckdb_value

##### 返回值

duckdb_decimal，如果值无法转换则返回 MinValue<decimal>

<br>

#### `duckdb_get_float`

返回给定值的 float 值。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">float</span> <span class="nv">duckdb_get_float</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">val
</span>);
</code></pre></div></div>

##### 参数

* `val`: 包含 float 的 duckdb_value

##### 返回值

float，如果值无法转换则返回 NAN

<br>

#### `duckdb_get_double`

返回给定值的 double 值。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">double</span> <span class="nv">duckdb_get_double</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">val
</span>);
</code></pre></div></div>

##### 参数

* `val`: 包含 double 的 duckdb_value

##### 返回值

double，如果值无法转换则返回 NAN

<br>

#### `duckdb_get_date`

返回给定值的 date 值。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_date</span> <span class="nv">duckdb_get_date</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">val
</span>);
</code></pre></div></div>

##### 参数

* `val`: 包含 date 的 duckdb_value

##### 返回值

duckdb_date，如果值无法转换则返回 MinValue<date>

<br>

#### `duckdb_get_time`

返回给定值的 time 值。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_time</span> <span class="nv">duckdb_get_time</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">val
</span>);
</code></pre></div></div>

##### 参数

* `val`: 包含 time 的 duckdb_value

##### 返回值

duckdb_time，如果值无法转换则返回 MinValue<time>

<br>

#### `duckdb_get_time_tz`

返回给定值的 time_tz 值。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_time_tz</span> <span class="nv">duckdb_get_time_tz</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">val
</span>);
</code></pre></div></div>

##### 参数

* `val`: 包含 time_tz 的 duckdb_value

##### 返回值

duckdb_time_tz，如果值无法转换则返回 MinValue<time_tz>

<br>

#### `duckdb_get_timestamp`

返回给定值的 TIMESTAMP 值。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_timestamp</span> <span class="nv">duckdb_get_timestamp</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">val
</span>);
</code></pre></div></div>

##### 参数

* `val`: 包含 TIMESTAMP 的 duckdb_value

##### 返回值

duckdb_timestamp，如果值无法转换则返回 MinValue<timestamp>

<br>

#### `duckdb_get_timestamp_tz`

返回给定值的 TIMESTAMP_TZ 值。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><p><code><span class="kt">duckdb_timestamp</span> <span class="nv">duckdb_get_timestamp_tz</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">val
</span>);
</code></pre></div></div>

##### 参数

* `val`: 包含 TIMESTAMP_TZ 的 duckdb_value

##### 返回值

duckdb_timestamp，如果值无法转换则返回 MinValue<timestamp_tz>

<br>

#### `duckdb_get_timestamp_s`

返回给定值的 duckdb_timestamp_s 值。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">duckdb_timestamp_s</span> <span class="nv">duckdb_get_timestamp_s</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">val
</span>);
</code></pre></div></div>

##### 参数

* `val`: 包含 TIMESTAMP_S 的 duckdb_value

##### 返回值

duckdb_timestamp_s，如果值无法转换则返回 MinValue<timestamp_s>

<br>

#### `duckdb_get_timestamp_ms`

返回给定值的 duckdb_timestamp_ms 值。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">duckdb_timestamp_ms</span> <span class="nv">duckdb_get_timestamp_ms</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">val
</span>);
</code></pre></div></div>

##### 参数

* `val`: 包含 TIMESTAMP_MS 的 duckdb_value

##### 返回值

duckdb_timestamp_ms，如果值无法转换则返回 MinValue<timestamp_ms>

<br>

#### `duckdb_get_timestamp_ns`

返回给定值的 duckdb_timestamp_ns 值。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">duckdb_timestamp_ns</span> <span class="nv">duckdb_get_timestamp_ns</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">val
</span>);
</code></pre></div></div>

##### 参数

* `val`: 包含 TIMESTAMP_NS 的 duckdb_value

##### 返回值

duckdb_timestamp_ns，如果值无法转换则返回 MinValue<timestamp_ns>

<br>

#### `duckdb_get_interval`

返回给定值的 interval 值。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_interval</span> <span class="nv">duckdb_get_interval</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">val
</span>);
</code></pre></div></div>

##### 参数

* `val`: 包含 interval 的 duckdb_value

##### 返回值

duckdb_interval，如果值无法转换则返回 MinValue<interval>

<br>

#### `duckdb_get_value_type`

返回给定值的类型。只要值未被销毁，该类型就有效。类型本身不能被销毁。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_logical_type</span> <span class="nv">duckdb_get_value_type</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">val
</span>);
</code></pre></div></div>

##### 参数

* `val`: duckdb_value

##### 返回值

duckdb_logical_type。

<br>

#### `duckdb_get_blob`

返回给定值的 blob 值。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_blob</span> <span class="nv">duckdb_get_blob</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">val
</span>);
</code></pre></div></div>

##### 参数

* `val`: 包含 blob 的 duckdb_value

##### 返回值

duckdb_blob

<br>

#### `duckdb_get_bit`

返回给定值的 duckdb_bit 值。`data` 字段必须使用 `duckdb_free` 释放。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">duckdb_bit</span> <span class="nv">duckdb_get_bit</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">val
</span>);
</code></pre></div></div>

##### 参数

* `val`: 包含 BIT 的 duckdb_value

##### 返回值

duckdb_bit

<br>

#### `duckdb_get_uuid`

返回给定值的 UUID 值的 duckdb_uhugeint。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_uhugeint</span> <span class="nv">duckdb_get_uuid</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">val
</span>);
</code></pre></div></div>

##### 参数

* `val`: 包含 UUID 的 duckdb_value

##### 返回值

表示 UUID 值的 duckdb_uhugeint

<br>

#### `duckdb_get_varchar`

获取给定值的字符串表示。结果必须使用 `duckdb_free` 释放。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">char</span> *<span class="nv">duckdb_get_varchar</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">value
</span>);
</code></pre></div></div>

##### 参数

* `value`: 值

##### 返回值

字符串值。必须使用 `duckdb_free` 释放。

<br>

#### `duckdb_create_struct_value`

从类型和值数组创建结构值。必须使用 `duckdb_destroy_value` 销毁。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_struct_value</span>(<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> <span class="nv">type</span>,<span class="nv">
</span>  <span class="kt">duckdb_value</span> *<span class="nv">values
</span>);
</code></pre></div></div>

##### 参数

* `type`: 结构类型
* `values`: 结构字段的值

##### 返回值

结构值，或 nullptr，如果任何子类型为 `DUCKDB_TYPE_ANY` 或 `DUCKDB_TYPE_INVALID`。

<br>

#### `duckdb_create_list_value`

从子类型（元素类型）和值数组创建列表值。必须使用 `duckdb_destroy_value` 销毁。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_list_value</span>(<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> <span class="nv">type</span>,<span class="nv">
</span>  <span class="kt">duckdb_value</span> *<span class="nv">values</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">value_count
</span>);
</code></pre></div></div>

##### 参数

* `type`: 列表类型
* `values`: 列表值
* `value_count`: 列表中的值数量

##### 返回值

列表值，或 nullptr，如果子类型为 `DUCKDB_TYPE_ANY` 或 `DUCKDB_TYPE_INVALID`。

<br>

#### `duckdb_create_array_value`

从子类型（元素类型）和值数组创建数组值。必须使用 `duckdb_destroy_value` 销毁。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_array_value</span>(<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> <span class="nv">type</span>,<span class="nv">
</span>  <span class="kt">duckdb_value</span> *<span class="nv">values</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">value_count
</span>);
</code></pre></div></div>

##### 参数

* `type`: 数组类型
* `values`: 数组值
* `value_count`: 数组中的值数量

##### 返回值

数组值，或 nullptr，如果子类型为 `DUCKDB_TYPE_ANY` 或 `DUCK1_TYPE_INVALID`。

<br>

#### `duckdb_create_map_value`

从映射类型和两个数组创建映射值，一个用于键，一个用于值，每个数组长度为 `entry_count`。必须使用 `duckdb_destroy_value` 销毁。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_map_value</span>(<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> <span class="nv">map_type</span>,<span class="nv">
</span>  <span class="kt">duckdb_value</span> *<span class="nv">keys</span>,<span class="nv">
</span>  <span class="kt">duckdb_value</span> *<span class="nv">values</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">entry_count
</span>);
</code></pre></div></div>

##### 参数

* `map_type`: 映射类型
* `keys`: 映射的键
* `values`: 映射的值
* `entry_count`: 映射中的条目数（键值对）

##### 返回值

映射值，或 nullptr，如果参数无效。

<br>

#### `duckdb_create_union_value`

从联合类型、标签索引和值创建联合值。必须使用 `duckdb_destroy_value` 销毁。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_union_value</span>(<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> <span class="nv">union_type</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">tag_index</span>,<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">value
</span>);
</code></pre></div></div>

##### 参数

* `union_type`: 联合类型
* `tag_index`: 联合标签的索引
* `value`: 联合值

##### 返回值

联合值，或 nullptr，如果参数无效。

<br>

#### `duckdb_get_map_size`

返回 MAP 值中的元素数量。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="nv">duckdb_get_map_size</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">value
</span>);
</code></pre></div></div>

##### 参数

* `value`: MAP 值。

##### 返回值

映射中的元素数量。

<br>

#### `duckdb_get_map_key`

返回 MAP 在索引处的键作为 duckdb_value。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_get_map_key</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">value</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">index
</span>);
</code></pre></div></div>

##### 参数

* `value`: MAP 值。
* `index`: 键的索引。

##### 返回值

键作为 duckdb_value。

<br>

#### `duckdb_get_map_value`

返回 MAP 在索引处的值作为 duckdb_value。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_get_map_value</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">value</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">index
</span>);
</code></pre></div></div>

##### 参数

* `value`: MAP 值。
* `index`: 值的索引。

##### 返回值

值作为 duckdb_value。

<br>

#### `duckdb_is_null_value`

返回值的类型是否为 SQLNULL。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">bool</span> <span class="nv">duckdb_is_null_value</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">value
</span>);
</code></pre></div></div>

##### 参数

* `value`: 要检查的值。

##### 返回值

如果值的类型是 SQLNULL，返回 true，否则返回 false。

<br>

#### `duckdb_create_null_value`

创建类型为 SQLNULL 的值。


##### 返回值

表示 SQLNULL 的 duckdb_value。必须使用 `duckdb_destroy_value` 销毁。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_null_value</span>(<span class="nv">
</span>  <span class="nv">
</span>);
</code></pre></div></div>
<br>

#### `duckdb_get_list_size`

返回 LIST 值中的元素数量。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="nv">duckdb_get_list_size</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">value
</span>);
</code></pre></div></div>

##### 参数

* `value`: LIST 值。

##### 返回值

列表中的元素数量。

<br>

#### `duckdb_get_list_child`

返回 LIST 在索引处的子项作为 duckdb_value。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_get_list_child</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">value</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">index
</span>);
</code></pre></div></div>

##### 参数

* `value`: LIST 值。
* `index`: 子项的索引。

##### 返回值

子项作为 duckdb_value。

<br>

#### `duckdb_create_enum_value`

从类型和值创建枚举值。必须使用 `duckdb_destroy_value` 销毁。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_create_enum_value</span>(<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> <span class="nv">type</span>,<span class="nv">
</span>  <span class="kt">uint64_t</span> <span class="nv">value
</span>);
</code></pre></div></div>

##### 参数

* `type`: 枚举类型
* `value`: 枚举值

##### 返回值

枚举值，或 nullptr。

<br>

#### `duckdb_get_enum_value`

返回给定值的枚举值。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">uint64_t</span> <span class="nv">duckdb_get_enum_value</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">value
</span>);
</code></pre></div></div>

##### 参数

* `value`: 包含枚举的 duckdb_value

##### 返回值

uint64_t，如果值无法转换则返回 MinValue<uint64>

<br>

#### `duckdb_get_struct_child`

返回 STRUCT 在索引处的子项作为 duckdb_value。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_get_struct_child</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">value</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">index
</span>);
</code></pre></div></div>

##### 参数

* `value`: STRUCT 值。
* `index`: 子项的索引。

##### 返回值

子项作为 duckdb_value。

<br>

#### `duckdb_value_to_string`

返回给定值的 SQL 字符串表示。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">char</span> *<span class="nv">duckdb_value_to_string</span>(<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">value
</span>);
</code></pre></div></div>

##### 参数

* `value`: duckdb_value。

##### 返回值

SQL 字符串表示作为以 null 终止的字符串。结果必须使用 `duckdb_free` 释放。