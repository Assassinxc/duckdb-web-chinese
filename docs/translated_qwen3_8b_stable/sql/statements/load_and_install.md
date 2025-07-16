---
---
layout: docu
railroad: statements/load_and_install.js
redirect_from:
- /docs/sql/statements/load_and_install
title: LOAD / INSTALL 语句
---

## `INSTALL`

`INSTALL` 语句用于下载扩展，以便将其加载到 DuckDB 会话中。

### 示例

安装 [`httpfs`]({% link docs/stable/core_extensions/httpfs/overview.md %}) 扩展：

```sql
INSTALL httpfs;
```

安装 [`h3` 社区扩展]({% link community_extensions/extensions/h3.md %})：

```sql
INSTALL h3 FROM community;
```

### 语法

<div id="rrdiagram2"></div>

## `LOAD`

`LOAD` 语句用于将已安装的 DuckDB 扩展加载到当前会话中。

### 示例

加载 [`httpfs`]({% link docs/stable/core_extensions/httpfs/overview.md %}) 扩展：

```sql
LOAD httpfs;
```

加载 [`spatial`]({% link docs/stable/core_extensions/spatial/overview.md %}) 扩展：

```sql
LOAD spatial;
```

### 语法

<div id="rrdiagram1"></div>

---