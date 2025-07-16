---
---
layout: docu
redirect_from:
- /docs/data/json/sql_to_and_from_json
title: SQL 与 JSON 之间的转换
---

DuckDB 提供了用于在 SQL 和 JSON 之间序列化和反序列化 `SELECT` 语句的函数，以及执行 JSON 序列化的语句。

| 函数 | 类型 | 描述 |
|:------|:-|:---------|
| `json_deserialize_sql(json)` | 标量 | 将一个或多个 `json` 序列化的语句反序列化为等效的 SQL 字符串。 |
| `json_execute_serialized_sql(varchar)` | 表 | 执行 `json` 序列化的语句并返回结果行。目前仅支持每次执行一条语句。 |
| `json_serialize_sql(varchar, skip_default := boolean, skip_empty := boolean, skip_null := boolean, format := boolean)` | 标量 | 将一组分号分隔的 (`;`) `SELECT` 语句序列化为等效的 `json` 序列化语句列表。 |
| `PRAGMA json_execute_serialized_sql(varchar)` | Pragma | `json_execute_serialized_sql` 函数的 Pragma 版本。 |

`json_serialize_sql(varchar)` 函数接受三个可选参数 `skip_empty`、`skip_null` 和 `format`，可用于控制序列化语句的输出。

如果你在事务中运行 `json_execute_serialized_sql(varchar)` 表函数，序列化的语句将无法看到事务本地的更改。这是因为这些语句是在单独的查询上下文中执行的。你可以使用 `PRAGMA json_execute_serialized_sql(varchar)` Pragma 版本来在与 Pragma 相同的查询上下文中执行语句，但限制是必须将序列化的 JSON 作为常量字符串提供，即你不能执行 `PRAGMA json_execute_serialized_sql(json_serialize_sql(...))`。

请注意，这些函数不会保留诸如 `FROM * SELECT ...` 这样的语法糖，因此通过 `json_deserialize_sql(json_serialize_sql(...))` 转换的语句可能与原始语句不完全相同，但应该始终语义等价并产生相同的结果。

### 示例

简单示例：

```sql
SELECT json_serialize_sql('SELECT 2');
```

```text
{"error":false,"statements":[{"node":{"type":"SELECT_NODE","modifiers":[],"cte_map":{"map":[]},"select_list":[{"class":"CONSTANT","type":"VALUE_CONSTANT","alias":"","query_location":7,"value":{"type":{"id":"INTEGER","type_info":null},"is_null":false,"value":2}}],"from_table":{"type":"EMPTY","alias":"","sample":null,"query_location":18446744073709551615},"where_clause":null,"group_expressions":[],"group_sets":[],"aggregate_handling":"STANDARD_HANDLING","having":null,"sample":null,"qualify":null},"named_param_map":[]}]}
```

包含多个语句及跳过选项的示例：

```sql
SELECT json_serialize_sql('SELECT 1 + 2; SELECT a + b FROM tbl1', skip_empty := true, skip_null := true);
```

```text
{"error":false,"statements":[{"node":{"type":"SELECT_NODE","select_list":[{"class":"FUNCTION","type":"FUNCTION","query_location":9,"function_name":"+","children":[{"class":"CONSTANT","type":"VALUE_CONSTANT","query_location":7,"value":{"type":{"id":"INTEGER"},"is_null":false,"value":1}},{"class":"CONSTANT","type":"VALUE_CONSTANT","query_location":11,"value":{"type":{"id":"INTEGER"},"is_null":false,"value":2}}],"order_bys":{"type":"ORDER_MODIFIER"},"distinct":false,"is_operator":true,"export_state":false}],"from_table":{"type":"EMPTY","query_location":18446744073709551615},"aggregate_handling":"STANDARD_HANDLING"}},{"node":{"type":"SELECT_NODE","select_list":[{"class":"FUNCTION","type":"FUNCTION","query_location":23,"function_name":"+","children":[{"class":"COLUMN_REF","type":"COLUMN_REF","query_location":21,"column_names":["a"]},{"class":"COLUMN_REF","type":"COLUMN_REF","query_location":25,"column_names":["b"]}],"order_bys":{"type":"ORDER_MODIFIER"},"distinct":false,"is_operator":true,"export_state":false}],"from_table":{"type":"BASE_TABLE","query_location":32,"table_name":"tbl1"},"aggregate_handling":"STANDARD_HANDLING"}}]}
```

跳过 AST 中的默认值（例如 `"distinct":false`）：

```sql
SELECT json_serialize_sql('SELECT 1 + 2; SELECT a + b FROM tbl1', skip_default := true, skip_empty := true, skip_null := true);
```

```text
{"error":false,"statements":[{"node":{"type":"SELECT_NODE","select_list":[{"class":"FUNCTION","type":"FUNCTION","query_location":9,"function_name":"+","children":[{"class":"CONSTANT","type":"VALUE_CONSTANT","query_location":7,"value":{"type":{"id":"INTEGER"},"is_null":false,"value":1}},{"class":"CONSTANT","type":"VALUE_CONSTANT","query_location":11,"value":{"type":{"id":"INTEGER"},"is_null":false,"value":2}}],"order_bys":{"type":"ORDER_MODIFIER"},"is_operator":true}],"from_table":{"type":"EMPTY"},"aggregate_handling":"STANDARD_HANDLING"}},{"node":{"type":"SELECT_NODE","select_list":[{"class":"FUNCTION","type":"FUNCTION","query_location":23,"function_name":"+","children":[{"class":"COLUMN_REF","type":"COLUMN_REF","query_location":21,"column_names":["a"]},{"class":"COLUMN_REF","type":"COLUMN_REF","query_location":25,"column_names":["b"]}],"order_bys":{"type":"ORDER_MODIFIER"},"is_operator":true}],"from_table":{"type":"BASE_TABLE","query_location":32,"table_name":"tbl1"},"aggregate_handling":"STANDARD_HANDLING"}}]}
```

带有语法错误的示例：

```sql
SELECT json_serialize_sql('TOTALLY NOT VALID SQL');
```

```text
{"error":true,"error_type":"parser","error_message":"syntax error at or near \"TOTALLY\"","error_subtype":"SYNTAX_ERROR","position":"0"}
```

带有反序列化的示例：

```sql
SELECT json_deserialize_sql(json_serialize_sql('SELECT 1 + 2'));
```

```text
SELECT (1 + 2)
```

带有反序列化和语法糖的示例，语法糖在转换过程中丢失：

```sql
SELECT json_deserialize_sql(json_serialize_sql('FROM x SELECT 1 + 2'));
```

```text
SELECT (1 + 2) FROM x
```

带有执行的示例：

```sql
SELECT * FROM json_execute_serialized_sql(json_serialize_sql('SELECT 1 + 2'));
```

```text
3
```

带有错误的示例：

```sql
SELECT * FROM json_execute_serialized_sql(json_serialize_sql('TOTALLY NOT VALID SQL'));
```

```console
Parser Error:
Error parsing json: parser: syntax error at or near "TOTALLY"
```