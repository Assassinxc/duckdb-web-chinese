---
---
layout: docu
redirect_from:
- /docs/guides/meta/describe
title: Describe
---

## 描述一个表

为了查看表的模式，可以使用 `DESCRIBE` 语句（或其别名 `DESC` 和 `SHOW`），后面跟上表名。

```sql
CREATE TABLE tbl (i INTEGER PRIMARY KEY, j VARCHAR);
DESCRIBE tbl;
SHOW tbl; -- 等同于 DESCRIBE tbl;
```

| column_name | column_type | null | key  | default | extra |
|-------------|-------------|------|------|---------|-------|
| i           | INTEGER     | NO   | PRI  | NULL    | NULL  |
| j           | VARCHAR     | YES  | NULL | NULL    | NULL  |

## 描述一个查询

为了查看查询结果的模式，可以在查询前加上 `DESCRIBE`。

```sql
DESCRIBE SELECT * FROM tbl;
```

| column_name | column_type | null | key  | default | extra |
|-------------|-------------|------|------|---------|-------|
| i           | INTEGER     | YES  | NULL | NULL    | NULL  |
| j           | VARCHAR     | YES  | NULL | NULL    | NULL  |

请注意，存在一些细微差别：与[描述一个表](#describing-a-table)的结果相比，可空性（`null`）和键信息（`key`）会丢失。

## 在子查询中使用 `DESCRIBE`

`DESCRIBE` 可以用作子查询。这允许根据描述创建表，例如：

```sql
CREATE TABLE tbl_description AS SELECT * FROM (DESCRIBE tbl);
```

## 描述远程表

可以通过 [`httpfs` 扩展]({% link docs/stable/core_extensions/httpfs/overview.md %}) 使用 `DESCRIBE TABLE` 语句来描述远程表。例如：

```sql
DESCRIBE TABLE 'https://blobs.duckdb.org/data/Star_Trek-Season_1.csv';
```

|               column_name               | column_type | null | key  | default | extra |
|-----------------------------------------|-------------|------|------|---------|-------|
| season_num                              | BIGINT      | YES  | NULL | NULL    | NULL  |
| episode_num                             | BIGINT      | YES  | NULL | NULL    | NULL  |
| aired_date                              | DATE        | YES  | NULL | NULL    | NULL  |
| cnt_kirk_hookups                        | BIGINT      | YES  | NULL | NULL    | NULL  |
| cnt_downed_redshirts                    | BIGINT      | YES  | NULL | NULL    | NULL  |
| bool_aliens_almost_took_over_planet     | BIGINT      | YES  | NULL | NULL    | NULL  |
| bool_aliens_almost_took_over_enterprise | BIGINT      | YES  | NULL | NULL    | NULL  |
| cnt_vulcan_nerve_pinch                  | BIGINT      | YES  | NULL | NULL    | NULL  |
| cnt_warp_speed_orders                   | BIGINT      | YES  | NULL | NULL    | NULL  |
| highest_warp_speed_issued               | BIGINT      | YES  | NULL | NULL    | NULL  |
| bool_hand_phasers_fired                 | BIGINT      | YES  | NULL | NULL    | NULL  |
| bool_ship_phasers_fired                 | BIGINT      | YES  | NULL | NULL    | NULL  |
| bool_ship_photon_torpedos_fired         | BIGINT      | YES  | NULL | NULL    | NULL  |
| cnt_transporter_pax                     | BIGINT      | YES  | NULL | NULL    | NULL  |
| cnt_damn_it_jim_quote                   | BIGINT      | YES  | NULL | NULL    | NULL  |
| cnt_im_givin_her_all_shes_got_quote     | BIGINT      | YES  | NULL | NULL    | NULL  |
| cnt_highly_illogical_quote              | BIGINT      | YES  | NULL | NULL    | NULL  |
| bool_enterprise_saved_the_day           | BIGINT      | YES  | NULL | NULL    | NULL  |