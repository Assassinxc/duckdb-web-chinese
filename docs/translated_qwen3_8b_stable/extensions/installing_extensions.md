---
---
layout: docu
redirect_from:
- /docs/extensions/working_with_extensions
- /docs/stable/core_extensions/working_with_extensions
title: 安装扩展
---

要安装核心 DuckDB 扩展，使用 `INSTALL` 命令。
例如：

```sql
INSTALL httpfs;
```

这将从默认仓库（`core`）安装扩展。

## 扩展仓库

默认情况下，DuckDB 扩展是从一个包含由核心 DuckDB 团队构建和签名的扩展的单一仓库中安装的。
这确保了核心扩展集的稳定性和安全性。
这些扩展位于默认的 `core` 仓库中，指向 `http://extensions.duckdb.org`。

除了核心仓库，DuckDB 还支持从其他仓库安装扩展。例如，`core_nightly` 仓库包含核心扩展的夜间构建版本，这些版本是为 DuckDB 的最新稳定版本构建的。这允许用户在正式发布之前尝试扩展中的新功能。

### 从不同仓库安装扩展

要从默认仓库（`core`）安装扩展，请运行：

```sql
INSTALL httpfs;
```

要显式地从核心仓库安装扩展，请运行：

```sql
INSTALL httpfs FROM core;
-- 或
INSTALL httpfs FROM 'http://extensions.duckdb.org';
```

要从核心夜间构建仓库安装扩展：

```sql
INSTALL spatial FROM core_nightly;
-- 或
INSTALL spatial FROM 'http://nightly-extensions.duckdb.org';
```

要从自定义仓库安装扩展：

```sql
INSTALL ⟨custom_extension⟩ FROM 'https://my-custom-extension-repository';
```

或者，可以使用 `custom_extension_repository` 设置更改 DuckDB 使用的默认仓库：

```sql
SET custom_extension_repository = 'http://nightly-extensions.duck
```