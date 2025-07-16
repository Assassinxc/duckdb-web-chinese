---
---
layout: docu
railroad: statements/setvariable.js
redirect_from:
- /docs/sql/statements/set_variable
title: SET VARIABLE 和 RESET VARIABLE 语句
---

DuckDB 支持使用 `SET VARIABLE` 和 `RESET VARIABLE` 语句定义 SQL 级别的变量。

## `SET VARIABLE`

`SET VARIABLE` 语句将值赋给变量，该变量可以通过 `getvariable` 调用来访问：

```sql
SET VARIABLE my_var = 30;
SELECT 20 + getvariable('my_var') AS total;
```

| total |
|------:|
| 50    |

如果对已有的变量调用 `SET VARIABLE`，它将覆盖该变量的值：

```sql
SET VARIABLE my_var = 30;
SET VARIABLE my_var = 100;
SELECT 20 + getvariable('my_var') AS total;
```

| total |
|------:|
| 120   |

变量可以有不同的类型：

```sql
SET VARIABLE my_date = DATE '2018-07-13';
SET VARIABLE my_string = 'Hello world';
SET VARIABLE my_map = MAP {'k1': 10, 'k2': 20};
```

变量也可以被赋值为查询的结果：

```sql
-- 写入一些 CSV 文件
COPY (SELECT 42 AS a) TO 'test1.csv';
COPY (SELECT 84 AS a) TO 'test2.csv';

-- 将 CSV 文件列表添加到表中
CREATE TABLE csv_files (file VARCHAR);
INSERT INTO csv_files VALUES ('test1.csv'), ('test2.csv');

-- 使用 CSV 文件列表初始化一个变量
SET VARIABLE list_of_files = (SELECT list(file) FROM csv_files);

-- 读取 CSV 文件
SELECT * FROM read_csv(getvariable('list_of_files'), filename := True);
```

| a    | filename    |
|-----:|------------:|
| 42   | test.csv    |
| 84   | test2.csv   |

如果变量未被设置，`getvariable` 函数将返回 `NULL`：

```sql
SELECT getvariable('undefined_var') AS result;
```

| result |
|--------|
| NULL   |

`getvariable` 函数也可以在 [`COLUMNS` 表达式]({% link docs/stable/sql/expressions/star.md %}#columns-expression) 中使用：

```sql
SET VARIABLE column_to_exclude = 'col1';
CREATE TABLE tbl AS SELECT 12 AS col0, 34 AS col1, 56 AS col2;
SELECT COLUMNS(c -> c != getvariable('column_to_exclude')) FROM tbl;
```

| col0 | col2 |
|-----:|-----:|
| 12   | 56   |

### 语法

<div id="rrdiagram1"></div>

## `RESET VARIABLE`

`RESET VARIABLE` 语句将变量取消设置。

```sql
SET VARIABLE my_var = 30;
RESET VARIABLE my_var;
SELECT getvariable('my_var') AS my_var;
```

| my_var |
|--------|
| NULL   |

### 语法

<div id="rrdiagram2"></div>

---