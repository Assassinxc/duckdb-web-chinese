---
---
layout: docu
redirect_from:
- /docs/dev/building/build_configuration
title: 构建配置
---

## 构建类型

DuckDB 可以在多种不同的设置下进行构建，其中大部分与 CMake 对应，但并非全部。

### `release`

此构建移除了所有断言和调试符号以及代码，优化了性能。

### `debug`

此构建包含所有调试信息，包括符号、断言和 `#ifdef DEBUG` 代码块。
由于这些原因，此构建的二进制文件预计会很慢。
注意：此构建不会自动设置特殊的调试定义。

### `relassert`

此构建不会触发 `#ifdef DEBUG` 代码块，但它仍保留调试符号，使其能够通过行号信息逐步执行，并且 `D_ASSERT` 行在此构建中仍然被检查。
此构建模式的二进制文件比 `debug` 模式快得多。

### `reldebug`

此构建在很多方面与 `relassert` 相似，只是此构建中也去除了断言。

### `benchmark`

此构建是 `release` 的简写形式，并设置了 `BUILD_BENCHMARK=1`。

### `tidy-check`

此构建会创建一个构建，然后运行 [Clang-Tidy](https://clang.llvm.org/extra/clang-tidy/) 通过静态分析检查问题或风格违规。
CI 也会运行此检查，如果此检查失败，会导致构建失败。

### `format-fix` | `format-changes` | `format-main`

此选项实际上不会创建构建，而是使用以下格式检查器检查风格问题：

* [clang-format](https://clang.llvm.org/docs/ClangFormat.html) 用于修复代码中的格式问题。
* [cmake-format](https://cmake-format.readthedocs.io/en/latest/) 用于修复 `CMakeLists.txt` 文件中的格式问题。

CI 也会运行此检查，如果此检查失败，会导致构建失败。

## 扩展选择

[核心 DuckDB 扩展]({% link docs/stable/core_extensions/overview.md %}) 是由 DuckDB 团队维护的。这些扩展托管在 `duckdb` GitHub 组织中，并由 `core` 扩展仓库提供。

核心扩展可以通过 `CORE_EXTENSIONS` 标志作为 DuckDB 的一部分进行构建，然后列出要构建的扩展名称。

```bash
CORE_EXTENSIONS='tpch;httpfs;fts;json;parquet' make
```

更多相关内容请参阅 [构建 DuckDB 扩展]({% link docs/stable/dev/building/building_extensions.md %}).

## 包标志

对于每个由核心 DuckDB 维护的包，Makefile 中都有一个标志来启用构建该包。
这些标志可以通过在当前 `env` 中设置、通过 `bashrc` 或 `zshrc` 等设置文件，或在调用 `make` 之前设置来启用，例如：

```bash
BUILD_PYTHON=1 make debug
```

### `BUILD_PYTHON`

当此标志被设置时，会构建 [Python]({% link docs/stable/clients/python/overview.md %}) 包。

### `BUILD_SHELL`

当此标志被设置时，会构建 [CLI]({% link docs/stable/clients/cli/overview.md %})，这通常默认启用。

### `BUILD_BENCHMARK`

当此标志被设置时，会构建 DuckDB 的内部基准测试套件。
有关此内容的更多信息，请参阅 [README](https://github.com/duckdb/duckdb/blob/main/benchmark/README.md)。

### `BUILD_JDBC`

当此标志被设置时，会构建 [Java]({% link docs/stable/clients/java.md %}) 包。

### `BUILD_ODBC`

当此标志被设置时，会构建 [ODBC]({% link docs/stable/clients/odbc/overview.md %}) 包。

## 其他标志

### `DISABLE_UNITY`

为了提高编译速度，我们使用 [Unity Build](https://cmake.org/cmake/help/latest/prop_tgt/UNITY_BUILD.html) 来合并翻译单元。
然而这可能会隐藏包含错误，此标志禁用 unity 构建，以便检测这些错误。

### `DISABLE_SANITIZER`

在某些情况下，运行带有 sanitizer 启用的可执行文件可能不被支持 / 可能导致问题。Julia 就是其中的一个例子。
启用此标志时，构建将禁用 sanitizer。

## 覆盖 Git 哈希和版本

在从源代码构建时，可以使用 `OVERRIDE_GIT_DESCRIBE` 环境变量覆盖 Git 哈希和版本。
这在构建不属于完整 Git 仓库的源代码时（例如，没有提交哈希和标签信息的存档文件）非常有用。
例如：

```bash
OVERRIDE_GIT_DESCRIBE=v0.10.0-843-g09ea97d0a9 GEN=ninja make
```

运行 `./build/release/duckdb` 时将输出以下内容：

```text
v0.10.1-dev843 09ea97d0a9
...
```