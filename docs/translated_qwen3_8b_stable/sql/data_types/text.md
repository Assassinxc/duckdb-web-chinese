---
---
blurb: 在DuckDB中，字符串可以存储在VARCHAR字段中。
layout: docu
redirect_from:
- /docs/sql/data_types/text
title: 文本类型
---

在DuckDB中，字符串可以存储在`VARCHAR`字段中。
该字段允许存储Unicode字符。内部数据以UTF-8编码。

| 名称 | 别名 | 描述 |
|:---|:---|:---|
| `VARCHAR` | `CHAR`, `BPCHAR`, `STRING`, `TEXT` | 可变长度字符字符串 |
| `VARCHAR(n)` | `CHAR(n)`, `BPCHAR(n)`, `STRING(n)`, `TEXT(n)` | 可变长度字符字符串。最大长度`n`没有影响，仅用于兼容性 |

## 指定长度限制

为`VARCHAR`、`STRING`和`TEXT`类型指定长度不是必需的，也不会对系统产生影响。指定长度不会提高数据库中字符串的性能或减少存储空间。这些变体是为了与其他需要指定字符串长度的系统兼容而支持的。

如果您出于数据完整性原因希望限制`VARCHAR`列中的字符数，应使用`CHECK`约束，例如：

```sql
CREATE TABLE strings (
    val VARCHAR CHECK (length(val) <= 10) -- val最大长度为10
);
```

`VARCHAR`字段允许存储Unicode字符。内部数据以UTF-8编码。

## 指定压缩类型

您可以使用`USING COMPRESSION`子句为字符串指定压缩类型。
例如，要应用zstd压缩，请运行：

```sql
CREATE TABLE tbl(s VARCHAR USING COMPRESSION zstd);
```

## 文本类型值

文本类型的值是字符字符串，也称为字符串值或简称为字符串。在运行时，字符串值可以通过以下方式构造：

* 引用声明类型或隐式类型为文本数据类型的列
* [字符串字面量]({% link docs/stable/sql/data_types/literal_types.md %}#string-literals)
* [转换]({% link docs/stable/sql/expressions/cast.md %}#explicit-casting)表达式为文本类型
* 应用[字符串操作符]({% link docs/stable/sql/functions/text.md %}#text-functions-and-operators)，或调用返回文本类型值的函数

## 包含特殊字符的字符串

要在字符串中使用特殊字符，请使用[转义字符串字面量]({% link docs/stable/sql/data_types/literal_types.md %}#escape-string-literals)或[美元引号字符串字面量]({% link docs/stable/sql/data_types/literal_types.md %}#dollar-quoted-string-literals)。或者，您可以使用连接运算符和[`chr`字符函数]({% link docs/stable/sql/functions/text.md %})：

```sql
SELECT 'Hello' || chr(10) || 'world' AS msg;
```

```text
┌──────────────┐
│     msg      │
│   varchar    │
├──────────────┤
│ Hello\nworld │
└──────────────┘
```

## 函数

参见[文本函数]({% link docs/stable/sql/functions/text.md %})和[模式匹配]({% link docs/stable/sql/functions/pattern_matching.md %})。