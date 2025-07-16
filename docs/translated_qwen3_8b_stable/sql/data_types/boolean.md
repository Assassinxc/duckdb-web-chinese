---
---
blurb: BOOLEAN 类型表示一个真值的陈述（“true” 或 “false”）。
layout: docu
redirect_from:
- /docs/sql/data_types/boolean
title: Boolean 类型
---

| 名称 | 别名 | 描述 |
|:---|:---|:---|
| `BOOLEAN` | `BOOL` | 逻辑布尔值 (`true` / `false`) |

`BOOLEAN` 类型表示一个真值的陈述（“true” 或 “false”）。在 SQL 中，`BOOLEAN` 字段还可以有第三种状态 “unknown”，它由 SQL 的 `NULL` 值表示。

选择 `BOOLEAN` 列的三个可能值：

```sql
SELECT true, false, NULL::BOOLEAN;
```

布尔值可以使用字面量 `true` 和 `false` 显式创建。然而，它们大多是通过比较或逻辑运算产生。例如，比较 `i > 10` 会生成一个布尔值。布尔值可以用于 SQL 语句的 `WHERE` 和 `HAVING` 子句中，以过滤结果中的元组。在这种情况下，对于谓词评估为 `true` 的元组会通过过滤，而谓词评估为 `false` 或 `NULL` 的元组会被过滤掉。请考虑以下示例：

创建一个包含值 5、15 和 `NULL` 的表：

```sql
CREATE TABLE integers (i INTEGER);
INSERT INTO integers VALUES (5), (15), (NULL);
```

选择所有满足 `i > 10` 的条目：

```sql
SELECT * FROM integers WHERE i > 10;
```

在这种情况下，5 和 `NULL` 会被过滤掉（`5 > 10` 为 `false`，`NULL > 10` 为 `NULL`）：

| i  |
|---:|
| 15 |

## 逻辑运算符

`AND` / `OR` 运算符可用于组合布尔值。

以下是 `AND` 运算符的真值表（即 `x AND y`）。

<div class="monospace_table"></div>

| `X` | `X AND true` | `X AND false` | `X AND NULL` |
|-------|-------|-------|-------|
| true  | true  | false | NULL  |
| false | false | false | false |
| NULL  | NULL  | false | NULL  |

以下是 `OR` 运算符的真值表（即 `x OR y`）。

<div class="monospace_table"></div>

| `X` | `X OR true` | `X OR false` | `X OR NULL` |
|-------|------|-------|------|
| true  | true | true  | true |
| false | true | false | NULL |
| NULL  | true | NULL  | NULL |

## 表达式

参见 [逻辑运算符]({% link docs/stable/sql/expressions/logical_operators.md %}) 和 [比较运算符]({% link docs/stable/sql/expressions/comparison_operators.md %})。