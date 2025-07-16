---
---
layout: docu
redirect_from:
- /docs/sql/data_types/map
title: Map 类型
---

`MAP` 与 `STRUCT` 类似，因为它们是按顺序排列的“条目”列表，其中键映射到值。然而，`MAP` 不需要每行都有相同的键，因此适用于其他使用场景。当模式在事先未知或每行模式不同时，`MAP` 非常有用；其灵活性是关键区别点。

`MAP` 必须为所有键指定一个单一类型，为所有值指定一个单一类型。键和值可以是任何类型，键的类型不需要与值的类型匹配（例如，`VARCHAR` 到 `INT` 的 `MAP` 是有效的）。`MAP` 不能有重复的键。如果找不到键，`MAP` 返回一个空列表，而不是像结构体那样抛出错误。

相比之下，`STRUCT` 必须使用字符串键，但每个键可以具有不同类型的值。有关嵌套数据类型的比较，请参阅 [数据类型概览]({% link docs/stable/sql/data_types/overview.md %}）。

要构建 `MAP`，请使用带 `MAP` 关键字的括号语法。

## 创建 Map

一个具有 `VARCHAR` 键和 `INTEGER` 值的 Map。此操作返回 `{key1=10, key2=20, key3=30}`：

```sql
SELECT MAP {'key1': 10, 'key2': 20, 'key3': 30};
```

也可以使用 `map_from_entries` 函数。此操作返回 `{key1=10, key2=20, key3=30}`：

```sql
SELECT map_from_entries([('key1', 10), ('key2', 20), ('key3', 30)]);
```

还可以使用两个列表（键和值）来创建 Map。此操作返回 `{key1=10, key2=20, key3=30}`：

```sql
SELECT MAP(['key1', 'key2', 'key3'], [10, 20, 30]);
```

Map 也可以使用 INTEGER 键和 NUMERIC 值。此操作返回 `{1=42.001, 5=-32.100}`：

```sql
SELECT MAP {1: 42.001, 5: -32.1};
```

键和/或值也可以是嵌套类型。此操作返回 `{[a, b]=[1.1, 2.2], [c, d]=[3.3, 4.4]}`：

```sql
SELECT MAP {['a', 'b']: [1.1, 2.2], ['c', 'd']: [3.3, 4.4]};
```

创建一个具有 Map 列的表，其中包含 INTEGER 键和 DOUBLE 值：

```sql
CREATE TABLE tbl (col MAP(INTEGER, DOUBLE));
```

## 从 Map 中检索

`MAP` 使用括号表示法来检索值。从 `MAP` 中选择会返回一个 `LIST` 而不是单个值，空的 `LIST` 表示键未找到。

使用括号表示法来检索键位置的值。注意，括号表示法中的表达式必须与 Map 键的类型匹配：

```sql
SELECT MAP {'key1': 5, 'key2': 43}['key1'];
```

```text
5
```

如果元素不在 Map 中，将返回 `NULL` 值。

```sql
SELECT MAP {'key1': 5, 'key2': 43}['key3'];
```

```text
NULL
```

可以使用 `element_at` 函数来检索 Map 值作为列表：

```sql
SELECT element_at(MAP {'key1': 5, 'key2': 43}, 'key1');
```

```text
[5]
```

## 比较运算符

可以使用所有 [比较运算符]({% link docs/stable/sql/expressions/comparison_operators.md %}) 来比较嵌套类型。
这些比较可以在 [逻辑表达式]({% link docs/stable/sql/expressions/logical_operators.md %}) 中用于 `WHERE` 和 `HAVING` 子句，也可以用于创建 [布尔值]({% link docs/stable/sql/data_types/boolean.md %})。

排序方式与词典中单词的排序方式相同，按位置定义。
`NULL` 值大于所有其他值，并且彼此相等。

在顶层，`NULL` 嵌套值遵循标准 SQL `NULL` 比较规则：
比较 `NULL` 嵌套值与非 `NULL` 嵌套值会生成 `NULL` 结果。
然而，比较嵌套值成员时，使用嵌套值内部的 `NULL` 规则，
`NULL` 嵌套值成员将比非 `NULL` 嵌套值成员排序更高。

## 函数

参见 [Map 函数]({% link docs/stable/sql/functions/map.md %})。