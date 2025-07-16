---
---
layout: docu
redirect_from:
- /docs/guides/data_viewers/youplot
title: 使用 YouPlot 进行 CLI 图表绘制
---

DuckDB 可以与 CLI 图表工具结合使用，以快速将输入传递到 stdout，从而在一行中绘制您的数据。

[YouPlot](https://github.com/red-data-tools/YouPlot) 是一个基于 Ruby 的 CLI 工具，可在终端中绘制美观的图表。它可以通过从 `stdin` 管道传输数据来接受来自其他程序的输入。它接受以制表符分隔（或您选择的分隔符）的数据，并且可以轻松生成各种类型的图表，包括条形图、折线图、直方图和散点图。

使用 DuckDB，您可以使用 `TO '/dev/stdout'` 命令将数据写入控制台 (`stdout`)。您也可以使用 `WITH (FORMAT csv, HEADER)` 来写入逗号分隔值。

## 安装 YouPlot

YouPlot 的安装说明可以在其主 [YouPlot 仓库](https://github.com/red-data-tools/YouPlot#installation) 中找到。如果您使用的是 Mac，可以使用：

```bash
brew install youplot
```

运行 `uplot --help` 确保您已成功安装！

## 将 DuckDB 查询结果输出到 stdout

通过结合 [`COPY...TO`]({% link docs/stable/sql/statements/copy.md %}#copy-to) 函数和 CSV 输出文件，可以从 DuckDB 支持的任何格式读取数据并将其传递给 YouPlot。进行此操作有三个重要步骤。

1. 例如，这是如何从 `input.json` 读取所有数据：

   ```bash
   duckdb -s "SELECT * FROM read_json_auto('input.json')"
   ```

2. 为了准备 YouPlot 的数据，编写一个简单的聚合查询：

   ```bash
   duckdb -s "SELECT date, sum(purchases) AS total_purchases FROM read_json_auto('input.json') GROUP BY 1 ORDER BY 2 DESC LIMIT 10"
   ```

3. 最后，将 `SELECT` 包裹在 `COPY ... TO` 函数中，并将输出位置设置为 `/dev/stdout`。

   语法如下：

   ```sql
   COPY (⟨query⟩) TO '/dev/stdout' WITH (FORMAT csv, HEADER);
   ```

   下面是完整的 DuckDB 命令，它以 CSV 格式输出带有标题的查询：

   ```bash
   duckdb -s "COPY (SELECT date, sum(purchases) AS total_purchases FROM read_json_auto('input.json') GROUP BY 1 ORDER BY 2 DESC LIMIT 10) TO '/dev/stdout' WITH (FORMAT csv, HEADER)"
   ```

## 将 DuckDB 连接到 YouPlot

现在，数据可以被传递给 YouPlot 了！假设我们有一个 `input.json` 文件，其中包含日期和某人在该日期的购买次数。使用上面的查询，我们将数据传递给 `uplot` 命令，绘制 Top 10 购买日期的图表。

```bash
duckdb -s "COPY (SELECT date, sum(purchases) AS total_purchases FROM read_json_auto('input.json') GROUP BY 1 ORDER BY 2 DESC LIMIT 10) TO '/dev/stdout' WITH (FORMAT csv, HEADER)" \
     | uplot bar -d, -H -t "Top 10 Purchase Dates"
```

这告诉 `uplot` 绘制一个条形图，使用逗号分隔符 (`-d,`)，数据包含标题 (`-H`)，并给图表添加标题 (`-t`)。

![youplot-top-10](/images/guides/youplot/top-10-plot.png)

## 额外技巧！stdin + stdout

也许您正在通过 `jq` 管道传输一些数据。也许您正在从某个地方下载 JSON 文件。您还可以通过将文件名更改为 `/dev/stdin` 来告诉 DuckDB 从另一个进程读取数据。

让我们结合一个来自 GitHub 的快速 `curl` 命令，查看某个用户最近的活动情况。

```bash
curl -sL "https://api.github.com/users/dacort/events?per_page=100" \
     | duckdb -s "COPY (SELECT type, count(*) AS event_count FROM read_json_auto('/dev/stdin') GROUP BY 1 ORDER BY 2 DESC LIMIT 10) TO '/dev/stdout' WITH (FORMAT csv, HEADER)" \
     | uplot bar -d, -H -t "GitHub Events for @dacort"
```

![github-events](/images/guides/youplot/github-events.png)