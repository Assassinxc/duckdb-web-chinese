---
---
layout: docu
redirect_from:
- /dev/sqllogictest/intro
- /dev/sqllogictest/intro/
- /docs/dev/sqllogictest/intro
title: sqllogictest 介绍
---

为了测试纯 SQL，我们使用了一个扩展版本的 SQL 逻辑测试套件，该套件源自 [SQLite](https://www.sqlite.org/sqllogictest/doc/trunk/about.wiki)。每个测试都作为一个单独的自包含文件，位于 `test/sql` 目录中。
要运行位于默认 `test` 目录之外的测试，请指定 `--test-dir <root_directory>`，并确保提供的测试文件路径相对于该根目录。

测试描述了一系列 SQL 语句，同时伴随着预期结果、`statement ok` 指示符或 `statement error` 指示符。一个测试文件的示例如下所示：

```sql
# name: test/sql/projection/test_simple_projection.test
# group [projection]

# 启用查询验证
statement ok
PRAGMA enable_verification

# 创建表
statement ok
CREATE TABLE a (i INTEGER, j INTEGER);

# 插入：影响一行
statement ok
INSERT INTO a VALUES (42, 8.
```

在这个示例中，执行了三个语句。前两个语句预计会成功（以 `statement ok` 开头）。第三个语句预计会返回一个包含两列的单行（由 `query II` 表示）。该行的值预计为 `42` 和 `84`（用制表符分隔）。有关查询结果验证的更多信息，请参见 [结果验证部分]({% link docs/stable/dev/sqllogictest/result_verification.md %}).

每个文件的顶部应包含一个注释，描述测试的名称和组。测试的名称始终是文件的相对文件路径。组是文件所在的文件夹。测试的名称和组是有意义的，因为它们可以用于在 unittest 组中仅执行该测试。例如，如果我们想要仅执行上面的测试，我们将运行命令 `unittest test/sql/projection/test_simple_projection.test`。如果我们想要运行特定目录中的所有测试，我们将运行命令 `unittest "[projection]"`.

任何放置在 `test` 目录中的测试都会自动添加到测试套件中。请注意，测试的扩展名很重要。sqllogictests 应该使用 `.test` 扩展名，或者 `.test_slow` 扩展名。`.test_slow` 扩展名表示该测试运行时间较长，只有在使用 `unittest *` 显式运行所有测试时才会执行。使用 `.test` 扩展名的测试将包含在快速测试集合中。

## 查询验证

许多简单的测试首先启用查询验证。这可以通过以下 `PRAGMA` 语句完成：

```sql
statement ok
PRAGMA enable_verification
```

查询验证执行额外的验证以确保底层代码运行正确。其中最重要的一部分是验证优化器不会在查询中导致错误。它通过运行未优化和优化后的查询版本，并验证这两个查询的结果是否相同来实现这一点。

查询验证非常有用，因为它不仅能够发现优化器中的错误，还能发现例如连接实现中的错误。这是因为未优化版本通常会使用交叉乘积。因此，当处理较大的数据集时，查询验证可能会非常慢。因此，建议对所有单元测试启用查询验证，但排除涉及较大数据集的测试（超过 ~10-100 行）。

## 编辑器 & 语法高亮

sqllogictests 并不完全是行业标准，但其他系统也采用了它们。解析 sqllogictests 是有意为之的简单。所有语句必须由空行分隔。因此，编写一个语法高亮器并不困难。

[Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=benesch.sqllogictest) 有一个语法高亮器。我们还 [创建了一个支持 sqllogictests 的 DuckDB 方言的 fork](https://github.com/Mytherin/vscode-sqllogictest)。您可以通过安装原始版本，然后将 `syntaxes/sqllogictest.tmLanguage.json` 复制到已安装的扩展中（在 macOS 上，该路径位于 `~/.vscode/extensions/benesch.sqllogictest-0.1.1`）。

[CLion](https://plugins.jetbrains.com/plugin/15295-sqltest) 也有一个语法高亮器。可以通过在市场中搜索 SQLTest 直接安装到 IDE。还有一个 [GitHub 仓库](https://github.com/pdet/SQLTest)，欢迎提交扩展和错误报告。

### 临时文件

对于一些测试（例如，CSV/Parquet 文件格式测试），需要创建临时文件。任何临时文件都应在临时测试目录中创建。这个目录可以通过在查询中放置字符串 `__TEST_DIR__` 来使用。此字符串将被替换为临时测试目录的路径。

```sql
statement ok
COPY csv_data TO '__TEST_DIR__/output_file.csv.gz' (COMPRESSION gzip);
```

### 需求 & 扩展

为了避免使核心系统臃肿，DuckDB 的某些功能仅作为扩展提供。通过在测试中添加 `require` 字段，可以为这些扩展构建测试。如果未加载扩展，任何出现在 `require` 字段之后的语句都会被跳过。例如，`require parquet` 或 `require icu`。

另一种用途是限制测试仅针对特定的向量大小。例如，向测试中添加 `require vector_size 512` 将防止测试运行，除非向量大小大于或等于 512。这很有用，因为某些功能在低向量大小时不支持，但我们在 CI 中使用向量大小为 2 来运行测试。