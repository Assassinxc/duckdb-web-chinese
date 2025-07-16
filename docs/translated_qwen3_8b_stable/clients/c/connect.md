---
---
layout: docu
redirect_from:
- /docs/api/c/connect
- /docs/api/c/connect/
- /docs/clients/c/connect
title: 启动与关闭
---

<!-- markdownlint-disable MD001 -->

要使用 DuckDB，您必须首先使用 `duckdb_open()` 初始化一个 `duckdb_database` 处理句柄。`duckdb_open()` 接受一个参数，即要读写的数据文件。特殊值 `NULL` (`nullptr`) 可用于创建一个 **内存数据库**。请注意，对于内存数据库，不会将任何数据持久化到磁盘（即，退出进程时所有数据都会丢失）。

使用 `duckdb_database` 处理句柄，您可以使用 `duckdb_connect()` 创建一个或多个 `duckdb_connection`。虽然单个连接是线程安全的，但在查询期间它们会被锁定。因此，建议每个线程使用其自己的连接以实现最佳的并行性能。

所有 `duckdb_connection` 必须显式地使用 `duckdb_disconnect()` 断开连接，且 `duckdb_database` 必须显式地使用 `duckdb_close()` 关闭，以避免内存和文件句柄泄漏。

## 示例

```c
duckdb_database db;
duckdb_connection con;

if (duckdb_open(NULL, &db) == DuckDBError) {
    // 处理错误
}
if (duckdb_connect(db, &con) == DuckDBError) {
    // 处理错误
}

// 运行查询...

// 清理
duckdb_disconnect(&con);
duckdb_close(&db);
```

## API 参考概述

<!-- 本节由 scripts/generate_c_api_docs.py 生成 -->

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">duckdb_instance_cache</span> <a href="#duckdb_create_instance_cache"><span class="nf">duckdb_create_instance_cache</span></a>();
<span class="kt">duckdb_state</span> <a href="#duckdb_get_or_create_from_cache"><span class="nf">duckdb_get_or_create_from_cache</span></a>(<span class="nv">duckdb_instance_cache</span> <span class="nv">instance_cache</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">path</span>, <span class="kt">duckdb_database</span> *<span class="nv">out_database</span>, <span class="kt">duckdb_config</span> <span class="nv">config</span>, <span class="kt">char</span> **<span class="nv">out_error</span>);
<span class="kt">void</span> <a href="#duckdb_destroy_instance_cache"><span class="nf">duckdb_destroy_instance_cache</span></a>(<span class="nv">duckdb_instance_cache</span> *<span class="nv">instance_cache</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_open"><span class="nf">duckdb_open</span></a>(<span class="kt">const</span> <span class="kt">char</span> *<span class="nv">path</span>, <span class="kt">duckdb_database</span> *<span class="nv">out_database</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_open_ext"><span class="nf">duckdb_open_ext</span></a>(<span class="kt">const</span> <span class="kt">char</span> *<span class="nv">path</span>, <span class="kt">duckdb_database</span> *<span class="nv">out_database</span>, <span class="kt">duckdb_config</span> <span class="nv">config</span>, <span class="kt">char</span> **<span class="nv">out_error</span>);
<span class="kt">void</span> <a href="#duckdb_close"><span class="nf">duckdb_close</span></a>(<span class="kt">duckdb_database</span> *<span class="nv">database</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_connect"><span class="nf">duckdb_connect</span></a>(<span class="kt">duckdb_database</span> <span class="nv">database</span>, <span class="kt">duckdb_connection</span> *<span class="nv">out_connection</span>);
<span class="kt">void</span> <a href="#duckdb_interrupt"><span class="nf">duckdb_interrupt</span></a>(<span class="kt">duckdb_connection</span> <span class="nv">connection</span>);
<span class="kt">duckdb_query_progress_type</span> <a href="#duckdb_query_progress"><span class="nf">duckdb_query_progress</span></a>(<span class="kt">duckdb_connection</span> <span class="nv">connection</span>);
<span class="kt">void</span> <a href="#duckdb_disconnect"><span class="nf">duckdb_disconnect</span></a>(<span class="kt">duckdb_connection</span> *<span class="nv">connection</span>);
<span class="kt">void</span> <a href="#duckdb_connection_get_client_context"><span class="nf">duckdb_connection_get_client_context</span></a>(<span class="kt">duckdb_connection</span> <span class="nv">connection</span>, <span class="nv">duckdb_client_context</span> *<span class="nv">out_context</span>);
<span class="kt">idx_t</span> <a href="#duckdb_client_context_get_connection_id"><span class="nf">duckdb_client_context_get_connection_id</span></a>(<span class="nv">duckdb_client
</span>  <span class="nv">context</span>);
<span class="kt">void</span> <a href="#duckdb_destroy_client_context"><span class="nf">duckdb_destroy_client_context</span></a>(<span class="nv">duckdb_client_context</span> *<span class="nv">context</span>);
<span class="kt">const</span> <span class="kt">char</span> *<a href="#duckdb_library_version"><span class="nf">duckdb_library_version</span></a>();
<span class="kt">duckdb_value</span> <a href="#duckdb_get_table_names"><span class="nf">duckdb_get_table_names</span></a>(<span class="kt">duckdb_connection</span> <span class="nv">connection</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">query</span>, <span class="kt">bool</span> <span class="nv">qualified</span>);
</code></pre></div></div>

#### `duckdb_create_instance_cache`

创建一个新的数据库实例缓存。
如果客户端/程序在同一进程内对同一文件打开多个数据库，实例缓存是必要的。必须使用 'duckdb_destroy_instance_cache' 来销毁它。

##### 返回值

数据库实例缓存。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">duckdb_instance_cache</span> <span class="nv">duckdb_create_instance_cache</span>(<span class="nv">
</span>  <span class="nv">
</span>);
</code></pre></div></div>
<br>

#### `duckdb_get_or_create_from_cache`

在实例缓存中创建一个新的数据库实例，或检索现有的数据库实例。
必须使用 'duckdb_close' 关闭。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_get_or_create_from_cache</span>(<span class="nv">
</span>  <span class="nv">duckdb_instance_cache</span> <span class="nv">instance_cache</span>,<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">path</span>,<span class="nv">
</span>  <span class="kt">duckdb_database</span> *<span class="nv">out_database</span>,<span class="nv">
</span>  <span class="kt">duckdb_config</span> <span class="nv">config</span>,<span class="nv">
</span>  <span class="kt">char</span> **<span class="nv">out_error
</span>);
</code></pre></div></div>

##### 参数

* `instance_cache`: 在其中创建数据库或从中获取数据库的实例缓存。
* `path`: 磁盘上的数据库文件路径。`nullptr` 和 `:memory:` 都会打开或检索一个内存数据库。
* `out_database`: 结果缓存的数据库。
* `config`: （可选）用于创建数据库的配置。
* `out_error`: 如果设置且函数返回 `DuckDBError`，则包含错误信息。
  注意：错误信息必须使用 `duckdb_free` 释放。

##### 返回值

成功返回 `DuckDBSuccess`，失败返回 `DuckDBError`。

<br>

#### `duckdb_destroy_instance_cache`

销毁现有的数据库实例缓存并释放其内存。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nv">duckdb_destroy_instance_cache</span>(<span class="nv">
</span>  <span class="nv">duckdb_instance_cache</span> *<span class="nv">instance_cache
</span>);
</code></pre></div></div>

##### 参数

* `instance_cache`: 要销毁的实例缓存。

<br>

#### `duckdb_open`

创建一个新的数据库或打开一个存储在给定路径的现有数据库文件。
如果未指定路径，则创建一个内存数据库。
数据库必须使用 'duckdb_close' 关闭。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_open</span>(<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">path</span>,<span class="nv">
</span>  <span class="kt">duckdb_database</span> *<span class="nv">out_database
</span>);
</code></pre></div></div>

##### 参数

* `path`: 磁盘上的数据库文件路径。`nullptr` 和 `:memory:` 都会打开一个内存数据库。
* `out_database`: 结果数据库对象。

##### 返回值

成功返回 `DuckDBSuccess`，失败返回 `DuckDBError`。

<br>

#### `duckdb_open_ext`

`duckdb_open` 的扩展版本。创建一个新的数据库或打开一个存储在给定路径的现有数据库文件。
数据库必须使用 'duckdb_close' 关闭。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_open_ext</span>(<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">path</span>,<span class="nv">
</span>  <span class="kt">duckdb_database</span> *<span class="nv">out_database</span>,<span class="nv">
</span>  <span class="kt">duckdb_config</span> <span class="nv">config</span>,<span class="nv">
</span>  <span class="kt">char</span> **<span class="nv">out_error
</span>);
</code></pre></div></div>

##### 参数

* `path`: 磁盘上的数据库文件路径。`nullptr` 和 `:memory:` 都会打开一个内存数据库。
* `out_database`: 结果数据库对象。
* `config`: （可选）用于启动数据库的配置。
* `out_error`: 如果设置且函数返回 `DuckDBError`，则包含错误信息。
  注意：错误信息必须使用 `duckdb_free` 释放。

##### 返回值

成功返回 `DuckDBSuccess`，失败返回 `DuckDBError`。

<br>

#### `duckdb_close`

关闭指定的数据库并释放为其分配的所有内存。
这应在使用通过 `duckdb_open` 或 `duckdb_open_ext` 分配的任何数据库后调用。
请注意，未调用 `duckdb_close`（例如程序崩溃）不会导致数据损坏。
不过，建议在使用完数据库对象后总是正确关闭它。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nv">duckdb_close</span>(<span class="nv">
</span>  <span class="kt">duckdb_database</span> *<span class="nv">database
</span>);
</code></pre></div></div>

##### 参数

* `database`: 要关闭的数据库对象。

<br>

#### `duckdb_connect`

打开到数据库的连接。连接用于查询数据库，并存储与连接相关的事务状态。
实例化的连接应使用 'duckdb_disconnect' 关闭。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_connect</span>(<span class="nv">
</span>  <span class="kt">duckdb_database</span> <span class="nv">database</span>,<span class="nv">
</span>  <span class="kt">duckdb_connection</span> *<span class="nv">out_connection
</span>);
</code></pre></div></div>

##### 参数

* `database`: 要连接的数据库文件。
* `out_connection`: 结果连接对象。

##### 返回值

成功返回 `DuckDBSuccess`，失败返回 `DuckDBError`。

<br>

#### `duckdb_interrupt`

中断正在运行的查询

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nv">duckdb_interrupt</span>(<span class="nv">
</span>  <span class="kt">duckdb_connection</span> <span class="nv">connection
</span>);
</code></pre></div></div>

##### 参数

* `connection`: 要中断的连接

<br>

#### `duckdb_query_progress`

获取正在运行的查询进度

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_query_progress_type</span> <span class="nv">duckdb_query_progress</span>(<span class="nv">
</span>  <span class="kt">duckdb_connection</span> <span class="nv">connection
</span>);
</code></pre></div></div>

##### 参数

* `connection`: 正在工作的连接

##### 返回值

-1 表示没有进度，或进度的百分比

<br>

#### `duckdb_disconnect`

关闭指定的连接并释放为其分配的所有内存。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nv">duckdb_disconnect</span>(<span class="nv">
</span>  <span class="kt">duckdb_connection</span> *<span class="nv">connection
</span>);
</code></pre></div></div>

##### 参数

* `connection`: 要关闭的连接。

<br>

#### `duckdb_connection_get_client_context`

获取连接的客户端上下文。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nv">duckdb_connection_get_client_context</span>(<span class="nv">
</span>  <span class="kt">duckdb_connection</span> <span class="nv">connection</span>,<span class="nv">
</span>  <span class="nv">duckdb_client_context</span> *<span class="nv">out_context
</span>);
</code></pre></div></div>

##### 参数

* `connection`: 连接。
* `out_context`: 连接的客户端上下文。必须使用 `duckdb_destroy_client_context` 销毁。

<br>

#### `duckdb_client_context_get_connection_id`

返回客户端上下文的连接 ID。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="nv">duckdb_client_context_get_connection_id</span>(<span class="nv">
</span>  <span class="nv">duckdb_client_context</span> <span class="nv">context
</span>);
</code></pre></div></div>

##### 参数

* `context`: 客户端上下文。

##### 返回值

客户端上下文的连接 ID。

<br>

#### `duckdb_destroy_client_context`

销毁客户端上下文并释放其内存。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nv">duckdb_destroy_client_context</span>(<span class="nv">
</span>  <span class="nv">duck
</span>  <span class="nv">context
</span>);
</code></pre></div></div>

##### 参数

* `context`: 要销毁的客户端上下文。

<br>

#### `duckdb_library_version`

返回链接的 DuckDB 的版本，开发版本带有版本后缀。

通常用于开发必须返回此版本以进行兼容性检查的 C 扩展。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">const</span> <span class="kt">char</span> *<span class="nv">duckdb_library_version</span>(<span class="nv">
</span>  <span class="nv">
</span>);
</code></pre></div></div>
<br>

#### `duckdb_get_table_names`

获取查询的（完全限定的）表名列表。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="nv">duckdb_get_table_names</span>(<span class="nv">
</span>  <span class="kt">duckdb_connection</span> <span class="nv">connection</span>,<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">query</span>,<span class="nv">
</span>  <span class="kt">bool</span> <span class="nv">qualified
</span>);
</code></pre></div></div>

##### 参数

* `connection`: 获取表名的连接。
* `query`: 获取表名的查询。
* `qualified`: 如果设置为 true，则返回完全限定的表名（catalog.schema.table），否则仅返回（未转义的）表名。

##### 返回值

包含查询的（完全限定的）表名的 `duckdb_value` 类型为 VARCHAR[]。必须使用 `duckdb_destroy_value` 销毁。

<br>