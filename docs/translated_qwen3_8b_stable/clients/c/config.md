---
---
layout: docu
redirect_from:
- /docs/api/c/config
- /docs/api/c/config/
- /docs/clients/c/config
title: 配置
---

<!-- markdownlint-disable MD001 -->

可以通过配置选项更改数据库系统的不同设置。请注意，其中许多设置也可以使用 [`PRAGMA` 语句](../../configuration/pragmas) 后续进行更改。配置对象应被创建、填充值并传递给 `duckdb_open_ext`。

## 示例

```c
duckdb_database db;
duckdb_config config;

// 创建配置对象
if (duckdb_create_config(&config) == DuckDBError) {
    // 处理错误
}
// 设置一些配置选项
duckdb_set_config(config, "access_mode", "READ_WRITE"); // 或 READ_ONLY
duckdb_set_config(config, "threads", "8");
duckdb_set_config(config, "max_memory", "8GB");
duckdb_set_config(config, "default_order", "DESC");

// 使用配置打开数据库
if (duckdb_open_ext(NULL, &db, config, NULL) == DuckDBError) {
    // 处理错误
}
// 清理配置对象
duckdb_destroy_config(&config);

// 运行查询...

// 清理
duckdb_close(&db);
```

## API 参考概览

<!-- 此部分由 scripts/generate_c_api_docs.py 生成 -->

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <a href="#duckdb_create_config"><span class="nf">duckdb_create_config</span></a>(<span class="kt">duckdb_config</span> *<span class="nv">out_config</span>);
<span class="kt">size_t</span> <a href="#duckdb_config_count"><span class="nf">duckdb_config_count</span></a>();
<span class="kt">duckdb_state</span> <a href="#duckdb_get_config_flag"><span class="nf">duckdb_get_config_flag</span></a>(<span class="kt">size_t</span> <span class="nv">index</span>, <span class="kt">const</span> <span class="kt">char</span> **<span class="nv">out_name</span>, <span class="kt">const</span> <span class="kt">char</span> **<span class="nv">out_description</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_set_config"><span class="nf">duckdb_set_config</span></a>(<span class="kt">duckdb_config</span> <span class="nv">config</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">name</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">option</span>);
<span class="kt">void</span> <a href="#duckdb_destroy_config"><span class="nf">duckdb_destroy_config</span></a>(<span class="kt">duckdb_config</span> *<span class="nv">config</span>);
</code></pre></div></div>

#### `duckdb_create_config`

初始化一个空的配置对象，可用于通过 `duckdb_open_ext` 提供 DuckDB 实例的启动选项。
`duckdb_config` 必须使用 `duckdb_destroy_config` 进行销毁。

除非发生内存分配失败，否则此函数总是成功。

请注意，即使函数返回 `DuckDBError`，也应始终调用 `duckdb_destroy_config` 来销毁结果配置。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_create_config</span>(<span class="nv">
</span>  <span class="kt">duckdb_config</span> *<span class="nv">out_config
</span>);
</code></pre></div></div>

##### 参数

* `out_config`: 结果配置对象。

##### 返回值

成功返回 `DuckDBSuccess`，失败返回 `DuckDBError`。

<br>

#### `duckdb_config_count`

返回可用于 `duckdb_get_config_flag` 的配置选项总数。

不应在循环中调用此函数，因为它内部会遍历所有选项。

##### 返回值

可用的配置选项数量。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">size_t</span> <span class="nv">duckdb_config_count</span>(<span class="nv">
</span>  <span class="nv">
</span>);
</code></pre></div></div>
<br>

#### `duckdb_get_config_flag`

获取特定配置选项的可读名称和描述。这可用于例如显示配置选项。除非 `index` 超出范围（即 `>= duckdb_config_count`），否则此函数将成功。

返回的名称或描述不得被释放。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_get_config_flag</span>(<span class="nv">
</span>  <span class="kt">size_t</span> <span class="nv">index</span>,<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> **<span class="nv">out_name</span>,<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> **<span class="nv">out_description
</span>);
</code></pre></div></div>

##### 参数

* `index`: 配置选项的索引（介于 0 和 `duckdb_config_count` 之间）
* `out_name`: 配置标志的名称。
* `out_description`: 配置标志的描述。

##### 返回值

成功返回 `DuckDBSuccess`，失败返回 `DuckDBError`。

<br>

#### `duckdb_set_config`

为指定的配置设置指定的选项。配置选项通过名称来标识。
要获取配置选项列表，请参阅 `duckdb_get_config_flag`。

在源代码中，配置选项在 `config.cpp` 中定义。

如果名称无效，或为选项提供的值无效，此函数可能失败。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_set_config</span>(<span class="nv">
</span>  <span class="kt">duckdb_config</span> <span class="nv">config</span>,<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">name</span>,<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">option
</span>);
</code></pre></div></div>

##### 参数

* `config`: 设置选项的配置对象。
* `name`: 要设置的配置标志的名称。
* `option`: 设置配置标志的值。

##### 返回值

成功返回 `DuckDBSuccess`，失败返回 `DuckDBError`。

<br>

#### `duckdb_destroy_config`

销毁指定的配置对象并释放对象所占用的所有内存。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nv">duckdb_destroy_config</span>(<span class="nv">
</span>  <span class="kt">duckdb_config</span> *<span class="nv">config
</span>);
</code></pre></div></div>

##### 参数

* `config`: 要销毁的配置对象。

<br>