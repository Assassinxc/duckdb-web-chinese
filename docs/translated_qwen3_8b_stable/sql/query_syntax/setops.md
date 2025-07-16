---
---
layout: docu
railroad: query_syntax/setops.js
redirect_from:
- /docs/sql/query_syntax/setops
title: 集合操作
---

集合操作允许根据 [集合操作语义](https://en.wikipedia.org/wiki/Set_(mathematics)#Basic_operations) 将查询进行组合。集合操作指的是 [`UNION [ALL]`](#union)、[`INTERSECT [ALL]`](#intersect) 和 [`EXCEPT [ALL]`](#except) 子句。基本变体使用集合语义，即它们会消除重复项，而带有 `ALL` 的变体使用多重集合语义。

传统集合操作通过 **列位置** 来统一查询，并要求要组合的查询具有相同数量的输入列。如果列的类型不同，可能会添加类型转换。结果将使用第一个查询的列名。

DuckDB 还支持 [`UNION [ALL] BY NAME`](#union-all-by-name)，它通过名称而不是位置来连接列。`UNION BY NAME` 不要求输入具有相同数量的列。在缺少列的情况下，会添加 `NULL` 值。

## `UNION`

`UNION` 子句可用于将多个查询的行进行组合。查询必须返回相同数量的列。[隐式转换](https://duckdb.org/docs/sql/data_types/typecasting#implicit-casting) 会执行到其中一种返回类型，以组合不同类型的列。如果无法完成此操作，`UNION` 子句将抛出错误。

### 基础 `UNION`（集合语义）

基础 `UNION` 子句遵循集合语义，因此会执行重复消除，即只有唯一的行将包含在结果中。

```sql
SELECT * FROM range(2) t1(x)
UNION
SELECT * FROM range(3) t2(x);
```

| x |
|--:|
| 2 |
| 1 |
| 0 |

### `UNION ALL`（多重集合语义）

`UNION ALL` 按多重集合语义返回两个查询的所有行，即 *不* 进行重复消除。

```sql
SELECT * FROM range(2) t1(x)
UNION ALL
SELECT * FROM range(3) t2(x);
```

| x |
|--:|
| 0 |
| 1 |
| 0 |
| 1 |
| 2 |

### `UNION [ALL] BY NAME`

`UNION [ALL] BY NAME` 子句可用于通过名称而不是位置将不同表的行进行组合。`UNION BY NAME` 不要求两个查询具有相同数量的列。任何只在其中一个查询中出现的列，在另一个查询中将填充为 `NULL` 值。

以下示例表：

```sql
CREATE TABLE capitals (city VARCHAR, country VARCHAR);
INSERT INTO capitals VALUES
    ('Amsterdam', 'NL'),
    ('Berlin', 'Germany');
CREATE TABLE weather (city VARCHAR, degrees INTEGER, date DATE);
INSERT INTO weather VALUES
    ('Amsterdam', 10, '2022-10-14'),
    ('Seattle', 8, '2022-10-12');
```

```sql
SELECT * FROM capitals
UNION BY NAME
SELECT * FROM weather;
```

|   city    | country | degrees |    date    |
|-----------|---------|--------:|------------|
| Seattle   | NULL    | 8       | 2022-10-12 |
| Amsterdam | NL      | NULL    | NULL       |
| Berlin    | Germany | NULL    | NULL       |
| Amsterdam | NULL    | 10      | 2022-10-14 |

`UNION BY NAME` 遵循集合语义（因此会进行重复消除），而 `UNION ALL BY NAME` 遵循多重集合语义。

## `INTERSECT`

`INTERSECT` 子句可用于选择同时出现在 **两个** 查询结果中的所有行。

### 基础 `INTERSECT`（集合语义）

基础 `INTERSECT` 会进行重复消除，因此只返回唯一的行。

```sql
SELECT * FROM range(2) t1(x)
INTERSECT
SELECT * FROM range(6) t2(x);
```

| x |
|--:|
| 0 |
| 1 |

### `INTERSECT ALL`（多重集合语义）

`INTERSECT ALL` 遵循多重集合语义，因此会返回重复项。

```sql
SELECT unnest([5, 5, 6, 6, 6, 6, 7, 8]) AS x
INTERSECT ALL
SELECT unnest([5, 6, 6, 7, 7, 9]);
```

| x |
|--:|
| 5 |
| 6 |
| 6 |
| 7 |

## `EXCEPT`

`EXCEPT` 子句可用于选择 **仅** 出现在左查询中的所有行。

### 基础 `EXCEPT`（集合语义）

基础 `EXCEPT` 遵循集合语义，因此会进行重复消除，只返回唯一的行。

```sql
SELECT * FROM range(5) t1(x)
EXCEPT
SELECT * FROM range(2) t2(x);
```

| x |
|--:|
| 2 |
| 3 |
| 4 |

### `EXCEPT ALL`（多重集合语义）

`EXCEPT ALL` 使用多重集合语义：

```sql
SELECT unnest([5, 5, 6, 6, 6, 6, 7, 8]) AS x
EXCEPT ALL
SELECT unnest([5, 6, 6, 7, 7, 9]);
```

| x |
|--:|
| 5 |
| 8 |
| 6 |
| 6 |

## 语法

<div id="rrdiagram"></div>