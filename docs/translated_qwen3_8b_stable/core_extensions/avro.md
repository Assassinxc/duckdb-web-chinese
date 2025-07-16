---
---
github_repository: https://github.com/duckdb/duckdb-avro
layout: docu
title: Avro 扩展
redirect_from:
- /docs/stable/extensions/avro
- /docs/stable/extensions/avro/
- /docs/extensions/avro
- /docs/extensions/avro/
---

`avro` 扩展使 DuckDB 能够读取 [Apache Avro](https://avro.apache.org) 文件。

> `avro` 扩展于 2024 年年底作为社区扩展发布（见 {% post_url 2024-12-09-duckdb-avro-extension %}），并在 2025 年初成为核心扩展。

## `read_avro` 函数

该扩展添加了一个 DuckDB 函数 `read_avro`。此函数可以这样使用：

```sql
FROM read_avro('⟨some_file⟩.avro');
```

此函数将 Avro 文件的内容暴露为一个 DuckDB 表。之后你可以使用任意的 SQL 构造来进一步转换这个表。

## 文件 I/O

`read_avro` 函数被集成到 DuckDB 的文件系统抽象中，这意味着你可以直接从例如 HTTP 或 S3 源读取 Avro 文件。例如：

```sql
FROM read_avro('http://blobs.duckdb.org/data/userdata1.avro');
FROM read_avro('s3://⟨your-bucket⟩/⟨some_file⟩.avro');
```

应该“只需”工作。

你还可以在单次读取调用中 *glob* 多个文件，或向函数传递文件列表：

```sql
FROM read_avro('some_file_*.avro');
FROM read_avro(['some_file_1.avro', 'some_file_2.avro']);
```

如果文件名中包含有价值的信息（不幸的是这种情况很常见），你可以将 `filename` 参数传递给 `read_avro`：

```sql
FROM read_avro('some_file_*.avro', filename=true);
```

这将在结果集中添加一个额外的列，包含 Avro 文件的实际文件名。

## 架构转换

此扩展会自动将 Avro 架构转换为 DuckDB 架构。*所有* Avro 类型都可以被转换，除了 *递归类型定义*，这 DuckDB 不支持。

类型映射非常直接，除了 Avro 处理 `NULL` 的方式。不同于其他系统，Avro 并不将 `NULL` 视为 `INTEGER` 等范围中的一个可能值，而是用实际类型与一个特殊的 `NULL` 类型的联合来表示 `NULL`。这与 DuckDB 不同，DuckDB 中任何值都可以是 `NULL`。当然，DuckDB 也支持 `UNION` 类型，但使用起来会很麻烦。

此扩展在可能的情况下 *简化* Avro 架构：任何类型与特殊 null 类型的 Avro 联合类型将简化为非 null 类型。例如，一个 Avro 记录的联合类型 `["int","null"]` 将成为 DuckDB 的 `INTEGER`，这在某些情况下恰好是 `NULL`。同样，一个只包含单一类型的 Avro 联合类型将被转换为该类型。例如，一个 Avro 记录的联合类型 `["int"]` 也变为 DuckDB 的 `INTEGER`。

此扩展还“扁平化”了 Avro 架构。Avro 将表定义为根级的“record”字段，这与 DuckDB 的 `STRUCT` 字段相同。为了更方便的处理，此扩展将单个根级 record 的条目转换为根级列。

## 实现

在内部，此扩展使用了“官方”的 [Apache Avro C API](https://avro.apache.org/docs/++version++/api/c/)，尽管进行了少量修改以允许从内存中读取 Avro 文件。

## 局限性与未来计划

* 此扩展目前在读取单个（大）Avro 文件或读取文件列表时，**不使用并行处理**。在后者的情况下支持并行处理已在计划中。
* 目前不支持 **投影** 或 **过滤下推**，但这也在后期计划中。
* 由于 Avro 库依赖的问题，目前不支持 DuckDB 的 Wasm 或 Windows-MinGW 构建（叹气）。我们计划最终解决这个问题。
* 如上所述，DuckDB 无法表达 Avro 的递归类型定义，这不太可能改变。
* 目前不支持允许用户提供单独的 Avro 架构文件。这不太可能改变，我们看到的所有 Avro 文件都已嵌入其架构。
* 目前不支持 `union_by_name` 标志，这是其他 DuckDB 读取器支持的功能。这计划在未来实现。