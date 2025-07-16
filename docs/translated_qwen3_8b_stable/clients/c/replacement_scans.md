---
---
layout: docu
redirect_from:
- /docs/api/c/replacement_scans
- /docs/api/c/replacement_scans/
- /docs/clients/c/replacement_scans
title: 替换扫描
---

<!-- markdownlint-disable MD001 -->

替换扫描 API 可用于注册一个回调函数，当读取一个在目录中不存在的表时调用该回调函数。例如，当执行一个如 `SELECT * FROM my_table` 的查询且 `my_table` 不存在时，替换扫描回调函数将被调用，并将 `my_table` 作为参数传递。替换扫描随后可以插入一个带有特定参数的表函数，以替换对表的读取。

## API 参考概述

<!-- 本节由 scripts/generate_c_api_docs.py 生成 -->

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <a href="#duckdb_add_replacement_scan"><span class="nf">duckdb_add_replacement_scan</span></a>(<span class="kt">duckdb_database</span> <span class="nv">db</span>, <span class="nv">duckdb_replacement_callback_t</span> <span class="nv">replacement</span>, <span class="kt">void</span> *<span class="nv">extra_data</span>, <span class="nv">duckdb_delete_callback_t</span> <span class="nv">delete_callback</span>);
<span class="kt">void</span> <a href="#duckdb_replacement_scan_set_function_name"><span class="nf">duckdb_replacement_scan_set_function_name</span></a>(<span class="kt">duckdb_replacement_scan_info</span> <span class="nv">info</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">function_name</span>);
<span class="kt">void</span> <a href="#duckdb_replacement_scan_add_parameter"><span class="nf">duckdb_replacement_scan_add_parameter</span></a>(<span class="kt">duckdb_replacement_scan_info</span> <span class="nv">info</span>, <span class="kt">duckdb_value</span> <span class="nv">parameter</span>);
<span class="kt">void</span> <a href="#duckdb_replacement_scan_set_error"><span class="nf">duckdb_replacement_scan_set_error</span></a>(<span class="kt">duckdb_replacement_scan_info</span> <span class="nv">info</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">error</span>);
</code></pre></div></div>

#### `duckdb_add_replacement_scan`

将一个替换扫描定义添加到指定的数据库中。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nv">duckdb_add_replacement_scan</span>(<span class="nv">
</span>  <span class="kt">duckdb_database</span> <span class="nv">db</span>,<span class="nv">
</span>  <span class="nv">duckdb_replacement_callback_t</span> <span class="nv">replacement</span>,<span class="nv">
</span>  <span class="kt">void</span> *<span class="nv">extra_data</span>,<span class="nv">
</span>  <span class="nv">duckdb_delete_callback_t</span> <span class="nv">delete_callback
</span>);
</code></pre></div></div>

##### 参数

* `db`: 要添加替换扫描的数据库对象
* `replacement`: 替换扫描回调函数
* `extra_data`: 传递回指定回调函数的额外数据
* `delete_callback`: 如果有的话，用于额外数据的删除回调函数

<br>

#### `duckdb_replacement_scan_set_function_name`

设置替换函数名。如果在替换回调函数中调用此函数，则执行替换扫描。如果不调用，则不执行替换回调函数。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nv">duckdb_replacement_scan_set_function_name</span>(<span class="nv">
</span>  <span class="kt">duckdb_replacement_scan_info</span> <span class="nv">info</span>,<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">function_name
</span>);
</code></pre></div></div>

##### 参数

* `info`: 信息对象
* `function_name`: 要替换的函数名。

<br>

#### `duckdb_replacement_scan_add_parameter`

向替换扫描函数添加一个参数。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nv">duckdb_replacement_scan_add_parameter</span>(<span class="nv">
</span>  <span class="kt">duckdb_replacement_scan_info</span> <span class="nv">info</span>,<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">parameter
</span>);
</code></pre></div></div>

##### 参数

* `info`: 信息对象
* `parameter`: 要添加的参数。

<br>

#### `duckdb_replacement_scan_set_error`

报告在执行替换扫描时发生错误。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nv">duckdb_replacement_scan_set_error</span>(<span class="nv">
</span>  <span class="kt">duckdb_replacement_scan_info</span> <span class="nv">info</span>,<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">error
</span>);
</code></pre></div></div>

##### 参数

* `info`: 信息对象
* `error`: 错误信息