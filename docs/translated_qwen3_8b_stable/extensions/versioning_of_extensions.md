---
---
layout: docu
redirect_from:
- /docs/extensions/versioning_of_extensions
title: 扩展版本控制
---

## 扩展版本控制

大多数软件都有某种版本号。版本号具有几个重要的目标：

* 将二进制文件与源代码的特定状态绑定
* 允许确定预期的功能集
* 允许确定 API 的状态
* 允许高效处理 bug 报告（例如，bug `#1337` 在版本 `v3.4.5` 中引入）
* 允许确定发布版本的先后顺序（例如，版本 `v1.2.3` 比 `v1.2.4` 更早）
* 提供预期稳定性的指示（例如，`v0.0.1` 可能不太稳定，而 `v13.11.0` 可能已经稳定）

与 [DuckDB 本身]({% link release_calendar.md %}) 一样，DuckDB 扩展也有自己的版本号。为了确保这些版本号在各种扩展之间具有一致的语义，DuckDB 的 [核心扩展]({% link docs/stable/core_extensions/overview.md %}) 采用了一种版本控制方案，规定了扩展应如何进行版本控制。核心扩展的版本控制方案由三种不同的稳定性级别组成：**不稳定**、**预发布** 和 **稳定**。让我们逐一了解这三种级别及其格式：

### 不稳定扩展

不稳定扩展是那些无法（或不想）对当前稳定性提供任何保证，或其目标是成为稳定扩展的扩展。不稳定扩展使用扩展的 **短 git 哈希值** 进行标记。

例如，在撰写本文时，`vss` 扩展的版本是一个不稳定扩展，版本为 `690bfc5`。

从一个版本号为 **不稳定** 格式的扩展中可以期待什么？

* 通过查找扩展仓库中的哈希值可以找到扩展源代码的状态
* 每次发布，功能可能会发生变化或完全被移除
* 该扩展的 API 可能会在每次发布时发生变化
* 该扩展可能不会遵循结构化的发布周期，新的（破坏性）版本可能随时推出

### 预发布扩展

预发布扩展是不稳定扩展的下一步。它们使用 **[语义化版本控制](https://semver.org/)** 格式进行标记，更具体地说，是 `v0.y.z` 格式。在语义化版本控制中，以 `v0` 开头的版本具有特殊含义：它们表示更严格的常规版本（`>v1.0.0`）语义尚未适用。基本上，这意味着该扩展正在朝向成为稳定扩展的方向发展，但尚未完全实现。

例如，在撰写本文时，`delta` 扩展的版本是一个预发布扩展，版本为 `v0.1.0`。

从一个版本号为 **预发布** 格式的扩展中可以期待什么？

* 该扩展是从与标签对应的源代码编译而来的。
* 语义化版本控制语义适用。详情请参阅 [语义化版本控制](https://semver.org/) 规范。
* 该扩展遵循一个发布周期，在此周期中，新功能会在夜间构建中进行测试，然后再将其归类为发布版本并推送到 `core` 仓库。
* 应该有发布说明，说明每个发布版本中新增了哪些内容，以便于理解不同版本之间的差异。

### 稳定扩展

稳定扩展是扩展稳定性的最终阶段。这通过使用 **稳定语义化版本控制** 格式 `vx.y.z` 来表示，其中 `x>0`。

例如，在撰写本文时，`parquet` 扩展的版本是一个稳定扩展，版本为 `v1.0.0`。

从一个版本号为 **稳定** 格式的扩展中可以期待什么？基本上和预发布扩展相同，但现在更严格的语义化版本控制语义适用：扩展的 API 应该是稳定的，只有在主版本升级时才会以向后不兼容的方式更改。详情请参阅语义化版本控制规范。

## 预发布和稳定核心扩展的发布周期

一般来说，扩展的发布周期取决于其稳定性级别。**不稳定** 扩展通常与 DuckDB 的发布周期保持同步，但可能在 DuckDB 发布之间进行静默更新。**预发布** 和 **稳定** 扩展遵循自己的发布周期。这些发布周期可能与 DuckDB 发布周期重合，也可能不重合。要了解特定扩展的发布周期，请参考相应扩展的文档或 GitHub 页面。通常，**预发布** 和 **稳定** 扩展会将它们的发布作为 GitHub 发布来记录，例如你可以在 [`delta` 扩展](https://github.com/duckdb/duckdb-delta/releases) 中看到示例。

最后，有一个小例外：所有 [内树]({% link docs/stable/extensions/advanced_installation_methods.md %}#in-tree-vs-out-of-tree) 扩展都简单地遵循 DuckDB 的发布周期。

## 夜间构建

与 DuckDB 本身一样，DuckDB 的核心扩展也有夜间或开发构建，可以在它们正式发布之前尝试这些功能。这对于你的工作流程依赖于新功能，或者需要确认你的栈与即将发布的版本兼容时非常有用。

由于目前 DuckDB 扩展二进制文件与单个 DuckDB 版本紧密绑定，因此夜间构建的扩展可能会略微复杂。由于这种紧密绑定，存在组合爆炸的潜在风险。因此，并非所有夜间扩展构建与夜间 DuckDB 构建的组合都是可用的。

一般来说，使用夜间构建有两种方式：使用夜间 DuckDB 构建和使用稳定 DuckDB 构建。让我们看看两者的区别：

### 从稳定 DuckDB

大多数情况下，用户会对特定扩展的夜间构建感兴趣，但不一定想切换到使用 DuckDB 本身的夜间构建。这允许使用特定的前沿功能，同时限制暴露于不稳定代码。

要实现这一点，核心扩展倾向于定期将构建推送到 [`core_nightly` 仓库]({% link docs/stable/extensions/installing_extensions.md %}#extension-repositories)。让我们看一个示例：

首先，我们安装一个 [**稳定 DuckDB 构建**]({% link docs/installation/index.html %}).

然后我们可以安装并加载一个 **夜间** 扩展，如下所示：

```sql
INSTALL aws FROM core_nightly;
LOAD aws;
```

在这个示例中，我们使用了 aws 扩展的最新 **夜间** 构建，以及 DuckDB 的最新 **稳定** 版本。

### 从夜间 DuckDB

当 DuckDB CI 生成 DuckDB 自身的夜间二进制文件时，这些二进制文件会与一组固定版本的扩展一起分发。该扩展版本会在特定的 DuckDB 构建中进行测试，但可能不是最新的开发构建。让我们看一个示例：

首先，我们安装一个 [**夜间 DuckDB 构建**]({% link docs/installation/index.html %})。然后，我们可以像预期一样安装并加载 `aws` 扩展：

```sql
INSTALL aws;
LOAD aws;
```

## 更新扩展

DuckDB 有一个专门的语句，可以自动将所有扩展更新到最新版本。输出将为用户提供哪些扩展从哪个版本更新到哪个版本的信息。例如：

```sql
UPDATE EXTENSIONS;
```

<div class="monospace_table"></div>

| extension_name | repository   | update_result       | previous_version | current_version |
| :------------- | :----------- | :------------------ | :--------------- | :-------------- |
| httpfs         | core         | NO_UPDATE_AVAILABLE | 70fd6a8a24       | 70fd6a8a24      |
| delta          | core         | UPDATED             | d9e5cc1          | 04c61e4         |
| azure          | core_nightly | NO_UPDATE_AVAILABLE | 49b63dc          | 49b63dc         |
| aws            | core         | NO_UPDATE_AVAILABLE | 42c78d3          | 42c78d3         |

请注意，DuckDB 会为每个扩展查找更新的源仓库。因此，如果一个扩展是从 `core_nightly` 安装的，它将使用最新的夜间构建进行更新。

更新语句还可以提供要更新的特定扩展列表：

```sql
UPDATE EXTENSIONS (httpfs, aws);
```

<div class="monospace_table"></div>

| extension_name | repository | update_result       | previous_version | current_version |
| :------------- | :--------- | :------------------ | :--------------- | :-------------- |
| httpfs         | core       | NO_UPDATE_AVAILABLE | 7ce5308          | 7ce5308         |
| aws            | core       | NO_UPDATE_AVAILABLE | 4f318eb          | 4f318eb         |

## 目标 DuckDB 版本

目前，当扩展被编译时，它们与特定版本的 DuckDB 绑定。这意味着，例如，为版本 0.10.3 编译的扩展二进制文件在版本 1.0.0 上无法运行。在大多数情况下，这不会造成任何问题，并且是完全透明的；DuckDB 会自动确保安装与其版本对应的正确二进制文件。对于扩展开发者来说，这意味着他们必须在每次发布新版本的 DuckDB 时创建新的二进制文件。然而，请注意，DuckDB 提供了一个 [扩展模板](https://github.com/duckdb/extension-template)，这使得这一过程变得相对简单。

## 内树 vs. 外树

最初，DuckDB 扩展仅存在于 DuckDB 主仓库 `github.com/duckdb/duckdb` 中，这些扩展称为内树扩展。后来，引入了外树扩展的概念，即扩展被分到自己的仓库中，我们称之为外树扩展。

从用户的角度来看，通常不会有明显的差异，但有一些与版本控制相关的细微差别：

* 内树扩展使用 DuckDB 的版本而不是自己的版本
* 内树扩展没有专门的发布说明，其更改会在常规的 [DuckDB 发布说明](https://github.com/duckdb/duckdb/releases) 中反映
* 核心外树扩展通常存在于名为 `github.com/duckdb/duckdb-⟨extension_name⟩`{:.language-sql .highlight} 的仓库中，但名称可能有所不同。有关核心扩展的完整列表，请参阅 [核心扩展列表]({% link docs/stable/core_extensions/overview.md %})。