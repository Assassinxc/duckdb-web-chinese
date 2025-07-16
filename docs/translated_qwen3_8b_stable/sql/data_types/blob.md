---
---
blurb: blob（二进制大对象）类型表示存储在数据库系统中的任意二进制对象。
layout: docu
redirect_from:
- /docs/sql/data_types/blob
title: Blob 类型
---

| 名称 | 别名 | 描述 |
|:---|:---|:---|
| `BLOB` | `BYTEA`, `BINARY`, `VARBINARY` | 可变长度的二进制数据 |

blob（**B**inary **L**arge **OB**ject）类型表示存储在数据库系统中的任意二进制对象。blob 类型可以包含任何类型的二进制数据，没有任何限制。数据库系统对实际字节所代表的内容是不透明的。

创建一个包含单个字节（170）的 `BLOB` 值：

```sql
SELECT '\xAA'::BLOB;
```

创建一个包含三个字节（170, 171, 172）的 `BLOB` 值：

```sql
SELECT '\xAA\xAB\xAC'::BLOB;
```

创建一个包含两个字节（65, 66）的 `BLOB` 值：

```sql
SELECT 'AB'::BLOB;
```

通常使用 blobs 来存储数据库没有显式支持的非文本对象，例如图像。虽然 blobs 可以存储最大达 4 GB 的对象，但通常不建议将非常大的对象存储在数据库系统中。在许多情况下，更好的做法是将大文件存储在文件系统中，并在数据库系统中使用 `VARCHAR` 字段存储文件路径。

## 函数

参见 [Blob 函数]({% link docs/stable/sql/functions/blob.md %})。