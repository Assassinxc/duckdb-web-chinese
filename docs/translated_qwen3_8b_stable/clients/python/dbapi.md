---
---
layout: docu
redirect_from:
- /docs/api/python/dbapi
- /docs/api/python/dbapi/
- /docs/clients/python/dbapi
title: Python DB API
---

DuckDB 的标准 Python API 提供了一个符合 [DB-API 2.0 规范](https://www.python.org/dev/peps/pep-0249/) 的 SQL 接口，该规范由 PEP 249 描述，类似于 [SQLite Python API](https://docs.python.org/3.7/library/sqlite3.html)。

## 连接

要使用该模块，您必须首先创建一个 `DuckDBPyConnection` 对象，该对象表示与数据库的连接。这通过 [`duckdb.connect`]({% link docs/stable/clients/python/reference/index.md %}#duckdb.connect) 方法完成。

`config` 关键字参数可用于提供一个 `dict`，其中包含 key->value 的键值对，引用 [设置]({% link docs/stable/configuration/overview.md %}#configuration-reference) 项，这些设置为 DuckDB 所支持。

### 内存连接

可以使用特殊值 `:memory:` 创建一个 **内存数据库**。请注意，对于内存数据库，不会将任何数据持久化到磁盘（即，当您退出 Python 进程时，所有数据都会丢失）。

#### 命名的内存连接

特殊值 `:memory:` 也可以附加一个名称，例如：`:memory:conn3`。当提供名称时，后续的 `duckdb.connect` 调用将创建到同一数据库的新连接，并共享目录（视图、表、宏等）。

不带名称使用 `:memory:` 将始终创建一个新的、独立的数据库实例。

### 默认连接

默认情况下，我们创建一个（未命名的）**内存数据库**，它位于 `duckdb` 模块中。`DuckDBPyConnection` 的每个方法也都可以在 `duckdb` 模块上使用，这些方法使用的就是这个连接。

特殊值 `:default:` 可以用于获取此默认连接。

### 基于文件的连接

如果 `database` 是一个文件路径，则会建立到持久数据库的连接。如果文件不存在，该文件将被创建（文件扩展名无关紧要，可以是 `.db`、`.duckdb` 或其他任何内容）。

#### 只读连接

如果您希望以只读模式连接，可以将 `read_only` 标志设置为 `True`。如果文件不存在，在只读模式下连接时**不会**创建该文件。如果多个 Python 进程希望同时访问同一个数据库文件，必须使用只读模式。

```python
import duckdb

duckdb.execute("CREATE TABLE tbl AS SELECT 42 a")
con = duckdb.connect(":default:")
con.sql("SELECT * FROM tbl")
# 或
duckdb.default_connection().sql("SELECT * FROM tbl")
```

```text
┌───────┐
│   a   │
│ int32 │
├───────┤
│    42 │
└───────┘
```

```python
import duckdb

# 启动一个内存数据库
con = duckdb.connect(database = ":memory:")
# 使用一个数据库文件（进程间不共享）
con = duckdb.connect(database = "my-db.duckdb", read_only = False)
# 使用一个数据库文件（进程间共享）
con = duckdb.connect(database = "my-db.duckdb", read_only = True)
# 显式获取默认连接
con = duckdb.connect(database = ":default:")
```

如果您想要创建到现有数据库的第二个连接，可以使用 `cursor()` 方法。这在允许并行线程独立运行查询时可能很有用。单个连接是线程安全的，但在查询期间会被锁定，从而有效地在此情况下串行化数据库访问。

当连接超出作用域或显式使用 `close()` 关闭时，连接将被隐式关闭。一旦某个数据库实例的最后一个连接被关闭，该数据库实例也将被关闭。

## 查询

可以使用连接的 `execute()` 方法将 SQL 查询发送到 DuckDB。一旦执行了查询，可以使用连接上的 `fetchone` 和 `fetchall` 方法获取结果。`fetchall` 会获取所有结果并完成事务。`fetchone` 每次调用会获取一行结果，直到没有更多结果可用。事务仅在调用 `fetchone` 并且没有剩余结果时才会关闭（返回值将为 `None`）。例如，在查询只返回一行结果的情况下，`fetchone` 应该被调用一次以获取结果，并再次调用以关闭事务。以下是一些简短示例：

```python
# 创建一个表
con.execute("CREATE TABLE items (item VARCHAR, value DECIMAL(10, 2), count INTEGER)")
# 将两条记录插入表中
con.execute("INSERT INTO items VALUES ('jeans', 20.0, 1), ('hammer', 42.2, 2)")

# 再次获取这些记录
con.execute("SELECT * FROM items")
print(con.fetchall())
# [('jeans', Decimal('20.00'), 1), ('hammer', Decimal('42.20'), 2)]

# 逐行获取这些记录
con.execute("SELECT * FROM items")
print(con.fetchone())
# ('jeans', Decimal('20.00'), 1)
print(con.fetchone())
# ('hammer', Decimal('42.20'), 2)
print(con.fetchone()) # 这会关闭事务。后续对 .fetchone 的调用将返回 None
# None
```

连接对象的 `description` 属性包含根据标准定义的列名。

### 预编译语句

DuckDB 还支持通过 `execute` 和 `executemany` 方法在 API 中使用 [预编译语句]({% link docs/stable/sql/query_syntax/prepared_statements.md %})。值可以作为额外的参数传递，这些参数位于包含 `?` 或 `$1`（美元符号和数字）占位符的查询之后。使用 `?` 表示法会按照在 Python 参数中传递的顺序添加值。使用 `$` 表示法允许根据 Python 参数中值的数字和索引在 SQL 语句中重用值。值会根据 [转换规则]({% link docs/stable/clients/python/conversion.md %}#object-conversion-python-object-to-duckdb) 进行转换。

以下是一些示例。首先，使用 [预编译语句]({% link docs/stable/sql/query_syntax/prepared_statements.md %}) 插入一行：

```python
con.execute("INSERT INTO items VALUES (?, ?, ?)", ["laptop", 2000, 1])
```

其次，使用 [预编译语句]({% link docs/stable/sql/query_syntax/prepared_statements.md %}) 插入多行：

```python
con.executemany("INSERT INTO items VALUES (?, ?, ?)", [["chainsaw", 500, 10], ["iphone", 300, 2]] )
```

使用 [预编译语句]({% link docs/stable/sql/query_syntax/prepared_statements.md %}) 查询数据库：

```python
con.execute("SELECT item FROM items WHERE value > ?", [400])
print(con.fetchall())
```

```text
[('laptop',), ('chainsaw',)]
```

使用 [预编译语句]({% link docs/stable/sql/query_syntax/prepared_statements.md %}) 和重用值的 `$` 表示法进行查询：

```python
con.execute("SELECT $1, $1, $2", ["duck", "goose"])
print(con.fetchall())
```

```text
[('duck', 'duck', 'goose')]
```

> 警告：不要使用 `executemany` 将大量数据插入 DuckDB。请参阅 [数据摄入页面]({% link docs/stable/clients/python/data_ingestion.md %}) 以获取更好的选项。

## 命名参数

除了标准的未命名参数（如 `$1`、`$2` 等），还可以提供命名参数，如 `$my_parameter`。使用命名参数时，您必须在 `parameters` 参数中提供一个 `str` 到值的字典映射。以下是一个使用示例：

```python
import duckdb

res = duckdb.execute("""
    SELECT
        $my_param,
        $other_param,
        $also_param
    """,
    {
        "my_param": 5,
        "other_param": "DuckDB",
        "also_param": [42]
    }
).fetchall()
print(res)
```

```text
[(5, 'DuckDB', [42])]
```