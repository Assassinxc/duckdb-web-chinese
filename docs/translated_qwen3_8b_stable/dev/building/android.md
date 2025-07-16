---
---
layout: docu
redirect_from:
- /docs/dev/building/android
title: Android
---

DuckDB 对 Android 有实验性支持。请使用 DuckDB 的最新 `main` 分支，而不是稳定版本。

## 使用 Android NDK 构建 DuckDB 库

我们为使用 macOS 和 Android Studio 的设置提供了构建说明。对于其他设置，请相应调整步骤。

1. 打开 [Android Studio](https://developer.android.com/studio)。
   选择 **Tools** 菜单，然后选择 **SDK Manager**。
   选择 SDK Tools 标签页，并勾选 **NDK (Side by side)** 选项。
   点击 **OK** 进行安装。

1. 设置 Android NDK 的路径。例如：

   ```batch
   ANDROID_NDK=~/Library/Android/sdk/nd
   ```

1. 设置 [Android ABI](https://developer.android.com/ndk/guides/abis)。例如：

   ```batch
   ANDROID_ABI=arm64-v8a
   ```

   或者：

   ```batch
   ANDROID_ABI=x86_64
   ```

1. 如果您想使用 [Ninja 构建系统]({% link docs/stable/dev/building/overview.md %}#prerequisites)，请确保已安装并添加到 `PATH` 中。

1. 设置要构建的 DuckDB 扩展列表。这些扩展将静态链接到二进制文件中。例如：

   ```batch
   DUCKDB_EXTENSIONS="icu;json;parquet"
   ```

1. 导航到 DuckDB 目录并按以下方式运行构建：

   ```batch
   PLATFORM_NAME="android_${ANDROID_ABI}"
   BUILDDIR=./build/${PLATFORM_NAME}
   mkdir -p ${BUILDDIR}
   cd ${BUILDDIR}
   cmake \
       -G "Ninja" \
       -DEXTENSION_STATIC_BUILD=1 \
       -DDUCKDB_EXTRA_LINK_FLAGS="-llog" \
       -DBUILD_EXTENSIONS=${DUCKDB_EXTENSIONS} \
       -DENABLE_EXTENSION_AUTOLOADING=1 \
       -DENABLE_EXTENSION_AUTOINSTALL=1 \
       -DCMAKE_VERBOSE_MAKEFILE=on \
       -DANDROID_PLATFORM=${ANDROID_PLATFORM} \
       -DLOCAL_EXTENSION_REPO="" \
       -DOVERRIDE_GIT_DESCRIBE="" \
       -DDUCKDB_EXPLICIT_PLATFORM=${PLATFORM_NAME} \
       -DBUILD_UNITTESTS=0 \
       -DBUILD_SHELL=1 \
       -DANDROID_ABI=${ANDROID_ABI} \
       -DCMAKE_TOOLCHAIN_FILE=${ANDROID_NDK}/build/cmake/android.toolchain.cmake \
       -DCMAKE_BUILD_TYPE=Release ../..
   cmake \
       --build . \
       --config Release
   ```

1. 对于 `arm64-v8a` ABI，构建将生成 `build/android_arm64-v8a/duckdb` 和 `build/android_arm64-v8a/src/libduckdb.so` 二进制文件。

## 在 Termux 中构建 CLI

1. 要在 [Termux 应用程序](https://termux.dev/) 中构建 [命令行客户端]({% link docs/stable/clients/cli/overview.md %})，请安装以下包：

   ```batch
   pkg install -y git ninja clang cmake python3
   ```

1. 设置要构建的 DuckDB 扩展列表。这些扩展将静态链接到二进制文件中。例如：

   ```batch
   DUCKDB_EXTENSIONS="icu;json"
   ```

1. 按以下方式构建 DuckDB：

   ```batch
   mkdir build
   cd build
   export LDFLAGS="-llog"
   cmake \
      -G "Ninja" \
      -DBUILD_EXTENSIONS="${DUCKDB_EXTENSIONS}" \
      -DDUCKDB_EXPLICIT_PLATFORM=linux_arm64_android \
      -DCMAKE_BUILD_TYPE=Release \
      ..
   cmake --build . --config Release
   ```

请注意，您也可以在 Termux 中使用 Python 客户端：

```batch
pip install --pre --upgrade duckdb
```

## 常见问题排查

### 缺少日志库

**问题：**
构建时出现以下错误：

```console
ld.lld: error: undefined symbol: __android_log_write
```

**解决方法：**
确保链接了日志库：

```batch
export LDFLAGS="-llog"
```