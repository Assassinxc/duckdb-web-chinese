---
---
layout: docu
title: 高级安装方法
---

## 直接从 S3 下载扩展

在构建 [Lambda 服务](https://aws.amazon.com/pm/lambda/) 或使用 DuckDB 的容器时，直接下载扩展可能很有帮助。
DuckDB 的扩展存储在公共的 S3 存储桶中，但这些存储桶的目录结构不可搜索。
因此，必须使用直接指向文件的 URL。
要直接下载扩展文件，请使用以下格式：

```text
http://extensions.duckdb.org/v⟨duckdb_version⟩/⟨platform_name⟩/⟨extension_name⟩.duckdb_extension.gz
```

例如：

```text
http://extensions.duckdb.org/v{{ site.current_duckdb_version }}/windows_amd64/json.duckdb_extension.gz
```

## 从显式路径安装扩展

可以使用 `INSTALL` 命令并指定 `.duckdb_extension` 文件的路径：

```sql
INSTALL 'path/to/httpfs.duckdb_extension';
```

请注意，压缩的 `.duckdb_extension.gz` 文件需要事先解压。也可以指定远程路径。

## 从显式路径加载扩展

`LOAD` 可以与指向 `.duckdb_extension` 文件的路径一起使用。
例如，如果文件位于 (相对) 路径 `path/to/httpfs.duckdb_extension`，可以按如下方式加载：

```sql
LOAD 'path/to/httpfs.duckdb_extension';
```

这将跳过当前已安装的扩展，并直接加载指定的扩展。

请注意，目前无法使用远程路径来处理压缩文件。

## 从源代码构建和安装扩展

有关从源代码构建和安装扩展的信息，请参阅 [DuckDB 构建指南]({% link docs/stable/dev/building/overview.md %}).

### 静态链接扩展

要静态链接扩展，请遵循 [开发者文档中的“使用扩展配置文件”部分](https://github.com/duckdb/duckdb/blob/main/extension/README.md#using-extension-config-files).