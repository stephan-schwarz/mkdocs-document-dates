# mkdocs-document-dates

English | [简体中文](README_zh.md)



A MkDocs plugin for displaying **accurate** document creation and last modification dates.

## Features

- Automatically displays document creation and last modification times
- Supports manual date specification in `Front Matter`
- No Git dependency, uses filesystem timestamps directly
- Cross-platform support (Windows, macOS, Linux)
- Configurable date and time formats
- Flexible display position (top or bottom)
- File exclusion rules support
- Material Design icons
- Elegant styling
- Lightweight with no extra dependencies

## Installation

```bash
pip install mkdocs-document-dates
```

## Configuration

Add the plugin to your mkdocs.yml:

```yaml
plugins:
  - document-dates
```

Or, customize the configuration:

```yaml
plugins:
  - document-dates:
      date_format: '%Y-%m-%d'    # Date format
      show_time: false           # Whether to show time
      time_format: '%H:%M:%S'    # Time format
      position: bottom           # Display position: top (after title) or bottom (end of document)
      exclude:                   # List of file patterns to exclude
        - "private/*"            # Exclude all files in private directory
        - "drafts/*.md"         # Exclude all markdown files in drafts directory
        - "temp.md"             # Exclude specific file
        - "*.tmp"               # Exclude all files with .tmp extension
```

## Manual Date Specification

You can also manually specify the date of a Markdown document in its `Front Matter` :

```yaml
---
created_date: 2023-01-01
modified_date: 2023-12-31
---

# Document Title
```

## Configuration Options

- `date_format`: Date format (default: %Y-%m-%d)
  - Supports all Python datetime format strings, examples: %Y-%m-%d, %b %d, %Y, etc.
- `show_time`: Whether to show time (default: false)
  - true: Show both date and time
  - false: Show date only
- `time_format`: Time format (default: %H:%M:%S)
  - Only effective when show_time is true
- `position`: Display position (default: bottom)
  - top: Display after the first heading
  - bottom: Display at the end of document
- `exclude`: List of files to exclude (default: [])
  - Supports glob patterns, example: ["private/*", "temp.md"]

## Notes

- Creation time behavior varies across operating systems:
  - Windows: Uses file creation time
  - macOS: Uses file creation time (birthtime)
  - Linux: Uses modification time as creation time due to system limitations
- For accurate creation times, it's recommended to use Front Matter for manual specification

