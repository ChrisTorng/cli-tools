# tee - Rust 實作

Windows 的 tee 命令實作,使用 Rust 開發。

## 功能

從標準輸入讀取資料,同時輸出到標準輸出和指定的檔案。

## 使用方式

```powershell
# 基本用法 - 寫入檔案(覆蓋模式)
echo "Hello" | tee output.txt

# 附加模式 - 附加到檔案末尾
echo "World" | tee -a output.txt

# 寫入多個檔案
echo "Hello" | tee file1.txt file2.txt

# 附加到多個檔案
echo "World" | tee -a file1.txt file2.txt
```

## 建構

需要安裝 Rust 工具鏈(rustc 和 cargo)。

```powershell
cargo build --release
```

編譯後的執行檔位於 `target\release\tee.exe`。

## 參數

- `-a` 或 `--append`: 附加模式,將內容附加到檔案末尾而不是覆蓋
- 其他參數: 視為輸出檔案路徑

## 範例

```powershell
# 列出目錄並同時儲存到檔案
dir | tee dir_list.txt

# 執行命令並記錄輸出
cargo build 2>&1 | tee build_log.txt

# 附加模式記錄
Get-Date | tee -a log.txt
```

