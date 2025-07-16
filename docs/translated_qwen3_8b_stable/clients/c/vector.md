---
layout: docu
redirect_from:
- /docs/api/c/vector
- /docs/api/c/vector/
- /docs/clients/c/vector
title: 向量
---

向量表示列的一个水平切片。它们保存特定类型的一组值，类似于数组。向量是DuckDB中使用的核心数据表示形式。向量通常存储在[数据块]({% link docs/stable/clients/c/data_chunk.md %})中。

向量和数据块接口是与DuckDB交互的最有效方式，允许实现最高性能。然而，这些接口也难以使用，使用时需格外注意。

## 向量格式

向量是特定数据类型的数组。可以通过`duckdb_vector_get_column_type`获取向量的逻辑类型。然后可以通过`duckdb_get_type_id`获取逻辑类型的类型ID。

向量本身没有大小。相反，父数据块有大小（可以通过`duckdb_data_chunk_get_size`获取）。所有属于同一数据块的向量具有相同的大小。

### 原始类型

对于原始类型，可以使用`duckdb_vector_get_data`方法获取底层数组。然后可以使用正确的本地类型访问该数组。以下表格列出了`duckdb_type`与数组本地类型的映射关系。

<div class="monospace_table"></div>

|       duckdb_type        |    NativeType    |
|--------------------------|------------------|
| DUCKDB_TYPE_BOOLEAN      | bool             |
| DUCKDB_TYPE_TINYINT      | int8_t           |
| DUCKDB_TYPE_SMALLINT     | int16_t          |
| DUCKDB_TYPE_INTEGER      | int32_t          |
| DUCKDB_TYPE_BIGINT       | int64_t          |
| DUCKDB_TYPE_UTINYINT     | uint8_t          |
| DUCKDB_TYPE_USMALLINT    | uint16_t         |
| DUCKDB_TYPE_UINTEGER     | uint32_t         |
| DUCKDB_TYPE_UBIGINT      | uint64_t         |
| DUCKDB_TYPE_FLOAT        | float            |
| DUCKDB_TYPE_DOUBLE       | double           |
| DUCKDB_TYPE_TIMESTAMP    | duckdb_timestamp |
| DUCKDB_TYPE_DATE         | duckdb_date      |
| DUCKDB_TYPE_TIME         | duckdb_time      |
| DUCKDB_TYPE_INTERVAL     | duckdb_interval  |
| DUCKDB_TYPE_HUGEINT      | duckdb_hugeint   |
| DUCKDB_TYPE_UHUGEINT     | duckdb_uhugeint  |
| DUCKDB_TYPE_VARCHAR      | duckdb_string_t  |
| DUCKDB_TYPE_BLOB         | duckdb_string_t  |
| DUCKDB_TYPE_TIMESTAMP_S  | duckdb_timestamp |
| DUCKDB_TYPE_TIMESTAMP_MS | duckdb_timestamp |
| DUCKDB_TYPE_TIMESTAMP_NS | duckdb_timestamp |
| DUCKDB_TYPE_UUID         | duckdb_hugeint   |
| DUCKDB_TYPE_TIME_TZ      | duckdb_time_tz   |
| DUCKDB_TYPE_TIMESTAMP_TZ | duckdb_timestamp |

### NULL值

向量中的任何值都可以是NULL。当值为NULL时，该值在主数组中对应的索引位置是未定义的（可以未初始化）。有效性掩码是一个由`uint64_t`元素组成的位掩码。对于向量中的每64个值，有一个`uint64_t`元素（向上取整）。有效性掩码中，如果值有效，则对应位设置为1，如果值无效（即为NULL），则设置为0。

可以直接读取位掩码中的位，或使用较慢的辅助方法`duckdb_validity_row_is_valid`来检查值是否为NULL。

`duckdb_vector_get_validity`返回有效性掩码的指针。请注意，如果向量中的所有值都是有效的，此函数**可能**返回`nullptr`，此时不需要检查有效性掩码。

### 字符串

字符串值存储为`duckdb_string_t`。这是一个特殊的结构，如果字符串较短（即`<= 12字节`），则直接存储字符串；如果较长，则存储指向字符串数据的指针。

```c
typedef struct {
	union {
		struct {
			uint32_t length;
			char prefix[4];
			char *ptr;
		} pointer;
		struct {
			uint32_t length;
			char inlined[12];
		} inlined;
	} value;
} duckdb_string_t;
```

长度可以直接访问，或使用`duckdb_string_is_inlined`检查字符串是否内联存储。

### 小数

小数在内部存储为整数值。小数类型的精确本地类型取决于小数类型的宽度，如下表所示：

<div class="monospace_table"></div>

| Width |   NativeType   |
|-------|----------------|
| <= 4  | int16_t        |
| <= 9  | int32_t        |
| <= 18 | int64_t        |
| <= 38 | duckdb_hugeint |

可以使用`duckdb_decimal_internal_type`获取小数的内部类型。

小数在内部存储为整数值乘以`10^scale`。小数的scale可以通过`duckdb_decimal_scale`获取。例如，一个`DECIMAL(8, 3)`类型的小数值`10.5`在内部存储为`int32_t`值`10500`。为了得到正确的十进制值，需要将值除以相应的十的幂。

### 枚举

枚举在内部存储为无符号整数值。枚举字典的大小决定了具体的本地类型，如下表所示：

<div class="monospace_table"></div>

| Dictionary size | NativeType |
|-----------------|------------|
| <= 255          | uint8_t    |
| <= 65535        | uint16_t   |
| <= 4294967295   | uint32_t   |

可以使用`duckdb_enum_internal_type`获取枚举的内部类型。

为了获取枚举的实际字符串值，必须使用`duckdb_enum_dictionary_value`函数获取与给定字典条目对应的枚举值。请注意，枚举字典对于整个列是相同的，因此只需构建一次。

### 结构

结构是包含任意数量子类型的嵌套类型。可以将其视为C语言中的`struct`。使用向量访问结构数据的方法是使用`duckdb_struct_vector_get_child`方法递归访问子向量。

结构向量本身不包含任何数据（即，不应在结构向量上使用`duckdb_vector_get_data`方法）。**然而**，结构向量本身**确实**具有一个有效性掩码。原因在于结构的子元素可以为NULL，但结构**本身**也可以为NULL。

### 列表

列表是包含一个子类型的嵌套类型，每行重复`x`次。可以将其视为C语言中的可变长度数组。使用向量访问列表数据的方法是使用`duckdb_list_vector_get_child`方法访问子向量。

必须使用`duckdb_vector_get_data`获取存储为`duckdb_list_entry`的列表的偏移量和长度，然后将其应用到子向量。

```c
typedef struct {
	uint64_t offset;
	uint64_t length;
} duckdb_list_entry;
```

请注意，列表条目本身**和**列表中存储的任何子元素也可以为NULL。这必须再次使用有效性掩码进行检查。

### 数组

数组是包含一个子类型的嵌套类型，每行重复恰好`array_size`次。可以将其视为C语言中的固定大小数组。数组的工作方式与列表完全相同，**除了**每个条目的长度和偏移量是固定的。固定数组大小可以通过使用`duckdb_array_type_array_size`获取。第`n`个条目的数据位于`offset = n * array_size`，并且长度始终为`array_size`。

请注意，与列表类似，数组也可以为NULL，必须使用有效性掩码进行检查。

## 示例

下面是一些完整的端到端示例，展示如何与向量进行交互。

### 示例：读取带有NULL值的int64向量

```c
duckdb_database db;
duckdb_connection con;
duckdb_open(nullptr, &db);
duckdb_connect(db, &con);

duckdb_result res;
duckdb_query(con, "SELECT CASE WHEN i%2=0 THEN NULL ELSE i END res_col FROM range(10) t(i)", &res);

// 迭代直到结果耗尽
while (true) {
	duckdb_data_chunk result = duckdb_fetch_chunk(res);
	if (!result) {
		// 结果已耗尽
		break;
	}
	// 从数据块中获取行数
	idx_t row_count = duckdb_data_chunk_get_size(result);
	// 获取第一个列
	duckdb_vector res_col = duckdb_data_chunk_get_vector(result, 0);
	// 获取向量的本地数组和有效性掩码
	int64_t *vector_data = (int64_t *) duckdb_vector_get_data(res_col);
	uint64_t *vector_validity = duckdb_vector_get_validity(res_col);
	// 迭代行
	for (idx_t row = 0; row < row_count; row++) {
		if (duckdb_validity_row_is_valid(vector_validity, row)) {
			printf("%lld\n", vector_data[row]);
		} else {
			printf("NULL\n");
		}
	}
	duckdb_destroy_data_chunk(&result);
}
// 清理
duckdb_destroy_result(&res);
duckdb_disconnect(&con);
duckdb_close(&db);
```

### 示例：读取字符串向量

```c
duckdb_database db;
duckdb_connection con;
duckdb_open(nullptr, &db);
duckdb_connect(db, &con);

duckdb_result res;
duckdb_query(con, "SELECT CASE WHEN i%2=0 THEN CONCAT('short_', i) ELSE CONCAT('longstringprefix', i) END FROM range(10) t(i)", &res);

// 迭代直到结果耗尽
while (true) {
	duckdb_data_chunk result = duckdb_fetch_chunk(res);
	if (!result) {
		// 结果已耗尽
		break;
	}
	// 从数据块中获取行数
	idx_t row_count = duckdb_data_chunk_get_size(result);
	// 获取第一个列
	duckdb_vector res_col = duckdb_data_chunk_get_vector(result, 0);
	// 获取向量的本地数组和有效性掩码
	duckdb_string_t *vector_data = (duckdb_string_t *) duckdb_vector_get_data(res_col);
	uint64_t *vector_validity = duckdb_vector_get_valid
```