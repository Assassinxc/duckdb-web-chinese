---
---
layout: docu
redirect_from:
- /docs/sql/data_types/typecasting
title: 类型转换
---

类型转换是一种将特定数据类型中的值转换为另一种数据类型中最接近的对应值的操作。
与其他 SQL 引擎一样，DuckDB 支持显式和隐式类型转换。

## 显式转换

显式类型转换通过使用 `CAST` 表达式进行。例如，`CAST(col AS VARCHAR)` 或 `col::VARCHAR` 显式地将列 `col` 转换为 `VARCHAR`。更多信息请参阅 [cast 页面]({% link docs/stable/sql/expressions/cast.md %}）。

## 隐式转换

在许多情况下，系统会自动添加类型转换。这称为 *隐式* 转换，例如，当调用一个函数时，如果参数与函数的类型不匹配，但可以转换为所需类型时，就会发生这种情况。

隐式转换只能在某些类型组合之间进行，并且通常只有在转换不会失败时才可能发生。例如，可以将 `INTEGER` 隐式转换为 `DOUBLE`，但不能将 `DOUBLE` 隐式转换为 `INTEGER`。

考虑函数 `sin(DOUBLE)`。该函数的输入参数是一个 `DOUBLE` 类型的列，但也可以使用整数调用：`sin(1)`。整数在传递给 `sin` 函数之前会被转换为双精度浮点数。

> 提示 要检查一种类型是否可以隐式转换为另一种类型，请使用 [`can_cast_implicitly` 函数]({% link docs/stable/sql/functions/utility.md %}#can_cast_implicitlysource_value-target_value)。

### 组合转换

当不同类型的值需要组合成一个未指定的父类型时，系统会执行隐式转换以自动选择父类型。例如，`list_value(1::INT64, 1::UINT64)` 会创建一个 `INT128[]` 类型的列表。在这种情况下执行的隐式转换有时比常规隐式转换更加宽松。例如，即使常规隐式转换无法进行，`BOOL` 值也可以转换为 `INT`（`true` 映射为 `1`，`false` 映射为 `0`）。

这种 *组合转换* 用于比较 (`=` / `<` / `>`)、集合操作 (`UNION` / `EXCEPT` / `INTERSECT`) 和嵌套类型构造器 (`list_value` / `[...]` / `MAP`)。

## 转换操作矩阵

特定数据类型的值不能总是转换为任意目标数据类型。唯一的例外是 `NULL` 值——它可以始终在不同类型之间进行转换。
以下矩阵描述了哪些转换是支持的。
如果允许隐式转换，则也意味着显式转换是可能的。

![类型转换矩阵](/images/typecasting-matrix.png)

即使基于源和目标数据类型支持转换操作，也不意味着在运行时转换操作一定会成功。

> 已弃用 在版本 0.10.0 之前，DuckDB 允许在函数绑定期间将任何类型隐式转换为 `VARCHAR`。
> 版本 0.10.0 引入了一个 [破坏性变更，不再允许隐式转换到 `VARCHAR`]({% post_url 2024-02-13-announcing-duckdb-0100 %}#breaking-sql-changes)。
> 可以使用 [`old_implicit_casting` 配置选项]({% link docs/stable/configuration/pragmas.md %}#implicit-casting-to-varchar) 来恢复旧的行为。
> 请注意，此标志将在未来被弃用。

### 损失性转换

导致精度丢失的转换操作是允许的。例如，可以显式地将带有小数位的数值类型（如 `DECIMAL`、`FLOAT` 或 `DOUBLE`）转换为整数类型（如 `INTEGER` 或 `BIGINT`）。数值将被四舍五入。

```sql
SELECT CAST(3.1 AS INTEGER);  -- 3
SELECT CAST(3.5 AS INTEGER);  -- 4
SELECT CAST(-1.7 AS INTEGER); -- -2
```

### 溢出

导致值溢出的转换操作会抛出错误。例如，值 `999` 超出了 `TINYINT` 数据类型的表示范围。因此，尝试将该值转换为该类型会导致运行时错误：

```sql
SELECT CAST(999 AS TINYINT);
```

```console
转换错误：
类型 INT32 值 999 无法转换，因为值超出目标类型 INT8 的范围
```

因此，尽管从 `INTEGER` 到 `TINYINT` 的转换操作是支持的，但对于这个特定值却无法进行。[TRY_CAST]({% link docs/stable/sql/expressions/cast.md %}) 可以将值转换为 `NULL` 而不是抛出错误。

### VARCHAR

[`VARCHAR`]({% link docs/stable/sql/data_types/text.md %}) 类型充当通用目标：任何任意类型的任意值都可以始终转换为 `VARCHAR` 类型。该类型也用于在 shell 中显示值。

```sql
SELECT CAST(42.5 AS VARCHAR);
```

从 `VARCHAR` 转换到其他数据类型是支持的，但如果 DuckDB 无法解析并转换提供的文本为目标数据类型，则可能在运行时引发错误。

```sql
SELECT CAST('NotANumber' AS INTEGER);
```

通常，将值转换为 `VARCHAR` 是无损操作，任何类型都可以在转换为文本后恢复为原始类型。

```sql
SELECT CAST(CAST([1, 2, 3] AS VARCHAR) AS INTEGER[]);
```

### 字面量类型

整数字面量（如 `42`）和字符串字面量（如 `'string'`）具有特殊的隐式转换规则。更多信息请参阅 [字面量类型页面]({% link docs/stable/sql/data_types/literal_types.md %}）。

### 列表 / 数组

列表可以通过相同的转换规则显式转换为其他列表。转换应用于列表的子元素。例如，如果我们把一个 `INTEGER[]` 列表转换为一个 `VARCHAR[]` 列表，那么列表中的每个 `INTEGER` 元素都会被单独转换为 `VARCHAR`，并构造一个新的列表。

```sql
SELECT CAST([1, 2, 3] AS VARCHAR[]);
```

### 数组

数组遵循与列表相同的转换规则。此外，数组可以隐式转换为相同类型的列表。例如，一个 `INTEGER[3]` 数组可以隐式转换为一个 `INTEGER[]` 列表。

### 结构体

只要结构体之间至少共享一个字段，结构体就可以转换为其他结构体。

> 这个要求的目的是为了避免意外的错误。如果两个结构体没有任何共同的字段，那么转换可能是不打算的。

```sql
SELECT CAST({'a': 42} AS STRUCT(a VARCHAR));
```

目标结构体中存在的但源结构体中不存在的字段默认为 `NULL`。

```sql
SELECT CAST({'a': 42} AS STRUCT(a VARCHAR, b VARCHAR));
```

仅存在于源结构体中的字段将被忽略。

```sql
SELECT CAST({'a': 42, 'b': 43} AS STRUCT(a VARCHAR));
```

结构体的字段名称顺序也可以不同。结构体的字段将根据结构体的名称重新排列。

```sql
SELECT CAST({'a': 42, 'b': 84} AS STRUCT(b VARCHAR, a VARCHAR));
```

当结构体转换与 [`UNION [ALL] BY NAME`]({% link docs/stable/sql/query_syntax/setops.md %}#union-all-by-name) 操作结合使用时，结构体转换的行为会有所不同。
在这种情况下，结果结构体的字段是所有输入结构体字段的超集。
这种逻辑也递归地适用于潜在的嵌套结构体。

```sql
SELECT {'outer1': {'inner1': 42, 'inner2': 42}} AS c
UNION ALL BY NAME 
SELECT {'outer1': {'inner2': 'hello', 'inner3': 'world'}, 'outer2': '100'} AS c;
```

```sql
SELECT [{'a': 42}, {'b': 84}];
```

### 联合类型

联合类型转换规则请参阅 [`UNION 类型页面`]({% link docs/stable/sql/data_types/union.md %}#casting-to-unions)。