---
---
layout: docu
redirect_from:
- /docs/sql/query_syntax/prepared_statements
title: 预编译语句
---

DuckDB 支持预编译语句，其中参数在查询执行时进行替换。
这可以提高可读性，并有助于防止 [SQL 注入](https://en.wikipedia.org/wiki/SQL_injection)。

## 语法

预编译语句中表示参数有三种语法：
自动递增 (`?`),
位置参数 (`$1`),
以及命名参数 (`$param`)。
请注意，并非所有客户端都支持所有这些语法，例如，[JDBC 客户端]({% link docs/stable/clients/java.md %}) 仅支持预编译语句中的自动递增参数。

### 示例数据集

以下内容介绍了三种不同的语法，并使用以下表格进行示例说明。

```sql
CREATE TABLE person (name VARCHAR, age BIGINT);
INSERT INTO person VALUES ('Alice', 37), ('Ana', 35), ('Bob', 41), ('Bea', 25);
```

在我们的示例查询中，我们将查找名字以 `B` 开头且年龄至少为 40 岁的人。
这将返回一行结果 `<'Bob', 41>`。

### 自动递增参数: `?`

DuckDB 支持使用带有自动递增索引的预编译语句，
即，查询中的参数位置与其在执行语句中的位置相对应。
例如：

```sql
PREPARE query_person AS
    SELECT *
    FROM person
    WHERE starts_with(name, ?)
      AND age >= ?;
```

使用 CLI 客户端，执行语句如下。

```sql
EXECUTE query_person('B', 40);
```

### 位置参数: `$1`

预编译语句可以使用位置参数，参数通过整数表示 (`$1`, `$2`)。
例如：

```sql
PREPARE query_person AS
    SELECT *
    FROM person
    WHERE starts_with(name, $2)
      AND age >= $1;
```

使用 CLI 客户端，执行语句如下。
请注意，第一个参数对应 `$1`，第二个对应 `$2`，依此类推。

```sql
EXECUTE query_person(40, 'B');
```

### 命名参数: `$parameter`

DuckDB 也支持命名参数，其中参数通过 `$parameter_name` 表示。
例如：

```sql
PREPARE query_person AS
    SELECT *
    FROM person
    WHERE starts_with(name, $name_start_letter)
      AND age >= $minimum_age;
```

使用 CLI 客户端，执行语句如下。

```sql
EXECUTE query_person(name_start_letter := 'B', minimum_age := 40);
```

## 删除预编译语句: `DEALLOCATE`

要删除预编译语句，请使用 `DEALLOCATE` 语句：

```sql
DEALLOCATE query_person;
```

或者使用：

```sql
DEALLOCATE PREPARE query_person;
```