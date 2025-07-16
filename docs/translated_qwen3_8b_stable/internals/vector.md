---
---
layout: docu
redirect_from:
- /internals/vector
- /internals/vector/
- /docs/internals/vector
title: 执行格式
---

`Vector` 是用于执行过程中存储内存数据的容器格式。
`DataChunk` 是一组 Vectors，例如用于表示 `PhysicalProjection` 运算符中的列列表。

## 数据流

DuckDB 使用向量化查询执行模型。
DuckDB 中的所有运算符都经过优化以在固定大小的 Vectors 上运行。

这种固定大小在代码中通常称为 `STANDARD_VECTOR_SIZE`。
默认的 `STANDARD_VECTOR_SIZE` 是 2048 个元组。

## Vector 格式

Vectors 逻辑上表示包含单一类型数据的数组。DuckDB 支持不同的 *Vector 格式*，这允许系统以不同的 *物理表示* 存储相同的逻辑数据。这允许更紧凑的表示，并且可能在整个系统中实现压缩执行。下面列出了支持的 Vector 格式。

### 平面 Vectors

平面 Vectors 以连续数组的形式物理存储，这是标准的未压缩 Vector 格式。
对于平面 Vectors，逻辑表示和物理表示是相同的。

<img src="/images/internals/flat.png" alt="平面 Vector 示例" style="max-width:40%;width:40%;height:auto;margin:auto"/>

### 常量 Vectors

常量 Vectors 以单个常量值的形式物理存储。

<img src="/images/internals/constant.png" alt="常量 Vector 示例" style="max-width:40%;width:40%;height:auto;margin:auto"/>

当数据元素重复时，常量 Vectors 非常有用，例如，当在函数调用中表示常量表达式的结果时，常量 Vector 允许我们只存储一次值。

```sql
SELECT lst || 'duckdb'
FROM range(1000) tbl(lst);
```

由于 `duckdb` 是一个字符串字面量，字面量的值在每一行都是相同的。在平面 Vector 中，我们必须为每一行复制一次字面量 'duckdb'。常量 Vector 允许我们只存储一次字面量。

常量 Vectors 也在解压常量压缩时由存储系统发出。

### 字典 Vectors

字典 Vectors 以一个子 Vector 和一个包含子 Vector 索引的选择 Vector 的形式物理存储。

<img src="/images/internals/dictionary.png" alt="字典 Vector 示例" style="max-width:40%;width:40%;height:auto;margin:auto"/>

字典 Vectors 在解压字典压缩时由存储系统发出。

就像常量 Vectors 一样，字典 Vectors 也由存储系统发出。
在反序列化字典压缩的列段时，我们将其存储在字典 Vector 中，以便在查询执行期间保持数据压缩。

### 序列 Vectors

序列 Vectors 以偏移量和增量值的形式物理存储。

<img src="/images/internals/sequence.png" alt="序列 Vector 示例" style="max-width:40%;width:40%;height:auto;margin:auto"/>

序列 Vectors 用于高效地存储递增序列。它们通常用于行标识符。

### 统一 Vector 格式

不同 Vector 格式的这些特性对于优化非常有用，例如，你可以想象一个场景，函数的所有参数都是常量，我们只需计算一次结果并发出一个常量 Vector。
但是，由于可能组合的爆炸性，为每种 Vector 类型的每种函数编写专门的代码是不可行的。

相反，当你希望无论类型如何通用地使用 Vector 时，可以使用 UnifiedVectorFormat。
这种格式本质上是 Vector 内容的通用视图。每种类型的 Vector 都可以转换为这种格式。

## 复杂类型

### 字符串 Vectors

为了高效地存储字符串，我们使用我们的 `string_t` 类。

```cpp
struct string_t {
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
};
```

短字符串（`<= 12 字节`）被内联到结构中，而较长的字符串则通过指向辅助字符串缓冲区的指针存储。长度在整个函数中被使用，以避免调用 `strlen` 并持续检查空指针。前缀用于比较，作为早期退出机制（当前缀不匹配时，我们知道字符串不相等，无需继续追踪任何指针）。

### 列表 Vectors

列表 Vectors 以一系列 *列表条目* 和一个子 Vector 的形式存储。子 Vector 包含列表中的 *值*，列表条目指定每个列表是如何构建的。

```cpp
struct list_entry_t {
    idx_t offset;
    idx_t length;
};
```

偏移量指的是子 Vector 中的起始行，长度跟踪该行列表的大小。

列表 Vectors 可以递归存储。对于嵌套列表 Vectors，列表 Vector 的子项本身又是一个列表 Vector。

例如，考虑这个类型为 `BIGINT[][]` 的 Vector 的模拟表示：

```json
{
   "type": "list",
   "data": "list_entry_t",
   "child": {
      "type": "list",
      "data": "list_entry_t",
      "child": {
         "type": "bigint",
         "data": "int64_t"
      }
   }
}
```

### 结构 Vectors

结构 Vectors 存储一组子 Vector。子 Vector 的数量和类型由结构的模式定义。

### 映射 Vectors

内部，映射 Vectors 以 `LIST[STRUCT(key KEY_TYPE, value VALUE_TYPE)]` 的形式存储。

### 联合 Vectors

内部，`UNION` 使用与 `STRUCT` 相同的结构。
第一个“子”始终是 `UNION` 的 Tag Vector，它记录每行适用于该行的 `UNION` 类型。