---
---
layout: docu
redirect_from:
- /docs/sql/data_types/literal_types
title: 字面量类型
---

DuckDB 有专门的字面量类型用于表示查询中的 `NULL`、整数和字符串字面量。这些类型有自己的绑定和转换规则。

> 在 DuckDB 0.10.0 版本之前，整数和字符串字面量的行为与 `INTEGER` 和 `VARCHAR` 类型相同。

## NULL 字面量

`NULL` 字面量使用关键字 `NULL` 表示。`NULL` 字面量可以隐式转换为任何其他类型。

## 整数字面量

整数字面量表示为一个或多个数字的序列。在运行时，这些结果为 `INTEGER_LITERAL` 类型。`INTEGER_LITERAL` 类型可以隐式转换为任何 [整数类型]({% link docs/stable/sql/data_types/numeric.md %}#integer-types)，只要值在该类型范围内。例如，整数字面量 `42` 可以隐式转换为 `TINYINT`，但整数字面量 `1000` 不能。

## 其他数值字面量

非整数的数值字面量可以用十进制表示法表示，使用句点字符 (`.` ) 分隔数字的整数部分和小数部分。
整数部分或小数部分可以省略：

```sql
SELECT 1.5;          -- 1.5
SELECT .50;          -- 0.5
SELECT 2.;           -- 2.0
```

非整数的数值字面量也可以使用 [_E 表示法_](https://en.wikipedia.org/wiki/Scientific_notation#E_notation) 表示。在 E 表示法中，一个整数或小数字面量后跟一个指数部分，指数部分由 `e` 或 `E` 表示，后接一个表示指数的字面量整数。指数部分表示前面的值应该乘以 10 的指数次方：

```sql
SELECT 1e2;           -- 100
SELECT 6.02214e23;    -- 阿伏伽德罗常数
SELECT 1e-10;         -- 1 ångström
```

## 数值字面量中的下划线

DuckDB 的 SQL 方言允许在数值字面量中使用下划线字符 `_` 作为可选分隔符。使用下划线的规则如下：

* 下划线可以在整数、十进制、十六进制和二进制表示法中使用。
* 下划线不能是字面量的第一个或最后一个字符。
* 下划线必须在两侧有整数/数值部分，即不能有多个连续的下划线，也不能紧接在小数点或指数前/后。

示例：

```sql
SELECT 100_000_000;          -- 100000000
SELECT '0xFF_FF'::INTEGER;   -- 65535
SELECT 1_2.1_2E0_1;          -- 121.2
SELECT '0b0_1_0_1'::INTEGER; -- 5
```

## 字符串字面量

字符串字面量使用单引号 (`'`, 引号) 进行界定，结果为 `STRING_LITERAL` 值。
请注意，双引号 (`"`) 不能用作字符串分隔符：相反，双引号用于界定 [带引号的标识符]({% link docs/stable/sql/dialect/keywords_and_identifiers.md %}#identifiers)。

### 隐式字符串字面量连接

仅由空白分隔的连续单引号字符串字面量（至少包含一个换行符）会被隐式连接：

```sql
SELECT 'Hello'
    ' '
    'World' AS greeting;
```

等价于：

```sql
SELECT 'Hello'
    || ' '
    || 'World' AS greeting;
```

它们都返回以下结果：

|  greeting   |
|-------------|
| Hello World |

请注意，隐式连接仅在字面量之间有至少一个换行符时才有效。使用没有换行符的相邻字符串字面量分隔符会导致语法错误：

```sql
SELECT 'Hello' ' ' 'World' AS greeting;
```

```console
解析错误：
在或附近出现语法错误 "' '"

LINE 1: SELECT 'Hello' ' ' 'World' AS greeting;
                       ^
```

另外请注意，隐式连接仅适用于单引号字符串字面量，不适用于其他类型的字符串值。

### 隐式字符串转换

`STRING_LITERAL` 实例可以隐式转换为 _任何_ 其他类型。

例如，我们可以将字符串字面量与日期进行比较：

```sql
SELECT d > '1992-01-01' AS result
FROM (VALUES (DATE '1992-01-01')) t(d);
```

| result |
|:-------|
| false  |

然而，我们无法将 `VARCHAR` 值与日期进行比较。

```sql
SELECT d > '1992-01-01'::VARCHAR
FROM (VALUES (DATE '1992-01-01')) t(d);
```

```console
绑定错误：
无法比较 DATE 类型和 VARCHAR 类型的值 - 需要显式转换
```

### 转义字符串字面量

要转义字符串字面量中的单引号（撇号）字符，使用 `''`。例如，`SELECT '''' AS s` 返回 `'`。

要启用一些常见的转义序列，如 `\n` 表示换行符，可以在字符串字面量前加上 `e`（或 `E`）。

```sql
SELECT e'Hello\nworld' AS msg;
```

<!-- 此输出故意使用 duckbox 格式化器 -->

```text
┌──────────────┐
│     msg      │
│   varchar    │
├──────────────┤
│ Hello\nworld │
└──────────────┘
```

支持的反斜杠转义序列如下：

| 转义序列 | 名称 | ASCII 码 |
|:--|:--|--:|
| `\b` | 退格 | 8 |
| `\f` | 换页 | 12 |
| `\n` | 换行 | 10 |
| `\r` | 回车 | 13 |
| `\t` | 制表 | 9 |

### 美元报价字符串字面量

DuckDB 支持美元报价字符串字面量，由双美元符号 (`$$`) 包围：

```sql
SELECT $$Hello
world$$ AS msg;
```

<!-- 此输出故意使用 duckbox 格式化器 -->

```text
┌──────────────┐
│     msg      │
│   varchar    │
├──────────────┤
│ Hello\nworld │
└──────────────┘
```

```sql
SELECT $$The price is $9.95$$ AS msg;
```

|        msg         |
|--------------------|
| The price is $9.95 |

甚至可以插入字母数字标签在双美元符号中，以允许在字符串字面量中使用常规的双美元符号：

```sql
SELECT $tag$ this string can contain newlines,
'single quotes',
"double quotes",
and $$dollar quotes$$ $tag$ AS msg;
```

<!-- 此输出故意使用 duckbox 格式化器 -->

```text
┌────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                              msg                                               │
│                                            varchar                                             │
├────────────────────────────────────────────────────────────────────────────────────────────────┤
│  this string can contain newlines,\n'single quotes',\n"double quotes",\nand $$dollar quotes$$  │
└────────────────────────────────────────────────────────────────────────────────────────────────┘
```

[隐式连接](#implicit-string-literal-concatenation) 仅适用于单引号字符串字面量，不适用于美元报价字符串字面量。