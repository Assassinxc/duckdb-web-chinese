---
---
layout: docu
redirect_from:
- /docs/data/appender
title: Appender
---

Appender 可用于将批量数据加载到 DuckDB 数据库中。目前它在 [C、C++、Go、Java 和 Rust API](#appender-support-in-other-clients) 中可用。Appender 与连接绑定，并在追加时使用该连接的事务上下文。Appender 始终将数据追加到数据库文件中的单个表中。

在 [C++ API]({% link docs/stable/clients/cpp.md %}) 中，Appender 的工作方式如下：

```cpp
DuckDB db;
Connection con(db);
// 创建表
con.Query("CREATE TABLE people (id INTEGER, name VARCHAR)");
// 初始化 Appender
Appender appender(con, "people");
```

`AppendRow` 函数是追加数据的最简单方法。它使用递归模板，允许您在一个函数调用中放入单行的所有值，如下所示：

```cpp
appender.AppendRow(1, "Mark");
```

还可以使用 `BeginRow`、`EndRow` 和 `Append` 方法单独构造行。这是 `AppendRow` 内部执行的操作，因此具有相同的性能特征。

```cpp
appender.BeginRow();
appender.Append<int32_t>(2);
appender.Append<string>("Hannes");
appender.EndRow();
```

添加到 Appender 的任何值在写入数据库系统之前都会被缓存，这是出于性能考虑。这意味着在追加过程中，行可能不会立即在系统中可见。当 Appender 超出作用域或调用 `appender.Close()` 时，缓存会自动刷新。还可以使用 `appender.Flush()` 方法手动刷新缓存。调用 `Flush` 或 `Close` 后，所有数据都已写入数据库系统。

## 日期、时间与时间戳

虽然数字和字符串相对直观，但日期、时间和时间戳需要一些解释。它们可以直接使用 `duckdb::Date`、`duckdb::Time` 或 `duckdb::Timestamp` 提供的方法进行追加。也可以使用内部的 `duckdb::Value` 类型进行追加，但这样会增加一些额外的开销，应尽量避免。

以下是一个简短示例：

```cpp
con.Query("CREATE TABLE dates (d DATE, t TIME, ts TIMESTAMP)");
Appender appender(con, "dates");

// 使用 Date/Time/Timestamp 类型构造值
// （这是最高效的方法）
appender.AppendRow(
    Date::FromDate(1992, 1, 1),
    Time::FromTime(1, 1, 1, 0),
    Timestamp::FromDatetime(Date::FromDate(1992, 1, 1), Time::FromTime(1, 1, 1, 0))
);
// 构造 duckdb::Value 对象
appender.AppendRow(
    Value::DATE(1992, 1, 1),
    Value::TIME(1, 1, 1, 0),
    Value::TIMESTAMP(1992, 1, 1, 1, 1, 1, 0)
);
```

## 提交频率

默认情况下，Appender 每 204,800 行提交一次。
您可以通过显式使用 [事务]({% link docs/stable/sql/statements/transactions.md %}) 并使用 `BEGIN TRANSACTION` 和 `COMMIT` 语句包围您的 `AppendRow` 批次来更改此设置。

## 处理约束违规

如果 Appender 遇到 `PRIMARY KEY` 冲突或 `UNIQUE` 约束违规，它将失败并返回以下错误：

```console
约束错误：
PRIMARY KEY 或 UNIQUE 约束被违反：重复键 "..."
```

在这种情况下，整个追加操作将失败，不会插入任何行。

## 其他客户端的 Appender 支持

Appender 也在以下客户端 API 中可用：

* [C]({% link docs/stable/clients/c/appender.md %})
* [Go]({% link docs/stable/clients/go.md %}#appender)
* [Java (JDBC)]({% link docs/stable/clients/java.md %}#appender)
* [Julia]({% link docs/stable/clients/julia.md %}#appender-api)
* [Rust]({% link docs/stable/clients/rust.md %}#appender)