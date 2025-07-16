---
---
layout: docu
redirect_from:
- /docs/sql/functions/list
title: 列函数
---

<!-- markdownlint-disable MD001 MD056 -->

| 名称 | 描述 |
|:--|:-------|
| [`list[index]`](#listindex) | 括号表示法是 `list_extract` 的别名。 |
| [`list[begin:end]`](#listbeginend) | 括号表示法带冒号是 `list_slice` 的别名。 |
| [`list[begin:end:step]`](#listbeginendstep) | 括号表示法的 `list_slice` 增加了 `step` 功能。 |
| [`array_pop_back(list)`](#array_pop_backlist) | 返回一个没有最后一个元素的列表。 |
| [`array_pop_front(list)`](#array_pop_frontlist) | 返回一个没有第一个元素的列表。 |
| [`flatten(list_of_lists)`](#flattenlist_of_lists) | 将列表的列表连接成一个列表。这仅扁平化列表的一层（参见 [示例](#flattening)）。 |
| [`len(list)`](#lenlist) | 返回列表的长度。 |
| [`list_aggregate(list, name)`](#list_aggregatelist-name) | 在 `list` 的元素上执行名为 `name` 的聚合函数。有关更多详细信息，请参阅 [列表聚合]({% link docs/stable/sql/functions/list.md %}#list-aggregates) 部分。 |
| [`list_any_value(list)`](#list_any_valuelist) | 返回列表中的第一个非空值。 |
| [`list_append(list, element)`](#list_appendlist-element) | 将 `element` 添加到 `list`。 |
| [`list_concat(list1, ..., listn)`](#list_concatlist1--listn) | 连接列表。`NULL` 输入会被跳过。另请参见 `||` |
| [`list_contains(list, element)`](#list_containslist-element) | 如果列表包含元素，返回 `true`。 |
| [`list_cosine_similarity(list1, list2)`](#list_cosine_similaritylist1-list2) | 计算两个列表的余弦相似度。 |
| [`list_cosine_distance(list1, list2)`](#list_cosine_distancelist1-list2) | 计算两个列表的余弦距离。等同于 `1.0 - list_cosine_similarity`。 |
| [`list_distance(list1, list2)`](#list_distancelist1-list2) | 计算两个列表中坐标点的欧几里得距离。 |
| [`list_distinct(list)`](#list_distinctlist) | 从列表中删除所有重复项和 `NULL` 值。不保留原始顺序。 |
| [`list_dot_product(list1, list2)`](#list_dot_productlist1-list2) | 计算两个相同大小的数字列表的点积。 |
| [`list_negative_dot_product(list1, list2)`](#list_negative_dot_productlist1-list2) | 计算两个相同大小的数字列表的负点积。等同于 `- list_dot_product`。 |
| [`list_extract(list, index)`](#list_extractlist-index) | 从列表中提取 `index`（1 基）的值。 |
| [`list_filter(list, lambda)`](#list_filterlist-lambda) | 从输入列表中构造一个列表，其中 lambda 函数返回 `true`。有关更多详细信息，请参阅 [Lambda 函数]({% link docs/stable/sql/functions/lambda.md %}#filter) 页面。 |
| [`list_grade_up(list)`](#list_grade_uplist) | 与排序类似，但结果是与原始 `list` 中位置对应的索引，而不是实际值。 |
| [`list_has_all(list, sub-list)`](#list_has_alllist-sub-list) | 如果子列表中的所有元素都存在于列表中，返回 `true`。 |
| [`list_has_any(list1, list2)`](#list_has_anylist1-list2) | 如果任何元素存在于两个列表中，返回 `true`。 |
| [`list_intersect(list1, list2)`](#list_intersectlist1-list2) | 返回两个 `l1` 和 `l2` 中都存在的所有元素的列表，没有重复项。 |
| [`list_position(list, element)`](#list_positionlist-element) | 如果列表包含元素，返回元素的索引。如果未找到元素，返回 `NULL`。 |
| [`list_prepend(element, list)`](#list_prependelement-list) | 将 `element` 添加到 `list` 的前面。 |
| [`list_reduce(list, lambda)`](#list_reducelist-lambda) | 返回一个值，该值是通过将 lambda 函数应用于输入列表的每个元素得到的结果。有关更多详细信息，请参阅 [Lambda 函数]({% link docs/stable/sql/functions/lambda.md %}#reduce) 页面。 |
| [`list_resize(list, size[, value])`](#list_resizelist-size-value) | 将列表调整为包含 `size` 个元素。用 `value` 或 `NULL`（如果未设置 `value`）初始化新元素。 |
| [`list_reverse_sort(list)`](#list_reverse_sortlist) | 按照降序对列表的元素进行排序。有关 `NULL` 排序顺序的更多详细信息，请参阅 [排序列表]({% link docs/stable/sql/functions/list.md %}#sorting-lists) 部分。 |
| [`list_reverse(list)`](#list_reverselist) | 反转列表。 |
| [`list_select(value_list, index_list)`](#list_selectvalue_list-index_list) | 根据 `index_list` 选择的元素返回一个列表。 |
| [`list_slice(list, begin, end, step)`](#list_slicelist-begin-end-step) | 带有 `step` 功能的 `list_slice`。 |
| [`list_slice(list, begin, end)`](#list_slicelist-begin-end) | 使用切片约定提取子列表。接受负值。参见 [切片]({% link docs/stable/sql/functions/list.md %}#slicing)。 |
| [`list_sort(list)`](#list_sortlist) | 对列表的元素进行排序。有关排序顺序和 `NULL` 排序顺序的更多详细信息，请参阅 [排序列表]({% link docs/stable/sql/functions/list.md %}#sorting-lists) 部分。 |
| [`list_transform(list, lambda)`](#list_transformlist-lambda) | 返回通过将 lambda 函数应用于输入列表的每个元素得到的结果列表。有关更多详细信息，请参阅 [Lambda 函数]({% link docs/stable/sql/functions/lambda.md %}#transform) 页面。 |
| [`list_unique(list)`](#list_uniquelist) | 计算列表中的唯一元素。 |
| [`list_value(any, ...)`](#list_valueany-) | 创建一个包含参数值的 `LIST`。 |
| [`list_where(value_list, mask_list)`](#list_wherevalue_list-mask_list) | 返回一个列表，其中 `mask_list` 中的 `BOOLEAN` 作为掩码应用于 `value_list`。 |
| [`list_zip(list_1, list_2, ...[, truncate])`](#list_ziplist1-list2-) | 将 _k_ 个 `LIST` 压缩成一个新的 `LIST`，其长度为最长的列表。其元素是每个列表 `list_1`、`list_k` 的 _k_ 个元素的结构，缺失的元素用 `NULL` 替换。如果设置了 `truncate`，所有列表将截断为最短列表长度。 |
| [`repeat(list, count)`](#repeatlist-count) | 重复 `list` `count` 次。 |
| [`unnest(list)`](#unnestlist) | 通过一个级别展开列表。请注意，这是一个特殊的函数，会改变结果的基数。有关更多详细信息，请参阅 [`unnest` 页面]({% link docs/stable/sql/query_syntax/unnest.md %})。 |

#### `list[index]`

<div class="nostroke_table"></div>

| **描述** | 括号表示法是 `list_extract` 的别名。 |
| **示例** | `[4, 5, 6][3]` |
| **结果** | `6` |
| **别名** | `list_extract` |

#### `list[begin:end]`

<div class="nostroke_table"></div>

| **描述** | 括号表示法带冒号是 `list_slice` 的别名。 |
| **示例** | `[4, 5, 6][2:3]` |
| **结果** | `[5, 6]` |
| **别名** | `list_slice` |

#### `list[begin:end:step]`

<div class="nostroke_table"></div>

| **描述** | 括号表示法的 `list_slice` 增加了 `step` 功能。 |
| **示例** | `[4, 5, 6][:-:2]` |
| **结果** | `[4, 6]` |
| **别名** | `list_slice` |

#### `array_pop_back(list)`

<div class="nostroke_table"></div>

| **描述** | 返回一个没有最后一个元素的列表。 |
| **示例** | `array_pop_back([4, 5, 6])` |
| **结果** | `[4, 5]` |

#### `array_pop_front(list)`

<div class="nostroke_table"></div>

| **描述** | 返回一个没有第一个元素的列表。 |
| **示例** | `array_pop_front([4, 5, 6])` |
| **结果** | `[5, 6]` |

#### `flatten(list_of_lists)`

<div class="nostroke_table"></div>

| **描述** | 将列表的列表连接成一个列表。这仅扁平化列表的一层（参见 [示例](#flattening)）。 |
| **示例** | `flatten([[1, 2], [3, 4]])` |
| **结果** | `[1, 2, 3, 4]` |

#### `len(list)`

<div class="nostroke_table"></div>

| **描述** | 返回列表的长度。 |
| **示例** | `len([1, 2, 3])` |
| **结果** | `3` |
| **别名** | `array_length` |

#### `list_aggregate(list, name)`

<div class="nostroke_table"></div>

| **描述** | 在 `list` 的元素上执行名为 `name` 的聚合函数。有关更多详细信息，请参阅 [列表聚合]({% link docs/stable/sql/functions/list.md %}#list-aggregates) 部分。 |
| **示例** | `list_aggregate([1, 2, NULL], 'min')` |
| **结果** | `1` |
| **别名** | `list_aggr`, `aggregate`, `array_aggregate`, `array_aggr` |

#### `list_any_value(list)`

<div class="nostroke_table"></div>

| **描述** | 返回列表中的第一个非空值。 |
| **示例** | `list_any_value([NULL, -3])` |
| **结果** | `-3` |

#### `list_append(list, element)`

<div class="nostroke_table"></div>

| **描述** | 将 `element` 添加到 `list`。 |
| **示例** | `list_append([2, 3], 4)` |
| **结果** | `[2, 3, 4]` |
| **别名** | `array_append`, `array_push_back` |

#### `list_concat(list1, ..., listn)`

<div class="nostroke_table"></div>

| **描述** | 连接列表。`NULL` 输入被跳过。另请参见 `||` |
| **示例** | `list_concat([2, 3], [4, 5, 6], [7])` |
| **结果** | `[2, 3, 4, 5, 6, 7]` |
| **别名** | `list_cat`, `array_concat`, `array_cat` |

#### `list_contains(list, element)`

<div class="nostroke_table"></div>

| **描述** | 如果列表包含元素，返回 `true`。 |
| **示例** | `list_contains([1, 2, NULL], 1)` |
| **结果** | `true` |
| **别名** | `list_has`, `array_contains`, `array_has` |

#### `list_cosine_similarity(list1, list2)`

<div class="nostroke_table"></div>

| **描述** | 计算两个列表的余弦相似度。 |
| **示例** | `list_cosine_similarity([1, 2, 3], [1, 2, 5])` |
| **结果** | `0.9759000729485332` |

#### `list_cosine_distance(list1, list2)`

<div class="nostroke_table"></div>

| **描述** | 计算两个列表的余弦距离。等同于 `1.0 - list_cosine_similarity` |
| **示例** | `list_cosine_distance([1, 2, 3], [1, 2, 5])` |
| **结果** | `0.024099927051466796` |

#### `list_distance(list1, list2)`

<div class="nostroke_table"></div>

| **描述** | 计算两个列表中坐标点的欧几里得距离。 |
| **示例** | `list_distance([1, 2, 3], [1, 2, 5])` |
| **结果** | `2.0` |

#### `list_distinct(list)`

<div class="nostroke_table"></div>

| **描述** | 从列表中删除所有重复项和 `NULL` 值。不保留原始顺序。 |
| **示例** | `list_distinct([1, 1, NULL, -3, 1, 5])` |
| **结果** | `[1, 5, -3]` |
| **别名** | `array_distinct` |

#### `list_dot_product(list1, list2)`

<div class="nostroke_table"></div>

| **描述** | 计算两个相同大小的数字列表的点积。 |
| **示例** | `list_dot_product([1, 2, 3], [1, 2, 5])` |
| **结果** | `20.0` |
| **别名** | `list_inner_product` |

#### `list_negative_dot_product(list1, list2)`

<div class="nostroke_table"></div>

| **描述** | 计算两个相同大小的数字列表的负点积。等同于 `- list_dot_product` |
| **示例** | `list_negative_dot_product([1, 2, 3], [1, 2, 5])` |
| **结果** | `-20.0` |
| **别名** | `list_negative_inner_product` |

#### `list_extract(list, index)`

<div class="nostroke_table"></div>

| **描述** | 从列表中提取 `index`（1 基）的值。 |
| **示例** | `list_extract([4, 5, 6], 3)` |
| **结果** | `6` |
| **别名** | `list_element`, `array_extract` |

#### `list_filter(list, lambda)`

<div class="nostroke_table"></div>

| **描述** | 从输入列表中构造一个列表，其中 lambda 函数返回 `true`。有关更多详细信息，请参阅 [Lambda 函数]({% link docs/stable/sql/functions/lambda.md %}#filter) 页面。 |
| **示例** | `list_filter([4, 5, 6], x -> x > 4)` |
| **结果** | `[5, 6]` |
| **别名** | `array_filter`, `filter` |

#### `list_grade_up(list)`

<div class="nostroke_table"></div>

| **描述** | 与排序类似，但结果是与原始 `list` 中位置对应的索引，而不是实际值。 |
| **示例** | `list_grade_up([30, 10, 40, 20])` |
| **结果** | `[2, 4, 1, 3]` |
| **别名** | `array_grade_up` |

#### `list_has_all(list, sub-list)`

<div class="nostroke_table"></div>

| **描述** | 如果子列表中的所有元素都存在于列表中，返回 `true`。 |
| **示例** | `list_has_all([4, 5, 6], [4, 6])` |
| **结果** | `true` |
| **别名** | `array_has_all` |

#### `list_has_any(list1, list2)`

<div class="nostroke_table"></div>

| **描述** | 如果任何元素存在于两个列表中，返回 `true`。 |
| **示例** | `list_has_any([1, 2, 3], [2, 3, 4])` |
| **结果** | `true` |
| **别名** | `array_has_any` |

#### `list_intersect(list1, list2)`

<div class="nostroke_table"></div>

| **描述** | 返回两个 `l1` 和 `l2` 中都存在的所有元素的列表，没有重复项。 |
| **示例** | `list_intersect([1, 2, 3], [2, 3, 4])` |
| **结果** | `[2, 3]` |
| **别名** | `array_intersect` |

#### `list_position(list, element)`

<div class="nostroke_table"></div>

| **描述** | 如果列表包含元素，返回元素的索引。如果未找到元素，返回 `NULL`。 |
| **示例** | `list_position([1, 2, NULL], 2)` |
| **结果** | `2` |
| **别名** | `list_indexof`, `array_position`, `array_indexof` |

#### `list_prepend(element, list)`

<div class="nostroke_table"></div>

| **描述** | 将 `element` 添加到 `list` 的前面。 |
| **示例** | `list_prepend(3, [4, 5, 6])` |
| **结果** | `[3, 4, 5, 6]` |
| **别名** | `array_prepend`, `array_push_front` |

#### `list_reduce(list, lambda)`

<div class="nostroke_table"></div>

| **描述** | 返回一个值，该值是通过将 lambda 函数应用于输入列表的每个元素得到的结果。有关更多详细信息，请参阅 [Lambda 函数]({% link docs/stable/sql/functions/lambda.md %}#reduce) 页面。 |
| **示例** | `list_reduce([4, 5, 6], (acc, x) -> acc + x)` |
| **结果** | `15` |
| **别名** | `array_reduce`, `reduce` |

#### `list_resize(list, size[, value])`

<div class="nostroke_table"></div>

| **描述** | 将列表调整为包含 `size` 个元素。用 `value` 或 `NULL`（如果未设置 `value`）初始化新元素。 |
| **示例** | `list_resize([1, 2, 3], 5, 0)` |
| **结果** | `[1, 2, 3, 0, 0]` |
| **别名** | `array_resize` |

#### `list_reverse_sort(list)`

<div class="nostroke_table"></div>

| **描述** | 按照降序对列表的元素进行排序。有关 `NULL` 排序顺序的更多详细信息，请参阅 [排序列表]({% link docs/stable/sql/functions/list.md %}#sorting-lists) 部分。 |
| **示例** | `list_reverse_sort([3, 6, 1, 2])` |
| **结果** | `[6, 3, 2, 1]` |
| **别名** | `array_reverse_sort` |

#### `list_reverse(list)`

<div class="nostroke_table"></div>

| **描述** | 反转列表。 |
| **示例** | `list_reverse([3, 6, 1, 2])` |
| **结果** | `[2, 1, 6, 3]` |
| **别名** | `array_reverse` |

#### `list_select(value_list, index_list)`

<div class="nostroke_table"></div>

| **描述** | 返回基于 `index_list` 选择的元素的列表。 |
| **示例** | `list_select([10, 20, 30, 40], [1, 4])` |
| **结果** | `[10, 40]` |
| **别名** | `array_select` |

#### `list_slice(list, begin, end, step)`

<div class="nostroke_table"></div>

| **描述** | 带有 `step` 功能的 `list_slice`。 |
| **示例** | `list_slice([4, 5, 6], 1, 3, 2)` |
| **结果** | `[4, 6]` |
| **别名** | `array_slice` |

#### `list_slice(list, begin, end)`

<div class="nostroke_table"></div>

| **描述** | 使用切片约定提取子列表。接受负值。参见 [切片]({% link docs/stable/sql/functions/list.md %}#slicing)。 |
| **示例** | `list_slice([4, 5, 6], 2, 3)` |
| **结果** | `[5, 6]` |
| **别名** | `array_slice` |

#### `list_sort(list)`

<div class="nostroke_table"></div>

| **描述** | 对列表的元素进行排序。有关排序顺序和 `NULL` 排序顺序的更多详细信息，请参阅 [排序列表]({% link docs/stable/sql/functions/list.md %}#sorting-lists) 部分。 |
| **示例** | `list_sort([3, 6, 1, 2])` |
| **结果** | `[1, 2, 3, 6]` |
| **别名** | `array_sort` |

#### `list_transform(list, lambda)`

<div class="nostroke_table"></div>

| **描述** | 返回通过将 lambda 函数应用于输入列表的每个元素得到的结果列表。有关更多详细信息，请参阅 [Lambda 函数]({% link docs/stable/sql/functions/lambda.md %}#transform) 页面。 |
| **示例** | `list_transform([4, 5, 6], x -> x + 1)` |
| **结果** | `[5, 6, 7]` |
| **别名** | `array_transform`, `apply`, `list_apply`, `array_apply` |

#### `list_unique(list)`

<div class="nostroke_table"></div>

| **描述** | 计算列表中的唯一元素。 |
| **示例** | `list_unique([1, 1, NULL, -3, 1, 5])` |
| **结果** | `3` |
| **别名** | `array_unique` |

#### `list_value(any, ...)`

<div class="nostroke_table"></div>

| **描述** | 创建一个包含参数值的 `LIST`。 |
| **示例** | `list_value(4, 5, 6)` |
| **结果** | `[4, 5, 6]` |
| **别名** | `list_pack` |

#### `list_where(value_list, mask_list)`

<div class="nostroke_table"></div>

| **描述** | 返回一个列表，其中 `mask_list` 中的 `BOOLEAN` 作为掩码应用于 `value_list`。 |
| **示例** | `list_where([10, 20, 30, 40], [true, false, false, true])` |
| **结果** | `[10, 40]` |
| **别名** | `array_where` |

#### `list_zip(list1, list2, ...)`

<div class="nostroke_table"></div>

| **描述** | 将 _k_ 个 `LIST` 压缩成一个新的 `LIST`，其长度为最长列表的长度。其元素是每个列表 `list_1`、`list_k` 的 _k_ 个元素的结构，缺失的元素用 `NULL` 替换。如果设置了 `truncate`，所有列表将截断为最短列表长度。 |
| **示例** | `list_zip([1, 2], [3, 4], [5, 6])` |
| **结果** | `[(1, 3, 5), (2, 4, 6)]` |
| **别名** | `array_zip` |

#### `repeat(list, count)`

<div class="nostroke_table"></div>

| **描述** | 重复 `list` `count` 次。 |
| **示例** | `repeat([1, 2], 5)` |
| **结果** | `[1, 2, 1, 2, 1, 2, 1, 2, 1, 2]` |

#### `unnest(list)`

<div class="nostroke_table"></div>

| **描述** | 通过一个级别展开列表。请注意，这是一个特殊的函数，会改变结果的基数。有关更多详细信息，请参阅 [`unnest` 页面]({% link docs/stable/sql/query_syntax/unnest.md %})。 |
| **示例** | `unnest([1, 2, 3])` |
| **结果** | `1`, `2`, `3` |

## 列操作符

以下操作符可用于列表：

<!-- markdownlint-disable MD056 -->

| 操作符 | 描述 | 示例 | 结果 |
|-|--|---|-|
| `&&`  | [`list_has_any`](#list_has_anylist1-list2) 的别名。                                                                   | `[1, 2, 3, 4, 5] && [2, 5, 5, 6]` | `true`               |
| `@>`  | [`list_has_all`](#list_has_alllist-sub-list) 的别名，其中操作符右侧的列表是子列表。 | `[1, 2, 3, 4] @> [3, 4, 3]`       | `true`               |
| `<@`  | [`list_has_all`](#list_has_alllist-sub-list) 的别名，其中操作符左侧的列表是子列表。  | `[1, 4] <@ [1, 2, 3, 4]`          | `true`               |
| `||`  | 与 [`list_concat`](#list_concatlist1--listn) 类似，但任何 `NULL` 输入会导致 `NULL`。                        | `[1, 2, 3] || [4, 5, 6]`          | `[1, 2, 3, 4, 5, 6]` |
| `<=>` | [`list_cosine_distance`](#list_cosine_distancelist1-list2) 的别名。                                                   | `[1, 2, 3] <=> [1, 2, 5]`         | `0.007416606`        |
| `<->` | [`list_distance`](#list_distancelist1-list2) 的别名。                                                                 | `[1, 2, 3] <-> [1, 2, 5]`         | `2.0`                |

<!-- markdownlint-enable MD056 -->

## 列推导

可以使用 Python 风格的列推导来计算列表中元素的表达式。例如：

```sql
SELECT [lower(x) FOR x IN strings] AS strings
FROM (VALUES (['Hello', '', 'World'])) t(strings);
```

<div class="monospace_table"></div>

|     strings      |
|------------------|
| [hello, , world] |

```sql
SELECT [upper(x) FOR x IN strings IF len(x) > 0] AS strings
FROM (VALUES (['Hello', '', 'World'])) t(strings);
```

<div class="monospace_table"></div>

|    strings     |
|----------------|
| [HELLO, WORLD] |

列推导还可以通过添加第二个变量来使用列表元素的位置。
在下面的示例中，我们使用 `x, i`，其中 `x` 是值，`i` 是位置：

```sql
SELECT [4, 5, 6] AS l, [x FOR x, i IN l IF i != 2] AS filtered;
```

<div class="monospace_table"></div>

|     l     | filtered |
|-----------|----------|
| [4, 5, 6] | [4, 6]   |

在底层，`[f(x) FOR x IN y IF g(x)]` 会被翻译为 `list_transform(list_filter(y, x -> f(x)), x -> f(x))`。

## 范围函数

DuckDB 提供了两个范围函数， [`range(start, stop, step)`](#range) 和 [`generate_series(start, stop, step)`](#generate_series)，以及它们具有默认参数的变体。这两个函数在 `stop` 参数的行为上有所不同。以下文档详细说明了这些差异。

### `range`

`range` 函数创建一个值在 `start` 和 `stop` 范围内的列表。
`start` 参数是包含的，而 `stop` 参数是排除的。
`start` 的默认值为 0，`step` 的默认值为 1。

根据参数的数量，`range` 存在以下变体。

#### `range(stop)`

```sql
SELECT range(5);
```

```text
[0, 1, 2, 3, 4]
```

#### `range(start, stop)`

```sql
SELECT range(2, 5);
```

```text
[2, 3, 4]
```

#### `range(start, stop, step)`

```sql
SELECT range(2, 5, 3);
```

```text
[2]
```

### `generate_series`

`generate_series` 函数创建一个值在 `start` 和 `stop` 范围内的列表。
`start` 和 `stop` 参数都是包含的。
`start` 的默认值为 0，`step` 的默认值为 1。
根据参数的数量，`generate_series` 存在以下变体。

#### `generate_series(stop)`

```sql
SELECT generate_series(5);
```

```text
[0, 1, 2, 3, 4, 5]
```

#### `generate_series(start, stop)`

```sql
SELECT generate_series(2, 5);
```

```text
[2, 3, 4, 5]
```

#### `generate_series(start, stop, step)`

```sql
SELECT generate_series(2, 5, 3);
```

```text
[2, 5]
```

#### `generate_subscripts(arr, dim)`

`generate_subscripts(arr, dim)` 函数生成数组 `arr` 的 `dim` 维度的索引。

```sql
SELECT generate_subscripts([4, 5, 6], 1) AS i;
```

| i |
|--:|
| 1 |
| 2 |
| 3 |

### 日期范围

`TIMESTAMP` 和 `TIMESTAMP WITH TIME ZONE` 值也支持日期范围。
请注意，对于这些类型，必须显式指定 `stop` 和 `step` 参数（不提供默认值）。

#### `range` 用于日期范围

```sql
SELECT *
FROM range(DATE '1992-01-01', DATE '1992-03-01', INTERVAL '1' MONTH);
```

|        range        |
|---------------------|
| 1992-01-01 00:00:00 |
| 1992-02-01 00:00:00 |

#### `generate_series` 用于日期范围

```sql
SELECT *
FROM generate_series(DATE '1992-01-01', DATE '1992-03-01', INTERVAL '1' MONTH);
```

|   generate_series   |
|---------------------|
| 1992-01-01 00:00:00 |
| 1992-02-01 00:00:00 |
| 1992-03-01 00:00:00 |

## 切片

可以使用 [`list_slice`](#list_slicelist-begin-end) 函数从列表中提取子列表。存在以下变体：

* `list_slice(list, begin, end)`
* `list_slice(list, begin, end, step)`
* `array_slice(list, begin, end)`
* `array_slice(list, begin, end, step)`
* `list[begin:end]`
* `list[begin:end:step]`

参数如下：

* `list`
    * 是要切片的列表
* `begin`
    * 是要包含在切片中的第一个元素的索引
    * 当 `begin < 0` 时，索引从列表末尾开始计算
    * 当 `begin < 0` 且 `-begin > length` 时，`begin` 会被限制为列表的开头
    * 当 `begin > length` 时，结果是一个空列表
    * **括号表示法**：当 `begin` 被省略时，默认为列表的开头
* `end`
    * 是要包含在切片中的最后一个元素的索引
    * 当 `end < 0` 时，索引从列表末尾开始计算
    * 当 `end > length` 时，`end` 会被限制为 `length`
    * 当 `end < begin` 时，结果是一个空列表
    * **括号表示法**：当 `end` 被省略时，默认为列表的末尾。当 `end` 被省略且提供了 `step` 时，`end` 必须替换为 `-`
* `step` *(可选)*
    * 是切片中元素之间的步长
    * 当 `step < 0` 时，切片会反转，且 `begin` 和 `end` 会被交换
    * 必须是非零值

示例：

```sql
SELECT list_slice([1, 2, 3, 4, 5], 2, 4);
```

```text
[2, 3, 4]
```

```sql
SELECT ([1, 2, 3, 4, 5])[2:4:2];
```

```text
[2, 4]
```

```sql
SELECT([1, 2, 3, 4, 5])[4:2:-2];
```

```text
[4, 2]
```

```sql
SELECT ([1, 2, 3, 4, 5])[:];
```

```text
[1, 2, 3, 4, 5]
```

```sql
SELECT ([1, 2, 3, 4, 5])[:-:2];
```

```text
[1, 3, 5]
```

```sql
SELECT ([1, 2, 3, 4, 5])[:-:-2];
```

```text
[5, 3, 1]
```

## 列聚合

`list_aggregate` 函数允许在列表的元素上执行任意现有的聚合函数。它的第一个参数是列表（列），第二个参数是聚合函数名称，例如 `min`、`histogram` 或 `sum`。

`list_aggregate` 可以在聚合函数名称之后接受额外的参数。这些额外的参数会直接传递给聚合函数，该函数作为 `list_aggregate` 的第二个参数。

```sql
SELECT list_aggregate([1, 2, -4, NULL], 'min');
```

```text
-4
```

```sql
SELECT list_aggregate([2, 4, 8, 42], 'sum');
```

```text
56
```

```sql
SELECT list_aggregate([[1, 2], [NULL], [2, 10, 3]], 'last');
```

```text
[2, 10, 3]
```

```sql
SELECT list_aggregate([2, 4, 8, 42], 'string_agg', '|');
```

```text
2|4|8|42
```

### `list_*` 重写函数

以下是一些现有的重写函数。重写函数通过仅接受列表（列）作为参数来简化列表聚合函数的使用。`list_avg`, `list_var_samp`, `list_var_pop`, `list_stddev_pop`, `list_stddev_samp`, `list_sem`, `list_approx_count_distinct`, `list_bit_xor`, `list_bit_or`, `list_bit_and`, `list_bool_and`, `list_bool_or`, `list_count`, `list_entropy`, `list_last`, `list_first`, `list_kurtosis`, `list_kurtosis_pop`, `list_min`, `list_max`, `list_product`, `list_skewness`, `list_sum`, `list_string_agg`, `list_mode`, `list_median`, `list_mad` 和 `list_histogram`。

```sql
SELECT list_min([1, 2, -4, NULL]);
```

```text
-4
```

```sql
SELECT list_sum([2, 4, 8, 42]);
```

```text
56
```

```sql
SELECT list_last([[1, 2], [NULL], [2, 10, 3]]);
```

```text
[2, 10, 3]
```

#### `array_to_string`

使用可选分隔符连接列表/数组元素。

```sql
SELECT array_to_string([1, 2, 3], '-') AS str;
```

```text
1-2-3
```

这等同于以下 SQL：

```sql
SELECT list_aggr([1, 2, 3], 'string_agg', '-') AS str;
```

```text
1-2-3
```

## 排序列表

`list_sort` 函数可以按升序或降序对列表元素进行排序。此外，它允许指定 `NULL` 值是否应移动到列表的开头或末尾。`list_sort` 的排序行为与 DuckDB 的 `ORDER BY` 子句相同。因此，在 `list_sort` 中，(嵌套) 值的比较与 `ORDER BY` 中的比较相同。

默认情况下，如果没有提供修饰符，DuckDB 会使用 `ASC NULLS FIRST` 排序。即，值按升序排列，`NULL` 值放在前面。这与 SQLite 的默认排序顺序相同。可以通过 [`PRAGMA` 语句.](../query_syntax/orderby) 修改默认排序顺序。

`list_sort` 留给用户决定是否使用默认排序顺序或自定义顺序。`list_sort` 可以接受最多两个额外的可选参数。第二个参数提供排序顺序，可以是 `ASC` 或 `DESC`。第三个参数提供 `NULL` 顺序，可以是 `NULLS FIRST` 或 `NULLS LAST`。

此查询使用默认排序顺序和默认的 `NULL` 顺序。

```sql
SELECT list_sort([1, 3, NULL, 5, NULL, -5]);
```

```sql
[NULL, NULL, -5, 1, 3, 5]
```

此查询提供排序顺序。`NULL` 顺序使用可配置的默认值。

```sql
SELECT list_sort([1, 3, NULL, 2], 'ASC');
```

```sql
[NULL, 1, 2, 3]
```

此查询提供排序顺序和 `NULL` 顺序。

```sql
SELECT list_sort([1, 3, NULL, 2], 'DESC', 'NULLS FIRST');
```

```sql
[NULL, 3, 2, 1]
```

`list_reverse_sort` 有一个可选的第二个参数，提供 `NULL` 排序顺序。它可以是 `NULLS FIRST` 或 `NULLS LAST`。

此查询使用默认的 `NULL` 排序顺序。

```sql
SELECT list_sort([1, 3, NULL, 5, NULL, -5]);
```

```sql
[NULL, NULL, -5, 1, 3, 5]
```

此查询提供 `NULL` 排序顺序。

```sql
SELECT list_reverse_sort([1, 3, NULL, 2], 'NULLS LAST');
```

```sql
[3, 2, 1, NULL]
```

## 扁平化

`flatten` 函数是一个标量函数，通过将每个子列表连接起来，将列表的列表转换为单个列表。请注意，这仅扁平化一层，而不是所有子列表的层。

将列表的列表转换为单个列表：

```sql
SELECT
    flatten([
        [1, 2],
        [3, 4]
    ]);
```

```text
[1, 2, 3, 4]
```

如果列表有多个层次的列表，仅将第一层的子列表连接成一个列表：

```sql
SELECT
    flatten([
        [
            [1, 2],
            [3, 4],
        ],
        [
            [5, 6],
            [7, 8],
        ]
    ]);
```

```text
[[1, 2], [3, 4], [5, 6], [7, 8]]
```

通常，`flatten` 函数的输入应是一个列表的列表（而不是一个单层列表）。然而，`flatten` 函数在处理空列表和 `NULL` 值时有特定的行为。

如果输入列表为空，返回一个空列表：

```sql
SELECT flatten([]);
```

```text
[]
```

如果整个 `flatten` 输入为 `NULL`，返回 `NULL`：

```sql
SELECT flatten(NULL);
```

```text
NULL
```

如果一个列表的唯一条目是 `NULL`，则扁平化后返回一个空列表：

```sql
SELECT flatten([NULL]);
```

```text
[]
```

如果一个列表的子列表仅包含 `NULL`，则不修改子列表：

```sql
-- （注意与前面示例中的额外括号）
SELECT flatten([[NULL]]);
```

```text
[NULL]
```

即使每个子列表的唯一内容是 `NULL`，仍然将其连接在一起。请注意，在扁平化时不会去重。有关去重，请参阅 `list_distinct` 函数：

```sql
SELECT flatten([[NULL], [NULL]]);
```

```text
[NULL, NULL]
```

## Lambda 函数

DuckDB 支持形式为 `(parameter1, parameter2, ...) -> expression` 的 Lambda 函数。有关详细信息，请参阅 [Lambda 函数页面]({% link docs/stable/sql/functions/lambda.md %})。

## 相关函数

* [聚合函数]({% link docs/stable/sql/functions/aggregates.md %}) `list` 和 `histogram` 生成列表和结构体列表。
* [`unnest` 函数]({% link docs/stable/sql/query_syntax/unnest.md %}) 用于展开列表一层。