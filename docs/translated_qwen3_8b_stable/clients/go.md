---
---
github_repository: https://github.com/marcboeker/go-duckdb
layout: docu
redirect_from:
- /docs/api/go
- /docs/api/go/
- /docs/clients/go
title: Go 客户端
---

> DuckDB Go 客户端的最新版本是 {{ site.current_duckdb_go_version }}。

DuckDB Go 驱动程序 `go-duckdb` 允许通过 `database/sql` 接口使用 DuckDB。有关如何使用此接口的示例，请参阅 [官方文档](https://pkg.go.dev/database/sql) 和 [教程](https://go.dev/doc/tutorial/database-access)。

> 项目 `go-duckdb` 位于 <https://github.com/marcboeker/go-duckdb>，是官方的 DuckDB Go 客户端。

## 安装

要安装 `go-duckdb` 客户端，请运行：

```bash
go get github.com/marcboeker/go-duckdb
```

## 导入

要导入 DuckDB Go 包，请将以下内容添加到您的导入语句中：

```go
import (
	"database/sql"
	_ "github.com/marcboeker/go-duckdb"
)
```

## Appender

DuckDB Go 客户端支持 [DuckDB Appender API]({% link docs/stable/data/appender.md %}) 用于批量插入。您可以通过将 DuckDB 连接提供给 `NewAppenderFromConn()` 来获取一个新的 Appender。例如：

```go
connector, err := duckdb.NewConnector("test.db", nil)
if err != nil {
  ...
}
conn, err := connector.Connect(context.Background())
if err != nil {
  ...
}
defer conn.Close()

// 从连接中获取 Appender（请注意，您必须事先创建表 'test'）。
appender, err := NewAppenderFromConn(conn, "", "test")
if err != nil {
  ...
}
defer appender.Close()

err = appender.AppendRow(...)
if err != nil {
  ...
}

// 可选，如果您希望立即访问已追加的行。
err = appender.Flush()
if err != nil {
  ...
}
```

## 示例

### 简单示例

使用 Go API 的一个示例如下：

```go
package main

import (
	"database/sql"
	"errors"
	"fmt"
	"log"

	_ "github.com/marcboeker/go-duckdb"
)

func main() {
	db, err := sql.Open("duckdb", "")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	_, err = db.Exec(`CREATE TABLE people (id INTEGER, name VARCHAR)`)
	if err != nil {
		log.Fatal(err)
	}
	_, err = db.Exec(`INSERT INTO people VALUES (42, 'John')`)
	if err != nil {
		log.Fatal(err)
	}

	var (
		id   int
		name string
	)
	row := db.QueryRow(`SELECT id, name FROM people`)
	err = row.Scan(&id, &name)
	if errors.Is(err, sql.ErrNoRows) {
		log.Println("没有行")
	} else if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("id: %d, name: %s\n", id, name)
}
```

### 更多示例

如需更多示例，请参阅 [`duckdb-go` 仓库中的示例](https://github.com/marcboeker/go-duckdb/tree/master/examples)。