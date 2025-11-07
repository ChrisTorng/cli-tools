#!/usr/bin/env python3

"""
dl-latest-rs - 下載最新的 Rust 工具發布版本
用法: dl-latest-rs <基礎URL> <目標路徑>
範例: dl-latest-rs https://github.com/ChrisTorng/cli-tools ./bin
"""

import os
import sys
import platform
import subprocess
from pathlib import Path


def show_usage():
    """顯示用法"""
    print("用法: dl-latest-rs <基礎URL> <目標路徑>")
    print("  基礎URL: GitHub release 的基礎下載網址")
    print("  目標路徑: 解壓縮的目標目錄")
    print()
    print("範例:")
    print("  dl-latest-rs https://github.com/ChrisTorng/cli-tools ./bin")
    sys.exit(1)


def get_platform_suffix():
    """取得當前平台的檔案後綴"""
    system = platform.system().lower()
    
    if system == 'linux':
        return '-linux.zip'
    elif system == 'windows':
        return '-windows.zip'
    elif system == 'darwin':
        return '-macos.zip'
    else:
        print(f"錯誤: 不支援的作業系統: {system}")
        sys.exit(1)


def make_executable(target_dir):
    """將目標目錄中的所有檔案設定為可執行"""
    target_path = Path(target_dir)
    
    if not target_path.exists():
        print(f"錯誤: 目標目錄不存在: {target_dir}")
        sys.exit(1)
    
    print(f"\n設定檔案為可執行...")
    
    system = platform.system().lower()
    
    if system in ['linux', 'darwin']:
        # Unix-like 系統使用 chmod
        for item in target_path.rglob('*'):
            if item.is_file():
                try:
                    # 設定 u+x (使用者可執行)
                    os.chmod(item, item.stat().st_mode | 0o100)
                    print(f"  ✓ {item.name}")
                except Exception as e:
                    print(f"  ✗ {item.name}: {e}")
    elif system == 'windows':
        # Windows 系統，檔案預設就有執行權限
        print("  Windows 系統，檔案已自動具有執行權限")
        for item in target_path.rglob('*'):
            if item.is_file():
                print(f"  ✓ {item.name}")
    
    print("完成!")


def main():
    """主程式"""
    # 檢查參數
    if len(sys.argv) != 3:
        show_usage()
    
    base_url = sys.argv[1]
    target_dir = sys.argv[2]
    
    # 取得平台後綴
    suffix = get_platform_suffix()
    
    # 從 repo URL 解析出 repo 名稱
    # 例如: https://github.com/ChrisTorng/cli-tools -> cli-tools
    normalized = base_url.rstrip('/')
    repo_name = normalized.split('/')[-1]
    
    # 組合完整下載網址
    # https://github.com/ChrisTorng/cli-tools/releases/latest/download/cli-tools-linux.zip
    download_url = f"{normalized}/releases/latest/download/{repo_name}{suffix}"

    
    print(f"平台: {platform.system()}")
    print(f"下載網址: {download_url}")
    print(f"目標目錄: {target_dir}")
    print()
    
    # 取得 dlunzip.py 的路徑
    script_dir = Path(__file__).parent
    dlunzip_script = script_dir / 'dlunzip.py'
    
    if not dlunzip_script.exists():
        print(f"錯誤: 找不到 dlunzip.py 於 {dlunzip_script}")
        sys.exit(1)
    
    # 呼叫 dlunzip.py 下載並解壓
    try:
        result = subprocess.run(
            [sys.executable, str(dlunzip_script), download_url, target_dir],
            check=True
        )
        
        # 設定所有檔案為可執行
        make_executable(target_dir)
        
    except subprocess.CalledProcessError as e:
        print(f"\n錯誤: 下載或解壓失敗 (退出碼: {e.returncode})")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n操作已取消")
        sys.exit(1)
    except Exception as e:
        print(f"\n錯誤: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
