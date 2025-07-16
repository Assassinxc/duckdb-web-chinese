---
---
blurb: 一个时间实例表示一天中的时间（小时、分钟、秒、微秒）。
layout: docu
redirect_from:
- /docs/sql/data_types/time
title: 时间类型
---

`TIME` 和 `TIMETZ` 类型指定一天中的小时、分钟、秒和微秒。

| 名称     | 别名                  | 描述                     |
| :------- | :----------------------- | :------------------------------ |
| `TIME`   | `TIME WITHOUT TIME ZONE` | 一天中的时间（忽略时区） |
| `TIMETZ` | `TIME WITH TIME ZONE`    | 一天中的时间（使用时区）    |

可以使用类型名称作为关键字来创建实例，其中数据必须按照 ISO 8601 格式（`hh:mm:ss[.zzzzzz][+-TT[:tt]]`）进行格式化。

```sql
SELECT TIME '1992-09-20 11:30:00.123456';
```

```text
11:30:00.123456
```

```sql
SELECT TIMETZ '1992-09-20 11:30:00.123456';
```

```text
11:30:00.123456+00
```

```sql
SELECT TIMETZ '1992-09-20 11:30:00.123456-02:00';
```

```text
13:30:00.123456+00
```

```sql
SELECT TIMETZ '1992-09-20 11:30:00.123456+05:30';
```

```text
06:00:00.123456+00
```

> 警告 `TIME` 类型应仅在罕见情况下使用，当时间戳的日期部分可以忽略时。
> 大多数应用程序应使用 [`TIMESTAMP` 类型]({% link docs/stable/sql/data_types/timestamp.md %}) 来表示其时间戳。