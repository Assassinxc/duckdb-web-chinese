---
---
layout: docu
redirect_from:
- /docs/api/cli/autocomplete
- /docs/api/cli/autocomplete/
- /docs/clients/cli/autocomplete
title: 自动补全
---

通过 [`autocomplete` 扩展]({% link docs/stable/core_extensions/autocomplete.md %})，shell 提供了针对 SQL 查询的上下文感知自动补全功能。按 `Tab` 键可触发自动补全。

可能会出现多个自动补全建议。你可以通过反复按 `Tab` 键向前循环浏览建议，或按 `Shift+Tab` 向后循环。按 `ESC` 键两次可撤销自动补全。

shell 会自动补全四种不同的组别：

* 关键字
* 表名和表函数
* 列名和标量函数
* 文件名

shell 会根据 SQL 语句中的位置来确定触发哪种自动补全。例如：

```sql
SELECT s
```

```text
student_id
```

```sql
SELECT student_id F
```

```text
FROM
```

```sql
SELECT student_id FROM g
```

```text
grades
```

```sql
SELECT student_id FROM 'd
```

```text
'data/
```

```sql
SELECT student_id FROM 'data/
```

```text
'data/grades.csv
```