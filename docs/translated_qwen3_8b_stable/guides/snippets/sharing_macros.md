---
---
layout: docu
redirect_from:
- /docs/guides/snippets/sharing_macros
title: 共享宏
---

DuckDB 具备强大的 [宏机制]({% link docs/stable/sql/statements/create_macro.md %})，允许为常见任务创建简写方式。

## 共享标量宏

首先，我们定义了一个宏，用于将非负整数以带有千位、百万位和十亿位（不进行四舍五入）的简短字符串形式进行格式化，如下所示：

```bash
duckdb pretty_print_integer_macro.duckdb
```

```sql
CREATE MACRO pretty_print_integer(n) AS
    CASE
        WHEN n >= 1_000_000_000 THEN printf('%dB', n // 1_000_000_000)
        WHEN n >= 1_000_000     THEN printf('%dM', n // 1_000_000)
        WHEN n >= 1_000         THEN printf('%dk', n // 1_000)
        ELSE printf('%d', n)
    END;

SELECT pretty_print_integer(25_500_000) AS x;
```

```text
┌─────────┐
│    x    │
│ varchar │
├─────────┤
│ 25M     │
└─────────┘
```

正如预期一样，宏会被持久化到数据库中。
但这也意味着我们可以将其托管在 HTTPS 端点上，并与任何人共享！
我们已经在 `blobs.duckdb.org` 上发布了这个宏。

你可以在 DuckDB 中尝试使用它：

```bash
duckdb
```

确保已安装 [`httpfs` 扩展]({% link docs/stable/core_extensions/httpfs/overview.md %})：

```sql
INSTALL httpfs;
```

现在你可以连接到远程端点并使用该宏：

```sql
ATTACH 'https://blobs.duckdb.org/data/pretty_print_integer_macro.duckdb'
    AS pretty_print_macro_db;

SELECT pretty_print_macro_db.pretty_print_integer(42_123) AS x;
```

```text
┌─────────┐
│    x    │
│ varchar │
├─────────┤
│ 42k     │
└─────────┘
```

## 共享表宏

也可以共享表宏。例如，我们创建了 [`checksum` 宏]({% post_url 2024-10-11-duckdb-tricks-part-2 %}#computing-checksums-for-columns)，如下所示：

```bash
duckdb compute_table_checksum.duckdb
```

```sql
CREATE MACRO checksum(table_name) AS TABLE
    SELECT bit_xor(md5_number(COLUMNS(*)::VARCHAR))
    FROM query_table(table_name);
```

使用它之前，请确保已安装 [`httpfs` 扩展]({% link docs/stable/core_extensions/httpfs/overview.md %})：

```sql
INSTALL httpfs;
```

现在你可以连接到远程端点并使用该宏：

```sql
ATTACH 'https://blobs.duckdb.org/data/compute_table_checksum.duckdb'
    AS compute_table_checksum_db;

CREATE TABLE stations AS
    FROM 'https://blobs.duckdb.org/stations.parquet';

.mode line
FROM compute_table_checksum_db.checksum('stations');
```

```text
         id = -132780776949939723506211681506129908318
       code = 126327004005066229305810236187733612209
        uic = -145623335062491121476006068124745817380
 name_short = -114540917565721687000878144381189869683
name_medium = -568264780518431562127359918655305384
  name_long = 126079956280724674884063510870679874110
       slug = -53458800462031706622213217090663245511
    country = 143068442936912051858689770843609587944
       type = 5665662315470785456147400604088879751
    geo_lat = 160608116135251821259126521573759502306
    geo_lng = -138297281072655463682926723171691547732
```