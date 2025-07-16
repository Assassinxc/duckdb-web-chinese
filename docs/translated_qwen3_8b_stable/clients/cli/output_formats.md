---
---
layout: docu
redirect_from:
- /docs/api/cli/output-formats
- /docs/api/cli/output-formats/
- /docs/api/cli/output_formats
- /docs/api/cli/output_formats/
- /docs/clients/cli/output_formats
title: 输出格式
---

`.mode` [点命令]({% link docs/stable/clients/cli/dot_commands.md %}) 可用于更改终端输出中返回表格的显示方式。除了自定义外观，这些模式还有其他好处。这在将 DuckDB 输出重定向到文件以在其他地方展示时非常有用。使用 `insert` 模式将构建一系列 SQL 语句，这些语句可在稍后用于插入数据。
`markdown` 模式在构建文档时特别有用，`latex` 模式则适用于撰写学术论文。

## 输出格式列表

<!-- markdownlint-disable MD056 -->

| 模式                                       | 描述                                                    |
| ------------------------------------------- | ------------------------------------------------------ |
| `ascii`                                     | 用 0x1F 和 0x1E 分隔列和行                            |
| `box`                                       | 使用 Unicode 箱线字符绘制表格                         |
| `csv`                                       | 逗号分隔值                                             |
| `column`                                    | 按列输出（参见 `.width`）                             |
| `duckbox`                                   | 具有丰富功能的表格（默认）                           |
| `html`                                      | HTML `<table>` 代码                                   |
| `insert ⟨TABLE⟩`{:.language-sql .highlight} | 用于 `⟨TABLE⟩`{:.language-sql .highlight} 的 SQL 插入语句 |
| `json`                                      | 结果以 JSON 数组形式呈现                              |
| `jsonlines`                                 | 结果以 NDJSON 形式呈现                                |
| `latex`                                     | LaTeX 表格环境代码                                    |
| `line`                                      | 每行一个值                                             |
| `list`                                      | 用 `|` 分隔值                                         |
| `markdown`                                  | Markdown 表格格式                                     |
| `quote`                                     | 以 SQL 方式转义答案                                   |
| `table`                                     | ASCII 艺术表格                                         |
| `tabs`                                      | 用制表符分隔值                                        |
| `tcl`                                       | TCL 列表元素                                          |
| `trash`                                     | 不输出                                                |

<!-- markdownlint-enable MD056 -->

## 更改输出格式

使用原始的 `.mode` 点命令查询当前使用的显示方式。

```sql
.mode
```

```text
current output mode: duckbox
```

使用带参数的 `.mode` 点命令设置输出格式。

```sql
.mode markdown
SELECT 'quacking intensifies' AS incoming_ducks;
```

```text
|    incoming_ducks    |
|----------------------|
| quacking intensifies |
```

还可以使用 `.separator` 命令调整输出显示。如果使用依赖分隔符的导出模式（如 `csv` 或 `tabs`），更改模式时分隔符将被重置。例如，`.mode csv` 将设置分隔符为逗号（`,`）。使用 `.separator "|"` 将会将输出转换为管道分隔。

```sql
.mode csv
SELECT 1 AS col_1, 2 AS col_2
UNION ALL
SELECT 10 AS col1, 20 AS col_2;
```

```csv
col_1,col_2
1,2
10,20
```

```sql
.separator "|"
SELECT 1 AS col_1, 2 AS col_2
UNION ALL
SELECT 10 AS col1, 20 AS col_2;
```

```csv
col_1|col_2
1|2
10|20
```

## `duckbox` 模式

默认情况下，DuckDB 使用 `duckbox` 模式呈现查询结果，这是一种功能丰富的 ASCII 艺术风格输出格式。

`duckbox` 模式支持 `large_number_rendering` 选项，该选项允许以人类可读的方式呈现大数字。它有三个级别：

- `off` – 所有数字都使用常规格式打印。
- `footer`（默认）– 大数字会附加人类可读格式。仅适用于单行结果。
- `all` – 所有大数字都会被替换为人类可读格式。

请参见以下示例：

```sql
.large_number_rendering off
SELECT pi() * 1_000_000_000 AS x;
```

```text
┌───────────────────┐
│         x         │
│      double       │
├───────────────────┤
│ 3141592653.589793 │
└───────────────────┘
```

```sql
.large_number_rendering footer
SELECT pi() * 1_000_000_000 AS x;
```

```text
┌───────────────────┐
│         x         │
│      double       │
├───────────────────┤
│ 3141592653.589793 │
│  (3.14 billion)   │
└───────────────────┘
```

```sql
.large_number_rendering all
SELECT pi() * 1_000_000_000 AS x;
```

```text
┌──────────────┐
│      x       │
│    double    │
├──────────────┤
│ 3.14 billion │
└──────────────┘
```