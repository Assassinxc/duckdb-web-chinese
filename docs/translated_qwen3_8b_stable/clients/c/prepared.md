---
---
layout: docu
redirect_from:
- /docs/api/c/prepared
- /docs/api/c/prepared/
- /docs/clients/c/prepared
title: 预编译语句
---

<!-- markdownlint-disable MD001 -->

预编译语句是一种参数化查询。查询使用问号（`?`）或美元符号（`$1`）表示查询的参数。之后可以将值绑定到这些参数上，然后使用这些参数执行预编译语句。一个查询可以被预编译一次并执行多次。

预编译语句有以下用途：

* 简化向函数提供参数，同时避免字符串拼接/SQL 注入攻击。
* 提高将要多次执行且参数不同的查询的速度。

DuckDB 在 C API 中支持预编译语句，使用 `duckdb_prepare` 方法。`duckdb_bind` 家族的函数用于为后续使用 `duckdb_execute_prepared` 执行预编译语句提供值。在我们完成预编译语句后，可以使用 `duckdb_destroy_prepare` 方法清理它。

## 示例

```c
duckdb_prepared_statement stmt;
duckdb_result result;
if (duckdb_prepare(con, "INSERT INTO integers VALUES ($1, $2)", &stmt) == DuckDBError) {
    // 处理错误
}

duckdb_bind_int32(stmt, 1, 42); // 参数索引从 1 开始计数！
duckdb_bind_int32(stmt, 2, 43);
// 第二个参数为 NULL 表示不请求结果集
duckdb_execute_prepared(stmt, NULL);
duckdb_destroy_prepare(&stmt);

// 我们也可以使用预编译语句查询结果集
if (duckdb_prepare(con, "SELECT * FROM integers WHERE i = ?", &stmt) == DuckDBError) {
    // 处理错误
}
duckdb_bind_int32(stmt, 1, 42);
duckdb_execute_prepared(stmt, &result);

// 对结果进行操作

// 清理
duckdb_destroy_result(&result);
duckdb_destroy_prepare(&stmt);
```

在调用 `duckdb_prepare` 之后，可以使用 `duckdb_nparams` 和 `duckdb_param_type` 检查预编译语句的参数。如果准备失败，可以通过 `duckdb_prepare_error` 获取错误信息。

`duckdb_bind` 家族的函数不一定要与预编译语句的参数类型完全匹配。值会自动转换为所需的类型。例如，对参数类型为 `DUCKDB_TYPE_INTEGER` 的参数调用 `duckdb_bind_int8` 会按预期工作。

> 警告 不要使用预编译语句将大量数据插入 DuckDB。相反，建议使用 [Appender]({% link docs/stable/clients/c/appender.md %}).

## API 参考概述

<!-- 本节由 scripts/generate_c_api_docs.py 生成 -->

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <a href="#duckdb_prepare"><span class="nf">duckdb_prepare</span></a>(<span class="kt">duckdb_connection</span> <span class="nv">connection</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">query</span>, <span class="kt">duckdb_prepared_statement</span> *<span class="nv">out_prepared_statement</span>);
<span class="kt">void</span> <a href="#duckdb_destroy_prepare"><span class="nf">duckdb_destroy_prepare</span></a>(<span class="kt">duckdb_prepared_statement</span> *<span class="nv">prepared_statement</span>);
<span class="kt">const</span> <span class="kt">char</span> *<a href="#duckdb_prepare_error"><span class="nf">duckdb_prepare_error</span></a>(<span class="kt">duckdb_prepared_statement</span> <span class="nv">prepared_statement</span>);
<span class="kt">idx_t</span> <a href="#duckdb_nparams"><span class="nf">duckdb_nparams</span></a>(<span class="kt">duckdb_prepared_statement</span> <span class="nv">prepared_statement</span>);
<span class="kt">const</span> <span class="kt">char</span> *<a href="#duckdb_parameter_name"><span class="nf">duckdb_parameter_name</span></a>(<span class="kt">duckdb_prepared_statement</span> <span class="nv">prepared_statement</span>, <span class="kt">idx_t</span> <span class="nv">index</span>);
<span class="kt">duckdb_type</span> <a href="#duckdb_param_type"><span class="nf">duckdb_param_type</span></a>(<span class="kt">duckdb_prepared_statement</span> <span class="nv">prepared_statement</span>, <span class="kt">idx
</span>);</code></pre></div></div>

#### `duckdb_prepare`

从查询创建一个预编译语句对象。

注意：在调用 `duckdb_prepare` 后，即使准备失败，也应始终使用 `duckdb_destroy_prepare` 销毁预编译语句。

如果准备失败，可以调用 `duckdb_prepare_error` 获取准备失败的原因。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_prepare</span>(<span class="nv">
</span>  <span class="kt">duckdb_connection</span> <span class="nv">connection</span>,<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">query</span>,<span class="nv">
</span>  <span class="kt">duckdb_prepared_statement</span> *<span class="nv">out_prepared_statement
</span>);</code></pre></div></div>

##### 参数

* `connection`: 连接对象
* `query`: 要预编译的 SQL 查询
* `out_prepared_statement`: 结果预编译语句对象

##### 返回值

成功返回 `DuckDBSuccess`，失败返回 `DuckDBError`。

<br>

#### `duckdb_destroy_prepare`

关闭预编译语句并释放所有分配给语句的内存。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nv">duckdb_destroy_prepare</span>(<span class="nv">
</span>  <span class="kt">duckdb_prepared_statement</span> *<span class="nv">prepared_statement
</span>);</code></pre></div></div>

##### 参数

* `prepared_statement`: 要销毁的预编译语句。

<br>

#### `duckdb_prepare_error`

返回与给定预编译语句关联的错误信息。如果预编译语句没有错误信息，将返回 `nullptr`。

错误信息不应被释放。当调用 `duckdb_destroy_prepare` 时，它将被释放。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">const</span> <span class="kt">char</span> *<span class="nv">duckdb_prepare_error</span>(<span class="nv">
</span>  <span class="kt">duckdb_pre
</span>);</code></pre></div></div>

##### 参数

* `prepared_statement`: 要获取错误信息的预编译语句。

##### 返回值

错误信息，如果没有错误信息则返回 `nullptr`。

<br>

#### `duckdb_nparams`

返回可以提供给给定预编译语句的参数数量。

如果查询未成功预编译，返回 0。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="nv">duckdb_nparams</span>(<span class="nv">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="nv">prepared_statement
</span>);</code></pre></div></div>

##### 参数

* `prepared_statement`: 获取参数数量的预编译语句。

<br>

#### `duckdb_parameter_name`

返回用于标识参数的名称。返回的字符串应使用 `duckdb_free` 释放。

如果索引超出提供的预编译语句范围，返回 NULL。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">const</span> <span class="kt">char</span> *<span class="nv">duckdb_parameter_name</span>(<span class="nv">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="nv">prepared_statement</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">index
</span>);</code></pre></div></div>

##### 参数

* `prepared_statement`: 获取参数名称的预编译语句。

<br>

#### `duckdb_param_type`

返回给定索引处参数的类型。

如果参数索引超出范围或语句未成功预编译，返回 `DUCKDB_TYPE_INVALID`。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_type</span> <span class="nv">duckdb_param_type</span>(<span class="nv">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="nv">prepared_statement</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">param_idx
</span>);</code></pre></div></div>

##### 参数

* `prepared_statement`: 预编译语句。
* `param_idx`: 参数索引。

##### 返回值

参数类型

<br>

#### `duckdb_param_logical_type`

返回给定索引处参数的逻辑类型。

如果参数索引超出范围或语句未成功预编译，返回 `nullptr`。

此调用的返回类型应使用 `duckdb_destroy_logical_type` 进行销毁。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_logical_type</span> <span class="nv">duckdb_param_logical_type</span>(<span class="nv">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="nv">prepared_statement</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">param_idx
</span>);</code></pre></div></div>

##### 参数

* `prepared_statement`: 预编译语句。
* `param_idx`: 参数索引。

##### 返回值

参数的逻辑类型

<br>

#### `duckdb_clear_bindings`

清除绑定到预编译语句的参数。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_clear_bindings</span>(<span class="nv">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="nv">prepared_statement
</span>);</code></pre></div></div>
<br>

#### `duckdb_prepared_statement_type`

返回将要执行的语句类型

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_statement_type</span> <span class="nv">duckdb_prepared_statement_type</span>(<span class="nv">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="nv">statement
</span>);</code></pre></div></div>

##### 参数

* `statement`: 预编译语句。

##### 返回值

duckdb_statement_type 值或 DUCKDB_STATEMENT_TYPE_INVALID

<br>