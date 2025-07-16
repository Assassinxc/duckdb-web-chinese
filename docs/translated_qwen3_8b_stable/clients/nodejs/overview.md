---
---
layout: docu
redirect_from:
- /docs/api/nodejs
- /docs/api/nodejs/
- /docs/api/nodejs/overview
- /docs/api/nodejs/overview/
- /docs/clients/nodejs/overview
title: Node.js API
---

> 最新的 DuckDB Node.js（已弃用）客户端版本是 {{ site.current_duckdb_nodejs_version }}。

> 已弃用 旧的 DuckDB Node.js 包已弃用。
> 请改用 [DuckDB Node Neo 包]({% link docs/stable/clients/node_neo/overview.md %})。

`duckdb` 包提供了用于 DuckDB 的 Node.js API。
此客户端的 API 在某种程度上与 SQLite Node.js 客户端兼容，以方便迁移。

## 初始化

加载包并创建数据库对象：

```js
const duckdb = require('duckdb');
const db = new duckdb.Database(':memory:'); // 或文件名用于持久化数据库
```

所有选项如 [数据库配置]({% link docs/stable/configuration/overview.md %}#configuration-reference) 中所述，都可以作为 `Database` 构造函数的第二个参数（可选）提供。第三个参数也可以（可选）提供以获取有关给定选项的反馈。

```js
const db = new duckdb.Database(':memory:', {
    "access_mode": "READ_WRITE",
    "max_memory": "512MB",
    "threads": "4"
}, (err) => {
  if (err) {
    console.error(err);
  }
});
```

## 运行查询

以下代码片段使用 `Database.all()` 方法运行一个简单的查询。

```js
db.all('SELECT 42 AS fortytwo', function(err, res) {
  if (err) {
    console.warn(err);
    return;
  }
  console.log(res[0].fortytwo)
});
```

其他可用的方法是 `each`，其中回调函数会在每一行被调用，`run` 用于执行单条语句但不返回结果，`exec` 可以一次执行多个 SQL 命令，但也不返回结果。所有这些命令都可以与预编译语句一起使用，将参数的值作为额外的参数传递。例如如下所示：

```js
db.all('SELECT ?::INTEGER AS fortytwo, ?::VARCHAR AS hello', 42, 'Hello, World', function(err, res) {
  if (err) {
    console.warn(err);
    return;
  }
  console.log(res[0].fortytwo)
  console.log(res[0].hello)
});
```

## 连接

一个数据库可以有多个 `Connection`，它们通过 `db.connect()` 创建。

```js
const con = db.connect();
```

您可以创建多个连接，每个连接都有自己的事务上下文。

`Connection` 对象还包含简写方式，可以直接调用 `run()`、`all()` 和 `each()`，并分别传递参数和回调函数，例如：

```js
con.all('SELECT 42 AS fortytwo', function(err, res) {
  if (err) {
    console.warn(err);
    return;
  }
  console.log(res[0].fortytwo)
});
```

## 预编译语句

通过连接，您可以使用 `con.prepare()` 创建预编译语句（仅此而已）：

```js
const stmt = con.prepare('SELECT ?::INTEGER AS fortytwo');
```

要执行此语句，您可以调用 `stmt` 对象上的 `all()` 方法：

```js
stmt.all(42, function(err, res) {
  if (err) {
    console.warn(err);
  } else {
    console.log(res[0].fortytwo)
  }
});
```

您还可以多次执行预编译语句。这在填充表数据时特别有用：

```js
con.run('CREATE TABLE a (i INTEGER)');
const stmt = con.prepare('INSERT INTO a VALUES (?)');
for (let i = 0; i < 10; i++) {
  stmt.run(i);
}
stmt.finalize();
con.all('SELECT * FROM a', function(err, res) {
  if (err) {
    console.warn(err);
  } else {
    console.log(res)
  }
});
```

`prepare()` 也可以接受一个回调函数，该函数的参数是预编译语句：

```js
const stmt = con.prepare('SELECT ?::INTEGER AS fortytwo', function(err, stmt) {
  stmt.all(42, function(err, res) {
    if (err) {
      console.warn(err);
    } else {
      console.log(res[0].fortytwo)
    }
  });
});
```

## 通过 Apache Arrow 插入数据

可以使用 [Apache Arrow]({% link docs/stable/guides/python/sql_on_arrow.md %}) 在不复制数据的情况下将数据插入 DuckDB：

```js
const arrow = require('apache-arrow');
const db = new duckdb.Database(':memory:');

const jsonData = [
  {"userId":1,"id":1,"title":"delectus aut autem","completed":false},
  {"userId":1,"id":2,"title":"quis ut nam facilis et officia qui","completed":false}
];

// 注意；目前尚未支持 Windows
db.exec(`INSTALL arrow; LOAD arrow;`, (err) => {
    if (err) {
        console.warn(err);
        return;
    }

    const arrowTable = arrow.tableFromJSON(jsonData);
    db.register_buffer("jsonDataTable", [arrow.tableToIPC(arrowTable)], true, (err, res) => {
        if (err) {
            console.warn(err);
            return;
        }

        // `SELECT * FROM jsonDataTable` 将返回 `jsonData` 中的条目
    });
});
```

## 加载无签名扩展

要加载 [无签名扩展]({% link docs/stable/core_extensions/overview.md %}#unsigned-extensions)，请按照以下方式实例化数据库：

```js
db = new duckdb.Database(':memory:', {"allow_unsigned_extensions": "true"});
```