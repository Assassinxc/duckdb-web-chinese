---
---
layout: docu
railroad: statements/drop.js
redirect_from:
- /docs/sql/statements/drop
title: DROP 语句
---

`DROP` 语句用于删除之前使用 `CREATE` 命令添加的目录条目。

## 示例

删除名为 `tbl` 的表：

```sql
DROP TABLE tbl;
```

删除名为 `v1` 的视图；如果视图不存在则不报错：

```sql
DROP VIEW IF EXISTS v1;
```

删除函数 `fn`：

```sql
DROP FUNCTION fn;
```

删除索引 `idx`：

```sql
DROP INDEX idx;
```

删除模式 `sch`：

```sql
DROP SCHEMA sch;
```

删除序列 `seq`：

```sql
DROP SEQUENCE seq;
```

删除宏 `mcr`：

```sql
DROP MACRO mcr;
```

删除宏表 `mt`：

```sql
DROP MACRO TABLE mt;
```

删除类型 `typ`：

```sql
DROP TYPE typ;
```

## 语法

<div id="rrdiagram"></div>

## 被删除对象的依赖关系

DuckDB 对某些对象类型进行有限的依赖关系跟踪。
默认情况下或如果提供了 `RESTRICT` 子句，如果有其他对象依赖于该对象，则不会删除该条目。
如果提供了 `CASCADE` 子句，则所有依赖该对象的对象也将被删除。

```sql
CREATE SCHEMA myschema;
CREATE TABLE myschema.t1 (i INTEGER);
DROP SCHEMA myschema;
```

```console
依赖错误：
无法删除条目 "myschema"，因为有其他条目依赖于它。
表 "t1" 依赖于模式 "myschema"。
使用 DROP...CASCADE 删除所有依赖项。
```

`CASCADE` 修饰符将删除 `myschema` 和 `myschema.t1`：

```sql
CREATE SCHEMA myschema;
CREATE TABLE myschema.t1 (i INTEGER);
DROP SCHEMA myschema CASCADE;
```

以下依赖关系会被跟踪，因此如果用户在不使用 `CASCADE` 修饰符的情况下尝试删除依赖对象，将会引发错误。

| 依赖对象类型 | 依赖对象类型 |
|--|--|
| `SCHEMA` | `FUNCTION` |
| `SCHEMA` | `INDEX` |
| `SCHEMA` | `MACRO TABLE` |
| `SCHEMA` | `MACRO` |
| `SCHEMA` | `SCHEMA` |
| `SCHEMA` | `SEQUENCE` |
| `SCHEMA` | `TABLE` |
| `SCHEMA` | `TYPE` |
| `SCHEMA` | `VIEW` |
| `TABLE`  | `INDEX` |

## 局限性

### 对视图的依赖

目前，视图的依赖关系不会被跟踪。例如，如果创建了一个引用表的视图，然后删除了该表，视图将处于无效状态：

```sql
CREATE TABLE tbl (i INTEGER);
CREATE VIEW v AS
    SELECT i FROM tbl;
DROP TABLE tbl RESTRICT;
SELECT * FROM v;
```

```console
目录错误：
名称为 tbl 的表不存在！
```

## 回收磁盘空间的限制

运行 `DROP TABLE` 应该释放表使用的内存，但不一定释放磁盘空间。
即使磁盘空间没有减少，空闲块也会被标记为 `free`。
例如，如果我们有一个 2 GB 的文件并删除了一个 1 GB 的表，该文件可能仍然是 2 GB，但其中应该有 1 GB 的空闲块。
要检查这一点，请使用以下 `PRAGMA` 并检查输出中的 `free_blocks` 数量：

```sql
PRAGMA database_size;
```

如需了解在删除表后如何回收空间，请参考 [“回收空间”页面]({% link docs/stable/operations_manual/footprint_of_duckdb/reclaiming_space.md %})。