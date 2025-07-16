---
---
layout: docu
redirect_from:
- /docs/sql/case_sensitivity
- /docs/sql/case_sensitivity/
- /docs/sql/keywords-and-identifiers
- /docs/sql/keywords-and-identifiers/
- /docs/sql/dialect/keywords-and-identifiers
- /docs/sql/dialect/keywords-and-identifiers/
- /docs/sql/dialect/keywords_and_identifiers
title: 关键字和标识符
---

## 标识符

与其它 SQL 方言和编程语言类似，DuckDB 的 SQL 中的标识符也遵循一些规则。

* 未加引号的标识符需要遵循一些规则：
    * 它们不能是保留关键字（参见 [`duckdb_keywords()`]({% link docs/stable/sql/meta/duckdb_table_functions.md %}#duckdb_keywords))，例如 `SELECT 123 AS SELECT` 会失败。
    * 它们不能以数字或特殊字符开头，例如 `SELECT 123 AS 1col` 是无效的。
    * 它们不能包含空格（包括制表符和换行符）。
* 可以使用双引号字符 (`"`) 来引用标识符。引用的标识符可以使用任何关键字、空格或特殊字符，例如 `"SELECT"` 和 `" § 🦆 ¶ "` 是有效的标识符。
* 双引号可以通过重复引号字符进行转义，例如要创建一个名为 `IDENTIFIER "X"` 的标识符，可以使用 `"IDENTIFIER ""X"""`。

### 去重标识符

在某些情况下，可能会出现重复的标识符，例如在展开嵌套数据结构时，列名可能会冲突。
在这种情况下，DuckDB 会自动去重列名，通过以下规则重命名它们：

* 对于名为 `⟨name⟩`{:.language-sql .highlight} 的列，第一个实例不会被重命名。
* 后续的实例将被重命名为 `⟨name⟩_⟨count⟩`{:.language-sql .highlight}，其中 `⟨count⟩`{:.language-sql .highlight} 从 1 开始。

例如：

```sql
SELECT *
FROM (SELECT UNNEST({'a': 42, 'b': {'a': 88, 'b': 99}}, recursive := true));
```

| a  | a_1 | b  |
|---:|----:|---:|
| 42 | 88  | 99 |

## 数据库名称

数据库名称遵循 [标识符](#identifiers) 的规则。

另外，最好避免使用 DuckDB 的两个内部 [数据库模式名称]({% link docs/stable/sql/meta/duckdb_table_functions.md %}#duckdb_databases)，即 `system` 和 `temp`。
默认情况下，持久化数据库的名称以其文件名（不含扩展名）命名。
因此，文件名 `system.db` 和 `temp.db`（以及 `system.duckdb` 和 `temp.duckdb`）分别导致数据库名称 `system` 和 `temp`。
如果需要连接到具有这些名称的数据库，请使用别名，例如：

```sql
ATTACH 'temp.db' AS temp2;
USE temp2;
```

## 大小写敏感规则

### 关键字和函数名称

DuckDB 中的 SQL 关键字和函数名称是不区分大小写的。

例如，以下两个查询是等价的：

```matlab
select COS(Pi()) as CosineOfPi;
SELECT cos(pi()) AS CosineOfPi;
```

| CosineOfPi |
|-----------:|
| -1.0       |

### 标识符的大小写敏感性

DuckDB 中的标识符始终是不区分大小写的，与 PostgreSQL 类似。
然而，与 PostgreSQL（以及一些其他主要的 SQL 实现）不同，DuckDB 也将带引号的标识符视为不区分大小写的。

**标识符的比较：**
大小写不敏感是通过基于 ASCII 的比较实现的：
`col_A` 和 `col_a` 是相等的，但 `col_á` 不等于它们。

```sql
SELECT col_A FROM (SELECT 'x' AS col_a); -- 成功
SELECT col_á FROM (SELECT 'x' AS col_a); -- 失败
```

**保留大小写：**
虽然 DuckDB 以不区分大小写的方式处理标识符，但它保留了这些标识符的大小写。
也就是说，每个字符的大小写（大写/小写）都会按照用户最初指定的方式保留，即使查询在引用标识符时使用了不同的大小写。
例如：

```sql
CREATE TABLE tbl AS SELECT cos(pi()) AS CosineOfPi;
SELECT cosineofpi FROM tbl;
```

| CosineOfPi |
|-----------:|
| -1.0       |

要更改此行为，请将 `preserve_identifier_case` [配置选项]({% link docs/stable/configuration/overview.md %}#configuration-reference) 设置为 `false`。

### 嵌套数据结构中键的大小写敏感性

`MAP` 的键是大小写敏感的：

```sql
SELECT MAP(['key1'], [1]) = MAP(['KEY1'], [1]) AS equal;
```

```text
false
```

`UNION` 和 `STRUCT` 的键是不区分大小写的：

```sql
SELECT {'key1': 1} = {'KEY1': 1} AS equal;
```

```text
true
```

```sql
SELECT union_value(key1 := 1) = union_value(KEY1 := 1) as equal;
```

```text
true
```

#### 处理冲突

在发生冲突时，如果相同的标识符以不同的大小写形式书写，会随机选择其中一个。例如：

```sql
CREATE TABLE t1 (idfield INTEGER, x INTEGER);
CREATE TABLE t2 (IdField INTEGER, y INTEGER);
INSERT INTO t1 VALUES (1, 123);
INSERT INTO t2 VALUES (1, 456);
SELECT * FROM t1 NATURAL JOIN t2;
```

| idfield |  x  |  y  |
|--------:|----:|----:|
| 1       | 123 | 456 |

#### 禁用保留大小写

将 `preserve_identifier_case` [配置选项]({% link docs/stable/configuration/overview.md %}#configuration-reference) 设置为 `false`，所有标识符都会被转换为小写：

```sql
SET preserve_identifier_case = false;
CREATE TABLE tbl AS SELECT cos(pi()) AS CosineOfPi;
SELECT CosineOfPi FROM tbl;
```

| cosineofpi |
|-----------:|
| -1.0       |