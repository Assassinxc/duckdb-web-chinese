---
---
layout: docu
redirect_from:
- /docs/data/json/creating_json
title: 创建 JSON
---

## JSON 创建函数

以下函数用于创建 JSON。

| 函数 | 描述 |
|:--|:----|
| `to_json(any)` | 从 `any` 类型的值创建 `JSON`。我们的 `LIST` 会转换为 JSON 数组，我们的 `STRUCT` 和 `MAP` 会转换为 JSON 对象。 |
| `json_quote(any)` | `to_json` 的别名。 |
| `array_to_json(list)` | 仅接受 `LIST` 的 `to_json` 的别名。 |
| `row_to_json(list)` | 仅接受 `STRUCT` 的 `to_json` 的别名。 |
| `json_array(any, ...)` | 从参数列表中的值创建 JSON 数组。 |
| `json_object(key, value, ...)` | 从参数列表中的 `key`, `value` 对创建 JSON 对象。需要偶数个参数。 |
| `json_merge_patch(json, json)` | 合并两个 JSON 文档。 |

示例：

```sql
SELECT to_json('duck');
```

```text
"duck"
```

```sql
SELECT to_json([1, 2, 3]);
```

```text
[1,2,3]
```

```sql
SELECT to_json({duck : 42});
```

```text
{"duck":42}
```

```sql
SELECT to_json(MAP(['duck'], [42]));
```

```text
{"duck":42}
```

```sql
SELECT json_array('duck', 42, 'goose', 123);
```

```text
["duck",42,"goose",123]
```

```sql
SELECT json_object('duck', 42, 'goose', 123);
```

```text
{"duck":42,"goose":123}
```

```sql
SELECT json_merge_patch('{"duck": 42}', '{"goose": 123}');
```

```text
{"goose":123,"duck":42}
```