---
---
layout: docu
redirect_from:
- /docs/guides/python/multiple_threads
title: 多线程 Python
---

本页演示了如何在多个 Python 线程中同时向 DuckDB 数据库进行插入和读取操作。
这在新数据持续流入且需要定期重新运行分析的场景中可能非常有用。
请注意，所有操作均在单个 Python 进程内进行（有关 DuckDB 并发性的详细信息，请参阅 [FAQ]({% link faq.md %})）。
您可以在此 [Google Colab 笔记本](https://colab.research.google.com/drive/190NB2m-LIfDcMamCY5lIzaD2OTMnYclB?usp=sharing) 中跟随操作。

## 设置

首先，导入 DuckDB 和 Python 标准库中的几个模块。
注意：如果使用 Pandas，请在脚本顶部添加 `import pandas`（因为必须在多线程之前导入）。
然后连接到一个基于文件的 DuckDB 数据库，并创建一个示例表以存储插入的数据。
此表将跟踪完成插入的线程名称，并使用 [`DEFAULT` 表达式]({% link docs/stable/sql/statements/create_table.md %}#syntax) 自动插入插入时间。

```python
import duckdb
from threading import Thread, current_thread
import random

duckdb_con = duckdb.connect('my_peristent_db.duckdb')
# 使用无参数连接创建内存数据库
# duckdb_con = duckdb.connect()
duckdb_con.execute("""
    CREATE OR REPLACE TABLE my_inserts (
        thread_name VARCHAR,
        insert_time TIMESTAMP DEFAULT current_timestamp
    )
""")
```

## 读取器和写入器函数

接下来，定义由写入线程和读取线程执行的函数。
每个线程必须使用 `.cursor()` 方法，基于原始连接创建线程本地的 DuckDB 连接。
这种方法也适用于内存中的 DuckDB 数据库。

```python
def write_from_thread(duckdb_con):
    # 为该线程创建一个 DuckDB 连接
    local_con = duckdb_con.cursor()
    # 插入一行，包含线程名称。insert_time 会自动生成。
    thread_name = str(current_thread().name)
    result = local_con.execute("""
        INSERT INTO my_inserts (thread_name)
        VALUES (?)
    """, (thread_name,)).fetchall()

def read_from_thread(duckdb_con):
    # 为该线程创建一个 DuckDB 连接
    local_con = duckdb_con.cursor()
    # 查询当前行数
    thread_name = str(current_thread().name)
    results = local_con.execute("""
        SELECT
            ? AS thread_name,
            count(*) AS row_counter,
            current_timestamp
        FROM my_inserts
    """, (thread_name,)).fetchall()
    print(results)
```

## 创建线程

我们定义要使用的写入器和读取器数量，并定义一个列表来跟踪将要创建的所有线程。
然后，创建第一个写入线程和读取线程。
接下来，将它们打乱顺序，以随机顺序启动，模拟同时的写入器和读取器。
请注意，线程尚未执行，只是定义了它们。

```python
write_thread_count = 50
read_thread_count = 5
threads = []

# 创建多个写入器和读取器线程（在同一个进程中）
# 将相同的连接作为参数传递
for i in range(write_thread_count):
    threads.append(Thread(target = write_from_thread,
                            args = (duckdb_con,),
                            name = 'write_thread_' + str(i)))

for j in range(read_thread_count):
    threads.append(Thread(target = read_from_thread,
                            args = (duckdb_con,),
                            name = 'read_thread_' + str(j)))

# 打乱线程顺序以模拟读取器和写入器的混合
random.seed(6) # 设置种子以确保测试时结果一致
random.shuffle(threads)
```

## 运行线程并显示结果

现在，启动所有线程并行运行，然后等待所有线程完成后再打印结果。
请注意，由于随机化，读取器和写入器的时间戳会交错出现，如预期那样。

```python
# 启动所有线程并行运行
for thread in threads:
    thread.start()

# 确保所有线程完成后再打印最终结果
for thread in threads:
    thread.join()

print(duckdb_con.execute("""
    SELECT *
    FROM my_inserts
    ORDER BY
        insert_time
""").df())
```