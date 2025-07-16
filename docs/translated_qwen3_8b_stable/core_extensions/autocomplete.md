---
---
github_directory: https://github.com/duckdb/duckdb/tree/main/extension/autocomplete
layout: docu
title: 自动补全扩展
redirect_from:
- /docs/stable/extensions/autocomplete
- /docs/stable/extensions/autocomplete/
---

`autocomplete` 扩展为 [CLI 客户端]({% link docs/stable/clients/cli/overview.md %}) 提供自动补全功能支持。
该扩展默认随 CLI 客户端一起提供。

## 行为

有关 `autocomplete` 扩展的行为，请参阅 [CLI 客户端的文档]({% link docs/stable/clients/cli/autocomplete.md %}).

## 函数

| 函数                          | 描述                                          |
|:----------------------------------|:-----------------------------------------------------|
| `sql_auto_complete(query_string)` | 对给定的 `query_string` 尝试自动补全。 |

## 示例

```sql
SELECT *
FROM sql_auto_complete('SEL');
```

返回：

| suggestion  | suggestion_start |
|-------------|------------------|
| SELECT      |                0 |
| DELETE      |                0 |
| INSERT      |                0 |
| CALL        |                0 |
| LOAD        |                0 |
| CALL        |                0 |
| ALTER       |                0 |
| BEGIN       |                0 |
| EXPORT      |                0 |
| CREATE      |                0 |
| PREPARE     |                0 |
| EXECUTE     |                0 |
| EXPLAIN     |                0 |
| ROLLBACK    |                0 |
| DESCRIBE    |                0 |
| SUMMARIZE   |                0 |
| CHECKPOINT  |                0 |
| DEALLOCATE  |                0 |
| UPDATE      |                0 |
| DROP        |                0 |