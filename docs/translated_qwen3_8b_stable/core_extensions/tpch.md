---
---
github_directory: https://github.com/duckdb/duckdb/tree/main/extension/tpch
layout: docu
title: TPC-H 扩展
redirect_from:
- /docs/stable/extensions/tpch
- /docs/stable/extensions/tpch/
- /docs/extensions/tpch
- /docs/extensions/tpch/
---

`tpch` 扩展实现了 [TPC-H 基准测试](https://www.tpc.org/tpch/) 的数据生成器和查询功能。

## 安装和加载

`tpch` 扩展在某些 DuckDB 构建中默认提供，否则会在首次使用时透明地[自动加载]({% link docs/stable/core_extensions/overview.md %}#autoloading-extensions)。
如果你想手动安装和加载它，请运行：

```sql
INSTALL tpch;
LOAD tpch;
```

## 使用

### 生成数据

要为 scale factor 1 生成数据，请使用：

```sql
CALL dbgen(sf = 1);
```

调用 `dbgen` 不会清理现有的 TPC-H 表。
要清理现有的表，请在运行 `dbgen` 前使用 `DROP TABLE`：

```sql
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS lineitem;
DROP TABLE IF EXISTS nation;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS part;
DROP TABLE IF EXISTS partsupp;
DROP TABLE IF EXISTS region;
DROP TABLE IF EXISTS supplier;
```

### 运行查询

要运行一个查询，例如查询 4，请使用：

```sql
PRAGMA tpch(4);
```

| o_orderpriority | order_count |
| --------------- | ----------: |
| 1-URGENT        |       10594 |
| 2-HIGH          |       10476 |
| 3-MEDIUM        |       10410 |
| 4-NOT SPECIFIED |       10556 |
| 5-LOW           |       10487 |

### 列出查询

要列出所有 22 个查询，请运行：

```sql
FROM tpch_queries();
```

此函数返回一个包含 `query_nr` 和 `query` 列的表。

### 列出预期结果

要生成 scale factor 0.01、0.1 和 1 的所有查询的预期结果，请运行：

```sql
FROM tpch_answers();
```

此函数返回一个包含 `query_nr`、`scale_factor` 和 `answer` 列的表。

## 生成模式

可以通过将 scale factor 设置为 0 来在不生成任何数据的情况下生成 TPC-H 的模式：

```sql
CALL dbgen(sf = 0);
```

## 数据生成器参数

数据生成器函数 `dbgen` 的参数如下：

| 名称        | 类型       | 描述                                                                                                                       |
| ----------- | ---------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `catalog`   | `VARCHAR`  | 目标目录                                                                                                                    |
| `children`  | `UINTEGER` | 分区数量                                                                                                              |
| `overwrite` | `BOOLEAN`  | （未使用）                                                                                                                        |
| `sf`        | `DOUBLE`   | scale factor                                                                                                                      |
| `step`      | `UINTEGER` | 定义要生成的分区，从 0 到 `children` - 1 索引。当 `children` 参数定义时必须定义 |
| `suffix`    | `VARCHAR`  | 将 `suffix` 追加到表名                                                                                              |

## 预生成的数据集

TPC-H 的预生成 DuckDB 数据库可供下载：

* [`tpch-sf1.db`](https://blobs.duckdb.org/data/tpch-sf1.db) (250 MB)
* [`tpch-sf3.db`](https://blobs.duckdb.org/data/tpch-sf3.db) (754 MB)
* [`tpch-sf10.db`](https://blobs.duckdb.org/data/tpch-sf10.db) (2.5 GB)
* [`tpch-sf30.db`](https://blobs.duckdb.org/data/tpch-sf30.db) (7.6 GB)
* [`tpch-sf100.db`](https://blobs.duckdb.org/data/tpch-sf100.db) (26 GB)
* [`tpch-sf300.db`](https://blobs.duckdb.org/data/tpch-sf300.db) (78 GB)
* [`tpch-sf1000.db`](https://blobs.duckdb.org/data/tpch-sf1000.db) (265 GB)
* [`tpch-sf3000.db`](https://blobs.duckdb.org/data/tpch-sf3000.db) (796 GB)

## 数据生成器资源使用情况

为大型 scale factor 生成 TPC-H 数据集需要大量时间。
此外，如果在单一步骤中进行生成，还需要大量内存。
以下表格给出了使用 128 个线程生成包含生成的 TPC-H 数据集的 DuckDB 数据库文件所需的资源估计。

| scale factor | 数据库大小 | 生成时间 | 单一步骤生成的内存使用 |
| -----------: | ------------: | --------------: | ------------------------------------: |
|          100 |         26 GB |      17 分钟 |                                 71 GB |
|          300 |         78 GB |      51 分钟 |                                211 GB |
|        1,000 |        265 GB |  2 h 53 分钟 |                                647 GB |
|        3,000 |        796 GB |  8 h 30 分钟 |                               1799 GB |

上述数字是通过单一步骤运行 `dbgen` 函数获得的，例如：

```sql
CALL dbgen(sf = 300);
```

如果你的内存有限，可以分步骤运行 `dbgen` 函数。
例如，你可以分 10 步生成 SF300：

```sql
CALL dbgen(sf = 300, children = 10, step = 0);
CALL dbgen(sf = 300, children = 10, step = 1);
...
CALL dbgen(sf = 300, children = 10, step = 9);
```

## 局限性

`tpch(⟨query_id⟩)`{:.language-sql .highlight} 函数运行一个固定 TPC-H 查询，并使用预定义的绑定参数（也称为替换参数）。无法使用 `tpch` 扩展更改查询参数。要运行符合 TPC-H 基准测试规定的查询，请使用 TPC-H 框架实现。