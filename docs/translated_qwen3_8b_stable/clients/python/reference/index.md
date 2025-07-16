以下是将您提供的英文内容翻译成中文的简化版本：

---

### DuckDB Python 模块方法列表

#### 连接相关
- `connect(database, read_only=False, memory=False, config=None)`：建立与数据库的连接。
- `checkpoint(connection, path, format='parquet')`：将数据库检查点保存到指定路径。
- `close(connection)`：关闭数据库连接。
- `check_database_exists(database)`：检查数据库是否存在。
- `create_database(database, path, config=None)`：创建数据库。
- `drop_database(database, path, config=None)`：删除数据库。
- `drop_checkpoint(path, format='parquet')`：删除检查点。
- `list_databases(path, config=None)`：列出数据库。
- `list_checkpoints(path, format='parquet')`：列出检查点。
- `read_checkpoint(path, format='parquet')`：读取检查点。
- `set_database_path(database, path, config=None)`：设置数据库路径。

#### SQL 查询
- `sql(sql, connection=None)`：执行 SQL 查询。
- `query_df(df, virtual_table_name, sql_query, connection=None)`：在虚拟表上执行 SQL 查询。
- `query(df, virtual_table_name, sql_query, connection=None)`：在虚拟表上执行 SQL 查询。
- `values(*args, connection=None)`：从传入值创建关系对象。
- `table(table_name, connection=None)`：从表名创建关系对象。
- `view(view_name, connection=None)`：从视图名创建关系对象。
- `table_function(name, parameters=None, connection=None)`：从表函数名创建关系对象。

#### 数据处理
- `read_csv(path_or_buffer, **kwargs)`：从 CSV 文件创建关系对象。
- `read_json(path_or_buffer, **kwargs)`：从 JSON 文件创建关系对象。
- `read_parquet(*args, **kwargs)`：从 Parquet 文件创建关系对象。
- `write_csv(df, filename, **kwargs)`：将关系对象写入 CSV 文件。
- `fetch(df, virtual_table_name, sql_query, connection=None)`：从虚拟表获取数据。

#### 数据类型
- `type(type_str, connection=None)`：通过类型字符串创建类型对象。
- `sqltype(type_str, connection=None)`：通过 SQL 类型字符串创建类型对象。
- `string_type(collation='', connection=None)`：创建带有排序规则的字符串类型。
- `row_type(fields, connection=None)`：从字段创建行类型。
- `struct_type(fields, connection=None)`：从字段创建结构类型。
- `union_type(members, connection=None)`：从成员创建联合类型。
- `map_type(key_type, value_type, connection=None)`：从键类型和值类型创建映射类型。
- `decimal_type(precision, scale, connection=None)`：创建十进制类型。
- `date_type(connection=None)`：创建日期类型。
- `time_type(connection=None)`：创建时间类型。
- `timestamp_type(connection=None)`：创建时间戳类型。
- `interval_type(connection=None)`：创建间隔类型。
- `boolean_type(connection=None)`：创建布尔类型。
- `integer_type(connection=None)`：创建整数类型。
- `real_type(connection=None)`：创建实数类型。
- `double_type(connection=None)`：创建双精度浮点数类型。
- `binary_type(connection=None)`：创建二进制类型。
- `null_type(connection=None)`：创建空类型。

#### 其他功能
- `checkpoint(connection, path, format='parquet')`：保存检查点。
- `list_checkpoints(path, format='parquet')`：列出检查点。
- `read_checkpoint(path, format='parquet')`：读取检查点。
- `drop_checkpoint(path, format='parquet')`：删除检查点。
- `tokenize(query)`：对 SQL 查询进行分词。
- `token_type`：分词类型。

---

如需更详细的翻译或特定方法的解释，请告诉我！