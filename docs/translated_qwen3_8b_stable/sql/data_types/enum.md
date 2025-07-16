---
---
blurb: Enum 类型表示一个列所有可能唯一值的字典数据结构。
layout: docu
redirect_from:
- /docs/sql/data_types/enum
title: Enum 数据类型
---

| 名称 | 描述 |
|:--|:-----|
| `ENUM` | 表示列所有可能字符串值的字典 |

Enum 类型表示一个列所有可能唯一值的字典数据结构。例如，一个存储一周中每一天的列可以是一个枚举类型，包含所有可能的天数。对于具有低基数（即较少不同值）的字符串列，枚举类型特别有用。这是因为列仅存储指向枚举字典中字符串的数值引用，从而在磁盘存储上节省大量空间，并提高查询性能。

## 枚举定义

枚举类型可以由硬编码的值集合或返回单列 `VARCHAR` 的 `SELECT` 语句创建。`SELECT` 语句中的值集合将被去重，但如果枚举类型由硬编码的值集合创建，则可能没有重复项。

使用硬编码值创建枚举：

```sql
CREATE TYPE ⟨enum_name⟩ AS ENUM (⟨value_1⟩, ⟨value_2⟩, ...);
```

使用返回单列 `VARCHAR` 的 `SELECT` 语句创建枚举：

```sql
CREATE TYPE ⟨enum_name⟩ AS ENUM (⟨select_expression⟩);
```

枚举类型也可以在 [类型转换]({% link docs/stable/sql/expressions/cast.md %}) 过程中动态创建：

```sql
SELECT 'some_string'::ENUM (⟨value_1⟩, ⟨value_2⟩, ...);
```

### 示例

创建新的用户定义类型 `mood` 作为枚举：

```sql
CREATE TYPE mood AS ENUM ('sad', 'ok', 'happy');
```

从 `SELECT` 语句创建枚举。首先创建一个示例值表：

```sql
CREATE TABLE my_inputs AS
    FROM (VALUES ('duck'), ('duck'), ('goose')) t(my_varchar);
```

动态创建匿名枚举值：

```sql
SELECT 'happy'::ENUM ('sad', 'ok', 'happy');
```

此语句会失败，因为枚举类型不能包含 `NULL` 值：

```sql
CREATE TYPE breed AS ENUM ('maltese', NULL);
```

此语句会失败，因为枚举值必须唯一：

```sql
CREATE TYPE breed AS ENUM ('maltese', 'maltese');
```

使用 `my_varchar` 列中的唯一字符串值创建枚举：

```sql
CREATE TYPE birds AS ENUM (SELECT my_varchar FROM my_inputs);
```

使用 `enum_range` 函数显示 `birds` 枚举中的可用值：

```sql
SELECT enum_range(NULL::birds) AS my_enum_range;
```

|  my_enum_range  |
|-----------------|
| `[duck, goose]` |

## 枚举使用

创建枚举类型后，可以在任何需要标准内置类型的地方使用它。例如，我们可以创建一个包含引用枚举类型的列的表。

创建一个 `person` 表，包含 `name`（字符串类型）和 `current_mood`（`mood` 类型）属性：

```sql
CREATE TABLE person (
    name TEXT,
    current_mood mood
);
```

向 `person` 表中插入元组：

```sql
INSERT INTO person
VALUES ('Pedro', 'happy'), ('Mark', NULL), ('Pagliacci', 'sad'), ('Mr. Mackey', 'ok');
```

以下查询会失败，因为 `mood` 类型没有 `quackity-quack` 值。

```sql
INSERT INTO person
VALUES ('Hannes', 'quackity-quack');
```

字符串 `sad` 被转换为 `mood` 类型，返回一个数值引用值。
这使得比较变为数值比较，而不是字符串比较。

```sql
SELECT *
FROM person
WHERE current_mood = 'sad';
```

|   name    | current_mood |
|-----------|--------------|
| Pagliacci | sad          |

如果你从文件导入数据，可以在导入前为 `VARCHAR` 列创建一个枚举类型。
鉴于此，以下子查询将自动选择唯一的值：

```sql
CREATE TYPE mood AS ENUM (SELECT mood FROM 'path/to/file.csv');
```

然后你可以创建一个包含枚举类型的表，并使用任何数据导入语句进行导入：

```sql
CREATE TABLE person (name TEXT, current_mood mood);
COPY person FROM 'path/to/file.csv';
```

## 枚举与字符串

DuckDB 枚举在需要时会自动转换为 `VARCHAR` 类型。这一特性允许枚举列在任何 `VARCHAR` 函数中使用。此外，它还允许在不同枚举列之间，或枚举列和 `VARCHAR` 列之间进行比较。

例如：

`regexp_matches` 是一个接受 `VARCHAR` 参数的函数，因此 `current_mood` 会被转换为 `VARCHAR`：

```sql
SELECT regexp_matches(current_mood, '.*a.*') AS contains_a
FROM person;
```

| contains_a |
|:-----------|
| true       |
| NULL       |
| true       |
| false      |

创建一个新的 `mood` 类型和表：

```sql
CREATE TYPE new_mood AS ENUM ('happy', 'anxious');
CREATE TABLE person_2 (
    name text,
    current_mood mood,
    future_mood new_mood,
    past_mood VARCHAR
);
```

由于 `current_mood` 和 `future_mood` 列是基于不同的枚举类型构建的，DuckDB 会将这两个枚举转换为字符串并进行字符串比较：

```sql
SELECT *
FROM person_2
WHERE current_mood = future_mood;
```

当比较 `past_mood` 列（字符串）时，DuckDB 会将 `current_mood` 枚举转换为 `VARCHAR` 并进行字符串比较：

```sql
SELECT *
FROM person_2
WHERE current_mood = past_mood;
```

## 枚举删除

枚举类型存储在目录中，并且每个使用它们的表都会添加一个目录依赖项。可以使用以下命令从目录中删除枚举类型：

```sql
DROP TYPE ⟨enum_name⟩;
```

目前，可以删除表中使用到的枚举类型，而不会影响表本身。

> 警告 枚举删除功能的行为可能会发生变化。在未来的版本中，预计在删除枚举类型之前必须先删除所有依赖列，或者必须使用额外的 `CASCADE` 参数进行删除。

## 枚举比较

枚举值的比较是根据其在枚举定义中的顺序进行的。例如：

```sql
CREATE TYPE mood AS ENUM ('sad', 'ok', 'happy');
```

```sql
SELECT 'sad'::mood < 'ok'::mood AS comp;
```

| comp |
|-----:|
| true |

```sql
SELECT unnest(['ok'::mood, 'happy'::mood, 'sad'::mood]) AS m
ORDER BY m;
```

|   m   |
|-------|
| sad   |
| ok    |
| happy |

## 函数

参见 [枚举函数]({% link docs/stable/sql/functions/enum.md %})。