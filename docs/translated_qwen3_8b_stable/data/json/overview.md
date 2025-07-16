---
---
layout: docu
redirect_from:
- /docs/data/json
- /docs/data/json/
- /docs/extensions/json
- /docs/extensions/json/
- /docs/data/json/overview
title: JSON 概述
---

DuckDB 支持用于从现有 JSON 中读取值和创建新 JSON 数据的 SQL 函数。
JSON 通过 `json` 扩展进行支持，该扩展随大多数 DuckDB 发行版一起提供，并在首次使用时自动加载。
如果您希望手动安装或加载它，请参阅 [“安装和加载”页面]({% link docs/stable/data/json/installing_and_loading.md %}).

## 关于 JSON

JSON 是一种开放标准的文件格式和数据交换格式，使用人类可读的文本存储和传输由属性-值对和数组（或其他可序列化值）组成的数据对象。
虽然它不是表格数据非常高效的格式，但它非常常见，尤其是作为数据交换格式。

## JSONPath 和 JSON Pointer 语法

DuckDB 实现了多个用于 JSON 提取的接口：[JSONPath](https://goessner.net/articles/JsonPath/) 和 [JSON Pointer](https://datatracker.ietf.org/doc/html/rfc6901)。两者均可与箭头运算符 (`->`) 和 `json_extract` 函数调用配合使用。

请注意，DuckDB 仅支持 JSONPath 的查找功能，即使用 `.<key>` 提取字段或使用 `[<index>]` 提取数组元素。
数组可以从后向前索引，两种方法均支持通配符 `*`。
DuckDB _不_ 支持完整的 JSONPath 语法，因为 SQL 可用于任何进一步的转换。

> 最好选择 JSONPath 或 JSON Pointer 语法中的一种，并在您的整个应用程序中使用。

<!-- DuckDB 主要使用 PostgreSQL 语法，一些函数来自 SQLite，以及一些其他 SQL 系统的函数 -->

## 索引

> 警告 根据 [PostgreSQL 的惯例]({% link docs/stable/sql/dialect/postgresql_compatibility.md %})，DuckDB 对其 [`ARRAY`]({% link docs/stable/sql/data_types/array.md %}) 和 [`LIST`]({% link docs/stable/sql/data_types/list.md %}) 数据类型使用 1 基索引，但对 JSON 数据类型使用 [0 基索引](https://www.postgresql.org/docs/17/functions-json.html#FUNCTIONS-JSON-PROCESSING)。

## 示例

### 加载 JSON

从磁盘读取 JSON 文件，自动推断选项：

```sql
SELECT * FROM 'todos.json';
```

使用 `read_json` 函数并自定义选项：

```sql
SELECT *
FROM read_json('todos.json',
               format = 'array',
               columns = {userId: 'UBIGINT',
                          id: 'UBIGINT',
                          title: 'VARCHAR',
                          completed: 'BOOLEAN'});
```

从标准输入读取 JSON 文件，自动推断选项：

```bash
cat data/json/todos.json | duckdb -c "SELECT * FROM read_json('/dev/stdin')"
```

将 JSON 文件读入表中：

```sql
CREATE TABLE todos (userId UBIGINT, id UBIGINT, title VARCHAR, completed BOOLEAN);
COPY todos FROM 'todos.json' (AUTO_DETECT true);
```

或者，使用 [`CREATE TABLE ... AS SELECT` 子句]({% link docs/stable/sql/statements/create_table.md %}#create-table--as-select-ctas) 不手动指定模式创建表：

```sql
CREATE TABLE todos AS
    SELECT * FROM 'todos.json';
```

自 DuckDB v1.3.0 起，JSON 读取器返回 `filename` 虚拟列：

```sql
SELECT filename, *
FROM 'todos-*.json';
```

### 写入 JSON

将查询结果写入 JSON 文件：

```sql
COPY (SELECT * FROM todos) TO 'todos.json';
```

### JSON 数据类型

创建一个包含用于存储 JSON 数据的列的表，并将其数据插入其中：

```sql
CREATE TABLE example (j JSON);
INSERT INTO example VALUES
    ('{ "family": "anatidae", "species": [ "duck", "goose", "swan", null ] }');
```

### 提取 JSON 数据

提取 family 键的值：

```sql
SELECT j.family FROM example;
```

```text
"anatidae"
```

使用 [JSONPath](https://goessner.net/articles/JsonPath/) 表达式作为 `JSON` 提取 family 键的值：

```sql
SELECT j->'$.family' FROM example;
```

```text
"an
```