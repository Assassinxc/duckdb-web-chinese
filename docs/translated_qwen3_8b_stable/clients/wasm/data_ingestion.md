---
---
layout: docu
redirect_from:
- /docs/api/wasm/data_ingestion
- /docs/api/wasm/data_ingestion/
- /docs/clients/wasm/data_ingestion
title: 数据导入
---

DuckDB-Wasm 提供了多种方式导入数据，具体取决于数据的格式。

将数据导入 DuckDB 有两步。

第一步，使用注册函数将数据文件导入到本地文件系统中 ([registerEmptyFileBuffer](https://shell.duckdb.org/docs/classes/index.AsyncDuckDB.html#registerEmptyFileBuffer), [registerFileBuffer](https://shell.duckdb.org/docs/classes/index.AsyncDuckDB.html#registerFileBuffer), [registerFileHandle](https://shell.duckdb.org/docs/classes/index.AsyncDuckDB.html#registerFileHandle), [registerFileText](https://shell.duckdb.org/docs/classes/index.AsyncDuckDB.html#registerFileText), [registerFileURL](https://shell.duckdb.org/docs/classes/index.AsyncDuckDB.html#registerFileURL))。

第二步，使用插入函数将数据文件导入到 DuckDB 中 ([insertArrowFromIPCStream](https://shell.duckdb.org/docs/classes/index.AsyncDuckDBConnection.html#insertArrowFromIPCStream), [insertArrowTable](https://shell.duckdb.org/docs/classes/index.AsyncDuckDBConnection.html#insertArrowTable), [insertCSVFromPath](https://shell.duckdb.org/docs/classes/index.AsyncDuckDBConnection.html#insertCSVFromPath), [insertJSONFromPath](https://shell.duckdb.org/docs/classes/index.AsyncDuckDBConnection.html#insertJSONFromPath)) 或者直接使用 FROM SQL 查询（使用 Parquet 等扩展或 [Wasm 风格 httpfs](#httpfs-wasm-flavored)）。

也可以使用 [插入语句]({% link docs/stable/data/insert.md %}) 来导入数据。

## 数据导入

### 打开 & 关闭连接

```ts
// 创建一个新连接
const c = await db.connect();

// ... 导入数据

// 关闭连接以释放内存
await c.close();
```

### Apache Arrow

```ts
// 可以从现有的 arrow.Table 插入数据
// 更多示例请查看 https://arrow.apache.org/docs/js/
import { tableFromArrays } from 'apache-arrow';

// 根据 Arrow IPC 流格式发送 EOS 信号
// 详见 https://arrow.apache.org/docs/format/Columnar.html#ipc-streaming-format
const EOS = new Uint8Array([255, 255, 255, 255, 0, 0, 0, 0]);

const arrowTable = tableFromArrays({
  id: [1, 2, 3],
  name: ['John', 'Jane', 'Jack'],
  age: [20, 21, 22],
});

await c.insertArrowTable(arrowTable, { name: 'arrow_table' });
// 写入 EOS
await c.insertArrowTable(EOS, { name: 'arrow_table' });

// ..., 从原始 Arrow IPC 流中
const streamResponse = await fetch(`someapi`);
const streamReader = streamResponse.body.getReader();
const streamInserts = [];
while (true) {
    const { value, done } = await streamReader.read();
    if (done) break;
    streamInserts.push(c.insertArrowFromIPCStream(value, { name: 'streamed' }));
}

// 写入 EOS
streamInserts.push(c.insertArrowFromIPCStream(EOS, { name: 'streamed' }));

await Promise.all(streamInserts);
```

### CSV

```ts
// ..., 从 CSV 文件中
// (可互换: registerFile{Text,Buffer,URL,Handle})
const csvContent = '1|foo\n2|bar\n';
await db.registerFileText(`data.csv`, csvContent);
// ... 带类型插入选项
await c.insertCSVFromPath('data.csv', {
    schema: 'main',
    name: 'foo',
    detect: false,
    header: false,
    delimiter: '|',
    columns: {
        col1: new arrow.Int32(),
        col2: new arrow.Utf8(),
    },
});
```

### JSON

```ts
// ..., 从行主序格式的 JSON 文档中
const jsonRowContent = [
    { "col1": 1, "col2": "foo" },
    { "col1": 2, "col2": "bar" },
];
await db.registerFileText(
    'rows.json',
    JSON.stringify(jsonRowContent),
);
await c.insertJSONFromPath('rows.json', { name: 'rows' });

// ... 或列主序格式
const jsonColContent = {
    "col1": [1, 2],
    "col2": ["foo", "bar"]
};
await db.registerFileText(
    'columns.json',
    JSON.stringify(jsonColContent),
);
await c.insertJSONFromPath('columns.json', { name: 'columns' });

// 从 API
const streamResponse = await fetch(`someapi/content.json`);
await db.registerFileBuffer('file.json', new Uint8Array(await streamResponse.arrayBuffer()))
await c.insertJSONFromPath('file.json', { name: 'JSONContent' });
```

### Parquet

```ts
// 从 Parquet 文件中
// ...本地
const pickedFile: File = letUserPickFile();
await db.registerFileHandle('local.parquet', pickedFile, DuckDBDataProtocol.BROWSER_FILEREADER, true);
// ...远程
await db.registerFileURL('remote.parquet', 'https://origin/remote.parquet', DuckDBDataProtocol.HTTP, false);
// ...使用 Fetch
const res = await fetch('https://origin/remote.parquet');
await db.registerFileBuffer('buffer.parquet', new Uint8Array(await res.arrayBuffer()));

// ..., 指定 SQL 文本中的 URL
await c.query(`
    CREATE TABLE direct AS
        SELECT * FROM 'https://origin/remote.parquet'
`);
// ..., 或者执行原始插入语句
await c.query(`
    INSERT INTO existing_table
    VALUES (1, 'foo'), (2, 'bar')`);
```

### httpfs (Wasm 风格)

```ts
// ..., 指定 SQL 文本中的 URL
await c.query(`
    CREATE TABLE direct AS
        SELECT * FROM 'https://origin/remote.parquet'
`);
```

> 提示 如果在尝试从 S3 查询文件时遇到网络错误 (`Failed to execute 'send' on 'XMLHttpRequest'`)，请配置 S3 权限 CORS 头。例如：

```json
[
    {
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "GET",
            "HEAD"
        ],
        "AllowedOrigins": [
            "*"
        ],
        "ExposeHeaders": [],
        "MaxAgeSeconds": 3000
    }
]
```

### 插入语句

```ts
// ..., 或者执行原始插入语句
await c.query(`
    INSERT INTO existing_table
    VALUES (1, 'foo'), (2, 'bar')`);
```