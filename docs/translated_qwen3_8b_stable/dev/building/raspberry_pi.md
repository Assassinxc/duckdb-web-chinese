---
---
layout: docu
redirect_from:
- /docs/dev/building/raspberry_pi
title: Raspberry Pi
---

DuckDB 并未正式为 Raspberry Pi OS（之前称为 Raspbian）发行。
您可以按照本页的说明进行构建。

## Raspberry Pi（64 位）

首先，安装所需的构建包：

```batch
sudo apt-get update
sudo apt-get install -y git g++ cmake ninja-build
```

然后，克隆并构建如下：

```batch
git clone https://github.com/duckdb/duckdb
cd duckdb
GEN=ninja CORE_EXTENSIONS="icu;json" make
```

最后，运行它：

```batch
build/release/duckdb
```

## Raspberry Pi（32 位）

在 32 位的 Raspberry Pi 开发板上，您需要添加 [`-latomic` 链接标志](https://github.com/duckdb/duckdb/issues/13855#issuecomment-2341539339)。
由于此平台不提供扩展的发行版，建议也在此构建中包含它们。
例如：

```batch
mkdir build
cd build
cmake .. \
    -DCORE_EXTENSIONS="httpfs;json;parquet" \
    -DDUCKDB_EXTRA_LINK_FLAGS="-latomic"
make -j4
```