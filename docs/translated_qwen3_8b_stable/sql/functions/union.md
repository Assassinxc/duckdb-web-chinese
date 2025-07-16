---
---
layout: docu
redirect_from:
- /docs/sql/functions/union
title: 联合函数
---

<!-- markdownlint-disable MD001 -->

| 名称 | 描述 |
|:--|:-------|
| [`union.tag`](#uniontag) | 使用点符号表示法作为 `union_extract` 的别名。 |
| [`union_extract(union, 'tag')`](#union_extractunion-tag) | 从联合中提取具有指定标签的值。如果当前未选择该标签，则返回 `NULL`。 |
| [`union_value(tag := any)`](#union_valuetag--any) | 创建一个包含参数值的单个成员 `UNION`。该值的标签将为绑定变量的名称。 |
| [`union_tag(union)`](#union_tagunion) | 以 [Enum]({% link docs/stable/sql/data_types/enum.md %}) 形式获取联合当前选择的标签。 |

#### `union.tag`

<div class="nostroke_table"></div>

| **描述** | 使用点符号表示法作为 `union_extract` 的别名。 |
| **示例** | `(union_value(k := 'hello')).k` |
| **结果** | `string` |

#### `union_extract(union, 'tag')`

<div class="nostroke_table"></div>

| **描述** | 从联合中提取具有指定标签的值。如果当前未选择该标签，则返回 `NULL`。 |
| **示例** | `union_extract(s, 'k')` |
| **结果** | `hello` |

#### `union_value(tag := any)`

<div class="nostroke_table"></div>

| **描述** | 创建一个包含参数值的单个成员 `UNION`。该值的标签将为绑定变量的名称。 |
| **示例** | `union_value(k := 'hello')` |
| **结果** | `'hello'::UNION(k VARCHAR)` |

#### `union_tag(union)`

<div class="nostroke_table"></div>

| **描述** | 以 [Enum]({% link docs/stable/sql/data_types/enum.md %}) 形式获取联合当前选择的标签。 |
| **示例** | `union_tag(union_value(k := 'foo'))` |
| **结果** | `'k'` |