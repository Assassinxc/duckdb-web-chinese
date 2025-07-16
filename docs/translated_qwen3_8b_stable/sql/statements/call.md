---
---
layout: docu
railroad: statements/call.js
redirect_from:
- /docs/sql/statements/call
title: CALL 语句
---

`CALL` 语句调用给定的表函数并返回结果。

## 示例

调用 'duckdb_functions' 表函数：

```sql
CALL duckdb_functions();
```

调用 'pragma_table_info' 表函数：

```sql
CALL pragma_table_info('pg_am');
```

仅选择名称以 `ST_` 开头的函数：

```sql
SELECT function_name, parameters, parameter_types, return_type
FROM duckdb_functions()
WHERE function_name LIKE 'ST_%';
```

## 语法

<div id="rrdiagram1"></div>