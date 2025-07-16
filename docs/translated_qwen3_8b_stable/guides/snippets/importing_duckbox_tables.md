---
---
layout: docu
redirect_from:
- /docs/guides/file_formats/duckbox
- /docs/guides/snippets/importing_duckbox_tables
title: 导入 Duckbox 表
---

> 本页提供的脚本适用于 Linux、macOS 和 WSL。

默认情况下，DuckDB 的 [CLI 客户端]({% link docs/stable/clients/cli/overview.md %}) 会使用 [duckbox 格式]({% link docs/stable/clients/cli/output_formats.md %}) 渲染查询结果，该格式使用丰富的 ASCII 艺术风格表格来展示数据。
这些表格经常直接用于其他文档中。
例如，以下是用于演示 [DuckDB v1.2.0 发布博客文章中的新 CSV 功能]({% post_url 2025-02-05-announcing-duckdb-120 %}#csv-features.md) 的表格：

```text
┌─────────┬───────┐
│    a    │   b   │
│ varchar │ int64 │
├─────────┼───────┤
│ hello   │    42 │
│ world   │    84 │
└─────────┴───────┘
```

如果我们想要将这些数据重新导入 DuckDB 中呢？
默认情况下不支持此操作，但可以通过一些脚本实现：
我们可以将表格转换为以 `│` 分隔的文件，并使用 DuckDB 的 [CSV 读取器]({% link docs/stable/data/csv/overview.md %}) 读取。
请注意，分隔符不是 `|` 字符，而是 [“轻量垂直线框”字符](https://www.compart.com/en/unicode/U+2502) `│`。

## 将 Duckbox 表导入 DuckDB

首先，我们将上面的表格保存为 `duckbox.csv`。
然后，使用 `sed` 清理该文件：

```batch
echo -n > duckbox-cleaned.csv
sed -n "2s/^│ *//;s/ *│$//;s/ *│ */│/p;2q" duckbox.csv >> duckbox-cleaned.csv
sed "1,4d;\$d;s/^│ *//;s/ *│$//;s/ *│ */│/g" duckbox.csv >> duckbox-cleaned.csv
```

清理后的 `duckbox-cleaned.csv` 文件内容如下：

```text
a│b
hello│42
world│84
```

然后，我们可以通过以下方式将数据导入 DuckDB：

```sql
FROM read_csv('duckbox-cleaned.csv', delim = '│');
```

并导出为 CSV：

```sql
COPY (FROM read_csv('duckbox-cleaned.csv', delim = '│')) TO 'out.csv';
```

```text
a,b
hello,42
world,84
```

## 使用 `shellfs`

为了通过单次 `read_csv` 调用解析 duckbox 表（且不创建任何临时文件），我们可以使用 [`shellfs` 社区扩展]({% link community_extensions/extensions/shellfs.md %})：

```sql
INSTALL shellfs FROM community;
LOAD shellfs;
FROM read_csv(
        '(sed -n "2s/^│ *//;s/ *│$//;s/ *│ */│/p;2q" duckbox.csv; ' ||
        'sed "1,4d;\$d;s/^│ *//;s/ *│$//;s/ *│ */│/g" duckbox.csv) |',
        delim = '│'
    );
```

我们还可以创建一个 [表宏]({% link docs/stable/sql/statements/create_macro.md %}#table-macros)：

```sql
CREATE MACRO read_duckbox(path) AS TABLE
    FROM read_csv(
            printf(
                '(sed -n "2s/^│ *//;s/ *│$//;s/ *│ */│/p;2q" %s; ' ||
                'sed "1,4d;\$d;s/^│ *//;s/ *│$//;s/ *│ */│/g" %s) |',
                path, path
            ),
            delim = '│'
        );
```

然后，读取 duckbox 表变得非常简单：

```sql
FROM read_duckbox('duckbox.csv');
```

> `shellfs` 是一个社区扩展，不提供任何支持或保证。
> 仅在确保其输入已适当清理的情况下使用。
> 请参阅 [DuckDB 安全性页面]({% link docs/stable/operations_manual/securing_duckdb/overview.md %}) 获取更多详情。

## 局限性

在运行此脚本时，请注意以下限制：

* 该方法仅在表格中不包含长管道 `│` 字符时有效。
  它还会从表格单元格值中去除空格。
  在运行脚本时，请确保考虑到这些假设。

* 该脚本兼容 BSD `sed`（在 macOS 上默认使用）和 GNU `sed`（在 Linux 上默认使用，也可在 macOS 上通过 `gsed` 使用）。

* 仅能正确解析 [CSV 识别器支持的数据类型]({% link docs/stable/data/csv/auto_detection.md %}#type-detection)。包含嵌套数据的值将被解析为 `VARCHAR`。