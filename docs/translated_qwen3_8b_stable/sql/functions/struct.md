---
---
layout: docu
redirect_from:
- /docs/sql/functions/struct
title: 结构函数
---

<!-- markdownlint-disable MD001 -->

| 名称 | 描述 |
|:--|:-------|
| [`struct.entry`](#structentry) | 用于从命名 `STRUCT` 中调用 `struct_extract` 的点符号别名。 |
| [`struct[entry]`](#structentry) | 用于从命名 `STRUCT` 中调用 `struct_extract` 的方括号符号别名。 |
| [`struct[idx]`](#structidx) | 用于从未命名 `STRUCT`（元组）中调用 `struct_extract` 的方括号符号别名，使用索引（1-based）。 |
| [`row(any, ...)`](#rowany-) | 创建一个未命名的 `STRUCT`（元组），包含参数值。 |
| [`struct_concat(structs...)`](#struct_concatstructs) | 将多个 `structs` 合并为一个 `STRUCT`。 |
| [`struct_extract(struct, 'entry')`](#struct_extractstruct-entry) | 从 `STRUCT` 中提取命名的条目。 |
| [`struct_extract(struct, idx)`](#struct_extractstruct-idx) | 使用索引（1-based）从未命名的 `STRUCT`（元组）中提取条目。 |
| [`struct_extract_at(struct, idx)`](#struct_extract_atstruct-idx) | 使用索引（1-based）从 `STRUCT`（元组）中提取条目。 |
| [`struct_insert(struct, name := any, ...)`](#struct_insertstruct-name--any-) | 向现有的 `STRUCT` 中添加字段/值，使用参数值。条目名称将为绑定变量名称。 |
| [`struct_pack(name := any, ...)`](#struct_packname--any-) | 创建一个包含参数值的 `STRUCT`。条目名称将为绑定变量名称。 |

#### `struct.entry`

<div class="nostroke_table"></div>

| **描述** | 用于从命名 `STRUCT` 中调用 `struct_extract` 的点符号别名。 |
| **示例** | `({'i': 3, 's': 'string'}).i` |
| **结果** | `3` |

#### `struct[entry]`

<div class="nostroke_table"></div>

| **描述** | 用于从命名 `STRUCT` 中调用 `struct_extract` 的方括号符号别名。 |
| **示例** | `({'i': 3, 's': 'string'})['i']` |
| **结果** | `3` |

#### `struct[idx]`

<div class="nostroke_table"></div>

| **描述** | 用于从未命名的 `STRUCT`（元组）中调用 `struct_extract` 的方括号符号别名，使用索引（1-based）。 |
| **示例** | `(row(42, 84))[1]` |
| **结果** | `42` |

#### `row(any, ...)`

<div class="nostroke_table"></div>

| **描述** | 创建一个未命名的 `STRUCT`（元组），包含参数值。 |
| **示例** | `row(i, i % 4, i / 4)` |
| **结果** | `(10, 2, 2.5)` |

#### `struct_concat(structs...)`

<div class="nostroke_table"></div>

| **描述** | 将多个 `structs` 合并为一个 `STRUCT`。 |
| **示例** | `struct_concat(struct_pack(i := 4), struct_pack(s := 'string'))` |
| **结果** | `{'i': 4, 's': string}` |

#### `struct_extract(struct, 'entry')`

<div class="nostroke_table"></div>

| **描述** | 从 `STRUCT` 中提取命名的条目。 |
| **示例** | `struct_extract({'i': 3, 'v2': 3, 'v3': 0}, 'i')` |
| **结果** | `3` |

#### `struct_extract(struct, idx)`

<div class="nostroke_table"></div>

| **描述** | 使用索引（1-based）从未命名的 `STRUCT`（元组）中提取条目。 |
| **示例** | `struct_extract(row(42, 84), 1)` |
| **结果** | `42` |

#### `struct_extract_at(struct, idx)`

<div class="nostroke_table"></div>

| **描述** | 使用索引（1-based）从 `STRUCT`（元组）中提取条目。 |
| **示例** | `struct_extract_at({'v1': 10, 'v2': 20, 'v3': 3}, 20)` |
| **结果** | `20` |

#### `struct_insert(struct, name := any, ...)`

<div class="nostroke_table"></div>

| **描述** | 向现有的 `STRUCT` 中添加字段/值，使用参数值。条目名称将为绑定变量名称。 |
| **示例** | `struct_insert({'a': 1}, b := 2)` |
| **结果** | `{'a': 1, 'b': 2}` |

#### `struct_pack(name := any, ...)`

<div class="nostroke_table"></div>

| **描述** | 创建一个包含参数值的 `STRUCT`。条目名称将为绑定变量名称。 |
| **示例** | `struct_pack(i := 4, s := 'string')` |
| **结果** | `{'i': 4, 's': string}` |