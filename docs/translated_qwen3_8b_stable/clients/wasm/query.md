---
---
layout: docu
redirect_from:
- /docs/api/wasm/query
- /docs/api/wasm/query/
- /docs/clients/wasm/query
title: 查询
---

DuckDB-Wasm 提供了用于查询数据的功能。查询是按顺序执行的。

首先，需要通过调用 [connect](https://shell.duckdb.org/docs/classes/index.AsyncDuckDB.html#connect) 创建一个连接。然后，可以通过调用 [query](https://shell.duckdb.org/docs/classes/index.AsyncDuckDBConnection.html#query) 或 [send](https://shell.duckdb.org/docs/classes/index.AsyncDuckDBConnection.html#send) 来执行查询。

## 查询执行

```ts
// 创建一个新的连接
const conn = await db.connect();

// 可以选择将查询结果物化
await conn.query<{ v: arrow.Int }>(`
    SELECT * FROM generate_series(1, 100) t(v)
`);
// ..., 或者惰性地获取结果块
for await (const batch of await conn.send<{ v: arrow.Int }>(`
    SELECT * FROM generate_series(1, 100) t(v)
`)) {
    // ...
}

// 关闭连接以释放内存
await conn.close();
```

## 预编译语句

```ts
// 创建一个新的连接
const conn = await db.connect();
// 预编译查询
const stmt = await conn.prepare(`SELECT v + ? FROM generate_series(0, 10_000) t(v);`);
// ... 并使用物化的结果运行查询
await stmt.query(234);
// ... 或者结果块
for await (const batch of await stmt.send(234)) {
    // ...
}
// 关闭语句以释放内存
await stmt.close();
// 关闭连接也会释放语句
await conn.close();
```

## Arrow 表转 JSON

```ts
// 创建一个新的连接
const conn = await db.connect();

// 查询
const arrowResult = await conn.query<{ v: arrow.Int }>(`
    SELECT * FROM generate_series(1, 100) t(v)
`);

// 将 Arrow 表转换为 JSON
const result = arrowResult.toArray().map((row) => row.toJSON());

// 关闭连接以释放内存
await conn.close();
```

## 导出 Parquet

```ts
// 创建一个新的连接
const conn = await db.connect();

// 导出 Parquet
conn.send(`COPY (SELECT * FROM tbl) TO 'result-snappy.parquet' (FORMAT parquet);`);
const parquet_buffer = await this._db.copyFileToBuffer('result-snappy.parquet');

// 生成下载链接
const link = URL.createObjectURL(new Blob([parquet_buffer]));

// 关闭连接以释放内存
await conn.close();
```