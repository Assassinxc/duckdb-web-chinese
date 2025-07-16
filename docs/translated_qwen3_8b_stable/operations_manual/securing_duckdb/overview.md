---
---
layout: docu
redirect_from:
- /docs/operations_manual/securing_duckdb/overview
title: 保护DuckDB
---

DuckDB功能非常强大，这在某些情况下可能会带来问题，特别是当运行不可信的SQL查询时，例如来自公开用户输入的查询。
本页面列出了一些选项，以限制恶意SQL查询可能带来的影响。

保护DuckDB的方法取决于您的使用场景、环境和潜在的攻击模型。
因此，请仔细考虑与安全相关的配置选项，尤其是在处理机密数据集时。

如果您计划将DuckDB嵌入到您的应用程序中，请参阅[“嵌入DuckDB”]({% link docs/stable/operations_manual/securing_duckdb/embedding_duckdb.md %})页面。

## 报告漏洞

如果您发现潜在的安全漏洞，请通过GitHub[保密报告](https://github.com/duckdb/duckdb/security/advisories/new)。

## 安全模式（CLI）

DuckDB的CLI客户端支持[“安全模式”]({% link docs/stable/clients/cli/safe_mode.md %})，该模式会阻止DuckDB访问除数据库文件以外的任何外部文件。
可以通过命令行参数或[点命令]({% link docs/stable/clients/cli/dot_commands.md %})激活此功能：

```bash
duckdb -safe ...
```

```plsql
.safe_mode
```

## 限制文件访问

DuckDB可以通过其CSV解析器的[`read_csv`函数]({% link docs/stable/data/csv/overview.md %})或通过[`read_text`函数]({% link docs/stable/sql/functions/text.md %}#read_textsource)读取任意文本文件，从而实现读取本地文件系统：

```sql
SELECT *
FROM read_csv('/etc/passwd', sep = ':');
```

### 禁用文件访问

可以通过两种方式禁用文件访问。第一种方法是禁用特定的文件系统。例如：

```sql
SET disabled_filesystems = 'LocalFileSystem';
```

第二种方法是将 [`enable_external_access`选项]({% link docs/stable/configuration/overview.md %}#configuration-reference) 设置为 `false`，以完全禁用外部访问。

```sql
SET enable_external_access = false;
```

此设置意味着：

* `ATTACH` 无法附加到文件中的数据库。
* `COPY` 无法读取或写入文件。
* 如 `read_csv`、`read_parquet`、`read_json` 等函数无法从外部源读取。

### `allowed_directories` 和 `allowed_paths` 选项

您可以使用 `allowed_directories` 和 `allowed_paths` 选项（分别）来限制DuckDB对某些目录或文件的访问。
这些选项允许对文件系统进行细粒度的访问控制。
例如，您可以设置DuckDB仅使用 `/tmp` 目录。

```sql
SET allowed_directories = ['/tmp'];  
SET enable_external_access = false;  
FROM read_csv('test.csv');  
```

应用此设置后，DuckDB将拒绝读取当前工作目录中的文件：

```console
权限错误：
无法访问文件 "test.csv" - 配置已禁用文件系统操作  
```

## 密钥

[密钥]({% link docs/stable/configuration/secrets_manager.md %}) 用于管理登录第三方服务（如AWS或Azure）的凭证。DuckDB可以使用 `duckdb_secrets()` 表函数列出所有密钥。默认情况下，该函数会隐去任何敏感信息，如安全密钥。可以通过设置 `allow_unredacted_secrets` 选项来显示安全密钥中的所有信息。如果您运行的是不可信的SQL输入，不建议启用此选项。

查询可以访问Secrets Manager中定义的密钥。例如，如果有一个密钥用于认证具有写入特定AWS S3存储桶权限的用户，查询可能会写入该存储桶。这适用于持久密钥和临时密钥。

[Persistent secrets]({% link docs/stable/configuration/secrets_manager.md %}#persistent-secrets) 以未加密的二进制格式存储在磁盘上。这些密钥的权限与SSH密钥相同，即 `600`，也就是说，只有运行DuckDB（父）进程的用户才能读取和写入这些密钥。

## 锁定配置

与安全相关的配置设置通常出于安全原因会自我锁定。例如，虽然我们可以通过 `SET allow_community_extensions = false` 禁用[社区扩展]({% link community_extensions/index.md %})，但无法在不重启数据库的情况下重新启用它们。尝试这样做会导致错误：

```console
无效输入错误：数据库运行时无法升级 allow_community_extensions 设置
```

这可以防止不可信的SQL输入重新启用因安全原因而显式禁用的设置。

尽管如此，许多配置设置不会自行禁用，例如资源限制。如果您允许用户在自己的硬件上无限制地运行SQL语句，建议在自己的配置完成后使用以下命令锁定配置：

```sql
SET lock_configuration = true;
```

这可以防止从该点之后任何配置设置被修改。

## 防止SQL注入的预编译语句

与大多数SQL数据库一样，建议在DuckDB中使用[预编译语句]({% link docs/stable/sql/query_syntax/prepared_statements.md %})以防止[SQL注入](https://en.wikipedia.org/wiki/SQL_injection)。

**因此，避免在查询中拼接字符串：**

```python
import duckdb
duckdb.execute("SELECT * FROM (VALUES (32, 'a'), (42, 'b')) t(x) WHERE x = " + str(42)).fetchall()
```

**而是使用预编译语句：**

```python
import duckdb
duckdb.execute("SELECT * FROM (VALUES (32, 'a'), (42, 'b')) t(x) WHERE x = ?", [42]).fetchall()
```

## 限制资源使用

DuckDB可以使用相当多的CPU、RAM和磁盘空间。为了避免拒绝服务攻击，可以限制这些资源。

可以使用以下命令设置DuckDB可以使用的CPU线程数：

```sql
SET threads = 4;
```

其中4是允许的线程数。

还可以限制最大内存（RAM）使用量，例如：

```sql
SET memory_limit = '4GB';
```

可以使用以下命令限制临时文件目录的大小：

```sql
SET max_temp_directory_size = '4GB';
```

## 扩展

DuckDB具有一个强大的扩展机制，其权限与运行DuckDB（父）进程的用户相同。
这引入了安全考虑。因此，我们建议查看[保护扩展]({% link docs/stable/operations_manual/securing_duckdb/securing_extensions.md %})的配置选项。

## 权限

避免以root用户身份运行DuckDB（例如，使用 `sudo`）。
没有理由以root身份运行DuckDB。

## 通用解决方案

也可以通过经过验证的方法来保护DuckDB，例如：

* 通过 [`chroot`](https://en.wikipedia.org/wiki/Chroot) 限制用户权限，依赖操作系统
* 容器化，例如Docker和Podman
* 在WebAssembly中运行DuckDB