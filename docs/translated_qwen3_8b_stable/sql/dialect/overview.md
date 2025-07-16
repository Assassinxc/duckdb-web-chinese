---
---
layout: docu
redirect_from:
- /docs/sql/dialect/overview
title: 概述
---

DuckDB 的 SQL 方言基于 PostgreSQL。
DuckDB 试图尽可能贴近 PostgreSQL 的语义，然而，某些用例需要稍微不同的行为。
例如，与数据框库的互操作性需要默认支持 [插入顺序保留]({% link docs/stable/sql/dialect/order_preservation.md %})。
这些差异在下面的页面中进行了说明。