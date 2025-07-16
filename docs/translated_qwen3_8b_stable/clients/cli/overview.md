---
---
layout: docu
redirect_from:
- /docs/api/cli
- /docs/api/cli/
- /docs/clients/cli
- /docs/clients/cli/
- /docs/api/cli/overview
- /docs/api/cli/overview/
- /docs/clients/cli/overview
title: CLI 客户端
---

> DuckDB CLI 客户端的最新版本是 {{ site.current_duckdb_version }}。

## 安装

DuckDB CLI（命令行界面）是一个独立的、无依赖项的可执行文件。它为 Windows、Mac 和 Linux 预编译了稳定版本和由 GitHub Actions 生成的夜间构建版本。请参阅 [安装页面]({% link docs/installation/index.html %}) 中的 CLI 标签以获取下载链接。

DuckDB CLI 基于 SQLite 命令行 shell，因此 CLI 客户端特有的功能与 [SQLite 文档](https://www.sqlite.org/cli.html) 中描述的类似（尽管 DuckDB 的 SQL 语法遵循 PostgreSQL 的约定，有一些 [例外情况]({% link docs/stable/sql/dialect/postgresql_compatibility.md %})）。

> DuckDB 有一个 [tldr 页面](https://tldr.inbrowser.app/pages/common/duckdb)，总结了 CLI 客户端最常见的用法。
> 如果你安装了 [tldr](https://github.com/tldr-pages/tldr)，可以通过运行 `tldr duckdb` 来显示它。

## 快速入门

一旦下载了 CLI 可执行文件，解压缩并保存到任意目录。
在终端中导航到该目录并输入命令 `duckdb` 来运行可执行文件。
如果在 PowerShell 或 POSIX shell 环境中，请使用命令 `./duckdb`。

## 使用方法

`duckdb` 命令的典型用法如下：

```bash
duckdb [OPTIONS] [FILENAME]
```

### 选项

`[OPTIONS]` 部分编码了 [CLI 客户端的参数]({% link docs/stable/clients/cli/arguments.md %})。常用选项包括：

* `-csv`: 设置输出模式为 CSV
* `-json`: 设置输出模式为 JSON
* `-readonly`: 以只读模式打开数据库（参见 [DuckDB 的并发性]({% link docs/stable/connect/concurrency.md %}#handling-concurrency)）

如需完整的选项列表，请参阅 [命令行参数页面]({% link docs/stable/clients/cli/arguments.md %}).

### 内存数据库与持久化数据库

当未提供 `[FILENAME]` 参数时，DuckDB CLI 将打开一个临时的 [内存数据库]({% link docs/stable/connect/overview.md %}#in-memory-database)。
你将看到 DuckDB 的版本号、连接信息以及以 `D` 开头的提示符。

```bash
duckdb
```

```text
DuckDB v{{ site.current_duckdb_version }} ({{ site.current_duckdb_codename }}) {{ site.current_duckdb_hash }}
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
D
```

要打开或创建一个 [持久化数据库]({% link docs/stable/connect/overview.md %}#persistent-database)，只需在命令行中提供路径作为参数：

```bash
duckdb my_database.duckdb
```

### 在 CLI 中运行 SQL 语句

一旦打开 CLI，输入一个 SQL 语句后跟分号，然后按 Enter 执行。结果将在终端中以表格形式显示。如果省略分号，按 Enter 将允许输入多行 SQL 语句。

```sql
SELECT 'quack' AS my_column;
```

| my_column |
|-----------|
| quack     |

CLI 支持 DuckDB 的所有丰富 [SQL 语法]({% link docs/stable/sql/introduction.md %})，包括 `SELECT`、`CREATE` 和 `ALTER` 语句。

### 编辑功能

CLI 支持 [自动补全]({% link docs/stable/clients/cli/autocomplete.md %})，并在某些平台上具有高级的 [编辑功能]({% link docs/stable/clients/cli/editing.md %}) 和 [语法高亮]({% link docs/stable/clients/cli/syntax_highlighting.md %}).

### 退出 CLI

要退出 CLI，请按 `Ctrl`+`D`（如果平台支持）。否则，按 `Ctrl`+`C` 或使用 `.exit` 命令。如果你使用了持久化数据库，DuckDB 会自动检查点（将最新更改保存到磁盘）并关闭。这将删除 `.wal` 文件（[写前日志](https://en.wikipedia.org/wiki/Write-ahead_logging)）并将所有数据合并到单个文件数据库中。

### 点命令

除了 SQL 语法，CLI 还支持特殊 [点命令]({% link docs/stable/clients/cli/dot_commands.md %})。要使用这些命令，请在行首输入一个点 (`.`)，紧接着是你要执行的命令名称。命令的额外参数以空格分隔输入。如果参数包含空格，可以使用单引号或双引号包裹。点命令必须在单行中输入，且在点之前不能有空格。行末不需要分号。

常用配置可以存储在文件 `~/.duckdbrc` 中，该文件在启动 CLI 客户端时会加载。有关这些选项的更多信息，请参阅下面的 [配置 CLI](#configuring-the-cli) 部分。

> 提示 为了防止 DuckDB CLI 客户端读取 `~/.duckdbrc` 文件，请按照以下方式启动：
> ```bash
> duckdb -init /dev/null
> ```

下面我们将总结几个重要的点命令。要查看所有可用命令，请参阅 [点命令页面]({% link docs/stable/clients/cli/dot_commands.md %}) 或使用 `.help` 命令。

#### 打开数据库文件

除了在打开 CLI 时连接数据库，还可以使用 `.open` 命令建立新的数据库连接。如果没有提供额外参数，则创建一个新的内存数据库连接。该数据库在关闭 CLI 连接时不会被持久化。

```text
.open
```

`.open` 命令可选地接受多个选项，但最后一个参数可以用来指示持久化数据库的路径（或应创建的路径）。也可以使用特殊字符串 `:memory:` 来打开临时的内存数据库。

```text
.open persistent.duckdb
```

> 警告 `.open` 会关闭当前数据库。
> 要保留当前数据库同时添加新数据库，使用 [`ATTACH` 语句]({% link docs/stable/sql/statements/attach.md %}).

`.open` 接受的一个重要选项是 `--readonly` 标志。这会禁止对数据库进行任何编辑。要以只读模式打开数据库，数据库必须已经存在。这也意味着无法以只读模式打开新的内存数据库，因为内存数据库是在连接时创建的。

```text
.open --readonly preexisting.duckdb
```

#### 输出格式

`.mode` [点命令]({% link docs/stable/clients/cli/dot_commands.md %}#mode) 可用于更改终端输出中返回表格的显示方式。
这些包括默认的 `duckbox` 模式、`csv` 和 `json` 模式用于其他工具的导入、`markdown` 和 `latex` 用于文档，以及 `insert` 模式用于生成 SQL 语句。

#### 将结果写入文件

默认情况下，DuckDB CLI 会将结果发送到终端的标准输出。但是，可以通过使用 `.output` 或 `.once` 命令来修改此行为。
详情请参阅 [输出点命令文档]({% link docs/stable/clients/cli/dot_commands.md %}#output-writing-results-to-a-file)。

#### 从文件读取 SQL

DuckDB CLI 可以从外部文件而不是终端读取 SQL 命令和点命令，使用 `.read` 命令。这允许按顺序运行多个命令，并保存和重用命令序列。

`.read` 命令只需要一个参数：包含 SQL 和/或要执行的命令的文件路径。运行完文件中的命令后，控制权将回到终端。执行该文件的输出由之前讨论的 `.output` 和 `.once` 命令控制。这允许将输出显示回终端，如下面的第一个示例，或输出到另一个文件，如下面的第二个示例。

在下面的示例中，文件 `select_example.sql` 位于与 duckdb.exe 相同的目录中，并包含以下 SQL 语句：

```sql
SELECT *
FROM generate_series(5);
```

要从 CLI 执行它，使用 `.read` 命令。

```text
.read select_example.sql
```

默认情况下，下面的输出将返回到终端。可以使用 `.output` 或 `.once` 命令调整表格的格式。

```text
| generate_series |
|----------------:|
| 0               |
| 1               |
| 2               |
| 3               |
| 4               |
| 5               |
```

多个命令（包括 SQL 和点命令）也可以在单个 `.read` 命令中运行。在下面的示例中，文件 `write_markdown_to_file.sql` 位于与 duckdb.exe 相同的目录中，并包含以下命令：

```sql
.mode markdown
.output series.md
SELECT *
FROM generate_series(5);
```

要从 CLI 执行它，使用 `.read` 命令如前所述。

```text
.read write_markdown_to_file.sql
```

在这种情况下，不会有任何输出返回到终端。相反，文件 `series.md` 将被创建（如果已存在则替换）并包含此处显示的格式化结果：

```text
| generate_series |
|----------------:|
| 0               |
| 1               |
| 2               |
| 3               |
| 4               |
| 5               |
```

<!-- The edit function does not appear to work -->

## 配置 CLI

可以使用多个点命令来配置 CLI。
启动时，CLI 会读取并执行文件 `~/.duckdbrc` 中的所有命令，包括点命令和 SQL 语句。
这允许你存储 CLI 的配置状态。
你也可以通过 `-init` 指向不同的初始化文件。

### 设置自定义提示符

例如，与 DuckDB CLI 在同一目录的文件 `prompt.sql` 会将 DuckDB 提示符更改为鸭子头并运行一个 SQL 语句。
请注意，鸭子头使用 Unicode 字符构建，并且在某些终端环境中可能无法正常工作（例如，在 Windows 中，除非使用 WSL 和 Windows Terminal）。

```text
.prompt '⚫◗ '
```

要在初始化时调用该文件，请使用以下命令：

```bash
duckdb -init prompt.sql
```

这将输出：

```text
-- Loading resources from prompt.sql
v⟨version⟩ ⟨git_hash⟩
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
⚫◗
```

## 非交互式使用

要读取/处理文件并立即退出，请将文件内容重定向到 `duckdb`：

```bash
duckdb < select_example.sql
```

要执行带有直接从命令行传递的 SQL 文本的命令，请使用两个参数调用 `duckdb`：数据库位置（或 `:memory:`），以及一个包含要执行的 SQL 语句的字符串。

```bash
duckdb :memory: "SELECT 42 AS the_answer"
```

## 加载扩展

要加载扩展，请使用 DuckDB 的 SQL `INSTALL` 和 `LOAD` 命令，如同使用其他 SQL 语句一样。

```sql
INSTALL fts;
LOAD fts;
```

详情请参阅 [扩展文档]({% link docs/stable/core_extensions/overview.md %}).

## 从 stdin 读取并写入 stdout

在 Unix 环境中，将数据在多个命令之间传递可能很有用。
DuckDB 可以通过 SQL 命令中的 stdin 路径 `/dev/stdin` 和 stdout 路径 `/dev/stdout` 读取数据并写入 stdout，因为管道作用非常类似于文件句柄。

此命令将创建一个示例 CSV：

```sql
COPY (SELECT 42 AS woot UNION ALL SELECT 43 AS woot) TO 'test.csv' (HEADER);
```

首先，读取一个文件并将其通过管道传递给 `duckdb` CLI 可执行文件。作为 DuckDB CLI 的参数，传入要打开的数据库位置，此处为内存数据库，并传入一个使用 `/dev/stdin` 作为文件位置的 SQL 命令。

```bash
cat test.csv | duckdb -c "SELECT * FROM read_csv('/dev/stdin')"
```

| woot |
|-----:|
| 42   |
| 43   |

要写回 stdout，可以使用 `copy` 命令并使用 `/dev/stdout` 文件位置。

```bash
cat test.csv | \
    duckdb -c "COPY (SELECT * FROM read_csv('/dev/stdin')) TO '/dev/stdout' WITH (FORMAT csv, HEADER)"
```

```csv
woot
42
43
```

## 读取环境变量

`getenv` 函数可以读取环境变量。

### 示例

要从 `HOME` 环境变量中获取家目录路径，使用：

```sql
SELECT getenv('HOME') AS home;
```

|       home       |
|------------------|
| /Users/user_name |

`getenv` 函数的输出可以用于设置 [配置选项]({% link docs/stable/configuration/overview.md %})。例如，要根据环境变量 `DEFAULT_NULL_ORDER` 设置 `NULL` 顺序，使用：

```sql
SET default_null_order = getenv('DEFAULT_NULL_ORDER');
```

### 读取环境变量的限制

`getenv` 函数只能在 [`enable_external_access`]({% link docs/stable/configuration/overview.md %}#configuration-reference) 选项设置为 `true`（默认设置）时运行。
它仅在 CLI 客户端中可用，不支持其他 DuckDB 客户端。

## 预编译语句

DuckDB CLI 除了支持常规的 `SELECT` 语句外，还支持执行 [预编译语句]({% link docs/stable/sql/query_syntax/prepared_statements.md %}).
要在 CLI 客户端中创建和执行预编译语句，请使用 `PREPARE` 子句和 `EXECUTE` 语句。