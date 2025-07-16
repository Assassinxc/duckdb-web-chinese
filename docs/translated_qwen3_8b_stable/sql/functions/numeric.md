---
---
layout: docu
redirect_from:
- /docs/test/functions/math
- /docs/test/functions/math/
- /docs/sql/functions/numeric
title: 数值函数
---

<!-- markdownlint-disable MD001 -->

## 数值运算符

下表显示了[数值类型]({% link docs/stable/sql/data_types/numeric.md %})可用的数学运算符。

<!-- markdownlint-disable MD056 -->

| 运算符 | 描述 | 示例 | 结果 |
|-|-----|--|-|
| `+`      | 加法                  | `2 + 3`   | `5`   |
| `-`      | 减法               | `2 - 3`   | `-1`  |
| `*`      | 乘法            | `2 * 3`   | `6`   |
| `/`      | 浮点除法            | `5 / 2`   | `2.5` |
| `//`     | 除法                  | `5 // 2`  | `2`   |
| `%`      | 取模（余数）        | `5 % 4`   | `1`   |
| `**`     | 幂运算                  | `3 ** 4`  | `81`  |
| `^`      | 幂运算（`**` 的别名） | `3 ^ 4`   | `81`  |
| `&`      | 按位与               | `91 & 15` | `11`  |
| `|`      | 按位或                | `32 | 3`  | `35`  |
| `<<`     | 按位左移        | `1 << 4`  | `16`  |
| `>>`     | 按位右移       | `8 >> 2`  | `2`   |
| `~`      | 按位取反          | `~15`     | `-16` |
| `!`      | `x` 的阶乘          | `4!`      | `24`  |

<!-- markdownlint-enable MD056 -->

### 除法和取模运算符

有两个除法运算符：`/` 和 `//`。
当至少有一个操作数是 `FLOAT` 或 `DOUBLE` 时，它们是等价的。
当两个操作数都是整数时，`/` 执行浮点除法（`5 / 2 = 2.5`），而 `//` 执行整数除法（`5 // 2 = 2`）。

### 支持的类型

取模、位运算和取反和阶乘运算符仅适用于整数类型数据，
而其他运算符适用于所有数值类型数据。

## 数值函数

下表显示了可用的数学函数。

| 名称 | 描述 |
|:--|:-------|
| [`@(x)`](#x) | 绝对值。如果 `x` 是列名，则括号是可选的。 |
| [`abs(x)`](#absx) | 绝对值。 |
| [`acos(x)`](#acosx) | 计算 `x` 的反余弦。 |
| [`acosh(x)`](#acoshx) | 计算 `x` 的反双曲余弦。 |
| [`add(x, y)`](#addx-y) | `x + y` 的别名。 |
| [`asin(x)`](#asinx) | 计算 `x` 的反正弦。 |
| [`asinh(x)`](#asinhx) | 计算 `x` 的反双曲正弦。 |
| [`atan(x)`](#atanx) | 计算 `x` 的反正切。 |
| [`atanh(x)`](#atanhx) | 计算 `x` 的反双曲正切。 |
| [`atan2(y, x)`](#atan2y-x) | 计算 `(y, x)` 的反正切。 |
| [`bit_count(x)`](#bit_countx) | 返回设置的位数。 |
| [`cbrt(x)`](#cbrtx) | 返回数字的立方根。 |
| [`ceil(x)`](#ceilx) | 向上取整。 |
| [`ceiling(x)`](#ceilingx) | 向上取整。`ceil` 的别名。 |
| [`cos(x)`](#cosx) | 计算 `x` 的余弦。 |
| [`cot(x)`](#cotx) | 计算 `x` 的余切。 |
| [`degrees(x)`](#degreesx) | 将弧度转换为度数。 |
| [`divide(x, y)`](#dividex-y) | `x // y` 的别名。 |
| [`even(x)`](#evenx) | 向零的方向舍入到下一个偶数。 |
| [`exp(x)`](#expx) | 计算 `e ** x`。 |
| [`factorial(x)`](#factorialx) | 参见 `!` 运算符。计算当前整数及其以下所有整数的乘积。 |
| [`fdiv(x, y)`](#fdivx-y) | 执行整数除法（`x // y`），但返回 `DOUBLE` 值。 |
| [`floor(x)`](#floorx) | 向下取整。 |
| [`fmod(x, y)`](#fmodx-y) | 计算取模值。始终返回 `DOUBLE` 值。 |
| [`gamma(x)`](#gammax) | 计算 `x - 1` 的阶乘的插值。允许小数输入。 |
| [`gcd(x, y)`](#gcdx-y) | 计算 `x` 和 `y` 的最大公约数。 |
| [`greatest_common_divisor(x, y)`](#greatest_common_divisorx-y) | 计算 `x` 和 `y` 的最大公约数。 |
| [`greatest(x1, x2, ...)`](#greatestx1-x2-) | 选择最大值。 |
| [`isfinite(x)`](#isfinitex) | 如果浮点值是有限的，返回 true，否则返回 false。 |
| [`isinf(x)`](#isinfx) | 如果浮点值是无穷大，返回 true，否则返回 false。 |
| [`isnan(x)`](#isnanx) | 如果浮点值不是数字，返回 true，否则返回 false。 |
| [`lcm(x, y)`](#lcmx-y) | 计算 `x` 和 `y` 的最小公倍数。 |
| [`least_common_multiple(x, y)`](#least_common_multiplex-y) | 计算 `x` 和 `y` 的最小公倍数。 |
| [`least(x1, x2, ...)`](#leastx1-x2-) | 选择最小值。 |
| [`lgamma(x)`](#lgammax) | 计算 `gamma` 函数的对数。 |
| [`ln(x)`](#lnx) | 计算 `x` 的自然对数。 |
| [`log(x)`](#logx) | 计算 `x` 的以 10 为底的对数。 |
| [`log10(x)`](#log10x) | `log` 的别名。计算 `x` 的以 10 为底的对数。 |
| [`log2(x)`](#log2x) | 计算 `x` 的以 2 为底的对数。 |
| [`multiply(x, y)`](#multiplyx-y) | `x * y` 的别名。 |
| [`nextafter(x, y)`](#nextafterx-y) | 返回 `x` 在 `y` 方向上的下一个浮点值。 |
| [`pi()`](#pi) | 返回 π 的值。 |
| [`pow(x, y)`](#powx-y) | 计算 `x` 的 `y` 次方。 |
| [`power(x, y)`](#powerx-y) | `pow` 的别名。计算 `x` 的 `y` 次方。 |
| [`radians(x)`](#radiansx) | 将度数转换为弧度。 |
| [`random()`](#random) | 返回范围在 `0.0 <= x < 1.0` 的随机数 `x`。 |
| [`round_even(v NUMERIC, s INTEGER)`](#round_evenv-numeric-s-integer) | `roundbankers(v, s)` 的别名。使用 [_rounding half to even_ 规则](https://en.wikipedia.org/wiki/Rounding#Rounding_half_to_even) 将数值四舍五入到 `s` 位小数。允许 `s < 0`。 |
| [`round(v NUMERIC, s INTEGER)`](#roundv-numeric-s-integer) | 将数值四舍五入到 `s` 位小数。允许 `s < 0`。 |
| [`setseed(x)`](#setseedx) | 设置随机函数使用的种子。 |
| [`sign(x)`](#signx) | 返回 `x` 的符号（-1、0 或 1）。 |
| [`signbit(x)`](#signbitx) | 返回符号位是否设置。 |
| [`sin(x)`](#sinx) | 计算 `x` 的正弦。 |
| [`sqrt(x)`](#sqrtx) | 返回数字的平方根。 |
| [`subtract(x, y)`](#subtractx-y) | `x - y` 的别名。 |
| [`tan(x)`](#tanx) | 计算 `x` 的正切。 |
| [`trunc(x)`](#truncx) | 截断数字。 |
| [`xor(x, y)`](#xorx-y) | 按位异或。 |

#### `@(x)`

<div class="nostroke_table"></div>

| **描述** | 绝对值。如果 `x` 是列名，则括号是可选的。 |
| **示例** | `@(-17.4)` |
| **结果** | `17.4` |
| **别名** | `abs` |

#### `abs(x)`

<div class="nostroke_table"></div>

| **描述** | 绝对值。 |
| **示例** | `abs(-17.4)` |
| **结果** | `17.4` |
| **别名** | `@` |

#### `acos(x)`

<div class="nostroke_table"></div>

| **描述** | 计算 `x` 的反余弦。 |
| **示例** | `acos(0.5)` |
| **结果** | `1.0471975511965976` |

#### `acosh(x)`

<div class="nostroke_table"></div>

| **描述** | 计算 `x` 的反双曲余弦。 |
| **示例** | `acosh(1.5)` |
| **结果** | `0.9624236501192069` |

#### `add(x, y)`

<div class="nostroke_table"></div>

| **描述** | `x + y` 的别名。 |
| **示例** | `add(2, 3)` |
| **结果** | `5` |

#### `asin(x)`

<div class="nostroke_table"></div>

| **描述** | 计算 `x` 的反正弦。 |
| **示例** | `asin(0.5)` |
| **结果** | `0.5235987755982989` |

#### `asinh(x)`

<div class="nostroke_table"></div>

| **描述** | 计算 `x` 的反双曲正弦。 |
| **示例** | `asinh(0.5)` |
| **结果** | `0.48121182505960347` |

#### `atan(x)`

<div class="nostroke_table"></div>

| **描述** | 计算 `x` 的反正切。 |
| **示例** | `atan(0.5)` |
| **结果** | `0.4636476090008061` |

#### `atanh(x)`

<div class="nostroke_table"></div>

| **描述** | 计算 `x` 的反双曲正切。 |
| **示例** | `atanh(0.5)` |
| **结果** | `0.5493061443340549` |

#### `atan2(y, x)`

<div class="nostroke_table"></div>

| **描述** | 计算 `(y, x)` 的反正切。 |
| **示例** | `atan2(0.5, 0.5)` |
| **结果** | `0.7853981633974483` |

#### `bit_count(x)`

<div class="nostroke_table"></div>

| **描述** | 返回设置的位数。 |
| **示例** | `bit_count(31)` |
| **结果** | `5` |

#### `cbrt(x)`

<div class="nostroke_table"></div>

| **描述** | 返回数字的立方根。 |
| **示例** | `cbrt(8)` |
| **结果** | `2` |

#### `ceil(x)`

<div class="nostroke_table"></div>

| **描述** | 向上取整。 |
| **示例** | `ceil(17.4)` |
| **结果** | `18` |

#### `ceiling(x)`

<div class="nostroke_table"></div>

| **描述** | 向上取整。`ceil` 的别名。 |
| **示例** | `ceiling(17.4)` |
| **结果** | `18` |

#### `cos(x)`

<div class="nostroke_table"></div>

| **描述** | 计算 `x` 的余弦。 |
| **示例** | `cos(90)` |
| **结果** | `-0.4480736161291701` |

#### `cot(x)`

<div class="nostroke_table"></div>

| **描述** | 计算 `x` 的余切。 |
| **示例** | `cot(0.5)` |
| **结果** | `1.830487721712452` |

#### `degrees(x)`

<div class="nostroke_table"></div>

| **描述** | 将弧度转换为度数。 |
| **示例** | `degrees(pi())` |
| **结果** | `180` |

#### `divide(x, y)`

<div class="nostroke_table"></div>

| **描述** | `x // y` 的别名。 |
| **示例** | `divide(5, 2)` |
| **结果** | `2` |

#### `even(x)`

<div class="nostroke_table"></div>

| **描述** | 向零的方向舍入到下一个偶数。 |
| **示例** | `even(2.9)` |
| **结果** | `4` |

#### `exp(x)`

<div class="nostroke_table"></div>

| **描述** | 计算 `e ** x`。 |
| **示例** | `exp(0.693)` |
| **结果** | `2` |

#### `factorial(x)`

<div class="nostroke_table"></div>

| **描述** | 参见 `!` 运算符。计算当前整数及其以下所有整数的乘积。 |
| **示例** | `factorial(4)` |
| **结果** | `24` |

#### `fdiv(x, y)`

<div class="nostroke_table"></div>

| **描述** | 执行整数除法（`x // y`），但返回 `DOUBLE` 值。 |
| **示例** | `fdiv(5, 2)` |
| **结果** | `2.0` |

#### `floor(x)`

<div class="nostroke_table"></div>

| **描述** | 向下取整。 |
| **示例** | `floor(17.4)` |
| **结果** | `17` |

#### `fmod(x, y)`

<div class="nostroke_table"></div>

| **描述** | 计算取模值。始终返回 `DOUBLE` 值。 |
| **示例** | `fmod(5, 2)` |
| **结果** | `1.0` |

#### `gamma(x)`

<div class="nostroke_table"></div>

| **描述** | 计算 `x - 1` 的阶乘的插值。允许小数输入。 |
| **示例** | `gamma(5.5)` |
| **结果** | `52.34277778455352` |

#### `gcd(x, y)`

<div class="nostroke_table"></div>

| **描述** | 计算 `x` 和 `y` 的最大公约数。 |
| **示例** | `gcd(42, 57)` |
| **结果** | `3` |

#### `greatest_common_divisor(x, y)`

<div class="nostroke_table"></div>

| **描述** | 计算 `x` 和 `y` 的最大公约数。 |
| **示例** | `greatest_common_divisor(42, 57)` |
| **结果** | `3` |

#### `greatest(x1, x2, ...)`

<div class="nostroke_table"></div>

| **描述** | 选择最大值。 |
| **示例** | `greatest(3, 2, 4, 4)` |
| **结果** | `4` |

#### `isfinite(x)`

<div class="nostroke_table"></div>

| **描述** | 如果浮点值是有限的，返回 true，否则返回 false。 |
| **示例** | `isfinite(5.5)` |
| **结果** | `true` |

#### `isinf(x)`

<div class="nostroke_table"></div>

| **描述** | 如果浮点值是无穷大，返回 true，否则返回 false。 |
| **示例** | `isinf('Infinity'::float)` |
| **结果** | `true` |

#### `isnan(x)`

<div class="nostroke_table"></div>

| **描述** | 如果浮点值不是数字，返回 true，否则返回 false。 |
| **示例** | `isnan('NaN'::float)` |
| **结果** | `true` |

#### `lcm(x, y)`

<div class="nostroke_table"></div>

| **描述** | 计算 `x` 和 `y` 的最小公倍数。 |
| **示例** | `lcm(42, 57)` |
| **结果** | `798` |

#### `least_common_multiple(x, y)`

<div class="nostroke_table"></div>

| **描述** | 计算 `x` 和 `y` 的最小公倍数。 |
| **示例** | `least_common_multiple(42, 57)` |
| **结果** | `798` |

#### `least(x1, x2, ...)`

<div class="nostroke_table"></div>

| **描述** | 选择最小值。 |
| **示例** | `least(3, 2, 4, 4)` |
| **结果** | `2` |

#### `lgamma(x)`

<div class="nostroke_table"></div>

| **描述** | 计算 `gamma` 函数的对数。 |
| **示例** | `lgamma(2)` |
| **结果** | `0` |

#### `ln(x)`

<div class="nostroke_table"></div>

| **描述** | 计算 `x` 的自然对数。 |
| **示例** | `ln(2)` |
| **结果** | `0.693` |

#### `log(x)`

<div class="nostroke_table"></div>

| **描述** | 计算 `x` 的以 10 为底的对数。 |
| **示例** | `log(100)` |
| **结果** | `2` |

#### `log10(x)`

<div class="nostroke_table"></div>

| **描述** | `log` 的别名。计算 `x` 的以 10 为底的对数。 |
| **示例** | `log10(1000)` |
| **结果** | `3` |

#### `log2(x)`

<div class="nostroke_table"></div>

| **描述** | 计算 `x` 的以 2 为底的对数。 |
| **示例** | `log2(8)` |
| **结果** | `3` |

#### `multiply(x, y)`

<div class="nostroke_table"></div>

| **描述** | `x * y` 的别名。 |
| **示例** | `multiply(2, 3)` |
| **结果** | `6` |

#### `nextafter(x, y)`

<div class="nostroke_table"></div>

| **描述** | 返回 `x` 在 `y` 方向上的下一个浮点值。 |
| **示例** | `nextafter(1::float, 2::float)` |
| **结果** | `1.0000001` |

#### `pi()`

<div class="nostroke_table"></div>

| **描述** | 返回 π 的值。 |
| **示例** | `pi()` |
| **结果** | `3.141592653589793` |

#### `pow(x, y)`

<div class="nostroke_table"></div>

| **描述** | 计算 `x` 的 `y` 次方。 |
| **示例** | `pow(2, 3)` |
| **结果** | `8` |

#### `power(x, y)`

<div class="nostroke_table"></div>

| **描述** | `pow` 的别名。计算 `x` 的 `y` 次方。 |
| **示例** | `power(2, 3)` |
| **结果** | `8` |

#### `radians(x)`

<div class="nostroke_table"></div>

| **描述** | 将度数转换为弧度。 |
| **示例** | `radians(90)` |
| **结果** | `1.5707963267948966` |

#### `random()`

<div class="nostroke_table"></div>

| **描述** | 返回范围在 `0.0 <= x < 1.0` 的随机数 `x`。 |
| **示例** | `random()` |
| **结果** | 各种 |

#### `round_even(v NUMERIC, s INTEGER)`

<div class="nostroke_table"></div>

| **描述** | `roundbankers(v, s)` 的别名。使用 [_rounding half to even_ 规则](https://en.wikipedia.org/wiki/Rounding#Rounding_half_to_even) 将数值四舍五入到 `s` 位小数。允许 `s < 0`。 |
| **示例** | `round_even(24.5, 0)` |
| **结果** | `24.0` |

#### `round(v NUMERIC, s INTEGER)`

<div class="nostroke_table"></div>

| **描述** | 将数值四舍五入到 `s` 位小数。允许 `s < 0`。 |
| **示例** | `round(42.4332, 2)` |
| **结果** | `42.43` |

#### `setseed(x)`

<div class="nostroke_table"></div>

| **描述** | 设置随机函数使用的种子。 |
| **示例** | `setseed(0.42)` |

#### `sign(x)`

<div class="nostroke_table"></div>

| **描述** | 返回 `x` 的符号（-1、0 或 1）。 |
| **示例** | `sign(-349)` |
| **结果** | `-1` |

#### `signbit(x)`

<div class="nostroke_table"></div>

| **描述** | 返回符号位是否设置。 |
| **示例** | `signbit(-1.0)` |
| **结果** | `true` |

#### `sin(x)`

<div class="nostroke_table"></div>

| **描述** | 计算 `x` 的正弦。 |
| **示例** | `sin(90)` |
| **结果** | `0.8939966636005579` |

#### `sqrt(x)`

<div class="nostroke_table"></div>

| **描述** | 返回数字的平方根。 |
| **示例** | `sqrt(9)` |
| **结果** | `3` |

#### `subtract(x, y)`

<div class="nostroke_table"></div>

| **描述** | `x - y` 的别名。 |
| **示例** | `subtract(2, 3)` |
| **结果** | `-1` |

#### `tan(x)`

<div class="nostroke_table"></div>

| **描述** | 计算 `x` 的正切。 |
| **示例** | `tan(90)` |
| **结果** | `-1.995200412208242` |

#### `trunc(x)`

<div class="nostroke_table"></div>

| **描述** | 截断数字。 |
| **示例** | `trunc(17.4)` |
| **结果** | `17` |

#### `xor(x, y)`

<div class="nostroke_table"></div>

| **描述** | 按位异或。 |
| **示例** | `xor(17, 5)` |
| **结果** | `20` |