---
---
github_repository: https://github.com/duckdb/duckdb-r
layout: docu
redirect_from:
- /docs/api/r
- /docs/api/r/
- /docs/clients/r
title: R 客户端
---

> DuckDB R 客户端的最新版本是 {{ site.current_duckdb_r_version }}。

## 安装

### `duckdb`: R 客户端

DuckDB R 客户端可以通过以下命令进行安装：

```r
install.packages("duckdb")
```

详细信息请参阅 [安装页面]({% link docs/installation/index.html %}?environment=r)。

### `duckplyr`: dplyr 客户端

DuckDB 提供了通过 `duckplyr` 包实现的 [dplyr](https://dplyr.tidyverse.org/)- 兼容 API。可以通过 `install.packages("duckplyr")` 进行安装。详细信息请参阅 [`duckplyr` 文档](https://tidyverse.github.io/duckplyr/)。

## 参考手册

DuckDB R 客户端的参考手册可在 [r.duckdb.org](https://r.duckdb.org) 查阅。

## 基本客户端使用

标准的 DuckDB R 客户端实现了 R 的 [DBI 接口](https://cran.r-project.org/package=DBI)。如果您还不熟悉 DBI，请参阅 [使用 DBI 页面](https://solutions.rstudio.com/db/r-packages/DBI/) 以获取介绍。

### 启动与关闭

要使用 DuckDB，您必须首先创建一个表示数据库的连接对象。连接对象接受一个参数，即要读写的数据文件。如果数据文件不存在，它将被创建（文件扩展名可以是 `.db`、`.duckdb` 或其他任何内容）。特殊值 `:memory:`（默认值）可用于创建一个 **内存数据库**。请注意，对于内存数据库，数据不会持久化到磁盘（即，当您退出 R 进程时，所有数据都会丢失）。如果您想以只读模式连接到现有数据库，请将 `read_only` 标志设置为 `TRUE`。如果多个 R 进程想要同时访问同一个数据库文件，必须使用只读模式。

```r
library("duckdb")
# 启动一个内存数据库
con <- dbConnect(duckdb())
# 或
con <- dbConnect(duckdb(), dbdir = ":memory:")
# 使用一个数据库文件（进程之间不共享）
con <- dbConnect(duckdb(), dbdir = "my-db.duckdb", read_only = FALSE)
# 使用一个数据库文件（进程之间共享）
con <- dbConnect(duckdb(), dbdir = "my-db.duckdb", read_only = TRUE)
```

当连接超出作用域或显式使用 `dbDisconnect()` 关闭时，连接会被隐式关闭。要关闭与连接相关的数据库实例，请使用 `dbDisconnect(con, shutdown = TRUE)`。

### 查询

DuckDB 支持标准的 DBI 方法发送查询并检索结果集。`dbExecute()` 用于无需返回结果的查询，例如 `CREATE TABLE` 或 `UPDATE` 等，而 `dbGetQuery()` 用于产生结果的查询（例如 `SELECT`）。以下是一个示例。

```r
# 创建一个表
dbExecute(con, "CREATE TABLE items (item VARCHAR, value DECIMAL(10, 2), count INTEGER)")
# 向表中插入两个项目
dbExecute(con, "INSERT INTO items VALUES ('jeans', 20.0, 1), ('hammer', 42.2, 2)")

# 再次检索这些项目
res <- dbGetQuery(con, "SELECT * FROM items")
print(res)
#     item value count
# 1  jeans  20.0     1
# 2 hammer  42.2     2
```

DuckDB 还支持在 R 客户端中使用 `dbExecute` 和 `dbGetQuery` 方法进行预编译语句。以下是一个示例：

```r
# 预编译语句的参数作为列表提供
dbExecute(con, "INSERT INTO items VALUES (?, ?, ?)", list('laptop', 2000, 1))

# 如果您想多次重用预编译语句，请使用 dbSendStatement() 和 dbBind()
stmt <- dbSendStatement(con, "INSERT INTO items VALUES (?, ?, ?)")
dbBind(stmt, list('iphone', 300, 2))
dbBind(stmt, list('android', 3.5, 1))
dbClearResult(stmt)

# 使用预编译语句查询数据库
res <- dbGetQuery(con, "SELECT item FROM items WHERE value > ?", list(400))
print(res)
#       item
# 1 laptop
```

> 警告：不要使用预编译语句将大量数据插入 DuckDB。有关更好的选项，请参见下文。

## 高效传输

要将 R 数据框写入 DuckDB，请使用标准 DBI 函数 `dbWriteTable()`。这将在 DuckDB 中创建一个表，并用数据框的内容填充它。例如：

```r
dbWriteTable(con, "iris_table", iris)
res <- dbGetQuery(con, "SELECT * FROM iris_table LIMIT 1")
print(res)
#   Sepal.Length Sepal.Width Petal.Length Petal.Width Species
# 1          5.1         3.5          1.4         0.2  setosa
```

您还可以将 R 数据框“注册”为虚拟表，类似于 SQL 的 `VIEW`。这 *不会实际将数据* 传输到 DuckDB。以下是一个示例：

```r
duckdb_register(con, "iris_view", iris)
res <- dbGetQuery(con, "SELECT * FROM iris_view LIMIT 1")
print(res)
#   Sepal.Length Sepal.Width Petal.Length Petal.Width Species
# 1          5.1         3.5          1.4         0.2  setosa
```

> DuckDB 在注册后会保留对 R 数据框的引用。这会阻止数据框被垃圾回收。当连接关闭时，该引用会被清除，也可以通过 `duckdb_unregister()` 方法手动清除。

请参考 [数据导入文档]({% link docs/stable/data/overview.md %}) 以获取更多高效导入数据的选项。

## dbplyr

DuckDB 也与 [dbplyr](https://CRAN.R-project.org/package=dbplyr) / [dplyr](https://dplyr.tidyverse.org) 包兼容，用于从 R 构建程序化查询。以下是一个示例：

```r
library("duckdb")
library("dplyr")
con <- dbConnect(duckdb())
duckdb_register(con, "flights", nycflights13::flights)

tbl(con, "flights") |>
  group_by(dest) |>
  summarise(delay = mean(dep_time, na.rm = TRUE)) |>
  collect()
```

在使用 dbplyr 时，可以使用 `dplyr::tbl` 函数读取 CSV 和 Parquet 文件。

```r
# 为示例创建一个 CSV 文件
write.csv(mtcars, "mtcars.csv")

# 在 DuckDB 中汇总数据集以避免将整个 CSV 读入 R 的内存
tbl(con, "mtcars.csv") |>
  group_by(cyl) |>
  summarise(across(disp:wt, .fns = mean)) |>
  collect()
```

```r
# 创建一组 Parquet 文件
dbExecute(con, "COPY flights TO 'dataset' (FORMAT parquet, PARTITION_BY (year, month))")

# 在 DuckDB 中汇总数据集以避免将 12 个 Parquet 文件读入 R 的内存
tbl(con, "read_parquet('dataset/**/*.parquet', hive_partitioning = true)") |>
  filter(month == "3") |>
  summarise(delay = mean(dep_time, na.rm = TRUE)) |>
  collect()
```

## 内存限制

您可以使用 [`memory_limit` 配置选项]({% link docs/stable/configuration/pragmas.md %}) 来限制 DuckDB 的内存使用，例如：

```sql
SET memory_limit = '2GB';
```

请注意，此限制仅适用于 DuckDB 使用的内存，不会影响其他 R 库的内存使用。因此，R 进程使用的总内存可能高于配置的 `memory_limit`。

## 故障排除

### 在 macOS 上安装时的警告

在 macOS 上安装 DuckDB 可能会出现警告 `unable to load shared object '.../R_X11.so'`：

```console
Warning message:
In doTryCatch(return(expr), name, parentenv, handler) :
  unable to load shared object '/Library/Frameworks/R.framework/Resources/modules//R_X11.so':
  dlopen(/Library/Frameworks/R.framework/Resources/modules//R_X11.so, 0x0006): Library not loaded: /opt/X11/lib/libSM.6.dylib
  Referenced from: <31EADEB5-0A17-3546-9944-9B3747071FE8> /Library/Frameworks/R.framework/Versions/4.4-arm64/Resources/modules/R_X11.so
  Reason: tried: '/opt/X11/lib/libSM.6.dylib' (no such file) ...
> ')
```

请注意，这只是警告，因此最简单的解决方法是忽略它。或者，您可以从 [R-universe](https://r-universe.dev/search) 安装 DuckDB：

```R
install.packages("duckdb", repos = c("https://duckdb.r-universe.dev", "https://cloud.r-project.org"))
```

您还可以通过 Homebrew 安装可选的 [`xquartz` 依赖项](https://formulae.brew.sh/cask/xquartz)。