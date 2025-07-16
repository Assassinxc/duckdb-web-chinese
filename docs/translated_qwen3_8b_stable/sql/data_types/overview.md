---
---
blurb: 下表显示了所有内置的一般用途数据类型。
layout: docu
redirect_from:
- /docs/sql/data_types/overview
title: 数据类型
---

## 一般用途数据类型

下表显示了所有内置的一般用途数据类型。别名列中列出的替代类型也可以用于引用这些类型，不过请注意，别名不是 SQL 标准的一部分，因此可能不被其他数据库引擎接受。

| 名称                       | 别名                            | 描述                                                                                                |
| :------------------------- | :--------------------------------- | :--------------------------------------------------------------------------------------------------------- |
| `BIGINT`                   | `INT8`, `LONG`                     | 带符号的八字节整数                                                                                  |
| `BIT`                      | `BITSTRING`                        | 由 1 和 0 组成的字符串                                                                                      |
| `BLOB`                     | `BYTEA`, `BINARY`, `VARBINARY`     | 可变长度的二进制数据                                                                                      |
| `BOOLEAN`                  | `BOOL`, `LOGICAL`                  | 逻辑布尔值 (`true` / `false`)                                                                           |
| `DATE`                     |                                    | 日历日期（年、月、日）                                                                               |
| `DECIMAL(prec, scale)`     | `NUMERIC(prec, scale)`             | 固定精度的数字，指定宽度（精度）和小数位数，缺省值为 `prec = 18` 和 `scale = 3` |
| `DOUBLE`                   | `FLOAT8`,                          | 双精度浮点数（8 字节）                                                                               |
| `FLOAT`                    | `FLOAT4`, `REAL`                   | 单精度浮点数（4 字节）                                                                               |
| `HUGEINT`                  |                                    | 带符号的十六字节整数                                                                               |
| `INTEGER`                  | `INT4`, `INT`, `SIGNED`            | 带符号的四字节整数                                                                                   |
| `INTERVAL`                 |                                    | 日期/时间差值                                                                                          |
| `JSON`                     |                                    | JSON 对象（通过 [`json` 扩展]({% link docs/stable/data/json/overview.md %})）                            |
| `SMALLINT`                 | `INT2`, `SHORT`                    | 带符号的二字节整数                                                                                      |
| `TIME`                     |                                    | 时间（无时区）                                                                                         |
| `TIMESTAMP WITH TIME ZONE` | `TIMESTAMPTZ`                      | 结合时间与日期，使用当前时区                                                                              |
| `TIMESTAMP`                | `DATETIME`                         | 结合时间与日期                                                                                         |
| `TINYINT`                  | `INT1`                             | 带符号的一字节整数                                                                                      |
| `UBIGINT`                  |                                    | 无符号的八字节整数                                                                                      |
| `UHUGEINT`                 |                                    | 无符号的十六字节整数                                                                                      |
| `UINTEGER`                 |                                    | 无符号的四字节整数                                                                                      |
| `USMALLINT`                |                                    | 无符号的二字节整数                                                                                      |
| `UTINYINT`                 |                                    | 无符号的一字节整数                                                                                      |
| `UUID`                     |                                    | UUID 数据类型                                                                                           |
| `VARCHAR`                  | `CHAR`, `BPCHAR`, `TEXT`, `STRING` | 可变长度的字符字符串                                                                                      |

可以在多种类型之间进行隐式和显式的类型转换，请参阅 [类型转换]({% link docs/stable/sql/data_types/typecasting.md %}) 页面以获取详细信息。

## 嵌套 / 复合类型

DuckDB 支持五种嵌套数据类型：`ARRAY`、`LIST`、`MAP`、`STRUCT` 和 `UNION`。每种类型支持不同的使用场景，并具有不同的结构。

| 名称 | 描述 | 在列中使用时的规则 | 从值构建 | 在 DDL/CREATE 中定义 |
|:-|:---|:---|:--|:--|
| [`ARRAY`]({% link docs/stable/sql/data_types/array.md %}) | 一种有序、固定长度的同类型数据值序列。 | 每个实例中的 `ARRAY` 必须具有相同的数据类型且元素数量相同。 | `[1, 2, 3]` | `INTEGER[3]` |
| [`LIST`]({% link docs/stable/sql/data_types/list.md %}) | 一种有序的同类型数据值序列。 | 每个实例中的 `LIST` 必须具有相同的数据类型，但可以具有任意数量的元素。 | `[1, 2, 3]` | `INTEGER[]` |
| [`MAP`]({% link docs/stable/sql/data_types/map.md %}) | 一个包含多个命名值的字典，每个键具有相同类型，每个值也具有相同类型。键和值可以是任意类型，也可以是彼此不同的类型。 | 行可以具有不同的键。 | `map([1, 2], ['a', 'b'])` | `MAP(INTEGER, VARCHAR)` |
| [`STRUCT`]({% link docs/stable/sql/data_types/struct.md %}) | 一个包含多个命名值的字典，其中每个键是字符串，但每个键的值可以是不同类型的值。 | 每行必须具有相同的键。 | `{'i': 42, 'j': 'a'}` | `STRUCT(i INTEGER, j VARCHAR)` |
| [`UNION`]({% link docs/stable/sql/data_types/union.md %}) | 一种包含多种替代数据类型的联合，每个值存储其中一种类型。联合还包含一个“标签”值，用于检查和访问当前设置的成员类型。 | 行可以设置为联合的不同成员类型。 | `union_value(num := 2)` | `UNION(num INTEGER, text VARCHAR)` |

### 大小写敏感规则

`MAP` 的键是大小写敏感的，而 `UNION` 和 `STRUCT` 的键是大小写不敏感的。
示例请参阅 [大小写敏感规则部分]({% link docs/stable/sql/dialect/overview.md %}#case-sensitivity-of-keys-in-nested-data-structures)。

### 更新嵌套类型值

在对嵌套类型值进行更新时，DuckDB 会先执行一个删除操作，然后执行一个插入操作。
当在具有 ART 索引的表中使用时（无论是显式索引还是主键/唯一约束），这可能导致 [意外的约束违规]({% link docs/stable/sql/indexes.md %}#constraint-checking-in-update-statements)。

## 嵌套

`ARRAY`、`LIST`、`MAP`、`STRUCT` 和 `UNION` 类型可以任意深度嵌套，只要遵守类型规则即可。

包含 `LIST` 的结构：

```sql
SELECT {'birds': ['duck', 'goose', 'heron'], 'aliens': NULL, 'amphibians': ['frog', 'toad']};
```

包含 `MAP` 列表的结构：

```sql
SELECT {'test': [MAP([1, 5], [42.1, 45]), MAP([1, 5], [42.1, 45])]};
```

一个 `UNION` 列表：

```sql
SELECT [union_value(num := 2), union_value(str := 'ABC')::UNION(str VARCHAR, num INTEGER)];
```

## 性能影响

数据类型的选择对性能有显著影响。请参阅 [性能指南]({% link docs/stable/guides/performance/schema.md %}) 以获取详细信息。