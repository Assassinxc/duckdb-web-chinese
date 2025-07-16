---
---
layout: docu
redirect_from:
- /docs/extensions
- /docs/extensions/
- /docs/extensions/overview
title: 扩展
---

DuckDB 具备灵活的扩展机制，允许动态加载扩展。
扩展可以通过提供对额外文件格式的支持、引入新类型以及领域特定功能来增强 DuckDB 的功能。

> 扩展可在所有客户端（例如 Python 和 R）上加载。
> 通过 Core 和 Community 仓库分发的扩展均在 macOS、Windows 和 Linux 上构建和测试。所有操作系统均支持 AMD64 和 ARM64 架构。

## 列出扩展

使用 `duckdb_extensions` 函数获取扩展列表：

```sql
SELECT extension_name, installed, description
FROM duckdb_extensions();
```

| extension_name    | installed | description                                                  |
|-------------------|-----------|--------------------------------------------------------------|
| arrow             | false     | Apache Arrow 和 DuckDB 之间的零拷贝数据集成                  |
| autocomplete      | false     | 在 shell 中添加自动补全支持                                  |
| ...               | ...       | ...                                                          |

此列表将显示哪些扩展可用，哪些已安装，版本如何，安装位置在哪里，以及更多信息。
该列表包含大多数，但并非所有，可用的核心扩展。完整的扩展列表请参阅 [核心扩展列表]({% link docs/stable/core_extensions/overview.md %}).

## 内置扩展

DuckDB 的二进制发行版默认包含几个内置扩展。它们被静态链接到二进制文件中，可直接使用。
例如，使用内置的 [`json` 扩展]({% link docs/stable/data/json/overview.md %}) 读取 JSON 文件：

```sql
SELECT *
FROM 'test.json';
```

为了使 DuckDB 发行版保持轻量，仅包含少量必要的扩展，不同发行版之间略有差异。哪个平台包含哪些扩展，请参阅 [核心扩展列表]({% link docs/stable/core_extensions/overview.md %}#default-extensions).

## 安装更多扩展

要使非内置的扩展在 DuckDB 中可用，需要完成以下两个步骤：

1. **扩展安装** 是下载扩展二进制文件并验证其元数据的过程。安装期间，DuckDB 会将下载的扩展和一些元数据存储在本地目录中。从该目录中，DuckDB 可以在需要时加载扩展。这意味着安装只需进行一次。

2. **扩展加载** 是将二进制文件动态加载到 DuckDB 实例中的过程。DuckDB 会在本地扩展目录中搜索已安装的扩展，然后加载它以使其功能可用。这意味着每次重启 DuckDB 时，所有使用的扩展都需要（重新）加载。

> 扩展安装和加载受一些 [限制]({% link docs/stable/extensions/installing_extensions.md %}#limitations) 的约束。

有两种主要方法可以让 DuckDB 执行 **安装** 和 **加载** 步骤：**显式** 和 **自动加载**。

### 显式 `INSTALL` 和 `LOAD`

在 DuckDB 中，也可以显式安装和加载扩展。非自动加载和自动加载的扩展都可以通过这种方式安装。
要显式安装和加载扩展，DuckDB 提供了专用的 SQL 语句 `LOAD` 和 `INSTALL`。例如，
要安装和加载 [`spatial` 扩展]({% link docs/stable/core_extensions/spatial/overview.md %})，运行：

```sql
INSTALL spatial;
LOAD spatial;
```

通过这些语句，DuckDB 会确保 spatial 扩展已安装（如果已安装则忽略 `INSTALL` 语句），然后继续
加载 spatial 扩展（如果已加载则再次忽略语句）。

#### 扩展仓库

可选地，可以通过在 `INSTALL` / `FORCE INSTALL` 命令后附加 `FROM ⟨repository⟩`{:.language-sql .highlight} 提供一个仓库，从该仓库安装扩展。
该仓库可以是别名，如 [`community`]({% link community_extensions/index.md %})，也可以是直接 URL，作为单引号字符串提供。

安装/加载扩展后，可以使用 [`duckdb_extensions` 函数](#listing-extensions) 获取更多信息。

### 自动加载扩展

对于许多 DuckDB 的核心扩展，显式加载和安装扩展并非必需。DuckDB 包含一个自动加载机制
可以在查询中使用扩展时立即安装和加载核心扩展。例如，当运行：

```sql
SELECT *
FROM 'https://raw.githubusercontent.com/duckdb/duckdb-web/main/data/weather.csv';
```

DuckDB 会自动安装并加载 [`httpfs`]({% link docs/stable/core_extensions/httpfs/overview.md %}) 扩展。不需要显式的 `INSTALL` 或 `LOAD` 语句。

并非所有扩展都可以自动加载。这可能有多种原因：某些扩展对运行中的 DuckDB 实例进行了多项更改，使自动加载在技术上尚不可行。对于其他扩展，由于它们对 DuckDB 的行为进行了修改，更倾向于在使用前让用户明确选择安装。

要查看哪些扩展可以自动加载，请参阅 [核心扩展列表]({% link docs/stable/core_extensions/overview.md %}).

### 社区扩展

DuckDB 支持安装第三方 [社区扩展]({% link community_extensions/index.md %})。例如，您可以通过以下方式安装 [`avro` 社区扩展]({% link community_extensions/extensions/avro.md %})：

```sql
INSTALL avro FROM community;
```

社区扩展由社区成员贡献，但它们会被构建、[签名]({% link docs/stable/extensions/extension_distribution.md %}#signed-extensions) 并在一个集中的仓库中分发。

## 更新扩展

由于内置扩展是作为 DuckDB 二进制文件的一部分构建的，因此它们与 DuckDB 的版本绑定。然而，可安装的扩展可以并确实会收到更新。为了确保所有当前安装的扩展都处于最新版本，可以调用：

```sql
UPDATE EXTENSIONS;
```

有关扩展版本的更多信息，请参阅 [扩展版本页面]({% link docs/stable/extensions/versioning_of_extensions.md %}).

## 开发扩展

核心扩展使用的相同 API 也适用于开发扩展。这允许用户扩展 DuckDB 的功能，使其最适合他们的领域。
创建扩展的模板可在 [`extension-template` 仓库](https://github.com/duckdb/extension-template/) 中找到。该模板还包含了一些关于如何开始构建您自己的扩展的文档。

## 使用扩展

查看 [安装指南]({% link docs/stable/extensions/installing_extensions.md %}) 和 [高级安装方法页面]({% link docs/stable/extensions/advanced_installation_methods.md %}).