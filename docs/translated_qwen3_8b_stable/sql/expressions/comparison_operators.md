---
---
layout: docu
railroad: expressions/comparison.js
redirect_from:
- /docs/sql/expressions/comparison_operators
title: 比较
---

## 比较运算符

<div id="rrdiagram2"></div>

下表展示了标准的比较运算符。
当任意一个输入参数为 `NULL` 时，比较的结果为 `NULL`。

| 运算符 | 描述 | 示例 | 结果 |
|:---|:---|:---|:---|
| `<` | 小于 | `2 < 3` | `true` |
| `>` | 大于 | `2 > 3` | `false` |
| `<=` | 小于等于 | `2 <= 3` | `true` |
| `>=` | 大于等于 | `4 >= NULL` | `NULL` |
| `=` 或 `==` | 等于 | `NULL = NULL` | `NULL` |
| `<>` 或 `!=` | 不等于 | `2 <> 2` | `false` |

下表展示了标准的区别运算符。
这些运算符将 `NULL` 值视为相等。

| 运算符 | 描述 | 示例 | 结果 |
|:---|:---|:---|:-|
| `IS DISTINCT FROM` | 不相等，包括 `NULL` | `2 IS DISTINCT FROM NULL` | `true` |
| `IS NOT DISTINCT FROM` | 相等，包括 `NULL` | `NULL IS NOT DISTINCT FROM NULL` | `true` |

### 类型组合转换

在对不同类型进行比较时，DuckDB 会执行 [类型组合转换]({% link docs/stable/sql/data_types/typecasting.md %}#combination-casting)。
这些转换引入是为了让交互式查询更方便，与一些编程语言中执行的转换行为一致，但通常与 PostgreSQL 的行为不兼容。例如，以下表达式在 DuckDB 中评估并返回 `true`，但在 PostgreSQL 中会失败。

```sql
SELECT 1 = true;
SELECT 1 = '1.1';
```

> 无法对 DuckDB 的比较运算符强制执行更严格的类型检查。如果您需要更严格的类型检查，我们建议使用 [`typeof` 函数]({% link docs/stable/sql/functions/utility.md %}#typeofexpression) 创建一个 [宏]({% link docs/stable/sql/statements/create_macro.md %}) 或实现一个 [用户自定义函数]({% link docs/stable/clients/python/function.md %}).

## `BETWEEN` 和 `IS [NOT] NULL`

<div id="rrdiagram1"></div>

除了标准的比较运算符之外，还有 `BETAND` 和 `IS (NOT) NULL` 运算符。这些运算符的行为类似于运算符，但语法由 SQL 标准规定。它们在下表中展示。

请注意，`BETWEEN` 和 `NOT BETWEEN` 仅在 `a`、`x` 和 `y` 都为相同类型时才等同于下面的示例，因为 `BETWEEN` 会将所有输入转换为相同类型。

| 运算符 | 描述 |
|:---|:---|
| `a BETWEEN x AND y` | 等同于 `x <= a AND a <= y` |
| `a NOT BETWEEN x AND y` | 等同于 `x > a OR a > y` |
| `expression IS NULL` | 如果表达式为 `NULL`，则返回 `true`，否则返回 `false` |
| `expression ISNULL` | `IS NULL` 的别名（非标准） |
| `expression IS NOT NULL` | 如果表达式为 `NULL`，则返回 `false`，否则返回 `true` |
| `expression NOTNULL` | `IS NOT NULL` 的别名（非标准） |

> 对于表达式 `BETWEEN x AND y`，`x` 作为下界，`y` 作为上界。因此，如果 `x > y`，结果将始终为 `false`。