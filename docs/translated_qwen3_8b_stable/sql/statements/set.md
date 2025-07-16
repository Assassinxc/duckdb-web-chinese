---
---
layout: docu
railroad: statements/set.js
redirect_from:
- /docs/sql/statements/set
title: SET 和 RESET 语句
---

`SET` 语句在指定的作用域中修改提供的 DuckDB 配置选项。

## 示例

更新 `memory_limit` 配置值：

```sql
SET memory_limit = '10GB';
```

配置系统使用 `1` 个线程：

```sql
SET threads = 1;
```

或者使用 `TO` 关键字：

```sql
SET threads TO 1;
```

将配置选项重置为默认值：

```sql
RESET threads;
```

检索配置值：

```sql
SELECT current_setting('threads');
```

全局设置默认排序顺序：

```sql
SET GLOBAL sort_order = 'desc';
```

为当前会话设置默认排序规则：

```sql
SET SESSION default_collation = 'nocase';
```

## 语法

<div id="rrdiagram1"></div>

`SET` 将 DuckDB 配置选项更新为提供的值。

## `RESET`

<div id="rrdiagram2"></div>

`RESET` 语句将给定的 DuckDB 配置选项重置为默认值。

## 作用域

配置选项可以具有不同的作用域：

* `GLOBAL`: 配置值在整个 DuckDB 实例中使用（或重置）。
* `SESSION`: 配置值仅在当前连接到 DuckDB 实例的会话中使用（或重置）。
* `LOCAL`: 尚未实现。

若未指定作用域，则使用配置选项的默认作用域。对于大多数选项，默认作用域是 `GLOBAL`。

## 配置

有关所有配置选项的完整列表，请参阅 [配置]({% link docs/stable/configuration/overview.md %}) 页面。