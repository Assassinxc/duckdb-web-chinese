---
---
layout: docu
redirect_from:
- /docs/guides/python/ibis
title: 与 Ibis 集成
---

[Ibis](https://ibis-project.org) 是一个 Python 数据框库，支持 20 多种后端，DuckDB 为默认后端。Ibis 与 DuckDB 结合提供了一个 Pythonic 的 SQL 接口，具有出色的性能。

## 安装

您可以使用 pip 安装 Ibis 并指定 DuckDB 后端：

```bash
pip install 'ibis-framework[duckdb,examples]' # examples 仅用于访问 Ibis 提供的示例数据
```

或者使用 conda：

```bash
conda install ibis-framework
```

或者使用 mamba：

```bash
mamba install ibis-framework
```

## 创建数据库文件

Ibis 可以与多种文件类型一起工作，但其核心是连接到现有的数据库并与其数据进行交互。您可以从自己的 DuckDB 数据库开始，或者使用示例数据创建一个新的数据库。

```python
import ibis

con = ibis.connect("duckdb://penguins.ddb")
con.create_table(
    "penguins", ibis.examples.penguins.fetch().to_pyarrow(), overwrite = True
)
```

```python
# 输出：
DatabaseTable: penguins
  species           string
  island            string
  bill_length_mm    float64
  bill_depth_mm     float64
  flipper_length_mm int64
  body_mass_g       int64
  sex               string
  year              int64
```

现在您可以查看示例数据集已复制到数据库中：

```python
# 重新连接到持久化数据库（删除临时表）
con = ibis.connect("duckdb://penguins.ddb")
con.list_tables()
```

```python
# 输出：
['penguins']
```

有一个名为 `penguins` 的表。我们可以要求 Ibis 提供一个我们可以交互的对象。

```python
penguins = con.table("penguins")
penguins
```

```text
# 输出：
DatabaseTable: penguins
  species           string
  island            string
  bill_length_mm    float64
  bill_depth_mm     float64
  flipper_length_mm int64
  body_mass_g       int64
  sex               string
  year              int64
```

Ibis 是惰性求值的，因此我们看到的是表的模式，而不是数据本身。要查看数据，我们可以调用 `head` 并使用 `to_pandas` 将表的前几行转换为 pandas DataFrame。

```python
penguins.head().to_pandas()
```

```text
  species     island  bill_length_mm  bill_depth_mm  flipper_length_mm  body_mass_g     sex  year
0  Adelie  Torgersen            39.1           18.7              181.0       3750.0    male  2007
1  Adelie  Torgersen            39.5           17.4              186.0       3800.0  female  2007
2  Adelie  Torgersen            40.3           18.0              195.0       3250.0  female  2007
3  Adelie  Torgersen             NaN            NaN                NaN          NaN    None  2007
4  Adelie  Torgersen            36.7           19.3              193.0       3450.0  female  2007
```

`to_pandas` 会将现有的惰性表表达式求值。如果省略 `to_pandas`，您将看到 `to_pandas` 将要评估的 Ibis 表表达式的表示（当您准备好时！）。

```python
penguins.head()
```

```python
# 输出：
r0 := DatabaseTable: penguins
  species           string
  island            string
  bill_length_mm    float64
  bill_depth_mm     float64
  flipper_length_mm int64
  body_mass_g       int64
  sex               string
  year              int64

Limit[r0, n=5]
```

Ibis 使用 `to_pandas` 返回结果为 pandas DataFrame，但并不使用 pandas 来执行任何计算。查询由 DuckDB 执行。只有在调用 `to_pandas` 时，Ibis 才会将结果拉回并转换为 DataFrame。

## 交互模式

在本简介的其余部分，我们将开启交互模式，该模式部分执行查询以提供用户的结果预览。输出格式略有不同，但除此之外，这与在表表达式上调用 `to_pandas` 并返回最多 10 行结果是相同的。

```python
ibis.options.interactive = True
penguins.head()
```

```text
┏━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┓
┃ species ┃ island    ┃ bill_length_mm ┃ bill_depth_mm ┃ flipper_length_mm ┃ body_mass_g ┃ sex    ┃ year  ┃
┡━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━┩
│ string  │ string    │ float64        │ float64       │ int64             │ int64       │ string │ int64 │
├─────────┼───────────┼────────────────┼───────────────┼───────────────────┼─────────────┼────────┼───────┤
│ Adelie  │ Torgersen │           39.1 │          18.7 │               181 │        3750 │ male   │  2007 │
│ Adelie  │ Torgersen │           39.5 │          17.4 │               186 │        3800 │ female │  2007 │
│ Adelie  │ Torgersen │           40.3 │          18.0 │               195 │        3250 │ female │  2007 │
│ Adelie  │ Torgersen │            nan │           nan │              NULL │        NULL │ NULL   │  2007 │
│ Adelie  │ Torgersen │           36.7 │          19.3 │               193 │        3450 │ female │  2007 │
└─────────┴───────────┴────────────────┴───────────────┴───────────────────┴─────────────┴────────┴───────┘
```

## 常见操作

Ibis 提供了一系列有用的表方法，用于操作和查询表中的数据。

### filter

`filter` 允许您根据条件或多个条件选择行。

我们可以过滤以只保留物种为 Adelie 的企鹅：

```python
penguins.filter(penguins.species == "Gentoo")
```

```text
┏━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┓
┃ species ┃ island ┃ bill_length_mm ┃ bill_depth_mm ┃ flipper_length_mm ┃ body_mass_g ┃ sex    ┃ year  ┃
┡━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━┩
│ string  │ string │ float64        │ float64       │ int64             │ int64       │ string │ int64 │
├─────────┼────────┼────────────────┼───────────────┼───────────────────┼─────────────┼────────┼───────┤
│ Gentoo  │ Biscoe │           46.1 │          13.2 │               211 │        4500 │ female │  2007 │
│ Gentoo  │ Biscoe │           50.0 │          16.3 │               230 │        5700 │ male   │  2007 │
│ Gentoo  │ Biscoe │           48.7 │          14.1 │               210 │        4450 │ female │  2007 │
│ Gentoo  │ Biscoe │           50.0 │          15.2 │               218 │        5700 │ male   │  2007 │
│ Gentoo  │ Biscoe │           47.6 │          14.5 │               215 │        5400 │ male   │  2007 │
│ Gentoo  │ Biscoe │           46.5 │          13.5 │               210 │        4550 │ female │  2007 │
│ Gentoo  │ Biscoe │           45.4 │          14.6 │               211 │        4800 │ female │  2007 │
│ Gentoo  │ Biscoe │           46.7 │          15.3 │               219 │        5200 │ male   │  2007 │
│ Gentoo  │ Biscoe │           43.3 │          13.4 │               209 │        4400 │ female │  2007 │
│ Gentoo  │ Biscoe │           46.8 │          15.4 │               215 │        5150 │ male   │  2007 │
│ …       │ …      │              … │             … │                 … │           … │ …      │     … │
└─────────┴────────┴────────────────┴───────────────┴───────────────────┴─────────────┴────────┴───────┘
```

或者过滤出身体质量大于 6 公斤的 Gentoo 企鹅：

```python
penguins.filter((penguins.species == "Gentoo") & (penguins.body_mass_g > 6000))
```

```text
┏━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┓
┃ species ┃ island ┃ bill_length_mm ┃ bill_depth_mm ┃ flipper_length_mm ┃ body_mass_g ┃ sex    ┃ year  ┃
┡━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━┩
│ string  │ string │ float64        │ float64       │ int64             │ int64       │ string │ int64 │
├─────────┼────────┼────────────────┼───────────────┼───────────────────┼─────────────┼────────┼───────┤
│ Gentoo  │ Biscoe │           49.2 │          15.2 │               221 │        6300 │ male   │  2007 │
│ Gentoo  │ Biscoe │           59.6 │          17.0 │               230 │        6050 │ male   │  2007 │
└─────────┴────────┴────────────────┴───────────────┴───────────────────┴─────────────┴────────┴───────┘
```

您可以在 filter 中使用任何布尔比较（虽然如果尝试在字符串上使用 `<`，Ibis 会提醒您）。

### select

您的数据分析可能不需要一个给定表中的所有列。`select` 让您可以只选择您要工作的那些列。

要选择一列，您可以使用列名作为字符串：

```python
penguins.select("species", "island", "year").limit(3)
```

```text
┏━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━┓
┃ species ┃ island    ┃ year  ┃
┡━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━┩
│ string  │ string    │ int64 │
├─────────┼───────────┼───────┤
│ Adelie  │ Torgersen │  2007 │
│ Adelie  │ Torgersen │  2007 │
│ Adelie  │ Torgersen │  2007 │
│ …       │ …         │     … │
└─────────┴───────────┴───────┘
```

或者您可以使用列对象直接（当与 tab-completion 配合使用时这很方便）：

```python
penguins.select(penguins.species, penguins.island, penguins.year).limit(3)
```

```text
┏━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━┓
┃ species ┃ island    ┃ year  ┃
┡━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━┩
│ string  │ string    │ int64 │
├─────────┼───────────┼───────┤
│ Adelie  │ Torgersen │  2007 │
│ Adelie  │ Torgersen │  2007 │
│ Adelie  │ Torgersen │  2007 │
│ …       │ …         │     … │
└─────────┴───────────┴───────┘
```

或者您可以混合使用：

```python
penguins.select("species", "island", penguins.year).limit(3)
```

```text
┏━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━┓
┃ species ┃ island    ┃ year  ┃
┡━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━┩
│ string  │ string    │ int64 │
├─────────┼───────────┼───────┤
│ Adelie  │ Torgersen │  2007 │
│ Adelie  │ Torgersen │  2007 │
│ Adelie  │ Torgersen │  2007 │
│ …       │ …         │     … │
└─────────┴───────────┴───────┘
```

### mutate

`mutate` 让您可以向表中添加新列，这些列由现有列的值推导而来。

```python
penguins.mutate(bill_length_cm=penguins.bill_length_mm / 10)
```

```text
┏━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ species ┃ island    ┃ bill_length_mm ┃ bill_depth_mm ┃ flipper_length_mm ┃ body_mass_g ┃ sex    ┃ year  ┃ bill_length_cm ┃
┡━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ string  │ string    │ float64        │ float64       │ int64             │ int64       │ string │ int64 │ float64        │
├─────────┼───────────┼────────────────┼───────────────┼───────────────────┼─────────────┼────────┼───────┼────────────────┤
│ Adelie  │ Torgersen │           39.1 │          18.7 │               181 │        3750 │ male   │  2007 │           3.91 │
│ Adelie  │ Torgersen │           39.5 │          17.4 │               186 │        3800 │ female │  2007 │           3.95 │
│ Adelie  │ Torgersen │           40.3 │          18.0 │               195 │        3250 │ female │  2007 │           4.03 │
│ Adelie  │ Torgersen │            nan │           nan │              NULL │        NULL │ NULL   │  2007 │            nan │
│ Adelie  │ Torgersen │           36.7 │          19.3 │               193 │        3450 │ female │  2007 │           3.67 │
│ Adelie  │ Torgersen │           39.3 │          20.6 │               190 │        3650 │ male   │  2007 │           3.93 │
│ Adelie  │ Torgersen │           38.9 │          17.8 │               181 │        3625 │ female │  2007 │           3.89 │
│ Adelie  │ Torgersen │           39.2 │          19.6 │               195 │        4675 │ male   │  2007 │           3.92 │
│ Adelie  │ Torgersen │           34.1 │          18.1 │               193 │        3475 │ NULL   │  2007 │           3.41 │
│ Adelie  │ Torgersen │           42.0 │          20.2 │               190 │        4250 │ NULL   │  2007 │           4.20 │
│ …       │ …         │              … │             … │                 … │           … │ …      │     … │              … │
└─────────┴───────────┴────────────────┴───────────────┴───────────────────┴─────────────┴────────┴───────┴────────────────┘
```

请注意，现在表的宽度有点太大，无法显示所有列（具体取决于屏幕大小）。`bill_length` 现在以毫米和厘米两种单位存在。使用 `select` 来减少我们查看的列数。

```python
penguins.mutate(bill_length_cm=penguins.bill_length_mm / 10).select(
    "species",
    "island",
    "bill_depth_mm",
    "flipper_length_mm",
    "body_mass_g",
    "sex",
    "year",
    "bill_length_cm",
)
```

```text
┏━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ species ┃ island    ┃ bill_depth_mm ┃ flipper_length_mm ┃ body_mass_g ┃ sex    ┃ year  ┃ bill_length_cm ┃
┡━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ string  │ string    │ float64       │ int64             │ int64       │ string │ int64 │ float64        │
├─────────┼───────────┼───────────────┼───────────────────┼─────────────┼────────┼───────┼────────────────┤
│ Adelie  │ Torgersen │          18.7 │               181 │        3750 │ male   │  2007 │           3.91 │
│ Adelie  │ Torgersen │          17.4 │               186 │        3800 │ female │  2007 │           3.95 │
│ Adelie  │ Torgersen │          18.0 │               195 │        3250 │ female │  2007 │           4.03 │
│ Adelie  │ Torgersen │           nan │              NULL │        NULL │ NULL   │  2007 │            nan │
│ Adelie  │ Torgersen │          19.3 │               193 │        3450 │ female │  2007 │           3.67 │
│ Adelie  │ Torgersen │          20.6 │               190 │        3650 │ male   │  2007 │           3.93 │
│ Adelie  │ Torgersen │          17.8 │               181 │        3625 │ female │  2007 │           3.89 │
│ Adelie  │ Torgersen │          19.6 │               195 │        4675 │ male   │  2007 │           3.92 │
│ Adelie  │ Torgersen │          18.1 │               193 │        3475 │ NULL   │  2007 │           3.41 │
│ Adelie  │ Torgersen │          20.2 │               190 │        4250 │ NULL   │  2007 │           4.20 │
│ …       │ …         │             … │                 … │           … │ …      │     … │              … │
└─────────┴───────────┴───────────────┴───────────────────┴─────────────┴────────┴───────┴────────────────┘
```

### selectors

输入所有列名（除了一个）有点烦人。为了避免重复输入，我们可以使用 `selector` 快速选择或取消选择一组列。

```python
import ibis.selectors as s

penguins.mutate(bill_length_cm=penguins.bill_length_mm / 10).select(
    ~s.matches("bill_length_mm")
    # 匹配除 `bill_length_mm` 以外的所有列
)
```

```text
┏━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ species ┃ island    ┃ bill_depth_mm ┃ flipper_length_mm ┃ body_mass_g ┃ sex    ┃ year  ┃ bill_length_cm ┃
┡━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ string  │ string    │ float64       │ int64             │ int64       │ string │ int64 │ float64        │
├─────────┼───────────┼───────────────┼───────────────────┼─────────────┼────────┼───────┼────────────────┤
│ Adelie  │ Torgersen │          18.7 │               181 │        3750 │ male   │  2007 │           3.91 │
│ Adelie  │ Torgersen │          17.4 │               186 │        3800 │ female │  2007 │           3.95 │
│ Adelie  │ Torgersen │          18.0 │               195 │        3250 │ female │  2007 │           4.03 │
│ Adelie  │ Torgersen │           nan │              NULL │        NULL │ NULL   │  2007 │            nan │
│ Adelie  │ Torgersen │          19.3 │               193 │        3450 │ female │  2007 │           3.67 │
│ Adelie  │ Torgersen │          20.6 │               190 │        3650 │ male   │  2007 │           3.93 │
│ Adelie  │ Torgersen │          17.8 │               181 │        3625 │ female │  2007 │           3.89 │
│ Adelie  │ Torgersen │          19.6 │               195 │        4675 │ male   │  2007 │           3.92 │
│ Adelie  │ Torgersen │          18.1 │               193 │        3475 │ NULL   │  2007 │           3.41 │
│ Adelie  │ Torgersen │          20.2 │               190 │        4250 │ NULL   │  2007 │           4.20 │
│ …       │ …         │             … │                 … │           … │ …      │     … │              … │
└─────────┴───────────┴───────────────┴───────────────────┴─────────────┴────────┴───────┴────────────────┘
```

您还可以将 `selector` 与列名一起使用。

```python
penguins.select("island", s.numeric())
```

```text
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ island    ┃ bill_length_mm ┃ bill_depth_mm ┃ flipper_length_mm ┃ body_mass_g ┃ year  ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ string    │ float64        │ float64       │ int64             │ int64       │ int64 │
├───────────┼────────────────┼───────────────┼───────────────────┼─────────────┼───────┤
│ Torgersen │           39.1 │          18.7 │               181 │        3750 │  2007 │
│ Torgersen │           39.5 │          17.4 │               186 │        3800 │  2007 │
│ Torgersen │           40.3 │          18.0 │               195 │        3250 │  2007 │
│ Torgersen │            nan │           nan │              NULL │        NULL │  2007 │
│ Torgersen │           36.7 │          19.3 │               193 │        3450 │  2007 │
│ Torgersen │           39.3 │          20.6 │               190 │        3650 │  2007 │
│ Torgersen │           38.9 │          17.8 │               181 │        3625 │  2007 │
│ Torgersen │           39.2 │          19.6 │               195 │        4675 │  2007 │
│ Torgersen │           34.1 │          18.1 │               193 │        3475 │  2007 │
│ Torgersen │           42.0 │          20.2 │               190 │        4250 │  2007 │
│ …         │              … │             … │                 … │           … │     … │
└───────────┴────────────────┴───────────────┴───────────────────┴─────────────┴───────┘
```

您可以阅读更多关于 [`selectors`](https://ibis-project.org/reference/selectors/) 的内容在文档中！

### `order_by`

`order_by` 按升序或降序排列一个或多个列的值。

默认情况下，`ibis` 以升序排序：

```python
penguins.order_by(penguins.flipper_length_mm).select(
    "species", "island", "flipper_length_mm"
)
```

```text
┏━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┓
┃ species   ┃ island    ┃ flipper_length_mm ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━┩
│ string    │ string    │ int64             │
├───────────┼───────────┼───────────────────┤
│ Adelie    │ Biscoe    │               172 │
│ Adelie    │ Biscoe    │               174 │
│ Adelie    │ Torgersen │               176 │
│ Adelie    │ Dream     │               178 │
│ Adelie    │ Dream     │               178 │
│ Adelie    │ Dream     │               178 │
│ Chinstrap │ Dream     │               178 │
│ Adelie    │ Dream     │               179 │
│ Adelie    │ Torgersen │               180 │
│ Adelie    │ Biscoe    │               180 │
│ …         │ …         │                 … │
└───────────┴───────────┴───────────────────┘
```

您可以使用 `desc` 方法来降序排序：

```python
penguins.order_by(penguins.flipper_length_mm.desc()).select(
    "species", "island", "flipper_length_mm"
)
```

```text
┏━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┓
┃ species ┃ island ┃ flipper_length_mm ┃
┡━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━┩
│ string  │ string │ int64             │
├─────────┼────────┼───────────────────┤
│ Gentoo  │ Biscoe │               231 │
│ Gentoo  │ Biscoe │               230 │
│ Gentoo  │ Biscoe │               230 │
│ Gentoo  │ Biscoe │               230 │
│ Gentoo  │ Biscoe │               230 │
│ Gentoo  │ Biscoe │               230 │
│ Gentoo  │ Biscoe │               230 │
│ Gentoo  │ Biscoe │               230 │
│ Gentoo  │ Biscoe │               229 │
│ Gentoo  │ Biscoe │               229 │
│ …       │ …      │                 … │
└─────────┴────────┴───────────────────┘
```

或者您可以使用 `ibis.desc`

```python
penguins.order_by(ibis.desc("flipper_length_mm")).select(
    "species", "island", "flipper_length_mm"
)
```

```text
┏━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┓
┃ species ┃ island ┃ flipper_length_mm ┃
┡━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━┩
│ string  │ string │ int64             │
├─────────┼────────┼───────────────────┤
│ Gentoo  │ Biscoe │               231 │
│ Gentoo  │ Biscoe │               230 │
│ Gentoo  │ Biscoe │               230 │
│ Gentoo  │ Biscoe │               230 │
│ Gentoo  │ Biscoe │               230 │
│ Gentoo  │ Biscoe │               230 │
│ Gentoo  │ Biscoe │               230 │
│ Gentoo  │ Biscoe │               230 │
│ Gentoo  │ Biscoe │               229 │
│ Gentoo  │ Biscoe │               229 │
│ …       │ …      │                 … │
└─────────┴────────┴───────────────────┘
```

### aggregate

Ibis 提供了多种聚合函数，以帮助总结数据。

`mean`, `max`, `min`, `count`, `sum`（列表还在继续）。

要对整个列进行聚合，可以调用该列的相应方法。

```python
penguins.flipper_length_mm.mean()
```

```python
# 输出：
200.91520467836258
```

您可以使用 `aggregate` 方法一次计算多个聚合：

```python
penguins.aggregate([penguins.flipper_length_mm.mean(), penguins.bill_depth_mm.max()])
```

```text
┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓
┃ Mean(flipper_length_mm) ┃ Max(bill_depth_mm) ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━┩
│ float64                 │ float64            │
├─────────────────────────┼────────────────────┤
│              200.915205 │               21.5 │
└─────────────────────────┴────────────────────┘
```

但是，`aggregate` 真正发挥作用的时候是它与 `group_by` 配对使用的时候。

### `group_by`

`group_by` 创建了行组，这些行在一个或多个列上具有相同的值。

但它本身并不做太多事情——您可以将其与 `aggregate` 配对以获得结果。

```python
penguins.group_by("species").aggregate()
```

```text
┏━━━━━━━━━━━┓
┃ species   ┃
┡━━━━━━━━━━━┩
│ string    │
├───────────┤
│ Adelie    │
│ Gentoo    │
│ Chinstrap │
└───────────┘
```

我们按 `species` 列分组，并传递了一个“空”聚合命令。该结果是一个 `species` 列的唯一值列。

如果我们向 `group_by` 添加第二个列，我们将得到这些列中值的每个唯一组合。

```python
penguins.group_by(["species", "island"]).aggregate()
```

```text
┏━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ species   ┃ island    ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━┩
│ string    │ string    │
├───────────┼───────────┤
│ Adelie    │ Torgersen │
│ Adelie    │ Biscoe    │
│ Adelie    │ Dream     │
│ Gentoo    │ Biscoe    │
│ Chinstrap │ Dream     │
└───────────┴───────────┘
```

现在，如果我们向该聚合添加一个聚合函数，我们就可以真正发挥其作用。

```python
penguins.group_by(["species", "island"]).aggregate(penguins.bill_length_mm.mean())
```

```text
┏━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ species   ┃ island    ┃ Mean(bill_length_mm) ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│ string    │ string    │ float64              │
├───────────┼───────────┼──────────────────────┤
│ Adelie    │ Torgersen │            38.950980 │
│ Adelie    │ Biscoe    │            38.975000 │
│ Adelie    │ Dream     │            38.501786 │
│ Gentoo    │ Biscoe    │            47.504878 │
│ Chinstrap │ Dream     │            48.833824 │
└───────────┴───────────┴──────────────────────┘
```

通过将 `mean` 添加到 `aggregate` 中，我们现在有了一个简洁的方式来计算 `group_by` 中每个不同组的聚合。我们也可以计算任意多的聚合。

```python
penguins.group_by(["species", "island"]).aggregate(
    [penguins.bill_length_mm.mean(), penguins.flipper_length_mm.max()]
)
```

```text
┏━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ species   ┃ island    ┃ Mean(bill_length_mm) ┃ Max(flipper_length_mm) ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│ string    │ string    │ float64              │ int64                  │
├───────────┼───────────┼──────────────────────┼────────────────────────┤
│ Adelie    │ Torgersen │            38.950980 │                    210 │
│ Adelie    │ Biscoe    │            38.975000 │                    203 │
│ Adelie    │ Dream     │            38.501786 │                    208 │
│ Gentoo    │ Biscoe    │            47.504878 │                    231 │
│ Chinstrap │ Dream     │            48.833824 │                    212 │
└───────────┴───────────┴──────────────────────┴────────────────────────┘
```

如果我们需要更具体的分组，可以添加到 `group_by` 中。

```python
penguins.group_by(["species", "island", "sex"]).aggregate(
    [penguins.bill_length_mm.mean(), penguins.flipper_length_mm.max()]
)
```

```text
┏━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ species ┃ island    ┃ sex    ┃ Mean(bill_length_mm) ┃ Max(flipper_length_mm) ┃
┡━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│ string  │ string    │ string │ float64              │ int64                  │
├─────────┼───────────┼────────┼──────────────────────┼────────────────────────┤
│ Adelie  │ Torgersen │ male   │            40.586957 │                    210 │
│ Adelie  │ Torgersen │ female │            37.554167 │                    196 │
│ Adelie  │ Torgersen │ NULL   │            37.925000 │                    193 │
│ Adelie  │ Biscoe    │ female │            37.359091 │                    199 │
│ Adelie  │ Bisco0    │ male   │            40.590909 │                    203 │
│ Adelie  │ Dream     │ female │            36.911111 │                    202 │
│ Adelie  │ Dream     │ male   │            40.071429 │                    208 │
│ Adelie  │ Dream     │ NULL   │            37.500000 │                    179 │
│ Gentoo  │ Biscoe    │ female │            45.563793 │                    222 │
│ Gentoo  │ Biscoe    │ male   │            49.473770 │                    231 │
│ …       │ …         │ …      │                    … │                      … │
└─────────┴───────────┴────────┴──────────────────────┴────────────────────────┘
```

## 将所有内容串联起来

我们已经将一些 Ibis 调用连接在一起。我们使用 `mutate` 创建了一个新列，然后使用 `select` 仅查看新表的一个子集。我们只是将 `group_by` 与 `aggregate` 连接在一起。

没有任何事情阻止我们将这些概念组合起来，以对数据提出问题。

比如：

* 每个岛屿上 2008 年最大的雌性企鹅（按体重）是什么？

```python
penguins.filter((penguins.sex == "female") & (penguins.year == 2008)).group_by(
    ["island"]
).aggregate(penguins.body_mass_g.max())
```

```text
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ island    ┃ Max(body_mass_g) ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ string    │ int64            │
├───────────┼──────────────────┤
│ Biscoe    │             5200 │
│ Torgersen │             3800 │
│ Dream     │             3900 │
└───────────┴──────────────────┘
```

* 每个岛屿每年收集数据时最大的雄性企鹅（按体重）是什么？

```python
penguins.filter(penguins.sex == "male").group_by(["island", "year"]).aggregate(
    penguins.body_mass_g.max().name("max_body_mass")
).order_by(["year", "max_body_mass"])
```

```text
┏━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ island    ┃ year  ┃ max_body_mass ┃
┡━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━┩
│ string    │ int64 │ int64         │
├───────────┼───────┼───────────────┤
│ Dream     │  2007 │          4650 │
│ Torgersen │  2007 │          4675 │
│ Biscoe    │  2007 │          6300 │
│ Torgersen │  2008 │          4700 │
│ Dream     │  2008 │          4800 │
│ Biscoe    │  2008 │          6000 │
│ Torgersen │  2009 │          4300 │
│ Dream     │  2009 │          4475 │
│ Biscoe    │  2009 │          6000 │
└───────────┴───────┴───────────────┘
```

## 进一步学习

这就是本快速入门指南的全部内容。如果您想了解更多，请查看 [Ibis 文档](https://ibis-project.org)。