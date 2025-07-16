---
---
layout: docu
redirect_from:
- /dev/sqllogictest/debugging
- /dev/sqllogictest/debugging/
- /docs/dev/sqllogictest/debugging
title: 调试
---

测试的目的是找出系统何时出现故障。不可避免地，对系统的更改会导致其中一个测试失败，当这种情况发生时，就需要对测试进行调试。

首先，建议始终以调试模式运行。这可以通过使用命令 `make debug` 编译系统来实现。其次，建议只运行导致失败的测试。这可以通过将导致失败的测试文件名作为命令行参数传递给测试套件来实现（例如：`build/debug/test/unittest test/sql/projection/test_simple_projection.test`）。如需更多关于运行测试子集的选项，请参阅 [触发运行哪些测试](#triggering-which-tests-to-run) 部分。

接下来，可以将调试器附加到程序并调试测试。在 sqllogictests 中，通常很难在特定查询上中断，不过我们已经扩展了测试套件，使得在每次运行查询时都会调用一个名为 `query_break` 的函数，并将行号 `line` 作为参数传递。这允许您在特定查询上设置条件断点。例如，如果我们想在测试文件的第 43 行中断，可以创建以下断点：

```text
gdb: break query_break if line==43
lldb: break s -n query_break -c line==43
```

您还可以通过在文件中放置 `mode skip` 来跳过某些查询，接着可选的 `mode unskip`。在两个语句之间的任何查询都不会被执行。

## 触发运行哪些测试

运行 unittest 程序时，默认会运行所有快速测试。可以通过将测试名称作为参数添加来运行特定的测试。对于 sqllogictests，这是相对于测试文件的路径。
要仅运行单个测试：

```bash
build/debug/test/unittest test/sql/projection/test_simple_projection.test
```

要运行某个目录中的所有测试，可以通过将目录名作为带方括号的参数提供。
要运行“projection”目录中的所有测试：

```bash
build/debug/test/unittest "[projection]"
```

要运行所有测试，包括慢速测试：
运行带有星号的测试即可。
要运行所有测试，包括慢速测试：

```bash
build/debug/test/unittest "*"
```

我们可以使用 `--start-offset` 和 `--end-offset` 参数运行测试子集。
要运行第 200..250 个测试：

```bash
build/debug/test/unittest --start-offset=200 --end-offset=250
```

这些参数也支持百分比形式。要运行 10% - 20% 的测试：

```bash
build/debug/test/unittest --start-offset-percentage=10 --end-offset-percentage=20
```

运行的测试集也可以从一个每行包含一个测试名称的文件中加载，并通过 `-f` 命令加载。

```bash
cat test.list
```

```text
test/sql/join/full_outer/test_full_outer_join_issue_4252.test
test/sql/join/full_outer/full_outer_join_cache.test
test/sql/join/full_outer/test_full_outer_join.test
```

要仅运行文件中标记的测试：

```bash
build/debug/test/unittest -f test.list
```