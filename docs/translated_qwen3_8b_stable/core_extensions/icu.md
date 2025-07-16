---
---
github_directory: https://github.com/duckdb/duckdb/tree/main/extension/icu
layout: docu
title: ICU 扩展
redirect_from:
- /docs/stable/extensions/icu
- /docs/stable/extensions/icu/
- /docs/extensions/ice
- /docs/extensions/ice/
---

`icu` 扩展包含 [ICU 库](https://github.com/unicode-org/icu) 中排序/时区部分的易于使用的版本。

## 安装和加载

`icu` 扩展将在首次使用时从官方扩展仓库中透明地[自动加载]({% link docs/stable/core_extensions/overview.md %}#autoloading-extensions)。
如果您希望手动安装和加载它，请运行：

```sql
INSTALL icu;
LOAD icu;
```

## 功能

`icu` 扩展引入了以下功能：

* [区域相关排序]({% link docs/stable/sql/expressions/collations.md %})
* [时区]({% link docs/stable/sql/data_types/timezones.md %})，用于 [时间戳数据类型]({% link docs/stable/sql/data_types/timestamp.md %}) 和 [时间戳函数]({% link docs/stable/sql/functions/timestamptz.md %})