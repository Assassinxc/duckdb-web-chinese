---
---
github_directory: https://github.com/duckdb/duckdb/tree/main/extension/jemalloc
layout: docu
title: jemalloc 扩展
redirect_from:
- /docs/stable/extensions/jemalloc
- /docs/stable/extensions/jemalloc/
- /docs/extensions/jemalloc
- /docs/extensions/jemalloc/
---

`jemalloc` 扩展将系统内存分配器替换为 [jemalloc](https://jemalloc.net/)。
与其他 DuckDB 扩展不同，`jemalloc` 扩展是静态链接的，无法在运行时安装或加载。

## 操作系统支持

`jemalloc` 扩展的可用性取决于操作系统。

### Linux

DuckDB 的 Linux 发行版已包含 `jemalloc` 扩展。
若要禁用 `jemalloc` 扩展，请[从源代码构建 DuckDB]({% link docs/stable/dev/building/overview.md %})，并按照以下方式设置 `SKIP_EXTENSIONS` 标志：

```bash
GEN=ninja SKIP_EXTENSIONS="jemalloc" make
```

### macOS

DuckDB 的 macOS 版本不包含 `jemalloc` 扩展，但可以通过[从源代码构建]({% link docs/stable/dev/building/macos.md %})来包含它：

```bash
GEN=ninja BUILD_JEMALLOC=1 make
```

### Windows

在 Windows 上，此扩展不可用。

## 配置

### 环境变量

DuckDB 中的 jemalloc 分配器可以通过 [`MALLOC_CONF` 环境变量](https://jemalloc.net/jemalloc.3.html#environment)进行配置。

### 后台线程

默认情况下，jemalloc 的[后台线程](https://jemalloc.net/jemalloc.3.html#background_thread)是禁用的。要启用它们，请使用以下配置选项：

```sql
SET allocator_background_threads = true;
```

后台线程异步清除未完成的分配，因此无需由前台线程同步执行。这可以提高分配性能，在分配密集型的工作负载中尤为明显，尤其是在多核 CPU 上。