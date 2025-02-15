# mkdocs-document-dates

[English](README_en.md) | 简体中文



一个用于显示准确的文档创建日期和最后修改日期的 MkDocs 插件。

## 特性

- 自动显示文档的创建时间和最后修改时间
- 支持在 `Front Matter` 中手动指定日期
- 不依赖 Git，直接使用文件系统的时间戳
- 跨平台支持（Windows、macOS、Linux）
- 可配置的日期和时间格式
- 灵活的显示位置（顶部或底部）
- 支持文件排除规则
- Material Design 风格的图标
- 优雅的样式设计
- 轻量级，无额外依赖

## 安装

```bash
pip install mkdocs-document-dates
```

## 配置

在你的 mkdocs.yml 中添加插件即可：

```yaml
plugins:
  - document-dates
```

或者，你要自定义配置：

```yaml
plugins:
  - document-dates:
      date_format: '%Y-%m-%d'    # 日期格式
      show_time: false           # 是否显示时间
      time_format: '%H:%M:%S'    # 时间格式
      position: bottom           # 显示位置：top（标题后）或 bottom（文档末尾）
      exclude:                   # 排除的文件模式列表
        - "private/*"            # 排除 private 目录下的所有文件
        - "drafts/*.md"         # 排除 drafts 目录下的所有 markdown 文件
        - "temp.md"             # 排除特定文件
        - "*.tmp"               # 排除所有 .tmp 后缀的文件
```

## 手动指定日期

你也可以为 Markdown 文档手动指定日期，在 Markdown 文件的 `Front Matter` 中设置：

```yaml
---
created_date: '2023-01-01'
modified_date: '2023-12-31'
---

# 文档标题
```

## 配置选项

- date_format: 日期格式（默认：%Y-%m-%d）
  - 支持所有 Python datetime 格式化字符串
  - 例如：%Y年%m月%d日、%b %d, %Y 等
- show_time: 是否显示时间（默认：false）
  - true: 同时显示日期和时间
  - false: 仅显示日期
- time_format: 时间格式（默认：%H:%M:%S）
  - 仅在 show_time 为 true 时生效
- position: 显示位置（默认：bottom）
  - top: 在文档第一个标题后显示
  - bottom: 在文档末尾显示
- exclude: 排除文件列表（默认：[]）
  - 支持 glob 模式
  - 例如：["private/*", "temp.md"]

## 注意事项

- 创建时间在不同操作系统上的行为可能不同：
  - Windows: 使用文件创建时间
  - macOS: 使用文件创建时间（birthtime）
  - Linux: 由于系统限制，使用修改时间作为创建时间
- 如果需要准确的创建时间，建议使用 Front Matter 手动指定

