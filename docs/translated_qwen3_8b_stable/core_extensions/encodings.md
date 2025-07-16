---
---
github_directory: https://github.com/duckdb/duckdb-encodings
layout: docu
title: 编码扩展
redirect_from:
- /docs/stable/extensions/encodings
- /docs/stable/extensions/encodings/
- /docs/extensions/encodings
- /docs/extensions/encodings/
---

`encodings` 扩展支持使用 [ICU 数据库中超过 1,000 种字符编码](https://github.com/unicode-org/icu-data/tree/main/charset/data/ucm) 读取 CSV 文件。

### 安装和加载

```sql
INSTALL encodings;
LOAD encodings;
```

## 使用

读取文件时指定编码：

```sql
FROM read_csv('my_shift_jis.csv', encoding = 'shift_jis');
```