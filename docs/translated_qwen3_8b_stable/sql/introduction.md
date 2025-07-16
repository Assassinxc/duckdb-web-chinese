---
---
layout: docu
redirect_from:
- /docs/sql/introduction
title: SQL 入门
---

在这里我们提供如何在 SQL 中执行简单操作的概述。
本教程仅用于提供一个简介，并不构成 SQL 的完整教程。
本教程改编自 [PostgreSQL 教程](https://www.postgresql.org/docs/current/tutorial-sql-intro.html)。

> DuckDB 的 SQL 方言密切遵循 PostgreSQL 方言的惯例。
> 例外情况在 [PostgreSQL 兼容性页面]({% link docs/stable/sql/dialect/postgresql_compatibility.md %}) 中列出。

在以下示例中，我们假设您已安装了 DuckDB 命令行界面 (CLI) shell。有关如何安装 CLI 的信息，请参阅 [安装页面]({% link docs/installation/index.html %}?environment=cli)。

## 概念

DuckDB 是一个关系型数据库管理系统 (RDBMS)。这意味着它是一个用于管理以关系形式存储数据的系统。关系本质上是一个数学术语，指的就是表。

每个表是一个命名的行集合。给定表的每一行都有相同的命名列集合，每个列都有特定的数据类型。表本身存储在模式中，一组模式构成了您可以访问的整个数据库。

## 创建新表

您可以使用指定表名以及所有列名和类型来创建新表：

```sql
CREATE TABLE weather (
    city    VARCHAR,
    temp_lo INTEGER, -- 一天中的最低温度
    temp_hi INTEGER, -- 一天中的最高温度
    prcp    FLOAT,
    date    DATE
);
```

您可以将此命令输入 shell 中，并按行分隔。命令在分号之前不会终止。

在 SQL 命令中，可以自由使用空白（即空格、制表符和换行符）。这意味着您可以输入与上述对齐方式不同的命令，甚至可以全部写在一行中。两个连字符 (`--`) 引入注释。在它们之后的内容将被忽略直到行尾。SQL 对关键字和标识符的大小写不敏感。在返回标识符时，[其原始大小写将被保留]({% link docs/stable/sql/dialect/keywords_and_identifiers.md %}#rules-for-case-sensitivity)。

在 SQL 命令中，我们首先指定要执行的命令类型：`CREATE TABLE`。之后是命令的参数。首先给出表名 `weather`。然后是列名和列类型。

`city VARCHAR` 指定表有一个名为 `city` 的列，其类型为 `VARCHAR`。`VARCHAR` 指定一个可以存储任意长度文本的数据类型。温度字段存储在 `INTEGER` 类型中，这是一种存储整数（即没有小数点的整数）的类型。`FLOAT` 列存储单精度浮点数（即带有小数点的数字）。`DATE` 存储日期（即年、月、日的组合）。`DATE` 仅存储特定的日期，而不是与该日期相关联的时间。

DuckDB 支持标准 SQL 类型 `INTEGER`、`SMALLINT`、`FLOAT`、`DOUBLE`、`DECIMAL`、`CHAR(n)`、`VARCHAR(n)`、`DATE`、`TIME` 和 `TIMESTAMP`。

第二个示例将存储城市及其相关的地理位置：

```sql
CREATE TABLE cities (
    name VARCHAR,
    lat  DECIMAL,
    lon  DECIMAL
);
```

最后，需要指出的是，如果您不再需要某个表或者希望以不同的方式重新创建它，可以使用以下命令将其删除：

```sql
DROP TABLE ⟨tablename⟩;
```

## 用行填充表

`INSERT` 语句用于向表中填充行：

```sql
INSERT INTO weather
VALUES ('San Francisco', 46, 50, 0.25, '1994-11-27');
```

非数字值的常量（例如文本和日期）必须用单引号 (`''`) 括起来，如示例所示。日期类型输入的日期必须格式化为 `'YYYY-MM-DD'`。

我们可以以相同的方式向 `cities` 表中插入数据。

```sql
INSERT INTO cities
VALUES ('San Francisco', -194.0, 53.0);
```

到目前为止使用的语法要求您记住列的顺序。另一种语法允许您显式列出列：

```sql
INSERT INTO weather (city, temp_lo, temp_hi, prcp, date)
VALUES ('San Francisco', 43, 57, 0.0, '1994-11-29');
```

如果您愿意，可以以不同的顺序列出列，甚至可以省略某些列，例如如果 `prcp` 不确定：

```sql
INSERT INTO weather (date, city, temp_hi, temp_lo)
VALUES ('1994-11-29', 'Hayward', 54, 37);
```

> 提示：许多开发人员认为显式列出列比依赖隐式顺序的风格更好。

请输入上述所有命令，以便在后续章节中使用一些数据。

或者，您可以使用 `COPY` 语句。对于大量数据，`COPY` 语句比 `INSERT` 更快，因为 `COPY` 命令针对批量加载进行了优化，但灵活性不如 `INSERT`。使用 [`weather.csv`](/data/weather.csv) 的示例将是：

```sql
COPY weather
FROM 'weather.csv';
```

其中，源文件的文件名必须在运行该进程的机器上可用。还有许多其他方法可以将数据加载到 DuckDB 中，请参阅 [相应的文档部分]({% link docs/stable/data/overview.md %}) 获取更多信息。

## 查询表

要从表中检索数据，需要查询该表。使用 SQL `SELECT` 语句来执行此操作。语句由选择列表（列出要返回的列的部分）、表列表（列出从中检索数据的表的部分）和可选的限定条件（指定任何限制的部分）组成。例如，要检索 `weather` 表的所有行，输入：

```sql
SELECT *
FROM weather;
```

这里 `*` 是“所有列”的简写。因此，使用以下命令也可以得到相同的结果：

```sql
SELECT city, temp_lo, temp_hi, prcp, date
FROM weather;
```

输出应为：

|     city      | temp_lo | temp_hi | prcp |    date    |
|---------------|--------:|--------:|-----:|------------|
| San Francisco | 46      | 50      | 0.25 | 1994-11-27 |
| San Francisco | 43      | 57      | 0.0  | 1994-11-29 |
| Hayward       | 37      | 54      | NULL | 1994-11-29 |

您可以在选择列表中编写表达式，而不仅仅是简单的列引用。例如，您可以这样做：

```sql
SELECT city, (temp_hi + temp_lo) / 2 AS temp_avg, date
FROM weather;
```

这应该给出：

|     city      | temp_avg |    date    |
|---------------|---------:|------------|
| San Francisco | 48.0     | 1994-11-27 |
| San Francisco | 50.0     | 1994-11-29 |
| Hayward       | 45.5     | 1994-11-29 |

请注意 `AS` 子句用于重命名输出列。（`AS` 子句是可选的。）

通过添加一个 `WHERE` 子句，可以对查询进行“限定”，以指定想要哪些行。`WHERE` 子句包含一个布尔（真值）表达式，只有满足布尔表达式为真的行才会被返回。通常允许使用布尔运算符（`AND`、`OR` 和 `NOT`）进行限定。例如，以下查询检索了旧金山的雨天天气：

```sql
SELECT *
FROM weather
WHERE city = 'San Francisco'
  AND prcp > 0.0;
```

结果：

|     city      | temp_lo | temp_hi | prcp |    date    |
|---------------|--------:|--------:|-----:|------------|
| San Francisco | 46      | 50      | 0.25 | 1994-11-27 |

您可以请求查询结果按排序顺序返回：

```sql
SELECT *
FROM weather
ORDER BY city;
```

|     city      | temp_lo | temp_hi | prcp |    date    |
|---------------|--------:|--------:|-----:|------------|
| Hayward       | 37      | 54      | NULL | 1994-11-29 |
| San Francisco | 43      | 57      | 0.0  | 1994-11-29 |
| San Francisco | 46      | 50      | 0.25 | 1994-11-27 |

在这个示例中，排序顺序没有完全指定，因此您可能会以任意顺序获得旧金山的行。但如果您执行以下命令：

```sql
SELECT *
FROM weather
ORDER BY city, temp_lo;
```

您将始终得到上述结果。

您可以请求从查询结果中删除重复行：

```sql
SELECT DISTINCT city
FROM weather;
```

|     city      |
|---------------|
| San Francisco |
| Hayward       |

在此结果中，行的顺序可能会有所不同。您可以使用 `DISTINCT` 和 `ORDER BY` 一起确保结果一致：

```sql
SELECT DISTINCT city
FROM weather
ORDER BY city;
```

## 表之间的连接

到目前为止，我们的查询一次只访问一个表。查询可以同时访问多个表，或者以某种方式访问同一表，使表中的多行同时被处理。一次访问同一表或多表的多行的查询称为连接查询。例如，假设您希望列出所有天气记录以及相关城市的地理位置。为此，我们需要将 `weather` 表中每一行的 `city` 列与 `cities` 表中所有行的 `name` 列进行比较，并选择这些值匹配的行对。

这可以通过以下查询实现：

```sql
SELECT *
FROM weather, cities
WHERE city = name;
```

|     city      | temp_lo | temp_hi | prcp |    date    |     name      |   lat    |  lon   |
|---------------|--------:|--------:|-----:|------------|---------------|---------:|-------:|
| San Francisco | 46      | 50      | 0.25 | 1994-11-27 | San Francisco | -194.000 | 53.000 |
| San Francisco | 43      | 57      | 0.0  | 1994-11-29 | San Francisco | -194.000 | 53.000 |

请注意结果集的两个方面：

* Hayward 城市没有结果行。这是因为 `cities` 表中没有匹配的条目，因此连接忽略了 `weather` 表中未匹配的行。我们很快将看到如何解决这个问题。
* 有两个包含城市名称的列。这是正确的，因为 `weather` 和 `cities` 表的列列表被连接在一起。在实践中，这并不理想，因此您可能更倾向于显式列出输出列而不是使用 `*`：

```sql
SELECT city, temp_lo, temp_hi, prcp, date, lon, lat
FROM weather, cities
WHERE city = name;
```

|     city      | temp_lo | temp_hi | prcp |    date    |  lon   |   lat    |
|---------------|--------:|--------:|-----:|------------|-------:|---------:|
| San Francisco | 46      | 50      | 0.25 | 1994-11-27 | 53.000 | -194.000 |
| San Francisco | 43      | 57      | 0.0  | 1994-11-29 | 53.000 | -194.000 |

由于所有列都有不同的名称，解析器会自动找到它们所属的表。如果两个表中存在重复的列名，您将需要使用限定列名以表明您指的是哪一个，例如：

```sql
SELECT weather.city, weather.temp_lo, weather.temp_hi,
       weather.prcp, weather.date, cities.lon, cities.lat
FROM weather, cities
WHERE cities.name = weather.city;
```

在连接查询中，通常认为对所有列名进行限定是良好的风格，这样即使以后在某个表中添加了重复的列名，查询也不会失败。

到目前为止看到的连接查询也可以使用以下替代形式编写：

```sql
SELECT *
FROM weather
INNER JOIN cities ON weather.city = cities.name;
```

这种语法不如上面的常见，但我们在下面展示它是为了帮助您理解后续主题。

现在，我们将弄清楚如何获取 Hayward 的记录。我们希望查询能扫描 `weather` 表，并为每一行找到匹配的 `cities` 行。如果找不到匹配的行，我们希望用 `cities` 表的列的“空值”来替代。这种类型的查询称为外连接。（我们之前看到的连接是内连接。）命令如下所示：

```sql
SELECT *
FROM weather
LEFT OUTER JOIN cities ON weather.city = cities.name;
```

|     city      | temp_lo | temp_hi | prcp |    date    |     name      |   lat    |  lon   |
|---------------|--------:|--------:|-----:|------------|---------------|---------:|-------:|
| San Francisco | 46      | 50      | 0.25 | 1994-11-27 | San Francisco | -194.000 | 53.000 |
| San Francisco | 43      | 57      | 0.0  | 1994-11-29 | San Francisco | -194.000 | 53.000 |
| Hayward       | 37      | 54      | NULL | 1994-11-29 | NULL          | NULL     | NULL   |

这个查询称为左外连接，因为连接操作符左侧提到的表的每一行至少会在输出中出现一次，而右侧的表只会输出与左侧表某些行匹配的那些行。当输出左侧表的行且没有右侧表的匹配行时，右侧表的列将用空值（null）代替。

## 聚合函数

像大多数其他关系型数据库产品一样，DuckDB 支持聚合函数。聚合函数从多个输入行中计算出单个结果。例如，有用于计算 `count`（计数）、`sum`（总和）、`avg`（平均值）、`max`（最大值）和 `min`（最小值）的聚合函数。

例如，我们可以找到最高最低温度：

```sql
SELECT max(temp_lo)
FROM weather;
```

| max(temp_lo) |
|-------------:|
| 46           |

如果我们想知道这个读数是在哪个城市（或哪些城市）发生的，我们可以尝试：

```sql
SELECT city
FROM weather
WHERE temp_lo = max(temp_lo);
```

但这将不起作用，因为聚合函数 `max` 不能在 `WHERE` 子句中使用：

```console
Binder Error:
WHERE 子句不能包含聚合函数！
```

这个限制存在是因为 `WHERE` 子句决定了哪些行将被包含在聚合计算中；显然，它必须在聚合函数计算之前进行评估。
然而，正如通常的情况一样，可以通过使用子查询重写查询以实现所需的结果：

```sql
SELECT city
FROM weather
WHERE temp_lo = (SELECT max(temp_lo) FROM weather);
```

|     city      |
|---------------|
| San Francisco |

这是可以接受的，因为子查询是一个独立的计算，它独立于外查询中的计算来计算其聚合函数。

聚合函数与 `GROUP BY` 子句结合也非常有用。例如，我们可以获取每个城市观察到的最高最低温度：

```sql
SELECT city, max(temp_lo)
FROM weather
GROUP BY city;
```

|     city      | max(temp_lo) |
|---------------|--------------|
| San Francisco | 46           |
| Hayward       | 37           |

这将为我们每个城市提供一行输出。每个聚合结果是在匹配该城市的表行上计算的。我们可以使用 `HAVING` 来过滤这些分组行：

```sql
SELECT city, max(temp_lo)
FROM weather
GROUP BY city
HAVING max(temp_lo) < 40;
```

|  city   | max(temp_lo) |
|---------|-------------:|
| Hayward | 37           |

这将只返回那些所有 `temp_lo` 值都低于 40 的城市的结果。最后，如果我们只关心以 `S` 开头的城市名称，可以使用 `LIKE` 运算符：

```sql
SELECT city, max(temp_lo)
FROM weather
WHERE city LIKE 'S%'            -- (1)
GROUP BY city
HAVING max(temp_lo) < 40;
```

有关 `LIKE` 运算符的更多信息，请参阅 [模式匹配页面]({% link docs/stable/sql/functions/pattern_matching.md %}).

理解聚合函数与 SQL 的 `WHERE` 和 `HAVING` 子句之间的相互作用非常重要。`WHERE` 和 `HAVING` 的基本区别如下：`WHERE` 在计算组和聚合之前选择输入行（因此，它控制哪些行进入聚合计算），而 `HAVING` 在计算组和聚合之后选择组行。因此，`WHERE` 子句不能包含聚合函数；尝试使用聚合函数来确定哪些行将成为聚合的输入是没有意义的。另一方面，`HAVING` 子句总是包含聚合函数。

在前面的例子中，我们可以在 `WHERE` 中应用城市名称限制，因为不需要聚合。这比将限制添加到 `HAVING` 更高效，因为我们避免了对所有未通过 `WHERE` 检查的行执行分组和聚合计算。

## 更新

您可以使用 `UPDATE` 命令更新现有行。假设您发现温度读数在 11 月 28 日之后都偏移了 2 度。您可以按以下方式更正数据：

```sql
UPDATE weather
SET temp_hi = temp_hi - 2,  temp_lo = temp_lo - 2
WHERE date > '1994-11-28';
```

查看数据的新状态：

```sql
SELECT *
FROM weather;
```

|     city      | temp_lo | temp_hi | prcp |    date    |
|---------------|--------:|--------:|-----:|------------|
| San Francisco | 46      | 50      | 0.25 | 1994-11-27 |
| San Francisco | 41      | 55      | 0.0  | 1994-11-29 |
| Hayward       | 35      | 52      | NULL | 1994-11-29 |

## 删除

可以使用 `DELETE` 命令从表中删除行。假设您不再对 Hayward 的天气感兴趣。那么您可以执行以下操作以从表中删除这些行：

```sql
DELETE FROM weather
WHERE city = 'Hayward';
```

所有属于 Hayward 的天气记录都将被删除。

```sql
SELECT *
FROM weather;
```

|     city      | temp_lo | temp_hi | prcp |    date    |
|---------------|--------:|--------:|-----:|------------|
| San Francisco | 46      | 50      | 0.25 | 1994-11-27 |
| San Francisco | 41      | 55      | 0.0  | 1994-11-29 |

在发出以下形式的语句时要小心：

```sql
DELETE FROM ⟨table_name⟩;
```

> 警告：如果没有限定条件，`DELETE` 将从给定表中删除所有行，使表变为空。系统在执行此操作前不会请求确认。