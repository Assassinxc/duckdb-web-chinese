---
layout: docu
redirect_from:
- /docs/api/node_neo/overview
- /docs/api/node_neo/overview/
- /docs/clients/node_neo/overview
title: Node.js 客户端 (Neo)
---

> DuckDB Node.js (Neo) 客户端的最新版本是 {{ site.current_duckdb_node_neo_version }}。

用于在 [Node.js](https://nodejs.org/) 中使用 [DuckDB]({% link index.html %}) 的 API。

主要包，[@duckdb/node-api](https://www.npmjs.com/package/@duckdb/node-api)，是一个高级 API，适用于应用程序。
它依赖于低级绑定，这些绑定紧密遵循 [DuckDB 的 C API]({% link docs/stable/clients/c/overview.md %})，
可单独作为 [@duckdb/node-bindings](https://www.npmjs.com/package/@duckdb/node-bindings) 获取。

## 功能

### 与 [duckdb-node](https://www.npmjs.com/package/duckdb) 的主要区别

* 原生支持 Promise；无需单独的 [duckdb-async](https://www.npmjs.com/package/duckdb-async) 包装器。
* DuckDB 特定的 API；不基于 [SQLite Node API](https://www.npmjs.com/package/sqlite3)。
* 对所有 [DuckDB 数据类型]({% link docs/stable/sql/data_types/overview.md %}) 提供无损且高效的值支持。
* 包裹 [发布版的 DuckDB 二进制文件](https://github.com/duckdb/duckdb/releases) 而不是重新构建 DuckDB。
* 基于 [DuckDB 的 C API]({% link docs/stable/clients/c/overview.md %})；暴露更多功能。

### 开发路线图

一些功能尚未完成：
* 绑定和追加 MAP 和 UNION 数据类型
* 按行追加默认值
* 用户定义的类型和函数
* 性能分析信息
* 表描述
* Arrow API

查看 [GitHub 上的 issue 列表](https://github.com/duckdb/duckdb-node-neo/issues)
获取最新的开发路线图。

### 支持的平台

* Linux arm64
* Linux x64
* Mac OS X (Darwin) arm64 (Apple Silicon)
* Mac OS X (Darwin) x64 (Intel)
* Windows (Win32) x64

## 示例

### 获取基本信息

```ts
import duckdb from '@duckdb/node-api';

console.log(duckdb.version());

console.log(duckdb.configurationOptionDescriptions());
```

### 连接

```ts
import { DuckDBConnection } from '@duckdb/node-api';

const connection = await DuckDBConnection.create();
```

这使用默认实例。
对于高级用法，您可以显式创建实例。

### 创建实例

```ts
import { DuckDBInstance } from '@duckdb/node-api';
```

创建一个内存数据库：
```ts
const instance = await DuckDBInstance.create(':memory:');
```

等同于上面的代码：
```ts
const instance = await DuckDBInstance.create();
```

从数据库文件中读取和写入，如果需要会创建文件：
```ts
const instance = await DuckDBInstance.create('my_duckdb.db');
```

设置 [配置选项]({% link docs/stable/configuration/overview.md %})：
```ts
const instance = await DuckDBInstance.create('my_duckdb.db', {
  threads: '4'
});
```

### 实例缓存

同一进程中的多个实例不应
附加到同一个数据库。

为了防止这种情况，可以使用实例缓存：
```ts
const instance = await DuckDBInstance.fromCache('my_duckdb.db');
```

这使用默认实例缓存。对于高级用法，您可以显式创建
实例缓存：
```ts
import { DuckDBInstanceCache } from '@duckdb/node-api';

const cache = new DuckDBInstanceCache();
const instance = await cache.getOrCreateInstance('my_duckdb.db');
```

### 连接到实例

```ts
const connection = await instance.connect();
```

### 断开连接

连接在引用被丢弃后不久会自动断开，但您也可以显式断开连接（如果需要的话）：

```ts
connection.disconnectSync();
```

或者等效地：

```ts
connection.closeSync();
```

### 运行 SQL

```ts
const result = await connection.run('from test_all_types()');
```

### 参数化 SQL

```ts
const prepared = await connection.prepare('select $1, $2, $3');
prepared.bindVarchar(1, 'duck');
prepared.bindInteger(2, 42);
prepared.bindList(3, listValue([10, 11, 12]), LIST(INTEGER));
const result = await prepared.run();
```

或者：

```ts
const prepared = await connection.prepare('select $a, $b, $c');
prepared.bind({
  'a': 'duck',
  'b': 42,
  'c': listValue([10, 11, 12]),
}, {
  'a': VARCHAR,
  'b': INTEGER,
  'c': LIST(INTEGER),
});
const result = await prepared.run();
```

或者甚至：

```ts
const result = await connection.run('select $a, $b, $c', {
  'a': 'duck',
  'b': 42,
  'c': listValue([10, 11, 12]),
}, {
  'a': VARCHAR,
  'b': INTEGER,
  'c': LIST(INTEGER),
});
```

未指定的类型将被推断：

```ts
const result = await connection.run('select $a, $b, $c', {
  'a': 'duck',
  'b': 42,
  'c': listValue([10, 11, 12]),
});
```

### 指定值

许多数据类型的值使用 JS 原始类型之一表示：
`boolean`、`number`、`bigint` 或 `string`。
此外，任何类型都可以具有 `null` 值。

某些数据类型的值需要使用特殊函数来构建。
这些是：

| 类型 | 函数 |
| ---- | -------- |
| `ARRAY` | `arrayValue` |
| `BIT` | `bitValue` |
| `BLOB` | `blobValue` |
| `DATE` | `dateValue` |
| `DECIMAL` | `decimalValue` |
| `INTERVAL` | `intervalValue` |
| `LIST` | `listValue` |
| `MAP` | `mapValue` |
| `STRUCT` | `structValue` |
| `TIME` | `timeValue` |
| `TIMETZ` | `timeTZValue` |
| `TIMESTAMP` | `timestampValue` |
| `TIMESTAMPTZ` | `timestampTZValue` |
| `TIMESTAMP_S` | `timestampSecondsValue` |
| `TIMESTAMP_MS` | `timestampMillisValue` |
| `TIMESTAMP_NS` | `timestampNanosValue` |
| `UNION` | `unionValue` |
| `UUID` | `uuidValue` |

### 流式结果

流式结果在读取行时进行惰性评估。

```ts
const result = await connection.stream('from range(10_000)');
```

### 检查结果元数据

获取列名和类型：
```ts
const columnNames = result.columnNames();
const columnTypes = result.columnTypes();
```

### 读取结果数据

运行并读取所有数据：
```ts
const reader = await connection.runAndReadAll('from test_all_types()');
const rows = reader.getRows();
// 或者: const columns = reader.getColumns();
```

流式读取并读取至少一定数量的行：
```ts
const reader = await connection.streamAndReadUntil(
  'from range(5000)',
  1000
);
const rows = reader.getRows();
// rows.length === 2048. (行是按 2048 行的块读取的。)
```

逐步读取行：
```ts
const reader = await connection.streamAndRead('from range(5000)');
reader.readUntil(2000);
// reader.currentRowCount === 2048 (行是按 2048 行的块读取的。)
// reader.done === false
reader.readUntil(4000);
// reader.currentRowCount === 4096
// reader.done === false
reader.readUntil(6000);
// reader.currentRowCount === 5000
// reader.done === true
```

### 获取结果数据

结果数据可以以多种形式获取：

```ts
const reader = await connection.runAndReadAll(
  'from range(3) select range::int as i, 10 + i as n'
);

const rows = reader.getRows();
// [ [0, 10], [1, 11], [2, 12] ]

const rowObjects = reader.getRowObjects();
// [ { i: 0, n: 10 }, { i: 1, n: 11 }, { i: 2, n: 12 } ]

const columns = reader.getColumns();
// [ [0, 1, 2], [10, 11, 12] ]

const columnsObject = reader.getColumnsObject();
// { i: [0, 1, 2], n: [10, 11, 12] }
```

### 转换结果数据

默认情况下，无法表示为 JS 原生类型的数据值
将返回为专门的 JS 对象；请参见下面的“检查数据值”。

要以不同的形式获取数据（例如 JS 原生类型或可以无损序列化为 JSON 的值），请使用上述结果数据方法的 `JS` 或 `Json` 形式。

您也可以提供自定义转换器。请参阅 [JSDuckDBValueConverter](https://github.com/duckdb/duckdb-node-neo/blob/main/api/src/JSDuckDBValueConverter.ts)
和 [JsonDuckDBValueConverters](https://github.com/duckdb/duckdb-node-neo/blob/main/api/src/JsonDuckDBValueConverter.ts)
的实现，了解如何做到这一点。

示例（使用 `Json` 形式）：

```ts
const reader = await connection.runAndReadAll(
  'from test_all_types() select bigint, date, interval limit 2'
);

const rows = reader.getRowsJson();
// [
//   [
//     "-9223372036854775808",
//     "5877642-06-25 (BC)",
//     { "months": 0, "days": 0, "micros": "0" }
//   ],
//   [
//     "9223372036854775807",
//     "5881580-07-10",
//     { "months": 999, "days": 999, "micros": "999999999" }
//   ]
// ]

const rowObjects = reader.getRowObjectsJson();
// [
//   {
//     "bigint": "-9223372036854775808",
//     "date": "5877642-06-25 (BC)",
//     "interval": { "months": 0, "days": 0, "micros": "0" }
//   },
//   {
//     "bigint": "9223372036854775807",
//     "date": "5881580-07-10",
//     "interval": { "months": 999, "days": 999, "micros": "999999999" }
//   }
// ]

const columns = reader.getColumnsJson();
// [
//   [ "-9223372036854775808", "9223372036854775807" ],
//   [ "5877642-06-25 (BC)", "5881580-07-10" ],
//   [
//     { "months": 0, "days": 0, "micros": "0" },
//     { "months": 999, "days": 999, "micros": "999999999" }
//   ]
// ]

const columnsObject = reader.getColumnsObjectJson();
// {
//   "bigint": [ "-9223372036854775808", "9223372036854775807" ],
//   "date": [ "5877642-06-25 (BC)", "5881580-07-10" ],
//   "interval": [
//     { "months": 0, "days": 0, "micros": "0" },
//     { "months": 999, "days": 999, "micros": "999999999" }
//   ]
// }
```

这些方法还处理嵌套类型：

```ts
const reader = await connection.runAndReadAll(
  'from test_all_types() select int_array, struct, map, "union" limit 2'
);

const rows = reader.getRowsJson();
// [
//   [
//     [],
//     { "a": null, "b": null },
//     [],
//     { "tag": "name", "value": "Frank" }
//   ],
//   [
//     [ 42, 999, null, null, -42],
//     { "a": 42, "b": "🦆🦆🦆🦆🦆🦆" },
//     [
//       { "key": "key1", "value": "🦆🦆🦆🦆🦆🦆" },
//       { "key": "key2", "value": "goose" }
//     ],
//     { "tag": "age", "value": 5 }
//   ]
// ]

const rowObjects = reader.getRowObjectsJson();
// [
//   {
//     "int_array": [],
//     "struct": { "a": null, "b": null },
//     "map": [],
//     "union": { "tag": "name", "value": "Frank" }
//   },
//   {
//     "int_array": [ 42, 999, null, null, -43 ],
//     "struct": { "a": 42, "b": "🦆🦆🦆🦆🦆🦆" },
//     "map": [
//       { "key": "key1", "value": "🦆🦆🦆🦆🦆🦆" },
//       { "key": "key2", "value": "goose" }
//     ],
//     "union": { "tag": "age", "value": 5 }
//   }
// ]

const columns = reader.getColumnsJson();
// [
//   [
//     [],
//     [42, 999, null, null, -42]
//   ],
//   [
//     { "a": null, "b": null },
//     { "a": 42, "b": "🦆🦆🦆🦆🦆🦆" }
//   ],
//   [
//     [],
//     [
//       { "key": "key1", "value": "🦆🦆🦆🦆🦆🦆" },
//       { "key": "key2", "value": "goose" }
//     ]
//   ],
//   [
//     { "tag": "name", "value": "Frank" },
//     { "tag": "age", "value": 5 }
//   ]
// ]

const columnsObject = reader.getColumnsObjectJson();
// {
//   "int_array": [
//     [],
//     [42, 999, null, null, -42]
//   ],
//   "struct": [
//     { "a": null, "b": null },
//     { "a": 42, "b": "🦆🦆🦆🦆🦆🦆" }
//   ],
//   "map": [
//     [],
//     [
//       { "key": "key1", "value": "🦆🦆🦆🦆🦆🦆" },
//       { "key": "key2", "value": "goose" }
//     ]
//   ],
//   "union": [
//     { "tag": "name", "value": "Frank" },
//     { "tag": "age", "value": 5 }
//   ]
// }
```

列名和类型也可以序列化为 JSON：
```ts
const columnNamesAndTypes = reader.columnNamesAndTypesJson();
// {
//   "columnNames": [
//     "int_array",
//     "struct",
//     "map",
//     "union"
//   ],
//   "columnTypes": [
//     {
//       "typeId": 24,
//       "valueType": {
//         "typeId": 4
//       }
//     },
//     {
//       "typeId": 25,
//       "entryNames": [
//         "a",
//         "b"
//       ],
//       "entryTypes": [
//         {
//           "typeId": 4
//         },
//         {
//           "typeId": 17
//         }
//       ]
//     },
//     {
//       "typeId": 26,
//       "keyType": {
//         "typeId": 17
//       },
//       "valueType": {
//         "typeId": 17
//       }
//     },
//     {
//       "typeId": 28,
//       "memberTags": [
//         "name",
//         "age"
//       ],
//       "memberTypes": [
//         {
//           "typeId": 17
//         },
//         {
//           "typeId": 3
//         }
//       ]
//     }
//   ]
// }

const columnNameAndTypeObjects = reader.columnNameAndTypeObjectsJson();
// [
//   {
//     "columnName": "int_array",
//     "columnType": {
//       "typeId": 24,
//       "valueType": {
//         "typeId": 4
//       }
//     }
//   },
//   {
//     "columnName": "struct",
//     "columnType": {
//       "typeId": 25,
//       "entryNames": [
//         "a",
//         "b"
//       ],
//       "entryTypes": [
//         {
//           "typeId": 4
//         },
//         {
//           "typeId": 17
//         }
//       ]
//     }
//   },
//   {
//     "columnName": "map",
//     "columnType": {
//       "typeId": 26,
//       "keyType": {
//         "typeId": 17
//       },
//       "valueType": {
//         "typeId": 17
//       }
//     }
//   },
//   {
//     "columnName": "union",
//     "columnType": {
//       "typeId": 28,
//       "memberTags": [
//         "name",
//         "age"
//       ],
//       "memberTypes": [
//         {
//           "typeId": 17
//         },
//         {
//           "typeId": 3
//         }
//       ]
//     }
//   }
// ]
```

### 获取数据块

获取所有数据块：
```ts
const chunks = await result.fetchAllChunks();
```

逐个获取数据块：
```ts
const chunks = [];
while (true) {
  const chunk = await result.fetchChunk();
  // 最后一个数据块将包含零行。
  if (chunk.rowCount === 0) {
    break;
  }
  chunks.push(chunk);
}
```

对于物化（非流式）结果，可以通过索引读取数据块：
```ts
const rowCount = result.rowCount;
const chunkCount = result.chunkCount;
for (let i = 0; i < chunkCount; i++) {
  const chunk = result.getChunk(i);
  // ...
}
```

获取数据块数据：
```ts
const rows = chunk.getRows();

const rowObjects = chunk.getRowObjects(result.deduplicatedColumnNames());

const columns = chunk.getColumns();

const columnsObject =
  chunk.getColumnsObject(result.deduplicatedColumnNames());
```

逐个获取数据块数据（一个值一个值地获取）
```ts
const columns = [];
const columnCount = chunk.columnCount;
for (let columnIndex = 0; columnIndex < columnCount; columnIndex++) {
  const columnValues = [];
  const columnVector = chunk.getColumnVector(columnIndex);
  const itemCount = columnVector.itemCount;
  for (let itemIndex = 0; itemIndex < itemCount; itemIndex++) {
    const value = columnVector.getItem(itemIndex);
    columnValues.push(value);
  }
  columns.push(columnValues);
}
```

### 检查数据类型

```ts
import { DuckDBTypeId } from '@duckdb/node-api';

if (columnType.typeId === DuckDBTypeId.ARRAY) {
  const arrayValueType = columnType.valueType;
  const arrayLength = columnType.length;
}

if (columnType.typeId === DuckDBTypeId.DECIMAL) {
  const decimalWidth = columnType.width;
  const decimalScale = columnType.scale;
}

if (columnType.typeId === DuckDBTypeId.ENUM) {
  const enumValues = columnType.values;
}

if (columnType.typeId === DuckDBTypeId.LIST) {
  const listValueType = columnType.valueType;
}

if (columnType.typeId === DuckDBTypeId.MAP) {
  const mapKeyType = columnType.keyType;
  const mapValueType = columnType.valueType;
}

if (columnType.typeId === DuckDBTypeId.STRUCT) {
  const structEntryNames = columnType.names;
  const structEntryTypes = columnType.valueTypes;
}

if (columnType.typeId === DuckDBTypeId.UNION) {
  const unionMemberTags = columnType.memberTags;
  const unionMemberTypes = columnType.memberTypes;
}

// 对于 JSON 类型（https://duckdb.org/docs/data/json/json_type）
if (columnType.alias === 'JSON') {
  const json = JSON.parse(columnValue);
}
```

每个类型都实现了 toString。
结果对人类友好，并且可以被 DuckDB 以适当表达式读取。

```ts
const typeString = columnType.toString();
```

### 检查数据值

```ts
import { DuckDBTypeId } from '@duckdb/node-api';

if (columnType.typeId === DuckDBTypeId.ARRAY) {
  const arrayItems = columnValue.items; // 值数组
  const arrayString = columnValue.toString();
}

if (columnType.typeId === DuckDBTypeId.BIT) {
  const bools = columnValue.toBools(); // 布尔数组
  const bits = columnValue.toBits(); // 0 和 1 的数组
  const bitString = columnValue.toString(); // '0' 和 '1' 的字符串
}

if (columnType.typeId === DuckDBTypeId.BLOB) {
  const blobBytes = columnValue.bytes; // Uint8Array
  const blobString = columnValue.toString();
}

if (columnType.typeId === DuckDBTypeId.DATE) {
  const dateDays = columnValue.days;
  const dateString = columnValue.toString();
  const { year, month, day } = columnValue.toParts();
}

if (columnType.typeId === DuckDBTypeId.DECIMAL) {
  const decimalWidth = columnValue.width;
  const decimalScale = columnValue.scale;
  // 扩展后的值。表示的数字是 value/(10^scale)。
  const decimalValue = columnValue.value; // bigint
  const decimalString = columnValue.toString();
  const decimalDouble = columnValue.toDouble();
}

if (columnType.typeId === DuckDBTypeId.INTERVAL) {
  const intervalMonths = columnValue.months;
  const intervalDays = columnValue.days;
  const intervalMicros = columnValue.micros; // bigint
  const intervalString = columnValue.toString();
}

if (columnType.typeId === DuckDBTypeId.LIST) {
  const listItems = columnValue.items; // 值数组
  const listString = columnValue.toString();
}

if (columnType.typeId === DuckDBTypeId.MAP) {
  const mapEntries = columnValue.entries; // { key, value } 数组
  const mapString = columnValue.toString();
}

if (columnType.typeId === DuckDBTypeId.STRUCT) {
  // { name1: value1, name2: value2, ... }
  const structEntries = columnValue.entries;
  const structString = columnValue.toString();
}

if (columnType.typeId === DuckDBTypeId.TIMESTAMP_MS) {
  const timestampMillis = columnValue.milliseconds; // bigint
  const timestampMillisString = columnValue.toString();
}

if (columnType.typeId === DuckDBTypeId.TIMESTAMP_NS) {
  const timestampNanos = columnValue.nanoseconds; // bigint
  const timestampNanosString = columnValue.toString();
}

if (columnType.typeId === DuckDBTypeId.TIMESTAMP_S) {
  const timestampSecs = columnValue.seconds; // bigint
  const timestampSecsString = columnValue.toString();
}

if (columnType.typeId === DuckDBTypeId.TIMESTAMP_TZ) {
  const timestampTZMicros = columnValue.micros; // bigint
  const timestampTZString = columnValue.toString();
  const {
    date: { year, month, day },
    time: { hour, min, sec, micros },
  } = columnValue.toParts();
}

if (columnType.typeId === DuckDBTypeId.TIMESTAMP) {
  const timestampMicros = columnValue.micros; // bigint
  const timestampString = columnValue.toString();
  const {
    date: { year, month, day },
    time: { hour, min, sec, micros },
  } = columnValue.toParts();
}

if (columnType.typeId === DuckDBTypeId.TIME_TZ) {
  const timeTZMicros = columnValue.micros; // bigint
  const timeTZOffset = columnValue.offset;
  const timeTZString = columnValue.toString();
  const {
    time: { hour, min, sec, micros },
    offset,
  } = columnValue.toParts();
}

if (columnType.typeId === DuckDBTypeId.TIME) {
  const timeMicros = columnValue.micros; // bigint
  const timeString = columnValue.toString();
  const { hour, min, sec, micros } = columnValue.toParts();
}

if (columnType.typeId === DuckDBTypeId.UNION) {
  const unionTag = columnValue.tag;
  const unionValue = columnValue.value;
  const unionValueString = columnValue.toString();
}

if (columnType.typeId === DuckDBTypeId.UUID) {
  const uuidHugeint = columnValue.hugeint; // bigint
  const uuidString = columnValue.toString();
}

// 其他可能的值是：null、boolean、number、bigint 或 string
```

### 显示时区

将 TIMESTAMP_TZ 值转换为字符串取决于时区偏移。
默认情况下，此偏移设置为 Node 进程启动时的本地时区偏移。

要更改此设置，请设置 `DuckDBTimestampTZValue` 的 `timezoneOffsetInMinutes` 属性：

```ts
DuckDBTimestampTZValue.timezoneOffsetInMinutes = -8 * 60;
const pst = DuckDBTimestampTZValue.Epoch.toString();
// 1969-12-31 16:00:00-08

DuckDBTimestampTZValue.timezoneOffsetInMinutes = +1 * 60;
const cet = DuckDBTimestampTZValue.Epoch.toString();
// 1970-01-01 01:00:00+01
```

注意，用于此字符串转换的时区偏移与 DuckDB 的 `TimeZone` 设置是不同的。

以下设置此偏移以匹配 DuckDB 的 `TimeZone` 设置：

```ts
const reader = await connection.runAndReadAll(
  `select (timezone(current_timestamp) / 60)::int`
);
DuckDBTimestampTZValue.timezoneOffsetInMinutes =
  reader.getColumns()[0][0];
```

### 追加到表

```ts
await connection.run(
  `create or replace table target_table(i integer, v varchar)`
);

const appender = await connection.createAppender('target_table');

appender.appendInteger(42);
appender.appendVarchar('duck');
appender.endRow();

appender.appendInteger(123);
appender.appendVarchar('mallard');
appender.endRow();

appender.flushSync();

appender.appendInteger(17);
appender.appendVarchar('goose');
appender.endRow();

appender.closeSync(); // 也会刷新
```

### 追加数据块

```ts
await connection.run(
  `create or replace table target_table(i integer, v varchar)`
);

const appender = await connection.createAppender('target_table');

const chunk = DuckDBDataChunk.create([INTEGER, VARCHAR]);
chunk.setColumns([
  [42, 123, 17],
  ['duck', 'mallad', 'goose'],
]);
// 或者：
// chunk.setRows([
//   [42, 'duck'],
//   [12, 'mallard'],
//   [17, 'goose'],
// ]);

appender.appendDataChunk(chunk);
appender.flushSync();
```

查看上面的“指定值”部分，了解如何向追加器提供值。

### 提取语句

```ts
const extractedStatements = await connection.extractStatements(`
  create or replace table numbers as from range(?);
  from numbers where range < ?;
  drop table numbers;
`);
const parameterValues = [10, 7];
const statementCount = extractedStatements.count;
for (let stmtIndex = 0; stmtIndex < statementCount; stmtIndex++) {
  const prepared = await extractedStatements.prepare(stmtIndex);
  let parameterCount = prepared.parameterCount;
  for (let paramIndex = 1; paramIndex <= parameterCount; paramIndex++) {
    prepared.bindInteger(paramIndex, parameterValues.shift());
  }
  const result = await prepared.run();
  // ...
}
```

### 控制任务的评估

```ts
import { DuckDBPendingResultState } from '@duckdb/node-api';

async function sleep(ms) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

const prepared = await connection.prepare('from range(10_000_000)');
const pending = prepared.start();
while (pending.runTask() !== DuckDBPendingResultState.RESULT_READY) {
  console.log('not ready');
  await sleep(1);
}
console.log('ready');
const result = await pending.getResult();
// ...
```

### 运行 SQL 的方法

```ts
// 运行直到完成，但尚未检索任何行。
// 可选地传入要绑定到 SQL 参数的值，
// 和（可选）这些参数的类型，
// 作为数组（用于位置参数）
// 或者一个键名参数的对象。
const result = await connection.run(sql);
const result = await connection.run(sql, values);
const result = await connection.run(sql, values, types);

// 运行直到完成，但尚未检索任何行。
// 包装在 DuckDBDataReader 中以方便数据检索。
const reader = await connection.runAndRead(sql);
const reader = await connection.runAndRead(sql, values);
const reader = await connection.runAndRead(sql, values, types);

// 运行直到完成，包装在 reader 中并读取所有行。
const reader = await connection.runAndReadAll(sql);
const reader = await connection.runAndReadAll(sql, values);
const reader = await connection.runAndReadAll(sql, values, types);

// 运行直到完成，包装在 reader 中并读取至少
// 指定的行数。 (行是按块读取的，因此可能读取的行数超过目标。)
const reader = await connection.runAndReadUntil(sql, targetRowCount);
const reader =
  await connection.runAndReadAll(sql, targetRowCount, values);
const reader =
  await connection.runAndReadAll(sql, targetRowCount, values, types);

// 创建流式结果，但尚未检索任何行。
const result = await connection.stream(sql);
const result = await connection.stream(sql, values);
const result = await connection.stream(sql, values, types);

// 创建流式结果，但尚未检索任何行。
// 包装在 DuckDBDataReader 中以方便数据检索。
const reader = await connection.streamAndRead(sql);
const reader = await connection.streamAndRead(sql, values);
const reader = await connection.streamAndRead(sql, values, types);

// 创建流式结果，包装在 reader 中并读取所有行。
const reader = await connection.streamAndReadAll(sql);
const reader = await connection.streamAndReadAll(sql, values);
const reader = await connection.streamAndReadAll(sql, values, types);

// 创建流式结果，包装在 reader 中并读取至少
// 指定的行数。
const reader = await connection.streamAndReadUntil(sql, targetRowCount);
const reader =
  await connection.streamAndReadUntil(sql, targetRowCount, values);
const reader =
  await connection.streamAndReadUntil(sql, targetRowCount, values, types);

// 预编译语句

// 预编译一个可能带参数的 SQL 语句供以后运行。
const prepared = await connection.prepare(sql);

// 绑定值到参数。
prepared.bind(values);
prepared.bind(values, types);

// 运行预编译语句。这些方法与连接上的方法相匹配。
const result = prepared.run();

const reader = prepared.runAndRead();
const reader = prepared.runAndReadAll();
const reader = prepared.runAndReadUntil(targetRowCount);

const result = prepared.stream();

const reader = prepared.streamAndRead();
const reader = prepared.streamAndReadAll();
const reader = prepared.streamAndReadUntil(targetRowCount);

// 悬挂结果

// 创建一个悬挂结果。
const pending = await connection.start(sql);
const pending = await connection.start(sql, values);
const pending = await connection.start(sql, values, types);

// 创建一个悬挂、流式结果。
const pending = await connection.startStream(sql);
const pending = await connection.startStream(sql, values);
const pending = await connection.startStream(sql, values, types);

// 从预编译语句创建一个悬挂结果。
const pending = await prepared.start();
const pending = await prepared.startStream();

while (pending.runTask() !== DuckDBPendingResultState.RESULT_READY) {
  // 可选地在任务之间睡眠或执行其他工作
}

// 获取结果。如果尚未准备好，则会运行直到准备好。
const result = await pending.getResult();

const reader = await pending.read();
const reader = await pending.readAll();
const reader = await pending.readUntil(targetRowCount);
```

### 获取结果数据的方法

```ts
// 从结果

// 异步获取所有行的数据：
const columns = await result.getColumns();
const columnsJson = await result.getColumnsJson();
const columnsObject = await result.getColumnsObject();
const columnsObjectJson = await result.getColumnsObjectJson();
const rows = await result.getRows();
const rowsJson = await result.getRowsJson();
const rowObjects = await result.getRowObjects();
const rowObjectsJson = await result.getRowObjectsJson();

// 从 reader

// 首先（异步）读取一些行：
await reader.readAll();
// 或者：
await reader.readUntil(targetRowCount);

// 然后（同步）获取已读行的结果数据：
const columns = reader.getColumns();
const columnsJson = reader.getColumnsJson();
const columnsObject = reader.getColumnsObject();
const columnsObjectJson = reader.getColumnsObjectJson();
const rows = reader.getRows();
const rowsJson = reader.getRowsJson();
const rowObjects = reader.getRowObjects();
const rowObjectsJson = reader.getRowObjectsJson();

// 也可以直接读取单个值：
const value = reader.value(columnIndex, rowIndex);

// 使用数据块

// 如果需要，可以从结果中获取一个或多个数据块：
const chunk = await result.fetchChunk();
const chunks = await result.fetchAllChunks();

// 然后可以从每个数据块中获取数据：
const columnValues = chunk.getColumnValues(columnIndex);
const columns = chunk.getColumns();
const rowValues = chunk.getRowValues(rowIndex);
const rows = chunk.getRows();

// 或者，可以遍历值：
chunk.visitColumnValues(columnIndex,
  (value, rowIndex, columnIndex, type) => { /* ... */ }
);
chunk.visitColumns((column, columnIndex, type) => { /* ... */ });
chunk.visitColumnMajor(
  (value, rowIndex, columnIndex, type) => { /* ... */ }
);
chunk.visitRowValues(rowIndex,
  (value, rowIndex, columnIndex, type) => { /* ... */ }
);
chunk.visitRows((row, rowIndex) => { /* ... */ });
chunk.visitRowMajor(
  (value, rowIndex, columnIndex, type) => { /* ... */ }
);

// 或者转换：
// `converter` 参数实现了 `DuckDBValueConverter`，
// 其中包含单个方法 convertValue(value, type)。
const columnValues = chunk.convertColumnValues(columnIndex, converter);
const columns = chunk.convertColumns(converter);
const rowValues = chunk.convertRowValues(rowIndex, converter);
const rows = chunk.convertRows(converter);

// 读者抽象了这些低级的数据块操作
// 并且推荐用于大多数情况。
```