---
---
layout: docu
redirect_from:
- /docs/sql/data_types/json
- /docs/sql/data_types/json/
- /docs/data/json/json_type
title: JSON 类型
---

DuckDB 通过 `JSON` 逻辑类型支持 `json`。
`JSON` 逻辑类型被解释为 JSON，即在 JSON 函数中被解析，而不是被解释为 `VARCHAR`，即普通字符串（除页面底部提到的相等比较外）。
所有创建 JSON 的函数都返回该类型的值。

我们还允许将 DuckDB 的任何类型转换为 JSON，也可以将 JSON 转换回 DuckDB 的任何类型。例如，要将 `JSON` 转换为 DuckDB 的 `STRUCT` 类型，可以运行：

```sql
SELECT '{"duck": 42}'::JSON::STRUCT(duck INTEGER);
```

```text
{'duck': 42}
```

再转换回来：

```sql
SELECT {duck: 42}::JSON;
```

```text
{"duck":42}
```

这适用于我们示例中展示的嵌套类型，也适用于非嵌套类型：

```sql
SELECT '2023-05-12'::DATE::JSON;
```

```text
"2023-05-12"
```

这种行为的唯一例外是将 `VARCHAR` 转换为 `JSON`，它不会改变数据，而是解析并验证 `VARCHAR` 的内容作为 JSON。