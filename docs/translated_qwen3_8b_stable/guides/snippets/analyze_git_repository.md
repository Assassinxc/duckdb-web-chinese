---
---
layout: docu
redirect_from:
- /docs/guides/snippets/analyze_git_repository
title: 分析 Git 仓库
---

您可以使用 DuckDB 通过 [`git log` 命令](https://git-scm.com/docs/git-log) 的输出来分析 Git 日志。

## 导出 Git 日志

我们首先选择一个在任何提交日志（作者名称、消息等）中都不会出现的字符。
自从 v1.2.0 版本起，DuckDB 的 CSV 读取器支持 [4 字节分隔符]({% post_url 2025-02-05-announcing-duckdb-120 %}#csv-features)，这使得使用表情符号成为可能！🎉

尽管它在 [表情电影](https://www.imdb.com/title/tt4877122/)（IMDb 评分：3.4）中被提及，
我们可以假设 [漩涡鱼蛋糕表情符号（🍥）](https://emojipedia.org/fish-cake-with-swirl) 在大多数 Git 日志中并不常见。
因此，让我们克隆 [`duckdb/duckdb` 仓库](https://github.com/duckdb/duckdb)，并按照以下方式导出其日志：

```bash
git log --date=iso-strict --pretty=format:%ad🍥%h🍥%an🍥%s > git-log.csv
```

生成的文件如下所示：

```text
2025-02-25T18:12:54+01:00🍥d608a31e13🍥Mark🍥MAIN_BRANCH_VERSIONING: Adopt also for Python build and amalgamation (#16400)
2025-02-25T15:05:56+01:00🍥920b39ad96🍥Mark🍥Read support for Parquet Float16 (#16395)
2025-02-25T13:43:52+01:00🍥61f55734b9🍥Carlo Piovesan🍥MAIN_BRANCH_VERSIONING: Adopt also for Python build and amalgamation
2025-02-25T12:35:28+01:00🍥87eff7ebd3🍥Mark🍥Fix issue #16377 (#16391)
2025-02-25T10:33:49+01:00🍥35af26476e🍥Hannes Mühleisen🍥Read support for Parquet Float16
```

## 将 Git 日志加载到 DuckDB

启动 DuckDB 并将日志作为 <s>CSV</s> 🍥SV 读取：

```sql
CREATE TABLE commits AS 
    FROM read_csv(
            'git-log.csv',
            delim = '🍥',
            header = false,
            column_names = ['timestamp', 'hash', 'author', 'message']
        );
```

这将得到一个漂亮的 DuckDB 表：

```sql
FROM commits
LIMIT 5;
```

```text
┌─────────────────────┬────────────┬──────────────────┬───────────────────────────────────────────────────────────────────────────────┐
│      timestamp      │    hash    │      author      │                                    message                                    │
│      timestamp      │  varchar   │     varchar      │                                    varchar                                    │
├─────────────────────┼────────────┼──────────────────┼───────────────────────────────────────────────────────────────────────────────┤
│ 2025-02-25 17:12:54 │ d608a31e13 │ Mark             │ MAIN_BRANCH_VERSIONING: Adopt also for Python build and amalgamation (#16400) │
│ 2025-02-25 14:05:56 │ 920b39ad96 │ Mark             │ Read support for Parquet Float16 (#16395)                                     │
│ 2025-02-25 12:43:52 │ 61f55734b9 │ Carlo Piovesan   │ MAIN_BRANCH_VERSIONING: Adopt also for Python build and amalgamation          │
│ 2025-02-25 11:35:28 │ 87eff7ebd3 │ Mark             │ Fix issue #16377 (#16391)                                                     │
│ 2025-02-25 09:33:49 │ 35af26476e │ Hannes Mühleisen │ Read support for Parquet Float16                                              │
└─────────────────────┴────────────┴──────────────────┴───────────────────────────────────────────────────────────────────────────────┘
```

## 分析日志

我们可以像分析其他表一样分析此表。

### 常见主题

让我们从一个简单的问题开始：在提交消息中，哪个主题被提及最多：CI、CLI 或 Python？

```sql
SELECT
    message.lower().regexp_extract('\b(ci|cli|python)\b') AS topic,
    count(*) AS num_commits
FROM commits
WHERE topic <> ''
GROUP BY ALL
ORDER BY num_commits DESC;
```

```text
┌─────────┬─────────────┐
│  topic  │ num_commits │
│ varchar │    int64    │
├─────────┼─────────────┤
│ ci      │         828 │
│ python  │         666 │
│ cli     │          49 │
└─────────┴─────────────┘
```

在这三个主题中，与持续集成相关的提交在日志中占主导地位！

我们还可以通过查看提交消息中的所有单词进行更深入的分析。
为此，我们首先对消息进行分词：

```sql
CREATE TABLE words AS
    SELECT unnest(
        message
            .lower()
            .regexp_replace('\W', ' ')
            .trim(' ')
            .string_split_regex('\W')
        ) AS word    
FROM commits;
```

然后，我们使用预定义的列表删除停用词：

```sql
CREATE TABLE stopwords AS
    SELECT unnest(['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'can', 'did', 'do', 'does', 'doing', 'don', 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'has', 'have', 'having', 'he', 'her', 'here', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'itself', 'just', 'me', 'more', 'most', 'my', 'myself', 'no', 'nor', 'not', 'now', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 's', 'same', 'she', 'should', 'so', 'some', 'such', 't', 'than', 'that', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'these', 'they', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'you', 'your', 'yours', 'yourself', 'yourselves']) AS word;

CREATE OR REPLACE TABLE words AS
    FROM words
    NATURAL ANTI JOIN stopwords
    WHERE word != '';
```

> 我们在这里使用了 `NATURAL ANTI JOIN` 子句，这使得我们能够优雅地过滤掉在 `stopwords` 表中出现的值。

最后，我们选择前 20 个最常见的单词。

```sql
SELECT word, count(*) AS count FROM words
GROUP BY ALL
ORDER BY count DESC
LIMIT 20;
```

```text
┌──────────┬───────┐
│    w     │ count │
│ varchar  │ int64 │
├──────────┼───────┤
│ merge    │ 12550 │
│ fix      │  6402 │
│ branch   │  6005 │
│ pull     │  5950 │
│ request  │  5945 │
│ add      │  5687 │
│ test     │  3801 │
│ master   │  3289 │
│ tests    │  2339 │
│ issue    │  1971 │
│ main     │  1935 │
│ remove   │  1884 │
│ format   │  1819 │
│ duckdb   │  1710 │
│ use      │  1442 │
│ mytherin │  1410 │
│ fixes    │  1333 │
│ hawkfish │  1147 │
│ feature  │  1139 │
│ function │  1088 │
├──────────┴───────┤
│     20 rows      │
└──────────────────┘
```

正如预期的那样，有很多 Git 术语（`merge`, `branch`, `pull` 等），接着是与开发相关的术语（`fix`, `test`/`tests`, `issue`, `format`）。
我们还看到一些开发者的账户名（[`mytherin`](https://github.com/Mytherin), [`hawkfish`](https://github.com/hawkfish)），这很可能是由于合并 pull 请求的提交信息（例如，[”Merge pull request #13776 from Mytherin/expressiondepth”](https://github.com/duckdb/duckdb/commit/4d18b9d05caf88f0420dbdbe03d35a0faabf4aa7)）。
最后，我们还看到一些与 DuckDB 相关的术语，如 `duckdb`（震惊！）和 `function`。

### 可视化提交数量

让我们可视化每年的提交数量：

```sql
SELECT
    year(timestamp) AS year,
    count(*) AS num_commits,
    num_commits.bar(0, 20_000) AS num_commits_viz
FROM commits
GROUP BY ALL
ORDER BY ALL;
```

```text
┌───────┬─────────────┬──────────────────────────────────────────────────────────────────────────────────┐
│ year  │ num_commits │                                 num_commits_viz                                  │
│ int64 │    int64    │                                     varchar                                      │
├───────┼─────────────┼──────────────────────────────────────────────────────────────────────────────────┤
│  2018 │         870 │ ███▍                                                                             │
│  2019 │        1621 │ ██████▍                                                                          │
│  2020 │        3484 │ █████████████▉                                                                   │
│  2021 │        6488 │ █████████████████████████▉                                                       │
│  2022 │        9817 │ ███████████████████████████████████████▎                                         │
│  2023 │       14585 │ ██████████████████████████████████████████████████████████▎                      │
│  2024 │       15949 │ ███████████████████████████████████████████████████████████████▊                 │
│  2025 │        1788 │ ███████▏                                                                         │
└───────┴─────────────┴──────────────────────────────────────────────────────────────────────────────────┘
```

我们看到提交数量逐年稳步增长——
特别是考虑到 DuckDB 的许多功能和客户端，最初是主仓库的一部分，现在由单独的仓库维护
（例如，[Java](https://github.com/duckdb/duckdb-java), [R](https://github.com/duckdb/duckdb-r)）。

快乐黑客！