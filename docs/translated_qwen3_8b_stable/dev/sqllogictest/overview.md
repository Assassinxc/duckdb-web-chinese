---
---
layout: docu
redirect_from:
- /dev/testing
- /dev/testing/
- /docs/dev/sqllogictest/overview
title: 概述
---

## DuckDB 是如何进行测试的？

测试对于确保 DuckDB 正常运行并持续正常运行至关重要。因此，我们非常重视彻底且频繁的测试：
* 我们在每次提交时使用 [GitHub Actions](https://github.com/duckdb/duckdb/actions) 运行一批小型测试，并在 pull request 和 `main` 分支中的提交运行更全面的测试批次。
* 我们使用 [fuzzer](https://github.com/duckdb/duckdb-fuzzer)，它会自动报告通过模糊测试发现的问题。
* 我们使用 [SQLsmith]({% link docs/stable/core_extensions/sqlsmith.md %}) 生成随机查询。