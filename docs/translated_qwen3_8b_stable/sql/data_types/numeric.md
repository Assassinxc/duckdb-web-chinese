blurb: 数值类型用于存储数字，且有不同的形状和大小。
layout: docu
redirect_from:
  - /docs/sql/data_types/numeric
title: 数值类型
---

## 整数类型

`TINYINT`、`SMALLINT`、`INTEGER`、`BIGINT` 和 `HUGEINT` 类型用于存储整数，即不带小数部分的数字，具有不同的范围。尝试存储超出允许范围的值会导致错误。
`UTINYINT`、`USMALLINT`、`UINTEGER`、`UBIGINT` 和 `UHUGEINT` 类型用于存储无符号整数。尝试存储负数或超出允许范围的值会导致错误。

<div class="center_aligned_header_table"></div>

| 名称        | 别名                          | 最小值 | 最大值 | 字节数 |
| :---------- | :------------------------------- | ------: | --------: | ------------: |
| `TINYINT`   | `INT1`                           |   - 2^7 |   2^7 - 1 |             1 |
| `SMALLINT`  | `INT2`, `INT16`, `SHORT`         |  - 2^15 |  2^15 - 1 |             2 |
| `INTEGER`   | `INT4`, `INT32`, `INT`, `SIGNED` |  - 2^31 |  2^31 - 1 |             4 |
| `BIGINT`    | `INT8`, `INT64`, `LONG`          |  - 2^63 |  2^63 - 1 |             8 |
| `HUGEINT`   | `INT128`                         | - 2^127 | 2^127 - 1 |            16 |
| `UTINYINT`  | `UINT8`                          |       0 |   2^8 - 1 |             1 |
| `USMALLINT` | `UINT16`                         |       0 |  2^16 - 1 |             2 |
| `UINTEGER`  | `UINT32`                         |       0 |  2^32 - 1 |             4 |
| `UBIGINT`   | `UINT64`                         |       0 |  2^64 - 1 |             8 |
| `UHUGEINT`  | `UINT128`                        |       0 | 2^128 - 1 |            16 |

整数类型是常见的选择，因为它在范围、存储大小和性能之间提供了最佳平衡。`SMALLINT` 类型通常仅在磁盘空间有限时使用。`BIGINT` 和 `HUGEINT` 类型设计用于在整数类型的范围不足时使用。

## 可变整数

前面提到的所有整数类型都有一个共同点，即最小和最大范围内的数字都具有相同的存储大小，`UTINYINT` 是 1 字节，`SMALLINT` 是 2 字节，等等。
但有时您需要的数字甚至比 `HUGEINT` 支持的还要大！对于这些情况，`VARINT` 类型会很有用，因为 `VARINT` 类型的限制要大得多（值可以由最多 1,262,612 位组成）。
`VARINT` 的最小存储大小为 4 字节，每个数字占用一个额外的位，四舍五入到 8 位（12 位四舍五入到 16 位，变成两个额外的字节）。

`VARINT` 类型支持正负值。

## 固定小数点

`DECIMAL(WIDTH, SCALE)` 数据类型（也称为 `NUMERIC(WIDTH, SCALE)`）表示精确的固定小数点值。创建 `DECIMAL` 类型值时，可以指定 `WIDTH` 和 `SCALE` 来定义字段中可以存储的十进制值的大小。`WIDTH` 字段决定可以存储的数字位数，`scale` 决定小数点后的数字位数。例如，`DECIMAL(3, 2)` 类型可以存储值 `1.23`，但不能存储值 `12.3` 或 `1.234`。如果未指定 `WIDTH` 和 `SCALE`，默认为 `DECIMAL(18, 3)`。

两个固定小数点值的加法、减法和乘法返回另一个具有所需 `WIDTH` 和 `SCALE` 的固定小数点值，以包含精确结果，或者如果所需 `WIDTH` 超出当前最大支持的 `WIDTH`（目前为 38），则抛出错误。

固定小数点值的除法通常不会产生有限小数扩展的数字。因此，DuckDB 对涉及固定小数点值的除法使用近似 [浮点运算](#floating-point-types)，并相应返回浮点数据类型。

在内部，十进制数根据其指定的 `WIDTH` 表示为整数。

| 宽度 | 内部表示 | 大小（字节） |
| :---- | :------- | -----------: |
| 1-4   | `INT16`  |            2 |
| 5-9   | `INT32`  |            4 |
| 10-18 | `INT64`  |            8 |
| 19-38 | `INT128` |           16 |

在不需要时使用过大的十进制数可能会影响性能。特别是宽度超过 19 的十进制数会很慢，因为涉及 `INT128` 类型的运算比涉及 `INT32` 或 `INT64` 类型的运算要昂贵得多。因此，建议使用宽度为 18 或以下的 `WIDTH`，除非有充分的理由认为这不足。

## 浮点类型

`FLOAT` 和 `DOUBLE` 数据类型是精度可变的数值类型。实际上，这些类型通常是 IEEE 标准 754 的二进制浮点算术实现（单精度和双精度），在底层处理器、操作系统和编译器支持的范围内。

| 名称     | 别名          | 描述                                      |
| :------- | :--------------- | :----------------------------------------------- |
| `FLOAT`  | `FLOAT4`, `REAL` | 单精度浮点数（4 字节） |
| `DOUBLE` | `FLOAT8`         | 双精度浮点数（8 字节） |

与固定小数点数据类型一样，从字面量或从其他数据类型转换到浮点类型时，无法精确表示的输入存储为近似值。但有时预测哪些输入受影响会更困难。例如，`1.3::DECIMAL(1, 0) - 0.7::DECIMAL(1, 0) != 0.6::DECIMAL(1, 0)` 不令人惊讶，但 `1.3::FLOAT - 0.7::FLOAT != 0.6::FLOAT` 可能令人惊讶。

此外，尽管固定小数点十进制数据类型的乘法、加法和减法是精确的，但这些操作在浮点二进制数据类型上仅是近似。

然而，对于更复杂的数学操作，内部使用浮点运算，如果中间步骤不转换为相同宽度的固定点格式，可以获得更精确的结果。例如，`(10::FLOAT / 3::FLOAT)::FLOAT * 3 = 10`，而 `(10::DECIMAL(18, 3) / 3::DECIMAL(18, 3))::DECIMAL(18, 3) * 3 = 9.999`。

总的来说，我们建议：

- 如果您需要存储具有已知小数位数的数字，并且需要精确的加法、减法和乘法（如用于货币金额），请使用 [`DECIMAL` 数据类型](#fixed-point-decimals) 或其 `NUMERIC` 别名。
- 如果您想进行快速或复杂的计算，浮点数据类型可能更合适。不过，如果您使用这些结果进行重要操作，应仔细评估实现中可能处理方式与预期不同的边缘情况（范围、无穷大、下溢、无效操作），并熟悉常见的浮点陷阱。文章 [“What Every Computer Scientist Should Know About Floating-Point Arithmetic” by David Goldberg](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html) 和 [Bruce Dawson 的浮点系列博客](https://randomascii.wordpress.com/2017/06/19/sometimes-floating-point-math-is-perfect/) 提供了很好的起点。

在大多数平台上，`FLOAT` 类型的范围至少为 1E-37 到 1E+37，精度至少为 6 位小数。`DOUBLE` 类型通常的范围约为 1E-307 到 1E+308，精度至少为 15 位。超出这些范围的正数（以及负数的镜像范围）可能在某些平台上导致错误，但通常会被转换为零或无穷大。

除了普通数值外，浮点类型还具有几个表示 IEEE 754 特殊值的特殊值：

- `Infinity`：无穷大
- `-Infinity`：负无穷大
- `NaN`：非数字

在具有所需 CPU/FPU 支持的机器上，DuckDB 遵循 IEEE 754 规范处理这些特殊值，有两个例外：

- `NaN` 与 `NaN` 相等且大于任何其他浮点数。
- 一些浮点函数（如 `sqrt` / `sin` / `asin`）在值超出其定义范围时会抛出错误，而不是返回 `NaN`。

要在 SQL 命令中插入这些值作为字面量，您必须将其用引号括起来，您可以缩写 `Infinity` 为 `Inf`，并且可以使用任何大小写。例如：

```sql
SELECT
    sqrt(2) > '-inf',
    'nan' > sqrt(2);
```

<div class="monospace_table"></div>

| `(sqrt(2) > '-inf')` | `('nan' > sqrt(2))` |
| -------------------: | ------------------: |
|                 true |                true |

## 全球唯一标识符（UUID）

DuckDB 通过 `UUID` 类型支持 [全球唯一标识符（UUIDs）](https://en.wikipedia.org/wiki/Universally_unique_identifier)。
这些标识符使用 128 位，内部表示为 `HUGEINT` 值。
打印时，它们以小写十六进制字符显示，由短横线分隔，格式如下：`⟨12345678⟩-⟨1234⟩-⟨1234⟩-⟨1234⟩-⟨1234567890ab⟩`{:.language-sql .highlight}（总共使用 36 个字符，包括短横线）。例如，`4ac7a9e9-607c-4c8a-84f3-843f0191e3fd` 是一个有效的 UUID。

DuckDB 支持生成 UUIDv4 和 [UUIDv7](https://uuid7.com/) 标识符。
要获取 UUID 值的版本，请使用 [`uuid_extract_version` 函数]({% link docs/stable/sql/functions/utility.md %}#uuid_extract_versionuuid)。

### UUIDv4

要生成 UUIDv4 值，使用 [`uuid()` 函数]({% link docs/stable/sql/functions/utility.md %}#uuid) 或其别名 [`uuidv4()`]({% link docs/stable/sql/functions/utility.md %}#uuidv4) 和 [`gen_random_uuid()`]({% link docs/stable/sql/functions/utility.md %}#gen_random_uuid) 函数。

### UUIDv7

要生成 UUIDv7 值，使用 [`uuidv7()`]({% link docs/stable/sql/functions/utility.md %}#uuidv7) 函数。
要从 UUIDv7 值中获取时间戳，使用 [`uuid_extract_timestamp` 函数]({% link docs/stable/sql/functions/utility.md %}#uuid_extract_timestampuuidv7):

```sql
SELECT uuid_extract_timestamp(uuidv7()) AS ts;
```

| ts                        |
| ------------------------- |
| 2025-04-19 15:51:20.07+00 |

## 函数

参见 [数值函数和运算符]({% link docs/stable/sql/functions/numeric.md %})。