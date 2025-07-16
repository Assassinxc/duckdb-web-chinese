---
---
layout: docu
redirect_from:
- /docs/sql/functions/map
title: Map 函数
---

<!-- markdownlint-disable MD001 -->

| 名称 | 描述 |
|:--|:-------|
| [`cardinality(map)`](#cardinalitymap) | 返回 map 的大小（或 map 中的条目数）。 |
| [`element_at(map, key)`](#element_atmap-key) | 返回给定 key 对应的值，如果 key 不在 map 中则返回 `NULL`。第二个参数提供的 key 类型必须与 map 的 key 类型匹配，否则将返回错误。 |
| [`map_concat(maps...)`](#map_concatmaps) | 返回由合并输入 `maps` 创建的 map。在 key 冲突时，取最后一个具有该 key 的 map 的值。 |
| [`map_contains(map, key)`](#map_containsmap-key) | 检查 map 是否包含指定的 key。 |
| [`map_contains_entry(map, key, value)`](#map_contains_entrymap-key-value) | 检查 map 是否包含指定的 key-value 对。 |
| [`map_contains_value(map, value)`](#map_contains_valuemap-value) | 检查 map 是否包含指定的 value。 |
| [`map_entries(map)`](#map_entriesmap) | 返回 map 中每个 key-value 对的 struct(k, v) 列表。 |
| [`map_extract(map, key)`](#map_extractmap-key) | 返回指定 `key` 的值作为列表，如果 key 不在 map 中则返回 `NULL`。第二个参数提供的 key 类型必须与 map 的 key 类型匹配，否则将返回错误。 |
| [`map_extract_value(map, key)`](#map_extract_valuemap-key) | 返回指定 `key` 的值，如果 `key` 不在 map 中则返回 `NULL`。第二个参数提供的 key 类型必须与 map 的 key 类型匹配，否则将返回错误。 |
| [`map_from_entries(STRUCT(k, v)[])`](#map_from_entriesstructk-v) | 从数组的条目创建 map。 |
| [`map_keys(map)`](#map_keysmap) | 返回 map 中的所有 key 列表。 |
| [`map_values(map)`](#map_valuesmap) | 返回 map 中的所有 value 列表。 |
| [`map()`](#map) | 返回一个空 map。 |
| [`map[entry]`](#mapentry) | 返回指定 key 的值，如果 key 不在 map 中则返回 `NULL`。第二个参数提供的 key 类型必须与 map 的 key 类型匹配，否则将返回错误。 |

#### `cardinality(map)`

<div class="nostroke_table"></div>

| **描述** | 返回 map 的大小（或 map 中的条目数）。 |
| **示例** | `cardinality(map([4, 2], ['a', 'b']))` |
| **结果** | `2` |

#### `element_at(map, key)`

<div class="nostroke_table"></div>

| **描述** | 返回给定 key 对应的值，如果 key 不在 map 中则返回 `NULL`。第二个参数提供的 key 类型必须与 map 的 key 类型匹配，否则将返回错误。 |
| **示例** | `element_at(map([100, 5], [42, 43]), 100)` |
| **结果** | `[42]` |
| **别名** | `map_extract(map, key)`, `map[key]` |

#### `map_concat(maps...)`

<div class="nostroke_table"></div>

| **描述** | 返回由合并输入 `maps` 创建的 map。在 key 冲突时，取最后一个具有该 key 的 map 的值。 |
| **示例** | `map_concat(MAP {'key1': 10, 'key2': 20}, MAP {'key3': 30}, MAP {'key2': 5})` |
| **结果** | `{key1=10, key2=5, key3=30}` |

#### `map_contains(map, key)`

<div class="nostroke_table"></div>

| **描述** | 检查 map 是否包含指定的 key。 |
| **示例** | `map_contains(MAP {'key1': 10, 'key2': 20, 'key3': 30}, 'key2')` |
| **结果** | `true` |

#### `map_contains_entry(map, key, value)`

<div class="nostroke_table"></div>

| **描述** | 检查 map 是否包含指定的 key-value 对。 |
| **示例** | `map_contains_entry(MAP {'key1': 10, 'key2': 20, 'key3': 30}, 'key2', 20)` |
| **结果** | `true` |

#### `map_contains_value(map, value)`

<div class="nostroke_table"></div>

| **描述** | 检查 map 是否包含指定的 value。 |
| **示例** | `map_contains_value(MAP {'key1': 10, 'key2': 20, 'key3': 30}, 20)` |
| **结果** | `true` |

#### `map_entries(map)`

<div class="nostroke_table"></div>

| **描述** | 返回 map 中每个 key-value 对的 struct(k, v) 列表。 |
| **示例** | `map_entries(map([100, 5], [42, 43]))` |
| **结果** | `[{'key': 100, 'value': 42}, {'key': 5, 'value': 43}]` |

#### `map_extract(map, key)`

<div class="nostroke_table"></div>

| **描述** | 返回指定 `key` 的值作为列表，如果 key 不在 map 中则返回 `NULL`。第二个参数提供的 key 类型必须与 map 的 key 类型匹配，否则将返回错误。 |
| **示例** | `map_extract(map([100, 5], [42, 43]), 100)` |
| **结果** | `[42]` |
| **别名** | `element_at(map, key)`, `map[key]` |

#### `map_extract_value(map, key)`

<div class="nostroke_table"></div>

| **描述** | 返回指定 `key` 的值，如果 `key` 不在 map 中则返回 `NULL`。第二个参数提供的 key 类型必须与 map 的 key 类型匹配，否则将返回错误。 |
| **示例** | `map_extract_value(map([100, 5], [42, 43]), 100);` |
| **结果** | `42` |

#### `map_from_entries(STRUCT(k, v)[])`

<div class="nostroke_table"></div>

| **描述** | 从数组的条目创建 map。 |
| **示例** | `map_from_entries([{k: 5, v: 'val1'}, {k: 3, v: 'val2'}])` |
| **结果** | `{5=val1, 3=val2}` |

#### `map_keys(map)`

<div class="nostroke_table"></div>

| **描述** | 返回 map 中的所有 key 列表。 |
| **示例** | `map_keys(map([100, 5], [42,43]))` |
| **结果** | `[100, 5]` |

#### `map_values(map)`

<div class="nostroke_table"></div>

| **描述** | 返回 map 中的所有 value 列表。 |
| **示例** | `map_values(map([100, 5], [42, 43]))` |
| **结果** | `[42, 43]` |

#### `map()`

<div class="nostroke_table"></div>

| **描述** | 返回一个空 map。 |
| **示例** | `map()` |
| **结果** | `{}` |

#### `map[entry]`

<div class="nostroke_table"></div>

| **描述** | 返回指定 key 的值，如果 key 不在 map 中则返回 `NULL`。第二个参数提供的 key 类型必须与 map 的 key 类型匹配，否则将返回错误。 |
| **示例** | `map([100, 5], ['a', 'b'])[100]` |
| **结果** | `a` |
| **别名** | `element_at(map, key)`, `map_extract(map, key)` |