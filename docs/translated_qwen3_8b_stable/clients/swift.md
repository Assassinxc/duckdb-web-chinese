---
---
github_repository: https://github.com/duckdb/duckdb-swift
layout: docu
redirect_from:
- /docs/api/swift
- /docs/api/swift/
- /docs/clients/swift
title: Swift 客户端
---

DuckDB 提供了 Swift 客户端。详情请参阅 [公告文章]({% post_url 2023-04-21-swift %})。

## 实例化 DuckDB

DuckDB 支持内存数据库和持久化数据库。
要使用内存数据库，请运行：

```swift
let database = try Database(store: .inMemory)
```

要使用持久化数据库，请运行：

```swift
let database = try Database(store: .file(at: "test.db"))
```

可以通过数据库连接执行查询。

```swift
let connection = try database.connect()
```

DuckDB 支持每个数据库的多个连接。

## 应用示例

本页其余部分基于我们 [公告文章]({% post_url 2023-04-21-swift %}) 中的示例，该示例使用了直接加载到 DuckDB 中的 [NASA 行星档案](https://exoplanetarchive.ipac.caltech.edu) 的原始数据。

### 创建应用程序特定类型

我们首先创建一个应用程序特定类型，用于存放我们的数据库和连接，并通过该类型最终定义我们的应用程序特定查询。

```swift
import DuckDB

final class ExoplanetStore {

  let database: Database
  let connection: Connection

  init(database: Database, connection: Connection) {
    self.database = database
    self.connection = connection
  }
}
```

### 加载 CSV 文件

我们从 [NASA 行星档案](https://exoplanetarchive.ipac.caltech.edu) 加载数据：

```text
wget https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name+,+disc_year+from+pscomppars&format=csv -O downloaded_exoplanets.csv
```

一旦我们本地下载了 CSV 文件，就可以使用以下 SQL 命令将其加载为 DuckDB 中的新表：

```sql
CREATE TABLE exoplanets AS
    SELECT * FROM read_csv('downloaded_exoplanets.csv');
```

我们将此封装为 `ExoplanetStore` 类型的新异步工厂方法：

```swift
import DuckDB
import Foundation

final class ExoplanetStore {

  // 工厂方法用于创建并准备一个新的 ExoplanetStore
  static func create() async throws -> ExoplanetStore {

  // 按照上面所述创建我们的数据库和连接
    let database = try Database(store: .inMemory)
    let connection = try database.connect()

  // 从行星档案下载 CSV 文件
  let (csvFileURL, _) = try await URLSession.shared.download(
    from: URL(string: "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name+,+disc_year+from+pscomppars&format=csv")!)

  // 向 DuckDB 发出我们的第一个查询
  try connection.execute("""
      CREATE TABLE exoplanets AS
          SELECT * FROM read_csv('\(csvFileURL.path)');
  """)

  // 创建我们预填充的 ExoplanetStore 实例
    return Exoplan
    database: database,
      connection: connection
  )
  }

  // 我们让之前定义的初始化器变为私有。这可以防止任何人意外地在没有将我们的 Exoplanet CSV 预加载到数据库的情况下实例化存储
  private init(database: Database, connection: Connection) {
  ...
  }
}
```

### 查询数据库

以下示例通过异步函数从 Swift 中查询 DuckDB。这意味着在查询执行期间，调用者不会被阻塞。我们随后使用 DuckDB 的 `ResultSet` `cast(to:)` 家族方法将结果列转换为 Swift 原生类型，最后将它们封装在 TabularData 框架的 `DataFrame` 中。

```swift
...

import TabularData

extension ExoplanetStore {

  // 获取按年份发现的系外行星数量
  func groupedByDiscoveryYear() async throws -> DataFrame {

  // 发出我们上面描述的查询
    let result = try connection.query("""
      SELECT disc_year, count(disc_year) AS Count
        FROM exoplanets
        GROUP BY disc_year
        ORDER BY disc_year
      """)

    // 将我们的 DuckDB 列转换为它们的 Swift 原生等价类型
    let discoveryYearColumn = result[0].cast(to: Int.self)
    let countColumn = result[1].cast(to: Int.self)

    // 使用我们的 DuckDB 列实例化 TabularData 列，并填充 TabularData DataFrame
    return DataFrame(columns: [
      TabularData.Column(discoveryYearColumn).eraseToAnyColumn(),
      TabularData.Column(countColumn).eraseToAnyColumn(),
    ])
  }
}
```

### 完整项目

要查看完整的示例项目，请克隆 [DuckDB Swift 仓库](https://github.com/duckdb/duckdb-swift)，并打开位于 [`Examples/SwiftUI/ExoplanetExplorer.xcodeproj`](https://github.com/duckdb/duckdb-swift/tree/main/Examples/SwiftUI/ExoplanetExplorer.xcodeproj) 的可运行应用项目。