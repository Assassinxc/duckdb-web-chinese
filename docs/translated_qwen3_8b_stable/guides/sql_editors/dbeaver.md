---
---
layout: docu
redirect_from:
- /docs/guides/sql_editors/dbeaver
title: DBeaver SQL IDE
---

[DBeaver](https://dbeaver.io/) 是一款功能强大且受欢迎的桌面 SQL 编辑器和集成开发环境（IDE）。它同时拥有开源版和企业版。它对于可视化查看 DuckDB 中可用的表以及快速构建复杂查询非常有用。DuckDB 的 [JDBC 连接器](https://search.maven.org/artifact/org.duckdb/duckdb_jdbc) 允许 DBeaver 查询 DuckDB 文件，由此扩展，也可以查询任何 DuckDB 可以访问的文件（例如 [Parquet 文件]({% link docs/stable/guides/file_formats/query_parquet.md %})）。

## 安装 DBeaver

1. 通过其 [下载页面](https://dbeaver.io/download/) 上的下载链接和说明安装 DBeaver。

2. 打开 DBeaver 并创建一个新连接。您可以点击“新建数据库连接”按钮，或者在菜单栏中选择“数据库 > 新建数据库连接”。

    <img src="/images/guides/DBeaver_new_database_connection.png" alt="DBeaver 新建数据库连接" title="DBeaver 新建数据库连接"/>
    <img src="/images/guides/DBeaver_new_database_connection_menu.png" alt="DBeaver 新建数据库连接菜单" title="DBeaver 新建数据库连接菜单"/>

3. 搜索 DuckDB，选择它，然后点击下一步。

    <img src="/images/guides/DBeaver_select_database_driver.png" alt="DBeaver 选择数据库驱动" title="DBeaver 选择数据库驱动"/>

4. 输入或浏览到您想要查询的 DuckDB 数据库文件路径。如需使用内存中的 DuckDB（主要用于查询 Parquet 文件或测试），请输入 `:memory:` 作为路径。

    <img src="/images/guides/DBeaver_connection_settings_path.png" alt="DBeaver 设置路径" title="DBeaver 设置路径"/>

5. 点击“测试连接”。这将提示您安装 DuckDB JDBC 驱动程序。如果您没有收到提示，请参阅下方的替代驱动安装说明。

    <img src="/images/guides/DBeaver_connection_settings_test_connection.png" alt="DBeaver 测试连接" title="DBeaver 测试连接"/>

6. 点击“下载”从 Maven 下载 DuckDB 的 JDBC 驱动。下载完成后，点击“确定”，然后点击“完成”。
* 注意：如果您处于企业环境或防火墙后，请在点击下载前点击“下载配置”链接以配置代理设置。

    <img src="/images/guides/DBeaver_download_driver_files.png" alt="DBeaver 下载驱动文件" title="DBeaver 下载驱动文件"/>

7. 现在您应该在左侧的“数据库导航器”窗格中看到连接到您的 DuckDB 数据库的数据库连接。展开它以查看数据库中的表和视图。右键点击该连接并创建一个新的 SQL 脚本。

    <img src="/images/guides/DBeaver_new_sql_script.png" alt="DBeaver 新建 SQL 脚本" title="DBeaver 新建 SQL 脚本"/>

8. 编写一些 SQL 并点击“执行”按钮。

    <img src="/images/guides/DBeaver_execute_query.png" alt="DBeaver 执行查询" title="DBeaver 执行查询"/>

9. 现在您就可以使用 DuckDB 和 DBeaver 飞速前进啦！

    <img src="/images/guides/DBeaver_query_results.png" alt="DBeaver 查询结果" title="DBeaver 查询结果"/>

## 替代驱动安装

1. 如果在测试连接时未提示安装 DuckDB 驱动，请返回到“连接到数据库”对话框并点击“编辑驱动设置”。

    <img src="/images/guides/DBeaver_edit_driver_settings.png" alt="DBeaver 编辑驱动设置" title="DBeaver 编辑驱动设置"/>

2. （替代方法）您也可以返回到主 DBeaver 窗口，点击菜单栏中的“数据库 > 驱动管理器”以访问驱动设置菜单。然后选择 DuckDB，再点击“编辑”。

    <img src="/images/guides/DBeaver_driver_manager.png" alt="DBeaver 驱动管理器" title="DBeaver 驱动管理器"/>
    <img src="/images/guides/DBeaver_driver_manager_edit.png" alt="DBeaver 驱动管理器编辑" title="DBeaver 驱动管理器编辑"/>

3. 转到“库”选项卡，然后点击 DuckDB 驱动并点击“下载/更新”。如果没有看到 DuckDB 驱动，请先点击“重置为默认值”。

    <img src="/images/guides/DBeaver_edit_driver_duckdb.png" alt="DBeaver 编辑驱动" title="DBeaver 编辑驱动"/>

4. 点击“下载”从 Maven 下载 DuckDB 的 JDBC 驱动。下载完成后，点击“确定”，然后返回主 DBeaver 窗口并继续执行上述第 7 步。

    * 注意：如果您处于企业环境或防火墙后，请在点击下载前点击“下载配置”链接以配置代理设置。

    <img src="/images/guides/DBeaver_download_driver_files_from_driver_settings.png" alt="DBeaver 下载驱动文件 2" title="DBeaver 下载驱动文件 2" />