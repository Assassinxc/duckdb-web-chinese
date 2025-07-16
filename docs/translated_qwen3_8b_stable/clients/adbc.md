---
---
layout: docu
redirect_from:
- /docs/api/adbc
- /docs/api/adbc/
- /docs/clients/adbc
title: ADBC 客户端
---

> DuckDB ADBC 客户端的最新版本是 {{ site.current_duckdb_version }}。

[Arrow 数据库连接性（ADBC）](https://arrow.apache.org/adbc/) 与 ODBC 和 JDBC 类似，是一种 C 风格的 API，它允许在不同的数据库系统之间实现代码的可移植性。这使得开发人员可以轻松地构建与数据库系统通信的应用程序，而无需使用特定于该系统的代码。ADBC 与 ODBC/JDBC 的主要区别在于，ADBC 使用 [Arrow](https://arrow.apache.org/) 在数据库系统和应用程序之间传输数据。DuckDB 具有 ADBC 驱动程序，该驱动程序利用了 [DuckDB 与 Arrow 之间的零拷贝集成]({% post_url 2021-12-03-duck-arrow %}) 来高效传输数据。

请参考 [ADBC 文档页面](https://arrow.apache.org/adbc/current/) 以了解 ADBC 的更详细讨论和详细 API 说明。

## 实现的功能

DuckDB-ADBC 驱动程序实现了完整的 ADBC 规范，除了 `ConnectionReadPartition` 和 `StatementExecutePartitions` 函数。这两个函数用于支持内部对查询结果进行分区的系统，这在 DuckDB 中并不适用。
在本节中，我们将介绍 ADBC 中存在的主要函数，以及它们所接受的参数，并为每个函数提供示例。

### 数据库

用于操作数据库的一组函数。

| 函数名称 | 描述 | 参数 | 示例 |
|:---|:-|:---|:----|
| `DatabaseNew` | 分配一个新的（但未初始化的）数据库。 | `(AdbcDatabase *database, AdbcError *error)` | `AdbcDatabaseNew(&adbc_database, &adbc_error)` |
| `DatabaseSetOption` | 设置一个 char* 选项。 | `(AdbcDatabase *database, const char *key, const char *value, AdbcError *error)` | `AdbcDatabaseSetOption(&adbc_database, "path", "test.db", &adbc_error)` |
| `DatabaseInit` | 完成设置选项并初始化数据库。 | `(AdbcDatabase *database, AdbcError *error)` | `AdbcDatabaseInit(&adbc_database, &adbc_error)` |
| `DatabaseRelease` | 销毁数据库。 | `(AdbcDatabase *database, AdbcError *error)` | `AdbcDatabaseRelease(&adbc_database, &adbc_error)` |

### 连接

用于创建和销毁与数据库交互的连接的一组函数。

| 函数名称 | 描述 | 参数 | 示例 |
|:---|:-|:---|:----|
| `ConnectionNew` | 分配一个新的（但未初始化的）连接。 | `(AdbcConnection*, AdbcError*)` | `AdbcConnectionNew(&adbc_connection, &adbc_error)` |
| `ConnectionSetOption` | 连接初始化前可以设置选项。 | `(AdbcConnection*, const char*, const char*, AdbcError*)` | `AdbcConnectionSetOption(&adbc_connection, ADBC_CONNECTION_OPTION_AUTOCOMMIT, ADBC_OPTION_VALUE_DISABLED, &adbc_error)` |
| `ConnectionInit` | 完成设置选项并初始化连接。 | `(AdbcConnection*, AdbcDatabase*, AdbcError*)` | `AdbcConnectionInit(&adbc_connection, &adbc_database, &adbc_error)` |
| `ConnectionRelease` | 销毁该连接。 | `(AdbcConnection*, AdbcError*)` | `AdbcConnectionRelease(&adbc_connection, &adbc_error)` |

用于获取数据库元数据的一组函数。通常，这些函数将返回 Arrow 对象，特别是 ArrowArrayStream。

| 函数名称 | 描述 | 参数 | 示例 |
|:---|:-|:---|:----|
| `ConnectionGetObjects` | 获取所有目录、数据库模式、表和列的层次视图。 | `(AdbcConnection*, int, const char*, const char*, const char*, const char**, const char*, ArrowArrayStream*, AdbcError*)` | `AdbcDatabaseInit(&adbc_database, &adbc_error)` |
| `ConnectionGetTableSchema` | 获取表的 Arrow 模式。 | `(AdbcConnection*, const char*, const char*, const char*, ArrowSchema*, AdbcError*)` | `A
AdbcDatabaseRelease(&adbc_database, &adbc_error)` |
| `ConnectionGetTableTypes` | 获取数据库中的表类型列表。 | `(AdbcConnection*, ArrowArrayStream*, AdbcError*)` | `AdbcDatabaseNew(&adbc_database, &adbc_error)` |

具有连接事务语义的一组函数。默认情况下，所有连接都以自动提交模式启动，但可以通过 ConnectionSetOption 函数将其关闭。

| 函数名称 | 描述 | 参数 | 示例 |
|:---|:-|:---|:----|
| `ConnectionCommit` | 提交任何待处理的事务。 | `(AdbcConnection*, AdbcError*)` | `AdbcConnectionCommit(&adbc_connection, &adbc_error)` |
| `ConnectionRollback` | 回滚任何待处理的事务。 | `(AdbcConnection*, AdbcError*)` | `AdbcConnectionRollback(&adbc_connection, &adbc_error)` |

### 语句

语句保存与查询执行相关的状态。它们代表一次性查询和预编译语句。它们可以被重用，但这样做将使该语句之前的结果集失效。

用于创建、销毁和设置语句选项的函数：

| 函数名称 | 描述 | 参数 | 示例 |
|:---|:-|:---|:----|
| `StatementNew` | 为给定连接创建一个新的语句。 | `(AdbcConnection*, AdbcStatement*, AdbcError*)` | `AdbcStatementNew(&adbc_connection, &adbc_statement, &adbc_error)` |
| `StatementRelease` | 销毁语句。 | `(AdbcStatement*, AdbcError*)` | `AdbcStatementRelease(&adbc_statement, &adbc_error)` |
| `StatementSetOption` | 设置语句的字符串选项。 | `(AdbcStatement*, const char*, const char*, AdbcError*)` | `StatementSetOption(&adbc_statement, ADBC_INGEST_OPTION_TARGET_TABLE, "TABLE_NAME", &adbc_error)` |

与查询执行相关的函数：

| 函数名称 | 描述 | 参数 | 示例 |
|:---|:-|:---|:----|
| `StatementSetSqlQuery` | 设置要执行的 SQL 查询。然后可以使用 StatementExecuteQuery 执行该查询。 | `(AdbcStatement*, const char*, AdbcError*)` | `AdbcStatementSetSqlQuery(&adbc_statement, "SELECT * FROM TABLE", &adbc_error)` |
| `StatementSetSubstraitPlan` | 设置要执行的 substrait 计划。然后可以使用 StatementExecuteQuery 执行该查询。 | `(AdbcStatement*, const uint8_t*, size_t, AdbcError*)` | `AdbcStatementSetSubstraitPlan(&adbc_statement, substrait_plan, length, &adbc_error)` |
| `StatementExecuteQuery` | 执行语句并获取结果。 | `(AdbcStatement*, ArrowArrayStream*, int64_t*, AdbcError*)` | `AdbcStatementExecuteQuery(&adbc_statement, &arrow_stream, &rows_affected, &adbc_error)` |
| `StatementPrepare` | 将此语句转换为可以多次执行的预编译语句。 | `(AdbcStatement*, AdbcError*)` | `AdbcStatementPrepare(&adbc_statement, &adbc_error)` |

与绑定相关的函数，用于批量插入或预编译语句。

| 函数名称 | 描述 | 参数 | 示例 |
|:---|:-|:---|:----|
| `StatementBindStream` | 绑定 Arrow 流。这可用于批量插入或预编译语句。 | `(AdbcStatement*, ArrowArrayStream*, AdbcError*)` | `StatementBindStream(&adbc_statement, &input_data, &adbc_error)` |

## 示例

无论使用哪种编程语言，要使用 ADBC 与 DuckDB，都需要两个数据库选项。第一个是 `driver`，它需要指向 DuckDB 库的路径。第二个选项是 `entrypoint`，它是 DuckDB-ADBC 驱动程序中导出的函数，用于初始化所有 ADBC 函数。一旦我们配置了这两个选项，还可以选择性地设置 `path` 选项，提供一个磁盘路径来存储我们的 DuckDB 数据库。如果不设置，将创建一个内存数据库。在配置完所有必要的选项后，我们可以继续初始化我们的数据库。下面是使用不同语言环境进行初始化的方法。

### C++

我们从 C++ 示例开始，声明通过 ADBC 查询数据所需的变量。这些变量包括错误处理、数据库、连接、语句处理和用于在 DuckDB 和应用程序之间传输数据的 Arrow 流。

```cpp
AdbcError adbc_error;
AdbcDatabase adbc_database;
AdbcConnection adbc_connection;
AdbcStatement adbc_statement;
ArrowArrayStream arrow_stream;
```

然后我们可以初始化我们的数据库变量。在初始化数据库之前，我们需要设置上面提到的 `driver` 和 `entrypoint` 选项。然后设置 `path` 选项并初始化数据库。以下示例中，字符串 `"path/to/libduckdb.dylib"` 应该是 DuckDB 动态库的路径。在 macOS 上是 `.dylib`，在 Linux 上是 `.so`。

```cpp
AdbcDatabaseNew(&adbc_database, &adbc_error);
AdbcDatabaseSetOption(&adbc_database, "driver", "path/to/libduckdb.dylib", &adbc_error);
AdbcDatabaseSetOption(&adbc_database, "entrypoint", "duckdb_adbc_init", &adbc_error);
// 默认情况下，我们启动一个内存数据库，但您可以选择性地定义一个路径来存储它。
AdbcDatabaseSetOption(&adbc_database, "path", "test.db", &adbc_error);
AdbcDatabaseInit(&adbc_database, &adbc_error);
```

在初始化数据库后，我们必须创建并初始化一个连接。

```cpp
AdbcConnectionNew(&adbc_connection, &adbc_error);
AdbcConnectionInit(&adbc_connection, &adbc_database, &adbc_error);
```

我们现在可以初始化我们的语句并通过连接运行查询。在调用 `AdbcStatementExecuteQuery` 后，`arrow_stream` 将被填充为结果。

```cpp
AdbcStatementNew(&adbc_connection, &adbc_statement, &adbc_error);
AdbcStatementSetSqlQuery(&adbc_statement, "SELECT 42", &adbc_error);
int64_t rows_affected;
AdbcStatementExecuteQuery(&adbc_statement, &arrow_stream, &rows_affected, &adbc_error);
arrow_stream.release(arrow_stream)
```

除了运行查询，我们还可以通过 `arrow_streams` 吸入数据。为此，我们需要设置一个选项以指定要插入的表名，绑定流，然后执行查询。

```cpp
StatementSetOption(&adbc_statement, ADBC_INGEST_OPTION_TARGET_TABLE, "AnswerToEverything", &adbc_error);
StatementBindStream(&adbc_statement, &arrow_stream, &adbc_error);
StatementExecuteQuery(&adbc_statement, nullptr, nullptr, &adbc_error);
```

### Python

第一步是使用 `pip` 安装 ADBC 驱动程序管理器。您还需要安装 `pyarrow` 以直接访问 Apache Arrow 格式的查询结果（例如使用 `fetch_arrow_table`）。

```bash
pip install adbc_driver_manager pyarrow
```

> 有关 `adbc_driver_manager` 包的详细信息，请参阅 [`adbc_driver_manager` 包文档](https://arrow.apache.org/adbc/current/python/api/adbc_driver_manager.html)。

与 C++ 类似，我们需要提供包含 libduckdb 共享对象位置和入口点函数的初始化选项。请注意，DuckDB 的 `path` 参数是通过 `db_kwargs` 字典传递的。

```python
import adbc_driver_duckdb.dbapi

with adbc_driver_duckdb.dbapi.connect("test.db") as conn, conn.cursor() as cur:
    cur.execute("SELECT 42")
    # 获取一个 pyarrow 表
    tbl = cur.fetch_arrow_table()
    print(tbl)
```

除了 `fetch_arrow_table`，DBApi 的其他方法（如 `fetchone` 和 `fetchall`）也在游标上实现。我们也可以通过 `arrow_streams` 吸入数据。只需在语句上设置选项以绑定数据流并执行查询即可。

```python
import adbc_driver_duckdb.dbapi
import pyarrow

data = pyarrow.record_batch(
    [[1, 2, 3, 4], ["a", "b", "c", "d"]],
    names = ["ints", "strs"],
)

with adbc_driver_duckdb.dbapi.connect("test.db") as conn, conn.cursor() as cur:
    cur.adbc_ingest("AnswerToEverything", data)
```

### Go

请首先从 [发布页面](https://github.com/duckdb/duckdb/releases) 下载 `libduckdb` 库（即 Linux 上的 `.so`、Mac 上的 `.dylib` 或 Windows 上的 `.dll`），并在运行代码前将其放在 `LD_LIBRARY_PATH` 中（如果不这样做，错误信息将说明该文件的位置选项。）

以下示例使用内存中的 DuckDB 数据库通过 SQL 查询修改内存中的 Arrow RecordBatches：

{% raw %}
```go
package main

import (
    "bytes"
    "context"
    "fmt"
    "io"

    "github.com/apache/arrow-adbc/go/adbc"
    "github.com/apache/arrow-adbc/go/adbc/drivermgr"
    "github.com/apache/arrow-go/v18/arrow"
    "github.com/apache/arrow-go/v18/arrow/array"
    "github.com/apache/arrow-go/v18/arrow/ipc"
    "github.com/apache/arrow-go/v18/arrow/memory"
)

func _makeSampleArrowRecord() arrow.Record {
    b := array.NewFloat64Builder(memory.DefaultAllocator)
    b.AppendValues([]float64{1, 2, 3}, nil)
    col := b.NewArray()

    defer col.Release()
    defer b.Release()

    schema := arrow.NewSchema([]arrow.Field{{Name: "column1", Type: arrow.PrimitiveTypes.Float64}}, nil)
    return array.NewRecord(schema, []arrow.Array{col}, int64(col.Len()))
}

type DuckDBSQLRunner struct {
    ctx  context.Context
    conn adbc.Connection
    db   adbc.Database
}

func NewDuckDBSQLRunner(ctx context.Context) (*DuckDBSQLRunner, error) {
    var drv drivermgr.Driver
    db, err := drv.NewDatabase(map[string]string{
        "driver":     "duckdb",
        "entrypoint": "duckdb_adbc_init",
        "path":       ":memory:",
    })
    if err != nil {
        return nil, fmt.Errorf("failed to create new in-memory DuckDB database: %w", err)
    }
    conn, err := db.Open(ctx)
    if err != nil {
        return nil, fmt.Errorf("failed to open connection to new in-memory DuckDB database: %w", err)
    }
    return &DuckDBSQLRunner{ctx: ctx, conn: conn, db: db}, nil
}

func serializeRecord(record arrow.Record) (io.Reader, error) {
    buf := new(bytes.Buffer)
    wr := ipc.NewWriter(buf, ipc.WithSchema(record.Schema()))
    if err := wr.Write(record); err != nil {
        return nil, fmt.Errorf("failed to write record: %w", err)
    }
    if err := wr.Close(); err != nil {
        return nil, fmt.Errorf("failed to close writer: %w", err)
    }
    return buf, nil
}

func (r *DuckDBSQLRunner) importRecord(sr io.Reader) error {
    rdr, err := ipc.NewReader(sr)
    if err != nil {
        return fmt.Errorf("failed to create IPC reader: %w", err)
    }
    defer rdr.Release()
    stmt, err := r.conn.NewStatement()
    if err != nil {
        return fmt.Errorf("failed to create new statement: %w", err)
    }
    if err := stmt.SetOption(adbc.OptionKeyIngestMode, adbc.OptionValueIngestModeCreate); err != nil {
        return fmt.Errorf("failed to set ingest mode: %w", err)
    }
    if err := stmt.SetOption(adbc.OptionKeyIngestTargetTable, "temp_table"); err != nil {
        return fmt.Errorf("failed to set ingest target table: %w", err)
    }
    if err := stmt.BindStream(r.ctx, rdr); err != nil {
        return fmt.Errorf("failed to bind stream: %w", err)
    }
    if _, err := stmt.ExecuteUpdate(r.ctx); err != nil {
        return fmt.Errorf("failed to execute update: %w", err)
    }
    return stmt.Close()
}

func (r *DuckDBSQLRunner) runSQL(sql string) ([]arrow.Record, error) {
    stmt, err := r.conn.NewStatement()
    if err != nil {
        return nil, fmt.Errorf("failed to create new statement: %w", err)
    }
    defer stmt.Close()

    if err := stmt.SetSqlQuery(sql); err != nil {
        return nil, fmt.Errorf("failed to set SQL query: %w", err)
    }
    out, n, err := stmt.ExecuteQuery(r.ctx)
    if err != nil {
        return nil, fmt.Errorf("failed to execute query: %w", err)
    }
    defer out.Release()

    result := make([]arrow.Record, 0, n)
    for out.Next() {
        rec := out.Record()
        rec.Retain() // .Next() 将释放记录，因此我们需要保留它
        result = append(result, rec)
    }
    if out.Err() != nil {
        return nil, out.Err()
    }
    return result, nil
}

func (r *DuckDBSQLRunner) RunSQLOnRecord(record arrow.Record, sql string) ([]arrow.Record, error) {
    serializedRecord, err := serializeRecord(record)
    if err != nil {
        return nil, fmt.Errorf("failed to serialize record: %w", err)
    }
    if err := r.importRecord(serializedRecord); err != nil {
        return nil, fmt.Errorf("failed to import record: %w", err)
    }
    result, err := r.runSQL(sql)
    if err != nil {
        return nil, fmt.Errorf("failed to run SQL: %w", err)
    }

    if _, err := r.runSQL("DROP TABLE temp_table"); err != nil {
        return nil, fmt.Errorf("failed to drop temp table after running query: %w", err)
    }
    return result, nil
}

func (r *DuckDBSQLRunner) Close() {
    r.conn.Close()
    r.db.Close()
}

func main() {
    rec := _makeSampleArrowRecord()
    fmt.Println(rec)

    runner, err := NewDuckDBSQLRunner(context.Background())
    if err != nil {
        panic(err)
    }
    defer runner.Close()

    resultRecords, err := runner.RunSQLOnRecord(rec, "SELECT column1+1 FROM temp_table")
    if err != nil {
        panic(err)
    }

    for _, resultRecord := range resultRecords {
        fmt.Println(resultRecord)
        resultRecord.Release()
    }
}
```
{% endraw %}

运行后将得到以下输出：

```go
record:
  schema:
  fields: 1
    - column1: type=float64
  rows: 3
  col[0][column1]: [1 2 3]

record:
  schema:
  fields: 1
    - (column1 + 1): type=float64, nullable
  rows: 3
  col[0][(column1 + 1)]: [2 3 4]
```