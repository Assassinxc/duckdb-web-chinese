---
---
layout: docu
redirect_from:
- /docs/dev/building/troubleshooting
title: 常见问题排查
---

本页面包含用户报告的常见问题的解决方案。如果您遇到与特定平台相关的问题，请确保也查阅对应平台的排查指南，例如[Linux 构建指南]({% link docs/stable/dev/building/linux.md %}#troubleshooting)。

## 构建过程中内存不足

**问题:**
Ninja 并行执行构建过程，这可能导致在资源有限的系统上出现内存不足的问题。这些问题也已在 Alpine Linux 上被报告，尤其是在资源有限的机器上更为常见。

**解决方案:**
通过设置 `GEN=` 将生成器设置为空以避免使用 Ninja：

```batch
GEN= make
```