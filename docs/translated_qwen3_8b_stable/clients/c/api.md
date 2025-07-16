#### `duckdb_create_cast_function`
创建一个新的转换函数对象。

##### 返回值
转换函数对象。

##### 语法
```c
duckdb_cast_function duckdb_create_cast_function(void);
```

#### `duckdb_cast_function_set_source_type`
设置转换函数的源类型。

##### 语法
```c
void duckdb_cast_function_set_source_type(duckdb_cast_function cast_function, duckdb_logical_type source_type);
```

##### 参数
- `cast_function`: 转换函数对象。
- `source_type`: 要设置的源类型。

#### `duckdb_cast_function_set_target_type`
设置转换函数的目标类型。

##### 语法
```c
void duckdb_cast_function_set_target_type(duckdb_cast_function cast_function, duckdb_logical_type target_type);
```

##### 参数
- `cast_function`: 转换函数对象。
- `target_type`: 要设置的目标类型。

#### `duckdb_cast_function_set_implicit_cast_cost`
设置隐式转换源类型到目标类型使用此函数的成本。

##### 语法
```c
void duckdb_cast_function_set_implicit_cast_cost(duckdb_cast_function cast_function, int64_t cost);
```

##### 参数
- `cast_function`: 转换函数对象。
- `cost`: 要设置的成本。

#### `duckdb_cast_function_set_function`
设置实际使用的转换函数。

##### 语法
```c
void duckdb_cast_function_set_function(duckdb_cast_function cast_function, duckdb_cast_function_t function);
```

##### 参数
- `cast_function`: 转换函数对象。
- `function`: 要设置的函数。

#### `duckdb_cast_function_set_extra_info`
为转换函数分配额外信息，可以在执行时获取。

##### 语法
```c
void duckdb_cast_function_set_extra_info(duckdb_cast_function cast_function, void *extra_info, duckdb_delete_callback_t destroy);
```

##### 参数
- `extra_info`: 额外信息。
- `destroy`: 用于销毁额外信息的回调函数（如果有的话）。

#### `duckdb_cast_function_get_extra_info`
从给定的函数信息中获取额外信息。

##### 语法
```c
void* duckdb_cast_function_get_extra_info(duckdb_function_info info);
```

##### 参数
- `info`: 信息对象。

##### 返回值
额外信息。

#### `duckdb_cast_function_get_cast_mode`
从给定的函数信息中获取转换执行模式。

##### 语法
```c
duckdb_cast_mode duckdb_cast_function_get_cast_mode(duckdb_function_info info);
```

##### 参数
- `info`: 信息对象。

##### 返回值
转换模式。

#### `duckdb_cast_function_set_error`
报告在执行转换函数时发生错误。

##### 语法
```c
void duckdb_cast_function_set_error(duckdb_function_info info, const char *error);
```

##### 参数
- `info`: 信息对象。
- `error`: 错误信息。

#### `duckdb_cast_function_set_row_error`
报告在执行转换函数时发生错误，设置对应的输出行为空。

##### 语法
```c
void duckdb_cast_function_set_row_error(duckdb_function_info info, const char *error, idx_t row, duckdb_vector output);
```

##### 参数
- `info`: 信息对象。
- `error`: 错误信息。
- `row`: 在输出向量中设置为空的行索引。
- `output`: 输出向量。

#### `duckdb_register_cast_function`
在给定的连接中注册一个转换函数。

##### 语法
```c
duckdb_state duckdb_register_cast_function(duckdb_connection con, duckdb_cast_function cast_function);
```

##### 参数
- `con`: 要使用的连接。
- `cast_function`: 要注册的转换函数。

##### 返回值
注册是否成功。

#### `duckdb_destroy_cast_function`
销毁转换函数对象。

##### 语法
```c
void duckdb_destroy_cast_function(duckdb_cast_function *cast_function);
```

##### 参数
- `cast_function`: 转换函数对象。