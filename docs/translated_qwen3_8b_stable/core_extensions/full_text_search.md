---
---
github_repository: https://github.com/duckdb/duckdb-fts
layout: docu
title: 全文搜索扩展
redirect_from:
- /docs/stable/extensions/full_text_search
- /docs/stable/extensions/full_text_search/
- /docs/extensions/full_text_search
- /docs/extensions/full_text_search/
---

全文搜索是 DuckDB 的一个扩展，允许对字符串进行搜索，类似于 [SQLite 的 FTS5 扩展](https://www.sqlite.org/fts5.html)。

## 安装和加载

`fts` 扩展将在首次使用时从官方扩展仓库中透明地[自动加载]({% link docs/stable/core_extensions/overview.md %}#autoloading-extensions)。
如果您希望手动安装并加载它，请运行：

```sql
INSTALL fts;
LOAD fts;
```

## 使用

该扩展为 DuckDB 添加了两个 `PRAGMA` 语句：一个用于创建索引，一个用于删除索引。此外，还添加了一个标量宏 `stem`，该宏由扩展内部使用。

### `PRAGMA create_fts_index`

```python
create_fts_index(input_table, input_id, *input_values, stemmer = 'porter',
                 stopwords = 'english', ignore = '(\\.|[^a-z])+',
                 strip_accents = 1, lower = 1, overwrite = 0)
```

用于为指定表创建 FTS 索引的 `PRAGMA`。

<!-- markdownlint-disable MD056 -->

| 名称 | 类型 | 描述 |
|:--|:--|:----------|
| `input_table` | `VARCHAR` | 指定表的限定名称，例如 `'table_name'` 或 `'main.table_name'` |
| `input_id` | `VARCHAR` | 文档标识符的列名，例如 `'document_identifier'` |
| `input_values...` | `VARCHAR` | 要索引的文本字段的列名（可变参数），例如 `'text_field_1'`, `'text_field_2'`, ..., `'text_field_N'`，或 `'\*'` 表示 `input_table` 中所有类型为 `VARCHAR` 的列 |
| `stemmer` | `VARCHAR` | 要使用的词干提取器类型。可选值包括 `'arabic'`, `'basque'`, `'catalan'`, `'danish'`, `'dutch'`, `'english'`, `'finnish'`, `'french'`, `'german'`, `'greek'`, `'hindi'`, `'hungarian'`, `'indonesian'`, `'irish'`, `'italian'`, `'lithuanian'`, `'nepali'`, `'norwegian'`, `'porter'`, `'portuguese'`, `'romanian'`, `'russian'`, `'serbian'`, `'spanish'`, `'swedish'`, `'tamil'`, `'turkish'`，或 `'none'` 表示不使用词干提取。默认值为 `'porter'` |
| `stopwords` | `VARCHAR` | 包含单个 `VARCHAR` 列的表的限定名称，该列包含所需的停用词，或 `'none'` 表示不使用停用词。默认值为 `'english'`，表示预定义的 571 个英文停用词 |
| `ignore` | `VARCHAR` | 要忽略的正则表达式模式。默认值为 `'(\\.|[^a-z])+'`，忽略所有转义字符和非小写字母字符 |
| `strip_accents` | `BOOLEAN` | 是否删除重音（例如，将 `á` 转换为 `a`）。默认值为 `1` |
| `lower` | `BOOLEAN` | 是否将所有文本转换为小写。默认值为 `1` |
| `overwrite` | `BOOLEAN` | 是否覆盖表上的现有索引。默认值为 `0` |

<!-- markdownlint-enable MD056 -->

此 `PRAGMA` 在新创建的模式下构建索引。该模式将根据输入表命名：如果在表 `'main.table_name'` 上创建索引，则模式将命名为 `'fts_main_table_name'`。

### `PRAGMA drop_fts_index`

```python
drop_fts_index(input_table)
```

删除指定表的 FTS 索引。

| 名称 | 类型 | 描述 |
|:--|:--|:-----------|
| `input_table` | `VARCHAR` | 输入表的限定名称，例如 `'table_name'` 或 `'main.table_name'` |

### `match_bm25` 函数

```python
match_bm25(input_id, query_string, fields := NULL, k := 1.2, b := 0.75, conjunctive := 0)
```

当索引构建完成后，会创建一个检索宏，可用于搜索索引。

| 名称 | 类型 | 描述 |
|:--|:--|:----------|
| `input_id` | `VARCHAR` | 文档标识符的列名，例如 `'document_identifier'` |
| `query_string` | `VARCHAR` | 要搜索的字符串 |
| `fields` | `VARCHAR` | 要搜索的字段列表，用逗号分隔，例如 `'text_field_2, text_field_N'`。默认为 `NULL`，表示搜索所有已索引字段 |
| `k` | `DOUBLE` | Okapi BM25 检索模型中的参数 _k<sub>1</sub>_。默认值为 `1.2` |
| `b` | `DOUBLE` | Okapi BM25 检索模型中的参数 _b_。默认值为 `0.75` |
| `conjunctive` | `BOOLEAN` | 是否使查询为合取查询，即查询字符串中的所有术语都必须存在才能检索到文档 |

### `stem` 函数

```python
stem(input_string, stemmer)
```

将单词缩减为其基本形式。由扩展内部使用。

| 名称 | 类型 | 描述 |
|:--|:--|:----------|
| `input_string` | `VARCHAR` | 要进行词干提取的列或常量。 |
| `stemmer` | `VARCHAR` | 要使用的词干提取器类型。可选值包括 `'arabic'`, `'basque'`, `'catalan'`, `'danish'`, `'dutch'`, `'english'`, `'finnish'`, `'french'`, `'german'`, `'greek'`, `'hindi'`, `'hungarian'`, `'indonesian'`, `'irish'`, `'italian'`, `'lithuanian'`, `'nepali'`, `'norwegian'`, `'porter'`, `'portuguese'`, `'romanian'`, `'russian'`, `'serbian'`, `'spanish'`, `'swedish'`, `'tamil'`, `'turkish'`，或 `'none'` 表示不使用词干提取。 |

## 示例用法

创建一个表并填充文本数据：

```sql
CREATE TABLE documents (
    document_identifier VARCHAR,
    text_content VARCHAR,
    author VARCHAR,
    doc_version INTEGER
);
INSERT INTO documents
    VALUES ('doc1',
            'The mallard is a dabbling duck that breeds throughout the temperate.',
            'Hannes Mühleisen',
            3),
           ('doc2',
            'The cat is a domestic species of small carnivorous mammal.',
            'Laurens Kuiper',
            2
           );
```

构建索引，并使 `text_content` 和 `author` 列可搜索。

```sql
PRAGMA create_fts_index(
    'documents', 'document_identifier', 'text_content', 'author'
);
```

搜索 `author` 字段索引，查找由 `Muhleisen` 撰写的文档。这将检索 `doc1`：

```sql
SELECT document_identifier, text_content, score
FROM (
    SELECT *, fts_main_documents.match_bm25(
        document_identifier,
        'Muhleisen',
        fields := 'author'
    ) AS score
    FROM documents
) sq
WHERE score IS NOT NULL
  AND doc_version > 2
ORDER BY score DESC;
```

| document_identifier |                             text_content                             | score |
|---------------------|----------------------------------------------------------------------|------:|
| doc1                | The mallard is a dabbling duck that breeds throughout the temperate. | 0.0   |

搜索关于 `small cats` 的文档。这将检索 `doc2`：

```sql
SELECT document_identifier, text_content, score
FROM (
    SELECT *, fts_main_documents.match_bm25(
        document_identifier,
        'small cats'
    ) AS score
    FROM documents
) sq
WHERE score IS NOT NULL
ORDER BY score DESC;
```

| document_identifier |                        text_content                        | score |
|---------------------|------------------------------------------------------------|------:|
| doc2                | The cat is a domestic species of small carnivorous mammal. | 0.0   |

> 警告 FTS 索引在输入表发生变化时不会自动更新。
> 一种解决此限制的方法是重新创建索引以刷新。