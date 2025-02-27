# mkdocs-document-dates

[English](README.md) | 简体中文



一个用于显示<mark>准确的</mark>文档创建日期和最后修改日期的 MkDocs 插件。

## 特性

- 自动显示文档的创建时间和最后修改时间
- **不依赖 Git**，直接使用文件系统的时间戳
- 支持在 `Front Matter` 中手动指定日期
- 跨平台支持（Windows、macOS、Linux）
- 支持多种时间格式（date、datetime、timeago）
- 灵活的显示位置（顶部或底部）
- 支持文档排除
- Material Design 风格的图标，优雅的样式设计
- 轻量级，无额外依赖
- 多语言支持
- 支持 CI/CD 构建系统（如 Github Actions）

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
      type: date               # 日期类型： date | datetime | timeago，默认 date
      locale: zh               # 本地化语言： zh zh_tw en es fr de ar ja ko ru ，默认：en
      date_format: '%Y-%m-%d'  # 日期格式
      time_format: '%H:%M:%S'  # 时间格式（仅在 type=datetime 时有效）
      position: bottom         # 显示位置：top（标题后） | bottom（文档末尾），默认 bottom
      exclude:                 # 排除的文件模式列表
        - temp.md              # 排除特定文件
        - private/*            # 排除 private 目录下的所有文件，包括子目录
        - drafts/*.md          # 排除当前目录 drafts 下的所有 markdown 文件，不包括子目录
```

## 手动指定日期

你也可以在 Markdown 文档的 `Front Matter` 中手动指定该文档的日期：

```yaml
---
created: 2023-01-01
modified: 2025-02-23
---

# 文档标题
```

## 配置选项

- **type**: 日期类型（默认：`date`）
  - `date`: 仅显示日期
  - `datetime`: 显示日期和时间
  - `timeago`: 显示相对时间（例如：2 分钟前）
- **locale**: 本地化语言（默认：`en`）
  - 支持： `zh zh_tw en es fr de ar ja ko ru`
- **date_format**: 日期格式（默认 `%Y-%m-%d`）
  - 支持所有 Python datetime 格式化字符串，例如：%Y年%m月%d日、%b %d, %Y 等
- **time_format**: 时间格式（默认：`%H:%M:%S`）
- **position**: 显示位置（默认：`bottom`）
  - `top`: 在文档第一个标题后显示
  - `bottom`: 在文档末尾显示
- **exclude**: 排除文件列表（默认：[]）
  - 支持 glob 模式，例如：["private/\*", "temp.md", "drafts/\*.md"]

## 注意事项

- 在使用 CI/CD 构建系统时（如 Github Actions），它仍然有效
  - 使用缓存文件 `.dates_cache.json` 解决了这个问题
  - 你可以这么配置：
    ```
    ...
    
      - run: pip install mkdocs-document-dates
      - run: mkdocs gh-deploy --force
    ```
- 如果你是在 Linux 系统下使用 MkDocs ，因为系统限制，则使用修改时间作为创建时间，如果需要准确的创建时间，可在 Front Matter 手动指定