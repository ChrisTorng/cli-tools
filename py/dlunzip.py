#!/usr/bin/env python3

"""
dlunzip - 下載並解壓各種壓縮檔
用法: dlunzip <URL> [目標目錄]
如果未指定目標目錄，則解壓到當前目錄
"""

import os
import sys
import argparse
import urllib.request
import urllib.parse
import tarfile
import zipfile
import gzip
import bz2
import lzma
import shutil
import subprocess
import tempfile
from pathlib import Path


def show_usage():
    """顯示用法"""
    print("用法: dlunzip <URL> [目標目錄]")
    print("  URL: 要下載的壓縮檔網址")
    print("  目標目錄: 解壓縮的目標目錄 (可選，預設為當前目錄)")
    sys.exit(1)


def download_file(url, temp_file):
    """下載檔案"""
    print(f"正在下載: {url}")
    
    try:
        # 使用 urllib 下載檔案
        with urllib.request.urlopen(url) as response:
            total_size = int(response.headers.get('content-length', 0))
            block_size = 8192
            downloaded = 0
            
            with open(temp_file, 'wb') as f:
                while True:
                    chunk = response.read(block_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    # 顯示進度
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\r進度: {percent:.1f}%", end='', flush=True)
            
            if total_size > 0:
                print()  # 換行
                
    except Exception as e:
        print(f"\n錯誤: 下載失敗 - {e}")
        sys.exit(1)


def extract_zip(temp_file, target_dir):
    """解壓 ZIP 檔案"""
    with zipfile.ZipFile(temp_file, 'r') as zip_ref:
        zip_ref.extractall(target_dir)


def extract_tar(temp_file, target_dir, mode='r'):
    """解壓 TAR 檔案"""
    with tarfile.open(temp_file, mode) as tar_ref:
        tar_ref.extractall(target_dir)


def extract_gz(temp_file, target_dir, filename):
    """解壓 GZ 檔案"""
    output_file = Path(target_dir) / filename.replace('.gz', '')
    with gzip.open(temp_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def extract_bz2(temp_file, target_dir, filename):
    """解壓 BZ2 檔案"""
    output_file = Path(target_dir) / filename.replace('.bz2', '')
    with bz2.open(temp_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def extract_7z(temp_file, target_dir):
    """解壓 7Z 檔案"""
    if not shutil.which('7z'):
        print("錯誤: 找不到 7z 命令")
        sys.exit(1)
    
    subprocess.run(['7z', 'x', temp_file, f'-o{target_dir}'], check=True)


def extract_rar(temp_file, target_dir):
    """解壓 RAR 檔案"""
    if not shutil.which('unrar'):
        print("錯誤: 找不到 unrar 命令")
        sys.exit(1)
    
    subprocess.run(['unrar', 'x', temp_file, f'{target_dir}/'], check=True)


def extract_file(temp_file, target_dir, filename):
    """根據檔案副檔名解壓"""
    print("正在解壓縮...")
    
    filename_lower = filename.lower()
    
    try:
        if filename_lower.endswith('.zip'):
            extract_zip(temp_file, target_dir)
        elif filename_lower.endswith(('.tar.gz', '.tgz')):
            extract_tar(temp_file, target_dir, 'r:gz')
        elif filename_lower.endswith(('.tar.bz2', '.tbz2')):
            extract_tar(temp_file, target_dir, 'r:bz2')
        elif filename_lower.endswith(('.tar.xz', '.txz')):
            extract_tar(temp_file, target_dir, 'r:xz')
        elif filename_lower.endswith('.tar'):
            extract_tar(temp_file, target_dir, 'r')
        elif filename_lower.endswith('.gz'):
            extract_gz(temp_file, target_dir, filename)
        elif filename_lower.endswith('.bz2'):
            extract_bz2(temp_file, target_dir, filename)
        elif filename_lower.endswith('.7z'):
            extract_7z(temp_file, target_dir)
        elif filename_lower.endswith('.rar'):
            extract_rar(temp_file, target_dir)
        else:
            print(f"錯誤: 不支援的壓縮格式: {filename}")
            sys.exit(1)
    except Exception as e:
        print(f"錯誤: 解壓失敗 - {e}")
        sys.exit(1)


def list_directory(target_dir):
    """列出目錄內容"""
    print("內容:")
    for item in sorted(Path(target_dir).iterdir()):
        size = item.stat().st_size if item.is_file() else 0
        size_str = f"{size:,}" if item.is_file() else "<DIR>"
        item_type = "/" if item.is_dir() else ""
        print(f"  {size_str:>15}  {item.name}{item_type}")


def clear_directory(target_dir):
    """清空目標目錄(保留目錄本身)"""
    target_path = Path(target_dir)
    if target_path.exists():
        print(f"正在清空目標目錄: {target_dir}")
        for item in target_path.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()


def move_extracted_files(temp_extract_dir, target_dir):
    """將解壓後的檔案從暫存目錄搬移到目標目錄"""
    print(f"正在搬移檔案到: {target_dir}")
    temp_path = Path(temp_extract_dir)
    target_path = Path(target_dir)
    
    # 確保目標目錄存在
    target_path.mkdir(parents=True, exist_ok=True)
    
    # 搬移所有檔案和目錄
    for item in temp_path.iterdir():
        dest = target_path / item.name
        shutil.move(str(item), str(dest))


def main():
    """主程式"""
    # 解析參數
    if len(sys.argv) < 2:
        show_usage()
    
    url = sys.argv[1]
    target_dir = sys.argv[2] if len(sys.argv) > 2 else '.'
    
    # 從 URL 取得檔案名稱
    parsed_url = urllib.parse.urlparse(url)
    filename = os.path.basename(parsed_url.path)
    
    if not filename:
        print("錯誤: 無法從 URL 取得檔案名稱")
        sys.exit(1)
    
    # 建立臨時目錄 (使用系統臨時目錄，跨平台相容)
    temp_base_dir = tempfile.mkdtemp(prefix=f"dlunzip_{os.getpid()}_")
    temp_file = os.path.join(temp_base_dir, filename)
    temp_extract_dir = os.path.join(temp_base_dir, "extracted")
    
    print(f"目標目錄: {target_dir}")
    
    try:
        # 下載檔案
        download_file(url, temp_file)
        print(f"下載完成: {filename}")
        
        # 解壓到暫存目錄
        Path(temp_extract_dir).mkdir(parents=True, exist_ok=True)
        extract_file(temp_file, temp_extract_dir, filename)
        print("解壓完成")
        
        # 確認解壓成功 (檢查暫存目錄有內容)
        extracted_items = list(Path(temp_extract_dir).iterdir())
        if not extracted_items:
            print("錯誤: 解壓後沒有找到任何檔案")
            sys.exit(1)
        
        # 清空目標目錄
        clear_directory(target_dir)
        
        # 搬移檔案到目標目錄
        move_extracted_files(temp_extract_dir, target_dir)
        
        # 清理臨時目錄
        if os.path.exists(temp_base_dir):
            shutil.rmtree(temp_base_dir)
        
        print(f"完成! 檔案已解壓到: {target_dir}")
        list_directory(target_dir)
        
    except KeyboardInterrupt:
        print("\n\n操作已取消")
        if os.path.exists(temp_base_dir):
            shutil.rmtree(temp_base_dir)
        sys.exit(1)
    except Exception as e:
        print(f"\n錯誤: {e}")
        if os.path.exists(temp_base_dir):
            shutil.rmtree(temp_base_dir)
        sys.exit(1)


if __name__ == '__main__':
    main()
