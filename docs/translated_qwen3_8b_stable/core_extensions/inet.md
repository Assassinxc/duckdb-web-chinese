---
---
github_repository: https://github.com/duckdb/duckdb-inet
layout: docu
title: inet 扩展
redirect_from:
- /docs/stable/extensions/inet
- /docs/stable/extensions/inet/
- /docs/extensions/inet
- /docs/extensions/inet/
---

`inet` 扩展定义了 `INET` 数据类型，用于存储 [IPv4](https://en.wikipedia.org/wiki/Internet_Protocol_version_4) 和 [IPv6](https://en.wikipedia.org/wiki/IPv6) 网络地址。它支持 [CIDR 表示法](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing#CIDR_notation) 用于子网掩码（例如：`198.51.100.0/22`、`2001:db8:3c4d::/48`）。

## 安装和加载

`inet` 扩展会在首次使用时从官方扩展仓库中透明地[自动加载]({% link docs/stable/core_extensions/overview.md %}#autoloading-extensions)。
如果你想手动安装和加载它，请运行：

```sql
INSTALL inet;
LOAD inet;
```

## 示例

```sql
SELECT '127.0.0.1'::INET AS ipv4, '2001:db8:3c4d::/48'::INET AS ipv6;
```

|   ipv4    |        ipv6        |
|-----------|--------------------|
| 127.0.0.1 | 2001:db8:3c4d::/48 |

```sql
CREATE TABLE tbl (id INTEGER, ip INET);
INSERT INTO tbl VALUES
    (1, '192.168.0.0/16'),
    (2, '127.0.0.1'),
    (3, '8.8.8.8'),
    (4, 'fe80::/10'),
    (5, '2001:db8:3c4d:15::1a2f:1a2b');
SELECT * FROM tbl;
```

| id |             ip              |
|---:|-----------------------------|
| 1  | 192.168.0.0/16              |
| 2  | 127.0.0.1                   |
| 3  | 8.8.8.8                     |
| 4  | fe80::/10                   |
| 5  | 2001:db8:3c4d:15::1a2f:1a2b |

## 对 `INET` 值的操作

`INET` 值可以自然地进行比较，IPv4 会排在 IPv6 前面。此外，IP 地址可以通过加减整数进行修改。

```sql
CREATE TABLE tbl (cidr INET);
INSERT INTO tbl VALUES
    ('127.0.0.1'::INET + 10),
    ('fe80::10'::INET - 9),
    ('127.0.0.1'),
    ('2001:db8:3c4d:15::1a2f:1a2b');
SELECT cidr FROM tbl ORDER BY cidr ASC;
```

|            cidr             |
|-----------------------------|
| 127.0.0.1                   |
| 127.0.0.11                  |
| 2001:db8:3c4d:15::1a2f:1a2b |
| fe80::7                     |

## `host` 函数

可以使用 `HOST()` 函数提取 `INET` 值的主机部分。

```sql
CREATE TABLE tbl (cidr INET);
INSERT INTO tbl VALUES
    ('192.168.0.0/16'),
    ('127.0.0.1'),
    ('2001:db8:3c4d:15::1a2f:1a2b/96');
SELECT cidr, host(cidr) FROM tbl;
```

|              cidr              |         host(cidr)          |
|--------------------------------|-----------------------------|
| 192.168.0.0/16                 | 192.168.0.0                 |
| 127.0.0.1                      | 127.0.0.1                   |
| 2001:db8:3c4d:15::1a2f:1a2b/96 | 2001:db8:3c4d:15::1a2f:1a2b |

## `netmask` 函数

计算地址网络的网络掩码。

```sql
CREATE TABLE tbl (cidr INET);
INSERT INTO tbl VALUES
    ('192.168.1.5/24'),
    ('127.0.0.1'),
    ('2001:db8:3c4d:15::1a2f:1a2b/96');
SELECT cidr, netmask(cidr) FROM tbl;
```

|              cidr              |              netmask(cidr)         |
|--------------------------------|------------------------------------|
| 192.168.1.5/24                 | 255.255.255.0/24                   |
| 127.0.0.1                      | 255.255.255.255                    |
| 2001:db8:3c4d:15::1a2f:1a2b/96 | ffff:ffff:ffff:ffff:ffff:ffff::/96 |

## `network` 函数

返回地址的网络部分，将网络掩码右边的部分置零。

```sql
CREATE TABLE tbl (cidr INET);
INSERT INTO tbl VALUES
    ('192.168.1.5/24'),
    ('127.0.0.1'),
    ('2001:db8:3c4d:15::1a2f:1a2b/96');
SELECT cidr, network(cidr) FROM tbl;
```

|              cidr              |              network(cidr)         |
|--------------------------------|------------------------------------|
| 192.168.1.5/24                 | 192.168.1.0/24                     |
| 127.0.0.1                      | 255.255.255.255                    |
| 2001:db8:3c4d:15::1a2f:1a2b/96 | ffff:ffff:ffff:ffff:ffff:ffff::/96 |

## `broadcast` 函数

计算地址网络的广播地址。

```sql
CREATE TABLE tbl (cidr INET);
INSERT INTO tbl VALUES
    ('192.168.1.5/24'),
    ('127.0.0.1'),
    ('2001:db8:3c4d:15::1a2f:1a2b/96');
SELECT cidr, broadcast(cidr) FROM tbl;
```

|              cidr              |            broadcast(cidr)         |
|--------------------------------|------------------------------------|
| 192.168.1.5/24                 | 192.168.1.0/24                     |
| 127.0.0.1                      | 127.0.0.1                          |
| 2001:db8:3c4d:15::1a2f:1a2b/96 | 2001:db8:3c4d:15::/96              |

## `<<=` 运算符

子网是否被包含或等于子网？

```sql
CREATE TABLE tbl (cidr INET);
INSERT INTO tbl VALUES
    ('192.168.1.0/24'),
    ('127.0.0.1'),
    ('2001:db8:3c4d:15::1a2f:1a2b/96');
SELECT cidr, INET '192.168.1.5/32' <<= cidr FROM tbl;
```

|              cidr              | (CAST('192.168.1.5/32' AS INET) <<= cidr)   |
|--------------------------------|---------------------------------------------|
| 192.168.1.5/24                 | true                                        |
| 127.0.0.1                      | false                                       |
| 2001:db8:3c4d:15::1a2f:1a2b/96 | false                                       |

## `>>=` 运算符

子网是否包含或等于子网？

```sql
CREATE TABLE tbl (cidr INET);
INSERT INTO tbl VALUES
    ('192.168.1.0/24'),
    ('127.0.0.1'),
    ('2001:db8:3c4d:15::1a2f:1a2b/96');
SELECT cidr, INET '192.168.0.0/16' >>= cidr FROM tbl;
```

|              cidr              | (CAST('192.168.0.0/16' AS INET) >>= cidr)   |
|--------------------------------|---------------------------------------------|
| 192.168.1.5/24                 | true                                        |
| 127.0.0.1                      | false                                       |
| 2001:db8:3c4d:15::1a2f:1a2b/96 | false                                       |

## HTML 转义和反转义函数

```sql
SELECT html_escape('&');
```

```text
┌──────────────────┐
│ html_escape('&') │
│     varchar      │
├──────────────────┤
│ &amp;            │
└──────────────────┘
```

```sql
SELECT html_unescape('&amp;');
```

```text
┌────────────────────────┐
│ html_unescape('&amp;') │
│        varchar         │
├────────────────────────┤
│ &                      │
└────────────────────────┘
```