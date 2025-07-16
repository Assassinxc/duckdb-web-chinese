---
---
github_repository: https://github.com/duckdb/duckdb-httpfs
layout: docu
title: HTTP 和 S3 支持的 httpfs 扩展
redirect_from:
- /docs/extensions/httpfs
- /docs/extensions/httpfs/
- /docs/extensions/httpfs/overview
- /docs/extensions/httpfs/overview/
- /docs/stable/extensions/httpfs
- /docs/stable/extensions/httpfs/
- /docs/stable/extensions/httpfs/overview
- /docs/stable/extensions/httpfs/overview/
---

`httpfs` 扩展是一个可自动加载的扩展，实现了一个文件系统，允许读取远程文件/写入远程文件。
对于普通的 HTTP(S)，仅支持文件读取。对于使用 S3 API 的对象存储，`httpfs` 扩展支持读取/写入/[globbing]({% link docs/stable/sql/functions/pattern_matching.md %}#globbing) 文件。

## 安装和加载

`httpfs` 扩展默认会在首次使用该扩展提供的任何功能时自动加载。

要手动安装并加载 `httpfs` 扩展，请运行：

```sql
INSTALL httpfs;
LOAD httpfs;
```

## HTTP(S)

`httpfs` 扩展支持连接到 [HTTP(S) 端点]({% link docs/stable/core_extensions/httpfs/https.md %}).

## S3 API

`httpfs` 扩展支持连接到 [S3 API 端点]({% link docs/stable/core_extensions/httpfs/s3api.md %}).