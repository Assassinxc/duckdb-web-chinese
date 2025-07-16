---
---
layout: docu
redirect_from:
- /dev/sqllogictest/loops
- /dev/sqllogictest/loops/
- /docs/dev/sqllogictest/loops
title: 循环
---

在 sqllogictest 中，当需要多次执行相同的查询但常量值略有变化时，可以使用循环。例如，假设我们想要执行 100 个查询，检查表中是否存在值 `0..100`：

```sql
# 创建名为 'integers' 的表，包含值 0..100
statement ok
CREATE TABLE integers AS SELECT * FROM range(0, 100, 1) t1(i);

# 逐个验证所有 100 个值是否存在
loop i 0 100

# 执行查询，替换值
query I
SELECT count(*) FROM integers WHERE i = ${i};
----
1

# 结束循环（注意，多个语句可以作为循环的一部分）
endloop
```

同样，`foreach` 可以用于遍历一组值。

```sql
foreach partcode millennium century decade year quarter month day hour minute second millisecond microsecond epoch

query III
SELECT i, date_part('${partcode}', i) AS p, date_part(['${partcode}'], i) AS st
FROM intervals
WHERE p <> st['${partcode}'];
----

endloop
```

`foreach` 还有一些预设的组合，在需要时应使用这些组合。这样，当新增预设组合时，旧的测试会自动使用这些新的组合。

<div class="monospace_table"></div>

|     预设      |                          扩展                           |
|--------------|--------------------------------------------------------|
| ⟨compression⟩ | none uncompressed rle bitpacking dictionary fsst chimp patas |
| ⟨signed⟩      | tinyint smallint integer bigint hugeint               |
| ⟨unsigned⟩    | utinyint usmallint uinteger ubigint uhugeint          |
| ⟨integral⟩    | ⟨signed⟩ ⟨unsigned⟩                                    |
| ⟨numeric⟩     | ⟨integral⟩ float double                                |
| ⟨alltypes⟩    | ⟨numeric⟩ bool interval varchar json                   |

> 少用大循环。执行数十万条 SQL 语句会无谓地减慢测试速度。不要使用循环来插入数据。

## 不使用循环的数据生成

应尽量少用循环。虽然使用插入语句插入数据可能很诱人，但这会显著降低测试用例的执行速度。相反，最好使用内置的 `range` 和 `repeat` 函数生成数据。

要创建包含值 `[0, 1, .., 98, 99]` 的表 `integers`，请运行：

```sql
CREATE TABLE integers AS SELECT * FROM range(0, 100, 1) t1(i);
```

要创建包含 100 次 `hello` 值的表 `strings`，请运行：

```sql
CREATE TABLE strings AS SELECT * FROM repeat('hello', 100) t1(s);
```

使用这两个函数，结合交叉积和其他表达式的巧妙使用，可以高效地生成许多不同类型的数据库。`random()` 函数也可以用来生成随机数据。

另一种选择是从现有的 CSV 或 Parquet 文件中读取数据。可以使用 `COPY INTO` 语句或 `read_csv_auto` 函数从目录 `test/sql/copy/csv/data/real` 中加载多个大型 CSV 文件。

TPC-H 和 TPC-DS 扩展也可以用来生成合成数据，例如使用 `CALL dbgen(sf = 1)` 或 `CALL dsdgen(sf = 1)`。