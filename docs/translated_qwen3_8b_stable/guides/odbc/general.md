---
---
layout: docu
redirect_from:
- /docs/guides/odbc/general
title: 'ODBC 101: 以鸭子为主题的ODBC指南'
---

## 什么是ODBC？

[ODBC](https://learn.microsoft.com/en-us/sql/odbc/microsoft-open-database-connectivity-odbc?view=sql-server-ver16) 是开放数据库连接（Open Database Connectivity）的缩写，是一种标准，允许不同的程序与不同的数据库进行通信，包括当然的DuckDB。这使得构建能够与多种不同数据库协同工作的程序变得更加容易，这节省了开发人员的时间，因为开发人员无需为每个数据库编写定制代码。相反，他们可以使用标准化的ODBC接口，这减少了开发时间和成本，并且程序更容易维护。然而，ODBC可能比使用原生驱动程序等其他数据库连接方法更慢，因为它在应用程序和数据库之间添加了一个额外的抽象层。此外，由于DuckDB是基于列的，而ODBC是基于行的，所以在使用ODBC与DuckDB时可能会有一些效率低下。

> 本页面中包含指向官方 [Microsoft ODBC文档](https://learn.microsoft.com/en-us/sql/odbc/reference/odbc-programmer-s-reference?view=sql-server-ver16) 的链接，这是学习更多ODBC知识的宝贵资源。

## 常见概念

* [句柄](#handles)
* [连接](#connecting)
* [错误处理和诊断](#error-handling-and-diagnostics)
* [缓冲区和绑定](#buffers-and-binding)

### 句柄

[句柄](https://learn.microsoft.com/en-us/sql/odbc/reference/develop-app/handles?view=sql-server-ver16) 是指向特定ODBC对象的指针，用于与数据库进行交互。有几种不同类型的句柄，每种都有不同的用途，它们是环境句柄、连接句柄、语句句柄和描述符句柄。句柄通过 [`SQLAllocHandle`](https://learn.microsoft.com/en-us/sql/odbc/reference/syntax/sqlallochandle-function?view=sql-server-ver16) 进行分配，该函数接受要分配的句柄类型和指向句柄的指针，驱动程序然后创建指定类型的句柄并将其返回给应用程序。

DuckDB ODBC驱动程序有以下句柄类型。

#### 环境

<div class="nostroke_table"></div>

| **句柄名称** | [环境](https://learn.microsoft.com/en-us/sql/odbc/reference/develop-app/environment-handles?view=sql-server-ver16) |
| **类型名称** | `SQL_HANDLE_ENV` |
| **描述** | 管理ODBC操作的环境设置，并提供一个全局上下文以访问数据。 |
| **使用场景** | 初始化ODBC、管理驱动程序行为、资源分配 |
| **附加信息** | 必须在应用程序启动时为每个应用程序分配一次，并在结束时释放。 |

#### 连接

<div class="nostroke_table"></div>

| **句柄名称** | [连接](https://learn.microsoft.com/en-us/sql/odbc/reference/develop-app/connection-handles?view=sql-server-ver16) |
| **类型名称** | `SQL_HANDLE_DBC` |
| **描述** | 表示与数据源的连接。用于建立、管理和终止连接。定义在驱动程序中使用的驱动程序和数据源。 |
| **使用场景** | 建立与数据库的连接、管理连接状态 |
| **附加信息** | 可以根据需要创建多个连接句柄 [https://learn.microsoft.com/en-us/sql/odbc/reference/develop-app/allocating-a-connection-handle-odbc?view=sql-server-ver16](https://learn.microsoft.com/en-us/sql/odbc/reference/develop-app/allocating-a-connection-handle-odbc?view=sql-server-ver16)，允许同时连接多个数据源。 *注意*：分配连接句柄不会建立连接，但必须先分配，然后在连接建立后使用。 |

#### 语句

<div class="nostroke_table"></div>

| **句柄名称** | [语句](https://learn.microsoft.com/en-us/sql/odbc/reference/develop-app/statement-handles?view=sql-server-ver16)
| **类型名称** | `SQL_HANDLE_STMT`
| **描述** | 处理SQL语句的执行以及返回的结果集。
| **使用场景** | 执行SQL查询、获取结果集、管理语句选项。
| **附加信息** | 为了便于并发查询的执行，每个连接可以分配多个句柄 [https://learn.microsoft.com/en-us/sql/odbc/reference/develop-app/allocating-a-statement-handle-odbc?view=sql-server-ver16](https://learn.microsoft.com/en-us/sql/odbc/reference/develop-app/allocating-a-statement-handle-odbc?view=sql-server-ver16)。

#### 描述符

<div class="nostroke_table"></div>

| **句柄名称** | [描述符](https://learn.microsoft.com/en-us/sql/odbc/reference/develop-app/descriptor-handles?view=sql-server-ver16)
| **类型名称** | `SQL_HANDLE_DESC`
| **描述** | 描述数据结构或参数的属性，并允许应用程序指定要绑定/检索的数据结构。
| **使用场景** | 描述表结构、结果集、将列绑定到应用程序缓冲区
| **附加信息** | 在需要显式定义数据结构的情况下使用，例如在参数绑定或结果集获取过程中。它们在语句分配时自动分配，也可以显式分配。

### 连接

第一步是连接到数据源，以便应用程序可以执行数据库操作。首先，应用程序必须分配一个环境句柄，然后分配一个连接句柄。然后使用连接句柄连接到数据源。有两项功能可用于连接到数据源， [`SQLDriverConnect`](https://learn.microsoft.com/en-us/sql/odbc/reference/syntax/sqldriverconnect-function?view=sql-server-ver16) 和 [`SQLConnect`](https://learn.microsoft.com/en-us/sql/odbc/reference/syntax/sqlconnect-function?view=sql-server-ver16)。前者用于使用连接字符串连接到数据源，后者用于使用DSN连接到数据源。

#### 连接字符串

[连接字符串](https://learn.microsoft.com/en-us/sql/odbc/reference/develop-app/connection-strings?view=sql-server-ver16) 是一个包含连接到数据源所需信息的字符串。它被格式化为分号分隔的关键值对列表，然而DuckDB目前只使用DSN并忽略其余参数。

#### DSN

DSN（数据源名称）是一个标识数据库的字符串。它可以是一个文件路径、URL或数据库名称。例如：`C:\Users\me\duckdb.db` 和 `DuckDB` 都是有效的DSN。有关DSN的更多信息，可以在 [SQL Server文档的“选择数据源或驱动程序”页面](https://learn.microsoft.com/en-us/sql/odbc/reference/develop-app/choosing-a-data-source-or-driver?view=sql-server-ver16) 找到。

### 错误处理和诊断

ODBC中的所有函数都返回一个代码，表示函数的成功或失败。这允许进行简单的错误处理，因为应用程序只需检查每个函数调用的返回代码以确定是否成功。当失败时，应用程序可以使用 [`SQLGetDiagRec`](https://learn.microsoft.com/en-us/sql/odbc/reference/syntax/sqlgetdiagrec-function?view=sql-server-ver16) 函数来检索错误信息。以下表格定义了 [返回代码](https://learn.microsoft.com/en-us/sql/odbc/reference/develop-app/return-codes-odbc?view=sql-server-ver16):

| 返回代码             | 描述                                        |
|-------------------------|----------------------------------------------------|
| `SQL_SUCCESS`           | 函数成功完成                                                                                                           |
| `SQL_SUCCESS_WITH_INFO` | 函数成功完成，但有额外的信息，包括警告                                              |
| `SQL_ERROR`             | 函数失败                                                                                                                           |
| `SQL_INVALID_HANDLE`    | 提供的句柄无效，表示编程错误，即句柄在使用前未分配或类型错误 |
| `SQL_NO_DATA`           | 函数成功完成，但没有更多可用数据                                                                             |
| `SQL_NEED_DATA`         | 需要更多数据，例如在执行时发送参数数据或需要额外的连接信息                |
| `SQL_STILL_EXECUTING`   | 异步执行的函数仍在执行                                                                                |

### 缓冲区和绑定

缓冲区是用于存储数据的内存块。缓冲区用于存储从数据库检索的数据，或发送到数据库的数据。缓冲区由应用程序分配，并使用 [`SQLBindCol`](https://learn.microsoft.com/en-us/sql/odbc/reference/syntax/sqlbindcol-function?view=sql-server-ver16) 和 [`SQLBindParameter`](https://learn.microsoft.com/en-us/sql/odbc/reference/syntax/sqlbindparameter-function?view=sql-server-ver16) 函数绑定到结果集中的列或查询中的参数。当应用程序从结果集中获取一行或执行查询时，数据存储在缓冲区中。当应用程序将查询发送到数据库时，缓冲区中的数据发送到数据库。

## 设置应用程序

以下是一个逐步指南，用于设置使用ODBC连接到数据库、执行查询并获取结果的C++应用程序。

> 要安装驱动程序以及您需要的其他内容，请按照这些 [指令]({% link docs/stable/clients/odbc/overview.md %}).

### 1. 包含SQL头文件

第一步是包含SQL头文件：

```cpp
#include <sql.h>
#include <sqlext.h>
```

这些文件包含ODBC函数的定义以及ODBC使用的数据类型。为了能够使用这些头文件，您必须安装`unixodbc`包：

在macOS上：

```bash
brew install unixodbc
```

在Ubuntu和Debian上：

```bash
sudo apt-get install -y unixodbc-dev
```

在Fedora、CentOS和Red Hat上：

```bash
sudo yum install -y unixODBC-devel
```

请记得在您的`CFLAGS`中包含头文件的位置。

对于`MAKEFILE`：

```make
CFLAGS=-I/usr/local/include
# 或
CFLAGS=-/opt/homebrew/Cellar/unixodbc/2.3.11/include
```

对于`CMAKE`：

```cmake
include_directories(/usr/local/include)
# 或
include_directories(/opt/homebrew/Cellar/unixodbc/2.3.11/include)
```

您还需要在您的`CMAKE`或`MAKEFILE`中链接库。
对于`CMAKE`：

```cmake
target_link_libraries(ODBC_application /path/to/duckdb_odbc/libduckdb_odbc.dylib)
```

对于`MAKEFILE`：

```make
LDLIBS=-L/path/to/duckdb_odbc/libduckdb_odbc.dylib
```

### 2. 定义ODBC句柄并连接到数据库

#### 2.a. 使用SQLConnect连接

然后设置ODBC句柄，分配它们，并连接到数据库。首先分配环境句柄，然后将环境设置为ODBC版本3，然后分配连接句柄，最后连接到数据库。以下代码片段展示了如何做到这一点：

```cpp
SQLHANDLE env;
SQLHANDLE dbc;

SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, &env);

SQLSetEnvAttr(env, SQL_ATTR_ODBC_VERSION, (void*)SQL_OV_ODBC3, 0);

SQLAllocHandle(SQL_HANDLE_DBC, env, &dbc);

std::string dsn = "DSN=duckdbmemory";
SQLConnect(dbc, (SQLCHAR*)dsn.c_str(), SQL_NTS, NULL, 0, NULL, 0);

std::cout << "Connected!" << std::endl;
```

#### 2.b. 使用SQLDriverConnect连接

或者，您可以使用 [`SQLDriverConnect`](https://learn.microsoft.com/en-us/sql/odbc/reference/syntax/sqldriverconnect-function?view=sql-server-ver16) 连接到ODBC驱动程序。
`SQLDriverConnect` 接受一个连接字符串，在其中您可以使用任何可用的 [DuckDB配置选项]({% link docs/stable/configuration/overview.md %}) 来配置数据库。

```cpp
SQLHANDLE env;
SQLHANDLE dbc;

SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, &env);

SQLSetEnvAttr(env, SQL_ATTR_ODBC_VERSION, (void*)SQL_OV_ODBC3, 0);

SQLAllocHandle(SQL_HANDLE_DBC, env, &dbc);

SQLCHAR str[1024];
SQLSMALLINT strl;
std::string dsn = "DSN=DuckDB;access_mode=READ_ONLY"
SQLDriverConnect(dbc, nullptr, (SQLCHAR*)dsn.c_str(), SQL_NTS, str, sizeof(str), &strl, SQL_DRIVER_COMPLETE)

std::cout << "Connected!" << std::endl;
```

### 3. 添加查询

现在应用程序已经设置好了，我们可以向其中添加一个查询。首先，我们需要分配一个语句句柄：

```cpp
SQLHANDLE stmt;
SQLAllocHandle(SQL_HANDLE_STMT, dbc, &stmt);
```

然后我们就可以执行一个查询：

```cpp
SQLExecDirect(stmt, (SQLCHAR*)"SELECT * FROM integers", SQL_NTS);
```

### 4. 获取结果

现在我们已经执行了查询，可以获取结果。首先，我们需要将结果集中的列绑定到缓冲区：

```cpp
SQLLEN int_val;
SQLLEN null_val;
SQLBindCol(stmt, 1, SQL_C_SLONG, &int_val, 0, &null_val);
```

然后我们就可以获取结果：

```cpp
SQLFetch(stmt);
```

### 5. 自由发挥

现在我们有了结果，可以对它们做任何想做的事情。例如，我们可以打印它们：

```cpp
std::cout << "Value: " << int_val << std::endl;
```

或者做任何其他处理。此外，还可以执行更多查询，并做任何想对数据库进行的操作，比如插入、更新或删除数据。

### 6. 释放句柄并断开连接

最后，我们需要释放句柄并断开与数据库的连接。首先，我们需要释放语句句柄：

```cpp
SQLFreeHandle(SQL_HANDLE_STMT, stmt);
```

然后我们需要断开与数据库的连接：

```cpp
SQLDisconnect(dbc);
```

最后，我们需要释放连接句柄和环境句柄：

```cpp
SQLFreeHandle(SQL_HANDLE_DBC, dbc);
SQLFreeHandle(SQL_HANDLE_ENV, env);
```

释放连接和环境句柄只能在断开与数据库的连接之后进行。在断开连接之前尝试释放它们会导致错误。

## 示例应用程序

以下是一个示例应用程序，它包含一个`.cpp`文件，该文件连接到数据库、执行查询、获取结果并打印它们。它还断开与数据库的连接并释放句柄，还包含一个用于检查ODBC函数返回值的函数。此外，它还包含一个`CMakeLists.txt`文件，可用于构建应用程序。

### 示例 `.cpp` 文件

```cpp
#include <iostream>
#include <sql.h>
#include <sqlext.h>

void check_ret(SQLRETURN ret, std::string msg) {
    if (ret != SQL_SUCCESS && ret != SQL_SUCCESS_WITH_INFO) {
        std::cout << ret << ": " << msg << " failed" << std::endl;
        exit(1);
    }
    if (ret == SQL_SUCCESS_WITH_INFO) {
        std::cout << ret << ": " << msg << " succeeded with info" << std::endl;
    }
}

int main() {
    SQLHANDLE env;
    SQLHANDLE dbc;
    SQLRETURN ret;

    ret = SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, &env);
    check_ret(ret, "SQLAllocHandle(env)");

    ret = SQLSetEnvAttr(env, SQL_ATTR_ODBC_VERSION, (void*)SQL_OV_ODBC3, 0);
    check_ret(ret, "SQLSetEnvAttr");

    ret = SQLAllocHandle(SQL_HANDLE_DBC, env, &dbc);
    check_ret(ret, "SQLAllocHandle(dbc)");

    std::string dsn = "DSN=duckdbmemory";
    ret = SQLConnect(dbc, (SQLCHAR*)dsn.c_str(), SQL_NTS, NULL, 0, NULL, 0);
    check_ret(ret, "SQLConnect");

    std::cout << "Connected!" << std::endl;

    SQLHANDLE stmt;
    ret = SQLAllocHandle(SQL_HANDLE_STMT, dbc, &stmt);
    check_ret(ret, "SQLAllocHandle(stmt)");

    ret = SQLExecDirect(stmt, (SQLCHAR*)"SELECT * FROM integers", SQL_NTS);
    check_ret(ret, "SQLExecDirect(SELECT * FROM integers)");

    SQLLEN int_val;
    SQLLEN null_val;
    ret = SQLBindCol(stmt, 1, SQL_C_SLONG, &int_val, 0, &null
    check_ret(ret, "SQLBindCol");

    ret = SQLFetch(stmt);
    check_ret(ret, "SQLFetch");

    std::cout << "Value: " << int_val << std::endl;

    ret = SQLFreeHandle(SQL_HANDLE_STMT, stmt);
    check_ret(ret, "SQLFreeHandle(stmt)");

    ret = SQLDisconnect(dbc);
    check_ret(ret, "SQLDisconnect");

    ret = SQLFreeHandle(SQL_HANDLE_DBC, dbc);
    check_ret(ret, "SQLFreeHandle(dbc)");

    ret = SQLFreeHandle(SQL_HANDLE_ENV, env);
    check_ret(ret, "SQLFreeHandle(env)");
}
```

### 示例 `CMakeLists.txt` 文件

```cmake
cmake_minimum_required(VERSION 3.25)
project(ODBC_Tester_App)

set(CMAKE_CXX_STANDARD 17)
include_directories(/opt/homebrew/Cellar/unixodbc/2.3.11/include)

add_executable(ODBC_Tester_App main.cpp)
target_link_libraries(ODBC_Tester_App /duckdb_odbc/libduckdb_odbc.dylib)
```