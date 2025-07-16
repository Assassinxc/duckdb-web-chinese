---
---
layout: docu
title: Hugging Face 支持
redirect_from:
- /docs/extensions/httpfs/hugging_face
- /docs/extensions/httpfs/hugging_face/
- /docs/stable/extensions/httpfs/hugging_face
- /docs/stable/extensions/httpfs/hugging_face/
---

`httpfs` 扩展引入了对 `hf://` 协议的支持，以访问托管在 [Hugging Face](https://huggingface.co/) 仓库中的数据集。详情请参阅 [公告博客文章]({% post_url 2024-05-29-access-150k-plus-datasets-from-hugging-face-with-duckdb %}).

## 使用

可以通过以下 URL 模式查询 Hugging Face 仓库：

```text
hf://datasets/⟨my_username⟩/⟨my_dataset⟩/⟨path_to_file⟩
```

例如，要读取 CSV 文件，可以使用以下查询：

```sql
SELECT *
FROM 'hf://datasets/datasets-examples/doc-formats-csv-1/data.csv';
```

其中：

* `datasets-examples` 是用户/组织的名称
* `doc-formats-csv-1` 是数据集仓库的名称
* `data.csv` 是仓库中的文件路径

查询结果为：

|  kind   | sound |
|---------|-------|
| dog     | woof  |
| cat     | meow  |
| pokemon | pika  |
| human   | hello |

要读取 JSONL 文件，可以运行以下查询：

```sql
SELECT *
FROM 'hf://datasets/datasets-examples/doc-formats-jsonl-1/data.jsonl';
```

最后，要读取 Parquet 文件，使用以下查询：

```sql
SELECT *
FROM 'hf://datasets/datasets-examples/doc-formats-parquet-1/data/train-00000-of-00001.parquet';
```

这些命令会从指定的文件格式中读取数据，并以结构化的表格形式显示。根据您正在处理的文件格式选择适当的命令。

## 创建本地表

为了避免每次查询都访问远程端点，可以通过运行 [`CREATE TABLE ... AS` 命令]({% link docs/stable/sql/statements/create_table.md %}#create-table--as-select-ctas) 将数据保存到 DuckDB 表中。例如：

```sql
CREATE TABLE data AS
    SELECT *
    FROM 'hf://datasets/datasets-examples/doc-formats-csv-1/data.csv';
```

然后，只需按如下方式查询 `data` 表：

```sql
SELECT *
FROM data;
```

## 多个文件

要查询特定目录下的所有文件，可以使用 [通配符模式]({% link docs/stable/data/multiple_files/overview.md %}#multi-file-reads-and-globs)。例如：

```sql
SELECT count(*) AS count
FROM 'hf://datasets/cais/mmlu/astronomy/*.parquet';
```

| count |
|------:|
| 173   |

通过使用通配符模式，您可以高效地处理大型数据集，并对多个文件执行全面的查询，简化您的数据检查和处理任务。在这里，您可以看到如何查找包含“planet”一词的天文学问题：

```sql
SELECT count(*) AS count
FROM 'hf://datasets/cais/mmlu/astronomy/*.parquet'
WHERE question LIKE '%planet%';
```

| count |
|------:|
| 21    |

## 版本和修订

在 Hugging Face 仓库中，数据集版本或修订版是不同的数据集更新。每个版本都是在特定时间点的快照，允许您跟踪更改和改进。在 Git 术语中，可以理解为一个分支或特定提交。

您可以使用以下 URL 查询不同的数据集版本/修订版：

```sql
hf://datasets/⟨my_username⟩/⟨my_dataset⟩@⟨my_branch⟩/⟨path_to_file⟩
```

例如：

```sql
SELECT *
FROM 'hf://datasets/datasets-examples/doc-formats-csv-1@~parquet/**/*.parquet';
```

|  kind   | sound |
|---------|-------|
| dog     | woof  |
| cat     | meow  |
| pokemon | pika  |
| human   | hello |

之前的查询会读取 `~parquet` 修订版下的所有 Parquet 文件。这是一个特殊分支，Hugging Face 会自动为每个数据集生成 Parquet 文件，以实现高效的扫描。

## 认证

在 DuckDB 密钥管理器中配置您的 Hugging Face Token 以访问私有或受保护的数据集。首先，访问 [Hugging Face 设置 – 令牌](https://huggingface.co/settings/tokens) 获取您的访问令牌。其次，使用 DuckDB 的 [密钥管理器]({% link docs/stable/configuration/secrets_manager.md %}) 在您的 DuckDB 会话中设置该令牌。DuckDB 支持两种用于管理密钥的提供者：

### `CONFIG`

用户必须将所有配置信息传递到 `CREATE SECRET` 语句中。要使用 `CONFIG` 提供者创建密钥，使用以下命令：

```sql
CREATE SECRET hf_token (
    TYPE huggingface,
    TOKEN 'your_hf_token'
);
```

### `credential_chain`

自动尝试获取凭据。对于 Hugging Face 令牌，它会尝试从 `~/.cache/huggingface/token` 获取。要使用 `credential_chain` 提供者创建密钥，使用以下命令：

```sql
CREATE SECRET hf_token (
    TYPE huggingface,
    PROVIDER credential_chain
);
```