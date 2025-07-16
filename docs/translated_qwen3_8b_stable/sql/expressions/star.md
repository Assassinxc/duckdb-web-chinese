---
---
layout: docu
railroad: expressions/star.js
redirect_from:
- /docs/sql/expressions/star
title: 星号表达式
---

## 语法

<div id="rrdiagram"></div>

`*` 表达式可以在 `SELECT` 语句中使用，以选择 `FROM` 子句中投影的所有列。

```sql
SELECT *
FROM tbl;
```

### `TABLE.*` 和 `STRUCT.*`

`*` 表达式可以被表名前缀，以仅选择该表的列。

```sql
SELECT table_name.*
FROM table_name
JOIN other_table_name USING (id);
```

同样，`*` 表达式也可以用来获取结构体的所有键作为单独的列。
这在先前操作创建了形状未知的结构体，或者查询必须处理任何可能的结构体键时特别有用。
有关如何使用结构体的更多信息，请参阅 [`STRUCT` 数据类型]({% link docs/stable/sql/data_types/struct.md %}) 和 [`STRUCT` 函数]({% link docs/stable/sql/functions/struct.md %}) 页面。

例如：

```sql
SELECT st.* FROM (SELECT {'x': 1, 'y': 2, 'z': 3} AS st);
```

| x | y | z |
|--:|--:|--:|
| 1 | 2 | 3 |


### `EXCLUDE` 子句

`EXCLUDE` 允许你从 `*` 表达式中排除特定的列。

```sql
SELECT * EXCLUDE (col)
FROM tbl;
```

### `REPLACE` 子句

`REPLACE` 允许你用替代表达式替换特定的列。

```sql
SELECT * REPLACE (col1 / 1_000 AS col1, col2 / 1_000 AS col2)
FROM tbl;
```

### `RENAME` 子句

`RENAME` 允许你替换特定的列。

```sql
SELECT * RENAME (col1 AS height, col2 AS width)
FROM tbl;
```

### 通过模式匹配运算符进行列筛选

[模式匹配运算符]({% link docs/stable/sql/functions/pattern_matching.md %}) `LIKE`, `GLOB`, `SIMILAR TO` 及其变体允许你通过匹配列名到模式来选择列。

```sql
SELECT * LIKE 'col%'
FROM tbl;
```

```sql
SELECT * GLOB 'col*'
FROM tbl;
```

```sql
SELECT * SIMILAR TO 'col.'
FROM tbl;
```

## `COLUMNS` 表达式


`COLUMNS` 表达式类似于常规的星号表达式，但还允许你对结果列执行相同的表达式。

```sql
CREATE TABLE numbers (id INTEGER, number INTEGER);
INSERT INTO numbers VALUES (1, 10), (2, 20), (3, NULL);
SELECT min(COLUMNS(*)), count(COLUMNS(*)) FROM numbers;
```

| id | number | id | number |
|---:|-------:|---:|-------:|
| 1  | 10     | 3  | 2      |

```sql
SELECT
    min(COLUMNS(* REPLACE (number + id AS number))),
    count(COLUMNS(* EXCLUDE (number)))
FROM numbers;
```

| id | min(number := (number + id)) | id |
|---:|-----------------------------:|---:|
| 1  | 11                           | 3  |

`COLUMNS` 表达式也可以组合使用，只要它们包含相同的星号表达式：

```sql
SELECT COLUMNS(*) + COLUMNS(*) FROM numbers;
```

| id | number |
|---:|-------:|
| 2  | 20     |
| 4  | 40     |
| 6  | NULL   |


### `COLUMNS` 表达式在 `WHERE` 子句中

`COLUMNS` 表达式也可以在 `WHERE` 子句中使用。条件将应用于所有列，并使用逻辑 `AND` 运算符进行组合。

```sql
SELECT *
FROM (
    SELECT 0 AS x, 1 AS y, 2 AS z
    UNION ALL
    SELECT 1 AS x, 2 AS y, 3 AS z
    UNION ALL
    SELECT 2 AS x, 3 AS y, 4 AS z
)
WHERE COLUMNS(*) > 1; -- 等价于：x > 1 AND y > 1 AND z > 1
```

| x | y | z |
|--:|--:|--:|
| 2 | 3 | 4 |

### `COLUMNS` 表达式中的正则表达式

`COLUMNS` 表达式目前不支持模式匹配运算符，但可以通过将星号替换为字符串常量来支持正则表达式匹配：

```sql
SELECT COLUMNS('(id|numbers?)') FROM numbers;
```

| id | number |
|---:|-------:|
| 1  | 10     |
| 2  | 20     |
| 3  | NULL   |

### 在 `COLUMNS` 表达式中使用正则表达式重命名列

正则表达式中捕获组的匹配可以用于重命名匹配的列。
捕获组是按一索引编号的；`\0` 是原始列名。

例如，要选择列名的前三个字母，运行：

```sql
SELECT COLUMNS('(\w{3}).*') AS '\1' FROM numbers;
```

| id | num  |
|---:|-----:|
| 1  | 10   |
| 2  | 20   |
| 3  | NULL |

要删除列名中间的冒号 (`:`) 字符，运行：

```sql
CREATE TABLE tbl ("Foo:Bar" INTEGER, "Foo:Baz" INTEGER, "Foo:Qux" INTEGER);
SELECT COLUMNS('(\w*):(\w*)') AS '\1\2' FROM tbl;
```

要将原始列名添加到表达式别名中，运行：
```sql
SELECT min(COLUMNS(*)) AS "min_\0" FROM numbers;
```

| min_id | min_number |
|-------:|-----------:|
|      1 |         10 |

### `COLUMNS` Lambda 函数

`COLUMNS` 也支持传入一个 lambda 函数。lambda 函数将对 `FROM` 子句中所有存在的列进行评估，并且只有匹配 lambda 函数的列才会被返回。这允许执行任意表达式以选择和重命名列。

```sql
SELECT COLUMNS(c -> c LIKE '%num%') FROM numbers;
```

| number |
|-------:|
| 10     |
| 20     |
| NULL   |


### `COLUMNS` 列表

`COLUMNS` 也支持传入列名列表。

```sql
SELECT COLUMNS(['id', 'num']) FROM numbers;
```

| id | num  |
|---:|-----:|
| 1  | 10   |
| 2  | 20   |
| 3  | NULL |

## `*COLUMNS` 解包列

`*COLUMNS` 子句是 `COLUMNS` 的一种变体，支持之前提到的所有功能。
区别在于表达式如何展开。

`*COLUMNS` 将在原地展开，类似于 [Python 中的可迭代展开行为](https://peps.python.org/pep-3132/)，这启发了 `*` 语法。
这意味着表达式会扩展到父表达式中。
一个展示 `COLUMNS` 与 `*COLUMNS` 区别的示例：

使用 `COLUMNS`：

```sql
SELECT coalesce(COLUMNS(['a', 'b', 'c'])) AS result
FROM (SELECT NULL a, 42 b, true c);
```

| result | result | result |
|--------|-------:|-------:|
| NULL   | 42     | true   |

使用 `*COLUMNS`，表达式在父表达式 `coalesce` 中展开，结果为一个结果列：

```sql
SELECT coalesce(*COLUMNS(['a', 'b', 'c'])) AS result
FROM (SELECT NULL AS a, 42 AS b, true AS c);
```

| result |
|-------:|
| 42     |

`*COLUMNS` 也支持 `(*)` 参数：

```sql
SELECT coalesce(*COLUMNS(*)) AS result
FROM (SELECT NULL a, 43 AS b, true AS c);
```

| result |
|-------:|
| 42     |

## `STRUCT.*`

`*` 表达式也可以用来获取结构体的所有键作为单独的列。
这在先前操作创建了形状未知的结构体，或者查询必须处理任何可能的结构体键时特别有用。
有关如何使用结构体的更多信息，请参阅 [`STRUCT` 数据类型]({% link docs/stable/sql/data_types/struct.md %}) 和 [`STRUCT` 函数]({% link docs/stable/sql/functions/struct.md %}) 页面。

例如：

```sql
SELECT st.* FROM (SELECT {'x': 1, 'y': 2, 'z': 3} AS st);
```

| x | y | z |
|--:|--:|--:|
| 1 | 2 | 3 |