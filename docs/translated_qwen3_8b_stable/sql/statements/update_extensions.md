---
---
layout: docu
redirect_from:
- /docs/sql/statements/update_extensions
title: UPDATE EXTENSIONS
---

`UPDATE EXTENSIONS` 语句允许将本地安装的扩展状态与发布该扩展的仓库进行同步。
这是保持与扩展开发者推出的新功能或修复 bug 同步的推荐方式。

请注意，DuckDB 扩展在运行时无法重新加载，因此 `UPDATE EXTENSIONS` 不会重新加载已更新的扩展。
要使用更新后的扩展，请重新启动正在运行 DuckDB 的进程。

## 更新所有扩展

要更新您客户端 DuckDB 版本所安装的所有扩展：

```sql
UPDATE EXTENSIONS;
```

这将遍历所有扩展，并返回其仓库和更新结果：

```text
┌────────────────┬──────────────┬─────────────────────┬──────────────────┬─────────────────┐
│ extension_name │  repository  │    update_result    │ previous_version │ current_version │
│    varchar     │   varchar    │       varchar       │     varchar      │     varchar     │
├────────────────┼──────────────┼─────────────────────┼──────────────────┼─────────────────┤
│ iceberg        │ core_nightly │ UPDATED             │ 6386ab5          │ b3ec51a         │
│ icu            │ core         │ NO_UPDATE_AVAILABLE │ v1.2.1           │ v1.2.1          │
│ autocomplete   │ core         │ NO_UPDATE_AVAILABLE │ v1.2.1           │ v1.2.1          │
│ httpfs         │ core_nightly │ NO_UPDATE_AVAILABLE │ cf3584b          │ cf3584b         │
│ json           │ core         │ NO_UPDATE_AVAILABLE │ v1.2.1           │ v1.2.1          │
│ aws            │ core_nightly │ NO_UPDATE_AVAILABLE │ d3c5013          │ d3c5013         │
└────────────────┴──────────────┴─────────────────────┴──────────────────┴─────────────────┘
```

## 更新选定的扩展

为了更精细地控制，您也可以提供要更新的扩展名称列表：

```sql
UPDATE EXTENSIONS (name_a, name_b, name_c);
```

## 工作原理

`UPDATE EXTENSIONS` 通过存储（如果可用）[ETag](https://en.wikipedia.org/wiki/HTTP_ETag) 信息，并发送一个基于远程扩展与本地可用扩展不同的条件 GET 请求（使用 ETag 作为代理）来实现。
这确保了如果远程状态未发生变化，后续的 `UPDATE EXTENSIONS` 调用将非常高效。

如果发现某个扩展发生了变化，DuckDB 会执行以下操作。例如，如果 `name_a` 和 `name_c` 发生了变化，那么：

```sql
UPDATE EXTENSIONS (name_a, name_b, name_c);
```

这将导致以下命令：

```sql
FORCE INSTALL name_a;
FORCE INSTALL name_c;
```