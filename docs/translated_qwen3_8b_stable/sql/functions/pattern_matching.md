---
---
layout: docu
railroad: expressions/like.js
redirect_from:
- /docs/sql/functions/patternmatching
- /docs/sql/functions/patternmatching/
- /docs/sql/functions/pattern_matching
title: 模式匹配
---

DuckDB 提供了四种独立的模式匹配方法：
传统的 SQL [`LIKE` 运算符](#like)，
较新的 [`SIMILAR TO` 运算符](#similar-to)（SQL:1999 中引入），
一个 [`GLOB` 运算符](#glob)，
以及 POSIX 风格的 [正则表达式](#regular-expressions)。

## `LIKE`

<div id="rrdiagram1"></div>

`LIKE` 表达式如果字符串与提供的模式匹配，将返回 `true`。（如预期，`NOT LIKE` 表达式如果 `LIKE` 返回 `true`，则返回 `false`，反之亦然。等效表达式是 `NOT (string LIKE pattern)`。）

如果模式中不包含百分号或下划线，则模式仅表示字符串本身；在这种情况下，`LIKE` 的行为与等于运算符相同。模式中的下划线（`_`）表示（匹配）任意单个字符；百分号（`%`）匹配任意零个或多个字符。

`LIKE` 模式匹配始终覆盖整个字符串。因此，如果希望匹配字符串中的任意序列，模式必须以百分号开头和结尾。

一些示例：

```sql
SELECT 'abc' LIKE 'abc';    -- true
SELECT 'abc' LIKE 'a%' ;    -- true
SELECT 'abc' LIKE '_b_';    -- true
SELECT 'abc' LIKE 'c';      -- false
SELECT 'abc' LIKE 'c%' ;    -- false
SELECT 'abc' LIKE '%c';     -- true
SELECT 'abc' NOT LIKE '%c'; -- false
```

可以使用关键字 `ILIKE` 替代 `LIKE` 以根据当前区域设置进行不区分大小写的匹配：

```sql
SELECT 'abc' ILIKE '%C'; -- true
```

```sql
SELECT 'abc' NOT ILIKE '%C'; -- false
```

要搜索字符串中某个字符是通配符（`%` 或 `_`），则模式必须使用 `ESCAPE` 子句和转义字符来指示通配符应被当作字面字符而不是通配符处理。请参见下面的例子。

此外，`like_escape` 函数的功能与带 `ESCAPE` 子句的 `LIKE` 表达式相同，但使用函数语法。详情请参见 [文本函数文档]({% link docs/stable/sql/functions/text.md %}).

搜索包含 'a' 后跟字面百分号再跟 'c' 的字符串：

```sql
SELECT 'a%c' LIKE 'a$%c' ESCAPE '$'; -- true
SELECT 'azc' LIKE 'a$%c' ESCAPE '$'; -- false
```

带 `ESCAPE` 的不区分大小写的 `ILIKE`：

```sql
SELECT 'A%c' ILIKE 'a$%c' ESCAPE '$'; -- true
```

还可以使用替代字符作为 `LIKE` 表达式的关键词。这些增强了对 PostgreSQL 的兼容性。

<div class="monospace_table"></div>

| PostgreSQL 风格 | `LIKE` 风格 |
| :--------------- | :----------- |
| `~~`             | `LIKE`       |
| `!~~`            | `NOT LIKE`   |
| `~~*`            | `ILIKE`      |
| `!~~*`           | `NOT ILIKE`  |

## `SIMILAR TO`

<div id="rrdiagram2"></div>

`SIMILAR TO` 运算符根据其模式是否匹配给定的字符串返回 `true` 或 `false`。它与 `LIKE` 相似，但使用 [正则表达式]({% link docs/stable/sql/functions/regular_expressions.md %}) 解释模式。与 `LIKE` 一样，`SIMILAR TO` 运算符只有在模式匹配整个字符串时才成功；这与常见正则表达式行为不同，常见正则表达式行为允许模式匹配字符串的任何部分。

正则表达式是一个字符序列，是字符串集合（正则集合）的简写定义。如果一个字符串是正则表达式所描述的正则集合的成员，则该字符串被认为匹配正则表达式。与 `LIKE` 一样，模式中的字符精确匹配字符串中的字符，除非它们是正则表达式语言中的特殊字符 —— 但正则表达式使用的特殊字符与 `LIKE` 不同。

一些示例：

```sql
SELECT 'abc' SIMILAR TO 'abc';       -- true
SELECT 'abc' SIMILAR TO 'a';         -- false
SELECT 'abc' SIMILAR TO '.*(b|d).*'; -- true
SELECT 'abc' SIMILAR TO '(b|c).*';   -- false
SELECT 'abc' NOT SIMILAR TO 'abc';   -- false
```

> 在 PostgreSQL 中，`~` 等同于 `SIMILAR TO`
> 且 `!~` 等同于 `NOT SIMILAR TO`。
> 在 DuckDB 中，这些等价关系目前并不成立，
> 详见 [PostgreSQL 兼容性页面]({% link docs/stable/sql/dialect/postgresql_compatibility.md %}).

## 通配符匹配

DuckDB 支持文件名展开，也称为通配符匹配，用于发现文件。
DuckDB 的通配符语法使用问号（`?`）通配符来匹配任何单个字符，使用星号（`*`）来匹配零个或多个字符。
此外，您可以使用方括号语法（`[...]`）来匹配括号内包含的任何单个字符，或括号内指定的字符范围。感叹号（`!`）可以在第一个括号内使用以搜索不包含在括号内的字符。
如需了解更多信息，请访问 [“glob (编程)” 维基百科页面](https://en.wikipedia.org/wiki/Glob_(programming))。

### `GLOB`

<div id="rrdiagram3"></div>

`GLOB` 运算符如果字符串匹配 `GLOB` 模式，将返回 `true` 或 `false`。`GLOB` 运算符最常用于搜索符合特定模式的文件名（例如特定的文件扩展名）。

一些示例：

```sql
SELECT 'best.txt' GLOB '*.txt';            -- true
SELECT 'best.txt' GLOB '????.txt';         -- true
SELECT 'best.txt' GLOB '?.txt';            -- false
SELECT 'best.txt' GLOB '[abc]est.txt';     -- true
SELECT 'best.txt' GLOB '[a-z]est.txt';     -- true
```

方括号语法是区分大小写的：

```sql
SELECT 'Best.txt' GLOB '[a-z]est.txt';     -- false
SELECT 'Best.txt' GLOB '[a-zA-Z]est.txt';  -- true
```

`!` 适用于方括号内的所有字符：

```sql
SELECT 'Best.txt' GLOB '[!a-zA-Z]est.txt'; -- false
```

要否定一个 `GLOB` 运算符，否定整个表达式：

```sql
SELECT NOT 'best.txt' GLOB '*.txt';        -- false
```

也可以使用三个波浪号（`~~~`）代替 `GLOB` 关键字。

| GLOB 风格 | 符号风格 |
| :--------- | :------------- |
| `GLOB`     | `~~~`          |

### 使用 Glob 函数查找文件名

`glob` 表函数还可以使用 glob 模式匹配语法来搜索文件名。
它接受一个参数：要搜索的路径（可能包含 glob 模式）。

搜索当前目录下的所有文件：

```sql
SELECT * FROM glob('*');
```

<div class="monospace_table"></div>

| file          |
| ------------- |
| duckdb.exe    |
| test.csv      |
| test.json     |
| test.parquet  |
| test2.csv     |
| test2.parquet |
| todos.json    |

### 通配符匹配语义

DuckDB 的通配符匹配实现遵循 [Python 的 `glob`](https://docs.python.org/3/library/glob.html) 的语义，而不是 shell 中使用的 `glob`。
一个显著的不同之处在于 `**/` 构造的行为：`**/⟨filename⟩`{:.language-sql .highlight} 不会返回在顶层目录中包含 `⟨filename⟩`{:.language-sql .highlight} 的文件。
例如，当目录中存在 `README.md` 文件时，以下查询可以找到它：

```sql
SELECT * FROM glob('README.md');
```

<div class="monospace_table"></div>

| file      |
| --------- |
| README.md |

然而，以下查询返回空结果：

```sql
SELECT * FROM glob('**/README.md');
```

与此同时，Bash、Zsh 等的 glob 匹配使用相同的语法找到文件：

```bash
ls **/README.md
```

```text
README.md
```

## 正则表达式

DuckDB 的正则表达式支持详见 [正则表达式页面]({% link docs/stable/sql/functions/regular_expressions.md %}).
DuckDB 支持一些 PostgreSQL 风格的正则表达式匹配运算符：

| PostgreSQL 风格 | 等效表达式                                                                                             |
| :--------------- | :------------------------------------------------------------------------------------------------------- |
| `~`              | [`regexp_full_match`]({% link docs/stable/sql/functions/text.md %}#regexp_full_matchstring-regex)       |
| `!~`             | `NOT` [`regexp_full_match`]({% link docs/stable/sql/functions/text.md %}#regexp_full_matchstring-regex) |
| `~*`             | (不支持)                                                                                          |
| `!~*`            | (不支持)                                                                                          |