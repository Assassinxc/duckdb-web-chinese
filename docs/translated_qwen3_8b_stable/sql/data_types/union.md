---
---
layout: docu
redirect_from:
- /docs/sql/data_types/union
title: 联合类型
---

`UNION` *类型*（不要与 SQL [`UNION` 运算符]({% link docs/stable/sql/query_syntax/setops.md %}#union-all-by-name) 混淆）是一种嵌套类型，可以容纳多个“替代”值中的一个，类似于 C 语言中的 `union`。主要区别在于这些 `UNION` 类型是 *带标签的联合体*，因此始终携带一个“标签”（discriminator），以表明当前存储的是哪一个替代值，即使内部值本身为 null。因此，`UNION` 类型更类似于 C++17 的 `std::variant`、Rust 的 `Enum` 或大多数函数式语言中的“和类型”（sum type）。

`UNION` 类型必须始终至少包含一个成员，虽然它们可以包含多个相同类型的成员，但标签名称必须唯一。`UNION` 类型最多可以有 256 个成员。

在底层实现中，`UNION` 类型是基于 `STRUCT` 类型实现的，并且简单地将“标签”作为第一个条目保存。

`UNION` 值可以通过 [`union_value(tag := expr)`]({% link docs/stable/sql/functions/union.md %}) 函数或通过 [从成员类型转换](#casting-to-unions) 创建。

## 示例

创建一个包含 `UNION` 列的表：

```sql
CREATE TABLE tbl1 (u UNION(num INTEGER, str VARCHAR));
INSERT INTO tbl1 VALUES (1), ('two'), (union_value(str := 'three'));
```

任何类型都可以隐式转换为包含该类型的 `UNION`。如果源 `UNION` 成员是目标 `UNION` 的子集（如果转换无歧义），任何 `UNION` 也可以隐式转换为另一个 `UNION`。

当将 `UNION` 转换为 `VARCHAR` 时，`UNION` 会使用成员类型的 `VARCHAR` 转换函数：

```sql
SELECT u FROM tbl1;
```

|   u   |
|-------|
| 1     |
| two   |
| three |

选择所有 `str` 成员：

```sql
SELECT union_extract(u, 'str') AS str
FROM tbl1;
```

|  str  |
|-------|
| NULL  |
| two   |
| three |

或者，您可以使用类似于 [`STRUCT`s]({% link docs/stable/sql/data_types/struct.md %}) 的“点语法”。

```sql
SELECT u.str
FROM tbl1;
```

|  str  |
|-------|
| NULL  |
| two   |
| three |

从 `UNION` 中选择当前活动的标签作为 `ENUM`。

```sql
SELECT union_tag(u) AS t
FROM tbl1;
```

|  t  |
|-----|
| num |
| str |
| str |

## 联合转换

与其他嵌套类型相比，`UNION` 允许一组隐式转换，以在将其成员作为“子类型”使用时实现无缝且自然的使用。然而，这些转换设计时考虑了两个原则，以避免歧义，并避免可能导致信息丢失的转换。这防止了 `UNION` 完全“透明”，但仍允许 `UNION` 类型与其成员之间具有“超类型”关系。

因此，`UNION` 类型通常不能隐式转换为任何成员类型，因为其他成员中与目标类型不匹配的信息会“丢失”。如果您想要将 `UNION` 转换为其成员之一，应使用 `union_extract` 函数显式转换。

唯一的例外是将 `UNION` 转换为 `VARCHAR`，此时所有成员都会使用其对应的 `VARCHAR` 转换函数。由于任何类型都可以转换为 `VARCHAR`，因此这种转换在某种意义上是“安全”的。

### 转换为联合

如果一种类型可以隐式转换为 `UNION` 的成员类型之一，则该类型可以始终隐式转换为 `UNION`。

* 如果有多个候选类型，内置的隐式转换优先级规则将决定目标类型。例如，`FLOAT` → `UNION(i INTEGER, v VARCHAR)` 的转换会始终先将 `FLOAT` 转换为 `INTEGER` 成员，然后才是 `VARCHAR`。
* 如果转换仍然存在歧义，即有多个候选类型具有相同的隐式转换优先级，将引发错误。这通常发生在 `UNION` 包含多个相同类型的成员时，例如 `FLOAT` → `UNION(i INTEGER, num INTEGER)` 会始终存在歧义。

那么，如果我们想要创建一个包含多个相同类型成员的 `UNION`，如何消除歧义？通过使用 `union_value` 函数，该函数接受一个指定标签的关键词参数。例如，`union_value(num := 2::INTEGER)` 将创建一个包含一个类型为 `INTEGER`、标签为 `num` 的 `UNION`。这可以用于在显式（或隐式，详见下文）的 `UNION` 到 `UNION` 转换中消除歧义，例如 `CAST(union_value(b := 2) AS UNION(a INTEGER, b INTEGER))`。

### 联合之间的转换

如果源类型是目标类型的“子集”，`UNION` 类型之间可以进行转换。换句话说，源 `UNION` 中的所有标签必须在目标 `UNION` 中存在，并且所有匹配标签的类型必须可以在源和目标之间隐式转换。本质上，这意味着 `UNION` 类型对其成员是协变的。

| 是否允许 | 源类型                 | 目标类型                 | 说明                               |
|----------|------------------------|------------------------|------------------------------------|
| ✅       | `UNION(a A, b B)`      | `UNION(a A, b B, c C)` |                                    |
| ✅       | `UNION(a A, b B)`      | `UNION(a A, b C)`      | 如果 `B` 可以隐式转换为 `C`       |
| ❌       | `UNION(a A, b B, c C)` | `UNION(a A, b B)`      |                                    |
| ❌       | `UNION(a A, b B)`      | `UNION(a A, b C)`      | 如果 `B` 无法隐式转换为 `C`       |
| ❌       | `UNION(A, B, D)`       | `UNION(A, B, C)`       |                                    |

## 比较和排序

由于 `UNION` 类型在内部是基于 `STRUCT` 类型实现的，因此它们可以与所有比较运算符一起使用，并且可以在 `WHERE` 和 `HAVING` 子句中使用，与 [`STRUCT`s 的相同语义]({% link docs/stable/sql/data_types/struct.md %}#comparison-operators)。"标签" 始终作为第一个结构条目存储，这确保了 `UNION` 类型首先按照“标签”进行比较和排序。

## 函数

参见 [联合函数]({% link docs/stable/sql/functions/union.md %})。