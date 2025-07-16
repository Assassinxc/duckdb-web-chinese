---
---
layout: docu
redirect_from:
- /docs/dev/building/r
title: R
---

本页面包含构建 R 客户端库的说明。

## 构建过程仅使用单线程

**问题：**
默认情况下，R 使用单线程编译包，这会导致构建过程变慢。

**解决方案：**
为了并行编译，创建或编辑 `~/.R/Makevars` 文件，并添加如下一行内容：

```ini
MAKEFLAGS = -j8
```

以上内容将使用 8 个线程并行编译。在 Linux/macOS 系统上，您可以添加以下内容以使用机器所有的线程：

```ini
MAKEFLAGS = -j$(nproc)
```

不过，请注意，使用的线程越多，内存消耗也越高。如果在编译过程中系统内存不足，R 会话将会崩溃。