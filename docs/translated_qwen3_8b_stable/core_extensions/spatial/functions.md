---
layout: docu
title: 空间函数
redirect_from:
- /docs/stable/extensions/spatial/functions
- /docs/stable/extensions/spatial/functions/
---

## 函数索引 
**[标量函数](#scalar-functions)**

| 函数 | 概要 |
| --- | --- |
| [`DuckDB_PROJ_Compiled_Version`](#duckdb_proj_compiled_version) | 返回DuckDB实例所编译的PROJ库版本的文本描述。 |
| [`DuckDB_Proj_Version`](#duckdb_proj_version) | 返回当前DuckDB实例所使用的PROJ库版本的文本描述。 |
| [`ST_Affine`](#st_affine) | 将仿射变换应用于几何体。 |
| [`ST_Area`](#st_area) | 计算几何体的面积。 |
| [`ST_Area_Spheroid`](#st_area_spheroid) | 使用地球椭球模型返回几何体以米为单位的面积。 |
| [`ST_AsGeoJSON`](#st_asgeojson) | 返回几何体作为GeoJSON片段。 |
| [`ST_AsHEXWKB`](#st_ashexwkb) | 返回几何体作为HEXWKB字符串。 |
| [`ST_AsSVG`](#st_assvg) | 将几何体转换为SVG片段或路径。 |
| [`ST_AsText`](#st_astext) | 返回几何体作为WKT字符串。 |
| [`ST_AsWKB`](#st_aswkb) | 返回几何体作为WKB（Well-Known-Binary）二进制块。 |
| [`ST_Azimuth`](#st_azimuth) | 返回两点之间的方位角（以北为起点顺时针测量的弧度）。 |
| [`ST_Boundary`](#st_boundary) | 返回几何体的“边界”。 |
| [`ST_Buffer`](#st_buffer) | 返回围绕输入几何体的目标距离的缓冲区。 |
| [`ST_BuildArea`](#st_buildarea) | 通过尝试“填充”输入几何体来创建多边形几何体。 |
| [`ST_Centroid`](#st_centroid) | 返回几何体的质心。 |
| [`ST_Collect`](#st_collect) | 将一系列几何体收集为一个集合几何体。 |
| [`ST_CollectionExtract`](#st_collectionextract) | 从GeometryCollection中提取几何体，形成一个类型化的多几何体。 |
| [`ST_ConcaveHull`](#st_concavehull) | 返回输入几何体的“凹”包络，包含所有源输入点，并可用于从点创建多边形。比率参数决定了凹度的水平；1.0返回凸包；0表示返回尽可能凹的包络。将allowHoles设置为非零值，以允许输出包含孔。 |
| [`ST_Contains`](#st_contains) | 如果第一个几何体包含第二个几何体，返回true。 |
| [`ST_ContainsProperly`](#st_containsproperly) | 如果第一个几何体“正确”包含第二个几何体，返回true。 |
| [`ST_ConvexHull`](#st_convexhull) | 返回包含几何体的凸包。 |
| [`ST_CoverageInvalidEdges`](#st_coverageinvalidedges) | 返回多边形覆盖中的无效边，这些边不被两个多边形共享。 |
| [`ST_CoverageSimplify`](#st_coveragesimplify) | 简化多边形覆盖的边，保持覆盖，确保简化后的多边形之间没有接缝。 |
| [`ST_CoverageUnion`](#st_coverageunion) | 将多边形覆盖中的所有几何体合并为一个几何体。 |
| [`ST_CoveredBy`](#st_coveredby) | 如果geom1被geom2“覆盖”，返回true。 |
| [`ST_Covers`](#st_covers) | 如果geom1“覆盖”geom2，返回true。 |
| [`ST_Crosses`](#st_crosses) | 如果geom1“穿过”geom2，返回true。 |
| [`ST_DWithin`](#st_dwithin) | 如果两个几何体之间的距离在目标距离以内，返回true。 |
| [`ST_DWithin_GEOS`](#st_dwithin_geos) | 如果两个几何体之间的距离在目标距离以内，返回true。 |
| [`ST_DWithin_Spheroid`](#st_dwithin_spheroid) | 使用地球椭球模型，返回两个POINT_2D在目标距离内（以米为单位）。 |
| [`ST_Difference`](#st_difference) | 返回两个几何体之间的“差”。 |
| [`ST_Dimension`](#st_dimension) | 返回几何体的“拓扑维度”。 |
| [`ST_Disjoint`](#st_disjoint) | 如果两个几何体不相交，返回true。 |
| [`ST_Distance`](#st_distance) | 返回两个几何体之间的平面距离。 |
| [`ST_Distance_GEOS`](#st_distance_geos) | 返回两个几何体之间的平面距离。 |
| [`ST_Distance_Sphere`](#st_distance_sphere) | 返回两个几何体之间的球面（大圆）距离。 |
| [`ST_Distance_Spheroid`](#st_distance_spheroid) | 使用地球椭球模型返回两个几何体之间的距离（以米为单位）。 |
| [`ST_Dump`](#st_dump) | 将几何体分解为一系列子几何体及其在原始几何体中的“路径”。 |
| [`ST_EndPoint`](#st_endpoint) | 返回LINESTRING的终点。 |
| [`ST_Envelope`](#st_envelope) | 返回几何体的最小包围矩形作为多边形几何体。 |
| [`ST_Equals`](#st_equals) | 如果两个几何体“相等”，返回true。 |
| [`ST_Extent`](#st_extent) | 返回包含输入几何体的最小包围框。 |
| [`ST_Extent_Approx`](#st_extent_approx) | 如果可用，返回几何体的近似包围框。 |
| [`ST_ExteriorRing`](#st_exteriorring) | 返回多边形几何体的外部环（壳）。 |
| [`ST_FlipCoordinates`](#st_flipcoordinates) | 返回一个新几何体，其输入几何体的坐标被“翻转”，使得x=y和y=x。 |
| [`ST_Force2D`](#st_force2d) | 强制几何体的顶点具有X和Y分量。 |
| [`ST_Force3DM`](#st_force3dm) | 强制几何体的顶点具有X、Y和M分量。 |
| [`ST_Force3DZ`](#st_force3dz) | 强制几何体的顶,点具有X、Y和Z分量。 |
| [`ST_Force4D`](#st_force4d) | 强制几何体的顶点具有X、Y、Z和M分量。 |
| [`ST_GeomFromGeoJSON`](#st_geomfromgeojson) | 从GeoJSON片段中反序列化GEOMETRY。 |
| [`ST_GeomFromHEXEWKB`](#st_geomfromhexewkb) | 从HEX(E)WKB编码字符串中反序列化GEOMETRY。 |
| [`ST_GeomFromHEXWKB`](#st_geomfromhexwkb) | 从HEX(E)WKB编码字符串中反序列化GEOMETRY。 |
| [`ST_GeomFromText`](#st_geomfromtext) | 从WKT编码字符串中反序列化GEOMETRY。 |
| [`ST_GeomFromWKB`](#st_geomfromwkb) | 从WKB编码的二进制块中反序列化GEOMETRY。 |
| [`ST_GeometryType`](#st_geometrytype) | 返回一个'GEOMETRY_TYPE'枚举，标识输入几何体的类型。可能的枚举返回类型是：`POINT`、`LINESTRING`、`POLYGON`、`MULTIPOINT`、`MULTILINESTRING`、`MULTIPOLYGON`和`GEOMETRYCOLLECTION`。 |
| [`ST_HasM`](#st_hasm) | 检查输入几何体是否有M值。 |
| [`ST_HasZ`](#st_hasz) | 检查输入几何体是否有Z值。 |
| [`ST_Hilbert`](#st_hilbert) | 将X和Y值编码为覆盖给定边界框的希尔伯特曲线索引。 |
| [`ST_Intersection`](#st_intersection) | 返回两个几何体的交集。 |
| [`ST_Intersects`](#st_intersects) | 如果几何体相交，返回true。 |
| [`ST_Intersects_Extent`](#st_intersects_extent) | 如果两个几何体的范围相交，返回true。 |
| [`ST_IsClosed`](#st_isclosed) | 检查几何体是否“闭合”。 |
| [`ST_IsEmpty`](#st_isempty) | 如果几何体是“空”，返回true。 |
| [`ST_IsRing`](#st_isring) | 如果几何体是一个环（同时满足ST_IsClosed和ST_IsSimple），返回true。 |
| [`ST_IsSimple`](#st_issimple) | 如果几何体是简单的，返回true。 |
| [`ST_IsValid`](#st_isvalid) | 如果几何体是有效的，返回true。 |
| [`ST_Length`](#st_length) | 返回输入线几何体的长度。 |
| [`ST_Length_Spheroid`](#st_length_spheroid) | 使用地球椭球模型返回输入几何体的长度（以米为单位）。 |
| [`ST_LineInterpolatePoint`](#st_lineinterpolatepoint) | 返回沿线在总2D长度的分数处插值的点。 |
| [`ST_LineInterpolatePoints`](#st_lineinterpolatepoints) | 返回沿线在总2D长度的分数处插值的多点。 |
| [`ST_LineMerge`](#st_linemerge) | “合并”输入线几何体，可选地考虑方向。 |
| [`ST_LineString2DFromWKB`](#st_linestring2dfromwkb) | 从WKB编码的二进制块中反序列化LINESTRING_2D。 |
| [`ST_LineSubstring`](#st_linesubstring) | 返回线在两个总2D长度分数之间的子字符串。 |
| [`ST_M`](#st_m) | 返回点几何体的M坐标。 |
| [`ST_MMax`](#st_mmax) | 返回几何体的最大M坐标。 |
| [`ST_MMin`](#st_mmin) | 返回几何体的最小M坐标。 |
| [`ST_MakeEnvelope`](#st_makeenvelope) | 从最小/最大坐标创建矩形多边形。 |
| [`ST_MakeLine`](#st_makeline) | 从一系列POINT几何体创建LINESTRING。 |
| [`ST_MakePolygon`](#st_makepolygon) | 从LINESTRING壳创建POLYGON。 |
| [`ST_MakeValid`](#st_makevalid) | 返回几何体的有效表示。 |
| [`ST_MaximumInscribedCircle`](#st_maximuminscribedcircle) | 返回输入几何体的最大内切圆，可选地带有容差。 |
| [`ST_MinimumRotatedRectangle`](#st_minimumrotatedrectangle) | 返回包围输入几何体的最小旋转矩形，通过使用旋转矩形而不是ST_Envelope()中最低和最高坐标值来找到周围框，具有最低面积。 |
| [`ST_Multi`](#st_multi) | 将单个几何体转换为多几何体。 |
| [`ST_NGeometries`](#st_ngeometries) | 返回集合几何体中的组件几何体数量。 |
| [`ST_NInteriorRings`](#st_ninteriorrings) | 返回多边形的内环数量。 |
| [`ST_NPoints`](#st_npoints) | 返回几何体中的顶点数量。 |
| [`ST_Node`](#st_node) | 返回由输入线字符串集合组合并添加额外顶点以形成交点的“节点化”MultiLinestring。 |
| [`ST_Normalize`](#st_normalize) | 返回几何体的“规范化”表示。 |
| [`ST_NumGeometries`](#st_numgeometries) | 返回集合几何体中的组件几何体数量。 |
| [`ST_NumInteriorRings`](#st_numinteriorrings) | 返回多边形的内环数量。 |
| [`ST_NumPoints`](#st_numpoints) | 返回几何体中的顶点数量。 |
| [`ST_Overlaps`](#st_overlaps) | 如果几何体重叠，返回true。 |
| [`ST_Perimeter`](#st_perimeter) | 返回几何体的周长。 |
| [`ST_Perimeter_Spheroid`](#st_perimeter_spheroid) | 使用地球椭球模型返回周长（以米为单位）。 |
| [`ST_Point`](#st_point) | 创建GEOMETRY点。 |
| [`ST_Point2D`](#st_point2d) | 创建POINT_2D。 |
| [`ST_Point2DFromWKB`](#st_point2dfromw, 0000000000000000000000000000000