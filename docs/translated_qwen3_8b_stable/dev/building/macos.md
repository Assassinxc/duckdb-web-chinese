---
---
layout: docu
redirect_from:
- /docs/dev/building/macos
title: macOS
---

## 前提条件

安装 Xcode 和 [Homebrew](https://brew.sh/)。然后，使用以下命令安装所需的软件包：

```batch
brew install git cmake ninja
```

## 构建 DuckDB

按照以下步骤克隆并构建 DuckDB。

```batch
git clone https://github.com/duckdb/duckdb
cd duckdb
GEN=ninja make
```

一旦构建成功完成，您可以在 `build` 目录中找到 `duckdb` 二进制文件：

```batch
build/release/duckdb
```

如需不同的构建配置（`debug`、`relassert` 等），请参阅 [构建配置页面]({% link docs/stable/dev/building/build_configuration.md %}).

## 故障排除

### 构建失败：`'string' 文件未找到`

**问题：**
在 macOS 上构建时出现以下错误：

```console
FAILED: third_party/libpg_query/CMakeFiles/duckdb_pg_query.dir/src_backend_nodes_list.cpp.o
/Library/Developer/CommandLineTools/usr/bin/c++ -DDUCKDB_BUILD_LIBRARY -DEXT_VERSION_PARQUET=\"9cba6a2a03\" -I/Users/builder/external/duckdb/src/include -I/Users/builder/external/duckdb/third_party/fsst -I/Users/builder/external/duckdb/third_party/fmt/include -I/Users/builder/external/duckdb/third_party/hyperloglog -I/Users/builder/external/duckdb/third_party/fastpforlib -I/Users/builder/external/duckdb/third_party/skiplist -I/Users/builder/external/duckdb/third_party/fast_float -I/Users/builder/external/duckdb/third_party/re2 -I/Users/builder/external/duckdb/third_party/miniz -I/Users/builder/external/duckdb/third_party/utf8proc/include -I/Users/builder/external/duckdb/third_party/concurrentqueue -I/Users/builder/external/duckdb/third_party/pcg -I/Users/builder/external/duckdb/third_party/tdigest -I/Users/builder/external/duckdb/third_party/mbedtls/include -I/Users/builder/external/duckdb/third_party/jaro_winkler -I/Users/builder/external/duckdb/third_party/yyjson/include -I/Users/builder/external/duckdb/third_party/libpg_query/include -O3 -DNDEBUG -O3 -DNDEBUG   -std=c++11 -arch arm64 -isysroot /Library/Developer/CommandLineTools/SDKs/MacOSX15.1.sdk -fPIC -fvisibility=hidden -fcolor-diagnostics -w -MD -MT third_party/libpg_query/CMakeFiles/duckdb_pg_query.dir/src_backend_nodes_list.cpp.o -MF third_party/libpg_query/CMakeFiles/duckdb_pg_query.dir/src_backend_nodes_list.cpp.o.d -o third_party/libpg_query/CMakeFiles/duckdb_pg_query.dir/src_backend_nodes_list.cpp.o -c /Users/builder/external/duckdb/third_party/libpg_query/src_backend_nodes_list.cpp
In file included from /Users/builder/external/duckdb/third_party/libpg_query/src_backend_nodes_list.cpp:35:
/Users/builder/external/duckdb/third_party/libpg_query/include/pg_functions.hpp:4:10: fatal error: 'string' file not found
    4 | #include <string>
```

**解决方案：**
用户报告重新安装 Xcode 解决了此问题。
有关相关讨论，请参阅 [DuckDB GitHub 问题](https://github.com/duckdb/duckdb/issues/14665#issuecomment-2452679953) 以及 [Stack Overflow](https://stackoverflow.com/questions/78999694/cant-compile-c-hello-world-with-clang-on-mac-sequoia-15-0-and-vs-code).

> 警告 重新安装您的 Xcode 套件可能会对系统上的其他应用程序产生影响。请谨慎操作。

```bash
sudo rm -rf /Library/Developer/CommandLineTools
xcode-select --install
```

### 调试构建打印 malloc 警告

**问题：**
在 macOS 上的 `debug` 构建会打印一个 `malloc` 警告，例如：

```text
duckdb(83082,0x205b30240) malloc: nano zone abandoned due to inability to reserve vm space.
```

**解决方案：**
为了防止此警告，请将 `MallocNanoZone` 标志设置为 0：

```batch
MallocNanoZone=0 make debug
```

为了在您未来的终端会话中应用此更改，可以将以下内容添加到您的 `~/.zshrc` 文件中：

```batch
export MallocNanoZone=0
```