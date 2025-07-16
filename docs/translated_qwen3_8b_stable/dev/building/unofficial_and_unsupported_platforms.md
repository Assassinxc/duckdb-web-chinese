---
---
layout: docu
redirect_from:
- /docs/dev/building/unofficial_and_unsupported_platforms
title: 非官方且不受支持的平台
---

> 警告
> 本页面列出的平台并非官方支持。
> 构建说明是基于尽力而为提供的。
> 社区贡献非常欢迎。

DuckDB 为多个平台构建并分发，这些平台具有[不同级别的支持]({% link docs/stable/dev/building/overview.md %}).
DuckDB _可以构建_ 在其他平台上，但成功程度各不相同。
本页面概述了这些平台，旨在明确哪些平台可以预期正常运行。

## 32 位架构

[32 位架构](https://en.wikipedia.org/wiki/32-bit_computing) 官方不支持，但可以手动为其中一些平台构建 DuckDB。
例如，查看 [32 位 Raspberry Pi 板]({% link docs/stable/dev/building/raspberry_pi.md %}#raspberry-pi-32-bit) 的构建说明。

请注意，32 位平台由于可寻址内存的限制，只能使用最多 4 GiB 的 RAM。

## 大端架构

[大端架构](https://en.wikipedia.org/wiki/Endianness)（如 PowerPC）不被 DuckDB 支持。
虽然 DuckDB 可能在这些架构上构建，
但生成的二进制文件在某些操作上可能会出现 [正确性](https://github.com/duckdb/duckdb/issues/5548) [错误](https://github.com/duckdb/duckdb/issues/9714)。
因此，不建议使用这些架构。

## RISC-V 架构

用户 [“LivingLinux” 在 Bluesky](https://bsky.app/profile/livinglinux.bsky.social) 成功为 [RISC-V](https://en.wikipedia.org/wiki/RISC-V) 架构 [构建了 DuckDB](https://bsky.app/profile/livinglinux.bsky.social/post/3lak5q7mmg42j)，并 [发布了一段关于此的视频](https://www.youtube.com/watch?v=G6uVDH3kvNQ)。构建 DuckDB（包括 `fts` 扩展）的指令如下：

```bash
GEN=ninja \
    CC='gcc-14 -march=rv64gcv_zicsr_zifencei_zihintpause_zvl256b' \
    CXX='g++-14 -march=rv64gcv_zicsr_zifencei_zihintpause_zvl256b' \
    CORE_EXTENSIONS='fts' \
    make
```

对于没有 RISC-V 芯片开发环境的用户，可以使用最新的 [g++-riscv64-linux-gnu](https://github.com/riscv-collab/riscv-gnu-toolchain) 来交叉编译 DuckDB：

```bash
GEN=ninja \
    CC='riscv64-linux-gnu-gcc -march=rv64gcv_zicsr_zifencei_zihintpause_zvl256b' \
    CXX='riscv64-linux-gnu-g++ -march=rv64gcv_zicsr_zifencei_zihintpause_zvl256b' \
    make
```

如需更多关于 DuckDB RISC-V 交叉编译的参考信息，请查看 [mocusez/duckdb-riscv-ci](https://github.com/mocusez/duckdb-riscv-ci) 和 [DuckDB Pull Request #16549](https://github.com/duckdb/duckdb/pull/16549)