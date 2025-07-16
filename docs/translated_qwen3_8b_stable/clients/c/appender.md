---
layout: docu
redirect_from:
- /docs/api/c/appender
- /docs/api/c/appender/
- /docs/clients/c/appender
title: Appender
---

<!-- markdownlint-disable MD001 -->

Appender 是从 C 接口将数据高效加载到 DuckDB 中的方法，推荐用于快速数据加载。Appender 比使用预编译语句或单个 `INSERT INTO` 语句要快得多。

数据以按行格式追加。对于每一列，应调用 `duckdb_append_[type]`，之后通过调用 `duckdb_appender_end_row` 来完成该行。在所有行追加完成后，应使用 `duckdb_appender_destroy` 来完成 Appender 并清理内存。

请注意，即使函数返回 `DuckDBError`，也应始终调用 `duckdb_appender_destroy` 来销毁生成的 Appender。

## 示例

```c
duckdb_query(con, "CREATE TABLE people (id INTEGER, name VARCHAR)", NULL);

duckdb_appender appender;
if (duckdb_appender_create(con, NULL, "people", &appender) == DuckDBError) {
  // 处理错误
}
// 追加第一行 (1, Mark)
duckdb_append_int32(appender, 1);
duckdb_append_varchar(appender, "Mark");
duckdb_appender_end_row(appender);

// 追加第二行 (2, Hannes)
duckdb_append_int32(appender, 2);
duckdb_append_varchar(appender, "Hannes");
duckdb_appender_end_row(appender);

// 完成追加并将所有行刷新到表中
duckdb_appender_destroy(&appender);
```

## API 参考概述

<!-- 本节由 scripts/generate_c_api_docs.py 生成 -->

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <a href="#duckdb_appender_create"><span class="nf">duckdb_appender_create</span></a>(<span class="kt">duckdb_connection</span> <span class="nv">connection</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">schema</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">table</span>, <span class="kt">duckdb_appender</span> *<span class="nv">out_appender</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_appender_create_ext"><span class="nf">duckdb_appender_create_ext</span></a>(<span class="kt">duckdb_connection</span> <span class="nv">connection</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">catalog</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">schema</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">table</span>, <span class="kt">duckdb_appender</span> *<span class="nv">out_appender</span>);
<span class="kt">idx_t</span> <a href="#duckdb_appender_column_count"><span class="nf">duckdb_appender_column_count</span></a>(<span class="kt">duckdb_appender</span> <span class="nv">appender</span>);
<span class="kt">duckdb_logical_type</span> <a href="#duckdb_appender_column_type"><span class="nf">duckdb_appender_column_type</span></a>(<span class="kt">duckdb_appender</span> <span class="nv">appender</span>, <span class="kt">idx_t</span> <span class="nv">col_idx</span>);
<span class="kt">const</span> <span class="kt">char</span> *<a href="#duckdb_appender_error"><span class="nf">duckdb_appender_error</span></a>(<span class="kt">duckdb_appender</span> <span class="nv">appender</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_appender_flush"><span class="nf">duckdb_appender_flush</span></a>(<span class="kt">duckdb_appender</span> <span class="nv">appender</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_appender_close"><span class="nf">duckdb_appender_close</span></a>(<span class="kt">duckdb_appender</span> <span class="nv">appender</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_appender_destroy"><span class="nf">duckdb_appender_destroy</span></a>(<span class="kt">duckdb_appender</span> *<span class="nv">appender</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_appender_add_column"><span class="nf">duckdb_appender_add_column</span></a>(<span class="kt">duckdb_appender</span> <span class="nv">appender</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">name</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_appender_clear_columns"><span class="nf">duckdb_appender_clear_columns</span></a>(<span class="kt">duckdb_appender</span> <span class="nv">appender</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_appender_begin_row"><span class="nf">duckdb_appender_begin_row</span></a>(<span class="kt">duckdb_appender</span> <span class="nv">appender</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_appender_end_row"><span class="nf">duckdb_appender_end_row</span></a>(<span class="kt">duckdb_appender</span> <span class="nv">appender</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_append_default"><span class="nf">duckdb_append_default</span></a>(<span class="kt">duckdb_appender</span> <span class="nv">appender</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_append_default_to_chunk"><span class="nf">duckdb_append_default_to_chunk</span></a>(<span class="kt">duckdb_appender</span> <span class="nv">appender</span>, <span class="kt">duckdb_data_chunk</span> <span class="nv">chunk</span>, <span class="kt">idx_t</span> <span class="nv">col</span>, <span class="kt">idx_t</span> <span class="nv">row</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_append_bool"><span class="nf">duckdb_append_bool</span></a>(<span class="kt">duckdb_appender</span> <span class="nv">appender</span>, <span class="kt">bool</span> <span class="nv">value</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_append_int8"><span class="nf">duckdb_append_int8</span></a>(<span class="kt">duckdb_appender</span> <span class="nv">appender</span>, <span class="kt">int8_t</span> <span class="nv">value</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_append_int16"><span class="nf">duckdb_append_int16</span></a>(<span class="kt">duckdb_appender</span> <span class="nv">appender</span>, <span class="kt">int16_t</span> <span class="nv">value</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_append_int32"><span class="nf">duckdb_append_int32</span></a>(<span class="kt">duckdb_appender</span> <span class="nv">appender</span>, <span class="kt">int32_t</span> <span class="nv">value</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_append_int64"><span class="nf">duckdb_append_int64</span></a>(<span class="kt">duckdb_appender</span> <span class="nv">appender</span>, <span class="kt">int64_t</span> <span class="nv">value</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_append_hugeint"><span class="nf">duckdb_append_hugeint</span></a>(<span class="kt">duckdb_appender</span> <span class="nv">appender</span>, <span class="kt">duckdb_hugeint</span> <span class="nv">value</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_append_uint8"><span class="nf">duckdb_append_uint8</span></a>(<span class="kt">duckdb_appender</span> <span class="nv">appender</span>, <span class="kt">uint8_t</span> <span class="nv">value</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_append_uint16"><span class="nf">duckdb_append_uint16</span></a>(<span class="kt">duckdb_appender</span> <span class="nv">appender</span>, <span class="kt">uint16_t</span> <span class="nv">value</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_append_uint32"><span class="nf">duckdb_append_uint32</span></a>(<span class="kt">duckdb_appender</span> <span class="nv">appender</span>, <span class="kt">uint32_t</span> <span class="nv">value</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_append_uint64"><span class="nf">duckdb_append_uint64</span></a>(<span class="kt">duckdb_appender</span> <span class="nv">appender</span>, <span class="kt">uint64_t</span> <span class="nv">value</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_append_uhugeint"><span class="nf">duckdb_append_uhugeint</span></a>(<span class="kt">duckdb_appender</span> <span class="nv">appender</span>, <span class="kt">duckdb_uhugeint</span> <span class="nv">value</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_append_float"><span class="nf">duckdb_append_float</span></a>(<span class="kt">duckdb_appender</span> <span class="nv">appender</span>, <span class="kt">float</span> <span class="nv">value</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_append_double"><span class="nf">duckdb_append_double</span></a>(<span class="kt">duckdb_appender</span> <span class="nv">appender</span>, <span class="kt">double</span> <span class="nv">value</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_append_date"><span class="nf">duckdb_append_date</span></a>(<span class="kt">duckdb_appender</span> <span class="nv">appender</span>, <span class="kt">duckdb_date</span> <span class="nv">value</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_append_time"><span class="nf">duckdb_append_time</span></a>(<span class="kt">duckdb_appender</span> <span class="nv">appender</span>, <span class="kt">duckdb_time</span> <span class="nv">value</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_append_timestamp"><span class="nf">duckdb_append_timestamp</span></a>(<span class="kt">duckdb_appender</span> <span class="nv">appender</span>, <span class="kt">duckdb_timestamp</span> <span class="nv">value</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_append_interval"><span class="nf">duckdb_append_interval</span></a>(<span class="kt">duckdb_appender</span> <span class="nv">appender</span>, <span class="kt">duckdb_interval</span> <span class="nv">value</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_append_varchar"><span class="nf">duckdb_append_varchar</span></a>(<span class="kt">duckdb_appender</span> <span class="nv">appender</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">val</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_append_varchar_length"><span class="nf">duckdb_append_varchar_length</span></a>(<span class="kt">duckdb_appender</span> <span class="nv">appender</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">val</span>, <span class="kt">idx_t</span> <span class="nv">length</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_append_blob"><span class="nf">duckdb_append_blob</span></a>(<span class="kt">duckdb_appender</span> <span class="nv">appender</span>, <span class="kt">const</span> <span class="kt">void</span> *<span class="nv">data</span>, <span class="kt">idx_t</span> <span class="nv">length</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_append_null"><span class="nf">duckdb_append_null</span></a>(<span class="kt">duckdb_appender</span> <span class="nv">appender</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_append_value"><span class="nf">duckdb_append_value</span></a>(<span class="kt">duckdb_appender</span> <span class="nv">appender</span>, <span class="kt">duckdb_value</span> <span class="nv">value</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_append_data_chunk"><span class="nf">duckdb_append_data_chunk</span></a>(<span class="kt">duckdb_appender</span> <span class="nv">appender</span>, <span class="kt">duckdb_data_chunk</span> <span class="nv">chunk</span>);
</code></pre></div></div>

#### `duckdb_appender_create`

创建一个 Appender 对象。

请注意，该对象必须使用 `duckdb_appender_destroy` 进行销毁。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_appender_create</span>(<span class="nv">
</span>  <span class="kt">duckdb_connection</span> <span class="nv">connection</span>,<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">schema</span>,<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">table</span>,<span class="nv">
</span>  <span class="kt">duckdb_appender</span> *<span class="nv">out_appender
</span>);
</code></pre></div></div>

##### 参数

* `connection`: 创建 Appender 的连接上下文。
* `schema`: 要追加到的表的模式，或 `nullptr` 表示默认模式。
* `table`: 要追加到的表名。
* `out_appender`: 结果 Appender 对象。

##### 返回值

成功时返回 `DuckDBSuccess`，失败时返回 `DuckDBError`。

<br>

#### `duckdb_appender_create_ext`

创建一个 Appender 对象。

请注意，该对象必须使用 `duckdb_appender_destroy` 进行销毁。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_appender_create_ext</span>(<span class="nv">
</span>  <span class="kt">duckdb_connection</span> <span class="nv">connection</span>,<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">catalog</span>,<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">schema</span>,<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">table</span>,<span class="nv">
</span>  <span class="kt">duckdb_appender</span> *<span class="nv">out_appender
</span>);
</code></pre></div></div>

##### 参数

* `connection`: 创建 Appender 的连接上下文。
* `catalog`: 要追加到的表的目录，或 `nullptr` 表示默认目录。
* `schema`: 要追加到的表的模式，或 `nullptr` 表示默认模式。
* `table`: 要追加到的表名。
* `out_app,ender`: 结果 Appender 对象。

##### 返回值

成功时返回 `DuckDBSuccess`，失败时返回 `DuckDBError`。

<br>

#### `duckdb_appender_column_count`

返回属于 Appender 的列数。如果没有活动的列列表，则等于表的物理列数。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="nv">duckdb_appender_column_count</span>(<span class="nv">
</span>  <span class="kt">duckdb_appender</span> <span class="nv">appender
</span>);
</code></pre></div></div>

##### 参数

* `appender`: 获取列数的 Appender。

##### 返回值

数据块中的列数。

<br>

#### `duckdb_appender_column_type`

返回指定索引处的列类型。这可以是活动列列表中的类型，也可以是接收表中列的相同类型。

注意：结果类型必须使用 `duckdb_destroy_logical_type` 进行销毁。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_logical_type</span> <span class="nv">duckdb_appender_column_type</span>(<span class="nv">
</span>  <span class="kt">duckdb_appender</span> <span class="nv">appender</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">col_idx
</span>);
</code></pre></div></div>

##### 参数

* `appender`: 获取列类型的 Appender。
* `col_idx`: 获取类型列的索引。

##### 返回值

列的 `duckdb_logical_type`。

<br>

#### `duckdb_appender_error`

返回与给定 Appender 关联的错误信息。如果 Appender 没有错误信息，此函数返回 `nullptr`。

错误信息不应被释放。当调用 `duckdb_appender_destroy` 时，它将被释放。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">const</span> <span class="kt">char</span> *<span class="nv">duckdb_appender_error</span>(<span class="nv">
</span>  <span class="kt">duckdb_appender</span> <span class="nv">appender
</span>);
</code></pre></div></div>

##### 参数

* `appender`: 获取错误信息的 Appender。

##### 返回值

错误信息，如果不存在则返回 `nullptr`。

<br>

#### `duckdb_appender_flush`

将 Appender 刷新到表中，强制清除 Appender 的缓存。如果刷新数据触发了约束违反或任何其他错误，所有数据将被无效化，此函数返回 `DuckDBError`。无法继续追加更多值。调用 `duckdb_appender_error` 获取错误信息，然后调用 `duckdb_appender_destroy` 销毁无效的 Appender。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_appender_flush</span>(<span class="nv">
</span>  <span class="kt">duckdb_appender</span> <span class="nv">appender
</span>);
</code></pre></div></div>

##### 参数

* `appender`: 要刷新的 Appender。

##### 返回值

成功返回 `DuckDBSuccess`，失败返回 `DuckDBError`。

<br>

#### `duckdb_appender_close`

通过刷新所有中间状态并关闭 Appender 来关闭 Appender。如果刷新数据触发了约束违反或任何其他错误，所有数据将被无效化，此函数返回 `DuckDBError`。调用 `duckdb_appender_error` 获取错误信息，然后调用 `duckdb_appender_destroy` 销毁无效的 Appender。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_appender_close</span>(<span class="nv">
</span>  <span class="kt">duckdb_appender</span> <span class="nv">appender
</span>);
</code></pre></div></div>

##### 参数

* `appender`: 要刷新和关闭的 Appender。

##### 返回值

成功返回 `DuckDBSuccess`，失败返回 `DuckDBError`。

<br>

#### `duckdb_appender_destroy`

通过刷新所有中间状态到表并销毁 Appender 来关闭 Appender。通过销毁 Appender，此函数将释放所有与 Appender 关联的内存。如果刷新数据触发了约束违反，所有数据将被无效化，此函数返回 `DuckDBError`。由于 Appender 被销毁，无法再通过 `duckdb_appender_error` 获取特定错误信息。因此，如果需要了解特定错误，请在销毁 Appender 之前调用 `duckdb_appender_close`。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_appender_destroy</span>(<span class="nv">
</span>  <span class="kt">duckdb_appender</span> *<span class="nv">appender
</span>);
</code></pre></div></div>

##### 参数

* `appender`: 要刷新、关闭和销毁的 Appender。

##### 返回值

成功返回 `DuckDBSuccess`，失败返回 `DuckDBError`。

<br>

#### `duckdb_appender_add_column`

将列追加到 Appender 的活动列列表中。立即刷新所有先前数据。

活动列列表指定了在刷新数据时预期的所有列。任何非活动列将使用其默认值填充，或设置为 NULL。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_appender_add_column</span>(<span class="nv">
</span>  <span class="kt">duckdb_appender</span> <span class="nv">appender</span>,<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">name
</span>);
</code></pre></div></div>

##### 参数

* `appender`: 要添加列的 Appender。

##### 返回值

成功返回 `DuckDBSuccess`，失败返回 `DuckDBError`。

<br>

#### `duckdb_appender_clear_columns`

从 Appender 的活动列列表中移除所有列，将 Appender 重置为将所有列视为活动列。立即刷新所有先前数据。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_appender_clear_columns</span>(<span class="nv">
</span>  <span class="kt">duckdb_appender</span> <span class="nv">appender
</span>);
</code></pre></div></div>

##### 参数

* `appender`: 要清除列的 Appender。

##### 返回值

成功返回 `DuckDBSuccess`，失败返回 `DuckDBError`。

<br>

#### `duckdb_appender_begin_row`

一个无操作函数，出于向后兼容性的原因提供。不执行任何操作。只有 `duckdb_appender_end_row` 是必需的。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_appender_begin_row</span>(<span class="nv">
</span>  <span class="kt">duckdb_appender</span> <span class="nv">appender
</span>);
</code></pre></div></div>
<br>

#### `duckdb_appender_end_row`

完成当前行的追加。调用 `end_row` 后，可以追加下一行。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_appender_end_row</span>(<span class="nv">
</span>  <span class="kt">duckdb_appender</span> <span class="nv">appender
</span>);
</code></pre></div></div>

##### 参数

* `appender`: Appender。

##### 返回值

成功返回 `DuckDBSuccess`，失败返回 `DuckDBError`。

<br>

#### `duckdb_append_default`

将 DEFAULT 值（如果列没有 DEFAULT，则为 NULL）追加到 Appender。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_append_default</span>(<span class="nv">
</span>  <span class="kt">duckdb_appender</span> <span class="nv">appender
</span>);
</code></pre></div></div>
<br>

#### `duckdb_append_default_to_chunk`

将 DEFAULT 值（如果列没有 DEFAULT，则为 NULL）追加到由指定 Appender 创建的数据块的指定行和列中。该列的默认值必须是一个常量值。不支持非确定性表达式，如 nextval('seq') 或 random()。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_append_default_to_chunk</span>(<span class="nv">
</span>  <span class="kt">duckdb_app
ender</span> <span class="nv">appender</span>,<span class="nv">
</span>  <span class="kt">duckdb_data_chunk</span> <span class="nv">chunk</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">col</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">row
</span>);
</code></pre></div></div>

##### 参数

* `appender`: 获取默认值的 Appender。
* `chunk`: 要追加默认值的数据块。
* `col`: 要追加默认值的数据块列索引。
* `row`: 要追加默认值的数据块行索引。

##### 返回值

成功返回 `DuckDBSuccess`，失败返回 `DuckDBError`。

<br>

#### `duckdb_append_bool`

将 bool 值追加到 Appender。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_append_bool</span>(<span class="nv">
</span>  <span class="kt">duckdb_appender</span> <span class="nv">appender</span>,<span class="nv">
</span>  <span class="kt">bool</span> <span class="nv">value
</span>);
</code></pre></div></div>
<br>

#### `duckdb_append_int8`

将 int8_t 值追加到 Appender。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_append_int8</span>(<span class="nv">
</span>  <span class="kt">duckdb_appender</span> <span class="nv">appender</span>,<span class="nv">
</span>  <span class="kt">int8_t</span> <span class="nv">value
</span>);
</code></pre></div></div>
<br>

#### `duckdb_append_int16`

将 int16_t 值追加到 Appender。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_append_int16</span>(<span class="nv">
</span>  <span class="kt">duckdb_appender</span> <span class="nv">appender</span>,<span class="nv">
</span>  <span class="kt">int16_t</span> <span class="nv">value
</span>);
</code></pre></div></div>
<br>

#### `duckdb_append_int32`

将 int32_t 值追加到 Appender。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_append_int32</span>(<span class="nv">
</span>  <span class="kt">duckdb_appender</span> <span class="nv">appender</span>,<span class="nv">
</span>  <span class="kt">int32_t</span> <span class="nv">value
</span>);
</code></pre></div></div>
<br>

#### `duckdb_append_int64`

将 int64_t 值追加到 Appender。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_append_int64</span>(<span class="nv">
</span>  <span class="kt">duckdb_appender</span> <span class="nv">appender</span>,<span class="nv">
</span>  <span class="kt">int64_t</span> <span class="nv">value
</span>);
</code></pre></div></div>
<br>

#### `duckdb_append_hugeint`

将 duckdb_hugeint 值追加到 Appender。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_append_hugeint</span>(<span class="nv">
</span>  <span class="kt">duckdb_appender</span> <span class="nv">appender</span>,<span class="nv">
</span>  <span class="kt">duckdb_hugeint</span> <span class="nv">value
</span>);
</code></pre></div></div>
<br>

#### `duckdb_append_uint8`

将 uint8_t 值追加到 Appender。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_append_uint8</span>(<span class="nv">
</span>  <span class="kt">duckdb_appender</span> <span class="nv">appender</span>,<span class="nv">
</span>  <span class="kt">uint8_t</span> <span class="nv">value
</span>);
</code></pre></div></div>
<br>

#### `duckdb_append_uint16`

将 uint16_t 值追加到 Appender。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_append_uint16</span>(<span class="nv">
</span>  <span class="kt">duckdb_appender</span> <span class="nv">appender</span>,<span class="nv">
</span>  <span class="kt">uint16_t</span> <span class="nv">value
</span>);
</code></pre></div></div>
<br>

#### `duckdb_append_uint32`

将 uint32_t 值追加到 Appender。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_append_uint32</span>(<span class="nv">
</span>  <span class="kt">duckdb_appender</span> <span class="nv">appender</span>,<span class="nv">
</span>  <span class="kt">uint32_t</span> <span class="nv">value
</span>);
</code></pre></div></div>
<br>

#### `duckdb_append_uint64`

将 uint64_t 值追加到 Appender。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_append_uint64</span>(<span class="nv">
</span>  <span class="kt">duckdb_appender</span> <span class="nv">appender</span>,<span class="nv">
</span>  <span class="kt">uint64_t</span> <span class="nv">value
</span>);
</code></pre></div></div>
<br>

#### `duckdb_append_uhugeint`

将 duckdb_uhugeint 值追加到 Appender。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_append_uhugeint</span>(<span class="nv">
</span>  <span class="kt">duckdb_appender</span> <span class="nv">appender</span>,<span class="nv">
</span>  <span class="kt">duckdb_uhugeint</span> <span class="nv">value
</span>);
</code></pre></div></div>
<br>

#### `duckdb_append_float`

将 float 值追加到 Appender。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_append_float</span>(<span class="nv">
</span>  <span class="kt">duckdb_appender</span> <span class="nv">appender</span>,<span class="nv">
</span>  <span class="kt">float</span> <span class="nv">value
</span>);
</code></pre></div></div>
<br>

#### `duckdb_append_double`

将 double 值追加到 Appender。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_append_double</span>(<span class="nv">
</span>  <span class="kt">duckdb_appender</span> <span class="nv">appender</span>,<span class="nv">
</span>  <span class="kt">double</span> <span class="nv">value
</span>);
</code></pre></div></div>
<br>

#### `duckdb_append_date`

将 duckdb_date 值追加到 Appender。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_append_date</span>(<span class="nv">
</span>  <span class="kt">duckdb_appender</span> <span class="nv">appender</span>,<span class="nv">
</span>  <span class="kt">duckdb_date</span> <span class="nv">value
</span>);
</code></pre></div></div>
<br>

#### `duckdb_append_time`

将 duckdb_time 值追加到 Appender。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_append_time</span>(<span class="nv">
</span>  <span class="kt">duckdb_appender</span> <span class="nv">appender</span>,<span class="nv">
</span>  <span class="kt">duckdb_time</span> <span class="nv">value
</span>);
</code></pre></div></div>
<br>

#### `duckdb_append_timestamp`

将 duckdb_timestamp 值追加到 Appender。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_append_timestamp</span>(<span class="nv">
</span>  <span class="kt">duckdb_appender</span> <span class="nv">appender</span>,<span class="nv">
</span>  <span class="kt">duckdb_timestamp</span> <span class="nv">value
</span>);
</code></pre></div></div>
<br>

#### `duckdb_append_interval`

将 duckdb_interval 值追加到 Appender。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_append_interval</span>(<span class="nv">
</span>  <span class="kt">duckdb_appender</span> <span class="nv">appender</span>,<span class="nv">
</span>  <span class="kt">duckdb_interval</span> <span class="nv">value
</span>);
</code></pre></div></div>
<br>

#### `duckdb_append_varchar`

将 varchar 值追加到 Appender。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_append_varchar</span>(<span class="nv">
</span>  <span class="kt">duckdb_appender</span> <span class="nv">appender</span>,<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">val
</span>);
</code></pre></div></div>
<br>

#### `duckdb_append_varchar_length`

将 varchar 值追加到 Appender。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_append_varchar_length</span>(<span class="nv">
</span>  <span class="kt">duckdb_appender</span> <span class="nv">appender</span>,<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">val</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">length
</span>);
</code></pre></div></div>
<br>

#### `duckdb_append_blob`

将 blob 值追加到 Appender。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_append_blob</span>(<span class="nv">
</span>  <span class="kt">duckdb_appender</span> <span class="nv">appender</span>,<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">void</span> *<span class="nv">data</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">length
</span>);
</code></pre></div></div>
<br>

#### `duckdb_append_null`

将 NULL 值追加到 Appender（任何类型）。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_append_null</span>(<span class="nv">
</span>  <span class="kt">duckdb_appender</span> <span class="nv">appender
</span>);
</code></pre></div></div>
<br>

#### `duckdb_append_value`

将 duckdb_value 值追加到 Appender。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_append_value</span>(<span class="nv">
</span>  <span class="kt">duckdb_appender</span> <span class="nv">appender</span>,<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">value
</span>);
</code></pre></div></div>
<br>

#### `duckdb_append_data_chunk`

将一个预填充的数据块追加到指定的 Appender。如果数据块类型与活动 Appender 类型不匹配，则尝试转换。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_append_data_chunk</span>(<span class="nv">
</span>  <span class="kt">duckdb_appender</span> <span class="nv">appender</span>,<span class="nv">
</span>  <span class="kt">duckdb_data_chunk</span> <span class="nv">chunk
</span>);
</code></pre></div></div>

##### 参数

* `appender`: 要追加到的 Appender。
* `chunk`: 要追加的数据块。

##### 返回值

成功返回 `DuckDBSuccess`，失败返回 `DuckDBError`。

<br>