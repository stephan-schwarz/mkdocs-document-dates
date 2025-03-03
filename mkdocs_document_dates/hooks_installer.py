import os
import sys
import shutil
import subprocess
from pathlib import Path
import platform

def get_config_dir():
    """获取用户配置目录"""
    if platform.system().lower().startswith('win'):
        return Path(os.getenv('APPDATA', str(Path.home() / 'AppData' / 'Roaming')))
    else:  # macOS 和 Linux 统一使用 ~/.config
        return Path.home() / '.config'

def install():
    """安装 git hooks"""
    try:
        # 检查 git 是否可用
        try:
            subprocess.run(['git', '--version'], check=True, capture_output=True, encoding='utf-8')
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("提示: 未检测到 Git, 跳过 hooks 安装")
            return False
        
        # 准备配置目录
        config_dir = get_config_dir() / 'mkdocs-document-dates' / 'hooks'
        try:
            config_dir.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            print(f"错误: 无权限创建目录: {config_dir}")
            return False
        except Exception as e:
            print(f"错误: 创建目录失败: {config_dir}, 原因: {e}")
            return False

        hook_path = config_dir / 'pre-commit'

        # 复制 hook 文件到配置目录
        source_hook = Path(__file__).parent / 'hooks' / 'pre-commit'
        if not source_hook.exists():
            print(f"错误: 源 hook 文件不存在: {source_hook}")
            return False

        try:
            if platform.system().lower().startswith('win'):
                # Windows 系统: 复制为 .py 文件
                py_hook_path = hook_path.with_suffix('.py')
                shutil.copy2(source_hook, py_hook_path)
                
                # 创建批处理文件作为入口
                bat_hook_path = hook_path.with_suffix('.bat')
                python_path = sys.executable
                with open(bat_hook_path, 'w') as f:
                    f.write('@echo off\n')
                    f.write('setlocal\n')
                    f.write('set ERRORLEVEL=\n')
                    # 1. 使用安装插件时的 Python 解释器路径
                    f.write(f'"{python_path}" "{py_hook_path}" %*\n')
                    f.write('if %ERRORLEVEL% EQU 0 goto :eof\n')
                    # 2. 尝试 python3 命令
                    f.write('python3 "%~dp0pre-commit.py" %*\n')
                    f.write('if %ERRORLEVEL% EQU 0 goto :eof\n')
                    # 3. 尝试 python 命令
                    f.write('python "%~dp0pre-commit.py" %*\n')
                    f.write('if %ERRORLEVEL% EQU 0 goto :eof\n')
                    # 4. 最后尝试 py 启动器
                    f.write('py -3 "%~dp0pre-commit.py" %*\n')
                    f.write('if %ERRORLEVEL% EQU 0 goto :eof\n')
                    # 如果所有方式都失败，返回最后一次的错误码
                    f.write('exit /b %ERRORLEVEL%\n')
                
                # Windows 下设置文件权限
                os.chmod(py_hook_path, 0o755)
                os.chmod(bat_hook_path, 0o755)
            else:
                # Unix-like 系统: 使用无扩展名文件
                shutil.copy2(source_hook, hook_path)
                os.chmod(config_dir, 0o755)
                os.chmod(hook_path, 0o755)
        except PermissionError:
            print(f"错误: 无权限复制文件到: {hook_path}")
            return False
        except Exception as e:
            print(f"错误: 复制文件失败, 原因: {e}")
            return False

        # 配置全局 git hooks 路径
        try:
            subprocess.run(['git', 'config', '--global', 'core.hooksPath', 
                          str(config_dir)], check=True, encoding='utf-8')
            # print(f"Git hooks 已安装到: {config_dir}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"错误: 设置 git hooks 路径失败: {e}")
            return False
            
    except Exception as e:
        print(f"安装 hooks 时出错: {e}")
        return False

if __name__ == '__main__':
    install()