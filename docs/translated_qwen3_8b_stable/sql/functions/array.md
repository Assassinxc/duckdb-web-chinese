---
---
layout: docu
redirect_from:
- /docs/sql/functions/array
title: 数组函数
---

<!-- markdownlint-disable MD001 -->

所有 [`LIST` 函数]({% link docs/stable/sql/functions/list.md %}) 都适用于 [`ARRAY` 数据类型]({% link docs/stable/sql/data_types/array.md %})。此外，还支持一些 `ARRAY` 原生函数。

## 数组原生函数

| 函数 | 描述 |
|----|-----|
| [`array_value(arg1, ...)`](#array_valueindex)                                                  | 创建一个包含参数值的 `ARRAY`。                                                                                                                                                                                              |
| [`array_cross_product(array1, array2)`](#array_cross_productarray1-array2)                     | 计算两个大小为 3 的数组的叉积。数组元素不能为 `NULL`。                                                                                                                                                       |
| [`array_cosine_similarity(array1, array2)`](#array_cosine_similarityarray1-array2)             | 计算两个大小相同的数组的余弦相似度。数组元素不能为 `NULL`。只要两个数组的大小相同，数组可以有任意大小。                                                      |
| [`array_cosine_distance(array1, array2)`](#array_cosine_distancearray1-array2)                 | 计算两个大小相同的数组的余弦距离。数组元素不能为 `NULL`。只要两个数组的大小相同，数组可以有任意大小。这等价于 `1.0 - array_cosine_similarity`。 |
| [`array_distance(array1, array2)`](#array_distancearray1-array2)                               | 计算两个大小相同的数组之间的距离。数组元素不能为 `NULL`。只要两个数组的大小相同，数组可以有任意大小。                                                               |
| [`array_inner_product(array1, array2)`](#array_inner_productarray1-array2)                     | 计算两个大小相同的数组的内积。数组元素不能为 `NULL`。只要两个数组的大小相同，数组可以有任意大小。                                                          |
| [`array_negative_inner_product(array1, array2)`](#array_negative_inner_productarray1-array2)   | 计算两个大小相同的数组的负内积。数组元素不能为 `NULL`。只要两个数组的大小相同，数组可以有任意大小。这等价于 `-array_inner_product`。   |
| [`array_dot_product(array1, array2)`](#array_dot_productarray1-array2)                         | `array_inner_product(array1, array2)` 的别名。                                                                                                                                                                                               |
| [`array_negative_dot_product(array1, array2)`](#array_negative_dot_productarray1-array2)       | `array_negative_inner_product(array1, array2)` 的别名。                                                                                                                                                                                      |

#### `array_value(arg1, ..)`

<div class="nostroke_table"></div>

| **描述** | 创建一个包含参数值的 `ARRAY`。 |
| **示例** | `array_value(1.0::FLOAT, 2.0::FLOAT, 3.0::FLOAT)` |
| **结果** | `[1.0, 2.0, 3.0]` |

#### `array_cross_product(array1, array2)`

<div class="nostroke_table"></div>

| **描述** | 计算两个大小为 3 的数组的叉积。数组元素不能为 `NULL`。 |
| **示例** | `array_cross_product(array_value(1.0::FLOAT, 2.0::FLOAT, 3.0::FLOAT), array_value(2.0::FLOAT, 3.0::FLOAT, 4.0::FLOAT))` |
| **结果** | `[-1.0, 2.0, -1.0]` |

#### `array_cosine_similarity(array1, array2)`

<div class="nostroke_table"></div>

| **描述** | 计算两个大小相同的数组的余弦相似度。数组元素不能为 `NULL`。只要两个数组的大小相同，数组可以有任意大小。 |
| **示例** | `array_cosine_similarity(array_value(1.0::FLOAT, 2.0::FLOAT, 3.0::FLOAT), array_value(2.0::FLOAT, 3.0::FLOAT, 4.0::FLOAT))` |
| **结果** | `0.9925833` |

#### `array_cosine_distance(array1, array2)`

<div class="nostroke_table"></div>

| **描述** | 计算两个大小相同的数组的余弦距离。数组元素不能为 `NULL`。只要两个数组的大小相同，数组可以有任意大小。这等价于 `1.0 - array_cosine_similarity`。 |
| **示例** | `array_cosine_distance(array_value(1.0::FLOAT, 2.0::FLOAT, 3.0::FLOAT), array_value(2.0::FLOAT, 3.0::FLOAT, 4.0::FLOAT))` |
| **结果** | `0.007416606` |

#### `array_distance(array1, array2)`

<div class="nostroke_table"></div>

| **描述** | 计算两个大小相同的数组之间的距离。数组元素不能为 `NULL`。只要两个数组的大小相同，数组可以有任意大小。 |
| **示例** | `array_distance(array_value(1.0::FLOAT, 2.0::FLOAT, 3.0::FLOAT), array_value(2.0::FLOAT, 3.0::FLOAT, 4.0::FLOAT))` |
| **结果** | `1.7320508` |

#### `array_inner_product(array1, array2)`

<div class="nostroke_table"></div>

| **描述** | 计算两个大小相同的数组的内积。数组元素不能为 `NULL`。只要两个数组的大小相同，数组可以有任意大小。 |
| **示例** | `array_inner_product(array_value(1.0::FLOAT, 2.0::FLOAT, 3.0::FLOAT), array_value(2.0::FLOAT, 3.0::FLOAT, 4.0::FLOAT))` |
| **结果** | `20.0` |

#### `array_negative_inner_product(array1, array2)`

<div class="nostroke_table"></div>

| **描述** | 计算两个大小相同的数组的负内积。数组元素不能为 `NULL`。只要两个数组的大小相同，数组可以有任意大小。这等价于 `-array_inner_product` |
| **示例** | `array_inner_product(array_value(1.0::FLOAT, 2.0::FLOAT, 3.0::FLOAT), array_value(2.0::FLOAT, 3.0::FLOAT, 4.0::FLOAT))` |
| **结果** | `-20.0` |

#### `array_dot_product(array1, array2)`

<div class="nostroke_table"></div>

| **描述** | `array_inner_product(array1, array2)` 的别名。 |
| **示例** | `array_dot_product(l1, l2)` |
| **结果** | `20.0` |

#### `array_negative_dot_product(array1, array2)`

<div class="nostroke_table"></div>

| **描述** | `array_negative_inner_product(array1, array2)` 的别名。 |
| **示例** | `array_negative_dot_product(l1, l2)` |
| **结果** | `-20.0` |