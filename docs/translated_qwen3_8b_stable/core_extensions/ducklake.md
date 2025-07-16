---
---
github_repository: https://github.com/duckdb/ducklake
layout: docu
title: DuckLake
redirect_from:
- /ducklake
- /docs/extensions/ducklake
- /docs/extensions/ducklake/
---

> DuckLake 于 2025 年 5 月发布。
> 阅读 [公告博客文章]({% post_url 2025-05-27-ducklake %}).

`ducklake` 扩展支持连接存储在 [DuckLake 格式](http://ducklake.select/ )中的数据库：

## 安装和加载

要安装 `ducklake`，请运行：

```sql
INSTALL ducklake;
```

`ducklake` 扩展将在首次使用 `ATTACH` 子句时透明地[自动加载]({% link docs/stable/core_extensions/overview.md %}#autoloading-extensions)。
如果你想手动加载它，请运行：

```sql
LOAD ducklake;
```

## 使用

```sql
ATTACH 'ducklake:metadata.ducklake' AS my_ducklake (DATA_PATH 'data_files');
USE my_ducklake;
```

## 表

在 DuckDB 中，`ducklake` 扩展将 [目录表](http://ducklake.select/docs/stable/specification/tables/overview) 存储在 `__ducklake_metadata_⟨my_ducklake⟩`{:.language-sql .highlight} 目录中。

## 函数

请注意，DuckLake 注册了多个函数。
这些函数应以目录名称作为第一个参数调用，例如：

```sql
FROM ducklake_snapshots('my_ducklake');
```

```text
┌─────────────┬────────────────────────────┬────────────────┬──────────────────────────┐
│ snapshot_id │       snapshot_time        │ schema_version │         changes          │
│    int64    │  timestamp with time zone  │     int64      │ map(varchar, varchar[])  │
├─────────────┼────────────────────────────┼────────────────┼──────────────────────────┤
│      0      │ 2025-05-26 11:41:10.838+02 │       0        │ {schemas_created=[main]} │
└─────────────┴────────────────────────────┴────────────────┴──────────────────────────┘
```

### `ducklake_snapshots`

返回存储在 DuckLake 目录名称 `catalog` 中的快照。

| 参数名称 | 参数类型 | 命名参数 | 描述 |
| -------------- | -------------- | --------------- | ----------- |
| `catalog`      | `VARCHAR`      | 否              |             |

信息编码到具有以下模式的表中：

| 列名称      | 列类型                |
| ---------------- | -------------------------- |
| `snapshot_id`    | `BIGINT`                   |
| `snapshot_time`  | `TIMESTAMP WITH TIME ZONE` |
| `schema_version` | `BIGINT`                   |
| `changes`        | `MAP(VARCHAR, VARCHAR[])`  |

### `ducklake_table_info`

`ducklake_table_info` 函数返回存储在 DuckLake 目录名为 `catalog` 的表的信息。

| 参数名称 | 参数类型 | 命名参数 | 描述 |
| -------------- | -------------- | --------------- | ----------- |
| `catalog`      | `VARCHAR`      | 否              |             |

信息编码到具有以下模式的表中：

| 列名称              | 列类型 |
| ------------------------ | ----------- |
| `table_name`             | `VARCHAR`   |
| `schema_id`              | `BIGINT`    |
| `table_id`               | `BIGINT`    |
| `table_uuid`             | `UUID`      |
| `file_count`             | `BIGINT`    |
| `file_size_bytes`        | `BIGINT`    |
| `delete_file_count`      | `BIGINT`    |
| `delete_file_size_bytes` | `BIGINT`    |

### `ducklake_table_insertions`

`ducklake_table_insertions` 函数返回给定表在指定版本或时间戳快照之间的插入行。
该函数有两种变体，取决于 `start_snapshot` 和 `end_snapshot` 是否具有 `BIGINT` 或 `TIMESTAMP WITH TIME ZONE` 类型。

| 参数名称   | 参数类型                        | 命名参数 | 描述 |
| ---------------- | ------------------------------------- | --------------- | ----------- |
| `catalog`        | `VARCHAR`                             | 否              |             |
| `schema_name`    | `VARCHAR`                             | 否              |             |
| `table_name`     | `VARCHAR`                             | 否              |             |
| `start_snapshot` | `BIGINT` / `TIMESTAMP WITH TIME ZONE` | 否              |             |
| `end_snapshot`   | `BIGINT` / `TIMESTAMP WITH TIME ZONE` | 否              |             |

函数返回的表的模式等同于表 `table_name` 的模式。

### `ducklake_table_deletions`

`ducklake_table_deletions` 函数返回给定表在指定版本或时间戳快照之间的删除行。
该函数有两种变体，取决于 `start_snapshot` 和 `end_snapshot` 是否具有 `BIGINT` 或 `TIMESTAMP WITH TIME ZONE` 类型。

| 参数名称   | 参数类型                        | 命名参数 | 描述 |
| ---------------- | ------------------------------------- | --------------- | ----------- |
| `catalog`        | `VARCHAR`                             | 否              |             |
| `schema_name`    | `VARCHAR`                             | 否              |             |
| `table_name`     | `VARCHAR`                             | 否              |             |
| `start_snapshot` | `BIGINT` / `TIMESTAMP WITH TIME ZONE` | 否              |             |
| `end_snapshot`   | `BIGINT` / `TIMESTAMP WITH TIME ZONE` | 否              |             |

函数返回的表的模式等同于表 `table_name` 的模式。

### `ducklake_table_changes`

`ducklake_table_changes` 函数返回给定表在指定版本或时间戳快照之间的更改行。
该函数有两种变体，取决于 `start_snapshot` 和 `end_snapshot` 是否具有 `BIGINT` 或 `TIMESTAMP WITH TIME ZONE` 类型。

| 参数名称   | 参数类型                        | 命名参数 | 描述 |
| ---------------- | ------------------------------------- | --------------- | ----------- |
| `catalog`        | `VARCHAR`                             | 否              |             |
| `schema_name`    | `VARCHAR`                             | 否              |             |
| `table_name`     | `VARCHAR`                             | 否              |             |
| `start_snapshot` | `BIGINT` / `TIMESTAMP WITH TIME ZONE` | 否              |             |
| `end_snapshot`   | `BIGINT` / `TIMESTAMP WITH TIME ZONE` | 否              |             |

函数返回的表的模式包含以下三列加上表 `table_name` 的模式。

| 列名称   | 列类型 | 描述                              |
| ------------- | ----------- | ---------------------------------------- |
| `snapshot_id` | `BIGINT`    |                                          |
| `rowid`       | `BIGINT`    |                                          |
| `change_type` | `VARCHAR`   | 更改类型: `insert` 或 `delete` |

## 命令

### `ducklake_cleanup_old_files`

`ducklake_cleanup_old_files` 函数清理 DuckLake 中由 `catalog` 指定的旧文件。
成功时，它返回一个包含单列 (`Success`) 且 0 行的表。

| 参数名称 | 参数类型             | 命名参数 | 描述 |
| -------------- | -------------------------- | --------------- | ----------- |
| `catalog`      | `VARCHAR`                  | 否              |             |
| `cleanup_all`  | `BOOLEAN`                  | 是             |             |
| `dry_run`      | `BOOLEAN`                  | 是             |             |
| `older_than`   | `TIMESTAMP WITH TIME ZONE` | 是             |             |

### `ducklake_expire_snapshots`

`ducklake_expire_snapshots` 函数根据 `versions` 参数指定的版本或 `older_than` 参数指定的旧版本来过期快照。
成功时，它返回一个包含单列 (`Success`) 且 0 行的表。

| 参数名称 | 参数类型             | 命名参数 | 描述 |
| -------------- | -------------------------- | --------------- | ----------- |
| `catalog`      | `VARCHAR`                  | 否              |             |
| `versions`     | `UBIGINT[]`                | 是             |             |
| `older_than`   | `TIMESTAMP WITH TIME ZONE` | 是             |             |

### `ducklake_merge_adjacent_files`

`ducklake_merge_adjacent_files` 函数合并存储中的相邻文件。
成功时，它返回一个包含单列 (`Success`) 且 0 行的表。

| 参数名称 | 参数类型 | 命名参数 | 描述 |
| -------------- | -------------- | --------------- | ----------- |
| `catalog`      | `VARCHAR`      | 否              |             |