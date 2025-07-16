---
---
github_repository: https://github.com/duckdb/duckdb-spatial
layout: docu
title: 空间扩展
redirect_from:
- /docs/stable/extensions/spatial
- /docs/stable/extensions/spatial/
- /docs/stable/extensions/spatial/overview
- /docs/stable/extensions/spatial/overview/
- /docs/extensions/spatial
- /docs/extensions/spatial/
---

`spatial` 扩展为 DuckDB 提供了对地理空间数据处理的支持。有关该扩展的概述，请参阅我们的 [博客文章]({% post_url 2023-04-28-spatial %}）。

## 安装和加载

要安装 `spatial` 扩展，请运行：

```sql
INSTALL spatial;
```

请注意，`spatial` 扩展不可自动加载。因此，在使用之前需要先加载它：

```sql
LOAD spatial;
```

## `GEOMETRY` 类型

空间扩展的核心是 `GEOMETRY` 类型。如果你不熟悉地理空间数据和 GIS 工具，这种类型可能与你预期的完全不同。

表面上看，`GEOMETRY` 类型是“几何”数据的二进制表示，由一组顶点（X 和 Y 的 `double` 精度浮点数对）组成。但使其略显特殊的是，它实际上用于存储几种不同的几何子类型。这些子类型包括 `POINT`、`LINESTRING`、`POLYGON`，以及它们的“集合”等价类型 `MULTIPOINT`、`MULTILINESTRING` 和 `MULTIPOLYGON`。最后是 `GEOMETRYCOLLECTION`，它可以包含其他任何子类型，也可以包含其他 `GEOMETRYCOLLECTION`，并可以递归嵌套。

乍看之下这可能有些奇怪，因为 DuckDB 已经有 `LIST`、`STRUCT` 和 `UNION` 这样的类型，可以以类似方式使用。但 `GE.OMETRY` 类型的设计和行为实际上基于 [Simple Features](https://en.wikipedia.org/wiki/Simple_Features) 几何模型，这是一种被许多其他数据库和 GIS 软件使用的标准。

空间扩展还包含几种实验性的非标准显式几何类型，如 `POINT_2D`、`LINESTRING_2D`、`POLYGON_2D` 和 `BOX_2D`，它们基于 DuckDB 原生的嵌套类型，如 `STRUCT` 和 `LIST`。由于这些类型的内部内存布局固定且可预测，理论上可以优化许多地理空间算法，使其在这些类型上运行得比在 `GEOMETRY` 类型上更快。不过，目前空间扩展中只有少数函数明确针对这些类型进行了优化。所有这些新类型都可以隐式转换为 `GEOMETRY`，但转换成本较低，因此如果计划使用大量不同的空间函数，目前仍推荐使用 `GEOMETRY` 类型。

目前 `GEOMETRY` 类型尚无法存储诸如曲线几何或三角网等其他几何类型。此外，`GEOMETRY` 类型不会按值存储 SRID 信息。这些限制可能在未来得到解决。