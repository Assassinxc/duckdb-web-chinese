---
---
github_directory: https://github.com/duckdb/duckdb/tree/main/extension/tpcds
layout: docu
title: TPC-DS 扩展
redirect_from:
- /docs/stable/extensions/tpcds
- /docs/stable/extensions/tpcds/
- /docs/extensions/tpcds
- /docs/extensions/tpcds/
---

`tpcds` 扩展实现了 [TPC-DS 基准测试](https://www.tpc.org/tpcds/) 的数据生成器和查询功能。

## 安装和加载

`tpcds` 扩展会在首次使用时从官方扩展仓库中透明地[自动加载]({% link docs/stable/core_extensions/overview.md %}#autoloading-extensions)。
如果你想手动安装和加载它，请运行：

```sql
INSTALL tpcds;
LOAD tpcds;
```

## 使用方法

要为规模因子 1 生成数据，请使用：

```sql
CALL dsdgen(sf = 1);
```

要运行一个查询，例如查询 8，请使用：

```sql
PRAGMA tpcds(8);
```

| s_store_name | sum(ss_net_profit) |
|--------------|-------------------:|
| able         | -10354620.18       |
| ation        | -10576395.52       |
| bar          | -10625236.01       |
| ese          | -10076698.16       |
| ought        | -10994052.78       |

## 生成模式

通过将规模因子设置为 0，可以不生成任何数据的情况下生成 TPC-DS 的模式：

```sql
CALL dsdgen(sf = 0);
```

## 局限性

`tpcds(⟨query_id⟩)`{:.language-sql .highlight} 函数会运行一个固定且预定义绑定参数（也称为替换参数）的 TPC-DS 查询。
无法使用 `tpcds` 扩展更改查询参数。