---
---
layout: docu
railroad: expressions/collate.js
redirect_from:
- /docs/sql/expressions/collations
title: 排序规则
---

<div id="rrdiagram"></div>

排序规则为执行引擎中文本的排序或比较提供了规则。排序规则对于本地化非常有用，因为不同语言或国家/地区对文本排序的规则是不同的。这些排序规则通常彼此不兼容。例如，在英语中，字母 `y` 位于 `x` 和 `z` 之间。然而，在立陶宛语中，字母 `y` 位于 `i` 和 `j` 之间。因此，支持不同的排序规则。用户在执行排序和比较操作时必须选择使用哪种排序规则。

默认情况下，使用 `BINARY` 排序规则。这意味着字符串的排序和比较仅基于其二进制内容。这对于标准 ASCII 字符（即大写字母 A-Z 和数字 0-9）是有意义的，但对于特殊 Unicode 字符通常没有多大意义。然而，这是执行排序和比较最快的方法。因此，除非另有需要，否则建议继续使用 `BINARY` 排序规则。

> `BINARY` 排序规则也以 `C` 和 `POSIX` 的别名提供。

> 警告 DuckDB 的排序规则支持有一些已知的限制，详见 [https://github.com/duckdb/duckdb/issues?q=is%3Aissue+is%3Aopen+collation+](https://github.com/duckdb/duckdb/issues?q=is%3Aissue+is%3Aopen+collation+)，并且计划有多个改进，详见 [https://github.com/duckdb/duckdb/issues/604](https://github.com/duckdb/duckdb/issues/604)。

## 使用排序规则

在 DuckDB 的独立安装中包含三种排序规则：`NOCASE`、`NOACCENT` 和 `NFC`。`NOCASE` 排序规则将字符视为相等，不论其大小写。`NOACCENT` 排序规则将字符视为相等，不论其重音。`NFC` 排序规则执行 NFC 归一化比较，更多信息请参见 [Unicode 归一化](https://en.wikipedia.org/wiki/Unicode_equivalence#Normalization)。

```sql
SELECT 'hello' = 'hElLO';
```

```text
false
```

```sql
SELECT 'hello' COLLATE NOCASE = 'hElLO';
```

```text
true
```

```sql
SELECT 'hello' = 'hëllo';
```

```text
false
```

```sql
SELECT 'hello' COLLATE NOACCENT = 'hëllo';
```

```text
true
```

可以通过使用点运算符链式组合排序规则。请注意，不是所有排序规则都可以组合在一起。通常，`NOCASE` 排序规则可以与任何其他排序规则组合，但大多数其他排序规则不能组合。

```sql
SELECT 'hello' COLLATE NOCASE = 'hElLÖ';
```

```text
false
```

```sql
SELECT 'hello' COLLATE NOACCENT = 'hElLÖ';
```

```text
false
```

```sql
SELECT 'hello' COLLATE NOCASE.NOACCENT = 'hElLÖ';
```

```text
true
```

## 默认排序规则

我们之前看到的排序规则都是按表达式指定的。也可以在全局数据库级别或基础表列级别指定默认排序规则。可以使用 `PRAGMA` `default_collation` 来指定全局默认排序规则。如果未指定其他排序规则，将使用该排序规则。

```sql
SET default_collation = NOCASE;
SELECT 'hello' = 'HeLlo';
```

```text
true
```

在创建表时也可以按列指定排序规则。当该列用于比较时，将使用该列的排序规则进行比较。

```sql
CREATE TABLE names (name VARCHAR COLLATE NOACCENT);
INSERT INTO names VALUES ('hännes');
```

```sql
SELECT name
FROM names
WHERE name = 'hannes';
```

```text
hännes
```

不过要注意，不同排序规则不能组合。这在你想要比较具有不同排序规则指定的列时可能会有问题。

```sql
SELECT name
FROM names
WHERE name = 'hannes' COLLATE NOCASE;
```

```console
错误：无法组合具有不同排序规则的类型！
```

```sql
CREATE TABLE other_names (name VARCHAR COLLATE NOCASE);
INSERT INTO other_names VALUES ('HÄNNES');
```

```sql
SELECT names.name AS name, other_names.name AS other_name
FROM names, other_names
WHERE names.name = other_names.name;
```

```console
错误：无法组合具有不同排序规则的类型！
```

我们需要手动覆盖排序规则：

```sql
SELECT names.name AS name, other_names.name AS other_name
FROM names, other_names
WHERE names.name COLLATE NOACCENT.NOCASE = other_names.name COLLATE NOACCENT.NOCASE;
```

|  name  | other_name |
|--------|------------|
| hännes | HÄNNES     |

## ICU 排序规则

我们之前看到的排序规则不依赖于地区，也不遵循任何特定的地区规则。如果你想遵循特定地区或语言的规则，你需要使用其中一个 ICU 排序规则。为此，你需要 [加载 ICU 扩展]({% link docs/stable/core_extensions/icu.md %}#installing-and-loading)。

加载此扩展将向你的数据库中添加多个语言和地区特定的排序规则。这些排序规则可以通过 `PRAGMA collations` 命令查询，或者通过查询 `pragma_collations` 函数。

```sql
PRAGMA collations;
SELECT list(collname) FROM pragma_collations();
```

```text
[af, am, ar, ar_sa, as, az, be, bg, bn, bo, br, bs, ca, ceb, chr, cs, cy, da, de, de_at, dsb, dz, ee, el, en, en_us, eo, es, et, fa, fa_af, ff, fi, fil, fo, fr, fr_ca, fy, ga, gl, gu, ha, haw, he, he_il, hi, hr, hsb, hu, hy, icu_noaccent, id, id_id, ig, is, it, ja, ka, kk, kl, km, kn, ko, kok, ku, ky, lb, lkt, ln, lo, lt, lv, mk, ml, mn, mr, ms, mt, my, nb, nb_no, ne, nfc, nl, nn, noaccent, nocase, om, or, pa, pa_in, pl, ps, pt, ro, ru, sa, se, si, sk, sl, smn, sq, sr, sr_ba, sr_me, sr_rs, sv, sw, ta, te, th, tk, to, tr, ug, uk, ur, uz, vi, wae, wo, xh, yi, yo, yue, yue_cn, zh, zh_cn, zh_hk, zh_mo, zh_sg, zh_tw, zu]
```

这些排序规则可以像其他排序规则一样使用。它们也可以与 `NOCASE` 排序规则组合使用。例如，要使用德语排序规则，可以使用以下代码片段：

```sql
CREATE TABLE strings (s VARCHAR COLLATE DE);
INSERT INTO strings VALUES ('Gabel'), ('Göbel'), ('Goethe'), ('Goldmann'), ('Göthe'), ('Götz');
SELECT * FROM strings ORDER BY s;
```

```text
"Gabel", "Göbel", "Goethe", "Goldmann", "Göthe", "Götz"
```