---
---
layout: docu
redirect_from:
- /docs/sql/data_types/struct
title: 结构体数据类型
---

从概念上讲，一个 `STRUCT` 列包含一个名为“条目”的有序列的列。这些条目通过字符串名称进行引用。本文档将这些条目名称称为键。`STRUCT` 列中的每一行必须具有相同的键。结构体条目名称是 *模式* 的一部分。`STRUCT` 列中的每一行必须具有相同的布局。结构体条目名称是大小写不敏感的。

`STRUCT` 通常用于将多个列嵌套到一个列中，嵌套的列可以是任何类型，包括其他 `STRUCT` 和 `LIST`。

`STRUCT` 与 PostgreSQL 的 `ROW` 类型相似。关键区别在于 DuckDB 的 `STRUCT` 要求 `STRUCT` 列中的每一行具有相同的键。这使得 DuckDB 能够通过充分利用其向量化执行引擎，显著提高性能，同时也强制类型一致性以提高正确性。DuckDB 包含一个 `row` 函数作为生成 `STRUCT` 的特殊方式，但没有 `ROW` 数据类型。下面是一个示例和 [`STRUCT` 函数文档]({% link docs/stable/sql/functions/struct.md %}) 中有详细说明。

查看 [嵌套数据类型比较]({% link docs/stable/sql/data_types/overview.md %}) 以了解嵌套数据类型的比较。

### 创建结构体

可以使用 [`struct_pack(name := expr, ...)`]({% link docs/stable/sql/functions/struct.md %}) 函数、等效的数组表示法 `{'name': expr, ...}`、行变量或 `row` 函数来创建结构体。

使用 `struct_pack` 函数创建结构体。注意键没有单引号，使用 `:=` 运算符：

```sql
SELECT struct_pack(key1 := 'value1', key2 := 42) AS s;
```

使用数组表示法创建结构体：

```sql
SELECT {'key1': 'value1', 'key2': 42} AS s;
```

使用行变量创建结构体：

```sql
SELECT d AS s FROM (SELECT 'value1' AS key1, 42 AS key2) d;
```

创建整数结构体：

```sql
SELECT {'x': 1, 'y': 2, 'z': 3} AS s;
```

创建带有 `NULL` 值的字符串结构体：

```sql
SELECT {'yes': 'duck', 'maybe': 'goose', 'huh': NULL, 'no': 'heron'} AS s;
```

创建每个键类型不同的结构体：

```sql
SELECT {'key1': 'string', 'key2': 1, 'key3': 12.345} AS s;
```

创建带有 `NULL` 值的结构体结构体：

```sql
SELECT {
        'birds': {'yes': 'duck', 'maybe': 'goose', 'huh': NULL, 'no': 'heron'},
        'aliens': NULL,
        'amphibians': {'yes': 'frog', 'maybe': 'salamander', 'huh': 'dragon', 'no': 'toad'}
    } AS s;
```

### 向结构体添加字段/值

向整数结构体添加值：

```sql
SELECT struct_insert({'a': 1, 'b': 2, 'c': 3}, d := 4) AS s;
```

### 从结构体中检索

使用点符号、方括号符号或通过 [结构体函数]({% link docs/stable/sql/functions/struct.md %}) 如 `struct_extract` 从结构体中检索值。

使用点符号检索键位置的值。在以下查询中，子查询生成一个结构体列 `a`，我们随后使用 `a.x` 查询它。

```sql
SELECT a.x FROM (SELECT {'x': 1, 'y': 2, 'z': 3} AS a);
```

如果键包含空格，只需将其用双引号 (`"`) 包围即可。

```sql
SELECT a."x space" FROM (SELECT {'x space': 1, 'y': 2, 'z': 3} AS a);
```

也可以使用方括号符号。请注意，由于目标是指定特定的字符串键，因此只能使用常量表达式：

```sql
SELECT a['x space'] FROM (SELECT {'x space': 1, 'y': 2, 'z': 3} AS a);
```

`struct_extract` 函数也等同于此。此查询返回 1：

```sql
SELECT struct_extract({'x space': 1, 'y': 2, 'z': 3}, 'x space');
```

#### `unnest` / `STRUCT.*`

而不是从结构体中检索单个键，可以使用 `unnest` 特殊函数来检索结构体的所有键作为单独的列。
这在之前的操作创建了形状未知的结构体，或者查询必须处理任何潜在的结构体键时特别有用：

```sql
SELECT unnest(a)
FROM (SELECT {'x': 1, 'y': 2, 'z': 3} AS a);
```

| x | y | z |
|--:|--:|--:|
| 1 | 2 | 3 |

同样，可以使用星号符号 (`*`) 实现，它还可以允许 [返回列的修改]({% link docs/stable/sql/expressions/star.md %})：

```sql
SELECT a.* EXCLUDE ('y')
FROM (SELECT {'x': 1, 'y': 2, 'z': 3} AS a);
```

| x | z |
|--:|--:|
| 1 | 3 |

> 警告 星号符号目前仅适用于顶层结构体列和非聚合表达式。

### 点符号的运算顺序

使用点符号引用结构体可能会与引用模式和表产生歧义。通常，DuckDB 会首先查找列，然后查找列中的结构体键。DuckDB 按照这些顺序解析引用，使用第一个匹配：

#### 没有点

```sql
SELECT part1
FROM tbl;
```

1. `part1` 是一个列

#### 一个点

```sql
SELECT part1.part2
FROM tbl;
```

1. `part1` 是一个表，`part2` 是一个列
2. `part1` 是一个列，`part2` 是该列的属性

#### 两个（或更多）点

```sql
SELECT part1.part2.part3
FROM tbl;
```

1. `part1` 是一个模式，`part2` 是一个表，`part3` 是一个列
2. `part1` 是一个表，`part2` 是一个列，`part3` 是该列的属性
3. `part1` 是一个列，`part2` 是该列的属性，`part3` 是该属性的属性

任何额外的部分（例如 `.part4.part5` 等）始终被视为属性

### 使用 `row` 函数创建结构体

`row` 函数可用于自动将多个列转换为单个结构体列。
使用 `row` 时，键将为空字符串，这使得轻松插入具有结构体列的表变得容易。
然而，列不能使用 `row` 函数进行初始化，必须显式命名。
例如，使用 `row` 函数将值插入结构体列：

```sql
CREATE TABLE t1 (s STRUCT(v VARCHAR, i INTEGER));
INSERT INTO t1 VALUES (row('a', 42));
SELECT * FROM t1;
```

该表将包含一个条目：

```sql
{'v': a, 'i': 42}
```

以下查询产生与上述相同的结果：

```sql
CREATE TABLE t1 AS (
    SELECT row('a', 42)::STRUCT(v VARCHAR, i INTEGER)
);
```

使用 `row` 函数初始化结构体列将失败：

```sql
CREATE TABLE t2 AS SELECT row('a');
```

```console
无效输入错误：
无法从未命名的结构体创建表
```

在结构体之间进行转换时，至少有一个字段的名称必须匹配。因此，以下查询将失败：

```sql
SELECT a::STRUCT(y INTEGER) AS b
FROM
    (SELECT {'x': 42} AS a);
```

```console
绑定错误：
结构体到结构体的转换必须至少有一个匹配的成员
```

一个解决方法是使用 [`struct_pack`](#creating-structs)：

```sql
SELECT struct_pack(y := a.x) AS b
FROM
    (SELECT {'x': 42} AS a);
```

`row` 函数可用于返回未命名的结构体。例如：

```sql
SELECT row(x, x + 1, y) FROM (SELECT 1 AS x, 'a' AS y) AS s;
```

这将产生 `(1, 2, a)`。

如果在创建结构体时使用多个表达式，`row` 函数是可选的。以下查询返回与前一个查询相同的结果：

```sql
SELECT (x, x + 1, y) AS s FROM (SELECT 1 AS x, 'a' AS y);
```

## 比较和排序

`STRUCT` 类型可以使用所有 [比较运算符]({% link docs/stable/sql/expressions/comparison_operators.md %}) 进行比较。
这些比较可以用于 [逻辑表达式]({% link docs/stable/sql/expressions/logical_operators.md %})，如 `WHERE` 和 `HAVING` 子句，并返回 [`BOOLEAN` 值]({% link docs/stable/sql/data_types/boolean.md %})。

对于比较，`STRUCT` 的键具有固定的顺序，从左到右。
比较行为与行比较相同，因此匹配的键必须处于相同位置。

具体来说，对于任何 `STRUCT` 比较，以下规则适用：

* **相等。** 如果所有对应值都相等，则 `s1` 和 `s2` 相等。
* **小于。** 对于第一个索引 `i`，其中 `s1.value[i] != s2.value[i]`：
如果 `s1.value[i] < s2.value[i]`，则 `s1` 小于 `s2`。

`NULL` 值的比较遵循 PostgreSQL 的语义。
较低的嵌套级别用于打破平局。

以下是返回 `true` 的比较查询。

```sql
SELECT {'k1': 2, 'k2': 3} < {'k1': 2, 'k2': 4} AS result;
```

```sql
SELECT {'k1': 'hello'} < {'k1': 'world'} AS result;
```

这些查询返回 `false`。

```sql
SELECT {'k2': 4, 'k1': 3} < {'k2': 2, 'k1': 4} AS result;
```

```sql
SELECT {'k1': [4, 3]} < {'k1': [3, 6, 7]} AS result;
```

这些查询返回 `NULL`。

```sql
SELECT {'k1': 2, 'k2': 3} < {'k1': 2, 'k2': NULL} AS result;
```

## 更新模式

从 DuckDB v1.3.0 开始，可以使用 [`ALTER TABLE` 子句]({% link docs/stable/sql/statements/alter_table.md %}) 更新结构体的子模式。

为了遵循示例，初始化 `test` 表如下：

```sql
CREATE TABLE test(s STRUCT(i INTEGER, j INTEGER));
INSERT INTO test VALUES (ROW(1, 1)), (ROW(2, 2));
```

### 添加字段

向 `test` 表中结构体 `s` 添加字段 `k INTEGER`：

```sql
ALTER TABLE test ADD COLUMN s.k INTEGER;
FROM test;
```

```text
┌─────────────────────────────────────────┐
│                    s                    │
│ struct(i integer, j integer, k integer) │
├─────────────────────────────────────────┤
│ {'i': 1, 'j': 1, 'k': NULL}             │
│ {'i': 2, 'j': 2, 'k': NULL}             │
└─────────────────────────────────────────┘
```

### 删除字段

从 `test` 表中结构体 `s` 删除字段 `i`：

```sql
ALTER TABLE test DROP COLUMN s.i;
FROM test;
```

```text
┌──────────────────────────────┐
│              s               │
│ struct(j integer, k integer) │
├──────────────────────────────┤
│ {'j': 1, 'k': NULL}          │
│ {'j': 2, 'k': NULL}          │
└──────────────────────────────┘
```

### 重命名字段

将 `test` 表中结构体 `s` 的字段 `j` 重命名为 `v1`：

```sql
ALTER TABLE test RENAME s.j TO v1;
FROM test;
```

```text
┌───────────────────────────────┐
│               s               │
│ struct(v1 integer, k integer) │
├───────────────────────────────┤
│ {'v1': 1, 'k': NULL}          │
│ {'v1': 2, 'k': NULL}          │
└───────────────────────────────┘
```

## 函数

查看 [结构体函数]({% link docs/stable/sql/functions/struct.md %})。