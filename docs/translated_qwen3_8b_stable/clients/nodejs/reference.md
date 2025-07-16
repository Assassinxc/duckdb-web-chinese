---
layout: docu
redirect_from:
- /docs/api/nodejs/reference
- /docs/api/nodejs/reference/
- /docs/clients/nodejs/reference
title: Node.js API
---

## 模块

<dl>
<dt><a href="#module_duckdb">duckdb</a></dt>
<dd></dd>
</dl>

## 类型定义

<dl>
<dt><a href="#ColumnInfo">ColumnInfo</a> : <code>object</code></dt>
<dd></dd>
<dt><a href="#TypeInfo">TypeInfo</a> : <code>object</code></dt>
<dd></dd>
<dt><a href="#DuckDbError">DuckDbError</a> : <code>object</code></dt>
<dd></dd>
<dt><a href="#HTTPError">HTTPError</a> : <code>object</code></dt>
<dd></dd>
</dl>

<a name="module_duckdb"></a>

## duckdb

**摘要**: DuckDB 是一个可嵌入的 SQL OLAP 数据库管理系统  

* [duckdb](#module_duckdb)
    * [~Connection](#module_duckdb..Connection)
        * [.run(sql, ...params, callback)](#module_duckdb..Connection+run) ⇒ <code>void</code>
        * [.all(sql, ...params, callback)](#module_duckdb..Connection+all) ⇒ <code>void</code>
        * [.arrowIPCAll(sql, ...params, callback)](#module_duckdb..Connection+arrowIPCAll) ⇒ <code>void</code>
        * [.arrowIPCStream(sql, ...params, callback)](#module_duckdb..Connection+arrowIPCStream) ⇒
        * [.each(sql, ...params, callback)](#module_duckdb..Connection+each) ⇒ <code>void</code>
        * [.stream(sql, ...params)](#module_duckdb..Connection+stream)
        * [.register_udf(name, return_type, fun)](#module_duckdb..Connection+register_udf) ⇒ <code>void</code>
        * [.prepare(sql, ...params, callback)](#module_duckdb..Connection+prepare) ⇒ <code>Statement</code>
        * [.exec(sql, ...params, callback)](#module_duckdb..Connection+exec) ⇒ <code>void</code>
        * [.register_udf_bulk(name, return_type, callback)](#module_duckdb..Connection+register_udf_bulk) ⇒ <code>void</code>
        - [.unregister_udf(name, return_type, callback)](#module_duckdb..Connection+unregister_udf) ⇒ <code>void</code>
        * [.register_buffer(name, array, force, callback)](#module_duckdb..Connection+register_buffer) ⇒ <code>void</code>
        * [.unregister_buffer(name, callback)](#module_duckdb..Connection+unregister_buffer) ⇒ <code>void</code>
        * [.close(callback)](#module_duckdb..Connection+close) ⇒ <code>void</code>
    * [~Statement](#module_duckdb..Statement)
        * [.sql](#module_duckdb..Statement+sql) ⇒
        * [.get()](#module_duckdb..Statement+get)
        * [.run(sql, ...params, callback)](#module_duckdb..Statement+run) ⇒ <code>void</code>
        * [.all(sql, ...params, callback)](#module_duckdb..Statement+all) ⇒ <code>void</code>
        * [.arrowIPCAll(sql, ...params, callback)](#module_duckdb..Statement+arrowIPCAll) ⇒ <code>void</code>
        * [.each(sql, ...params, callback)](#module_duckdb..Statement+each) ⇒ <code>void</code>
        * [.finalize(sql, ...params, callback)](#module_duckdb..Statement+finalize) ⇒ <code>void</code>
        * [.stream(sql, ...params)](#module_duckdb..Statement+stream)
        * [.columns()](#module_duckdb..Statement+columns) ⇒ [<code>Array.&lt;ColumnInfo&gt;</code>](#ColumnInfo)
    * [~QueryResult](#module_duckdb..QueryResult)
        * [.nextChunk()](#module_duckdb..QueryResult+nextChunk) ⇒
        * [.nextIpcBuffer()](#module_duckdb..QueryResult+nextIpcBuffer) ⇒
        * [.asyncIterator()](#module_duckdb..QueryResult+asyncIterator)
    * [~Database](#module_duckdb..Database)
        * [.close(callback)](#module_duckdb..Database+close) ⇒ <code>void</code>
        * [.close_internal(callback)](#module_duckdb..Database+close_internal) ⇒ <code>void</code>
        * [.wait(callback)](#module_duckdb..Database+wait) ⇒ <code>void</code>
        * [.serialize(callback)](#module_duckdb..Database+serialize) ⇒ <code>void</code>
        * [.parallelize(callback)](#module_duckdb..Database+parallelize) ⇒ <code>void</code>
        * [.connect(path)](#module_duckdb..Database+connect) ⇒ <code>Connection</code>
        * [.interrupt(callback)](#module_duckdb..Database+interrupt) ⇒ <code>void</code>
        * [.prepare(sql)](#module_duckdb..Database+prepare) ⇒ <code>Statement</code>
        * [.run(sql, ...params, callback)](#module_duckdb..Database+run) ⇒ <code>void</code>
        * [.scanArrowIpc(sql, ...params, callback)](#module_duckdb..Database+scanArrowIpc) ⇒ <code>void</code>
        * [.each(sql, ...params, callback)](#module_duckdb..Database+each) ⇒ <code>void</code>
        * [.stream(sql, ...params)](#module_duckdb..Database+stream)
        * [.all(sql, ...params, callback)](#module_duckdb..Database+all) ⇒ <code>void</code>
        * [.arrowIPCAll(sql, ...params, callback)](#module_duckdb..Database+arrowIPCAll) ⇒ <code>void</code>
        * [.arrowIPCStream(sql, ...params, callback)](#module_duckdb..Database+arrowIPCStream) ⇒ <code>void</code>
        * [.exec(sql, ...params, callback)](#module_duckdb..Database+exec) ⇒ <code>void</code>
        * [.register_udf(name, return_type, fun)](#module_duckdb..Database+register_udf) ⇒ <code>this</code>
        * [.register_buffer(name)](#module_duckdb..Database+register_buffer) ⇒ <code>this</code>
        * [.unregister_buffer(name)](#module_duckdb..Database+unregister_buffer) ⇒ <code>this</code>
        * [.unregister_udf(name)](#module_duckdb..Database+unregister_ud, ⇒ <code>this</code>
        * [.registerReplacementScan(fun)](#module_duckdb..Database+registerReplacementScan) ⇒ <code>this</code>
        * [.tokenize(text)](#module_duckdb..Database+tokenize) ⇒ <code>ScriptTokens</code>
        * [.get()](#module_duckdb..Database+get)
    * [~TokenType](#module_duckdb..TokenType)
    * [~ERROR](#module_duckdb..ERROR) : <code>number</code>
    * [~OPEN_READONLY](#module_duckdb..OPEN_READONLY) : <code>number</code>
    * [~OPEN_READWRITE](#module_duckdb..OPEN_READWRITE) : <code>number</code>
    * [~OPEN_CREATE](#module_duckdb..OPEN_CREATE) : <code>number</code>
    * [~OPEN_FULLMUTEX](#module_duckdb..OPEN_FULLMUTEX) : <code>number</code>
    * [~OPEN_SHAREDCACHE](#module_duckdb..OPEN_SHAREDCACHE) : <code>number</code>
    * [~OPEN_PRIVATECACHE](#module_duckdb..OPEN_PRIVATECACHE) : <code>number</code>

<a name="module_duckdb..Connection"></a>

### duckdb~Connection

**类型**: duckdb 的内部类  

* [~Connection](#module_duckdb..Connection)
    * [.run(sql, ...params, callback)](#module_duckdb..Connection+run) ⇒ <code>void</code>
    * [.all(sql, ...params, callback)](#module_duckdb..Connection+all) ⇒ <code>void</code>
    * [.arrowIPCAll(sql, ...params, callback)](#module_duckdb..Connection+arrowIPCAll) ⇒ <code>void</code>
    * [.arrowIPCStream(sql, ...params, callback)](#module_duckdb..Connection+arrowIPCStream) ⇒
    * [.each(sql, ...params, callback)](#module_duckdb..Connection+each) ⇒ <code>void</code>
    * [.stream(sql, ...params)](#module_duckdb..Connection+stream)
    * [.register_udf(name, return_type, fun)](#module_duckdb..Connection+register_udf) ⇒ <code>void</code>
    * [.prepare(sql, ...params, callback)](#module_duckdb..Connection+prepare) ⇒ <code>Statement</code>
    * [.exec(sql, ...params, callback)](#module_duckdb..Connection+exec) ⇒ <code>void</code>
    * [.register_udf_bulk(name, return_type, callback)](#module_duckdb..Connection+register_udf_bulk) ⇒ <code>void</code>
    * [.unregister_udf(name, return_type, callback)](#module_duckdb..Connection+unregister_udf) ⇒ <code>void</code>
    * [.register_buffer(name, array, force, callback)](#module_duckdb..Connection+register_buffer) ⇒ <code>void</code>
    * [.unregister_buffer(name, callback)](#module_duckdb..Connection+unregister_buffer) ⇒ <code>void</code>
    * [.close(callback)](#module_duckdb..Connection+close) ⇒ <code>void</code>

<a name="module_duckdb..Connection+run"></a>

#### connection.run(sql, ...params, callback) ⇒ <code>void</code>

运行 SQL 语句并在完成时触发回调

**类型**: [Connection](#module_duckdb..Connection) 的实例方法  

| 参数 | 类型 |
| --- | --- |
| sql |  |
| ...params | <code>\*</code> |
| callback |  |

<a name="module_duckdb..Connection+all"></a>

#### connection.all(sql, ...params, callback) ⇒ <code>void</code>

运行 SQL 查询，并为所有结果行触发回调

**类型**: [Connection](#module_duckdb..Connection) 的实例方法  

| 参数 | 类型 |
| --- | --- |
| sql |  |
| ...params | <code>\*</code> |
| callback |  |

<a name="module_duckdb..Connection+arrowIPCAll"></a>

#### connection.arrowIPCAll(sql, ...params, callback) ⇒ <code>void</code>

运行 SQL 查询，并将结果序列化为 Apache Arrow IPC 格式（需要加载 arrow 扩展）

**类型**: [Connection](#module_duckdb..Connection) 的实例方法  

| 参数 | 类型 |
| --- | --- |
| sql |  |
| ...params | <code>\*</code> |
| callback |  |

<a name="module_duckdb..Connection+arrowIPCStream"></a>

#### connection.arrowIPCStream(sql, ...params, callback) ⇒

运行 SQL 查询，返回一个 IpcResultStreamIterator，允许将结果流式传输到 Apache Arrow IPC 格式（需要加载 arrow 扩展）

**类型**: [Connection](#module_duckdb..Connection) 的实例方法  
**返回**: Promise<IpcResultStreamIterator>  

| 参数 | 类型 |
| --- | --- |
| sql |  |
| ...params | <code>\*</code> |
| callback |  |

<a name="module_duckdb..Connection+each"></a>

#### connection.each(sql, ...params, callback) ⇒ <code>void</code>

运行 SQL 查询，并为每个结果行触发回调

**类型**: [Connection](#module_duckdb..Connection) 的实例方法  

| 参数 | 类型 |
| --- | --- |
| sql |  |
| ...params | <code>\*</code> |
| callback |  |

<a name="module_duckdb..Connection+stream"></a>

#### connection.stream(sql, ...params)

**类型**: [Connection](#module_duckdb..Connection) 的实例方法  

| 参数 | 类型 |
| --- | --- |
| sql |  |
| ...params | <code>\*</code> |

<a name="module_duckdb..Connection+register_udf"></a>

#### connection.register_udf(name, return_type, fun) ⇒ <code>void</code>

注册一个用户自定义函数

**类型**: [Connection](#module_duckdb..Connection) 的实例方法  
**注意**: 这与 wasm udfs 类似，但由于我们可以更清晰地传递数据，所以更简单  

| 参数 |
| --- |
| name |
| return_type |
| fun |

<a name="module_duckdb..Connection+prepare"></a>

#### connection.prepare(sql, ...params, callback) ⇒ <code>Statement</code>

为执行准备 SQL 查询

**类型**: [Connection](#module_duckdb..Connection) 的实例方法  

| 参数 | 类型 |
| --- | --- |
| sql |  |
| ...params | <code>\*</code> |
| callback |  |

<a name="module_duckdb..Connection+exec"></a>

#### connection.exec(sql, ...params, callback) ⇒ <code>void</code>

执行 SQL 查询

**类型**: [Connection](#module_duckdb..Connection) 的实例方法  

| 参数 | 类型 |
| --- | --- |
| sql |  |
| ...params | <code>\*</code> |
| callback |  |

<a name="module_duckdb..Connection+register_udf_bulk"></a>

#### connection.register_udf_bulk(name, return_type, callback) ⇒ <code>void</code>

注册一个用户自定义函数

**类型**: [Connection](#module_duckdb..Connection) 的实例方法  

| 参数 |
| --- |
| name |
| return_type |
| callback |

<a name="module_duckdb..Connection+unregister_udf"></a>

#### connection.unregister_udf(name, return_type, callback) ⇒ <code>void</code>

取消注册一个用户自定义函数

**类型**: [Connection](#module_duckdb..Connection) 的实例方法  

| 参数 |
| --- |
| name |
| return_type |
| callback |

<a name="module_duckdb..Connection+register_buffer"></a>

#### connection.register_buffer(name, array, force, callback) ⇒ <code>void</code>

注册一个缓冲区，以便使用 Apache Arrow IPC 扫描器进行扫描（需要加载 arrow 扩展）

**类型**: [Connection](#module_duckdb..Connection) 的实例方法  

| 参数 |
| --- |
| name |
| array |
| force |
| callback |

<a name="module_duckdb..Connection+unregister_buffer"></a>

#### connection.unregister_buffer(name, callback) ⇒ <code>void</code>

取消注册缓冲区

**类型**: [Connection](#module_duckdb..Connection) 的实例方法  

| 参数 |
| --- |
| name |
| callback |

<a name="module_duckdb..Connection+close"></a>

#### connection.close(callback) ⇒ <code>void</code>

关闭连接

**类型**: [Connection](#module_duckdb..Connection) 的实例方法  

| 参数 |
| --- |
| callback |

<a name="module_duckdb..Statement"></a>

### duckdb~Statement

**类型**: duckdb 的内部类  

* [~Statement](#module_duckdb..Statement)
    * [.sql](#module_duckdb..Statement+sql) ⇒
    * [.get()](#module_duckdb..Statement+get)
    * [.run(sql, ...params, callback)](#module_duckdb..Statement+run) ⇒ <code>void</code>
    * [.all(sql, ...params, callback)](#module_duckdb..Statement+all) ⇒ <code>void</code>
    * [.arrowIPCAll(sql, ...params, callback)](#module_duckdb..Statement+arrowIPCAll) ⇒ <code>void</code>
    * [.each(sql, ...params, callback)](#module_duckdb..Statement+each) ⇒ <code>void</code>
    * [.finalize(sql, ...params, callback)](#module_duckdb..Statement+finalize) ⇒ <code>void</code>
    * [.stream(sql, ...params)](#module_duckdb..Statement+stream)
    * [.columns()](#module_duckdb..Statement+columns) ⇒ [<code>Array.&lt;ColumnInfo&gt;</code>](#ColumnInfo)

<a name="module_duckdb..Statement+sql"></a>

#### statement.sql ⇒

**类型**: [Statement](#module_duckdb..Statement) 的实例属性  
**返回**: 语句中包含的 SQL  
**字段**:   
<a name="module_duckdb..Statement+get"></a>

#### statement.get()

未实现

**类型**: [Statement](#module_duckdb..Statement) 的实例方法  
<a name="module_duckdb..Statement+run"></a>

#### statement.run(sql, ...params, callback) ⇒ <code>void</code>

**类型**: [Statement](#module_duckdb..Statement) 的实例方法  

| 参数 | 类型 |
| --- | --- |
| sql |  |
| ...params | <code>\*</code> |
| callback |  |

<a name="module_duckdb..Statement+all"></a>

#### statement.all(sql, ...params, callback) ⇒ <code>void</code>

**类型**: [Statement](#module_duckdb..Statement) 的实例方法  

| 参数 | 类型 |
| --- | --- |
| sql |  |
| ...params | <code>\*</code> |
| callback |  |

<a name="module_duckdb..Statement+arrowIPCAll"></a>

#### statement.arrowIPCAll(sql, ...params, callback) ⇒ <code>void</code>

**类型**: [Statement](#module_duckdb..Statement) 的实例方法  

| 参数 | 类型 |
| --- | --- |
| sql |  |
| ...params | <code>\*</code> |
| callback |  |

<a name="module_duckdb..Statement+each"></a>

#### statement.each(sql, ...params, callback) ⇒ <code>void</code>

**类型**: [Statement](#module_duckdb..Statement) 的实例方法  

| 参数 | 类型 |
| --- | --- |
| sql |  |
| ...params | <code>\*</code> |
| callback |  |

<a name="module_duckdb..Statement+finalize"></a>

#### statement.finalize(sql, ...params, callback) ⇒ <code>void</code>

**类型**: [Statement](#module_duckdb..Statement) 的实例方法  

| 参数 | 类型 |
| --- | --- |
| sql |  |
| ...params | <code>\*</code> |
| callback |  |

<a name="module_duckdb..Statement+stream"></a>

#### statement.stream(sql, ...params)

**类型**: [Statement](#module_duckdb..Statement) 的实例方法  

| 参数 | 类型 |
| --- | --- |
| sql |  |
| ...params | <code>\*</code> |

<a name="module_duckdb..Statement+columns"></a>

#### statement.columns() ⇒ [<code>Array.&lt;ColumnInfo&gt;</code>](#ColumnInfo)

**类型**: [Statement](#module_duckdb..Statement) 的实例方法  
**返回**: [<code>Array.&lt;ColumnInfo&gt;</code>](#ColumnInfo) - - 列名和类型的数组  
<a name="module_duckdb..QueryResult"></a>

### duckdb~QueryResult

**类型**: duckdb 的内部类  

* [~QueryResult](#module_duckdb..QueryResult)
    * [.nextChunk()](#module_duckdb..QueryResult+nextChunk) ⇒
    * [.nextIpcBuffer()](#module_duckdb..QueryResult+nextIpc, ⇒
    * [.asyncIterator()](#module_duckdb..QueryResult+asyncIterator)

<a name="module_duckdb..QueryResult+nextChunk"></a>

#### queryResult.nextChunk() ⇒

**类型**: [QueryResult](#module_duckdb..QueryResult) 的实例方法  
**返回**: 数据块  
<a name="module_duckdb..QueryResult+nextIpcBuffer"></a>

#### queryResult.nextIpcBuffer() ⇒

函数用于以零拷贝方式获取 Apache Arrow IPC 流的下一个结果 blob（需要加载 arrow 扩展）

**类型**: [QueryResult](#module_duckdb..QueryResult) 的实例方法  
**返回**: 数据块  
<a name="module_duckdb..QueryResult+asyncIterator"></a>

#### queryResult.asyncIterator()

**类型**: [QueryResult](#module_duckdb..QueryResult) 的实例方法  
<a name="module_duckdb..Database"></a>

### duckdb~Database

主数据库接口

**类型**: duckdb 的内部属性  

| 参数 | 描述 |
| --- | --- |
| path | 数据库文件路径或 :memory: 表示内存数据库 |
| access_mode | 访问模式 |
| config | 配置对象 |
| callback | 回调函数 |

* [~Database](#module_duckdb..Database)
    * [.close(callback)](#module_duckdb..Database+close) ⇒ <code>void</code>
    * [.close_internal(callback)](#module_duckdb..Database+close_internal) ⇒ <code>void</code>
    * [.wait(callback)](#module_duckdb..Database+wait) ⇒ <code>void</code>
    * [.serialize(callback)](#module_duckdb..Database+serialize) ⇒ <code>void</code>
    * [.parallelize(callback)](#module_duckdb..Database+parallelize) ⇒ <code>void</code>
    * [.connect(path)](#module_duckdb..Database+connect) ⇒ <code>Connection</code>
    * [.interrupt(callback)](#module_duckdb..Database+interrupt) ⇒ <code>void</code>
    * [.prepare(sql)](#module_duckdb..Database+prepare) ⇒ <code>Statement</code>
    * [.run(sql, ...params, callback)](#module_duckdb..Database+run) ⇒ <code>void</code>
    * [.scanArrowIpc(sql, ...params, callback)](#module_duckdb..Database+scanArrowIpc) ⇒ <code>void</code>
    * [.each(sql, ...params, callback)](#module_duckdb..Database+each) ⇒ <code>void</code>
    * [.stream(sql, ...params)](#module_duckdb..Database+stream)
    * [.all(sql, ...params, callback)](#module_duckdb..Database+all) ⇒ <code>void</code>
    * [.arrowIPCAll(sql, ...params, callback)](#module_duckdb..Database+arrowIPCAll) ⇒ <code>void</code>
    * [.arrowIPCStream(sql, ...params, callback)](#module_duckdb..Database+arrowIPCStream) ⇒ <code>void</code>
    * [.exec(sql, ...params, callback)](#module_duckdb..Database+exec) ⇒ <code>void</code>
    * [.register_udf(name, return_type, fun)](#module_duckdb..Database+register_udf) ⇒ <code>this</code>
    * [.register_buffer(name)](#module_duckdb..Database+register_buffer) ⇒ <code>this</code>
    * [.unregister_buffer(name)](#module_duckdb..Database+unregister_buffer) ⇒ <code>this</code>
    * [.unregister_udf(name)](#module_duckdb..Database+unregister_udf) ⇒ <code>this</code>
    * [.registerReplacementScan(fun)](#module_duckdb..Database+registerReplacementScan) ⇒ <code>this</code>
    * [.tokenize(text)](#module_duckdb..Database+tokenize) ⇒ <code>ScriptTokens</code>
    * [.get()](#module_duckdb..Database+get)

<a name="module_duckdb..Database+close"></a>

#### database.close(callback) ⇒ <code>void</code>

关闭数据库实例

**类型**: [Database](#module_duckdb..Database) 的实例方法  

| 参数 |
| --- |
| callback | 

<a name="module_duckdb..Database+close_internal"></a>

#### database.close_internal(callback) ⇒ <code>void</code>

内部方法。不要使用，调用 Connection#close 即可

**类型**: [Database](#module_duckdb..Database) 的实例方法  

| 参数 |
| --- |
| callback | 

<a name="module_duckdb..Database+wait"></a>

#### database.wait(callback) ⇒ <code>void</code>

当所有计划的数据库任务完成时触发回调。

**类型**: [Database](#module_duckdb..Database) 的实例方法  

| 参数 |
| --- |
| callback | 

<a name="module_duckdb..Database+serialize"></a>

#### database.serialize(callback) ⇒ <code>void</code>

目前是一个无操作。为了 SQLite 兼容性而提供

**类型**: [Database](#module_duckdb..Database) 的实例方法  

| 参数 |
| --- |
| callback | 

<a name="module_duckdb..Database+parallelize"></a>

#### database.parallelize(callback) ⇒ <code>void</code>

目前是一个无操作。为了 SQLite 兼容性而提供

**类型**: [Database](#module_duckdb..Database) 的实例方法  

| 参数 |
| --- |
| callback | 

<a name="module_duckdb..Database+connect"></a>

#### database.connect(path) ⇒ <code>Connection</code>

创建一个新的数据库连接

**类型**: [Database](#module_duckdb..Database) 的实例方法  

| 参数 | 描述 |
| --- | --- |
| path | 要连接的数据库，可以是文件路径或 `:memory:` |

<a name="module_duckdb..Database+interrupt"></a>

#### database.interrupt(callback) ⇒ <code>void</code>

据称可以中断查询，但目前不执行任何操作。

**类型**: [Database](#module_duckdb..Database) 的实例方法  

| 参数 |
| --- |
| callback | 

<a name="module_duckdb..Database+prepare"></a>

#### database.prepare(sql) ⇒ <code>Statement</code>

为执行准备 SQL 查询

**类型**: [Database](#module_duckdb..Database) 的实例方法  

| 参数 |
| --- |
| sql | 

<a name="module_duckdb..Database+run"></a>

#### database.run(sql, ...params, callback) ⇒ <code>void</code>

使用内置默认连接的 Connection#run 的便捷方法

**类型**: [Database](#module_duckdb..Database) 的实例方法  

| 参数 | 类型 |
| --- | --- |
| sql |  |
| ...params | <code>\*</code> |
| callback |  |

<a name="module_duckdb..Database+scanArrowIpc"></a>

#### database.scanArrowIpc(sql, ...params, callback) ⇒ <code>void</code>

使用内置默认连接的 Connection#scanArrowIpc 的便捷方法

**类型**: [Database](#module_duckdb..Database) 的实例方法  

| 参数 | 类型 |
| --- | --- |
| sql |  |
| ...params | <code>\*</code> |
| callback |  |

<a name="module_duckdb..Database+each"></a>

#### database.each(sql, ...params, callback) ⇒ <code>void</code>

**类型**: [Database](#module_duckdb..Database) 的实例方法  

| 参数 | 类型 |
| --- | --- |
| sql |  |
| ...params | <code>\*</code> |
| callback |  |

<a name="module_duckdb..Database+stream"></a>

#### database.stream(sql, ...params)

**类型**: [Database](#module_duckdb..Database) 的实例方法  

| 参数 | 类型 |
| --- | --- |
| sql |  |
| ...params | <code>\*</code> |

<a name="module_duckdb..Database+all"></a>

#### database.all(sql, ...params, callback) ⇒ <code>void</code>

使用内置默认连接的 Connection#apply 的便捷方法

**类型**: [Database](#module_duckdb..Database) 的实例方法  

| 参数 | 类型 |
| --- | --- |
| sql |  |
| ...params | <code>\*</code> |
| callback |  |

<a name="module_duckdb..Database+arrowIPCAll"></a>

#### database.arrowIPCAll(sql, ...params, callback) ⇒ <code>void</code>

使用内置默认连接的 Connection#arrowIPCAll 的便捷方法

**类型**: [Database](#module_duckdb..Database) 的实例方法  

| 参数 | 类型 |
| --- | --- |
| sql |  |
| ...params | <code>\*</code> |
| callback |  |

<a name="module_duckdb..Database+arrowIPCStream"></a>

#### database.arrowIPCStream(sql, ...params, callback) ⇒ <code>void</code>

使用内置默认连接的 Connection#arrowIPCStream 的便捷方法

**类型**: [Database](#module_duckdb..Database) 的实例方法  

| 参数 | 类型 |
| --- | --- |
| sql |  |
| ...params | <code>\*</code> |
| callback |  |

<a name="module_duckdb..Database+exec"></a>

#### database.exec(sql, ...params, callback) ⇒ <code>void</code>

**类型**: [Database](#module_duckdb..Database) 的实例方法  

| 参数 | 类型 |
| --- | --- |
| sql |  |
| ...params | <code>\*</code> |
| callback |  |

<a name="module_duckdb..Database+register_udf"></a>

#### database.register_udf(name, return_type, fun) ⇒ <code>this</code>

注册一个用户自定义函数

Connection#register_udf 的便捷方法

**类型**: [Database](#module_duckdb..Database) 的实例方法  

| 参数 |
| --- |
| name |
| return_type |
| fun |

<a name="module_duckdb..Database+register_buffer"></a>

#### database.register_buffer(name) ⇒ <code>this</code>

注册一个包含序列化数据的缓冲区，以便从 DuckDB 扫描

Connection#unregister_buffer 的便捷方法

**类型**: [Database](#module_duckdb..Database) 的实例方法  

| 参数 |
| --- |
| name |

<a name="module_duckdb..Database+unregister_buffer"></a>

#### database.unregister_buffer(name) ⇒ <code>this</code>

取消注册缓冲区

Connection#unregister_buffer 的便捷方法

**类型**: [Database](#module_duckdb..Database) 的实例方法  

| 参数 |
| --- |
| name |

<a name="module_duckdb..Database+unregister_udf"></a>

#### database.unregister_udf(name) ⇒ <code>this</code>

取消注册 UDF

Connection#unregister_udf 的便捷方法

**类型**: [Database](#module_duckdb..Database) 的实例方法  

| 参数 |
| --- |
| name |

<a name="module_duckdb..Database+registerReplacementScan"></a>

#### database.registerReplacementScan(fun) ⇒ <code>this</code>

注册一个表替换扫描函数

**类型**: [Database](#module_duckdb..Database) 的实例方法  

| 参数 | 描述 |
| --- | --- |
| fun | 替换扫描函数 |

<a name="module_duckdb..Database+tokenize"></a>

#### database.tokenize(text) ⇒ <code>ScriptTokens</code>

返回给定文本中 token 的位置和类型

**类型**: [Database](#module_duckdb..Database) 的实例方法  

| 参数 |
| --- |
| text |

<a name="module_duckdb..Database+get"></a>

#### database.get()

未实现

**类型**: [Database](#module_duckdb..Database) 的实例方法  
<a name="module_duckdb..TokenType"></a>

### duckdb~TokenType

`tokenize` 返回的 token 类型

**类型**: duckdb 的内部属性  
<a name="module_duckdb..ERROR"></a>

### duckdb~ERROR : <code>number</code>

检查 errno 属性是否等于此值以检查 duckdb 错误

**类型**: duckdb 的内部常量  
<a name="module_duckdb..OPEN_READONLY"></a>

### duckdb~OPEN_READONLY : <code>number</code>

以只读模式打开数据库

**类型**: duckdb 的内部常量  
<a name="module_duckdb..OPEN_READWRITE"></a>

### duckdb~OPEN_READWRITE : <code>number</code>

目前忽略

**类型**: duckdb 的内部常量  
<a name="module_duckdb..OPEN_CREATE"></a>

### duckdb~OPEN_CREATE : <code>number</code>

目前忽略

**类型**: duckdb 的内部常量  
<a name="module_duckdb..OPEN_FULLMUTEX"></a>

### duckdb~OPEN_FULLMUTEX : <code>number</code>

目前忽略

**类型**: duckdb 的内部常量  
<a name="module_duckdb..OPEN_SHAREDCACHE"></a>

### duckdb~OPEN_SHAREDCACHE : <code>number</code>

目前忽略

**类型**: duckdb 的内部常量  
<a name="module_duckdb..OPEN_PRIVATECACHE"></a>

### duckdb~OPEN_PRIVATECACHE : <code>number</code>

目前忽略

**类型**: duckdb 的内部常量  
<a name="ColumnInfo"></a>

## ColumnInfo : <code>object</code>

**类型**: 全局类型定义  
**属性**

| 名称 | 类型 | 描述 |
| --- | --- | --- |
| name | <code>string</code> | 列名 |
| type | [<code>TypeInfo</code>](#TypeInfo) | 列类型 |

<a name="TypeInfo"></a>

## TypeInfo : <code>object</code>

**类型**: 全局类型定义  
**属性**

| 名称 | 类型 | 描述 |
| --- | --- | --- |
| id | <code>string</code> | 类型 ID |
| [alias] | <code>string</code> | SQL 类型别名 |
| sql_type | <code>string</code> | SQL 类型名称 |

<a name="DuckDbError"></a>

## DuckDbError : <code>object</code>

**类型**: 全局类型定义  
**属性**

| 名称 | 类型 | 描述 |
| --- | --- | --- |
| errno | <code>number</code> | -1 表示 DuckDB 错误 |
| message | <code>string</code> | 错误信息 |
| code | <code>string</code> | DuckDB 错误时为 'DUCKDB_NODEJS_ERROR' |
| errorType | <code>string</code> | DuckDB 错误类型代码（例如，HTTP、IO、Catalog） |

<a name="HTTPError"></a>

## HTTPError : <code>object</code>

**类型**: 全局类型定义  
**继承**: [<code>DuckDbError</code>](#DuckDbError)  
**属性**

| 名称 | 类型 | 描述 |
| --- | --- | --- |
| statusCode | <code>number</code> | HTTP 响应状态码 |
| reason | <code>string</code> | HTTP 响应原因 |
| response | <code>string</code> | HTTP 响应正文 |
| headers | <code>object</code> | HTTP 头部 |