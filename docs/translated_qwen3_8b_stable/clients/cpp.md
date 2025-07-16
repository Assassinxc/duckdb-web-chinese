---
---
layout: docu
redirect_from:
- /docs/api/cpp
- /docs/api/cpp/
- /docs/clients/cpp
title: C++ API
---

> DuckDB C++ API 的最新版本是 {{ site.current_duckdb_version }}。

> 警告 DuckDB 的 C++ API 主要用于内部用途。
> 它不保证稳定性，可能会在不通知的情况下发生变化。
> 如果您希望在 DuckDB 上构建应用程序，
> 我们建议使用 [C API]({% link docs/stable/clients/c/overview.md %}).

## 安装

DuckDB 的 C++ API 可以作为 `libduckdb` 包的一部分进行安装。请参阅 [安装页面]({% link docs/installation/index.html %}?environment=cplusplus) 以获取详细信息。

## 基本 API 使用

DuckDB 实现了一个定制的 C++ API。该 API 基于数据库实例（`DuckDB` 类）、多个 `Connection` 连接到数据库实例以及 `QueryResult` 实例作为查询结果。C++ API 的头文件是 `duckdb.hpp`。

### 启动与关闭

要使用 DuckDB，您必须首先使用其构造函数初始化一个 `DuckDB` 实例。`DuckDB()` 接受一个参数，即要读取和写入的数据库文件。特殊值 `nullptr` 可用于创建一个 **内存数据库**。请注意，对于内存数据库，不会将任何数据持久化到磁盘（即，退出进程时所有数据都会丢失）。`DuckDB` 构造函数的第二个参数是一个可选的 `DBConfig` 对象。在 `DBConfig` 中，您可以设置各种数据库参数，例如读/写模式或内存限制。`DuckDB` 构造函数可能会抛出异常，例如如果数据库文件不可用。

使用 `DuckDB` 实例，您可以使用 `Connection()` 构造函数创建一个或多个 `Connection` 实例。虽然连接应是线程安全的，但在查询期间它们会被锁定。因此，如果您在多线程环境中，建议每个线程使用自己的连接。

```cpp
DuckDB db(nullptr);
Connection con(db);
```

### 查询

连接通过 `Query()` 方法将 SQL 查询字符串发送到 DuckDB。`Query()` 在返回之前会完全将查询结果作为 `MaterializedQueryResult` 实现在内存中，此时可以消费查询结果。还有一个查询的流式 API，详见下文。

```cpp
// 创建一个表
con.Query("CREATE TABLE integers (i INTEGER, j INTEGER)");

// 向表中插入三行数据
con.Query("INSERT INTO integers VALUES (3, 4), (5, 6), (7, NULL)");

auto result = con.Query("SELECT * FROM integers");
if (result->HasError()) {
    cerr << result->GetError() << endl;
} else {
    cout << result->ToString() << endl;
}
```

`MaterializedQueryResult` 实例首先包含两个字段，用于指示查询是否成功。`Query` 在正常情况下不会抛出异常。相反，无效的查询或其他问题会导致查询结果实例中的 `success` 布尔字段设置为 `false`。在这种情况下，错误信息可能在 `error` 中作为字符串提供。如果成功，其他字段会被设置：刚刚执行的语句类型（例如 `StatementType::INSERT_STATEMENT`）包含在 `statement_type` 中。结果集列的高级（“逻辑类型”/“SQL 类型”）类型在 `types` 中。结果列的名称在 `names` 字符串向量中。如果返回了多个结果集（例如，因为结果集包含多个语句），可以通过 `next` 字段链接结果集。

DuckDB 还通过 `Prepare()` 方法在 C++ API 中支持预编译语句。这会返回一个 `PreparedStatement` 实例。该实例可用于执行带参数的预编译语句。下面是一个示例：

```cpp
std::unique_ptr<PreparedStatement> prepare = con.Prepare("SELECT count(*) FROM a WHERE i = $1");
std::unique_ptr<QueryResult> result = prepare->Execute(12);
```

> 警告 不要使用预编译语句将大量数据插入 DuckDB。请参阅 [数据导入文档]({% link docs/stable/data/overview.md %}) 以获得更好的选项。

### UDF API

UDF API 允许定义用户自定义函数。它通过 `duckdb:Connection` 中的方法 `CreateScalarFunction()`、`CreateVectorizedFunction()` 和其变体暴露出来。
这些方法在所有者连接的临时模式（`TEMP_SCHEMA`）中创建 UDF，该模式是唯一允许使用和更改它们的模式。

#### CreateScalarFunction

用户可以编写一个普通的标量函数，并调用 `CreateScalarFunction()` 注册并在 `SELECT` 语句中使用该 UDF，例如：

```cpp
bool bigger_than_four(int value) {
    return value > 4;
}

connection.CreateScalarFunction<bool, int>("bigger_than_four", &bigger_than_four);

connection.Query("SELECT bigger_than_four(i) FROM (VALUES(3), (5)) tbl(i)")->Print();
```

`CreateScalarFunction()` 方法会自动创建矢量化标量 UDF，因此它们与内置函数一样高效。我们有这个方法的两个变体接口如下：

**1.**

```cpp
template<typename TR, typename... Args>
void CreateScalarFunction(string name, TR (*udf_func)(Args…))
```

- 模板参数：
    - **TR** 是 UDF 函数的返回类型；
    - **Args** 是 UDF 函数的参数（最多 3 个）（此方法只支持三元函数）；
- **name** 是注册 UDF 函数的名称；
- **udf_func** 是 UDF 函数的指针。

此方法会从模板类型名自动发现对应的 LogicalTypes：

- `bool` → `LogicalType::BOOLEAN`
- `int8_t` → `LogicalType::TINYINT`
- `int16_t` → `LogicalType::SMALLINT`
- `int32_t` → `LogicalType::INTEGER`
- `int64_t` → `LogicalType::BIGINT`
- `float` → `LogicalType::FLOAT`
- `double` → `LogicalType::DOUBLE`
- `string_t` → `LogicalType::VARCHAR`

在 DuckDB 中，一些原始类型，例如 `int32_t`，映射到相同的 `LogicalType`：`INTEGER`、`TIME` 和 `DATE`，因此为了区分，用户可以使用以下重载方法。

**2.**

```cpp
template<typename TR, typename... Args>
void CreateScalarFunction(string name, vector<LogicalType> args, LogicalType ret_type, TR (*udf_func)(Args…))
```

使用示例如下：

```cpp
int32_t udf_date(int32_t a) {
    return a;
}

con.Query("CREATE TABLE dates (d DATE)");
con.Query("INSERT INTO dates VALUES ('1992-01-01')");

con.CreateScalarFunction<int32_t, int32_t>("udf_date", {LogicalType::DATE}, LogicalType::DATE, &udf_date);

con.Query("SELECT udf_date(d) FROM dates")->Print();
```

- 模板参数：
    - **TR** 是 UDF 函数的返回类型；
    - **Args** 是 UDF 函数的参数（最多 3 个）（此方法只支持三元函数）；
- **name** 是注册 UDF 函数的名称；
- **args** 是函数使用的 LogicalType 参数，应与模板 Args 类型匹配；
- **ret_type** 是函数返回的 LogicalType，应与模板 TR 类型匹配；
- **udf_func** 是 UDF 函数的指针。

此函数会检查模板类型与传递的 LogicalTypes 是否匹配，如下所示：

- LogicalTypeId::BOOLEAN → bool
- LogicalTypeId::TINYINT → int8_t
- LogicalTypeId::SMALLINT → int16_t
- LogicalTypeId::DATE, LogicalTypeId::TIME, LogicalTypeId::INTEGER → int32_t
- LogicalTypeId::BIGINT, LogicalTypeId::TIMESTAMP → int64_t
- LogicalTypeId::FLOAT, LogicalTypeId::DOUBLE, LogicalTypeId::DECIMAL → double
- LogicalTypeId::VARCHAR, LogicalTypeId::CHAR, LogicalTypeId::BLOB → string_t
- LogicalTypeId::VARBINARY → blob_t

#### CreateVectorizedFunction

`CreateVectorizedFunction()` 方法注册一个矢量化 UDF，例如：

```cpp
/*
* 此矢量化函数将输入值复制到结果向量中
*/
template<typename TYPE>
static void udf_vectorized(DataChunk &args, ExpressionState &state, Vector &result) {
    // 设置结果向量类型
    result.vector_type = VectorType::FLAT_VECTOR;
    // 从结果获取原始数组
    auto result_data = FlatVector::GetData<TYPE>(result);

    // 获取唯一的输入向量
    auto &input = args.data[0];
    // 现在获取一个或化向量
    VectorData vdata;
    input.Orrify(args.size(), vdata);

    // 从或化输入获取原始数组
    auto input_data = (TYPE *)vdata.data;

    // 处理数据
    for (idx_t i = 0; i < args.size(); i++) {
        auto idx = vdata.sel->get_index(i);
        if ((*vdata.nullmask)[idx]) {
            continue;
        }
        result_data[i] = input_data[idx];
    }
}

con.Query("CREATE TABLE integers (i INTEGER)");
con.Query("INSERT INTO integers VALUES (1), (2), (3), (999)");

con.CreateVectorizedFunction<int, int>("udf_vectorized_int", &&udf_vectorized<int>);

con.Query("SELECT udf_vectorized_int(i) FROM integers")->Print();
```

矢量化 UDF 是类型为 _scalar_function_t_ 的指针：

```cpp
typedef std::function<void(DataChunk &args, ExpressionState &expr, Vector &result)> scalar_function_t;
```

- **args** 是 [DataChunk](https://github.com/duckdb/duckdb/blob/main/src/include/duckdb/common/types/data_chunk.hpp)，它包含 UDF 的一组输入向量，所有向量长度相同；
- **expr** 是 [ExpressionState](https://github.com/duckdb/duckdb/blob/main/src/include/duckdb/execution/expression_executor_state.hpp)，它为查询的表达式状态提供信息；
- **result** 是 [Vector](https://github.com/duckdb/duckdb/blob/main/src/include/duckdb/common/types/vector.hpp)，用于存储结果值。

在矢量化 UDF 中处理不同的向量类型：
- ConstantVector；
- DictionaryVector；
- FlatVector；
- ListVector；
- StringVector；
- StructVector；
- SequenceVector。

`CreateVectorizedFunction()` 方法的一般 API 如下：

**1.**

```cpp
template<typename TR, typename... Args>
void CreateVectorizedFunction(string name, scalar_function_t udf_func, LogicalType varargs = LogicalType::INVALID)
```

- 模板参数：
    - **TR** 是 UDF 函数的返回类型；
    - **Args** 是 UDF 函数的参数（最多 3 个）。
- **name** 是注册 UDF 函数的名称；
- **udf_func** 是一个 _矢量化_ UDF 函数；
- **varargs** 支持的变长参数类型，或 LogicalTypeId::INVALID（默认值）如果函数不接受可变长度参数。

此方法会从模板类型名自动发现对应的 LogicalTypes：

- bool → LogicalType::BOOLEAN；
- int8_t → LogicalType::TINYINT；
- int16_t → LogicalType::SMALLINT
- int32_t → LogicalType::INTEGER
- int64_t → LogicalType::BIGINT
- float → LogicalType::FLOAT
- double → LogicalType::DOUBLE
- string_t → LogicalType::VARCHAR

**2.**

```cpp
template<typename TR, typename... Args>
void CreateVectorizedFunction(string name, vector<LogicalType> args, LogicalType ret_type, scalar_function_t udf_func, LogicalType varargs = LogicalType::INVALID)
```