blurb: FROM 子句可以包含一个表、多个通过 JOIN 子句连接在一起的表的组合，或者一个子查询节点中的另一个 SELECT 查询。
layout: docu
railroad: query_syntax/from.js
redirect_from:
- /docs/sql/query_syntax/from
title: FROM 和 JOIN 子句

`FROM` 子句指定了查询其余部分应操作的数据*来源*。逻辑上，`FROM` 子句是查询开始执行的地方。`FROM` 子句可以包含一个表、多个通过 `JOIN` 子句连接在一起的表的组合，或者一个子查询节点中的另一个 `SELECT` 查询。DuckDB 还支持一个可选的 `FROM`-first 语法，使您能够在不使用 `SELECT` 语句的情况下进行查询。

## 示例

从名为 `table_name` 的表中选择所有列：

```sql
SELECT *
FROM table_name;
```

使用 `FROM`-first 语法从表中选择所有列：

```sql
FROM table_name
SELECT *;
```

使用 `FROM`-first 语法选择所有列并省略 `SELECT` 子句：

```sql
FROM table_name;
```

从名为 `table_name` 的表中通过别名 `tn` 选择所有列：

```sql
SELECT tn.*
FROM table_name tn;
```

使用前缀别名：

```sql
SELECT tn.*
FROM tn: table_name;
```

从名为 `schema_name` 的模式中的表 `table_name` 中选择所有列：

```sql
SELECT *
FROM schema_name.table_name;
```

从表函数 `range` 中选择列 `i`，其中范围函数的第一个列被重命名为 `i`：

```sql
SELECT t.i
FROM range(100) AS t(i);
```

从名为 `test.csv` 的 CSV 文件中选择所有列：

```sql
SELECT *
FROM 'test.csv';
```

从子查询中选择所有列：

```sql
SELECT *
FROM (SELECT * FROM table_name);
```

将表的整行作为结构体选择：

```sql
SELECT t
FROM t;
```

将子查询的整行作为结构体选择（即，一个列）：

```sql
SELECT t
FROM (SELECT unnest(generate_series(41, 43)) AS x, 'hello' AS y) t;
```

将两个表连接在一起：

```sql
SELECT *
FROM table_name
JOIN other_table
  ON table_name.key = other_table.key;
```

从表中选择 10% 的样本：

```sql
SELECT *
FROM table_name
TABLESAMPLE 10%;
```

从表中选择 10 行的样本：

```sql
SELECT *
FROM table_name
TABLESAMPLE 10 ROWS;
```

使用 `FROM`-first 语法与 `WHERE` 子句和聚合：

```sql
FROM range(100) AS t(i)
SELECT sum(t.i)
WHERE i % 2 = 0;
```

## 连接

连接是用于水平连接两个表或关系的基本关系操作。
关系被称为连接的 _左_ 和 _右_ 侧，这取决于它们在连接子句中的写法。
每行结果包含两个关系的列。

连接使用一个规则来匹配每个关系中的行对。
通常这是一个谓词，但还可能有其他隐含规则。

### 外连接

如果指定了 `OUTER` 连接，即使没有匹配的行也可以返回。
外连接可以是以下之一：

* `LEFT`（左关系的所有行至少出现一次）
* `RIGHT`（右关系的所有行至少出现一次）
* `FULL`（两个关系的所有行至少出现一次）

不是 `OUTER` 的连接是 `INNER`（仅返回配对的行）。

当返回未配对的行时，其他表的属性将设置为 `NULL`。

### 笛卡尔积连接

最简单的连接类型是 `CROSS JOIN`。
这种连接没有条件，
它只返回所有可能的配对。

返回所有行对：

```sql
SELECT a.*, b.*
FROM a
CROSS JOIN b;
```

这等同于省略 `JOIN` 子句：

```sql
SELECT a.*, b.*
FROM a, b;
```

### 条件连接

大多数连接由一个将一侧属性与另一侧属性连接的谓词指定。
条件可以使用 `ON` 子句显式指定（更清晰）或通过 `WHERE` 子句隐含指定（旧式）。

我们使用 TPC-H 模式中的 `l_regions` 和 `l_nations` 表：

```sql
CREATE TABLE l_regions (
    r_regionkey INTEGER NOT NULL PRIMARY KEY,
    r_name      CHAR(25) NOT NULL,
    r_comment   VARCHAR(152)
);

CREATE TABLE l_nations (
    n_nationkey INTEGER NOT NULL PRIMARY KEY,
    n_name      CHAR(25) NOT NULL,
    n_regionkey INTEGER NOT NULL,
    n_comment   VARCHAR(152),
    FOREIGN KEY (n_regionkey) REFERENCES l_regions(r_regionkey)
);
```

返回国家的地区：

```sql
SELECT n.*, r.*
FROM l_nations n
JOIN l_regions r ON (n_regionkey = r_regionkey);
```

如果列名相同且需要相等，则可以使用更简单的 `USING` 语法：

```sql
CREATE TABLE l_regions (regionkey INTEGER NOT NULL PRIMARY KEY,
                        name      CHAR(25) NOT NULL,
                        comment   VARCHAR(152));

CREATE TABLE l_nations (nationkey INTEGER NOT NULL PRIMARY KEY,
                        name      CHAR(25) NOT NULL,
                        regionkey INTEGER NOT NULL,
                        comment   VARCHAR(152),
                        FOREIGN KEY (regionkey) REFERENCES l_regions(regionkey));
```

返回国家的地区：

```sql
SELECT n.*, r.*
FROM l_nations n
JOIN l_regions r USING (regionkey);
```

表达式不一定要相等，可以使用任何谓词：

返回一对任务，其中一项运行时间更长但成本更低：

```sql
SELECT s1.t_id, s2.t_id
FROM west s1, west s2
WHERE s1.time > s2.time
  AND s1.cost < s2.cost;
```

### 自然连接

自然连接基于具有相同名称的属性连接两个表。

例如，考虑以下带有城市、机场代码和机场名称的示例。请注意，这两个表都故意不完整，即它们在另一个表中没有匹配的对。

```sql
CREATE TABLE city_airport (city_name VARCHAR, iata VARCHAR);
CREATE TABLE airport_names (iata VARCHAR, airport_name VARCHAR);
INSERT INTO city_airport VALUES
    ('Amsterdam', 'AMS'),
    ('Rotterdam', 'RTM'),
    ('Eindhoven', 'EIN'),
    ('Groningen', 'GRQ');
INSERT INTO airport_names VALUES
    ('AMS', 'Amsterdam Airport Schiphol'),
    ('RTM', 'Rotterdam The Hague Airport'),
    ('MST', 'Maastricht Aachen Airport');
```

要通过它们共享的 [`IATA`](https://en.wikipedia.org/wiki/IATA_airport_code) 属性连接这些表，请运行：

```sql
SELECT *
FROM city_airport
NATURAL JOIN airport_names;
```

这将产生以下结果：

| city_name | iata |        airport_name         |
|-----------|------|-----------------------------|
| Amsterdam | AMS  | Amsterdam Airport Schiphol  |
| Rotterdam | RTM  | Rotterdam The Hague Airport |

请注意，只有在两个表中都存在相同的 `iata` 属性的行才会包含在结果中。

我们也可以使用普通的 `JOIN` 子句和 `USING` 关键字表达查询：

```sql
SELECT *
FROM city_airport
JOIN airport_names
USING (iata);
```

### 半连接和反连接

半连接返回左表中至少在右表中有一个匹配的行。
反连接返回左表中在右表中没有任何匹配的行。
使用半连接或反连接时，结果中的行数永远不会超过左侧表的行数。
半连接提供了与 [`IN` 操作符]({% link docs/stable/sql/expressions/in.md %}) 语句相同的逻辑。
反连接提供了与 `NOT IN` 操作符相同的逻辑，但反连接会忽略右表中的 `NULL` 值。

#### 半连接示例

从 `city_airport` 表中返回城市-机场代码对列表，其中机场名称在 `airport_names` 表中存在：

```sql
SELECT *
FROM city_airport
SEMI JOIN airport_names
    USING (iata);
```

| city_name | iata |
|-----------|------|
| Amsterdam | AMS  |
| Rotterdam | RTM  |

这个查询等同于：

```sql
SELECT *
FROM city_airport
WHERE iata IN (SELECT iata FROM airport_names);
```

#### 反连接示例

从 `city_airport` 表中返回城市-机场代码对列表，其中机场名称在 `airport_names` 表中不存在：

```sql
SELECT *
FROM city_airport
ANTI JOIN airport_names
    USING (iata);
```

| city_name | iata |
|-----------|------|
| Eindhoven | EIN  |
| Groningen | GRQ  |

这个查询等同于：

```sql
SELECT *
FROM city_airport
WHERE iata NOT IN (SELECT iata FROM airport
```

### 侧向连接

`LATERAL` 关键字允许在 `FROM` 子句中的子查询引用前面的子查询。此功能也称为 _侧向连接_。

```sql
SELECT *
FROM range(3) t(i), LATERAL (SELECT i + 1) t2(j);
```

<div class="center_aligned_header_table"></div>

| i | j |
|--:|--:|
| 0 | 1 |
| 2 | 3 |
| 1 | 2 |

侧向连接是相关子查询的一般化，因为它们可以返回每个输入值的多个值，而不仅仅是单个值。

```sql
SELECT *
FROM
    generate_series(0, 1) t(i),
    LATERAL (SELECT i + 10 UNION ALL SELECT i + 100) t2(j);
```

<div class="center_aligned_header_table"></div>

| i |  j  |
|--:|----:|
| 0 | 10  |
| 1 | 11  |
| 0 | 100 |
| 1 | 101 |

将 `LATERAL` 视为一个循环可能会有所帮助，我们在第一个子查询的行上进行迭代，并将其作为第二个（`LATERAL`）子查询的输入。
在上面的例子中，我们迭代表 `t` 并从表 `t2` 的定义中引用其列 `i`。表 `t2` 的行形成结果中的列 `j`。

可以引用多个 `LATERAL` 子查询的属性。使用第一个示例中的表：

```sql
CREATE TABLE t1 AS
    SELECT *
    FROM range(3) t(i), LATERAL (SELECT i + 1) t2(j);

SELECT *
    FROM t1, LATERAL (SELECT i + j) t2(k)
    ORDER BY ALL;
```

<div class="center_aligned_header_table"></div>

| i | j | k |
|--:|--:|--:|
| 0 | 1 | 1 |
| 1 | 2 | 3 |
| 2 | 3 | 5 |

> DuckDB 会检测何时应使用 `LATERAL` 连接，因此 `LATERAL` 关键字的使用是可选的。

### 位置连接

在处理大小相同的 DataFrame 或其他嵌入表时，行可能基于其物理顺序有自然的对应关系。
在脚本语言中，这可以通过循环轻松表达：

```cpp
for (i = 0; i < n; i++) {
    f(t1.a[i], t2.b[i]);
}
```

在标准 SQL 中表达这一点比较困难，因为关系表是无序的，但导入表如 [DataFrame]({% link docs/stable/clients/python/data_ingestion.md %}#pandas-dataframes-–-object-columns)
或磁盘文件（如 [CSV]({% link docs/stable/data/csv/overview.md %}) 或 [Parquet 文件]({% link docs/stable/data/parquet/overview.md %})) 有自然顺序。

使用这种顺序连接它们称为 _位置连接_：

```sql
CREATE TABLE t1 (x INTEGER);
CREATE TABLE t2 (s VARCHAR);

INSERT INTO t1 VALUES (1), (2), (3);
INSERT INTO t2 VALUES ('a'), ('b');

SELECT *
FROM t1
POSITIONAL JOIN t2;
```

<div class="center_aligned_header_table"></div>

| x |  s   |
|--:|------|
| 1 | a    |
| 2 | b    |
| 3 | NULL |

位置连接始终是 `FULL OUTER` 连接，即缺失值（较短列的最后值）设置为 `NULL`。

### 作为-为连接

在处理时间序列或类似顺序数据时，常见的操作是找到参考表（如价格）中的最近（第一个）事件。
这称为 _作为-为连接_：

将价格附加到股票交易：

```sql
SELECT t.*, p.price
FROM trades t
ASOF JOIN prices p
       ON t.symbol = p.symbol AND t.when >= p.when;
```

`ASOF` 连接至少需要一个对排序字段的不等条件。
不等条件可以是任何不等式条件（`>=`, `>`, `<=`, `<`）在任何数据类型上，但最常见的形式是 `>=` 在时间类型上。
任何其他条件必须是等式（或 `NOT DISTINCT`）。
这意味着表的左右顺序是有意义的。

`ASOF` 将每个左表行与最多一个右表行进行连接。
它可以指定为 `OUTER` 连接以查找未配对的行
（例如，没有价格的交易或没有交易的价格。）

将价格或 NULL 附加到股票交易：

```sql
SELECT *
FROM trades t
ASOF LEFT JOIN prices p
            ON t.symbol = p.symbol
           AND t.when >= p.when;
```

`ASOF` 连接还可以使用 `USING` 语法指定匹配的列名，
但列表中的最后一个属性必须是不等式，
这将大于或等于（`>=`）：

```sql
SELECT *
FROM trades t
ASOF JOIN prices p USING (symbol, "when");
```

返回符号、交易.when、价格（但 NOT prices.when）：

如果您将 `USING` 与 `SELECT *` 结合使用，
查询将返回匹配的左侧（探针）列值，
而不是右侧（构建）列值。
要获取示例中的 `prices` 时间，
您需要显式列出列：

```sql
SELECT t.symbol, t.when AS trade_when, p.when AS price_when, price
FROM trades t
ASOF LEFT JOIN prices p USING (symbol, "when");
```

### 自连接

DuckDB 允许所有类型的自连接。
请注意，表需要使用别名，使用相同的表名而不使用别名会导致错误：

```sql
CREATE TABLE t (x INTEGER);
SELECT * FROM t JOIN t USING(x);
```

```console
Binder 错误：
查询中重复的别名 "t"!
```

添加别名后，查询可以成功解析：

```sql
SELECT * FROM t AS t t1 JOIN t t2 USING(x);
```

### `JOIN` 子句中的简写

您可以在 `JOIN` 子句中指定列名：

```sql
CREATE TABLE t1 (x INTEGER);
CREATE TABLE t2 (y INTEGER);
INSERT INTO t1 VALUES (1), (2), (4);
INSERT INTO t2 VALUES (2), (3);
SELECT * FROM t1 NATURAL JOIN t2 t2(x);
```

| x |
|--:|
| 2 |

您也可以在 `JOIN` 子句中使用 `VALUES` 子句：

```sql
SELECT * FROM t1 NATURAL JOIN (VALUES (2), (4)) _(x);
```

| x |
|--:|
| 2 |
| 4 |

## `FROM`-First 语法

DuckDB 的 SQL 支持 `FROM`-first 语法，即允许将 `FROM` 子句放在 `SELECT` 子句之前，或者完全省略 `SELECT` 子句。我们使用以下示例来演示它：

```sql
CREATE TABLE tbl AS
    SELECT *
    FROM (VALUES ('a'), ('b')) t1(s), range(1, 3) t2(i);
```

### 带有 `SELECT` 子句的 `FROM`-First 语法

以下语句演示了 `FROM`-First 语法的使用：

```sql
FROM tbl
SELECT i, s;
```

这等同于：

```sql
SELECT i, s
FROM tbl;
```

<div class="center_aligned_header_table"></div>

| i | s |
|--:|---|
| 1 | a |
| 2 | a |
| 1 | b |
| 2 | b |

### 不带 `SELECT` 子句的 `FROM`-First 语法

以下语句演示了可选的 `SELECT` 子句的使用：

```sql
FROM tbl;
```

这等同于：

```sql
SELECT *
FROM tbl;
```

<div class="center_aligned_header_table"></div>

| s | i |
|---|--:|
| a | 1 |
| a | 2 |
| b | 1 |
| b | 2 |

## 使用 `AT` 实现时间旅行

DuckDB v1.3.0 引入了对 [时间旅行查询](https://docs.snowflake.com/en/user-guide/data-time-travel) 的支持，这些查询可以用于数据湖格式，如
[Delta]({% link docs/stable/core_extensions/delta.md %}),
[DuckLake]({% link docs/stable/core_extensions/ducklake.md %}) 和
[Iceberg]({% link docs/stable/core_extensions/iceberg/overview.md %}).

要指定时间旅行查询，请在 `FROM` 子句中使用 `AT` 修饰符。
时间旅行查询可以使用版本号或使用
`VERSION => ⟨version⟩`{:.language-sql .highlight}
和
`TIMESTAMP => ⟨timestamp or date⟩`{:.language-sql .highlight}
分别指定的 timestamp。例如：

```sql
FROM my_ducklake.demo AT (VERSION => 2);
FROM my_ducklake.demo AT (TIMESTAMP => DATE '2025-05-26');
```

## 语法

<div id="rrdiagram"></div>