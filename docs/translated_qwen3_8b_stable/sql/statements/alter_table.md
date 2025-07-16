---
---
layout: docu
railroad: statements/alter.js
redirect_from:
- /docs/sql/statements/alter_table
title: ALTER TABLE 语句
---

`ALTER TABLE` 语句用于更改目录中现有表的模式。

## 示例

```sql
CREATE TABLE integers (i INTEGER, j INTEGER);
```

向表 `integers` 中添加一个名为 `k` 的新列，该列将被填充默认值 `NULL`：

```sql
ALTER TABLE integers
ADD COLUMN k INTEGER;
```

向表 `integers` 中添加一个名为 `l` 的新列，该列将被填充默认值 10：

```sql
ALTER TABLE integers
ADD COLUMN l INTEGER DEFAULT 10;
```

从表 `integers` 中删除列 `k`：

```sql
ALTER TABLE integers
DROP k;
```

使用标准类型转换将列 `i` 的类型更改为 `VARCHAR`：

```sql
ALTER TABLE integers
ALTER i TYPE VARCHAR;
```

使用指定表达式将列 `i` 的类型更改为 `VARCHAR`，并为每一行数据进行转换：

```sql
ALTER TABLE integers
ALTER i SET DATA TYPE VARCHAR USING concat(i, '_', j);
```

设置列的默认值：

```sql
ALTER TABLE integers
ALTER COLUMN i SET DEFAULT 10;
```

删除列的默认值：

```sql
ALTER TABLE integers
ALTER COLUMN i DROP DEFAULT;
```

使列变为非空：

```sql
ALTER TABLE integers
ALTER COLUMN i SET NOT NULL;
```

删除非空约束：

```sql
ALTER TABLE integers
ALTER COLUMN i DROP NOT NULL;
```

重命名表：

```sql
ALTER TABLE integers
RENAME TO integers_old;
```

重命名表中的列：

```sql
ALTER TABLE integers
RENAME i TO ii;
```

向表中的列添加主键：

```sql
ALTER TABLE integers
ADD PRIMARY KEY (i);
```

## 语法

<div id="rrdiagram"></div>

`ALTER TABLE` 用于更改现有表的模式。
`ALTER TABLE` 所做的所有更改都完全遵循事务语义，即直到提交后，其他事务才可见，且可以通过回滚完全撤销。

## `RENAME TABLE`

重命名表：

```sql
ALTER TABLE integers
RENAME TO integers_old;
```

`RENAME TO` 子句用于重命名整个表，更改其在模式中的名称。请注意，任何依赖该表的视图**不会**自动更新。

## `RENAME COLUMN`

要重命名表中的列，使用 `RENAME` 或 `RENAME COLUMN` 子句：

```sql
ALTER TABLE integers 
RENAME COLUMN i TO j;
```

```sql
ALTER TABLE integers
RENAME i TO j;
```

`RENAME [COLUMN]` 子句用于重命名表中的单个列。任何依赖此名称的约束（例如 `CHECK` 约束）会自动更新。但是，请注意，任何依赖此列名称的视图**不会**自动更新。

## `ADD COLUMN`

要向表中添加列，使用 `ADD` 或 `ADD COLUMN` 子句。

例如，向表 `integers` 中添加一个名为 `k` 的新列，该列将被填充默认值 `NULL`：

```sql
ALTER TABLE integers
ADD COLUMN k INTEGER;
```

或者：

```sql
ALTER TABLE integers
ADD k INTEGER;
```

向表 `integers` 中添加一个名为 `l` 的新列，该列将被填充默认值 10：

```sql
ALTER TABLE integers
ADD COLUMN l INTEGER DEFAULT 10;
```

`ADD [COLUMN]` 子句可用于向表中添加一个指定类型的列。新列将被填充指定的默认值，如果没有指定默认值，则填充 `NULL`。

## `DROP COLUMN`

要删除表中的列，使用 `DROP` 或 `DROP COLUMN` 子句：

例如，从表 `integers` 中删除列 `k`：

```sql
ALTER TABLE integers
DROP COLUMN k;
```

或者：

```sql
ALTER TABLE integers
DROP k;
```

`DROP [COLUMN]` 子句可用于从表中删除列。请注意，只有当列没有依赖它的索引时才能删除列。这包括任何作为 `PRIMARY KEY` 或 `UNIQUE` 约束创建的索引。同时，不能删除作为多列检查约束一部分的列。
如果你尝试删除带有索引的列，DuckDB 将返回以下错误信息：

```console
依赖错误：
无法更改条目 "..."，因为有依赖它的条目。
```

## `[SET [DATA]] TYPE`

使用标准类型转换将列 `i` 的类型更改为 `VARCHAR`：

```sql
ALTER TABLE integers
ALTER i TYPE VARCHAR;
```

> 除了 `ALTER ⟨column_name⟩ TYPE ⟨type⟩`{:.language-sql .highlight}，你还可以使用等效的
> `ALTER ⟨column_name⟩ SET TYPE ⟨type⟩`{:.language-sql .highlight} 和
> `ALTER ⟨column_name⟩ SET DATA TYPE ⟨type⟩`{:.language-sql .highlight} 子句。

使用指定表达式将列 `i` 的类型更改为 `VARCHAR`，并为每一行数据进行转换：

```sql
ALTER TABLE integers
ALTER i SET DATA TYPE VARCHAR USING concat(i, '_', j);
```

`[SET [DATA]] TYPE` 子句用于更改表中列的类型。列中存在的任何数据将根据 `USING` 子句中提供的表达式进行转换，或者如果没有指定 `USING` 子句，则转换为新的数据类型。请注意，只有当列没有依赖它的索引且不属于任何 `CHECK` 约束时，才能更改其类型。

### 处理结构体

更改 [`STRUCT`]({% link docs/stable/sql/data_types/struct.md %}) 类型列的子模式有两种选项。

#### 使用 `struct_insert` 的 `ALTER TABLE`

你可以使用 `ALTER TABLE` 与 `struct_insert` 函数。
例如：

```sql
CREATE TABLE tbl (col STRUCT(i INTEGER));
ALTER TABLE tbl
ALTER col TYPE USING struct_insert(col, a := 42, b := NULL::VARCHAR);
```

#### 使用 `ADD COLUMN` / `DROP COLUMN` / `RENAME COLUMN` 的 `ALTER TABLE`

从 DuckDB v1.3.0 开始，`ALTER TABLE` 支持
[`ADD COLUMN`, `DROP COLUMN` 和 `RENAME COLUMN` 子句]({% link docs/stable/sql/data_types/struct.md %}#updating-the-schema)
来更新 `STRUCT` 的子模式。

## `SET` / `DROP DEFAULT`

设置列的默认值：

```sql
ALTER TABLE integers
ALTER COLUMN i SET DEFAULT 10;
```

删除列的默认值：

```sql
ALTER TABLE integers
ALTER COLUMN i DROP DEFAULT;
```

`SET/DROP DEFAULT` 子句修改现有列的 `DEFAULT` 值。请注意，这不会修改列中已有的数据。删除默认值等同于将默认值设置为 `NULL`。

> 警告 当前 DuckDB 不允许在存在依赖关系的情况下修改表。这意味着如果你在某一列上创建了索引，你需要先删除索引，修改表，然后再重新创建索引。否则，你将收到一个 `Dependency Error`。

## `ADD PRIMARY KEY`

向表中的列添加主键：

```sql
ALTER TABLE integers
ADD PRIMARY KEY (i);
```

向表中的多个列添加主键：

```sql
ALTER TABLE integers
ADD PRIMARY KEY (i, j);
```

## `ADD` / `DROP CONSTRAINT`

> `ADD CONSTRAINT` 和 `DROP CONSTRAINT` 子句在 DuckDB 中尚未支持。

## 限制

如果表中曾经出现过冲突类型值，`ALTER COLUMN` 将失败，即使这些值已被删除：

```sql
CREATE TABLE tbl (col VARCHAR);

INSERT INTO tbl
VALUES ('asdf'), ('42');

DELETE FROM tbl
WHERE col = 'asdf';

ALTER TABLE tbl
ALTER COLUMN col TYPE INTEGER;
```

```console
转换错误：
无法将字符串 'asdf' 转换为 INT32
```

目前这是预期的行为。
作为变通方法，你可以创建表的副本：

```sql
CREATE OR REPLACE TABLE tbl AS FROM tbl;
```