---
---
layout: docu
redirect_from:
- /docs/dev/building/building_extensions
title: 构建扩展
---

[扩展]({% link docs/stable/core_extensions/overview.md %}) 可以从源代码构建，并从生成的本地二进制文件进行安装。

## 构建扩展

要使用扩展标志进行构建，请将 `CORE_EXTENSIONS` 标志设置为要构建的扩展列表。例如：

```batch
CORE_EXTENSIONS='autocomplete;httpfs;icu;json;tpch' GEN=ninja make
```

此选项还支持外部扩展，例如 [`delta`]({% link docs/stable/core_extensions/delta.md %})：

```batch
CORE_EXTENSIONS='autocomplete;httpfs;icu;json;tpch;delta' GEN=ninja make
```

在大多数情况下，扩展将直接链接到生成的 DuckDB 可执行文件中。

## 特殊扩展标志

### `BUILD_JEMALLOC`

当此标志被设置时，会构建 [`jemalloc` 扩展]({% link docs/stable/core_extensions/jemalloc.md %}).

### `BUILD_TPCE`

当此标志被设置时，会构建 [TPCE](https://www.tpc.org/tpce/) 库。与 TPC-H 和 TPC-DS 不同，这不是一个真正的扩展，也不会以扩展形式分发。启用此标志允许通过我们的测试套件执行 TPC-E 启用的查询。

## 调试标志

### `CRASH_ON_ASSERT`

`D_ASSERT(condition)` 在代码中被广泛使用，这些在调试构建中会引发 InternalException。
启用此标志时，当断言触发时，将直接导致崩溃。

### `DISABLE_STRING_INLINE`

在我们的执行格式中，`string_t` 具有“内联”字符串的功能，这些字符串长度小于特定值（12 字节），这意味着它们不需要单独的分配。
当此标志被设置时，我们将禁用此功能，不内联小字符串。

### `DISABLE_MEMORY_SAFETY`

我们用于非性能关键代码中的数据结构具有额外的检查以确保内存安全，这些检查包括：

* 确保 `nullptr` 从不被解引用。
* 确保索引越界访问不会导致崩溃。

启用此标志时，我们将移除这些检查，这主要是为了检查这些检查对性能的影响是否可以忽略。

### `DESTROY_UNPINNED_BLOCKS`

当缓冲区管理器中之前被固定的块被取消固定时，启用此标志时，我们将立即销毁它们，以确保即使未被固定，这些内存也不会被使用。

### `DEBUG_STACKTRACE`

当测试中发生崩溃或断言时，打印堆栈跟踪。
这在调试难以定位的崩溃时非常有用，尤其是在附加调试器的情况下。

## 使用 CMake 配置文件

要使用 CMake 配置文件进行构建，请创建一个名为 `extension_config.cmake` 的扩展配置文件，例如包含以下内容：

```cmake
duckdb_extension_load(autocomplete)
duckdb_extension
```