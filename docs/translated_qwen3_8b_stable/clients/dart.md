---
---
github_repository: https://github.com/TigerEyeLabs/duckdb-dart
layout: docu
redirect_from:
- /docs/api/dart
- /docs/api/dart/
- /docs/clients/dart
title: Dart 客户端
---

> DuckDB Dart 客户端的最新版本是 {{ site.current_duckdb_dart_version }}。

DuckDB.Dart 是 [DuckDB](https://duckdb.org/) 的原生 Dart API。

## 安装

可以从 [pub.dev](https://pub.dev/packages/dart_duckdb) 安装 DuckDB.Dart。请参阅 [API 参考文档](https://pub.dev/documentation/dart_duckdb/latest/) 获取详细信息。

### 将此包作为库使用

#### 依赖它

使用 Flutter 添加依赖项：

```bash
flutter pub add dart_duckdb
```

这会将以下内容添加到您的包的 `pubspec.yaml` 文件中（并隐式运行 `flutter pub get`）：

```yaml
dependencies:
  dart_duckdb: ^1.1.3
```

或者，您的编辑器可能支持 `flutter pub get`。请查阅您编辑器的文档以了解更多信息。

#### 导入它

现在在您的 Dart 代码中，您可以导入它：

```dart
import 'package:dart_duckdb/dart_duckdb.dart';
```

## 使用示例

查看 [`duckdb-dart` 仓库](https://github.com/TigerEyeLabs/duckdb-dart/) 中的示例项目：

* [`cli`](https://github.com/TigerEyeLabs/duckdb-dart/tree/main/examples/cli)：命令行应用
* [`duckdbexplorer`](https://github.com/TigerEyeLabs/duckdb-dart/tree/main/examples/duckdbexplorer)：图形用户界面应用，可构建为桌面操作系统以及 Android 和 iOS。

以下是 DuckDB.Dart 的一些常见代码片段：

### 查询内存数据库

```dart
import 'package:dart_duckdb/dart_duckdb.dart';

void main() {
  final db = duckdb.open(":memory:");
  final connection = duckdb.connect(db);

  connection.execute('''
    CREATE TABLE users (id INTEGER, name VARCHAR, age INTEGER);
    INSERT INTO users VALUES (1, 'Alice', 30), (2, 'Bob', 25);
  ''');

  final result = connection.query("SELECT * FROM users WHERE age > 28").fetchAll();

  for (final row in result) {
    print(row);
  }

  connection.dispose();
  db.dispose();
}
```

### 在后台隔离中执行查询

```dart
import 'package:dart_duckdb/dart_duckdb.dart';

void main() {
  final db = duckdb.open(":memory:");
  final connection = duckdb.connect(db);

  await Isolate.spawn(backgroundTask, db.transferrable);

  connection.dispose();
  db.dispose();
}

void backgroundTask(TransferableDatabase transferableDb) {
  final connection = duckdb.connectWithTransferred(transferableDb);
  // 访问数据库 ...
  // fetch 是必需的，以便将数据发送回主隔离
}
```