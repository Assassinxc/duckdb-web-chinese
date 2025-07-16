---
---
layout: docu
title: GDAL 集成
redirect_from:
- /docs/stable/extensions/spatial/gdal
- /docs/stable/extensions/spatial/gdal/
---

空间扩展集成了 [GDAL](https://gdal.org/en/latest/) 转换库，以读取和写入多种地理空间矢量文件格式中的空间数据。请参阅 [`st_read` 表函数]({% link docs/stable/core_extensions/spatial/functions.md %}#st_read) 的文档，了解如何在实际中使用此功能。

为了免去用户在系统上设置和安装额外依赖项的麻烦，空间扩展自带了 GDAL 库的副本。这意味着空间扩展中的 GDAL 版本可能不是最新版本，也不一定支持系统级 GDAL 安装所支持的所有文件格式。请参阅 [`st_drivers` 表函数]({% link docs/stable/core_extensions/spatial/functions.md %}#st_drivers) 部分，以查看当前可用的 GDAL 驱动程序。

## 基于 GDAL 的 `COPY` 函数

空间扩展不仅可以导入地理空间文件格式（通过 `ST_Read` 函数），还可以通过基于 GDAL 的 `COPY` 函数将 DuckDB 表导出为不同的地理空间矢量格式。

例如，要将表导出为 GeoJSON 文件，并生成边界框，可以使用以下查询：

```sql
COPY ⟨table⟩ TO 'some/file/path/filename.geojson'
WITH (FORMAT gdal, DRIVER 'GeoJSON', LAYER_CREATION_OPTIONS 'WRITE_BBOX=YES');
```

可用选项：

* `FORMAT`：是唯一必需的选项，必须设置为 `GDAL` 才能使用基于 GDAL 的复制功能。
* `DRIVER`：是用于导出的 GDAL 驱动程序。使用 `ST_Drivers()` 列出所有可用驱动程序的名称。
* `LAYER_CREATION_OPTIONS`：传递给 GDAL 驱动程序的选项列表。请参阅您正在使用的 GDAL 文档，以获取可用选项列表。
* `SRS`：设置用于导出的空间参考系统作为元数据。这可以是 WKT 字符串、EPSG 代码或 proj 字符串，基本上是您通常可以传递给 GDAL 的任何内容。请注意，这**不会**对输入几何进行重投影，如果目标驱动程序支持，它只会设置元数据。

## 局限性

请注意，GDAL 集成仅支持基于矢量的驱动程序。读取和写入栅格格式不受支持。