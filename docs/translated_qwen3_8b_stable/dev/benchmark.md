---
---
layout: docu
redirect_from:
- /dev/benchmark
- /dev/benchmark/
- /docs/dev/benchmark
title: 基准测试套件
---

DuckDB 拥有一个广泛的基准测试套件。
在进行可能影响性能的更改时，运行这些基准测试以检测潜在的性能退化非常重要。

## 入门

要构建基准测试套件，请在 [DuckDB 仓库](https://github.com/duckdb/duckdb) 中运行以下命令：

```bash
BUILD_BENCHMARK=1 CORE_EXTENSIONS='tpch' make
```

## 列出基准测试

要列出所有可用的基准测试，请运行：

```bash
build/release/benchmark/benchmark_runner --list
```

## 运行基准测试

### 运行单个基准测试

要运行单个基准测试，请执行以下命令：

```bash
build/release/benchmark/benchmark_runner benchmark/micro/nulls/no_nulls_addition.benchmark
```

输出将以 CSV 格式打印到 `stdout`，格式如下：

```text
name	run	timing
benchmark/micro/nulls/no_nulls_addition.benchmark	1	0.121234
benchmark/micro/nulls/no_nulls_addition.benchmark	2	0.121702
benchmark/micro/nulls/no_nulls_addition.benchmark	3	0.122948
benchmark/micro/nulls/no_nulls_addition.benchmark	4	0.122534
benchmark/micro/nulls/no_nulls_addition.benchmark	5	0.124102
```

您还可以使用 `--out` 标志指定输出文件。这将仅将时间（以换行符分隔）写入该文件。

```bash
build/release/benchmark/benchmark_runner benchmark/micro/nulls/no_nulls_addition.benchmark --out=timings.out
```

输出将包含以下内容：

```text
0.182472
0.185027
0.184163
0.185281
0.182948
```

### 使用正则表达式运行多个基准测试

您还可以使用正则表达式来指定要运行的基准测试。
请注意某些正则表达式字符（例如 `*`）可能会被 shell 扩展，因此需要正确引用或转义。

```bash
build/release/benchmark/benchmark_runner "benchmark/micro/nulls/.*"
```

#### 运行所有基准测试

不指定任何参数将运行所有基准测试。

```bash
build/release/benchmark/benchmark_runner
```

#### 其他选项

`--info` 标志会为您提供一些有关基准测试的其他信息。

```bash
build/release/benchmark/benchmark_runner benchmark/micro/nulls/no_nulls_addition.benchmark --info
```

```text
display_name:NULL Addition (no nulls)
group:micro
subgroup:nulls
```

`--query` 标志将打印由基准测试运行的查询。

```sql
SELECT min(i + 1) FROM integers;
```

`--profile` 标志将输出一个查询树。