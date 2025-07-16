---
---
github_repository: https://github.com/duckdb/duckdb-sqlsmith
layout: docu
title: SQLSmith 扩展
redirect_from:
- /docs/stable/extensions/sqlsmith
- /docs/stable/extensions/sqlsmith/
- /docs/extensions/sqlsmith
- /docs/extensions/sqlsmith/
---

`sqlsmith` 扩展用于测试。

## 安装和加载

```sql
INSTALL sqlsmith;
LOAD sqlsmith;
```

## 函数

`sqlsmith` 扩展注册了以下函数：

* `sqlsmith`
* `fuzzyduck`
* `reduce_sql_statement`
* `fuzz_all_functions`