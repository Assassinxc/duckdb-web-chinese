---
---
layout: docu
redirect_from:
- /docs/test/functions/enum
- /docs/test/functions/enum/
- /docs/sql/functions/enum
title: 枚举函数
---

<!-- markdownlint-disable MD001 -->

本节描述了用于检查和操作 [`ENUM` 值]({% link docs/stable/sql/data_types/enum.md %}) 的函数和运算符。
示例假设创建了一个枚举类型，如下所示：

```sql
CREATE TYPE mood AS ENUM ('sad', 'ok', 'happy', 'anxious');
```

这些函数可以接受 `NULL` 或该类型的特定值作为参数。
除 `enum_range_boundary` 外，结果仅取决于参数的类型，而与其值无关。

| 名称 | 描述 |
|:--|:-------|
| [`enum_code(enum_value)`](#enum_codeenum_value) | 返回给定枚举值的 numeric 值。 |
| [`enum_first(enum)`](#enum_firstenum) | 返回输入枚举类型的第一个值。 |
| [`enum_last(enum)`](#enum_lastenum) | 返回输入枚举类型的最后一个值。 |
| [`enum_range(enum)`](#enum_rangeenum) | 返回输入枚举类型的全部值作为数组。 |
| [`enum_range_boundary(enum, enum)`](#enum_range_boundaryenum-enum) | 返回两个给定枚举值之间的范围作为数组。 |

#### `enum_code(enum_value)`

<div class="nostroke_table"></div>

| **描述** | 返回给定枚举值的 numeric 值。 |
| **示例** | `enum_code('happy'::mood)` |
| **结果** | `2` |

#### `enum_first(enum)`

<div class="nostroke_table"></div>

| **描述** | 返回输入枚举类型的第一个值。 |
| **示例** | `enum_first(NULL::mood)` |
| **结果** | `sad` |

#### `enum_last(enum)`

<div class="nostroke_table"></div>

| **描述** | 返回输入枚举类型的最后一个值。 |
| **示例** | `enum_last(NULL::mood)` |
| **结果** | `anxious` |

#### `enum_range(enum)`

<div class="nostroke_table"></div>

| **描述** | 返回输入枚举类型的全部值作为数组。 |
| **示例** | `enum_range(NULL::mood)` |
| **结果** | `[sad, ok, happy, anxious]` |

#### `enum_range_boundary(enum, enum)`

<div class="nostroke_table"></div>

| **描述** | 返回两个给定枚举值之间的范围作为数组。这两个值必须是相同枚举类型。如果第一个参数为 `NULL`，则结果从枚举类型的第一个值开始。如果第二个参数为 `NULL`，则结果以枚举类型的最后一个值结束。 |
| **示例** | `enum_range_boundary(NULL, 'happy'::mood)` |
| **结果** | `[sad, ok, happy]` |