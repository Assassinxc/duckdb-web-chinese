---
---
layout: docu
redirect_from:
- /dev/sqllogictest/result_verification
- /dev/sqllogictest/result_verification/
- /docs/dev/sqllogictest/result_verification
title: 结果验证
---

验证查询结果的标准方式是使用 `query` 语句，后跟字母 `I` 乘以预期结果中的列数。在查询之后，预期有四个连字符 (`----`)，随后是用制表符分隔的结果值。例如，

```sql
query II
SELECT 42, 84 UNION ALL SELECT 10, 20;
----
42	84
10	20
```

由于历史原因，字母 `R` 和 `T` 也被接受用于表示列。

> 已弃用 DuckDB 已弃用 sqllogictest 中的类型用法。DuckDB 测试运行器内部不需要或使用它们，因此，只应使用 `I` 来表示列。

## NULL 值和空字符串

空行对 SQLLogic 测试运行器有特殊意义：它们表示当前语句或查询的结束。因此，空字符串和 NULL 值在结果验证中有特殊的语法。NULL 值应使用字符串 `NULL`，空字符串应使用字符串 `(empty)`，例如：

```sql
query II
SELECT NULL, ''
----
NULL
(empty)
```

## 错误验证

为了表示预期会出错，可以使用 `statement error` 指示器。`statement error` 还可以接受一个可选的预期结果，该结果被解释为 *预期的错误信息*。与 `query` 类似，预期的错误信息应放在查询后的四个连字符 (`----`) 之后。如果错误信息 *包含* `statement error` 下的文本，测试即通过——不需要提供整个错误信息。建议只使用错误信息的一个子集，以防止在错误信息格式更改时测试意外失败。

```sql
statement error
SELECT * FROM non_existent_table;
----
Table with name non_existent_table does not exist!
```

## 正则表达式

在某些情况下，结果值可能非常大或复杂，我们可能只关心结果 *是否包含* 某段文本。在这种情况下，可以使用 `<REGEX>:` 修饰符后跟一个正则表达式。如果结果值与正则表达式匹配，测试即通过。这主要用于查询计划分析。

```sql
query II
EXPLAIN SELECT tbl.a FROM 'data/parquet-testing/arrow/alltypes_plain.parquet' tbl(a) WHERE a = 1 OR a = 2
----
physical_plan	<REGEX>:.*PARQUET_SCAN.*Filters: a=1 OR a=2.*
```

如果我们希望结果 *不包含* 某段文本，可以使用 `<!REGEX>:` 修饰符。

## 文件

由于结果可能会变得非常庞大，且我们可能希望在多个文件中重用结果，也可以使用 `<FILE>` 命令从文件中读取预期结果。预期结果从给定的文件中读取。按惯例，文件路径应相对于 GitHub 仓库的根目录提供。

```sql
query I
PRAGMA tpch(1)
----
<FILE>:extension/tpch/dbgen/answers/sf1/q01.csv
```

## 按行顺序与按值顺序的结果排序

查询的结果值可以按行顺序提供，各个值用制表符分隔，也可以按值顺序提供。在按值顺序时，查询的各个 *值* 必须按行、列顺序分别出现在单独的一行中。以下示例展示了按行顺序和按值顺序的对比：

```sql
# 按行顺序
query II
SELECT 42, 84 UNION ALL SELECT 10, 20;
----
42	84
10	20

# 按值顺序
query II
SELECT 42, 84 UNION ALL SELECT 10, 20;
----
42
84
10
20
```

## 哈希值与输出值

除了直接的结果验证，sqllogic 测试套件还支持使用 MD5 哈希值进行值比较。使用哈希值进行结果验证的测试如下所示：

```sql
query I
SELECT g, string_agg(x,',') FROM strings GROUP BY g
----
200 values hashing to b8126ea73f21372cdb3f2dc483106a12
```

这种方法在结果包含许多输出行时有助于减小测试的规模。然而，应谨慎使用，因为哈希值会使测试在失败时更难以调试。

在确保系统输出正确结果后，可以在测试文件中添加 `mode output_hash` 来计算查询的哈希值。例如：

```sql
mode output_hash

query II
SELECT 42, 84 UNION ALL SELECT 10, 20;
----
42	84
10	20
```

测试文件中每个查询的预期输出哈希值将被打印到终端，如下所示：

```text
================================================================================
SQL Query
SELECT 42, 84 UNION ALL SELECT 10, 20;
================================================================================
4 values hashing to 498c69da8f30c24da3bd5b322a2fd455
================================================================================
```

以类似的方式，可以使用 `mode output_result` 强制程序在测试文件中运行每个查询时将结果输出到终端。

## 结果排序

查询可以有一个可选字段，用于指示结果应以特定方式排序。该字段位于与连接标签相同的位置。因此，连接标签和结果排序不能混用。

该字段的可能值为 `nosort`、`rowsort` 和 `valuesort`。下面是一个使用示例：

```sql
query I rowsort
SELECT 'world' UNION ALL SELECT 'hello'
----
hello
world
```

通常，我们不建议使用该字段，而是依靠查询中的 `ORDER BY` 生成确定性的查询结果。然而，现有的 sqllogictests 广泛使用该字段，因此了解其存在非常重要。

## 查询标签

另一个可用于结果验证的特性是 `query labels`。这些标签可用于验证不同的查询是否提供相同的结果。这对于比较逻辑等价但表达方式不同的查询非常有用。查询标签在连接标签或排序说明符之后提供。

带有查询标签的查询不需要提供结果。相反，具有相同标签的每个查询的结果将被相互比较。例如，以下脚本验证了查询 `SELECT 42+1` 和 `SELECT 44-1` 提供相同的结果：

```sql
query I nosort r43
SELECT 42+1;
----

query I nosort r43
SELECT 44-1;
----
```