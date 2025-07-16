---
---
layout: docu
redirect_from:
- /docs/guides/import/json_export
- /docs/guides/import/json_export/
- /docs/guides/file_formats/json_export
title: JSON 导出
---

要将表中的数据导出为 JSON 文件，可以使用 `COPY` 语句：

```sql
COPY tbl TO 'output.json';
```

查询结果也可以直接导出为 JSON 文件：

```sql
COPY (SELECT * FROM range(3) tbl(n)) TO 'output.json';
```

```text
{"n":0}
{"n":1}
{"n":2}
```

JSON 导出默认以 JSON 行格式写入，标准化为 [换行分隔的 JSON](https://en.wikipedia.org/wiki/JSON_streaming#NDJSON)。
可以使用 `ARRAY` 选项将数据写入单个 JSON 数组对象。

```sql
COPY (SELECT * FROM range(3) tbl(n)) TO 'output.json' (ARRAY);
```

```text
[
        {"n":0},
        {"n":1},
        {"n":2}
]
```

如需其他选项，请参阅 [`COPY` 语句文档]({% link docs/stable/sql/statements/copy.md %})。