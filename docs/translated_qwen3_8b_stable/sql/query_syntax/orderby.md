---
---
layout: docu
railroad: query_syntax/orderby.js
redirect_from:
- /docs/sql/query_syntax/orderby
title: ORDER BY 子句
---

`ORDER BY` 是一个输出修饰符。逻辑上，它是在查询的最后一步（在 [`LIMIT`]({% link docs/stable/sql/query_syntax/limit.md %}) 或 [`OFFSET`]({% link docs/stable/sql/query_syntax/limit.md %}) 之前，如果存在的话）应用的。
`ORDER BY` 子句根据排序条件对行进行升序或降序排序。
此外，每个排序子句都可以指定 `NULL` 值是否应排在最前面或最后面。

`ORDER BY` 子句可能包含一个或多个表达式，用逗号分隔。
如果没有包含表达式，将抛出错误，因为在这种情况下应删除 `ORDER BY` 子句。
这些表达式可以以任意标量表达式（可以是列名）开头，也可以是列位置数字（索引从 1 开始），或者关键字 `ALL`。
每个表达式可以可选地后跟一个排序修饰符（`ASC` 或 `DESC`，默认是 `ASC`），以及/或一个 `NULL` 排序修饰符（`NULLS FIRST` 或 `NULLS LAST`，默认是 `NULLS LAST`）。

## `ORDER BY ALL`

`ALL` 关键字表示应按照从左到右的顺序对所有列进行排序。
可以使用 `ORDER BY ALL ASC` 或 `ORDER BY ALL DESC` 和/或 `NULLS FIRST` 或 `NULLS LAST` 来修改此排序的方向。
请注意，`ALL` 不能与其他 `ORDER BY` 子句中的表达式一起使用 – 它必须单独使用。
请参见下面的示例。

## `NULL` 排序修饰符

默认情况下，DuckDB 以 `ASC` 和 `NULLS LAST` 排序，即值按升序排序，`NULL` 值放在最后。
这与 PostgreSQL 的默认排序顺序相同。
可以通过以下配置选项更改默认排序顺序。

使用 `default_null_order` 选项更改默认的 `NULL` 排序顺序为 `NULLS_FIRST`、`NULLS_LAST`、`NULLS_FIRST_ON_ASC_LAST_ON_DESC` 或 `NULLS_LAST_ON_ASC_FIRST_ON_DESC`：

```sql
SET default_null_order = 'NULLS_FIRST';
```

使用 `default_order` 更改默认排序顺序的方向为 `DESC` 或 `ASC`：

```sql
SET default_order = 'DESC';
```

## 排序规则

默认情况下，文本使用二进制比较排序规则进行排序，这意味着值根据其二进制 UTF-8 值进行排序。
虽然这对于 ASCII 文本（例如英语数据）效果很好，但对于其他语言的排序顺序可能不正确。
为此，DuckDB 提供了排序规则。
有关排序规则的更多信息，请参阅 [排序规则页面]({% link docs/stable/sql/expressions/collations.md %}）。

## 示例

所有示例都使用以下示例表：

```sql
CREATE OR REPLACE TABLE addresses AS
    SELECT '123 Quack Blvd' AS address, 'DuckTown' AS city, '11111' AS zip
    UNION ALL
    SELECT '111 Duck Duck Goose Ln', 'DuckTown', '11111'
    UNION ALL
    SELECT '111 Duck Duck Goose Ln', 'Duck Town', '11111'
    UNION ALL
    SELECT '111 Duck Duck Goose Ln', 'Duck Town', '11111-0001';
```

按城市名称选择地址，使用默认的 `NULL` 排序和默认排序：

```sql
SELECT *
FROM addresses
ORDER BY city;
```

按城市名称选择地址，降序排列，`NULL` 值排在最后：

```sql
SELECT *
FROM addresses
ORDER BY city DESC NULLS LAST;
```

按城市和邮编排序，均使用默认排序：

```sql
SELECT *
FROM addresses
ORDER BY city, zip;
```

按城市名称使用德国排序规则进行排序：

```sql
SELECT *
FROM addresses
ORDER BY city COLLATE DE;
```

### `ORDER BY ALL` 示例

按从左到右的顺序（按地址、城市、邮编）升序排列：

```sql
SELECT *
FROM addresses
ORDER BY ALL;
```

|        address         |   city    |    zip     |
|------------------------|-----------|------------|
| 111 Duck Duck Goose Ln | Duck Town | 11111      |
| 111 Duck Duck Goose Ln | Duck Town | 11111-0001 |
| 111 Duck Duck Goose Ln | DuckTown  | 11111      |
| 123 Quack Blvd         | DuckTown  | 11111      |

按从左到右的顺序（按地址、城市、邮编）降序排列：

```sql
SELECT *
FROM addresses
ORDER BY ALL DESC;
```

|        address         |   city    |    zip     |
|------------------------|-----------|------------|
| 123 Quack Blvd         | DuckTown  | 11111      |
| 111 Duck Duck Goose Ln | DuckTown  | 11111      |
| 111 Duck Duck Goose Ln | Duck Town | 11111-0001 |
| 111 Duck Duck Goose Ln | Duck Town | 11111      |

## 语法

<div id="rrdiagram"></div>