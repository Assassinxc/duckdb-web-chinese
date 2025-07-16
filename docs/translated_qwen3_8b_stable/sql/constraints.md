---
---
layout: docu
railroad: statements/constraints.js
redirect_from:
- /docs/sql/constraints
title: 约束
---

在 SQL 中，可以为表指定约束。约束对插入到表中的数据施加某些属性。约束可以与表的模式一起作为 [`CREATE TABLE` 语句]({% link docs/stable/sql/statements/create_table.md %}) 的一部分进行指定。在某些情况下，也可以使用 [`ALTER TABLE` 语句]({% link docs/stable/sql/statements/alter_table.md %}) 将约束添加到表中，但目前并非所有约束都支持这种方式。

> 警告 约束会对性能产生重大影响：它们会减慢加载和更新的速度，但会加快某些查询。请参阅 [性能指南]({% link docs/stable/guides/performance/schema.md %}#constraints) 以获取详细信息。

## 语法

<div id="rrdiagram"></div>

## 检查约束

检查约束允许您指定任意布尔表达式。任何不满足该表达式的列都会违反约束。例如，我们可以使用以下 `CHECK` 约束来强制 `name` 列不包含空格。

```sql
CREATE TABLE students (name VARCHAR CHECK (NOT contains(name, ' ')));
INSERT INTO students VALUES ('this name contains spaces');
```

```console
约束错误：
CHECK 约束在 students 表上失败，表达式为 CHECK((NOT contains("name", ' ')))
```

## 非空约束

非空约束指定列不能包含任何 `NULL` 值。默认情况下，表中的所有列都是可为空的。在列定义中添加 `NOT NULL` 可以强制该列不能包含 `NULL` 值。

```sql
CREATE TABLE students (name VARCHAR NOT NULL);
INSERT INTO students VALUES (NULL);
```

```console
约束错误：
NOT NULL 约束失败: students.name
```

## 主键和唯一约束

主键或唯一约束定义了一个列或列集，它们是表中行的唯一标识符。该约束确保指定的列在表中是 *唯一的*，即最多只能有一行具有给定的列集合值。

```sql
CREATE TABLE students (id INTEGER PRIMARY KEY, name VARCHAR);
INSERT INTO students VALUES (1, 'Student 1');
INSERT INTO students VALUES (1, 'Student 2');
```

```console
约束错误：
重复键 "id: 1" 违反主键约束
```

```sql
CREATE TABLE students (id INTEGER, name VARCHAR, PRIMARY KEY (id, name));
INSERT INTO students VALUES (1, 'Student 1');
INSERT INTO students VALUES (1, 'Student 2');
INSERT INTO students VALUES (1, 'Student 1');
```

```console
约束错误：
重复键 "id: 1, name: Student 1" 违反主键约束
```

为了高效地强制此属性，[ART 索引会自动创建]({% link docs/stable/sql/indexes.md %})，用于表中定义的每个主键或唯一约束。

主键约束和唯一约束除了以下两点外完全相同：

* 一个表只能定义一个主键约束，但可以有多个唯一约束
* 主键约束还强制键不能为 `NULL`

```sql
CREATE TABLE students (id INTEGER PRIMARY KEY, name VARCHAR, email VARCHAR UNIQUE);
INSERT INTO students VALUES (1, 'Student 1', 'student1@uni.com');
INSERT INTO students VALUES (2, 'Student 2', 'student1@uni.com');
```

```console
约束错误：
重复键 "email: student1@uni.com" 违反唯一约束
```

```sql
INSERT INTO students(id, name) VALUES (3, 'Student 3');
INSERT INTO students(name, email) VALUES ('Student 3', 'student3@uni.com');
```

```console
约束错误：
NOT NULL 约束失败: students.id
```

> 警告 索引有一定的限制，可能会导致约束被过早评估，从而导致 `违反主键约束` 和 `违反唯一约束` 等约束错误。有关更多信息，请参阅 [索引部分]({% link docs/stable/sql/indexes.md %}#index-limitations)。

## 外键

外键定义了一个列或列集，它们引用了 *另一个* 表的主键或唯一约束。该约束确保键存在于另一个表中。

```sql
CREATE TABLE students (id INTEGER PRIMARY KEY, name VARCHAR);
CREATE TABLE subjects (id INTEGER PRIMARY KEY, name VARCHAR);
CREATE TABLE exams (
    exam_id INTEGER PRIMARY KEY,
    subject_id INTEGER REFERENCES subjects(id),
    student_id INTEGER REFERENCES students(id),
    grade INTEGER
);
INSERT INTO students VALUES (1, 'Student 1');
INSERT INTO subjects VALUES (1, 'CS 101');
INSERT INTO exams VALUES (1, 1, 1, 10);
INSERT INTO exams VALUES (2, 1, 2, 10);
```

```console
约束错误：
违反外键约束，因为键 "id: 2" 不存在于引用表中
```

为了高效地强制此属性，[ART 索引会自动创建]({% link docs/stable/sql/indexes.md %})，用于表中定义的每个外键约束。

> 警告 索引有一定的限制，可能会导致约束被过早评估，从而导致 `违反主键约束` 和 `违反唯一约束` 等约束错误。有关更多信息，请参阅 [索引部分]({% link docs/stable/sql/indexes.md %}#index-limitations)。