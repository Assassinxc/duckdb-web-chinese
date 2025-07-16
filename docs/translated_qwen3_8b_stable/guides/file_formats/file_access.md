---
---
layout: docu
redirect_from:
- /docs/guides/file_formats/file_access
title: '使用 file: 协议进行文件访问'
---

DuckDB 支持使用 `file:` 协议。它目前支持以下格式：

* `file:/some/path`（完全省略主机）
* `file:///some/path`（空主机）
* `file://localhost/some/path`（主机为 `localhost`）

请注意，以下格式 *不支持*，因为它们是非标准的：

* `file:some/relative/path`（相对路径）
* `file://some/path`（双斜杠路径）

此外，`file:` 协议目前不支持远程（非 localhost）主机。