---
---
layout: docu
redirect_from:
- /docs/dev/building/linux
title: Linux
---

## 先决条件

在 Linux 系统上，使用发行版的包管理器安装所需的软件包。

### Ubuntu 和 Debian

#### CLI 客户端

在 Ubuntu 和 Debian（以及 MX Linux、Linux Mint 等）系统上，构建 DuckDB CLI 客户端所需的条件如下：

```batch
sudo apt-get update
sudo apt-get install -y git g++ cmake ninja-build libssl-dev
git clone https://github.com/duckdb/duckdb
cd duckdb
GEN=ninja make
```

### Fedora、CentOS 和 Red Hat

#### CLI 客户端

在 Fedora、CentOS、Red Hat、AlmaLinux、Rocky Linux 等系统上，构建 DuckDB CLI 客户端所需的条件如下：

```batch
sudo yum install -y git g++ cmake ninja-build openssl-devel
git clone https://github.com/duckdb/duckdb
cd duckdb
GEN=ninja make
```

### Alpine Linux

#### CLI 客户端

在 Alpine Linux 系统上，构建 DuckDB CLI 客户端所需的条件如下：

```batch
apk add g++ git make cmake ninja
git clone https://github.com/duckdb/duckdb
cd duckdb
GEN=ninja make
```

#### 使用 musl libc 的性能

请注意，Alpine Linux 使用 [musl libc](https://musl.libc.org/) 作为其 C 标准库。使用 musl libc 构建的 DuckDB 二进制文件相比 glibc 版本性能较低：对于某些工作负载，性能下降可能超过 5 倍。因此，对于性能导向的工作负载，建议使用 glibc。

#### `linux_*_musl` 平台的发行版

从 DuckDB v1.2.0 开始，[_extensions 为 `linux_amd64_musl` 平台提供支持]({% post_url 2025-02-05-announcing-duckdb-120 %}#musl-extensions)（但尚未为 `linux_amd32_musl` 平台提供支持）。然而，目前没有官方的 _DuckDB 二进制文件_ 为 musl libc 提供支持，但可以按照本页的说明手动构建。

#### Alpine Linux 上的 Python 客户端

目前，在 Alpine Linux 上安装 DuckDB Python 需要从源代码进行编译。为此，请在运行 `pip` 之前安装所需的软件包：

```batch
apk add g++ py3-pip python3-dev
pip install duckdb
```

## 在 Linux 上使用 DuckDB CLI 客户端

一旦构建成功，您可以在 `build` 目录中找到 `duckdb` 二进制文件：

```batch
build/release/duckdb
```

对于不同的构建配置（`debug`、`relassert` 等），请参阅 [“构建配置”页面]({% link docs/stable/dev/building/build_configuration.md %}）。

## 使用扩展标志进行构建

要使用扩展标志进行构建，请将 `CORE_EXTENSIONS` 标志设置为要构建的扩展列表。例如：

```batch
CORE_EXTENSIONS='autocomplete;httpfs;icu;json;tpch' GEN=ninja make
```

## 故障排除

### Linux AArch64 上的 R 包：`too many GOT entries` 构建错误

**问题：**
在 ARM64 架构（AArch64）的 Linux 系统上构建 R 包时，可能会出现以下错误信息：

```console
/usr/bin/ld: /usr/include/c++/10/bits/basic_string.tcc:206:
warning: too many GOT entries for -fpic, please recompile with -fPIC
```

**解决方案：**
创建或编辑 `~/.R/Makevars` 文件。此示例还包含 [`MAKEFLAGS 设置以并行化构建]({% link docs/stable/dev/building/r.md %}#the-build-only-uses-a-single-thread )`：

```ini
ALL_CXXFLAGS = $(PKG_CXXFLAGS) -fPIC $(SHLIB_CXXFLAGS) $(CXXFLAGS)
MAKEFLAGS = -j$(nproc)
```

### 构建 httpfs 扩展失败

**问题：**
在 Linux 上构建 [`httpfs` 扩展]({% link docs/stable/core_extensions/httpfs/overview.md %}) 时，可能会出现以下错误。

```console
CMake 错误 at /usr/share/cmake-3.22/Modules/FindPackageHandleStandardArgs.cmake:230 (message):
  无法找到 OpenSSL，请尝试在系统变量 OPENSSL_ROOT_DIR 中设置 OpenSSL 根文件夹路径（缺失：OPENSSL_CRYPTO_LIBRARY
  OPENSSL_INCLUDE_DIR）
```

**解决方案：**
安装 `libssl-dev` 库。

```batch
sudo apt-get install -y libssl-dev
```

然后，使用以下命令进行构建：

```batch
GEN=ninja CORE_EXTENSIONS="httpfs" make
```