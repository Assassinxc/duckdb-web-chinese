---
---
layout: docu
redirect_from:
- /docs/guides/import/read_file
- /docs/guides/import/read_file/
- /docs/guides/file_formats/read_file
title: 直接读取文件
---

DuckDB 允许通过 [`read_text`](#read_text) 和 [`read_blob`](#read_blob) 函数直接读取文件。
这些函数接受文件名、文件名列表或通配符模式，并分别将每个文件的内容作为 `VARCHAR` 或 `BLOB` 输出，同时还会提供额外的元数据，如文件大小和最后修改时间。

## `read_text`

`read_text` 表函数将选定源的数据读取为 `VARCHAR`。每个文件对应一行数据，其中 `content` 字段包含相应文件的全部内容。

```sql
SELECT size, parse_path(filename), content
FROM read_text('test/sql/table_function/files/*.txt');
```

| size |             parse_path(filename)              |      content     |
|-----:|-----------------------------------------------|------------------|
| 12   | [test, sql, table_function, files, one.txt]   | Hello World!     |
| 2    | [test, sql, table_function, files, three.txt] | 42               |
| 10   | [test, sql, table_function, files, two.txt]   | Foo Bar\nFöö Bär |

文件内容首先会验证是否为有效的 UTF-8。如果 `read_text` 尝试读取无效 UTF-8 的文件，将抛出错误，并建议使用 [`read_blob`](#read_blob)。

## `read_blob`

`read_blob` 表函数将选定源的数据读取为 `BLOB`：

```sql
SELECT size, content, filename
FROM read_blob('test/sql/table_function/files/*');
```

| size |                              content                         |                filename                 |
|-----:|--------------------------------------------------------------|-----------------------------------------|
| 178  |  PK\x03\x04\x0A\x00\x00\x00\x00\x00\xACi=X\x14t\xCE\xC7\x0A… | test/sql/table_function/files/four.blob |
| 12   | Hello World!                                                 | test/sql/table_function/files/one.txt   |
| 2    | 42                                                           | test/sql/table_function/files/three.txt |
| 10   | F\xC3\xB6\xC3\xB6 B\xC3\xA4r                                 | test/sql/table_function/files/two.txt   |

## 结构

`read_text` 和 `read_blob` 返回的表的结构完全相同：

```sql
DESCRIBE FROM read_text('README.md');
```

|  column_name  | column_type | null | key  | default | extra |
|---------------|-------------|------|------|---------|-------|
| filename      | VARCHAR     | YES  | NULL | NULL    | NULL  |
| content       | VARCHAR     | YES  | NULL | NULL    | NULL  |
| size          | BIGINT      | YES  | NULL | NULL    | NULL  |
| last_modified | TIMESTAMP   | YES  | NULL | NULL    | NULL  |

## 处理缺失的元数据

在某些情况下，由于底层文件系统无法提供部分数据（例如，HTTPFS 无法始终返回有效的时间戳），这些单元格将被设置为 `NULL`。

## 对投影下推的支持

这些表函数还利用投影下推来避免不必要的属性计算。例如，您可以使用此功能通配一个包含大量文件的目录，仅获取文件大小列中的文件大小，只要不包含内容列，数据就不会被读入 DuckDB。