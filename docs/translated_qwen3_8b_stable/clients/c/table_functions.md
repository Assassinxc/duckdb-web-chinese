---
layout: docu
redirect_from:
- /docs/api/c/table_functions
- /docs/api/c/table_functions/
- /docs/clients/c/table_functions
title: 表函数
---

<!-- markdownlint-disable MD001 -->

表函数 API 可用于定义一个表函数，然后可以在 DuckDB 查询的 `FROM` 子句中调用该函数。

## API 参考概述

<!-- 此部分由 scripts/generate_c_api_docs.py 生成 -->

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_table_function</span> <a href="#duckdb_create_table_function"><span class="nf">duckdb_create_table_function</span></a>();
<span class="kt">void</span> <a href="#duckdb_destroy_table_function"><span class="nf">duckdb_destroy_table_function</span></a>(<span class="kt">duckdb_table_function</span> *<span class="nv">table_function</span>);
<span class="kt">void</span> <a href="#duckdb_table_function_set_name"><span class="nf">duckdb_table_function_set_name</span></a>(<span class="kt">duckdb_table_function</span> <span class="nv">table_function</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">name</span>);
<span class="kt">void</span> <a href="#duckdb_table_function_add_parameter"><span class="nf">duckdb_table_function_add_parameter</span></a>(<span class="kt">duckdb_table_function</span> <span class="nv">table_function</span>, <span class="kt">duckdb_logical_type</span> <span class="nv">type</span>);
<span class="kt">void</span> <a href="#duckdb_table_function_add_named_parameter"><span class="nf">duckdb_table_function_add_named_parameter</span></a>(<span class="kt">duckdb_table_function</span> <span class="nv">table_function</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">name</span>, <span class="kt">duckdb_logical_type</span> <span class="nv">type</span>);
<span class="kt">void</span> <a href="#duckdb_table_function_set_extra_info"><span class="nf">duckdb_table_function_set_extra_info</span></a>(<span class="kt">duckdb_table_function</span> <span class="nv">table_function</span>, <span class="kt">void</span> *<span class="nv">extra_info</span>, <span class="nv">duckdb_delete_callback_t</span> <span class="nv">destroy</span>);
<span class="kt">void</span> <a href="#duckdb_table_function_set_bind"><span class="nf">duckdb_table_function_set_bind</span></a>(<span class="kt">duckdb_table_function</span> <span class="nv">table_function</span>, <span class="nv">duckdb_table_function_bind_t</span> <span class="nv">bind</span>);
<span class="kt">void</span> <a href="#duckdb_table_function_set_init"><span class="nf">duckdb_table_function_set_init</span></a>(<span class="kt">duckdb_table_function</span> <span class="nv">table_function</span>, <span class="nv">duckdb_table_function_init_t</span> <span class="nv">init</span>);
<span class="kt">void</span> <a href="#duckdb_table_function_set_local_init"><span class="nf">duckdb_table_function_set_local_init</span></a>(<span class="kt">duckdb_table_function</span> <span class="nv">table_function</span>, <span class="nv">duckdb_table_function_init_t</span> <span class="nv">init</span>);
<span class="kt">void</span> <a href="#duckdb_table_function_set_function"><span class="nf">duckdb_table_function_set_function</span></a>(<span class="kt">duckdb_table_function</span> <span class="nv">table_function</span>, <span class="nv">duckdb_table_function_t</span> <span class="nv">function</span>);
<span class="kt">void</span> <a href="#duckdb_table_function_supports_projection_pushdown"><span class="nf">duckdb_table_function_supports_projection_pushdown</span></a>(<span class="kt">duckdb_table_function</span> <span class="nv">table_function</span>, <span class="kt">bool</span> <span class="nv">pushdown</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_register_table_function"><span class="nf">duckdb_register_table_function</span></a>(<span class="kt">duckdb_connection</span> <span class="nv">con</span>, <span class="kt">duckdb_table_function</span> <span class="nv">function</span>);
</code></pre></div></div>

### 表函数绑定

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> *<a href="#duckdb_bind_get_extra_info"><span class="nf">duckdb_bind_get_extra_info</span></a>(<span class="kt">duckdb_bind_info</span> <span class="nv">info</span>);
<span class="kt">void</span> <a href="#duckdb_bind_add_result_column"><span class="nf">duckdb_bind_add_result_column</span></a>(<span class="kt">duckdb_bind_info</span> <span class="nv">info</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">name</span>, <span class="kt">duckdb_logical_type</span> <span class="nv">type</span>);
<span class="kt">idx_t</span> <a href="#duckdb_bind_get_parameter_count"><span class="nf">duckdb_bind_get_parameter_count</span></a>(<span class="kt">duckdb_bind_info</span> <span class="nv">info</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_bind_get_parameter"><span class="nf">duckdb_bind_get_parameter</span></a>(<span class="kt">duckdb_bind_info</span> <span class="nv">info</span>, <span class="kt">idx_t</span> <span class="nv">index</span>);
<span class="kt">duckdb_value</span> <a href="#duckdb_bind_get_named_parameter"><span class="nf">duckdb_bind_get_named_parameter</span></a>(<span class="kt">duckdb_bind_info</span> <span class="nv">info</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">name</span>);
<span class="kt">void</span> <a href="#duckdb_bind_set_bind_data"><span class="nf">duckdb_bind_set_bind_data</span></a>(<span class="kt">duckdb_bind_info</span> <span class="nv">info</span>, <span class="kt">void</span> *<span class="nv">bind_data</span>, <span class="nv">duckdb_delete_callback_t</span> <span class="nv">destroy</span>);
<span class="kt">void</span> <a href="#duckdb_bind_set_cardinality"><span class="nf">duckdb_bind_set_cardinality</span></a>(<span class="kt">duckdb_bind_info</span> <span class="nv">info</span>, <span class="kt">idx_t</span> <span class="nv">cardinality</span>, <span class="kt">bool</span> <span class="nv">is_exact</span>);
<span class="kt">void</span> <a href="#duckdb_bind_set_error"><span class="nf">duckdb_bind_set_error</span></a>(<span class="kt">duckdb_bind_info</span> <span class="nv">info</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">error</span>);
</code></pre></div></div>

### 表函数初始化

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> *<a href="#duckdb_init_get_extra_info"><span class="nf">duckdb_init_get_extra_info</span></a>(<span class="kt">duckdb_init_info</span> <span class="nv">info</span>);
<span class="kt">void</span> *<a href="#duckdb_init_get_bind_data"><span class="nf">duckdb_init_get_bind_data</span></a>(<span class="kt">duckdb_init_info</span> <span class="nv">info</span>);
<span class="kt">void</span> <a href="#duckdb_init_set_init_data"><span class="nf">duckdb_init_set_init_data</span></a>(<span class="kt">duckdb_init_info</span> <span class="nv">info</span>, <span class="kt">void</span> *<span class="nv">init_data</span>, <span class="nv">duckdb_delete_callback_t</span> <span class="nv">destroy</span>);
<span class="kt">idx_t</span> <a href="#duckdb_init_get_column_count"><span class="nf">duckdb_init_get_column_count</span></a>(<span class="kt">duckdb_init_info</span> <span class="nv">info</span>);
<span class="kt">idx_t</span> <a href="#duckdb_init_get_column_index"><span class="nf">duckdb_init_get_column_index</span></a>(<span class="kt">duckdb_init_info</span> <span class="nv">info</span>, <span class="kt">idx_t</span> <span class="nv">column_index</span>);
<span class="kt">void</span> <a href="#duckdb_init_set_max_threads"><span class="nf">duckdb_init_set_max_threads</span></a>(<span class="kt">duckdb_init_info</span> <span class="nv">info</span>, <span class="kt">idx_t</span> <span class="nv">max_threads</span>);
<span class="kt">void</span> <a href="#duckdb_init_set_error"><span class="nf">duckdb_init_set_error</span></a>(<span class="kt">duckdb_init_info</span> <span class="nv">info</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">error</span>);
</code></pre></div></div>

### 表函数

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> *<a href="#duckdb_function_get_extra_info"><span class="nf">duckdb_function_get_extra_info</span></a>(<span class="kt">duckdb_function_info</span> <span class="nv">info</span>);
<span class="kt">void</span> *<a href="#duckdb_function_get_bind_data"><span class="nf">duckdb_function_get_bind_data</span></a>(<span class="kt">duckdb_function_info</span> <span class="nv">info</span>);
<span class="kt">void</span> *<a href="#duckdb_function_get_init_data"><span class="nf">duckdb_function_get_init_data</span></a>(<span class="kt">duckdb_function_info</span> <span class="nv">info</span>);
<span class="kt">void</span> *<a href="#duckdb_function_get_local_init_data"><span class="nf">duckdb_function_get_local_init_data</span></a>(<span class="kt">duckdb_function_info</span> <span class="nv">info</span>);
<span class="kt">void</span> <a href="#duckdb_function_set_error"><span class="nf">duckdb_function_set_error</span></a>(<span class="kt">duckdb_function_info</span> <span class="nv">info</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">error</span>);
</code></pre></div></div>

#### `duckdb_create_table_function`

创建一个新的空表函数。

返回值应使用 `duckdb_destroy_table_function` 进行销毁。

##### 返回值

表函数对象。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_table_function</span> <span class="nf">duckdb_create_table_function</span>(<span class="nv">
</span>);
</code></pre></div></div>
<br>

#### `duckdb_destroy_table_function`

销毁给定的表函数对象。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nf">duckdb_destroy_table_function</span>(<span class="nv">
</span>  <span class="kt">duckdb_table_function</span> *<span class="nv">table_function
</span>);
</code></pre></div></div>

##### 参数

* `table_function`: 要销毁的表函数

<br>

#### `duckdb_table_function_set_name`

设置给定表函数的名称。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nf">duckdb_table_function_set_name</span>(<span class="nv">
</span>  <span class="kt">duckdb_table_function</span> <span class="nv">table_function</span>,<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">name
</span>);
</code></pre></div></div>

##### 参数

* `table_function`: 表函数
* `name`: 表函数的名称

<br>

#### `duckdb_table_function_add_parameter`

向表函数添加一个参数。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nf">duckdb_table_function_add_parameter</span>(<span class="nv">
</span>  <span class="kt">duckdb_table_function</span> <span class="nv">table_function</span>,<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> <span class="nv">type
</span>);
</code></pre></div></div>

##### 参数

* `table_function`: 表函数。
* `type`: 参数类型。不能包含 INVALID。

<br>

#### `duckdb_table_function_add_named_parameter`

向表函数添加一个命名参数。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nf">duckdb_table_function_add_named_parameter</span>(<span class="nv">
</span>  <span class="kt">duckdb_table_function</span> <span class="nv">table_function</span>,<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">name</span>,<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> <span class="nv">type
</span>);
</code></pre></div></div>

##### 参数

* `table_function`: 表函数。
* `name`: 参数名称。
* `type`: 参数类型。不能包含 INVALID。

<br>

#### `duckdb_table_function_set_extra_info`

将额外信息分配给表函数，以便在绑定等过程中获取。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nf">duckdb_table_function_set_extra_info</span>(<span class="nv">
</span>  <span class="kt">duckdb_table_function</span> <span class="nv">table_function</span>,<span class="nv">
</span>  <span class="kt">void</span> *<span class="nv">extra_info</span>,<span class="nv">
</span>  <span class="nv">duckdb_delete_callback_t</span> <span class="nv">destroy
</span>);
</code></pre></div></div>

##### 参数

* `table_function`: 表函数
* `extra_info`: 额外信息
* `destroy`: 用于销毁额外信息的回调（如果有的话）

<br>

#### `duckdb_table_function_set_bind`

设置表函数的绑定函数。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nf">duckdb_table_function_set_bind</span>(<span class="nv">
</span>  <span class="kt">duckdb_table_function</span> <span class="nv">table_function</span>,<span class="nv">
</span>  <span class="nv">duckdb_table_function_bind_t</span> <span class="nv">bind
</span>);
</code></pre></div></div>

##### 参数

* `table_function`: 表函数
* `bind`: 绑定函数

<br>

#### `duckdb_table_function_set_init`

设置表函数的初始化函数。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nf">duckdb_table_function_set_init</span>(<span class="nv">
</span>  <span class="kt">duckdb_table_function</span> <span class="nv">table_function</span>,<span class="nv">
</span>  <span class="nv">duckdb_table_function_init_t</span> <span class="nv">init
</span>);
</code></pre></div></div>

##### 参数

* `table_function`: 表函数
* `init`: 初始化函数

<br>

#### `duckdb_table_function_set_local_init`

设置表函数的线程本地初始化函数。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nf">duckdb_table_function_set_local_init</span>(<span class="nv">
</span>  <span class="kt">duckdb_table_function</span> <span class="nv">table_function</span>,<span class="nv">
</span>  <span class="nv">duckdb_table_function_init_t</span> <span class="nv">init
</span>);
</code></pre></div></div>

##### 参数

* `table_function`: 表函数
* `init`: 初始化函数

<br>

#### `duckdb_table_function_set_function`

设置表函数的主要函数。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nf">duckdb_table_function_set_function</span>(<span class="nv">
</span>  <span class="kt">duckdb_table_function</span> <span class="nv">table_function</span>,<span class="nv">
</span>  <span class="nv">duckdb_table_function_t</span> <span class="nv">function
</span>);
</code></pre></div></div>

##### 参数

* `table_function`: 表函数
* `function`: 函数

<br>

#### `duckdb_table_function_supports_projection_pushdown`

设置给定表函数是否支持投影下推。

如果设置为 true，系统将在 `init` 阶段通过 `duckdb_init_get_column_count` 和 `duckdb_init_get_column_index` 函数提供所有必需列的列表。
如果设置为 false（默认），系统将期望所有列都被投影。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nf">duckdb_table_function_supports_projection_pushdown</span>(<span class="nv">
</span>  <span class="kt">duckdb_table_function</span> <span class="nv">table_function</span>,<span class="nv">
</span>  <span class="kt">bool</span> <span class="nv">pushdown
</span>);
</code></pre></div></div>

##### 参数

* `table_function`: 表函数
* `pushdown`: 如果表函数支持投影下推则为 true，否则为 false。

<br>

#### `duckdb_register_table_function`

在给定的连接中注册表函数对象。

该函数至少需要一个名称、一个绑定函数、一个初始化函数和一个主函数。

如果函数不完整或已有同名函数，将返回 DuckDBError。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nf">duckdb_register_table_function</span>(<span class="nv">
</span>  <span class="kt">duckdb_connection</span> <span class="nv">con</span>,<span class="nv">
</span>  <span class="kt">duckdb_table_function</span> <span class="nv">function
</span>);
</code></pre></div></div>

##### 参数

* `con`: 要注册的连接。
* `function`: 函数指针

##### 返回值

注册是否成功。

<br>

#### `duckdb_bind_get_extra_info`

获取在 `duckdb_table_function_set_extra_info` 中设置的函数额外信息。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> *<span class="nf">duckdb_bind_get_extra_info</span>(<span class="nv">
</span>  <span class="kt">duckdb_bind_info</span> <span class="nv">info
</span>);
</code></pre></div></div>

##### 参数

* `info`: 信息对象

##### 返回值

额外信息

<br>

#### `duckdb_bind_add_result_column`

向表函数的输出添加一个结果列。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nf">duckdb_bind_add_result_column</span>(<span class="nv">
</span>  <span class="kt">duckdb_bind_info</span> <span class="nv">info</span>,<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">name</span>,<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> <span class="nv">type
</span>);
</code></pre></div></div>

##### 参数

* `info`: 表函数的绑定信息。
* `name`: 列名。
* `type`: 逻辑列类型。

<br>

#### `duckdb_bind_get_parameter_count`

获取函数的普通（非命名）参数数量。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="nf">duckdb_bind_get_parameter_count</span>(<span class="nv">
</span>  <span class="kt">duckdb_bind_info</span> <span class="nv">info
</span>);
</code></pre></div></div>

##### 参数

* `info`: 信息对象

##### 返回值

参数数量

<br>

#### `duckdb_bind_get_parameter`

获取指定索引的参数。

结果必须使用 `duckdb_destroy_value` 进行销毁。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nf">duckdb_bind_get_parameter</span>(<span class="nv">
</span>  <span class="kt">duckdb_bind_info</span> <span class="nv">info</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">index
</span>);
</code></pre></div></div>

##### 参数

* `info`: 信息对象
* `index`: 要获取的参数索引

##### 返回值

参数的值。必须使用 `duckdb_destroy_value` 进行销毁。

<br>

#### `duckdb_bind_get_named_parameter`

获取具有给定名称的命名参数。

结果必须使用 `duckdb_destroy_value` 进行销毁。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nf">duckdb_bind_get_named_parameter</span>(<span class="nv">
</span>  <span class="kt">duckdb_bind_info</span> <span class="nv">info</span>,<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">name
</span>);
</code></pre></div></div>

##### 参数

* `info`: 信息对象
* `name`: 参数名称

##### 返回值

参数的值。必须使用 `duckdb_destroy_value` 进行销毁。

<br>

#### `duckdb_bind_set_bind_data`

在表函数的绑定对象中设置用户提供的绑定数据。
此对象可以在执行期间再次获取。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nf">duckdb_bind_set_bind_data</span>(<span class="nv">
</span>  <span class="kt">duckdb_bind_info</span> <span class="nv">info</span>,<span class="nv">
</span>  <span class="kt">void</span> *<span class="nv">bind_data</span>,<span class="nv">
</span>  <span class="nv">duckdb_delete_callback_t</span> <span class="nv">destroy
</span>);
</code></pre></div></div>

##### 参数

* `info`: 表函数的绑定信息。
* `bind_data`: 绑定数据对象。
* `destroy`: 用于销毁绑定数据的回调（如果有的话）。

<br>

#### `duckdb_bind_set_cardinality`

设置表函数的基数估计值，用于优化。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nf">duckdb_bind_set_cardinality</span>(<span class="nv">
</span>  <span class="kt">duckdb_bind_info</span> <span class="nv">info</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">cardinality</span>,<span class="nv">
</span>  <span class="kt">bool</span> <span class="nv">is_exact
</span>);
</code></pre></div></div>

##### 参数

* `info`: 绑定数据对象。
* `is_exact`: 基数估计值是否精确，还是近似值。

<br>

#### `duckdb_bind_set_error`

报告在调用表函数的绑定时发生错误。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nf">duckdb_bind_set_error</span>(<span class="nv">
</span>  <span class="kt">duckdb_bind_info</span> <span class="nv">info</span>,<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">error
</span>);
</code></pre></div></div>

##### 参数

* `info`: 信息对象
* `error`: 错误消息

<br>

#### `duckdb_init_get_extra_info`

获取在 `duckdb_table_function_set_extra_info` 中设置的函数额外信息。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> *<span class="nf">duckdb_init_get_extra_info</span>(<span class="nv">
</span>  <span class="kt">duckdb_init_info</span> <span class="nv">info
</span>);
</code></pre></div></div>

##### 参数

* `info`: 信息对象

##### 返回值

额外信息

<br>

#### `duckdb_init_get_bind_data`

获取在绑定期间通过 `duckdb_bind_set_bind_data` 设置的绑定数据。
请注意，绑定数据应被视为只读。
若需跟踪状态，请使用初始化数据。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> *<span class="nf">duckdb_init_get_bind_data</span>(<span class="nv">
</span>  <span class="kt">duckdb_init_info</span> <span class="nv">info
</span>);
</code></pre></div></div>

##### 参数

* `info`: 信息对象

##### 返回值

绑定数据对象

<br>

#### `duckdb_init_set_init_data`

在初始化对象中设置用户提供的初始化数据。此对象可以在执行期间再次获取。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nf">duckdb_init_set_init_data</span>(<span class="nv">
</span>  <span class="kt">duckdb_init_info</span> <span class="nv">info</span>,<span class="nv">
</span>  <span class="kt">void</span> *<span class="nv">init_data</span>,<span class="nv">
</span>  <span class="nv">duckdb_delete_callback_t</span> <span class="nv">destroy
</span>);
</code></pre></div></div>

##### 参数

* `info`: 信息对象
* `init_data`: 初始化数据对象。
* `destroy`: 用于销毁初始化数据的回调（如果有的话）

<br>

#### `duckdb_init_get_column_count`

返回投影列的数量。

如果启用了投影下推，必须使用此函数来确定要发出哪些列。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="nf">duckdb_init_get_column_count</span>(<span class="nv">
</span>  <span class="kt">duckdb_init_info</span> <span class="nv">info
</span>);
</code></pre></div></div>

##### 参数

* `info`: 信息对象

##### 返回值

投影列的数量。

<br>

#### `duckdb_init_get_column_index`

返回指定位置的投影列的列索引。

如果启用了投影下推，必须使用此函数来确定要发出哪些列。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="nf">duckdb_init_get_column_index</span>(<span class="nv">
</span>  <span class="kt">duckdb_init_info</span> <span class="nv">info</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">column_index
</span>);
</code></pre></div></div>

##### 参数

* `info`: 信息对象
* `column_index`: 获取投影列索引的位置，从 0..duckdb_init_get_column_count(info)

##### 返回值

投影列的列索引。

<br>

#### `duckdb_init_set_max_threads`

设置可以并行处理此表函数的线程数（默认值：1）

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nf">duckdb_init_set_max_threads</span>(<span class="nv">
</span>  <span class="kt">duckdb_init_info</span> <span class="nv">info</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">max_threads
</span>);
</code></pre></div></div>

##### 参数

* `info`: 信息对象
* `max_threads`: 可以处理此表函数的最大线程数

<br>

#### `duckdb_init_set_error`

报告在调用初始化时发生错误。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nf">duckdb_init_set_error</span>(<span class="nv">
</span>  <span class="kt">duckdb_init_info</span> <span class="nv">info</span>,<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">error
</span>);
</code></pre></div></div>

##### 参数

* `info`: 信息对象
* `error`: 错误消息

<br>

#### `duckdb_function_get_extra_info`

获取在 `duckdb_table_function_set_extra_info` 中设置的函数额外信息。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> *<span class="nf">duckdb_function_get_extra_info</span>(<span class="nv">
</span>  <span class="kt">duckdb_function_info</span> <span class="nv">info
</span>);
</code></pre></div></div>

##### 参数

* `info`: 信息对象

##### 返回值

额外信息

<br>

#### `duckdb_function_get_bind_data`

获取通过 `duckdb_bind_set_bind_data` 设置的表函数绑定数据。

请注意，绑定数据是只读的。
若需跟踪状态，请使用初始化数据。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> *<span class="nf">duckdb_function_get_bind_data</span>(<span class="nv">
</span>  <span class="kt">duckdb_function_info</span> <span class="nv">info
</span>);
</code></pre></div></div>

##### 参数

* `info`: 函数信息对象。

##### 返回值

绑定数据对象。

<br>

#### `duckdb_function_get_init_data`

获取在初始化期间通过 `duckdb_init_set_init_data` 设置的初始化数据。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> *<span class="nf">duckdb_function_get_init_data</span>(<span class="nv">
</span>  <span class="kt">duckdb_function_info</span> <span class="nv">info
</span>);
</code></pre></div></div>

##### 参数

* `info`: 信息对象

##### 返回值

初始化数据对象

<br>

#### `duckdb_function_get_local_init_data`

获取在本地初始化期间通过 `duckdb_init_set_init_data` 设置的线程本地初始化数据。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> *<span class="nf">duckdb_function_get_local_init_data</span>(<span class="nv">
</span>  <span class="kt">duckdb_function_info</span> <span class="nv">info
</span>);
</code></pre></div></div>

##### 参数

* `info`: 信息对象

##### 返回值

初始化数据对象

<br>

#### `duckdb_function_set_error`

报告在执行函数时发生错误。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nf">duckdb_function_set_error</span>(<span class="nv">
</span>  <span class="kt">duckdb_function_info</span> <span class="nv">info</span>,<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">error
</span>);
</code></pre></div></div>

##### 参数

* `info`: 信息对象
* `error`: 错误消息

<br>