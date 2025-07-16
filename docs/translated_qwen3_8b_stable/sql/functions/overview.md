---
---
layout: docu
railroad: expressions/function.js
redirect_from:
- /docs/test/functions/overview
- /docs/test/functions/overview/
- /docs/sql/functions/overview
title: 函数
---

## 函数语法

<div id="rrdiagram"></div>

## 使用点运算符进行函数链式调用

DuckDB 支持使用点语法进行函数链式调用。这允许将函数调用 `fn(arg1, arg2, arg3, ...)` 重写为 `arg1.fn(arg2, arg3, ...)`. 例如，以下使用 [`replace` 函数]({% link docs/stable/sql/functions/text.md %}#replacestring-source-target) 的示例：

```sql
SELECT replace(goose_name, 'goose', 'duck') AS duck_name
FROM unnest(['African goose', 'Faroese goose', 'Hungarian goose', 'Pomeranian goose']) breed(goose_name);
```

可以重写为以下形式：

```sql
SELECT goose_name.replace('goose', 'duck') AS duck_name
FROM unnest(['African goose', 'Faroese goose', 'Hungarian goose', 'Pomeranian goose']) breed(goose_name);
```

### 与字面量和数组一起使用

要将函数链式调用应用于字面量和随后的数组访问操作，必须用括号将参数括起来，例如：

```sql
SELECT ('hello world').replace(' ', '_');
```

```sql
SELECT (2).sqrt();
```

```sql
SELECT (m[1]).map_entries()
FROM (VALUES ([MAP {'hello': 42}, MAP {'world': 42}])) t(m);
```

如果没有这些括号，DuckDB 将返回一个 `Parser Error` 错误：

```console
Parser Error:
syntax error at or near "("
```

### 限制

通过点运算符进行函数链式调用仅限于 *标量* 函数，不支持 *表* 函数。
例如，以下调用将返回一个 `Parser Error` 错误：

```sql
SELECT * FROM ('my_file.parquet').read_parquet(); -- 不支持
```

## 查询函数

`duckdb_functions()` 表函数用于显示当前系统中内置的函数列表。

```sql
SELECT DISTINCT ON(function_name)
    function_name,
    function_type,
    return_type,
    parameters,
    parameter_types,
    description
FROM duckdb_functions()
WHERE function_type = 'scalar'
  AND function_name LIKE 'b%'
ORDER BY function_name;
```

| function_name | function_type | return_type |       parameters       |         parameter_types          |                                                               description                                                                |
|---------------|---------------|-------------|------------------------|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| bar           | scalar        | VARCHAR     | [x, min, max, width]   | [DOUBLE, DOUBLE, DOUBLE, DOUBLE] | 绘制一个带状图，其宽度与 (x - min) 成比例，当 x = max 时，宽度等于 width 字符。width 默认为 80                   |
| base64        | scalar        | VARCHAR     | [blob]                 | [BLOB]                           | 将 blob 转换为 base64 编码的字符串                                                                                                |
| bin           | scalar        | VARCHAR     | [value]                | [VARCHAR]                        | 将值转换为二进制表示形式                                                                                              |
| bit_count     | scalar        | TINYINT     | [x]                    | [TINYINT]                        | 返回设置的位数                                                                                                  |
| bit_length    | scalar        | BIGINT      | [col0]                 | [VARCHAR]                        | NULL                                                                                                                                     |
| bit_position  | scalar        | INTEGER     | [substring, bitstring] | [BIT, BIT]                       | 返回指定子字符串在位字符串中的第一个起始索引，如果不存在则返回零。第一个（最左边）位的索引为 1 |
| bitstring     | scalar        | BIT         | [bitstring, length]    | [VARCHAR, INTEGER]               | 将位字符串填充至指定长度                                                                                            |

> 目前，`duckdb_functions()` 函数中不包含函数的描述和参数名称。