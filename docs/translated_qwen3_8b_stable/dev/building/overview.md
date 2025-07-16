---
---
layout: docu
title: 从源码构建 DuckDB
---

## 何时需要构建 DuckDB？

DuckDB 的二进制文件在 [安装页面]({% link docs/installation/index.html %}) 上提供了 _稳定版_ 和 _预览版_ 构建。
在大多数情况下，建议使用这些二进制文件。
当你在运行实验性平台（例如 [Raspberry Pi]({% link docs/stable/dev/building/raspberry_pi.md %}）或你想为一个未合并的 pull request 构建项目时，可以基于 GitHub 上的 [`duckdb/duckdb` 仓库](https://github.com/duckdb/duckdb/) 构建 DuckDB 从源码。
此页面解释了构建 DuckDB 的步骤。

## 先决条件

DuckDB 需要 CMake 和一个符合 C++11 标准的编译器（例如 GCC、Apple-Clang、MSVC）。
此外，我们建议使用 [Ninja 构建系统](https://ninja-build.org/)，它可以自动并行化构建过程。

## 开始构建

一个 `Makefile` 包装了构建过程。
查看 [构建配置]({% link docs/stable/dev/building/build_configuration.md %}) 了解目标和配置标志。

```batch
make
make release # 与 plain make 相同
make debug
GEN=ninja make # 用于 Ninja
BUILD_BENCHMARK=1 make # 构建时包含基准测试
```

## 支持平台

### 完全支持的平台

DuckDB 完全支持 Linux、macOS 和 Windows。这些平台都提供了 x86_64（amd64）和 AArch64（arm64）的构建，并且几乎所有扩展都为这些平台提供。

| 平台名称      | 描述                                                            |
|----------------|------------------------------------------------------------------|
| `linux_amd64`  | Linux x86_64 (amd64) 配备 [glibc](https://www.gnu.org/software/libc/) |
| `linux_arm64`  | Linux AArch64 (arm64) 配备 [glibc](https://www.gnu.org/software/libc/) |
| `osx_amd64`    | macOS 12+ amd64 (Intel 处理器)                                   |
| `osx_arm64`    | macOS 12+ arm64 (Apple Silicon 处理器)                           |
| `windows_amd64`| Windows 10+ x86_64 (amd64)                                       |
| `windows_arm64`| Windows 10+ AArch64 (arm64)                                      |

对于这些平台，构建了最新稳定版和预览版（夜间构建）。
在某些情况下，你可能仍然想从源码构建 DuckDB，例如测试一个未合并的 [pull request](https://github.com/duckdb/duckdb/pulls)。
有关这些平台的构建说明，请参阅：

* [Linux]({% link docs/stable/dev/building/linux.md %})
* [macOS]({% link docs/stable/dev/building/macos.md %})
* [Windows]({% link docs/stable/dev/building/windows.md %})

### 部分支持的平台

有几个部分支持的平台。
对于某些平台，DuckDB 的二进制文件和扩展（或 [扩展子集]({% link docs/stable/extensions/extension_distribution.md %}#platforms)）是分发的。
对于其他平台，可以从源码构建。

| 平台名称          | 描述                                                                                          |
|------------------|-----------------------------------------------------------------------------------------------|
| `linux_amd64_musl` | Linux x86_64 (amd64) 配备 [musl libc](https://musl.libc.org/)，例如 Alpine Linux             |
| `linux_arm64_musl` | Linux AArch64 (arm64) 配备 [musl libc](https://musl.libc.org/)，例如 Alpine Linux            |
| `linux_arm64_android` | Android AArch64 (arm64)                                                                      |
| `wasm_eh`          | WebAssembly 异常处理                                                                           |

下面，我们提供了一些平台的详细构建说明：

* [Android]({% link docs/stable/dev/building/android.md %})
* [Raspberry Pi]({% link docs/stable/dev/building/raspberry_pi.md %})

### 最佳努力支持的平台

| 平台名称          | 描述                                                                                          |
|------------------|-----------------------------------------------------------------------------------------------|
| `freebsd_amd64`  | FreeBSD x86_64 (amd64)                                                                         |
| `freebsd_arm64`  | FreeBSD AArch64 (arm64)                                                                        |
| `wasm_mvp`       | WebAssembly 最小可行产品                                                                       |
| `windows_amd64_mingw` | Windows 10+ x86_64 (amd64) 配备 MinGW                                                       |
| `windows_arm64_mingw` | Windows 10+ AArch64 (arm64) 配备 MinGW                                                      |

> 这些平台不在 DuckDB 社区支持范围内。有关商业支持的详细信息，请查看 [支持政策页面](https://duckdblabs.com/community_support_policy#platforms)。

也可以查看 [“非官方和不支持的平台”页面]({% link docs/stable/dev/building/unofficial_and_unsupported_platforms.md %}) 了解更多详情。

### 过时平台

一些平台在旧版 DuckDB 中得到了支持，但现在不再支持。

| 平台名称          | 描述                                                                                          |
|------------------|-----------------------------------------------------------------------------------------------|
| `linux_amd64_gcc4` | Linux AMD64 (x86_64) 配备 GCC 4，例如 CentOS 7                                               |
| `linux_arm64_gcc4` | Linux AArch64 (arm64) 配备 GCC 4，例如 CentOS 7                                               |
| `windows_amd64_rtools` | Windows 10+ x86_64 (amd64) 用于 [RTools](https://cran.r-project.org/bin/windows/Rtools/)     |

也可以使用为 macOS 和 Linux 提供的说明，构建 DuckDB 用于诸如 [macOS 11](https://endoflife.date/macos) 和 [CentOS 7/8](https://endoflife.date/centos) 等生命周期结束的平台。

## 合并构建

DuckDB 可以构建为一个包含 C++ 头文件和源代码文件（`duckdb.hpp` 和 `duckdb.cpp`）的单个文件，大约有 0.5M 行代码。
要生成此文件，请运行：

```batch
python scripts/amalgamation.py
```

请注意，合并构建仅提供最佳努力支持，不提供官方支持。

## 局限性

目前，DuckDB 有以下限制：

* DuckDB 代码库不兼容 [C++23](https://en.wikipedia.org/wiki/C%2B%2B23)。因此，尝试使用 `-std=c++23` 编译 DuckDB 会失败。
* `-march=native` 构建标志，即使用本地机器的原生指令集编译 DuckDB，不被支持。

## 故障排除指南

我们为构建 DuckDB 提供了故障排除指南：

* [通用问题]({% link docs/stable/dev/building/troubleshooting.md %})
* [Python]({% link docs/stable/dev/building/python.md %})
* [R]({% link docs/stable/dev/building/r.md %})