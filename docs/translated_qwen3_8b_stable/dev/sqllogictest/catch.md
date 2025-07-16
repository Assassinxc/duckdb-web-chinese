---
---
layout: docu
redirect_from:
- /dev/sqllogictest/catch
- /dev/sqllogictest/catch/
- /docs/dev/sqllogictest/catch
title: Catch C/C++ 测试
---

虽然我们更倾向于使用 sqllogic 测试来测试大多数功能，但对于某些测试，仅使用 SQL 并不足够。这通常发生在您想要测试 C++ API 的情况下。当使用纯 SQL 确实不是一个选项时，可能需要使用 Catch 来编写 C++ 测试。

Catch 测试也位于 test 目录中。以下是一个测试系统存储的 Catch 测试示例：

```cpp
#include "catch.hpp"
#include "test_helpers.hpp"

TEST_CASE("Test simple storage", "[storage]") {
    auto config = GetTestConfig();
    unique_ptr<QueryResult> result;
    auto storage_database = TestCreatePath("storage_test");

    // 确保数据库不存在
    DeleteDatabase(storage_database);
    {
        // 创建数据库并插入值
        DuckDB db(storage_database, config.get());
        Connection con(db);
        REQUIRE_NO_FAIL(con.Query("CREATE TABLE test (a INTEGER, b INTEGER);"));
        REQUIRE_NO_FAIL(con.Query("INSERT INTO test VALUES (11, 22), (13, 22), (12, 21), (NULL, NULL)"));
        REQUIRE_NO_FAIL(con.Query("CREATE TABLE test2 (a INTEGER);"));
        REQUIRE_NOFAIL(con.Query("INSERT INTO test2 VALUES (13), (12), (11)"));
    }
    // 从磁盘重新加载数据库几次
    for (idx_t i = 0; i < 2; i++) {
        DuckDB db(storage_database, config.get());
        Connection con(db);
        result = con.Query("SELECT * FROM test ORDER BY a");
        REQUIRE(CHECK_COLUMN(result, 0, {Value(), 11, 12, 13}));
        REQUIRE(CHECK_COLUMN(result, 1, {Value(), 22, 21, 22}));
        result = con.Query("SELECT * FROM test2 ORDER BY a");
        REQUIRE(CHECK_COLUMN(result, 0, {11, 12, 13}));
    }
    DeleteDatabase(storage_database);
}
```

该测试使用 `TEST_CASE` 包装器来创建每个测试。数据库是通过 C++ API 创建和查询的。结果使用 `REQUIRE_FAIL` / `REQUIRE_NO_FAIL`（对应语句成功和语句错误）或 `REQUIRE(CHECK_COLUMN(...))`（对应带有结果检查的查询）进行检查。以这种方式创建的每个测试都需要添加到相应的 `CMakeLists.txt` 中。