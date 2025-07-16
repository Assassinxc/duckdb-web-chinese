---
---
layout: docu
redirect_from:
- /docs/api/cli/syntax_highlighting
- /docs/api/cli/syntax_highlighting/
- /docs/clients/cli/syntax_highlighting
title: 语法高亮
---

> 当前CLI中的语法高亮功能仅适用于macOS和Linux。

在shell中编写的SQL查询会自动使用语法高亮功能进行突出显示。

![显示shell中语法高亮的图片](/images/syntax_highlighting_screenshot.png)

查询中的一些组件会以不同颜色进行高亮显示。颜色可以通过[点命令]({% link docs/stable/clients/cli/dot_commands.md %})进行配置。
还可以使用`.highlight off`命令完全禁用语法高亮功能。

以下是可配置的组件列表。

|          类型           |   命令   |  默认颜色  |
|-------------------------|-------------|-----------------|
| 关键字                | `.keyword`  | `green`         |
| 常量和字面量           | `.constant` | `yellow`        |
| 注释                  | `.comment`  | `brightblack`   |
| 错误                  | `.error`    | `red`           |
| 续行                  | `.cont`     | `brightblack`   |
| 续行（选中）           | `.cont_sel` | `green`         |

组件可以通过支持的颜色名称（例如：`.keyword red`）或直接提供用于渲染的终端代码（例如：`.keywordcode \033[31m`）进行配置。以下是支持的颜色名称及其对应的终端代码列表。

|     颜色     | 终端代码 |
|---------------|---------------|
| red           | `\033[31m`    |
| green         | `\033[32m`    |
| yellow        | `\033[33m`    |
| blue          | `\033[34m`    |
| magenta       | `\033[35m`    |
| cyan          | `\033[36m`    |
| white         | `\033[37m`    |
| brightblack   | `\033[90m`    |
| brightred     | `\033[91m`    |
| brightgreen   | `\033[92m`    |
| brightyellow  | `\033[93m`    |
| brightblue    | `\033[94m`    |
| brightmagenta | `\033[95m`    |
| brightcyan    | `\033[96m`    |
| brightwhite   | `\033[97m`    |

例如，以下是一个替代的语法高亮颜色设置：

```text
.keyword brightred
.constant brightwhite
.comment cyan
.error yellow
.cont blue
.cont_sel brightblue
```

如果您希望每次启动CLI时使用不同的颜色设置，可以将这些命令放在CLI启动时加载的`~/.duckdbrc`文件中。

## 错误高亮

shell支持对某些错误进行高亮显示。特别是不匹配的括号和未闭合的引号会以红色（或指定的其他颜色）高亮显示。对于大型查询，此高亮功能会自动禁用。此外，还可以使用`.render_errors off`命令手动禁用此功能。