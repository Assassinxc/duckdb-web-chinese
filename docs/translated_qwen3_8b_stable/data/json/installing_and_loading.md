---
---
layout: docu
redirect_from:
- /docs/data/json/installing_and_loading
title: 安装和加载 JSON 扩展
---

`json` 扩展默认包含在 DuckDB 构建中，否则在首次使用时会透明地[自动加载]({% link docs/stable/core_extensions/overview.md %}#autoloading-extensions)。如果您希望手动安装和加载它，请运行：

```sql
INSTALL json;
LOAD json;
```