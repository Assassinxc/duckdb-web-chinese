---
---
layout: docu
redirect_from:
- /docs/operations_manual/securing_duckdb/securing_extensions
title: 扩展安全
---

DuckDB 有一个强大的扩展机制，其权限与运行 DuckDB 的（父）进程的用户权限相同。
这引入了安全考虑。因此，我们建议您审查本页列出的配置选项，并根据您的攻击模型进行设置。

## DuckDB 签名检查

DuckDB 扩展在每次加载时都会通过二进制文件的签名进行检查。
目前扩展有三个类别：

* 使用 `core` 密钥签名。只有经过核心 DuckDB 团队审核的扩展才会使用这些密钥进行签名。
* 使用 `community` 密钥签名。这些是通过 [DuckDB 社区扩展仓库]({% link community_extensions/index.md %}) 分发的开源扩展。
* 未签名。

## 扩展的安全级别概述

DuckDB 为扩展提供了以下安全级别。

| 可用扩展 | 描述 | 配置 |
|-----|---|---|
| `core` | 仅能加载由 `core` 密钥签名的扩展。 | `SET allow_community_extensions = false` |
| `core` 和 `community` | 仅能加载由 `core` 或 `community` 密钥签名的扩展。 | 这是默认的安全级别。 |
| 任何扩展，包括未签名 | 可以加载任何扩展。 | `SET allow_unsigned_extensions = true` |

与安全相关的配置设置 [会锁定自身]({% link docs/stable/operations_manual/securing_duckdb/overview.md %}#locking-configurations)，即只能在当前进程中限制能力。

例如，尝试以下配置更改将导致错误：

```sql
SET allow_community_extensions = false;
SET allow_community,extensions = true;
```

```console
无效输入错误：数据库运行时无法升级 allow_community_extensions 设置
```

## 社区扩展

DuckDB 有一个 [社区扩展仓库]({% link community_extensions/index.md %})，允许方便地安装第三方扩展。
像 pip 或 npm 这样的社区扩展仓库本质上是通过设计启用远程代码执行。这比听起来要不那么严重。无论好坏，我们已经习惯于将随机脚本从网络导入我们的 shell，而且通常在不加思索的情况下安装大量传递依赖。一些仓库如 CRAN 会在某个阶段强制进行人工检查，但这并不能保证任何安全性。

我们研究了多种不同的社区扩展仓库方法，并选择了我们认为合理的方法：我们不尝试审核提交内容，但要求 *扩展的源代码必须公开*。我们接管了完整的构建、签名和分发流程。请注意，这比 pip 和 npm 允许上传任意二进制文件要更严格，但比手动审核所有内容要宽松。我们允许用户 [报告恶意扩展](https://github.com/duckdb/community-extensions/security/advisories/new)，并展示 GitHub 星标和下载数量等采用统计信息。因为我们管理仓库，我们可以迅速将有问题的扩展从分发中移除。

尽管如此，从社区扩展仓库安装和加载 DuckDB 扩展将执行由第三方开发者编写的代码，因此 *可能* 是危险的。恶意开发者可以创建并注册一个看起来无害的 DuckDB 扩展，窃取您的加密货币。
如果您正在运行一个执行用户未信任 SQL 的网络服务，并使用 DuckDB，我们建议禁用社区扩展。要做到这一点，请运行：

```sql
SET allow_community_extensions = false;
```

## 禁用自动安装和自动加载已知扩展

默认情况下，DuckDB 会自动安装和加载已知扩展。要禁用自动安装已知扩展，请运行：

```sql
SET autoinstall_known_extensions = false;
```

要禁用自动加载已知扩展，请运行：

```sql
SET autoload_known_extensions = false;
```

要锁定此配置，请使用 [`lock_configuration` 选项]({% link docs/stable/operations_manual/securing_duckdb/overview.md %}#locking-configurations)：

```sql
SET lock_configuration = true;
```

## 总是要求签名扩展

默认情况下，DuckDB 要求扩展必须是签名的 core 扩展（由 DuckDB 开发者创建）或 community 扩展（由第三方开发者创建，但由 DuckDB 开发者分发）。
可以在启动时启用 [`allow_unsigned_extensions` 设置]({% link docs/stable/core_extensions/overview.md %}#unsigned-extensions)，以允许加载未签名的扩展。
虽然此设置对扩展开发很有用，但启用它将允许 DuckDB 加载 *任何扩展*，这意味着必须更加小心以确保不加载恶意扩展。