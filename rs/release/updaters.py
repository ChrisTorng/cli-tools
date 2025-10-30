#!/usr/bin/env python3
"""
更新 Rust 專案的發布檔案
從 rs 下所有的 target/release 資料夾中取得 *.exe 檔案，
移動到 rs/release 目錄，然後刪除 target 資料夾。
"""

import os
import shutil
from pathlib import Path


def main():
    # 取得 rs 目錄的絕對路徑
    script_dir = Path(__file__).parent
    rs_dir = script_dir.parent
    release_dir = script_dir
    
    print(f"搜尋目錄: {rs_dir}")
    print(f"目標目錄: {release_dir}")
    print()
    
    # 搜尋所有的 target/release 資料夾
    for target_release_dir in rs_dir.glob("*/target/release"):
        print(f"找到: {target_release_dir}")
        
        # 取得所有 .exe 檔案
        exe_files = list(target_release_dir.glob("*.exe"))
        
        if not exe_files:
            print(f"  沒有找到 .exe 檔案")
        else:
            # 移動每個 .exe 檔案
            for exe_file in exe_files:
                dest_file = release_dir / exe_file.name
                print(f"  移動: {exe_file.name} -> {dest_file}")
                
                # 如果目標檔案已存在，先刪除
                if dest_file.exists():
                    dest_file.unlink()
                
                shutil.move(str(exe_file), str(dest_file))
        
        # 刪除 target 資料夾
        target_dir = target_release_dir.parent
        print(f"  刪除: {target_dir}")
        try:
            shutil.rmtree(target_dir)
            print(f"  成功刪除 target 資料夾")
        except Exception as e:
            print(f"  刪除失敗: {e}")
        
        print()
    
    print("完成！")


if __name__ == "__main__":
    main()
