---
---
layout: docu
railroad: expressions/logical.js
redirect_from:
- /docs/sql/expressions/logical_operators
title: 逻辑运算符
---

<div id="rrdiagram"></div>

可用的逻辑运算符有：`AND`、`OR` 和 `NOT`。SQL 使用一种三值逻辑系统，包含 `true`、`false` 和 `NULL`。请注意，涉及 `NULL` 的逻辑运算符并不总是评估为 `NULL`。例如，`NULL AND false` 会评估为 `false`，而 `NULL OR true` 会评估为 `true`。以下是完整的真值表。

### 二元运算符：`AND` 和 `OR`

<div class="monospace_table"></div>

| `a` | `b` | `a AND b` | `a OR b` |
|:---|:---|:---|:---|
| true | true | true | true |
| true | false | false | true |
| true | NULL | NULL | true |
| false | false | false | false |
| false | NULL | false | NULL |
| NULL | NULL | NULL | NULL |

### 一元运算符：NOT

<div class="monospace_table"></div>

| `a` | `NOT a` |
|:---|:---|
| true | false |
| false | true |
| NULL | NULL |

`AND` 和 `OR` 运算符是交换的，也就是说，交换左右操作数不会影响结果。