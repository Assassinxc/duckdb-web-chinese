---
---
layout: docu
railroad: expressions/like.js
redirect_from:
- /docs/sql/functions/regular_expressions
title: 正则表达式
---

<!-- markdownlint-disable MD001 -->

DuckDB 提供了 [模式匹配运算符]({% link docs/stable/sql/functions/pattern_matching.md %})（[`LIKE`]({% link docs/stable/sql/functions/pattern_matching.md %}#like), [`SIMILAR TO`]({% link docs/stable/sql/functions/pattern_matching.md %}#similar-to), [`GLOB`]({% link docs/stable/sql/functions/pattern_matching.md %}#glob)），以及通过函数支持正则表达式。

## 正则表达式语法

DuckDB 使用 [RE2 库](https://github.com/google/re2) 作为其正则表达式引擎。有关正则表达式语法，请参阅 [RE2 文档](https://github.com/google/re2/wiki/Syntax)。

## 函数

所有函数都接受一个可选的 [选项](#regular-expression-function-options) 集合。

| 名称 | 描述 |
|:--|:-------|
| [`regexp_extract(string, pattern[, group = 0][, options])`](#regexp_extractstring-pattern-group--0-options) | 如果 `string` 包含正则表达式 `pattern`，则返回由可选参数 `group` 指定的捕获组；否则返回空字符串。`group` 必须是一个常量值。如果没有提供 `group`，则默认为 0。可以设置一组可选的 [`options`](#regular-expression-function-options)。 |
| [`regexp_extract(string, pattern, name_list[, options])`](#regexp_extractstring-pattern-name_list-options) | 如果 `string` 包含正则表达式 `pattern`，则返回一个带有 `name_list` 中对应名称的结构体；否则返回一个具有相同键和空字符串值的结构体。 |
| [`regexp_extract_all(string, regex[, group = 0][, options])`](#regexp_extract_allstring-regex-group--0-options) | 在 `string` 中查找非重叠的 `regex` 出现，并返回 `group` 的对应值。 |
| [`regexp_full_match(string, regex[, options])`](#regexp_full_matchstring-regex-options) | 如果整个 `string` 匹配 `regex`，则返回 `true`。 |
| [`regexp_matches(string, pattern[, options])`](#regexp_matchesstring-pattern-options) | 如果 `string` 包含正则表达式 `pattern`，则返回 `true`，否则返回 `false`。 |
| [`regexp_replace(string, pattern, replacement[, options])`](#regexp_replacestring-pattern-replacement-options) | 如果 `string` 包含正则表达式 `pattern`，则用 `replacement` 替换匹配部分。默认情况下，仅替换第一个匹配项。可以设置一组可选的 [`options`](#regular-expression-function-options)，包括全局标志 `g`。 |
| [`regexp_split_to_array(string, regex[, options])`](#regexp_split_to_arraystring-regex-options) | `string_split_regex` 的别名。根据 `regex` 拆分 `string`。 |
| [`regexp_split_to_table(string, regex[, options])`](#regexp_split_to_tablestring-regex-options) | 根据 `regex` 拆分 `string`，并为每个部分返回一行。 |

#### `regexp_extract(string, pattern[, group = 0][, options])`

<div class="nostroke_table"></div>

| **描述** | 如果 `string` 包含正则表达式 `pattern`，则返回由可选参数 `group` 指定的捕获组；否则返回空字符串。`group` 必须是一个常量值。如果没有提供 `group`，则默认为 0。可以设置一组可选的 [`options`](#regular-expression-function-options)。 |
| **示例** | `regexp_extract('abc', '([a-z])(b)', 1)` |
| **结果** | `a` |

#### `regexp_extract(string, pattern, name_list[, options])`

<div class="nostroke_table"></div>

| **描述** | 如果 `string` 包含正则表达式 `pattern`，则返回一个带有 `name_list` 中对应名称的结构体；否则返回一个具有相同键和空字符串值的结构体。可以设置一组可选的 [`options`](#regular-expression-function-options)。 |
| **示例** | `regexp_extract('2023-04-15', '(\d+)-(\d+)-(\d+)', ['y', 'm', 'd'])` |
| **结果** | `{'y':'2023', 'm':'04', 'd':'15'}` |

#### `regexp_extract_all(string, regex[, group = 0][, options])`

<div class="nostroke_table"></div>

| **描述** | 在 `string` 中查找非重叠的 `regex` 出现，并返回 `group` 的对应值。可以设置一组可选的 [`options`](#regular-expression-function-options)。 |
| **示例** | `regexp_extract_all('Peter: 33, Paul:14', '(\w+):\s*(\d+)', 2)` |
| **结果** | `[33, 14]` |

#### `regexp_full_match(string, regex[, options])`

<div class="nostroke_table"></div>

| **描述** | 如果整个 `string` 匹配 `regex`，则返回 `true`。可以设置一组可选的 [`options`](#regular-expression-function-options)。 |
| **示例** | `regexp_full_match('anabanana', '(an)*')` |
| **结果** | `false` |

#### `regexp_matches(string, pattern[, options])`

<div class="nostroke_table"></div>

| **描述** | 如果 `string` 包含正则表达式 `pattern`，则返回 `true`，否则返回 `false`。可以设置一组可选的 [`options`](#regular-expression-function-options)。 |
| **示例** | `regexp_matches('anabanana', '(an)*')` |
| **结果** | `true` |

#### `regexp_replace(string, pattern, replacement[, options])`

<div class="nostroke_table"></div>

| **描述** | 如果 `string` 包含正则表达式 `pattern`，则用 `replacement` 替换匹配部分。默认情况下，仅替换第一个匹配项。可以设置一组可选的 [`options`](#regular-expression-function-options)，包括全局标志 `g`。 |
| **示例** | `regexp_replace('hello', '[lo]', '-')` |
| **结果** | `he-lo` |

#### `regexp_split_to_array(string, regex[, options])`

<div class="nostroke_table"></div>

| **描述** | `string_split_regex` 的别名。根据 `regex` 拆分 `string`。可以设置一组可选的 [`options`](#regular-expression-function-options)。 |
| **示例** | `regexp_split_to_array('hello world; 42', ';? ')` |
| **结果** | `['hello', 'world', '42']` |

#### `regexp_split_to_table(string, regex[, options])`

<div class="nostroke_table"></div>

| **描述** | 根据 `regex` 拆分 `string`，并为每个部分返回一行。可以设置一组可选的 [`options`](#regular-expression-function-options)。 |
| **示例** | `regexp_split_to_table('hello world; 42', ';? ')` |
| **结果** | 三行：`'hello'`，`'world'`，`'42'` |

`regexp_matches` 函数类似于 `SIMILAR TO` 运算符，但不需要整个字符串匹配。相反，`regexp_matches` 返回 `true` 如果字符串仅包含模式（除非使用特殊令牌 `^` 和 `$` 将正则表达式锚定在字符串的开头和结尾）。以下是一些示例：

```sql
SELECT regexp_matches('abc', 'abc');       -- true
SELECT regexp_matches('abc', '^abc$');     -- true
SELECT regexp_matches('abc', 'a');         -- true
SELECT regexp_matches('abc', '^a$');       -- false
SELECT regexp_matches('abc', '.*(b|d).*'); -- true
SELECT regexp_matches('abc', '(b|c).*');   -- true
SELECT regexp_matches('abc', '^(b|c).*');  -- false
SELECT regexp_matches('abc', '(?i)A');     -- true
SELECT regexp_matches('abc', 'A', 'i');    -- true
```

## 正则表达式函数选项

正则表达式函数支持以下 `options`。

| 选项 | 描述 |
|:---|:---|
| `'c'`               | 区分大小写的匹配                             |
| `'i'`               | 不区分大小写的匹配                           |
| `'l'`               | 匹配字面量而不是正则表达式令牌 |
| `'m'`, `'n'`, `'p'` | 换行敏感的匹配                          |
| `'g'`               | 全局替换，仅适用于 `regexp_replace` |
| `'s'`               | 不换行敏感的匹配                      |

例如：

```sql
SELECT regexp_matches('abcd', 'ABC', 'c'); -- false
SELECT regexp_matches('abcd', 'ABC', 'i'); -- true
SELECT regexp_matches('ab^/$cd', '^/$', 'l'); -- true
SELECT regexp_matches(E'hello\nworld', 'hello.world', 'p'); -- false
SELECT regexp_matches(E'hello\nworld', 'hello.world', 's'); -- true
```

### 使用 `regexp_matches`

当可能时，`regexp_matches` 操作符将被优化为 `LIKE` 操作符。为了达到最佳性能，如果适用，应传递 `'c'` 选项（区分大小写的匹配）。请注意，默认情况下 [`RE2` 库](#regular-expression-syntax) 不会将 `.` 字符匹配到换行符。

| 原始 | 优化等价 |
|:---|:---|
| `regexp_matches('hello world', '^hello', 'c')`      | `prefix('hello world', 'hello')` |
| `regexp_matches('hello world', 'world$', 'c')`      | `suffix('hello world', 'world')` |
| `regexp_matches('hello world', 'hello.world', 'c')` | `LIKE 'hello_world'`             |
| `regexp_matches('hello world', 'he.*rld', 'c')`     | `LIKE '%he%rld'`                 |

### 使用 `regexp_replace`

`regexp_replace` 函数可用于将字符串中与正则表达式模式匹配的部分替换为替换字符串。可以使用 `\d`（其中 `d` 是一个数字，表示组）在替换字符串中引用正则表达式中捕获的组。请注意，默认情况下，`regexp_replace` 仅替换正则表达式的第一个匹配项。要替换所有匹配项，请使用全局替换（`g`）标志。

使用 `regexp_replace` 的一些示例：

```sql
SELECT regexp_replace('abc', '(b|c)', 'X');        -- aXc
SELECT regexp_replace('abc', '(b|c)', 'X', 'g');   -- aXX
SELECT regexp_replace('abc', '(b|c)', '\1\1\1\1'); -- abbbbc
SELECT regexp_replace('abc', '(.*)c', '\1e');      -- abe
SELECT regexp_replace('abc', '(a)(b)', '\2\1');    -- bac
```

### 使用 `regexp_extract`

`regexp_extract` 函数用于提取与正则表达式模式匹配的字符串的一部分。可以使用 `group` 参数提取模式中的特定捕获组。如果未指定 `group`，则默认为 0，提取整个模式的第一个匹配项。

```sql
SELECT regexp_extract('abc', '.b.');           -- abc
SELECT regexp_extract('abc', '.b.', 0);        -- abc
SELECT regexp_extract('abc', '.b.', 1);        -- (empty)
SELECT regexp_extract('abc', '([a-z])(b)', 1); -- a
SELECT regexp_extract('abc', '([a-z])(b)', 2); -- b
```

`regexp_extract` 函数还支持一个 `name_list` 参数，它是一个字符串列表。使用 `name_list`，`regexp_extract` 将返回相应的捕获组作为结构体的字段：

```sql
SELECT regexp_extract('2023-04-15', '(\d+)-(\d+)-(\d+)', ['y', 'm', 'd']);
```

```text
{'y': 2023, 'm': 04, 'd': 15}
```

```sql
SELECT regexp_extract('2023-04-15 07:59:56', '^(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+)', ['y', 'm', 'd']);
```

```text
{'y': 2023, 'm': 04, 'd': 15}
```

```sql
SELECT regexp_extract('duckdb_0_7_1', '^(\w+)_(\d+)_(\d+)', ['tool', 'major', 'minor', 'fix']);
```

```console
Binder Error:
Not enough group names in regexp_extract
```

如果列名的数量少于捕获组的数量，则只返回前几个组。如果列名的数量更多，则会生成错误。

## 局限性

正则表达式仅支持 9 个捕获组：`\1`, `\2`, `\3`, ..., `\9`。不支持两位或更多位数的捕获组。