---
---
layout: docu
redirect_from:
  - /docs/data/json/json_functions
title: JSON 处理函数
---

## JSON 提取函数

有两种提取函数，它们各自拥有对应的运算符。这些运算符只能在字符串以 `JSON` 逻辑类型存储时使用。
这些函数支持与 [JSON 标量函数](#json-scalar-functions) 相同的两种位置表示法。

| 函数                         | 别名               | 运算符 | 描述                                                                                                                       |
| :--------------------------- | :------------------ | :----- | ------------------------------------------------------------------------------------------------------------------------- |
| `json_exists(json, path)`    |                    |        | 如果 `json` 中存在指定的 `path`，则返回 `true`，否则返回 `false`。                                                      |
| `json_extract(json, path)`   | `json_extract_path` | `->`   | 从 `json` 中提取 `JSON`，在给定的 `path` 处。如果 `path` 是一个 `LIST`，结果将是一个 `LIST` 的 `JSON`。                    |
| `json_extract_string(json, path)` | `json_extract_path_text` | `->>`    | 从 `json` 中提取 `VARCHAR`，在给定的 `path` 处。如果 `path` 是一个 `LIST`，结果将是一个 `LIST` 的 `VARCHAR`。              |
| `json_value(json, path)`     |                    |        | 从 `json` 中提取 `JSON`，在给定的 `path` 处。如果在给定的 `path` 处的 `json` 不是标量值，将返回 `NULL`。 |

注意，用于 JSON 提取的箭头运算符 `->` 的优先级较低，因为它也用于 [lambda 函数]({% link docs/stable/sql/functions/lambda.md %})。因此，在表达诸如相等比较（`=`）等操作时，需要将 `->` 运算符用括号括起来。
例如：

```sql
SELECT ((JSON '{"field": 42}')->'field') = 42;
```

> 警告 DuckDB 的 JSON 数据类型使用 [0 基础索引]({% link docs/stable/data/json/overview.md %}#indexing)。

示例：

```sql
CREATE TABLE example (j JSON);
INSERT INTO example VALUES
    ('{ "family": "anatidae", "species": [ "duck", "goose", "swan", null ] }');
```

```sql
SELECT json_extract(j, '$.family') FROM example;
```

```text
"anatidae"
```

```sql
SELECT j->'$.family' FROM example;
```

```text
"anatidae"
```

```sql
SELECT j->'$.species[0]' FROM example;
```

```text
"duck"
```

```sql
SELECT j->'$.species[*]' FROM example;
```

```text
["duck", "goose", "swan", null]
```

```sql
SELECT j->>'$.species[*]' FROM example;
```

```text
[duck, goose, swan, null]
```

```sql
SELECT j->'$.species'->0 FROM example;
```

```text
"duck"
```

```sql
SELECT j->'species'->['/0', '/1'] FROM example;
```

```text
['"duck"', '"goose"']
```

```sql
SELECT json_extract_string(j, '$.family') FROM example;
```

```text
anatidae
```

```sql
SELECT j->>'$.family' FROM example;
```

```text
anatidae
```

```sql
SELECT j->>'$.species[0]' FROM example;
```

```text
duck
```

```sql
SELECT j->'species'->>0 FROM example;
```

```text
duck
```

```sql
SELECT j->'species'->>['/0', '/1'] FROM example;
```

```text
[duck, goose]
```

注意，DuckDB 的 JSON 数据类型使用 [0 基础索引]({% link docs/stable/data/json/overview.md %}#indexing)。

如果需要从同一个 JSON 中提取多个值，提取路径列表会更高效：

以下操作会导致 JSON 解析两次：

导致查询变慢且内存使用更多：

```sql
SELECT
    json_extract(j, 'family') AS family,
    json_extract(j, 'species') AS species
FROM example;
```

<div class="monospace_table"></div>

| family     | species                      |
| ---------- | ---------------------------- |
| "anatidae" | ["duck","goose","swan",null] |

以下操作会生成相同结果，但更快且更节省内存：

```sql
WITH extracted AS (
    SELECT json_extract(j, ['family', 'species']) AS extracted_list
    FROM example
)
SELECT
    extracted_list[1] AS family,
    extracted_list[2] AS species
FROM extracted;
```

## JSON 标量函数

以下标量 JSON 函数可用于获取存储的 JSON 值的信息。
除 `json_valid(json)` 外，所有 JSON 函数在输入无效 JSON 时都会报错。

我们支持两种描述 JSON 内部位置的表示法：[JSON Pointer](https://datatracker.ietf.org/doc/html/rfc6901) 和 JSONPath。

| 函数                                    | 描述                                                                                                                                                                                                                                                                        |
| :-------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `json_array_length(json[, path])`       | 返回 JSON 数组 `json` 的元素数量，如果不是 JSON 数组则返回 `0`。如果指定了 `path`，则返回给定 `path` 处的 JSON 数组的元素数量。如果 `path` 是一个 `LIST`，结果将是一个 `LIST` 的数组长度。                                               |
| `json_contains(json_haystack, json_needle)` | 如果 `json_needle` 包含在 `json_haystack` 中，则返回 `true`。两个参数都是 JSON 类型，但 `json_needle` 也可以是数值或字符串，不过字符串必须用双引号包裹。                                                                                                                       |
| `json_keys(json[, path])`               | 如果 `json` 是一个 JSON 对象，则返回 `VARCHAR` 类型的键列表。如果指定了 `path`，则返回给定 `path` 处的 JSON 对象的键。如果 `path` 是一个 `LIST`，结果将是一个 `LIST` 的 `LIST` 的 `VARCHAR`。                                               |
| `json_structure(json)`                  | 返回 `json` 的结构。如果结构不一致（例如数组中类型不兼容），默认返回 `JSON`。                                                                                                                                                                                            |
| `json_type(json[, path])`               | 返回 `json` 的类型，可能是 `ARRAY`、`BIGINT`、`BOOLEAN`、`DOUBLE`、`OBJECT`、`UBIGINT`、`VARCHAR` 和 `NULL`。如果指定了 `path`，则返回给定 `path` 处的元素类型。如果 `path` 是一个 `LIST`，结果将是一个 `LIST` 的类型。 |
| `json_valid(json)`                      | 返回 `json` 是否为有效的 JSON。                                                                                                                                                                                                                                            |
| `json(json)`                            | 解析并压缩 `json`。                                                                                                                                                                                                                                                         |

JSONPointer 语法使用 `/` 分隔每个字段。
例如，要提取键为 `duck` 的数组的第一个元素，可以这样做：

```sql
SELECT json_extract('{"duck": [1, 2, 3]}', '/duck/0');
```

```text
1
```

JSONPath 语法使用 `.` 分隔字段，使用 `[i]` 访问数组元素，并始终以 `$` 开始。使用同样的示例，我们可以这样做：

```sql
SELECT json_extract('{"duck": [1, 2, 3]}', '$.duck[0]');
```

```text
1
```

注意，DuckDB 的 JSON 数据类型使用 [0 基础索引]({% link docs/stable/data/json/overview.md %}#indexing)。

JSONPath 表达力更强，也可以从列表的末尾访问：

```sql
SELECT json_extract('{"duck": [1, 2, 3]}', '$.duck[#-1]');
```

```text
3
```

JSONPath 还允许使用双引号转义语法标记：

```sql
SELECT json_extract('{"duck.goose": [1, 2, 3]}', '$."duck.goose"[1]');
```

```text
2
```

使用 [anatidae 生物学家族](https://en.wikipedia.org/wiki/Anatidae) 的示例：

```sql
CREATE TABLE example (j JSON);
INSERT INTO example VALUES
    ('{ "family": "anatidae", "species": [ "duck", "goose", "swan", null ] }');
```

```sql
SELECT json(j) FROM example;
```

```text
{"family":"anatidae","species":["duck","goose","swan",null]}
```

```sql
SELECT j.family FROM example;
```

```text
"anatidae"
```

```sql
SELECT j.species[0] FROM example;
```

```text
"duck"
```

```sql
SELECT json_valid(j) FROM example;
```

```text
true
```

```sql
SELECT json_valid('{');
```

```text
false
```

```sql
SELECT json_array_length('["duck", "goose", "swan", null]');
```

```text
4
```

```sql
SELECT json_array_length(j, 'species') FROM example;
```

```text
4
```

```sql
SELECT json_array_length(j, '/species') FROM example;
```

```text
4
```

```sql
SELECT json_array_length(j, '$.species') FROM example;
```

```text
4
```

```sql
SELECT json_array_length(j, ['$.species']) FROM example;
```

```text
[4]
```

```sql
SELECT json_type(j) FROM example;
```

```text
OBJECT
```

```sql
SELECT json_keys(j) FROM example;
```

```text
[family, species]
```

```sql
SELECT json_structure(j) FROM example;
```

```text
{"family":"VARCHAR","species":["VARCHAR"]}
```

```sql
SELECT json_structure('["duck", {"family": "anatidae"}]');
```

```text
["JSON"]
```

```sql
SELECT json_contains('{"key": "value"}', '"value"');
```

```text
true
```

```sql
SELECT json_contains('{"key": 1}', '1');
```

```text
true
```

```sql
SELECT json_contains('{"top_key": {"key": "value"}}', '{"key": "value"}');
```

```text
true
```

## JSON 聚合函数

有三个 JSON 聚合函数。

| 函数                         | 描述                                                            |
| :--------------------------- | :------------------------------------------------------------- |
| `json_group_array(any)`      | 返回一个包含 `any` 所有值的 JSON 数组。                         |
| `json_group_object(key, value)` | 返回一个包含所有 `key`、`value` 对的 JSON 对象。               |
| `json_group_structure(json)` | 返回所有 `json` 的 `json_structure` 的组合。                   |

示例：

```sql
CREATE TABLE example1 (k VARCHAR, v INTEGER);
INSERT INTO example1 VALUES ('duck', 42), ('goose', 7);
```

```sql
SELECT json_group_array(v) FROM example1;
```

```text
[42, 7]
```

```sql
SELECT json_group_object(k, v) FROM example1;
```

```text
{"duck":42,"goose":7}
```

```sql
CREATE TABLE example2 (j JSON);
INSERT INTO example2 VALUES
    ('{"family": "anatidae", "species": ["duck", "goose"], "coolness": 42.42}'),
    ('{"family": "canidae", "species": ["labrador", "bulldog"], "hair": true}');
```

```sql
SELECT json_group_structure(j) FROM example2;
```

```text
{"family":"VARCHAR","species":["VARCHAR"],"coolness":"DOUBLE","hair":"BOOLEAN"}
```

## 将 JSON 转换为嵌套类型

在许多情况下，逐个从 JSON 提取值是低效的。
相反，我们可以“一次提取”所有值，将 JSON 转换为嵌套类型 `LIST` 和 `STRUCT`。

| 函数                                 | 描述                                                            |
| :----------------------------------- | :------------------------------------------------------------- |
| `json_transform(json, structure)`    | 根据指定的 `structure` 转换 `json`。                           |
| `from_json(json, structure)`         | `json_transform` 的别名。                                       |
| `json_transform_strict(json, structure)` | 与 `json_transform` 相同，但类型转换失败时会抛出错误。         |
| `from_json_strict(json, structure)`  | `json_transform_strict` 的别名。                                |

`structure` 参数是与 `json_structure` 返回形式相同的 JSON。
`structure` 参数可以修改以将 JSON 转换为所需的结构和类型。
可以提取的键/值对少于 JSON 中存在的数量，也可以提取更多：缺少的键将变为 `NULL`。

示例：

```sql
CREATE TABLE example (j JSON);
INSERT INTO example VALUES
    ('{"family": "anatidae", "species": ["duck", "goose"], "coolness": 42.42}'),
    ('{"family": "canidae", "species": ["labrador", "bulldog"], "hair": true}');
```

```sql
SELECT json_transform(j, '{"family": "VARCHAR", "coolness": "DOUBLE"}') FROM example;
```

```text
{'family': anatidae, 'coolness': 42.420000}
{'family': canidae, 'coolness': NULL}
```

```sql
SELECT json_transform(j, '{"family": "TINYINT", "coolness": "DECIMAL(4, 2)"}') FROM example;
```

```text
{'family': NULL, 'coolness': 42.42}
{'family': NULL, 'coolness': NULL}
```

```sql
SELECT json_transform_strict(j, '{"family": "TINYINT", "coolness": "DOUBLE"}') FROM example;
```

```console
Invalid Input Error: Failed to cast value: "anatidae"
```

## JSON 表函数

DuckDB 实现了两个 JSON 表函数，它们接受一个 JSON 值并将其转换为表。

| 函数                 | 描述                                                                                  |
| :------------------- | :----------------------------------------------------------------------------------- |
| `json_each(json[ ,path]` | 遍历 `json`，并为顶级数组或对象中的每个元素返回一行。                                |
| `json_tree(json[ ,path]` | 以深度优先方式遍历 `json`，并为结构中的每个元素返回一行。                           |

如果元素不是数组或对象，将返回该元素本身。
如果提供了可选的 `path` 参数，则遍历从给定的路径开始，而不是从根元素开始。

结果表包含以下列：

| 字段     | 类型               | 描述                                 |
| :-------- | :----------------- | :---------------------------------- |
| `key`     | `VARCHAR`          | 元素相对于其父元素的键               |
| `value`   | `JSON`             | 元素的值                            |
| `type`    | `VARCHAR`          | 元素的 `json_type`（函数）           |
| `atom`    | `JSON`             | 元素的 `json_value`（函数）          |
| `id`      | `UBIGINT`          | 元素标识符，按解析顺序编号           |
| `parent`  | `UBIGINT`          | 父元素的 `id`                       |
| `fullkey` | `VARCHAR`          | 元素的 JSON 路径                    |
| `path`    | `VARCHAR`          | 父元素的 JSON 路径                  |
| `json`    | `JSON` (虚拟)      | `json` 参数                         |
| `root`    | `TEXT` (虚拟)      | `path` 参数                         |
| `rowid`   | `BIGINT` (虚拟)    | 行标识符                            |

这些函数与 [SQLite 具有相同名称的函数](https://www.sqlite.org/json1.html#jeach) 类似。
请注意，因为 `json_each` 和 `json_tree` 函数引用了同一 FROM 子句中的前一个子查询，因此它们是 [*lateral joins*]({% link docs/stable/sql/query_syntax/from.md %}#lateral-joins)。

示例：

```sql
CREATE TABLE example (j JSON);
INSERT INTO example VALUES
    ('{"family": "anatidae", "species": ["duck", "goose"], "coolness": 42.42}'),
    ('{"family": "canidae", "species": ["labrador", "bulldog"], "hair": true}');
```

```sql
SELECT je.*, je.rowid
FROM example AS e, json_each(e.j) AS je;
```

| key      | value                  | type    | atom       |  id | parent | fullkey    | path | rowid |
| -------- | ---------------------- | ------- | ---------- | --: | ------ | ---------- | ---- | ----: |
| family   | "anatidae"             | VARCHAR | "anatidae" |   2 | NULL   | $.family   | $    |     0 |
| species  | ["duck","goose"]       | ARRAY   | NULL       |   4 | NULL   | $.species  | $    |     1 |
| coolness | 42.42                  | DOUBLE  | 42.42      |   8 | NULL   | $.coolness | $    |     2 |
| family   | "canidae"              | VARCHAR | "canidae"  |   2 | NULL   | $.family   | $    |     0 |
| species  | ["labrador","bulldog"] | ARRAY   | NULL       |   4 | NULL   | $.species  | $    |     1 |
| hair     | true                   | BOOLEAN | true       |   8 | NULL   | $.hair     | $    |     2 |

```sql
SELECT je.*, je.rowid
FROM example AS e, json_each(e.j, '$.species') AS je;
```

| key | value      | type    | atom       |  id | parent | fullkey      | path      | rowid |
| --- | ---------- | ------- | ---------- | --: | ------ | ------------ | --------- | ----: |
| 0   | "duck"     | VARCHAR | "duck"     |   5 | NULL   | $.species[0] | $.species |     0 |
| 1   | "goose"    | VARCHAR | "goose"    |   6 | NULL   | $.species[1] | $.species |     1 |
| 0   | "labrador" | VARCHAR | "labrador" |   5 | NULL   | $.species[0] | $.species |     0 |
| 1   | "bulldog"  | VARCHAR | "bulldog"  |   6 | NULL   | $.species[1] | $.species |     1 |

```sql
SELECT je.key, je.value, je.type, je.id, je.parent, je.fullkey, je.rowid
FROM example AS e, json_tree(e.j) AS je;
```

| key      | value                                                             | type    |  id | parent | fullkey      | rowid |
| -------- | ----------------------------------------------------------------- | ------- | --: | ------ | ------------ | ----: |
| NULL     | {"family":"anatidae","species":["duck","goose"],"coolness":42.42} | OBJECT  |   0 | NULL   | $            |     0 |
| family   | "anatidae"                                                        | VARCHAR |   2 | 0      | $.family     |     1 |
| species  | ["duck","goose"]                                                  | ARRAY   |   4 | 0      | $.species    |     2 |
| 0        | "duck"                                                            | VARCHAR |   5 | 4      | $.species[0] |     3 |
| 1        | "goose"                                                           | VARCHAR |   6 | 4      | $.species[1] |     4 |
| coolness | 42.42                                                             | DOUBLE  |   8 | 0      | $.coolness   |     5 |
| NULL     | {"family":"canidae","species":["labrador","bulldog"],"hair":true} | OBJECT  |   0 | NULL   | $            |     0 |
| family   | "canidae"                                                         | VARCHAR |   2 | 0      | $.family     |     1 |
| species  | ["labrador","bulldog"]                                            | ARRAY   |   4 | 0      | $.species    |     2 |
| 0        | "labrador"                                                        | VARCHAR |   5 | 4      | $.species[0] |     3 |
| 1        | "bulldog"                                                         | VARCHAR |   6 | 4      | $.species[1] |     4 |
| hair     | true                                                              | BOOLEAN |   8 | 0      | $.hair       |     5 |