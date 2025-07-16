---
---
layout: docu
redirect_from:
- /docs/api/julia
- /docs/api/julia/
- /docs/clients/julia
title: Julia 客户端
---

DuckDB Julia 包为 DuckDB 提供了一个高性能的前端。与 SQLite 类似，DuckDB 在 Julia 客户端中以内存方式运行，并提供了一个 DBInterface 前端。

该包还支持多线程执行。它使用 Julia 线程/任务来实现此功能。如果您希望并行执行查询，必须通过设置 `JULIA_NUM_THREADS` 环境变量等方式启动支持多线程的 Julia。

## 安装

安装 DuckDB 的方式如下：

```julia
using Pkg
Pkg.add("DuckDB")
```

或者，使用 `]` 键进入包管理器，并执行以下命令：

```julia
pkg> add DuckDB
```

## 基础用法

```julia
using DuckDB

# 创建一个新的内存数据库
con = DBInterface.connect(DuckDB.DB, ":memory:")

# 创建一个表
DBInterface.execute(con, "CREATE TABLE integers (i INTEGER)")

# 通过执行预编译语句插入数据
stmt = DBInterface.prepare(con, "INSERT INTO integers VALUES(?)")
DBInterface.execute(stmt, [42])

# 查询数据库
results = DBInterface.execute(con, "SELECT 42 a")
print(results)
```

某些 SQL 语句，如 PIVOT 和 IMPORT DATABASE，会被执行为多个预编译语句，并在使用 `DuckDB.execute()` 时出错。相反，可以使用 `DuckDB.query()` 替代 `DuckDB.execute()`，并始终返回一个物化结果。

## 扫描数据框

DuckDB Julia 包还支持查询 Julia 数据框。请注意，数据框是直接由 DuckDB 读取的，而不是插入或复制到数据库中。

如果您希望将数据从数据框加载到 DuckDB 表中，可以运行 `CREATE TABLE ... AS` 或 `INSERT INTO` 查询。

```julia
using DuckDB
using DataFrames

# 创建一个新的内存数据库
con = DBInterface.connect(DuckDB.DB)

# 创建一个数据框
df = DataFrame(a = [1, 2, 3], b = [42, 84, 42])

# 将其注册为数据库中的视图
DuckDB.register_data_frame(con, df, "my_df")

# 在数据框上运行 SQL 查询
results = DBInterface.execute(con, "SELECT * FROM my_df")
print(results)
```

## 追加 API

DuckDB Julia 包还支持 [追加 API]({% link docs/stable/data/appender.md %})，其速度远快于使用预编译语句或单个 `INSERT INTO` 语句。追加操作以行格式进行。对于每一列，应调用 `append()`，之后通过调用 `flush()` 完成该行。在所有行追加完成后，应使用 `close()` 来完成追加器并清理生成的内存。

```julia
using DuckDB, DataFrames, Dates
db = DuckDB.DB()
# 创建一个表
DBInterface.execute(db,
    "CREATE OR REPLACE TABLE data (id INTEGER PRIMARY KEY, value FLOAT, timestamp TIMESTAMP, date DATE)")
# 创建要插入的数据
len = 100
df = DataFrames.DataFrame(
        id = collect(1:len),
        value = rand(len),
        timestamp = Dates.now() + Dates.Second.(1:len),
        date = Dates.today() + Dates.Day.(1:len)
    )
# 按行追加数据
appender = DuckDB.Appender(db, "data")
for i in eachrow(df)
    for j in i
        DuckDB.append(appender, j)
    end
    DuckDB.end_row(appender)
end
# 在所有行追加完成后关闭追加器
DuckDB.close(appender)
```

## 并发

在 Julia 进程中，只要每个任务都维护自己的数据库连接，任务就可以并发地读写数据库。在下面的示例中，一个任务被创建以定期读取数据库，而许多任务被创建以使用 [`INSERT` 语句]({% link docs/stable/sql/statements/insert.md %}) 和 [追加 API]({% link docs/stable/data/appender.md %}) 向数据库写入数据。

```julia
using Dates, DataFrames, DuckDB
db = DuckDB.DB()
DBInterface.connect(db)
DBInterface.execute(db, "CREATE OR REPLACE TABLE data (date TIMESTAMP, id INTEGER)")

function run_reader(db)
    # 为该任务创建一个 DuckDB 连接
    conn = DBInterface.connect(db)
    while true
        println(DBInterface.execute(conn,
                "SELECT id, count(date) AS count, max(date) AS max_date
                FROM data GROUP BY id ORDER BY id") |> DataFrames.DataFrame)
        Threads.sleep(1)
    end
    DBInterface.close(conn)
end
# 启动一个读取任务
Threads.@spawn run_reader(db)

function run_inserter(db, id)
    # 为该任务创建一个 DuckDB 连接
    conn = DBInterface.connect(db)
    for i in 1:1000
        Threads.sleep(0.01)
        DuckDB.execute(conn, "INSERT INTO data VALUES (current_timestamp, ?)"; id);
    end
    DBInterface.close(conn)
end
# 启动多个插入任务
for i in 1:100
    Threads.@spawn run_inserter(db, 1)
end

function run_appender(db, id)
    # 为该任务创建一个 DuckDB 连接
    appender = DuckDB.Appender(db, "data")
    for i in 1:1000
        Threads.sleep(0.01)
        row = (Dates.now(Dates.UTC), id)
        for j in row
            DuckDB.append(appender, j);
        end
        DuckDB.end_row(appender);
    end
    DuckDB.close(appender);
end
# 启动多个追加任务
for i in 1:100
    Threads.@spawn run_appender(db, 2)
end
```

## 原始 Julia 连接器

感谢 kimmolinna 提供 [原始的 DuckDB Julia 连接器](https://github.com/kimmolinna/DuckDB.jl)。