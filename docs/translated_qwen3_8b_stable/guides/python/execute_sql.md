---
---
layout: docu
redirect_from:
- /docs/guides/python/execute_sql
title: 在 Python 中执行 SQL
---

可以使用 `duckdb.sql` 函数执行 SQL 查询。

```python
import duckdb

duckdb.sql("SELECT 42").show()
```

默认情况下，这会创建一个关系对象。可以使用结果转换函数将结果转换为各种格式。例如，可以使用 `fetchall` 方法将结果转换为 Python 对象。

```python
results = duckdb.sql("SELECT 42").fetchall()
print(results)
```

```text
[(42,)]
```

还存在其他几种结果对象。例如，可以使用 `df` 将结果转换为 Pandas DataFrame。

```python
results = duckdb.sql("SELECT 42").df()
print(results)
```

```text
    42
 0  42
```

默认情况下，会使用一个全局的内存连接。程序关闭后，存储在文件中的数据将丢失。可以使用 `connect` 函数创建到持久化数据库的连接。

连接后，可以使用 `sql` 命令执行 SQL 查询。

```python
con = duckdb.connect("file.db")
con.sql("CREATE TABLE integers (i INTEGER)")
con.sql("INSERT INTO integers VALUES (42)")
con.sql("SELECT * FROM integers").show()
```