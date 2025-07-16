---
---
layout: docu
redirect_from:
- /docs/api/rust
- /docs/api/rust/
- /docs/clients/rust
title: Rust 客户端
---

> DuckDB Rust 客户端的最新版本是 {{ site.current_duckdb_rust_version }}。

## 安装

DuckDB Rust 客户端可以从 [crates.io](https://crates.io/crates/duckdb) 进行安装。请参阅 [docs.rs](http://docs.rs/duckdb) 以获取详细信息。

## 基础 API 使用

duckdb-rs 是基于 [DuckDB C API](https://github.com/duckdb/duckdb/blob/main/src/include/duckdb.h) 的人性化封装，请参阅 [README](https://github.com/duckdb/duckdb-rs) 以获取详细信息。

### 启动与关闭

要使用 duckdb，您必须首先使用 `Connection::open()` 初始化一个 `Connection` 处理句柄。`Connection::open()` 接收一个参数，即要读写的数据库文件。如果数据库文件不存在，它将被创建（文件扩展名可能是 `.db`、`.duckdb` 或其他任何内容）。您也可以使用 `Connection::open_in_memory()` 来创建一个 **内存数据库**。请注意，对于内存数据库，不会将任何数据持久化到磁盘（即，当您退出进程时，所有数据都会丢失）。

```rust
use duckdb::{params, Connection, Result};
let conn = Connection::open_in_memory()?;
```

当 `Connection` 超出作用域时，它会自动为您关闭底层的数据库连接（通过 `Drop`）。您也可以显式关闭 `Connection`，使用 `conn.close()`。在大多数情况下，这两种方式没有太大的区别，但在发生错误时，您可以使用显式关闭来处理错误。

### 查询

可以使用连接的 `execute()` 方法将 SQL 查询发送到 DuckDB，也可以准备语句然后在该语句上进行查询。

```rust
#[derive(Debug)]
struct Person {
    id: i32,
    name: String,
    data: Option<Vec<u8>>,
}

conn.execute(
    "INSERT INTO person (name, data) VALUES (?, ?)",
    params![me.name, me.data],
)?;

let mut stmt = conn.prepare("SELECT id, name, data FROM person")?;
let person_iter = stmt.query_map([], |row| {
    Ok(Person {
        id: row.get(0)?,
        name: row.get(1)?,
        data: row.get(2)?,
    })
})?;

for person in person_iter {
    println!("Found person {:?}", person.unwrap());
}
```

## Appender

Rust 客户端支持 [DuckDB Appender API]({% link docs/stable/data/appender.md %}) 用于批量插入。例如：

```rust
fn insert_rows(conn: &Connection) -> Result<()> {
    let mut app = conn.appender("foo")?;
    app.append_rows([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]])?;
    Ok(())
}
```