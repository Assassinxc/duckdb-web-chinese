---
---
layout: docu
redirect_from:
- /docs/dev/building/python
title: Python
---

DuckDB Python 包位于 [DuckDB 源代码仓库](https://github.com/duckdb/duckdb/) 的 `/tools/pythonpkg/` 文件夹下。它使用 [pybind11](https://pybind11.readthedocs.io/en/stable/) 来创建与 DuckDB 的 Python 绑定。

## 前提条件

对于本页面中描述的所有内容，我们做如下假设：

1. 你有一个 DuckDB 源代码的工作副本（包括 Git 标签），并且你从源代码根目录运行命令。
2. 你有一个适合的 Python 安装，并且它位于一个专用的虚拟环境中。

### 1. DuckDB 仓库

确保你已经克隆了 [DuckDB 源代码](https://github.com/duckdb/duckdb/) 并且你在其根目录下。例如：

```batch
git clone https://github.com/duckdb/duckdb
...
cd duckdb
```

如果你已经 _forked_ DuckDB，当你在构建 Python 包时如果没有拉取标签，可能会遇到问题。

```batch
# 检查你的远程仓库
git remote -v

# 如果你没有看到 upstream git@github.com:duckdb/duckdb.git，则添加它
git remote add upstream git@github.com:duckdb/duckdb.git

# 现在你可以拉取和推送标签
git fetch --tags upstream
git push --tags
```

### 2. Python 虚拟环境

在本页中描述的所有内容都需要一个合适的 Python 安装。虽然你技术上可能能够使用系统 Python，但我们 **强烈建议** 你使用一个 Python 虚拟环境。虚拟环境可以隔离依赖项，并且根据你使用的工具，还能让你控制使用的 Python 解释器。这样就不会污染系统范围的 Python 安装，也不会让项目所需的包相互干扰。

虽然我们在下面的例子中使用了 Python 的内置 `venv` 模块，而且技术上这可能会（或可能不会）对你有效，但我们 **强烈建议** 使用像 [astral uv](https://docs.astral.sh/uv/)（或 Poetry、conda 等）这样的工具，它可以管理 _Python 解释器版本_ 和 _虚拟环境_。

创建并激活一个虚拟环境如下：

```batch
# 在 duckdb 源代码根目录下创建一个虚拟环境
python3 -m venv --prompt duckdb .venv

# 激活虚拟环境
source .venv/bin/activate
```

确保你的虚拟环境中有一个足够新的 `pip` 版本：

```batch
# 打印 pip 帮助
python3 -m pip install --upgrade pip
```

如果失败并提示 `No module named pip` 并且你使用的是 `uv`，则运行：

```batch
# 安装 pip
uv pip install pip
```

## 从源代码构建

以下是构建 Python 库的几种选项，可以包含或不包含调试符号，并使用默认或自定义的 [扩展]({% link docs/stable/extensions/overview.md %})。如果你在构建 DuckDB 主库时遇到问题，请查看 [DuckDB 构建文档]({% link docs/stable/dev/building/overview.md %})。

### 默认发布版、调试构建或云存储

以下将使用默认的扩展集（json、parquet、icu 和 core_functions）构建包。

#### 发布构建

```batch
GEN=ninja BUILD_PYTHON=1 make release
```

#### 调试构建

```batch
GEN=ninja BUILD_PYTHON=1 make debug
```

#### 验证

```batch
python3 -c "import duckdb; print(duckdb.sql('SELECT 42').fetchall())"
```

### 添加扩展

在考虑静态链接扩展之前，你应该知道 Python 包目前对链接的扩展处理得不是很好。如果你不需要将扩展内联，建议你只需按照 [运行时安装它们]({% link docs/stable/extensions/installing_extensions.md %})。查看 `tools/pythonpkg/duckdb_extension_config.cmake` 以了解默认构建的扩展列表。任何其他扩展都应被视为有问题。

尽管如此，如果你想尝试一下，以下是具体步骤。

> 有关构建 DuckDB 扩展的更多细节，请查看 [文档]({% link docs/stable/dev/building/building_extensions.md %}).

DuckDB 构建过程遵循以下逻辑来构建扩展：

1. 首先组合可能包含在构建中的所有扩展。
1. 然后组合不应包含在构建中的所有扩展。
1. 通过从包含的扩展中减去排除的扩展，组合最终的扩展集。

以下机制会增加到 **_包含_ 的扩展** 集合中：

| 机制                                                                 | 语法 / 示例                                                                                               |
| -------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| **默认启用的内置扩展**                                               | `extension/extension_config.cmake`（≈30 个内置）                                                         |
| **默认启用的 Python 包扩展**                                         | `tools/pythonpkg/duckdb_extension_config.cmake`（`json;parquet;icu`）                                     |
| **分号分隔的包含列表**                                               | `DUCKDB_EXTENSIONS=fts;tpch;json`                                                                         |
| **标志**                                                             | `BUILD_TPCH=1`, `BUILD_JEMALLOC=1`, `BUILD_FTS=1`, …                                                     |
| **预设**                                                             | `BUILD_ALL_EXT=1` - 构建所有内树扩展<br/>`BUILD_ALL_IT_EXT=1` - _仅_ 构建内树扩展<br/>`BUILD_ALL_OOT_EXT=1` - 构建所有外树扩展 |
| **自定义配置文件**                                                   | `DUCKDB_EXTENSION_CONFIGS=path/to/my.cmake`                                                               |
| **仅核心扩展覆盖** <br/>_仅在 `DISABLE_BUILTIN_EXTENSIONS=1` 时相关_ | `CORE_EXTENSIONS=httpfs;fts`                                                                              |

---

以下机制会增加到 **_排除_ 的扩展** 集合中：

| 机制                                                                                              | 语法 / 示例                                   |
| -------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| **分号分隔的跳过列表**                                                                              | `SKIP_EXTENSIONS=parquet;jemalloc`             |
| **标志**                                                                                          | `DISABLE_PARQUET=1`, `DISABLE_CORE_FUNCTIONS=1`, … |
| **“无内置”开关** <br/>_排除 *所有* 静态链接的扩展 **除了** `core_functions`。使用 `CORE_EXTENSIONS=…` 来重新白名单_ | `DISABLE_BUILTIN_EXTENSIONS=1`                 |

---

### 显示所有已安装的扩展

```batch
python3 -c "import duckdb; print(duckdb.sql('SELECT extension_name, installed, description FROM duckdb_extensions();'))"
```

## 开发环境

本节将引导你完成以下步骤：

* 创建一个 CMake 配置文件用于开发
* 使用 lldb 调试 Python 扩展代码

你可以在 CLI 或 IDE 中执行这些操作。下面的文档显示了 CLion 的配置，但你也应该能够使用其他 IDE，如 VSCode。

### 从 CLI 调试

运行以下命令来配置调试所需的 CMake 配置文件：

```batch
GEN=ninja BUILD_PYTHON=1 PYTHON_DEV=1 make debug
```

这将完成以下操作：

* 构建带有调试符号的主 DuckDB 库和 Python 库。
* 生成一个 `compile-commands.json` 文件，其中包括 CPython 和 pybind11 头文件，以便你的 IDE 能够使用 intellisense 和 clang-tidy 检查。
* 在你的虚拟环境中安装所需的 Python 依赖项。

构建完成后，进行一个简单的检查以确保一切正常：

```batch
python3 -c "import duckdb; print(duckdb.sql('SELECT 42').fetchall())"
```

### 调试

基本步骤是启动 `lldb`，使用你的虚拟环境的 Python 解释器和你的脚本，然后设置一个断点并运行脚本。
例如，给定一个名为 `dataframe.df` 的脚本，内容如下：

```python
import duckdb
print(duckdb.sql("select * from range(1000)").df())
```

以下命令应该可以工作：

```batch
lldb -- .venv/bin/python3 my_script.py
```

```batch
# 设置断点
(lldb) br s -n duckdb::DuckDBPyRelation::FetchDF
Breakpoint 1: no locations (pending).
WARNING:  Unable to resolve breakpoint to any actual locations.
# 上述警告无害 - 库尚未被导入

# 运行脚本
(lldb) r
...
    frame #0: 0x000000013025833c duckdb.cpython-310-darwin.so`duckdb::DuckDBPyRelation::FetchDF(this=0x00006000012f8d20, date_as_object=false) at pyrelation.cpp:808:7
   805   }
   806
   807   PandasDataFrame DuckDBPyRelation::FetchDF(bool date_as_object) {
-> 808     if (!result) {
   809       if (!rel) {
   810         return py::none();
   811       }
Target 0: (python3) stopped.
```

### 在 IDE / CLion 中调试

你可以在支持 `lldb` 的 IDE 中进行调试。以下是 CLion 的配置说明，你也可以将这些设置复制到你最喜欢的 IDE 中。

#### 配置 CMake 调试配置文件

以下 CMake 配置文件通过生成 `compile-commands.json` 文件来启用 Intellisense 和 clang-tidy，使你的 IDE 知道如何检查源代码，并确保 Python 包会在你的 Python 虚拟环境中构建和安装。

在 **Settings** -> **Build, Execution, Deployment** -> **CMake** 下，添加一个配置文件，并设置如下字段：

* **Name**: Debug
* **Build type**: Debug
* **Generator**: Ninja
* **CMake Options**（单行）：
  ```console
  -DCMAKE_PREFIX_PATH=$CMakeProjectDir$/.venv;$CMAKE_PREFIX_PATH
  -DPython3_EXECUTABLE=$CMakeProjectDir$/.venv/bin/python3
  -DBUILD_PYTHON=1
  -DPYTHON_DEV=1
  ```

#### 创建调试运行配置

在 **Run** -> **Edit Configurations...** 下创建一个新的 **CMake Application**。使用以下值：

* **Name**: Python Debug
* **Target**: `All targets`
* **Executable**: `[ABS_PATH_TO_YOUR_VENV]/bin/python3`（注意：这是一个符号链接，有时 IDE 会尝试跟随它并填充到实际可执行文件的路径，但这样不会起作用）
* **Program arguments**: `$FilePath$`
* **Working directory**: `$ProjectFileDir$`
* **Before Launch**: `Build`（这应该已经设置好了）

保存并关闭即可。

现在你可以在 C++ 文件中设置断点，然后在编辑器中打开你的 Python 脚本，并使用此配置以调试模式运行 `Python Debug`。

### 开发和存根

`duckdb-stubs` 中的 `*.pyi` 存根文件是手动维护的。连接相关的存根文件使用 `tools/pythonpkg/scripts/` 中的专用脚本生成：

* `generate_connection_stubs.py`
* `generate_connection_wrapper_stubs.py`

这些存根文件对于许多 IDE 的自动补全非常重要，因为基于静态分析的语言服务器无法 introspect `duckdb` 的二进制模块。

为了验证存根文件是否与实际实现匹配：

```batch
python3 -m pytest tests/stubs
```

如果你向 DuckDB Python API 添加了新方法，你需要手动将相应的类型提示添加到存根文件中。

### 什么是 py::objects 和 py::handles？

这些是由 pybind11 提供的类，我们使用它来管理与 Python 环境的交互。
`py::handle` 是一个直接封装 PyObject* 的类，不管理任何引用。
`py::object` 与 `py::handle` 类似，但可以处理引用计数。

我之所以用 *can* 是因为它不一定要这么做，使用 `py::reinterpret_borrow<py::object>(...)` 我们可以创建一个非拥有 `py::object`，这实际上只是一个 `py::handle`，但 `py::handle` 不能用于原型要求 `py::object` 的情况。

`py::reinterpret_steal<py::object>(...)` 创建一个拥有 `py::object`，这会增加 Python 对象的引用计数，并在 `py::object` 超出作用域时减少引用计数。

当直接与返回 `PyObject*` 的 Python 函数（如 `PyDateTime_DATE_GET_TZINFO`）进行交互时，通常应将调用包装在 `py::reinterpret_steal` 中，以获取返回对象的所有权。

## 故障排除

### Pip 出现 `No names found, cannot describe anything` 错误

如果你 fork 了 DuckDB，当你在构建 Python 包时如果没有拉取标签，可能会遇到问题。

```batch
# 检查你的远程仓库
git remote -v

# 如果你没有看到 upstream git@github.com:duckdb/duckdb.git，则添加它
git remote add upstream git@github.com:duckdb/duckdb.git

# 现在你可以拉取和推送标签
git fetch --tags upstream
git push --tags
```

### 使用 httpfs 扩展构建时失败

在 OSX 上，当同时包含 [`httpfs` 扩展]({% link docs/stable/core_extensions/httpfs/overview.md %}) 和 Python 包时，构建会失败：

```console
ld: library not found for -lcrypto
clang: error: linker command failed with exit code 1 (use -v to see invocation)
error: command '/usr/bin/clang++' failed with exit code 1
ninja: build stopped: subcommand failed.
make: *** [release] Error 1
```

链接 httpfs 扩展是有问题的。请在运行时安装它，如果可以的话。

### 导入 DuckDB 时出现 `symbol not found in flat namespace` 错误

如果你看到如下错误：

```console
ImportError: dlopen(/usr/bin/python3/site-packages/duckdb/duckdb.cpython-311-darwin.so, 0x0002): symbol not found in flat namespace '_MD5_Final'
```

...那么你很可能尝试链接了一个有问题的扩展。如上所述：`tools/pythonpkg/duckdb_extension_config.cmake` 包含默认的扩展列表，这些扩展与 Python 包一起构建。任何其他扩展都可能引起问题。

### Python 出现 `No module named 'duckdb.duckdb'` 错误

如果你在 `tools/pythonpkg` 目录下并尝试 `import duckdb`，你可能会看到：

```console
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/duckdb/tools/pythonpkg/duckdb/__init__.py", line 4, in <module>
    import duckdb.functional as functional
  File "/duckdb/tools/pythonpkg/duckdb/functional/__init__.py", line 1, in <module>
    from duckdb.duckdb.functional import (
ModuleNotFoundError: No module named 'duckdb.duckdb'
```

这是因为 Python 从 `duckdb` 目录（即 `tools/pythonpkg/duckdb/`）导入，而不是从安装的包中导入。你应该从不同的目录启动你的解释器。