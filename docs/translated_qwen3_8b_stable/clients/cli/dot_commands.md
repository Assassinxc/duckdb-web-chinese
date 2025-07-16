---
layout: docu
redirect_from:
- /docs/api/cli/dot-commands
- /docs/api/cli/dot-commands/
- /docs/api/cli/dot_commands
- /docs/api/cli/dot_commands/
- /docs/clients/cli/dot_commands
title: 点命令
---

DuckDB CLI 客户端支持点命令。要使用这些命令，请以句点（`.`）开头，紧接着是您要执行的命令名称。命令的额外参数在命令之后输入，用空格分隔。如果参数中包含空格，可以使用单引号或双引号来包裹该参数。点命令必须在单行中输入，且句点前不能有空格。行末不需要分号。要查看可用命令，请使用 `.help` 命令。

## 点命令列表

<!-- markdownlint-disable MD056 -->

| 命令                                                                 | 描述                                                                                                                                                                 |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `.bail ⟨on/off⟩`{:.language-sql .highlight}                         | 在遇到错误后停止。默认值: `off`                                                                                                                                   |
| `.binary ⟨on/off⟩`{:.language-sql .highlight}                       | 启用或禁用二进制输出。默认值: `off`                                                                                                                                |
| `.cd ⟨DIRECTORY⟩`{:.language-sql .highlight}                        | 将工作目录更改为 `DIRECTORY`                                                                                                                                      |
| `.changes ⟨on/off⟩`{:.language-sql .highlight}                      | 显示 SQL 修改的行数                                                                                                                                                |
| `.columns`{:.language-sql .highlight}                              | 以列形式显示查询结果                                                                                                                                                |
| `.constant ⟨COLOR⟩`{:.language-sql .highlight}                      | 设置用于常量值的语法高亮颜色                                                                                                                                       |
| `.constantcode ⟨CODE⟩`{:.language-sql .highlight}                   | 设置用于常量值的语法高亮终端代码                                                                                                                                   |
| `.databases`{:.language-sql .highlight}                            | 列出附加数据库的名称和文件                                                                                                                                         |
| `.echo ⟨on/off⟩`{:.language-sql .highlight}                        | 启用或禁用命令回显                                                                                                                                                 |
| `.exit ⟨CODE⟩`{:.language-sql .highlight}                          | 以返回码 `CODE` 退出程序                                                                                                                                           |
| `.headers ⟨on/off⟩`{:.language-sql .highlight}                      | 启用或禁用显示表头。不适用于 duckbox 模式                                                                                                                         |
| `.help ⟨-all⟩ ⟨PATTERN⟩`{:.language-sql .highlight}                | 显示 `PATTERN` 的帮助文本                                                                                                                                          |
| `.highlight ⟨on/off⟩`{:.language-sql .highlight}                    | 在 shell 中切换语法高亮 `on` / `off`。有关更多详细信息，请参阅 [查询语法高亮部分](#configuring-the-query-syntax-highlighter) |
| `.highlight_colors ⟨COMPONENT⟩ ⟨COLOR⟩`{:.language-sql .highlight} | 配置每个组件的颜色（仅适用于 duckbox）。有关更多详细信息，请参阅 [结果语法高亮部分](#configuring-the-query-syntax-highlighter) |
| `.highlight_results ⟨on/off⟩`{:.language-sql .highlight}           | 在结果表中切换高亮 `on` / `off`（仅适用于 duckbox）。有关更多详细信息，请参阅 [结果语法高亮部分](#configuring-the-query-syntax-highlighter) |
| `.import ⟨FILE⟩ ⟨TABLE⟩`{:.language-sql .highlight}                | 从 `FILE` 导入数据到 `TABLE`                                                                                                                                      |
| `.indexes ⟨TABLE⟩`{:.language-sql .highlight}                      | 显示索引名称                                                                                                                                                       |
| `.keyword ⟨COLOR⟩`{:.language-sql .highlight}                      | 设置用于关键字的语法高亮颜色                                                                                                                                       |
| `.keywordcode ⟨CODE⟩`{:.language-sql .highlight}                   | 设置用于关键字的语法高亮终端代码                                                                                                                                   |
| `.large_number_rendering ⟨all/footer/off⟩`{:.language-sql .highlight} | 切换大数字的可读渲染（仅适用于 duckbox，默认值: `footer`）                                                                                                         |
| `.log ⟨FILE/off⟩`{:.language-sql .highlight}                       | 启用或禁用日志。`FILE` 可以是 `stderr` / `stdout`                                                                                                                  |
| `.maxrows ⟨COUNT⟩`{:.language-sql .highlight}                      | 设置显示的最大行数。仅适用于 [duckbox 模式]({% link docs/stable/clients/cli/output_formats.md %})                                                                 |
| `.maxwidth ⟨COUNT⟩`{:.language-sql .highlight}                     | 设置最大宽度（字符数）。0 默认为终端宽度。仅适用于 [duck
| `.mode ⟨MODE⟩ ⟨TABLE⟩`{:.language-sql .highlight}                  | 设置 [输出模式]({% link docs/stable/clients/cli/output_formats.md %})                                                                                              |
| `.multiline`{:.language-sql .highlight}                           | 设置多行模式（默认）                                                                                                                                               |
| `.nullvalue ⟨STRING⟩`{:.language-sql .highlight}                   | 使用 `STRING` 替代 `NULL` 值。默认值: `NULL`                                                                                                                       |
| `.once ⟨OPTIONS⟩ ⟨FILE⟩`{:.language-sql .highlight}                | 仅输出下一个 SQL 命令到 `FILE`                                                                                                                                     |
| `.open ⟨OPTIONS⟩ ⟨FILE⟩`{:.language-sql .highlight}                | 关闭现有数据库并重新打开 `FILE`                                                                                                                                   |
| `.output ⟨FILE⟩`{:.language-sql .highlight}                        | 将输出发送到 `FILE` 或如果省略 `FILE` 则发送到 `stdout`                                                                                                            |
| `.print ⟨STRING...⟩`{:.language-sql .highlight}                    | 打印字面 `STRING`                                                                                                                                                  |
| `.prompt ⟨MAIN⟩ ⟨CONTINUE⟩`{:.language-sql .highlight}             | 替换标准提示                                                                                                                                                      |
| `.quit`{:.language-sql .highlight}                                | 退出程序                                                                                                                                                           |
| `.read ⟨FILE⟩`{:.language-sql .highlight}                         | 从 `FILE` 读取输入                                                                                                                                                 |
| `.rows`{:.language-sql .highlight}                                | 以行形式显示查询结果（默认）                                                                                                                                       |
| `.safe_mode`{:.language-sql .highlight}                           | 启用 [安全模式]({% link docs/stable/clients/cli/safe_mode.md %})                                                                                                   |
| `.schema ⟨PATTERN⟩`{:.language-sql .highlight}                     | 显示匹配 `PATTERN` 的 `CREATE` 语句                                                                                                                                |
| `.separator ⟨COL⟩ ⟨ROW⟩`{:.language-sql .highlight}                | 更改列和行分隔符                                                                                                                                                   |
| `.shell ⟨CMD⟩ ⟨ARGS...⟩`{:.language-sql .highlight}                | 在系统 shell 中运行 `CMD` 与 `ARGS...`                                                                                                                             |
| `.show`{:.language-sql .highlight}                                | 显示各种设置的当前值                                                                                                                                                |
| `.singleline`{:.language-sql .highlight}                          | 设置单行模式                                                                                                                                                       |
| `.system ⟨CMD⟩ ⟨ARGS...⟩`{:.language-sql .highlight}               | 在系统 shell 中运行 `CMD` 与 `ARGS...`                                                                                                                             |
| `.tables ⟨TABLE⟩`{:.language-sql .highlight}                       | 列出表名 [匹配 `LIKE` 模式]({% link docs/stable/sql/functions/pattern_matching.md %}) `TABLE`                                                                     |
| `.timer ⟨on/off⟩`{:.language-sql .highlight}                       | 启用或禁用 SQL 计时器。SQL 语句用 `;` 分隔但 _不_ 用换行分隔的会被一起测量                                                                                         |
| `.width ⟨NUM1⟩ ⟨NUM2⟩ ...`{:.language-sql .highlight}              | 设置列式输出的最小列宽                                                                                                                                             |

## 使用 `.help` 命令

`.help` 文本可以通过传入一个文本字符串作为第一个参数进行过滤。

```sql
.help m
```

```sql
.maxrows COUNT           设置显示的最大行数（默认值: 40）。仅适用于 duckbox 模式。
.maxwidth COUNT          设置最大宽度（字符数）。0 默认为终端宽度。仅适用于 duckbox 模式。
.mode MODE ?TABLE?       设置输出模式
```

## `.output`：将结果写入文件

默认情况下，DuckDB CLI 会将结果发送到终端的标准输出。但是，可以通过使用 `.output` 或 `.once` 命令来更改此设置。将所需的输出文件路径作为参数传递。`.once` 命令只会输出下一个结果集，然后恢复到标准输出，而 `.output` 会将所有后续输出重定向到该文件路径。请注意，每个结果都会覆盖该目标文件的整个内容。要恢复到标准输出，请使用不带文件参数的 `.output` 命令。

在此示例中，输出格式被更改为 `markdown`，目标被识别为 Markdown 文件，然后 DuckDB 会将 SQL 语句的输出写入该文件。使用不带参数的 `.output` 命令将输出恢复到标准输出。

```sql
.mode markdown
.output my_results.md
SELECT 'taking flight' AS output_column;
.output
SELECT 'back to the terminal' AS displayed_column;
```

文件 `my_results.md` 将包含以下内容：

```text
| output_column |
|---------------|
| taking flight |
```

终端将显示：

```text
|   displayed_column   |
|----------------------|
| back to the terminal |
```

一种常见的输出格式是 CSV（逗号分隔值）。DuckDB 支持 [SQL 语法以 CSV 或 Parquet 格式导出数据]({% link docs/stable/sql/statements/copy.md %}#copy-to)，但如果需要，也可以使用 CLI 特定命令来写入 CSV。

```sql
.mode csv
.once my_output_file.csv
SELECT 1 AS col_1, 2 AS col_2
UNION ALL
SELECT 10 AS col1, 20 AS col_2;
```

文件 `my_output_file.csv` 将包含以下内容：

```csv
col_1,col_2
1,2
10,20
```

通过向 `.once` 命令传递特殊选项（标志），查询结果也可以发送到临时文件并自动在用户的默认程序中打开。使用 `-e` 标志来打开文本文件（在默认文本编辑器中打开），或使用 `-x` 标志来打开 CSV 文件（在默认电子表格编辑器中打开）。这在需要更详细检查查询结果时特别有用，尤其是当结果集相对较大时。`.excel` 命令等同于 `.once -x`。

```sql
.once -e
SELECT 'quack' AS hello;
```

结果将在系统的默认文本文件编辑器中打开，例如：

<img src="/images/cli_docs_output_to_text_editor.jpg" alt="cli_docs_output_to_text_editor" title="输出到文本编辑器" style="width:293px;"/>

> 提示 macOS 用户可以使用 [`pbcopy`](https://ss64.com/mac/pbcopy.html) 将结果复制到剪贴板，通过使用 `.once` 将输出发送到 `pbcopy` 通过管道：`.once |pbcopy`
>
> 结合使用 `.headers off` 和 `.mode lines` 选项可以特别有效。

## 查询数据库模式

所有 DuckDB 客户端均支持 [使用 SQL 查询数据库模式]({% link docs/stable/sql/meta/information_schema.md %})，但 CLI 还有额外的 [点命令]({% link docs/stable/clients/cli/dot_commands.md %}) 可以帮助更好地理解数据库内容。
`.tables` 命令将返回数据库中的表列表。它有一个可选参数，可以根据 [`LIKE` 模式]({% link docs/stable/sql/functions/pattern_matching.md %}#like) 过滤结果。

```sql
CREATE TABLE swimmers AS SELECT 'duck' AS animal;
CREATE TABLE fliers AS SELECT 'duck' AS animal;
CREATE TABLE walkers AS SELECT 'duck' AS animal;
.tables
```

```text
fliers    swimmers  walkers
```

例如，要过滤只包含 `l` 的表，可以使用 `LIKE` 模式 `%l%`。

```sql
.tables %l%
```

```text
fliers   walkers
```

`.schema` 命令将显示用于定义数据库模式的所有 SQL 语句。

```text
.schema
```

```sql
CREATE TABLE fliers (animal VARCHAR);
CREATE TABLE swimmers (animal VARCHAR);
CREATE TABLE walkers (animal VARCHAR);
```

## 语法高亮器

DuckDB CLI 客户端支持 SQL 查询的语法高亮器和 duckbox 格式化结果表的语法高亮器。

## 配置查询语法高亮器

默认情况下，shell 包含语法高亮支持。
可以通过以下命令配置 CLI 的语法高亮器。

要关闭高亮器：

```text
.highlight off
```

要打开高亮器：

```text
.highlight on
```

要配置用于高亮常量的颜色：

```text
.constant [red|green|yellow|blue|magenta|cyan|white|brightblack|brightred|brightgreen|brightyellow|brightblue|brightmagenta|brightcyan|brightwhite]
```

```text
.constantcode ⟨terminal_code⟩
```

例如：

```text
.constantcode 033[31m
```

要配置用于高亮关键字的颜色：

```text
.keyword [red|green|yellow|blue|magenta|cyan|white|brightblack|brightred|brightgreen|brightyellow|brightblue|brightmagenta|brightcyan|brightwhite]
```

```text
.keywordcode ⟨terminal_code⟩
```

例如：

```text
.keywordcode 033[31m
```

## 配置结果语法高亮器

默认情况下，结果高亮器会进行一些小的修改：

- 列名加粗
- `NULL` 值变为灰色
- 布局元素变为灰色

可以使用 `.highlight_colors` 命令自定义每个组件的高亮效果。
例如：

```sql
.highlight_colors layout red
.highlight_colors column_type yellow
.highlight_colors column_name yellow bold_underline
.highlight_colors numeric_value cyan underline
.highlight_colors temporal_value red bold
.highlight_colors string_value green bold
.highlight_colors footer gray
```

使用 `.highlight_results off` 可以禁用结果高亮。

## 快捷方式

DuckDB 的 CLI 允许使用点命令的快捷方式。
一旦一组字符可以无歧义地完成点命令或参数，CLI（静默地）会自动补全它们。
例如：

```text
.mo ma
```

等同于：

```text
.mode markdown
```

> 提示 在 SQL 脚本中避免使用快捷方式，以提高可读性并确保脚本和未来兼容性。

## 从 CSV 导入数据

> 已弃用 该功能仅出于兼容性原因包含，未来可能会被删除。
> 使用 [`read_csv` 函数或 `COPY` 语句]({% link docs/stable/data/csv/overview.md %}) 加载 CSV 文件。

DuckDB 支持 [SQL 语法直接查询或导入 CSV 文件]({% link docs/stable/data/csv/overview.md %})，但如果需要，也可以使用 CLI 特定命令导入 CSV。`.import` 命令有两个参数，还支持多个选项。第一个参数是 CSV 文件的路径，第二个是创建的 DuckDB 表的名称。由于 DuckDB 的类型要求比 SQLite（DuckDB CLI 是基于 SQLite 的）更严格，因此在使用 `.import` 命令之前必须先创建目标表。要自动检测模式并从 CSV 创建表，请参阅 [`read_csv` 示例在导入文档中]({% link docs/stable/data/csv/overview.md %}).

在此示例中，通过切换到 CSV 模式并设置输出文件路径生成 CSV 文件：

```sql
.mode csv
.output import_example.csv
SELECT 1 AS col_1, 2 AS col_2 UNION ALL SELECT 10 AS col1, 20 AS col_2;
```

现在 CSV 已写入，可以创建具有所需模式的表并导入 CSV。将输出重置为终端以避免继续编辑上面指定的输出文件。使用 `--skip N` 选项忽略第一行数据，因为它是表头行，且表已经创建并具有正确的列名。

```text
.mode csv
.output
CREATE TABLE test_table (col_1 INTEGER, col_2 INTEGER);
.import import_example.csv test_table --skip 1
```

注意 `.import` 命令使用当前的 `.mode` 和 `.separator` 设置来识别要导入的数据结构。`--csv` 选项可以用来覆盖此行为。

```text
.import import_example.csv test_table --skip 1 --csv
```