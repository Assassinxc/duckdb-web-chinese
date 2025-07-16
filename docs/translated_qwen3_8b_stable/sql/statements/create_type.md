---
---
layout: docu
railroad: statements/createtype.js
redirect_from:
- /docs/sql/statements/create_type
title: CREATE TYPE 语句
---

`CREATE TYPE` 语句在目录中定义一个新的类型。

## 示例

创建一个简单的 `ENUM` 类型：

```sql
CREATE TYPE mood AS ENUM ('happy', 'sad', 'curious');
```

创建一个简单的 `STRUCT` 类型：

```sql
CREATE TYPE many_things AS STRUCT(k INTEGER, l VARCHAR);
```

创建一个简单的 `UNION` 类型：

```sql
CREATE TYPE one_thing AS UNION(number INTEGER, string VARCHAR);
```

创建一个类型别名：

```sql
CREATE TYPE x_index AS INTEGER;
```

## 语法

<div id="rrdiagram"></div>

`CREATE TYPE` 子句定义了一个新数据类型，该类型可用于此 DuckDB 实例。
这些新类型随后可以在 [`duckdb_types` 表]({% link docs/stable/sql/meta/duckdb_table_functions.md %}#duckdb_types) 中进行检查。

## 局限性

* 通过纯 SQL 无法扩展类型以支持自定义运算符（例如 PostgreSQL 的 `&&` 运算符）。
  而是需要添加额外的 C++ 代码。要实现这一点，请创建一个 [扩展]({% link docs/stable/core_extensions/overview.md %}).

* `CREATE TYPE` 子句不支持 `OR REPLACE` 修改符。