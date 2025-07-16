---
---
layout: docu
title: Lambda 函数
---

> DuckDB 1.3.0 已弃用旧的 lambda 单箭头语法 (`x -> x + 1`)，并采用 Python 风格的语法 (`lambda x : x + 1`)。
>
> DuckDB 1.3.0 还引入了一个新设置来配置 lambda 语法。
>
> ```sql
> SET lambda_syntax = 'DEFAULT';
> SET lambda_syntax = 'ENABLE_SINGLE_ARROW';
> SET lambda_syntax = 'DISABLE_SINGLE_ARROW';
> ```
>
> 当前，`DEFAULT` 启用两种语法风格，即旧的单箭头语法和 Python 风格语法。
>
> DuckDB 1.4.0 将是最后一个在未显式启用的情况下支持单箭头语法的版本。
>
> DuckDB 1.5.0 默认禁用单箭头语法。
>
> DuckDB 1.6.0 移除了 `lambda_syntax` 标志并完全弃用了单箭头语法，因此旧的行为将不再可能。

Lambda 函数使查询中可以使用更复杂和灵活的表达式。
DuckDB 支持多个标量函数，这些函数作用于 [`LIST`s]({% link docs/preview/sql/data_types/list.md %}) 并接受 lambda 函数作为参数，形式为 `lambda ⟨parameter1⟩, ⟨parameter2⟩, ... : ⟨expression⟩`{:.language-sql .highlight}。
如果 lambda 函数只有一个参数，则可以省略括号。
参数可以有任意名称。
例如，以下都是有效的 lambda 函数：

* `lambda param : param > 1`{:.language-sql .highlight}
* `lambda s : contains(concat(s, 'DB'), 'duck')`{:.language-sql .highlight}
* `lambda acc, x : acc + x`{:.language-sql .highlight}

## 接受 Lambda 函数的标量函数

| 名称 | 描述 |
|:--|:-------|
| [`list_transform(list, lambda(x))`](#list_transformlist-lambdax) | 返回一个列表，该列表是将 lambda 函数应用于输入列表的每个元素的结果。返回类型由 lambda 函数的返回类型定义。请参见 [`list_transform` 示例](#list_transform-examples)。 |
| [`list_filter(list, lambda(x))`](#list_filterlist-lambdax) | 从输入列表中构造一个列表，其中包含 lambda 函数返回 `true` 的元素。DuckDB 必须能够将 lambda 函数的返回类型转换为 `BOOL`。`list_filter` 的返回类型与输入列表相同。请参见 [`list_filter` 示例](#list_filter-examples)。 |
| [`list_reduce(list, lambda(x, y)[, initial_value]`](#list_reducelist-lambdax-y-initial_value) | 通过将 lambda 函数应用于运行结果和下一个列表元素，将输入列表的所有元素减少为一个标量值。lambda 函数有一个可选的 `initial_value` 参数。请参见 [`list_reduce` 示例](#list_reduce-examples) 或详细信息。 |

### `list_transform(list, lambda(x))`

<div class="nostroke_table"></div>

| **描述** | 返回一个列表，该列表是将 lambda 函数应用于输入列表的每个元素的结果。返回类型由 lambda 函数的返回类型定义。请参见 [`list_transform` 示例](#list_transform-examples)。 |
| **示例** | `list_transform([4, 5, 6], lambda x : x + 1)`{:.language-sql .highlight} |
| **结果** | `[5, 6, 7]` |
| **别名** | `array_transform`, `apply`, `list_apply`, `array_apply` |

### `list_filter(list, lambda(x))`

<div class="nostroke_table"></div>

| **描述** | 从输入列表中构造一个列表，其中包含 lambda 函数返回 `true` 的元素。DuckDB 必须能够将 lambda 函数的返回类型转换为 `BOOL`。`list_filter` 的返回类型与输入列表相同。请参见 [`list_filter` 示例](#list_filter-examples)。 |
| **示例** | `list_filter([4, 5, 6], lambda x : x > 4)`{:.language-sql .highlight} |
| **结果** | `[5, 6]` |
| **别名** | `array_filter`, `filter` |

### `list_reduce(list, lambda(x, y)[, initial_value]`

<div class="nostroke_table"></div>

| **描述** | 通过将 lambda 函数应用于运行结果和下一个列表元素，将输入列表的所有元素减少为一个标量值。lambda 函数有一个可选的 `initial_value` 参数。请参见 [`list_reduce` 示例](#list_reduce-examples) 或详细信息。 |
| **示例** | `list_reduce([1, 2, 3], lambda x, y : x + y, 100)`{:.language-sql .highlight} |
| **结果** | `106` |
| **别名** | `array_reduce`, `reduce` |

## 嵌套 Lambda 函数

所有标量函数都可以任意嵌套。例如，嵌套 lambda 函数以获取列表中所有偶数元素的平方：

```sql
SELECT list_transform(
        list_filter([0, 1, 2, 3, 4, 5], lambda x: x % 2 = 0),
        lambda y: y * y
    );
```

```text
[0, 4, 16]
```

嵌套 lambda 函数将第一个列表的每个元素与第二个列表的总和相加：

```sql
SELECT list_transform(
        [1, 2, 3],
        lambda x :
            list_reduce([4, 5, 6], lambda a, b: a + b) + x
    );
```

```text
[16, 17, 18]
```

## 作用域

Lambda 函数遵循以下顺序的作用域规则：

* 内部 lambda 参数
* 外部 lambda 参数
* 列名
* 宏参数

```sql
CREATE TABLE tbl (x INTEGER);
INSERT INTO tbl VALUES (10);
SELECT list_apply(
            [1, 2],
            lambda x: list_apply([4], lambda x: x + tbl.x)[1] + x
    )
FROM tbl;
```

```text
[15, 16]
```

## 索引作为参数

所有 lambda 函数都接受一个可选的额外参数，该参数表示当前元素的索引。
这总是 lambda 函数的最后一个参数（例如 `(x, i)` 中的 `i`），并且是 1 基的（即第一个元素的索引为 1）。

获取所有大于其索引的元素：

```sql
SELECT list_filter([1, 3, 1, 5], lambda x, i: x > i);
```

```text
[3, 5]
```

## 示例

### `list_transform` 示例

将每个列表元素加一：

```sql
SELECT list_transform([1, 2, NULL, 3], lambda x: x + 1);
```

```text
[2, 3, NULL, 4]
```

转换字符串：

```sql
SELECT list_transform(['Duck', 'Goose', 'Sparrow'], lambda s: concat(s, 'DB'));
```

```text
[DuckDB, GooseDB, SparrowDB]
```

将 lambda 函数与其他函数结合使用：

```sql
SELECT list_transform([5, NULL, 6], lambda x: coalesce(x, 0) + 1);
```

```text
[6, 1, 7]
```

### `list_filter` 示例

过滤掉负值：

```sql
SELECT list_filter([5, -6, NULL, 7], lambda x: x > 0);
```

```text
[5, 7]
```

能被 2 和 5 整除：

```sql
SELECT list_filter(
        list_filter([2, 4, 3, 1, 20, 10, 3, 30], lambda x: x % 2 = 0),
        lambda y: y % 5 = 0
    );
```

```text
[20, 10, 30]
```

与 `range(...)` 结合以构造列表：

```sql
SELECT list_filter([1, 2, 3, 4], lambda x: x > #1) FROM range(4);
```

```text
[1, 2, 3, 4]
[2, 3, 4]
[3, 4]
[4]
```

### `list_reduce` 示例

所有列表元素的总和：

```sql
SELECT list_reduce([1, 2, 3, 4], lambda acc, x: acc + x);
```

```text
10
```

只有当列表元素大于 2 时才进行加法：

```sql
SELECT list_reduce(
        list_filter([1, 2, 3, 4], lambda x: x > 2),
        lambda acc, x: acc + x
    );
```

```text
7
```

拼接所有列表元素：

```sql
SELECT list_reduce(['DuckDB', 'is', 'awesome'], lambda acc, x: concat(acc, ' ', x));
```

```text
DuckDB is awesome
```

不带初始值的索引拼接：

```sql
SELECT list_reduce(
        ['a', 'b', 'c', 'd'],
        lambda x, y, i: x || ' - ' || CAST(i AS VARCHAR) || ' - ' || y
    );
```

```text
a - 2 - b - 3 - c - 4 - d
```

带初始值的索引拼接：

```sql
SELECT list_reduce(
        ['a', 'b', 'c', 'd'],
        lambda x, y, i: x || ' - ' || CAST(i AS VARCHAR) || ' - ' || y, 'INITIAL'
    );
```

```text
INITIAL - 1 - a - 2 - b - 3 - c - 4 - d
```

## 局限性

目前不支持 lambda 表达式中的子查询。
例如：

```sql
SELECT list_apply([1, 2, 3], lambda x: (SELECT 42) + x);
```

```console
Binder 错误：
不支持 lambda 表达式中的子查询
```