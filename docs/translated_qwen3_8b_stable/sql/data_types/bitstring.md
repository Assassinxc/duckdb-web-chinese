---
---
blurb: bitstring 类型是 1 和 0 的字符串。
layout: docu
redirect_from:
- /docs/sql/data_types/bitstring
title: bitstring 类型
---

| 名称 | 别名 | 描述 |
|:---|:---|:---|
| `BITSTRING` | `BIT` | 可变长度的 1 和 0 字符串 |

bitstring 是由 1 和 0 组成的字符串。bit 类型的数据是可变长度的。bitstring 值每 8 位需要 1 个字节，再加上一些元数据存储的固定开销。

默认情况下，bitstring 不会用 0 填充。
bitstring 可以非常大，具有与 `BLOB` 相同的大小限制。

## 创建 bitstring

可以将表示 bitstring 的字符串转换为 `BITSTRING`：

```sql
SELECT '101010'::BITSTRING AS b;
```

<div class="monospace_table"></div>

|   b    |
|--------|
| 101010 |

可以使用 `bitstring` 函数创建具有预定义长度的 `BITSTRING`。生成的 bitstring 会以 0 左填充。

```sql
SELECT bitstring('0101011', 12) AS b;
```

|      b       |
|--------------|
| 000000101011 |

整数和浮点数也可以通过转换为 `BITSTRING`。例如：

```sql
SELECT 123::BITSTRING AS b;
```

<div class="monospace_table"></div>

|                b                 |
|----------------------------------|
| 00000000000000000000000001111011 |

## 函数

详见 [Bitstring 函数]({% link docs/stable/sql/functions/bitstring.md %})。