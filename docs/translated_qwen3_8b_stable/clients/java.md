---
---
github_repository: https://github.com/duckdb/duckdb-java
layout: docu
redirect_from:
- /docs/api/java
- /docs/api/java/
- /docs/api/scala
- /docs/api/scala/
- /docs/clients/java
title: Java JDBC 客户端
---

> DuckDB Java (JDBC) 客户端的最新版本是 {{ site.current_duckdb_java_short_version }}。

## 安装

DuckDB Java JDBC API 可以从 [Maven Central](https://search.maven.org/artifact/org.duckdb/duckdb_jdbc) 进行安装。请参阅 [安装页面]({% link docs/installation/index.html %}?environment=java) 获取更多详细信息。

## 基本 API 使用

DuckDB 的 JDBC API 实现了标准 Java 数据库连接 (JDBC) API 的主要部分，版本 4.1。描述 JDBC 超出了本页面的范围，请参阅 [官方文档](https://docs.oracle.com/javase/tutorial/jdbc/basics/index.html) 获取详细信息。下面我们将专注于 DuckDB 特有的部分。

请参考外部托管的 [API 参考](https://javadoc.io/doc/org.duckdb/duckdb_jdbc) 以获取我们对 JDBC 规范的扩展信息，或查看下面的 [Arrow 方法](#arrow-methods)。

### 启动与关闭

在 JDBC 中，数据库连接是通过标准的 `java.sql.DriverManager` 类创建的。
如果驱动程序无法自动注册到 `DriverManager`，你可以使用以下语句强制注册：

```java
Class.forName("org.duckdb.DuckDBDriver");
```

要创建 DuckDB 连接，请使用 `jdbc:duckdb:` JDBC URL 前缀调用 `DriverManager`，如下所示：

```java
import java.sql.Connection;
import java.sql.DriverManager;

Connection conn = DriverManager.getConnection("jdbc:duckdb:");
```

要使用 DuckDB 特有的功能，例如 [Appender](#appender)，请将对象转换为 `DuckDBConnection`：

```java
import java.sql.DriverManager;
import org.duckdb.DuckDBConnection;

DuckDBConnection conn = (DuckDBConnection) DriverManager.getConnection("jdbc:duckdb:");
```

当仅使用 `jdbc:duckdb:` URL 时，会创建一个 **内存数据库**。请注意，对于内存数据库，不会将数据持久化到磁盘（即，当你退出 Java 程序时，所有数据都会丢失）。如果你想访问或创建一个持久数据库，请在路径后追加其文件名。例如，如果数据库存储在 `/tmp/my_database`，请使用 JDBC URL `jdbc:duckdb:/tmp/my_database` 来创建连接。

可以以 **只读模式** 打开 DuckDB 数据库文件。这在多个 Java 进程希望同时读取同一个数据库文件时非常有用。要以只读模式打开现有数据库文件，请设置连接属性 `duckdb.read_only`，如下所示：

```java
Properties readOnlyProperty = new Properties();
readOnlyProperty.setProperty("duckdb.read_only", "true");
Connection conn = DriverManager.getConnection("jdbc:duckdb:/tmp/my_database", readOnlyProperty);
```

可以使用 `DriverManager` 创建额外的连接。更高效的方法是调用 `DuckDBConnection#duplicate()` 方法：

```java
Connection conn2 = ((DuckDBConnection) conn).duplicate();
```

允许创建多个连接，但混合使用读写和只读连接是不支持的。

### 配置连接

可以通过配置选项更改数据库系统的不同设置。请注意，其中许多设置可以在以后使用 [`PRAGMA` 语句]({% link docs/stable/configuration/pragmas.md %}) 进行更改。

```java
Properties connectionProperties = new Properties();
connectionProperties.setProperty("temp_directory", "/path/to/temp/dir/");
Connection conn = DriverManager.getConnection("jdbc:duckdb:/tmp/my_database", connectionProperties);
```

### 查询

DuckDB 支持标准 JDBC 方法发送查询和检索结果集。首先需要从 `Connection` 创建一个 `Statement` 对象，然后可以使用 `execute` 和 `executeQuery` 发送查询。`execute()` 用于不期望结果的查询，例如 `CREATE TABLE` 或 `UPDATE` 等，而 `executeQuery()` 用于生成结果的查询（例如 `SELECT`）。以下是两个示例。另请参阅 JDBC 的 [`Statement`](https://docs.oracle.com/javase/7/docs/api/java/sql/Statement.html) 和 [`ResultSet`](https://docs.oracle.com/javase/7/docs/api/java/sql/ResultSet.html) 文档。

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

Connection conn = DriverManager.getConnection("jdbc:duckdb:");

// 创建表
Statement stmt = conn.createStatement();
stmt.execute("CREATE TABLE items (item VARCHAR, value DECIMAL(10, 2), count INTEGER)");
// 向表中插入两个项目
stmt.execute("INSERT INTO items VALUES ('jeans', 20.0, 1), ('hammer', 42.2, 2)");

try (ResultSet rs = stmt.executeQuery("SELECT * FROM items")) {
    while (rs.next()) {
        System.out.println(rs.getString(1));
        System.out.println(rs.getInt(3));
    }
}
stmt.close();
```

```text
jeans
1
hammer
2
```

DuckDB 还支持按照 JDBC API 的预编译语句：

```java
import java.sql.PreparedStatement;

try (PreparedStatement stmt = conn.prepareStatement("INSERT INTO items VALUES (?, ?, ?);")) {
    stmt.setString(1, "chainsaw");
    stmt.setDouble(2, 500.0);
    stmt.setInt(3, 42);
    stmt.execute();
    // 可以进行更多的 execute() 调用
}
```

> 警告：不要使用预编译语句将大量数据插入 DuckDB。请参阅 [数据导入文档]({% link docs/stable/data/overview.md %}) 获取更好的选项。

### Arrow 方法

请参考 [API 参考](https://javadoc.io/doc/org.duckdb/duckdb_jdbc/latest/org/duckdb/DuckDBResultSet.html#arrowExportStream(java.lang.Object,long)) 获取类型签名

#### Arrow 导出

以下演示了如何导出一个 Arrow 流并使用 Java Arrow 绑定进行消费：

```java
import org.apache.arrow.memory.RootAllocator;
import org.apache.arrow.vector.ipc.ArrowReader;
import org.duckdb.DuckDBResultSet;

try (var conn = DriverManager.getConnection("jdbc:duckdb:");
    var stmt = conn.prepareStatement("SELECT * FROM generate_series(2000)");
    var resultset = (DuckDBResultSet) stmt.executeQuery();
    var allocator = new RootAllocator()) {
    try (var reader = (ArrowReader) resultset.arrowExportStream(allocator, 256)) {
        while (reader.loadNextBatch()) {
            System.out.println(reader.getVectorSchemaRoot().getVector("generate_series"));
        }
    }
    stmt.close();
}
```

#### Arrow 导入

以下演示了如何从 Java Arrow 绑定中消费一个 Arrow 流。

```java
import org.apache.arrow.memory.RootAllocator;
import org.apache.arrow.vector.ipc.ArrowReader;
import org.duckdb.DuckDBConnection;

// Arrow 绑定
try (var allocator = new RootAllocator();
     ArrowStreamReader reader = null; // 当然不应为 null
     var arrow_array_stream = ArrowArrayStream.allocateNew(allocator)) {
    Data.exportArrayStream(allocator, reader, arrow_array_stream);

    // DuckDB 设置
    try (var conn = (DuckDBConnection) DriverManager.getConnection("jdbc:duckdb:")) {
        conn.registerArrowStream("asdf", arrow_array_stream);

        // 运行查询
        try (var stmt = conn.createStatement();
             var rs = (DuckDBResultSet) stmt.executeQuery("SELECT count(*) FROM asdf")) {
            while (rs.next()) {
                System.out.println(rs.getInt(1));
            }
        }
    }
}
```

### 流式结果

结果流式传输在 JDBC 驱动程序中是可选的 – 在运行查询之前设置 `jdbc_stream_results` 配置为 `true`。最简单的方法是通过 `Properties` 对象传递它。

```java
Properties props = new Properties();
props.setProperty(DuckDBDriver.JDBC_STREAM_RESULTS, String.valueOf(true));

Connection conn = DriverManager.getConnection("jdbc:duckdb:", props);
```

### Appender

[Appender]({% link docs/stable/data/appender.md %}) 可以通过 `org.duckdb.DuckDBAppender` 类在 DuckDB JDBC 驱动中使用。
该类的构造函数需要模式名称和它应用于的表名。
当调用 `close()` 方法时，Appender 会被刷新。

示例：

```java
import java.sql.DriverManager;
import java.sql.Statement;
import org.duckdb.DuckDBConnection;

DuckDBConnection conn = (DuckDBConnection) DriverManager.getConnection("jdbc:duckdb:");
try (var stmt = conn.createStatement()) {
    stmt.execute("CREATE TABLE tbl (x BIGINT, y FLOAT, s VARCHAR)");

    // 使用 try-with-resources 在作用域结束时自动关闭 appender
    try (var appender = conn.createAppender(DuckDBConnection.DEFAULT_SCHEMA, "tbl")) {
        appender.beginRow();
        appender.append(10);
        appender.append(3.2);
        appender.append("hello");
        appender.endRow();
        appender.beginRow();
        appender.append(20);
        appender.append(-8.1);
        appender.append("world");
        appender.endRow();
    }
}
```

### 批量写入器

DuckDB JDBC 驱动提供批量写入功能。
批量写入器支持预编译语句以减少查询解析的开销。

> 批量插入的首选方法是使用 [Appender](#appender)，因为其性能更高。
> 但是，当使用 Appender 不可行时，批量写入器可以作为替代方案。

#### 使用预编译语句的批量写入器

```java
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import org.duckdb.DuckDBConnection;

DuckDBConnection conn = (DuckDBConnection) DriverManager.getConnection("jdbc:duckdb:");
PreparedStatement stmt = conn.prepareStatement("INSERT INTO test (x, y, z) VALUES (?, ?, ?);");

stmt.setObject(1, 1);
stmt.setObject(2, 2);
stmt.setObject(3, 3);
stmt.addBatch();

stmt.setObject(1, 4);
stmt.setObject(2, 5);
stmt.setObject(3, 6);
stmt.addBatch();

stmt.executeBatch();
stmt.close();
```

#### 使用普通语句的批量写入器

批量写入器也支持普通的 SQL 语句：

```java
import java.sql.DriverManager;
import java.sql.Statement;
import org.duckdb.DuckDBConnection;

DuckDBConnection conn = (DuckDBConnection) DriverManager.getConnection("jdbc:duckdb:");
Statement stmt = conn.createStatement();

stmt.execute("CREATE TABLE test (x INTEGER, y INTEGER, z INTEGER)");

stmt.addBatch("INSERT INTO test (x, y, z) VALUES (1, 2, 3);");
stmt.addBatch("INSERT INTO test (x, y, z) VALUES (4, 5, 6);");

stmt.executeBatch();
stmt.close();
```

## 故障排除

### 未找到驱动类

如果 Java 应用程序无法找到 DuckDB，可能会抛出以下错误：

```console
Exception in thread "main" java.sql.SQLException: No suitable driver found for jdbc:duckdb:
    at java.sql/java.sql.DriverManager.getConnection(DriverManager.java:706)
    at java.sql/java.sql.DriverManager.getConnection(DriverManager.java:252)
    ...
```

当手动加载类时，可能会导致以下错误：

```console
Exception in thread "main" java.lang.ClassNotFoundException: org.duckdb.DuckDBDriver
    at java.base/jdk.internal.loader.BuiltinClassLoader.loadClass(BuiltinClassLoader.java:641)
    at java.base/jdk.internal.loader.ClassLoaders$AppClassLoader.loadClass(ClassLoaders.java:188)
    at java.base/java.lang.ClassLoader.loadClass(ClassLoader.java:520)
    at java.base/java.lang.Class.forName0(Native Method)
    at java.base/java.lang.Class.forName(Class.java:375)
    ...
```

这些错误源于未检测到 DuckDB Maven/Gradle 依赖项。为了确保检测到它，请在 IDE 中刷新 Maven 配置。