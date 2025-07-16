---
---
layout: docu
redirect_from:
- /internals/storage
- /internals/storage/
- /docs/internals/storage
title: 存储版本和格式
---

## 兼容性

### 向后兼容性

_向后兼容性_ 指的是较新的 DuckDB 版本能够读取由旧版 DuckDB 创建的存储文件。DuckDB v0.10 是第一个支持存储格式向后兼容的版本。DuckDB v0.10 可以读取并操作由之前版本 DuckDB 创建的文件 – DuckDB v0.9。

对于未来的 DuckDB 版本，我们的目标是确保从此次发布开始，任何在之后发布的 DuckDB 版本都可以读取以前版本创建的文件。我们希望确保文件格式是完全向后兼容的。这允许您保留存储在 DuckDB 文件中的数据，并保证您无需担心文件是用哪个版本写入的，也无需在版本之间转换文件即可读取这些文件。

### 向前兼容性

_向前兼容性_ 指的是旧版 DuckDB 能够读取由新版 DuckDB 创建的存储文件。DuckDB v0.9 [**部分向前兼容 DuckDB v0.10**]({% post_url 2024-02-13-announcing-duckdb-0100 %}#forward-compatibility)。某些由 DuckDB v0.10 创建的文件可以被 DuckDB v0.9 读取。

向前兼容性基于 **尽力而为** 的原则。虽然存储格式的稳定性很重要，但仍有许多改进和创新我们希望在未来对存储格式进行。因此，向前兼容性可能会（部分）偶尔失效。

## 如何在不同存储格式之间迁移

当您升级 DuckDB 并打开一个旧数据库文件时，可能会遇到有关不兼容存储格式的错误信息，指向本页面。
要将您的数据库迁移到较新的格式，您只需要旧版和新版的 DuckDB 可执行文件。

使用旧版的 DuckDB 打开您的数据库文件并运行 SQL 语句 `EXPORT DATABASE 'tmp'`。这允许您将当前正在使用的数据库的完整状态保存到 `tmp` 文件夹中。
`tmp` 文件夹的内容将被覆盖，因此请选择一个空的或尚未存在的位置。然后，启动新版的 DuckDB 并执行 `IMPORT DATABASE 'tmp'`（指向之前填充的文件夹）以加载数据库，之后可以将其保存到您指定的文件中。

以下是一个 Bash 脚本（请根据文件名和可执行文件路径进行调整）：

```batch
/older/duckdb mydata.old.db -c "EXPORT DATABASE 'tmp'"
/newer/duckdb mydata.new.db -c "IMPORT DATABASE 'tmp'"
```

执行之后，`mydata.old.db` 将保留在旧格式中，`mydata.new.db` 将包含相同的数据，但使用新版 DuckDB 可以访问的格式，`tmp` 文件夹将保存相同的数据，以通用格式作为不同文件存在。

有关语法的更多详细信息，请查看 [`EXPORT` 文档]({% link docs/stable/sql/statements/export.md %}).

### 显式存储版本

[DuckDB v1.2.0 引入了 `STORAGE_VERSION` 选项]({% post_url 2025-02-05-announcing-duckdb-120 %}#explicit-storage-versions)，允许显式指定存储版本。
使用此功能，您可以选择启用新的向前不兼容特性：

```sql
ATTACH 'file.db' (STORAGE_VERSION 'v1.2.0');
```

此设置指定能够读取数据库文件的最小 DuckDB 版本。当使用此选项写入数据库文件时，生成的文件无法被比指定版本更早的 DuckDB 版本打开。它们可以被指定版本和所有更新版本的 DuckDB 读取。

如果您连接到 DuckDB 数据库，可以使用以下命令查询存储版本：

```sql
SELECT database_name, tags FROM duckdb_databases();
```

这将显示存储版本：

```text
┌───────────────┬───────────────────────────────────┐
│ database_name │               tags                │
│    varchar    │       map(varchar, varchar)       │
├───────────────┼───────────────────────────────────┤
│ file1         │ {storage_version=v1.2.0}          │
│ file2         │ {storage_version=v1.0.0 - v1.1.3} │
│ ...           │ ...                               │
└───────────────┴───────────────────────────────────┘
```

这意味着 `file2` 可以被旧版 DuckDB 打开，而 `file1` 仅与 `v1.2.0`（或未来版本）兼容。

### 在存储版本之间转换

要将新格式转换为旧格式以实现兼容性，在 DuckDB v1.2.0+ 中使用以下序列：

```sql
ATTACH 'file1.db';
ATTACH 'converted_file.db' (STORAGE_VERSION 'v1.0.0');
COPY FROM DATABASE file1 TO converted_file;
```

## 存储头

DuckDB 文件以一个 `uint64_t` 开始，该值包含主头的校验和，接着是四个魔法字节（`DUCK`），然后是存储版本号，存储为 `uint64_t`。

```bash
hexdump -n 20 -C mydata.db
```

```text
00000000  01 d0 e2 63 9c 13 39 3e  44 55 43 4b 2b 00 00 00  |...c..9>DUCK+...|
00000010  00 00 00 00                                       |....|
00000014
```

下面是使用 Python 读取存储版本的简单示例。

```python
import struct

pattern = struct.Struct('<8x4sQ')

with open('test/sql/storage_version/storage_version.db', 'rb') as fh:
    print(pattern.unpack(fh.read(pattern.size)))
```

## 存储版本表

查看每个发布版本的更改，请查看 GitHub 上的 [更改日志](https://github.com/duckdb/duckdb/releases)。
要查看更改每个存储版本的提交，请查看 [提交日志](https://github.com/duckdb/duckdb/commits/main/src/storage/storage_info.cpp)。

| 存储版本 | DuckDB 版本 |
|---------:|----------------|
| 66       | v1.3.x         |
| 65       | v1.2.x         |
| 64       | v0.9.x, v0.10.x, v1.0.0, v1.1.x |
| 51       | v0.8.x         |
| 43       | v0.7.x         |
| 39       | v0.6.x         |
| 38       | v0.5.x         |
| 33       | v0.3.3, v0.3.4, v0.4.0 |
| 31       | v0.3.2         |
| 27       | v0.3.1         |
| 25       | v0.3.0         |
| 21       | v0.2.9         |
| 18       | v0.2.8         |
| 17       | v0.2.7         |
| 15       | v0.2.6         |
| 13       | v0.2.5         |
| 11       | v0.2.4         |
| 6        | v0.2.3         |
| 4        | v0.2.2         |
| 1        | v0.2.1 及更早版本 |

## 压缩

DuckDB 使用 [轻量级压缩]({% post_url 2022-10-28-lightweight-compression %}).
请注意，压缩仅应用于持久化数据库，**不适用于内存实例**。

### 压缩算法

DuckDB 支持的压缩算法包括以下内容：

* [常量编码]({% post_url 2022-10-28-lightweight-compression %}#constant-encoding)
* [运行长度编码 (RLE)]({% post_url 2022-10-28-lightweight-compression %}#run-length-encoding-rle)
* [位打包]({% post_url 2022-10-28-lightweight-compression %}#bit-packing)
* [参考框架 (FOR)]({% post_url 2022-10-28-lightweight-compression %}#frame-of-reference)
* [字典编码]({% post_url 2022-10-28-lightweight-compression %}#dictionary-encoding)
* [快速静态符号表 (FSST)]({% post_url 2022-10-28-lightweight-compression %}#fsst) – [VLDB 2020 论文](https://www.vldb.org/pvldb/vol13/p2649-boncz.pdf)
* [自适应无损浮点压缩 (ALP)]({% post_url 2024-02-13-announcing-duckdb-0100 %}#adaptive-lossless-floating-point-compression-alp) – [SIGMOD 2024 论文](https://ir.cwi.nl/pub/33334/33334.pdf)
* [Chimp]({% post_url 2022-10-28-lightweight-compression %}#chimp--patas) – [VLDB 2022 论文](https://www.vldb.org/pvldb/vol15/p3058-liakos.pdf)
* [Patas]({% post_url 2022-11-14-announcing-duckdb-060 %}#compression-improvements)

## 磁盘使用

DuckDB 格式的磁盘使用情况取决于多个因素，包括数据类型和数据分布、使用的压缩方法等。
粗略估计，将 100 GB 的未压缩 CSV 文件加载到 DuckDB 数据库文件中将需要 25 GB 的磁盘空间，而将 100 GB 的 Parquet 文件加载将需要 120 GB 的磁盘空间。

## 行组

DuckDB 的存储格式将数据存储为 _行组_，即数据的水平分区。
这个概念等同于 [Parquet 的行组](https://parquet.apache.org/docs/concepts/)。
DuckDB 的多个特性，包括 [并行处理]({% link docs/stable/guides/performance/how_to_tune_workloads.md %}) 和 [压缩]({% post_url 2022-10-28-lightweight-compression %}) 都基于行组。

## 故障排除

### 打开不兼容数据库文件时的错误信息

当您尝试打开由不同 DuckDB 版本写入的数据库文件时，可能会出现以下错误信息：

```console
错误：无法打开数据库 "...": 序列化错误：无法反序列化: ...
```

此信息表明数据库文件是使用较新的 DuckDB 版本创建的，并且使用了与读取文件的 DuckDB 版本不兼容的特性。

有两种可能的解决方法：

1. 将您的 DuckDB 版本升级到最新的稳定版本。
2. 使用最新版本的 DuckDB 打开数据库，将其导出为标准格式（例如 Parquet），然后使用任何版本的 DuckDB 导入。有关详细信息，请查看 [`EXPORT/IMPORT DATABASE` 语句]({% link docs/stable/sql/statements/export.md %}).

---