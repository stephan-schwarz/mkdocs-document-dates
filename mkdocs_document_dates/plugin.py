import os
import platform
from datetime import datetime
from pathlib import Path
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options

class DocumentDatesPlugin(BasePlugin):
    config_scheme = (
        ('date_format', config_options.Type(str, default='%Y-%m-%d')),
        ('show_time', config_options.Type(bool, default=False)),
        ('time_format', config_options.Type(str, default='%H:%M:%S')),
        ('position', config_options.Type(str, default='bottom')),
        ('exclude', config_options.Type(list, default=[])),
    )

    def __init__(self):
        super().__init__()

    def get_css_content(self):
        """返回插件的 CSS 样式"""
        return """
.document-dates-plugin {
    color: #8e8e8e;
    font-size: 0.75rem;
    padding: 0.2rem 0;
    opacity: 0.8;
    display: flex;
    gap: 1.5rem;
    align-items: center;
    margin-bottom: 0.3rem;
}
.document-dates-plugin span {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
}
.document-dates-plugin .material-icons {
    font-size: 0.9rem;
    opacity: 0.7;
}
.document-dates-plugin-wrapper {
    margin: 0.3rem 0 1rem 0;
    border-bottom: 1px solid rgba(0, 0, 0, 0.07);
    padding-bottom: 0.5rem;
}
"""

    def on_config(self, config):
        """配置插件并添加必要的 CSS"""
        if 'extra_css' not in config:
            config['extra_css'] = []
        
        # 添加 Material Icons
        material_icons_url = 'https://fonts.googleapis.com/icon?family=Material+Icons'
        if material_icons_url not in config['extra_css']:
            config['extra_css'].append(material_icons_url)
        
        # 添加自定义 CSS
        css_file = Path(config['docs_dir']) / 'assets' / 'document_dates.css'
        css_file.parent.mkdir(parents=True, exist_ok=True)
        css_file.write_text(self.get_css_content())
        config['extra_css'].append('assets/document_dates.css')
        
        return config

    def format_date_info(self, created, modified):
        """格式化日期信息的 HTML"""
        return (
            f"\n\n"
            f"<div class='document-dates-plugin-wrapper'>"
            f"<div class='document-dates-plugin'>"
            f"<span><span class='material-icons'>add_circle</span>"
            f"{self.format_date(created)}</span>"
            f"<span><span class='material-icons'>update</span>"
            f"{self.format_date(modified)}</span>"
            f"</div>"
            f"</div>\n"
        )

    def insert_date_info(self, markdown, date_info):
        """根据配置将日期信息插入到合适的位置"""
        if self.config['position'] == 'top':
            lines = markdown.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('#'):
                    lines.insert(i + 1, date_info)
                    return '\n'.join(lines)
            return date_info + markdown
        return markdown + "\n\n" + date_info

    def on_page_markdown(self, markdown, page, config, files):
        """处理页面内容，添加日期信息"""
        file_path = page.file.abs_src_path
        
        # 检查是否在排除列表中
        for exclude_pattern in self.config['exclude']:
            if Path(file_path).match(exclude_pattern):
                return markdown
        
        # 直接获取日期信息
        created, modified = self.get_file_dates(file_path)
        
        # 检查 frontmatter 中的日期
        meta = getattr(page, 'meta', {})
        if 'created_date' in meta:
            try:
                date_str = str(meta['created_date']).strip("'\"")  # 移除可能存在的引号
                created = datetime.fromisoformat(date_str)
            except (ValueError, TypeError):
                # 如果解析失败，保持原有的文件系统日期
                pass
                
        if 'modified_date' in meta:
            try:
                date_str = str(meta['modified_date']).strip("'\"")  # 移除可能存在的引号
                modified = datetime.fromisoformat(date_str)
            except (ValueError, TypeError):
                # 如果解析失败，保持原有的文件系统日期
                pass
        
        # 格式化并插入日期信息
        date_info = self.format_date_info(created, modified)
        return self.insert_date_info(markdown, date_info)

    def get_file_dates(self, file_path):
        """获取文件的创建时间和修改时间"""
        
        stat = os.stat(file_path)
        modified = datetime.fromtimestamp(stat.st_mtime)
        
        system = platform.system().lower()
        if system == 'darwin':  # macOS
            try:
                created = datetime.fromtimestamp(stat.st_birthtime)
            except AttributeError:
                created = datetime.fromtimestamp(stat.st_ctime)
        elif system == 'windows':  # Windows
            created = datetime.fromtimestamp(stat.st_ctime)
        else:  # Linux 和其他系统
            # Linux 没有可靠的创建时间，使用修改时间作为创建时间
            created = modified
        
        return created, modified

    def format_date(self, date):
        if self.config['show_time']:
            return date.strftime(f"{self.config['date_format']} {self.config['time_format']}")
        return date.strftime(self.config['date_format'])

