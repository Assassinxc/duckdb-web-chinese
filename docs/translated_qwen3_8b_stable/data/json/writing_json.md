---
---
layout: docu
redirect_from:
- /docs/data/json/writing_json
title: JSON格式写入
---

可以使用`COPY`语句将表的内容或查询结果直接写入JSON文件。
例如：

```sql
CREATE TABLE cities AS
    FROM (VALUES ('Amsterdam', 1), ('London', 2)) cities(name, id);
COPY cities TO 'cities.json';
```

这将生成一个`cities.json`文件，内容如下：

```json
{"name":"Amsterdam","id":1}
{"name":"London","id":2}
```

如需更多信息，请参阅 [`COPY`语句]({% link docs/stable/sql/statements/copy.md %}#copy-to)。