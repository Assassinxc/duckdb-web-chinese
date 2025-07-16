---
---
layout: docu
railroad: statements/indexes.js
redirect_from:
- /docs/sql/statements/create_index
title: CREATE INDEX 语句
---

## `CREATE INDEX`

`CREATE INDEX` 语句在指定表的指定列上构建索引。

### 示例

在表 `films` 的列 `id` 上创建一个唯一索引 `films_id_idx`：

```sql
CREATE UNIQUE INDEX films_id_idx ON films (id);
```

在表 `films` 的列 `revenue` 上创建一个允许重复值的索引 `s_idx`：

```sql
CREATE INDEX s_idx ON films (revenue);
```

如果索引尚不存在则创建索引：

```sql
CREATE INDEX IF NOT EXISTS s_idx ON films (revenue);
```

> `CREATE INDEX IF NOT EXISTS` 语句目前不支持“提前退出”，它会尝试创建索引，并在提交到存储之前检查其是否存在。因此，与其它 `IF NOT EXISTS` 语句相比，它可能会执行更长时间。

在 `genre` 和 `year` 列上创建复合索引 `gy_idx`：

```sql
CREATE INDEX gy_idx ON films (genre, year);
```

在表 `integers` 的列 `j` 和 `k` 的总和表达式上创建索引 `i_index`：

```sql
CREATE INDEX i_index ON integers ((j + k));
```

### 参数

| 名称 | 描述 |
|:-|:-----|
| `UNIQUE` | 在创建索引时（如果数据已存在）以及每次添加数据时，系统会检查表中是否有重复值。尝试插入或更新会导致重复条目的数据将生成错误。 |
| `name` | 要创建的索引的名称。 |
| `table` | 要建立索引的表的名称。 |
| `column` | 要建立索引的列的名称。 |
| `expression` | 基于表的一个或多个列的表达式。该表达式通常必须用括号括起来，如语法所示。但如果表达式形式为函数调用，则可以省略括号。 |
| `index type` | 指定索引类型，详见 [Indexes]({% link docs/stable/sql/indexes.md %})。可选。 |
| `option` | 以布尔值 true 形式（例如 `is_cool`）或键值对形式（例如 `my_option = 2`）表示的索引选项。可选。 |

### 语法

<div id="rrdiagram1"></div>

## `DROP INDEX`

`DROP INDEX` 从数据库系统中删除现有的索引。

### 示例

删除索引 `title_idx`：

```sql
DROP INDEX title_idx;
```

### 参数

| 名称 | 描述 |
|:---|:---|
| `IF EXISTS` | 如果索引不存在，则不抛出错误。 |
| `name` | 要删除的索引的名称。 |

### 语法

<div id="rrdiagram2"></div>

## 限制

`CREATE INDEX` 子句不支持 `OR REPLACE` 修饰符。