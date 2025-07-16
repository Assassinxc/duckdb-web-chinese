---
---
layout: docu
railroad: statements/indexes.js
redirect_from:
- /docs/sql/indexes
title: 索引
---

## 索引类型

DuckDB 有两种内置的索引类型。索引也可以通过 [扩展]({% link docs/stable/core_extensions/overview.md %}) 定义。

### 最小-最大索引（Zonemap）

[最小-最大索引](https://en.wikipedia.org/wiki/Block_Range_Index)（也称为 zonemap 或块范围索引）会为所有 [通用数据类型]({% link docs/stable/sql/data_types/overview.md %} 的列 _自动创建_。

### 自适应基数树（ART）

[自适应基数树（ART）](https://db.in.tum.de/~leis/papers/ART.pdf) 主要用于确保主键约束，并加速点查询和高度选择性（即 < 0.1%）的查询。ART 索引可以通过 `CREATE INDEX` 子句手动创建，并且对于具有 `UNIQUE` 或 `PRIMARY KEY` 约束的列会自动创建。

> 警告 ART 索引在当前必须能够在索引创建时完全存入内存。如果索引在创建时无法完全存入内存，请避免创建 ART 索引。

### 由扩展定义的索引

DuckDB 通过 `spatial` 扩展支持 [用于空间索引的 R 树]({% link docs/stable/core_extensions/spatial/r-tree_indexes.md %}。

## 持久化

最小-最大索引和 ART 索引都会持久化到磁盘。

## `CREATE INDEX` 和 `DROP INDEX` 语句

要创建 [ART 索引](#adaptive-radix-tree-art)，请使用 [`CREATE INDEX` 语句]({% link docs/stable/sql/statements/create_index.md %}#create-index)。
要删除 [ART 索引](#adaptive-radix-tree-art)，请使用 [`DROP INDEX` 语句]({% link docs/stable/sql/statements/create_index.md %}#drop-index)。

## ART 索引的限制

ART 索引会在另一个位置创建数据的副本——这会增加处理复杂度，尤其是在结合事务使用时。对存储在二级索引中的数据进行修改时，存在一些限制。

> 如预期的那样，索引对性能有显著影响，会减慢加载和更新速度，但能加速某些查询。请参阅 [性能指南]({% link docs/stable/guides/performance/indexing.md %}) 以获取更多详情。

### `UPDATE` 语句中的约束检查

对已建立索引的列和无法就地更新的列执行 `UPDATE` 语句时，会将其转换为删除原始行，然后插入更新后的行。
这种重写对宽表性能有影响，因为整个行都会被重写，而不是仅更新受影响的列。

此外，它还会导致 `UPDATE` 语句的以下约束检查限制。
其他数据库管理系统（如 PostgreSQL）也存在同样的限制。

在下面的例子中，请注意行数超过了 DuckDB 的标准向量大小 2048。
`UPDATE` 语句被重写为 `DELETE`，然后是 `INSERT`。
这种重写是在数据块（2048 行）通过 DuckDB 的处理管道时进行的。
当我们将 `i = 2047` 更新为 `i = 2048` 时，我们还不知道 `2048` 会变成 `2049`，依此类推。
这是因为我们尚未看到该数据块。
因此，我们抛出一个约束违反错误。

```sql
CREATE TABLE my_table (i INTEGER PRIMARY KEY);
INSERT INTO my_table SELECT range FROM range(3_000);
UPDATE my_table SET i = i + 1;
```

```console
Constraint Error:
Duplicate key "i: 2048" violates primary key constraint.
```

一个解决方法是将 `UPDATE` 拆分为 `DELETE ... RETURNING ...` 后再执行 `INSERT`，
并添加一些额外逻辑来（暂时）存储 `DELETE` 的结果。
所有语句应通过 `BEGIN` 在事务中执行，最终使用 `COMMIT` 提交。

下面是命令行客户端中如何实现的示例。

```sql
CREATE TABLE my_table (i INTEGER PRIMARY KEY);
INSERT INTO my_table SELECT range FROM range(3_000);

BEGIN;
CREATE TEMP TABLE tmp AS SELECT i FROM my_table;
DELETE FROM my_table;
INSERT INTO my_table SELECT i FROM tmp;
DROP TABLE tmp;
COMMIT;
```

在其他客户端中，您可能可以获取 `DELETE ... RETURNING ...` 的结果。
然后，您可以使用该结果在后续的 `INSERT ...` 语句中，
或在客户端支持的情况下使用 DuckDB 的 `Appender`。

### 外键中的过度约束检查

如果满足以下条件，会出现此限制：

* 一个表具有 `FOREIGN KEY` 约束。
* 对应的 `PRIMARY KEY` 表发生 `UPDATE`，DuckDB 将其重写为 `DELETE` 后的 `INSERT`。
* 被删除的行存在于外键表中。

如果这些条件成立，您将遇到意外的约束违反错误：

```sql
CREATE TABLE pk_table (id INTEGER PRIMARY KEY, payload VARCHAR[]);
INSERT INTO pk_table VALUES (1, ['hello']);
CREATE TABLE fk_table (id INTEGER REFERENCES pk_table(id));
INSERT INTO fk_table VALUES (1);
UPDATE pk_table SET payload = ['world'] WHERE id = 1;
```

```console
Constraint Error:
Violates foreign key constraint because key "id: 1" is still referenced by a foreign key in a different table. If this is an unexpected constraint violation, please refer to our foreign key limitations in the documentation
```

造成此问题的原因是 DuckDB 不支持“预览”功能。
在 `INSERT` 期间，它不知道在 `UPDATE` 重写过程中会重新插入外键值。