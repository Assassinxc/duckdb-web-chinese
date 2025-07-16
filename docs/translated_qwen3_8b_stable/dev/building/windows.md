---
---
layout: docu
redirect_from:
- /docs/dev/building/windows
title: Windows
---

在 Windows 上，DuckDB 需要 [Microsoft Visual C++ Redistributable package](https://learn.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist) 作为构建和运行时的依赖项。请注意，与 UNIX 类系统上的构建过程不同，Windows 构建过程会直接调用 CMake。

## Visual Studio

为了在 Windows 上构建 DuckDB，我们推荐使用 Visual Studio 编译器。
要使用它，请按照 [CI workflow](https://github.com/duckdb/duckdb/blob/52b43b166091c82b3f04bf8af15f0ace18207a64/.github/workflows/Windows.yml#L73) 中的说明操作：

```batch
python scripts/windows_ci.py
cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_GENERATOR_PLATFORM=x64 \
    -DENABLE_EXTENSION_AUTOLOADING=1 \
    -DENABLE_EXTENSION_AUTOINSTALL=1 \
    -DDUCKDB_EXTENSION_CONFIGS="${GITHUB_WORKSPACE}/.github/config/bundled_extensions.cmake" \
    -DDISABLE_UNITY=1 \
    -DOVERRIDE_GIT_DESCRIBE="$OVERRIDE_GIT_DESCRIBE"
cmake --build . --config Release --parallel
```

## MSYS2 和 MinGW64

DuckDB 也可以使用 [MSYS2](https://www.msys2.org/) 和 [MinGW64](https://www.mingw-w64.org/) 在 Windows 上进行构建。
请注意，这种构建方式仅出于兼容性原因支持，如果在特定平台上无法使用 Visual Studio 构建，请才应使用这种方式。
要使用 MinGW64 构建 DuckDB，请使用 Pacman 安装所需的依赖项。
当提示 `Enter a selection (default=all)` 时，请按 `Enter` 选择默认选项。

```batch
pacman -Syu git mingw-w64-x86_64-toolchain mingw-w64-x86_64-cmake mingw-w64-x86_64-ninja
git clone https://github.com/duckdb/duckdb
cd duckdb
cmake -G "Ninja" -DCMAKE_BUILD_TYPE=Release -DBUILD_EXTENSIONS="icu;parquet;json"
cmake --build . --config Release
```

一旦构建成功，您可以在仓库目录中找到 `duckdb.exe` 二进制文件：

```batch
./duckdb.exe
```

## 构建 Go 客户端

在 Windows 上构建可能会遇到以下错误：

```bash
go build
```

```console
collect2.exe: error: ld returned 5 exit status
```

GitHub 用户 [vdmitriyev](https://github.com/vdmitriyev) 分享了在 Windows 上构建 [DuckDB Go 客户端](https://github.com/marcboeker/go-duckdb/issues/4#issuecomment-2176409066) 的说明：

1. 从 `libduckdb-windows-amd64.zip` 归档文件中获取四个文件（`.dll, .lib, .hpp, .h`）。

2. 将它们放到例如 `C:\DuckDB-Go\libs\` 目录中。

3. 按照 [`go-duckdb` 项目](https://github.com/marcboeker/go-duckdb) 安装依赖项。

4. 使用以下说明构建您的项目：

   ```batch
   set PATH=C:\DuckDB-Go\libs\;%PATH%
   set CGO_CFLAGS=-IC:\DuckDB-Go\libs\
   set CGO_LDFLAGS=-LC:\DuckDB-Go\libs\ -lduckdb
   go build
   ```