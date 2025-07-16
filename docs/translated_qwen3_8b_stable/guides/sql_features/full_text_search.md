---
---
layout: docu
redirect_from:
- /docs/guides/sql_features/full_text_search
title: 全文搜索
---

DuckDB 通过 [`fts` 扩展]({% link docs/stable/core_extensions/full_text_search.md %}) 支持全文搜索。
全文索引允许查询在较长文本字符串中快速查找所有单个单词的出现情况。

## 示例：莎士比亚语料库

以下是一个构建莎士比亚戏剧全文索引的示例。

```sql
CREATE TABLE corpus AS
    SELECT * FROM 'https://blobs.duckdb.org/data/shakespeare.parquet';
```

```sql
DESCRIBE corpus;
```

<div class="monospace_table"></div>

| column_name | column_type | null | key  | default | extra |
|-------------|-------------|------|------|---------|-------|
| line_id     | VARCHAR     | YES  | NULL | NULL    | NULL  |
| play_name   | VARCHAR     | YES  | NULL | NULL    | NULL  |
| line_number | VARCHAR     | YES  | NULL | NULL    | NULL  |
| speaker     | VARCHAR     | YES  | NULL | NULL    | NULL  |
| text_entry  | VARCHAR     | YES  | NULL | NULL    | NULL  |

每行的文本内容存储在 `text_entry` 中，每行的唯一键存储在 `line_id` 中。

## 创建全文搜索索引

首先，我们创建索引，指定表名、唯一标识列以及要索引的列。我们将只对单个列 `text_entry` 进行索引，该列包含戏剧中各行的文本内容。

```sql
PRAGMA create_fts_index('corpus', 'line_id', 'text_entry');
```

现在可以使用 [Okapi BM25](https://en.wikipedia.org/wiki/Okapi_BM25) 排名函数对表进行查询。没有匹配的行返回 `NULL` 分数。

莎士比亚对黄油有什么说法？

```sql
SELECT
    fts_main_corpus.match_bm25(line_id, 'butter') AS score,
    line_id, play_name, speaker, text_entry
FROM corpus
WHERE score IS NOT NULL
ORDER BY score DESC;
```

|       score        |   line_id   |        play_name         |   speaker    |                     text_entry                     |
|-------------------:|-------------|--------------------------|--------------|----------------------------------------------------|
| 4.427313429798464  | H4/2.4.494  | Henry IV                 | Carrier      | As fat as butter.                                  |
| 3.836270302568675  | H4/1.2.21   | Henry IV                 | FALSTAFF     | prologue to an egg and butter.                     |
| 3.836270302568675  | H4/2.1.55   | Henry IV                 | Chamberlain  | They are up already, and call for eggs and butter; |
| 3.3844488405497115 | H4/4.2.21   | Henry IV                 | FALSTAFF     | toasts-and-butter, with hearts in their bellies no |
| 3.3844488405497115 | H4/4.2.62   | Henry IV                 | PRINCE HENRY | already made thee butter. But tell me, Jack, whose |
| 3.3844488405497115 | AWW/4.1.40  | Alls well that ends well | PAROLLES     | butter-womans mouth and buy myself another of      |
| 3.3844488405497115 | AYLI/3.2.93 | As you like it           | TOUCHSTONE   | right butter-womens rank to market.                |
| 3.3844488405497115 | KL/2.4.132  | King Lear                | Fool         | kindness to his horse, buttered his hay.           |
| 3.0278411214953107 | AWW/5.2.9   | Alls well that ends well | Clown        | henceforth eat no fish of fortunes buttering.      |
| 3.0278411214953107 | MWW/2.2.260 | Merry Wives of Windsor   | FALSTAFF     | Hang him, mechanical salt-butter rogue! I will     |
| 3.0278411214953107 | MWW/2.2.284 | Merry Wives of Windsor   | FORD         | rather trust a Fleming with my butter, Parson Hugh |
| 3.0278411214953107 | MWW/3.5.7   | Merry Wives of Windsor   | FALSTAFF     | Ill have my brains taen out and buttered, and give |
| 3.0278411214953107 | MWW/3.5.102 | Merry Wives of Windsor   | FALSTAFF     | to heat as butter; a man of continual dissolution  |
| 2.739219044070792  | H4/2.4.115  | Henry IV                 | PRINCE HENRY | Didst thou never see Titan kiss a dish of butter?  |

与标准索引不同，全文索引在底层数据更改时不会自动更新，因此您需要执行 `PRAGMA drop_fts_index(my_fts_index)` 并在适当的时候重新创建索引。

## 关于生成语料库表的说明

如需了解更多信息，请参阅 [“从 JSON 生成用于全文搜索的莎士比亚语料库” 博客文章](https://duckdb.blogspot.com/2023/04/generating-shakespeare-corpus-for-full.html)。

* 列包括：line_id、play_name、line_number、speaker、text_entry。
* 为了使全文搜索正常工作，每行都需要一个唯一的键。
* line_id `KL/2.4.132` 表示 King Lear，第 2 幕，第 4 场，第 132 行。