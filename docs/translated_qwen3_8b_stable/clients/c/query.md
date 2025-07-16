---
---
layout: docu
redirect_from:
- /docs/api/c/query
- /docs/api/c/query/
- /docs/clients/c/query
title: 查询
---

<!-- markdownlint-disable MD001 -->

`duckdb_query` 方法允许从 C 语言在 DuckDB 中运行 SQL 查询。此方法接受两个参数，一个（以空字符结尾）的 SQL 查询字符串和一个 `duckdb_result` 结果指针。结果指针可以是 `NULL`，如果应用程序不关心结果集或查询不产生结果。在结果被消费后，应使用 `duckdb_destroy_result` 方法清理结果。

可以使用多种方法从 `duckdb_result` 对象中提取元素。`duckdb_column_count` 可用于提取列数。`duckdb_column_name` 和 `duckdb_column_type` 可用于提取单个列的名称和类型。

## 示例

```c
duckdb_state state;
duckdb_result result;

// 创建一个表
state = duckdb_query(con, "CREATE TABLE integers (i INTEGER, j INTEGER);", NULL);
if (state == DuckDBError) {
    // 处理错误
}
// 向表中插入三行数据
state = duckdb_query(con, "INSERT INTO integers VALUES (3, 4), (5, 6), (7, NULL);", NULL);
if (state == DuckDBError) {
    // 处理错误
}
// 再次查询数据
state = duckdb_query(con, "SELECT * FROM integers", &result);
if (state == DuckDBError) {
    // 处理错误
}
// 处理结果
// ...

// 在使用完结果后销毁结果
duckdb_destroy_result(&result);
```

## 值提取

可以使用 `duckdb_fetch_chunk` 函数或 `duckdb_value` 方便函数来提取值。`duckdb_fetch_chunk` 函数直接将数据块以 DuckDB 原生数组格式传递给您，因此可以非常快速。`duckdb_value` 函数执行边界检查和类型检查，并会自动将值转换为所需类型。这使得它们更方便和易于使用，但速度更慢。

有关更多信息，请参阅 [类型]({% link docs/stable/clients/c/types.md %}) 页面。

> 为了获得最佳性能，请使用 `duckdb_fetch_chunk` 从查询结果中提取数据。
> `duckdb_value` 函数会执行内部类型检查、边界检查和转换，因此它们速度较慢。

### `duckdb_fetch_chunk`

下面是一个完整的示例，使用 `duckdb_fetch_chunk` 函数将上述结果打印为 CSV 格式。请注意，该函数不是通用的：我们需要确切知道结果列的类型。

```c
duckdb_database db;
duckdb_connection con;
duckdb_open(nullptr, &db);
duckdb_connect(db, &con);

duckdb_result res;
duckdb_query(con, "CREATE TABLE integers (i INTEGER, j INTEGER);", NULL);
duckdb_query(con, "INSERT INTO integers VALUES (3, 4), (5, 6), (7, NULL);", NULL);
duckdb_query(con, "SELECT * FROM integers;", &res);

// 循环直到结果耗尽
while (true) {
    duckdb_data_chunk result = duckdb_fetch_chunk(res);
    if (!result) {
        // 结果已耗尽
        break;
    }
    // 获取数据块中的行数
    idx_t row_count = duckdb_data_chunk_get_size(result);
    // 获取第一个列
    duckdb_vector col1 = duckdb_data_chunk_get_vector(result, 0);
    int32_t *col1_data = (int32_t *) duckdb_vector_get_data(col1);
    uint64_t *col1_validity = duckdb_vector_get_validity(col1);

    // 获取第二个列
    duckdb_vector col2 = duckdb_data_chunk_get_vector(result, 1);
    int32_t *col2_data = (int32_t *) duckdb_vector_get_data(col2);
    uint64_t *col2_validity = duckdb_vector_get_validity(col2);

    // 遍历行
    for (idx_t row = 0; row < row_count; row++) {
        if (duckdb_validity_row_is_valid(col1_validity, row)) {
            printf("%d", col1_data[row]);
        } else {
            printf("NULL");
        }
        printf(",");
        if (duckdb_validity_row_is_valid(col2_validity, row)) {
            printf("%d", col2_data[row]);
        } else {
            printf("NULL");
        }
        printf("\n");
    }
    duckdb_destroy_data_chunk(&result);
}
// 清理
duckdb_destroy_result(&res);
duckdb_disconnect(&con);
duckdb_close(&db);
```

这将打印以下结果：

```csv
3,4
5,6
7,NULL
```

### `duckdb_value`

> 已弃用 `duckdb_value` 函数已弃用，并计划在未来版本中移除。

下面是一个使用 `duckdb_value_varchar` 函数将上述结果打印为 CSV 格式的示例。请注意，该函数是通用的：我们不需要知道结果列的类型。

```c
// 使用 `duckdb_value_varchar` 函数将上述结果打印为 CSV 格式
idx_t row_count = duckdb_row_count(&result);
idx_t column_count = duckdb_column_count(&result);
for (idx_t row = 0; row < row_count; row++) {
    for (idx_t col = 0; col < column_count; col++) {
        if (col > 0) printf(",");
        auto str_val = duckdb_value_varchar(&result, col, row);
        printf("%s", str_val);
        duckdb_free(str_val);
   }
   printf("\n");
}
```

## API 参考概述

<!-- 本节由 scripts/generate_c_api_docs.py 脚本生成 -->

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <a href="#duckdb_query"><span class="nf">duckdb_query</span></a>(<span class="kt">duckdb_connection</span> <span class="nv">connection</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">query</span>, <span class="kt">duckdb_result</span> *<span class="nv">out_result</span>);
<span class="kt">void</span> <a href="#duckdb_destroy_result"><span class="nf">duckdb_destroy_result</span></a>(<span class="kt">duckdb_result</span> *<span class="nv">result</span>);
<span class="kt">const</span> <span class="kt">char</span> *<a href="#duckdb_column_name"><span class="nf">duckdb_column_name</span></a>(<span class="kt">duckdb_result</span> *<span class="nv">result</span>, <span class="kt">idx_t</span> <span class="nv">col</span>);
<span class="kt">duckdb_type</span> <a href="#duckdb_column_type"><span class="nf">duckdb_column_type</span></a>(<span class="kt">duckdb_result</span> *<span class="nv">result</span>, <span class="kt">idx_t</span> <span class="nv">col</span>);
<span class="kt">duckdb_statement_type</span> <a href="#duckdb_result_statement_type"><span class="nf">duckdb_result_statement_type</span></a>(<span class="kt">duckdb_result</span> <span class="nv">result</span>);
<span class="kt">duckdb_logical_type</span> <a href="#duckdb_column_logical_type"><span class="nf">duckdb_column_logical_type</span></a>(<span class="kt">duckdb_result</span> *<span class="nv">result</span>, <span class="kt">idx_t</span> <span class="nv">col</span>);
<span class="kt">idx_t</span> <a href="#duckdb_column_count"><span class="nf">duckdb_column_count</span></a>(<span class="kt">duckdb_result</span> *<span class="nv">result</span>);
<span class="kt">idx_t</span> <a href="#duckdb_row_count"><span class="nf">duckdb_row_count</span></a>(<span class="kt">duckdb_result</span> *<span class="nv">result</span>);
<span class="kt">idx_t</span> <a href="#duckdb_rows_changed"><span class="nf">duckdb_rows_changed</span></a>(<span class="kt">duckdb_result</span> *<span class="nv">result</span>);
<span class="kt">void</span> *<a href="#duckdb_column_data"><span class="nf">duckdb_column_data</span></a>(<span class="kt">duckdb_result</span> *<span class="nv">result</span>, <span class="kt">idx_t</span> <span class="nv">col</span>);
<span class="kt">bool</span> *<a href="#duckdb_nullmask_data"><span class="nf">duckdb_nullmask_data</span></a>(<span class="kt">duckdb_result</span> *<span class="nv">result</span>, <span class="kt">idx_t</span> <span class="nv">col</span>);
<span class="kt">const</span> <span class="kt">char</span> *<a href="#duckdb_result_error"><span class="nf">duckdb_result_error</span></a>(<span class="kt">duckdb_result</span> *<span class="nv">result</span>);
<span class="kt">duckdb_error_type</span> <a href="#duckdb_result_error_type"><span class="nf">duckdb_result_error_type</span></a>(<span class="kt">duckdb_result</span> *<span class="nv">result</span>);
</code></pre></div></div>

#### `duckdb_query`

在连接中执行 SQL 查询，并将完整的（物化）结果存储在 `out_result` 指针中。
如果查询执行失败，将返回 `DuckDBError`，并通过调用 `duckdb_result_error` 获取错误信息。

注意：在运行 `duckdb_query` 后，即使查询失败，也必须调用 `duckdb_destroy_result` 销毁结果对象，否则结果中存储的错误将无法正确释放。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_query</span>(<span class="nv">
</span>  <span class="kt">duckdb_connection</span> <span class="nv">connection</span>,<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">query</span>,<span class="nv">
</span>  <span class="kt">duckdb_result</span> *<span class="nv">out_result
</span>);
</code></pre></div></div>

##### 参数

* `connection`：执行查询的连接。
* `query`：要运行的 SQL 查询。
* `out_result`：查询结果。

##### 返回值

成功返回 `DuckDBSuccess`，失败返回 `DuckDBError`。

<br>

#### `duckdb_destroy_result`

关闭结果并释放该结果分配的所有内存。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nv">duckdb_destroy_result</span>(<span class="nv">
</span>  <span class="kt">duckdb_result</span> *<span class="nv">result
</span>);
</code></pre></div></div>

##### 参数

* `result`：要销毁的结果。

<br>

#### `duckdb_column_name`

返回指定列的列名。结果不需要释放；列名将在结果销毁时自动销毁。

如果列超出范围，返回 `NULL`。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">const</span> <span class="kt">char</span> *<span class="nv">duckdb_column_name</span>(<span class="nv">
</span>  <span class="kt">duckdb_result</span> *<span class="nv">result</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">col
</span>);
</code></pre></div></div>

##### 参数

* `result`：获取列名的结果对象。
* `col`：列索引。

##### 返回值

指定列的列名。

<br>

#### `duckdb_column_type`

返回指定列的列类型。

如果列超出范围，返回 `DUCKDB_TYPE_INVALID`。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_type</span> <span class="nv">duckdb_column_type</span>(<span class="nv">
</span>  <span class="kt">duckdb_result</span> *<span class="nv">result</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <
</span>  <span class="kt">idx_t</span> <span class="nv">col
</span>);
</code></pre></div></div>

##### 参数

* `result`：获取列类型的结果对象。
* `col`：列索引。

##### 返回值

指定列的列类型。

<br>

#### `duckdb_result_statement_type`

返回已执行语句的语句类型。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_statement_type</span> <span class="nv">duckdb_result_statement_type</span>(<span class="nv">
</span>  <span class="kt">duckdb_result</span> <span class="nv">result
</span>);
</code></pre></div></div>

##### 参数

* `result`：获取语句类型的結果对象。

##### 返回值

`duckdb_statement_type` 值或 `DUCKDB_STATEMENT_TYPE_INVALID`

<br>

#### `duckdb_column_logical_type`

返回指定列的逻辑列类型。

此调用的返回类型应使用 `duckdb_destroy_logical_type` 进行销毁。

如果列超出范围，返回 `NULL`。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_logical_type</span> <span class="nv">duckdb_column_logical_type</span>(<span class="nv">
</span>  <span class="kt">duckdb_result</span> *<span class="nv">result</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">col
</span>);
</code></pre></div></div>

##### 参数

* `result`：获取列类型的结果对象。
* `col`：列索引。

##### 返回值

指定列的逻辑列类型。

<br>

#### `duckdb_column_count`

返回结果对象中列的数量。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="nv">duckdb_column_count</span>(<span class="nv">
</span>  <span class="kt">duck
</span>  <span class="kt">duckdb_result</span> *<span class="nv">result
</span>);
</code></pre></div></div>

##### 参数

* `result`：结果对象。

##### 返回值

结果对象中的列数。

<br>

#### `duckdb_row_count`

> 警告 已弃用。此方法将在未来的版本中移除。

返回结果对象中的行数。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="nv">duckdb_row_count</span>(<span class="nv">
</span>  <span class="kt">duckdb_result</span> *<span class="nv">result
</span>);
</code></pre></div></div>

##### 参数

* `result`：结果对象。

##### 返回值

结果对象中的行数。

<br>

#### `duckdb_rows_changed`

返回结果中查询更改的行数。这仅适用于 INSERT/UPDATE/DELETE 查询。对于其他查询，rows_changed 将为 0。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="nv">duckdb_rows_changed</span>(<span class="nv">
</span>  <span class="kt">duckdb_result</span> *<span class="nv">result
</span>);
</code></pre></div></div>

##### 参数

* `result`：结果对象。

##### 返回值

更改的行数。

<br>

#### `duckdb_column_data`

> 已弃用 此方法已弃用。请改用 `duckdb_result_get_chunk`。

以列式格式返回结果特定列的数据。

该函数返回一个密集数组，包含结果数据。数组中存储的确切类型取决于对应的 duckdb_type（由 `duckdb_column_type` 提供）。要了解数据应以何种类型访问，请参阅 [类型部分](types) 中的注释或 `DUCKDB_TYPE` 枚举。

例如，对于类型为 `DUCKDB_TYPE_INTEGER` 的列，可以按以下方式访问行：
```c
int32_t *data = (int32_t *) duckdb_column_data(&result, 0);
printf("Data for row %d: %d\n", row, data[row]);
```

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> *<span class="nv">duckdb_column_data</span>(<span class="nv">
</span>  <span class="kt">duckdb_result</span> *<span class="nv">result</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">col
</span>);
</code></pre></div></div>

##### 参数

* `result`：获取列数据的结果对象。
* `col`：列索引。

##### 返回值

指定列的列数据。

<br>

#### `duckdb_nullmask_data`

> 已弃用 此方法已弃用。请改用 `duckdb_result_get_chunk`。

以列式格式返回结果特定列的 nullmask。nullmask 表示每行是否为 `NULL`。如果某行是 `NULL`，则由 `duckdb_column_data` 提供的数组中的值是未定义的。

```c
int32_t *data = (int32_t *) duckdb_column_data(&result, 0);
bool *nullmask = duckdb_nullmask_data(&result, 0);
if (nullmask[row]) {
printf("Data for row %d: NULL\n", row);
} else {
printf("Data for row %d: %d\n", row, data[row]);
}
```

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">bool</span> *<span class="nv">duckdb_nullmask_data</span>(<span class="nv">
</span>  <span class="kt">duckdb_result</span> *<span class="nv">result</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">col
</span>);
</code></pre></div></div>

##### 参数

* `result`：获取 nullmask 的结果对象。
* `col`：列索引。

##### 返回值

指定列的 nullmask。

<br>

#### `duckdb_result_error`

返回结果中的错误信息。只有在 `duckdb_query` 返回 `DuckDBError` 时才会设置错误。

此函数的结果不得释放。当调用 `duckdb_destroy_result` 时，它将被清理。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">const</span> <span class="kt">char</span> *<span class="nv">duckdb_result_error</span>(<span class="nv">
</span>  <span class="kt">duckdb_result</span> *<span class="nv">result
</span>);
</code></pre></div></div>

##### 参数

* `result`：获取错误的结果对象。

##### 返回值

结果的错误信息。

<br>

#### `duckdb_result_error_type`

返回结果中的错误类型。只有在 `duckdb_query` 返回 `DuckDBError` 时才会设置错误类型。

##### 语法

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_error_type</span> <span class="nv">duckdb_result_error_type</span>(<span class="nv">
</span>  <span class="kt">duckdb_result</span> *<span class="nv">result
</span>);
</code></pre></div></div>

##### 参数

* `result`：获取错误类型的结果对象。

##### 返回值

结果的错误类型。

<br>