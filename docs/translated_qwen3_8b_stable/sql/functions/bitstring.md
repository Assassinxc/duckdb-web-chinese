---
---
layout: docu
redirect_from:
- /docs/test/functions/bitstring
- /docs/test/functions/bitstring/
- /docs/sql/functions/bitstring
title: 位字符串函数
---

<!-- markdownlint-disable MD001 -->

本节描述了用于检查和操作 [`BITSTRING`]({% link docs/stable/sql/data_types/bitstring.md %}) 值的函数和运算符。
执行按位运算符 AND、OR 和 XOR 时，位字符串必须长度相等。进行位移位操作时，字符串的原始长度将被保留。

## 位字符串运算符

下表显示了 `BIT` 类型可用的数学运算符。

<!-- markdownlint-disable MD056 -->

| 运算符 | 描述 | 示例 | 结果 |
|:---|:---|:---|---:|
| `&` | 按位与 | `'10101'::BITSTRING & '10001'::BITSTRING` | `10001` |
| `|` | 按位或 | `'1011'::BITSTRING | '0001'::BITSTRING` | `1011` |
| `xor` | 按位异或 | `xor('101'::BITSTRING, '001'::BITSTRING)` | `100` |
| `~` | 按位非 | `~('101'::BITSTRING)` | `010` |
| `<<` | 按位左移 | `'1001011'::BITSTRING << 3` | `1011000` |
| `>>` | 按位右移 | `'1001011'::BITSTRING >> 3` | `0001001` |

<!-- markdownlint-enable MD056 -->

## 位字符串函数

下表显示了 `BIT` 类型可用的标量函数。

| 名称 | 描述 |
|:--|:-------|
| [`bit_count(bitstring)`](#bit_countbitstring) | 返回位字符串中设置的位数。 |
| [`bit_length(bitstring)`](#bit_lengthbitstring) | 返回位字符串中的位数。 |
| [`bit_position(substring, bitstring)`](#bit_positionsubstring-bitstring) | 返回指定子字符串在位字符串中的第一个起始索引，如果不存在则返回零。第一个（最左边）位的索引为 1。 |
| [`bitstring(bitstring, length)`](#bitstringbitstring-length) | 返回指定长度的位字符串。 |
| [`get_bit(bitstring, index)`](#get_bitbitstring-index) | 从位字符串中提取第 n 位；第一个（最左边）位的索引为 0。 |
| [`length(bitstring)`](#lengthbitstring) | `bit_length` 的别名。 |
| [`octet_length(bitstring)`](#octet_lengthbitstring) | 返回位字符串中的字节数。 |
| [`set_bit(bitstring, index, new_value)`](#set_bitbitstring-index-new_value) | 将位字符串中的第 n 位设置为 newvalue；第一个（最左边）位的索引为 0。返回一个新的位字符串。 |

#### `bit_count(bitstring)`

<div class="nostroke_table"></div>

| **描述** | 返回位字符串中设置的位数。 |
| **示例** | `bit_count('1101011'::BITSTRING)` |
| **结果** | `5` |

#### `bit_length(bitstring)`

<div class="nostroke_table"></div>

| **描述** | 返回位字符串中的位数。 |
| **示例** | `bit_length('1101011'::BITSTRING)` |
| **结果** | `7` |

#### `bit_position(substring, bitstring)`

<div class="nostroke_table"></div>

| **描述** | 返回指定子字符串在位字符串中的第一个起始索引，如果不存在则返回零。第一个（最左边）位的索引为 1 |
| **示例** | `bit_position('010'::BITSTRING, '1110101'::BITSTRING)` |
| **结果** | `4` |

#### `bitstring(bitstring, length)`

<div class="nostroke_table"></div>

| **描述** | 返回指定长度的位字符串。 |
| **示例** | `bitstring('1010'::BITSTRING, 7)` |
| **结果** | `0001010` |

#### `get_bit(bitstring, index)`

<div class="nostroke_table"></div>

| **描述** | 从位字符串中提取第 n 位；第一个（最左边）位的索引为 0。 |
| **示例** | `get_bit('0110010'::BITSTRING, 2)` |
| **结果** | `1` |

#### `length(bitstring)`

<div class="nostroke_table"></div>

| **描述** | `bit_length` 的别名。 |
| **示例** | `length('1101011'::BITSTRING)` |
| **结果** | `7` |

#### `octet_length(bitstring)`

<div class="nostroke_table"></div>

| **描述** | 返回位字符串中的字节数。 |
| **示例** | `octet_length('1101011'::BITSTRING)` |
| **结果** | `1` |

#### `set_bit(bitstring, index, new_value)`

<div class="nostroke_table"></div>

| **描述** | 将位字符串中的第 n 位设置为 newvalue；第一个（最左边）位的索引为 0。返回一个新的位字符串。 |
| **示例** | `set_bit('0110010'::BITSTRING, 2, 0)` |
| **结果** | `0100010` |

## 位字符串聚合函数

这些聚合函数适用于 `BIT` 类型。

| 名称 | 描述 |
|:--|:-------|
| [`bit_and(arg)`](#bit_andarg) | 返回给定表达式中所有位字符串的按位与操作结果。 |
| [`bit_or(arg)`](#bit_orarg) | 返回给定表达式中所有位字符串的按位或操作结果。 |
| [`bit_xor(arg)`](#bit_xorarg) | 返回给定表达式中所有位字符串的按位异或操作结果。 |
| [`bitstring_agg(arg)`](#bitstring_aggarg) | 返回一个位字符串，其中每个在 `arg` 中定义的唯一位置的位都被设置。 |
| [`bitstring_agg(arg, min, max)`](#bitstring_aggarg-min-max) | 返回一个位字符串，其中每个在 `arg` 中定义的唯一位置的位都被设置。所有位置必须在 [`min`, `max`] 范围内，否则会抛出 `Out of Range Error` 错误。 |

#### `bit_and(arg)`

<div class="nostroke_table"></div>

| **描述** | 返回给定表达式中所有位字符串的按位与操作结果。 |
| **示例** | `bit_and(A)` |

#### `bit_or(arg)`

<div class="nostroke_table"></div>

| **描述** | 返回给定表达式中所有位字符串的按位或操作结果。 |
| **示例** | `bit_or(A)` |

#### `bit_xor(arg)`

<div class="nostroke_table"></div>

| **描述** | 返回给定表达式中所有位字符串的按位异或操作结果。 |
| **示例** | `bit_xor(A)` |

#### `bitstring_agg(arg)`

<div class="nostroke_table"></div>

| **描述** | `bitstring_agg` 函数接受任何整数类型作为输入，并返回一个位字符串，其中每个唯一值的位都被设置。最左边的位代表列中的最小值，最右边的位代表最大值。如果可能，最小值和最大值将从列统计信息中获取。否则，也可以提供最小值和最大值。 |
| **示例** | `bitstring_agg(A)` |

> 提示 `bit_count` 和 `bitstring_agg` 的组合可以作为 `count(DISTINCT ...)` 的替代方法，在低基数和密集值的情况下可能带来性能提升。

#### `bitstring_agg(arg, min, max)`

<div class="nostroke_table"></div>

| **描述** | 返回一个位字符串，其中每个在 `arg` 中定义的唯一位置的位都被设置。所有位置必须在 [`min`, `max`] 范围内，否则会抛出 `Out of Range Error` 错误。 |
| **示例** | `bitstring_agg(A, 1, 42)` |