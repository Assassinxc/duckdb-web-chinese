---
---
layout: docu
redirect_from:
- /docs/dev/internal_errors
title: 内部错误
---

内部错误表示在 DuckDB 中发生了断言失败。它们通常由程序中未预期的条件或逻辑错误引起。

例如，在 DuckDB v1.2.1 上运行 [issue 17002](https://github.com/duckdb/duckdb/issues/17002) 会导致内部错误。

```console
INTERNAL 错误：
尝试访问大小为 3 的向量中的索引 3
```

> 该问题在 DuckDB v1.2.2 及更新版本中已修复。

遇到内部错误后，DuckDB 会进入“受限模式”，任何进一步的操作都会导致以下错误信息：

```console
FATAL 错误：
数据库由于之前的致命错误而失效。
在再次使用数据库之前必须重新启动数据库。
```

要继续使用同一个数据库，请在同一个数据库上启动一个新的 DuckDB 会话。

DuckDB 进入“受限模式”的原因是数据库处于未定义状态。内部错误本质上是 bug，理论上不应该发生，因此这些代码路径从未被测试过。

如果您遇到内部错误，请考虑创建一个最小可复现示例，并向 [DuckDB 问题跟踪器](https://github.com/duckdb/duckdb/issues/new/choose) 提交问题。