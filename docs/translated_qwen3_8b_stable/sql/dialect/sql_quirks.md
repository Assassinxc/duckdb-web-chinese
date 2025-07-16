---
---
layout: docu
redirect_from:
- /docs/sql/dialect/sql_quirks
title: SQL 特殊行为
---

与所有编程语言和库一样，DuckDB 也有其独特的怪癖和不一致之处。  
有些是由于我们“羽翼朋友”的进化遗留下来的；其他则是不可避免的，因为我们努力遵循 [SQL 标准](https://blog.ansi.org/sql-standard-iso-iec-9075-2023-ansi-x3-135/)，并特别遵循 PostgreSQL 的方言（有关例外情况，请参阅 [“PostgreSQL 兼容性”]({% link docs/stable/sql/dialect/postgresql_compatibility.md %}) 页面）。  
其余可能仅仅是由于不同的偏好，或者我们甚至可能已经达成共识，但只是尚未实施。

承认这些怪癖是我们能做的最好的事，这也是为什么我们整理了以下示例列表。

## 对空组的聚合

在空组上，聚合函数 `sum`、`list` 和 `string_agg` 都返回 `NULL`，而不是 `0`、`[]` 和 `''`。这是由 SQL 标准决定的，也是我们所知道的所有 SQL 实现都遵循的规则。这种行为被继承自列表聚合函数 [`list_sum`]({% link docs/stable/sql/functions/list.md %}#list_-rewrite-functions)，但不是 DuckDB 原生的 [`list_dot_product`]({% link docs/stable/sql/functions/list.md %}#list_dot_productlist1-list2)，后者在空列表上返回 `0`。

## 0 基索引 vs 1 基索引

为了符合标准 SQL，几乎所有地方都使用 1 基索引，例如数组和字符串索引和切片，以及窗口函数（`row_number`、`rank`、`dense_rank`）。  
然而，与 PostgreSQL 类似，[JSON 特性使用 0 基索引]({% link docs/stable/data/json/overview.md %}#indexing)。

## 类型

### `UINT8` vs. `INT8`

`UINT8` 和 `INT8` 是不同宽度整数类型的别名：

* `UINT8` 对应 `UTINYINT`，因为它是一个 8 位无符号整数  
* `INT8` 对应 `BIGINT`，因为它是一个 8 字节有符号整数  

解释：在数值类型 `INTn` 和 `UINTn` 中，`n` 表示数值的位数或字节数。  
`INT1`、`INT2`、`INT4` 对应字节数，而 `INT16`、`INT32` 和 `INT64` 对应位数。  
`UINT` 值也适用相同规则。  
然而，`n = 8` 可以表示位数或字节数。  
对于无符号值，`UINT8` 对应 `UTINYINT`（8 位）。  
对于有符号值，`INT8` 对应 `BIGINT`（8 字节）。

## 表达式

### 可能令人惊讶的结果

<!-- markdownlint-disable MD056 -->

| 表达式                  | 结果  | 说明                                                                          |
|-------------------------|-------|-------------------------------------------------------------------------------|
| `-2^2`                  | `4.0` | PostgreSQL 兼容性意味着一元减号的优先级高于指数运算符。使用额外的括号，例如 `-(2^2)` 或 [`pow` 函数]({% link docs/stable/sql/functions/numeric.md %}#powx-y)，例如 `-pow(2, 2)`，以避免错误。 |
| `'t' = true`            | `true` | 与 PostgreSQL 兼容。                                                         |
| `1 = '1'`               | `true` | 与 PostgreSQL 兼容。                                                         |
| `1 = ' 1'`              | `true` | 与 PostgreSQL 兼容。                                                         |
| `1 = '01'`              | `true` | 与 PostgreSQL 兼容。                                                         |
| `1 = ' 01 '`            | `true` | 与 PostgreSQL 兼容。                                                         |
| `1 = true`              | `true` | 不兼容 PostgreSQL。                                                         |
| `1 = '1.1'`             | `true` | 不兼容 PostgreSQL。                                                         |
| `1 IN (0, NULL)`        | `NULL` | 如果将输入和输出中的 `NULL` 视为 `UNKNOWN`，则这是合理的。                   |
| `1 in [0, NULL]`        | `false` |                                                                               |
| `concat('abc', NULL)`   | `abc`  | 与 PostgreSQL 兼容。`list_concat` 的行为类似。                               |
| `'abc' || NULL`         | `NULL` |                                                                               |

<!-- markdownlint-enable MD056 -->

### `NaN` 值

`'NaN'::FLOAT = 'NaN'::FLOAT` 和 `'NaN'::FLOAT > 3` 违反 IEEE-754，但意味着浮点数据类型具有一个全序，就像其他所有数据类型一样（注意 `greatest` / `least` 的后果）。

### `age` 函数

`age(x)` 是 `current_date - x` 而不是 `current_timestamp - x`。这是从 PostgreSQL 继承的另一个怪癖。

### 提取函数

`list_extract` / `map_extract` 在不存在的键上返回 `NULL`。`struct_extract` 会抛出错误，因为结构体的键类似于列。

## 子句

### `SELECT` 中的自动列去重

列名通过首次出现的名称进行去重，后续的名称被覆盖：

```sql
CREATE TABLE tbl AS SELECT 1 AS a;
SELECT a FROM (SELECT *, 2 AS a FROM tbl);
```

| a |
|--:|
| 1 |

### `SELECT` 列时的大小写不敏感

由于大小写不敏感，当 `file.parquet` 中的列 `A` 在所需列 `a` 之前出现时，无法使用 `SELECT a FROM 'file.parquet'`。

### `USING SAMPLE`

`USING SAMPLE` 子句在语法上位于 `WHERE` 和 `GROUP BY` 子句之后（与 `LIMIT` 子句相同），但在语义上在两者之前应用（与 `LIMIT` 子句不同）。