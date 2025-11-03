# cli-tools

跨平台命令列工具集合，提供實用的文字處理和系統工具。

## 專案概述

這個 repository 收集了各種小型但實用的命令列工具，使用不同的程式語言實作以滿足不同的使用場景。

## 目錄結構

```
cli-tools/
├── cmd/            - Windows 批次檔腳本
│   ├── dequote.cmd      - 整合多個工具的處理流程
│   ├── kvcookies.cmd - Cookies 格式化快捷指令
│   └── kvpath.cmd  - PATH 環境變數格式化快捷指令
├── ps/             - PowerShell 腳本 (待開發)
├── py/             - Python 實作
│   └── dequote.py       - 雙引號移除工具 (Python 版本)
└── rs/             - Rust 實作 (主要開發方向)
    ├── dequote/         - 雙引號移除工具 (Rust 版本)
    ├── kv-splitter/ - Key/Value 字串切割工具 (Rust 版本)
    ├── tee/        - tee 命令 (Rust 版本)
    ├── release/    - 編譯後的執行檔
    │   ├── dequote.exe
    │   ├── kv-splitter.exe
    │   ├── tee.exe
    │   └── updaters.py - 自動化發布腳本
    └── RustInstructions.md - Rust 開發指南
```

## 工具清單

### dequote - 雙引號移除工具

移除輸入字串前後的雙引號。

**可用版本:**
- **Python** (`py/dequote.py`): 跨平台,需要 Python 3
- **Rust** (`rs/dequote/`): 高效能,編譯為原生執行檔

**使用方式:**
```powershell
# Python 版本
echo '"hello"' | python py/dequote.py

# Rust 版本 (編譯後)
echo '"hello"' | rs/release/dequote.exe
# 輸出: hello
```

### tee - 標準輸入複製工具

從標準輸入讀取資料,同時輸出到標準輸出和指定的檔案 (Windows tee 命令的功能完整實作)。

**可用版本:**
- **Rust** (`rs/tee/`): 完整功能實作

**使用方式:**
```powershell
# 基本用法 - 寫入檔案
echo "Hello" | rs/release/tee.exe output.txt

# 附加模式
echo "World" | rs/release/tee.exe -a output.txt

# 寫入多個檔案
dir | rs/release/tee.exe file1.txt file2.txt
```

**功能特色:**
- 支援覆蓋模式和附加模式 (`-a` 或 `--append`)
- 可同時寫入多個檔案
- 保持標準輸入/輸出的資料流

詳細說明請參考 [rs/tee/README.md](rs/tee/README.md)

### kv-splitter - Key/Value 字串切割工具

從標準輸入讀取 key/value 格式的字串，進行切割和格式化輸出。

**可用版本:**
- **Rust** (`rs/kv-splitter/`): 完整功能實作

**使用方式:**
```powershell
# PATH 環境變數格式化
echo "C:\Python313\Scripts\;C:\Python313\" | rs/release/kv-splitter.exe -p path
# 輸出: 每個路徑單獨一行

# Cookies 格式化
echo "_device_id=abc123; _octo=GH1.1.1471563711" | rs/release/kv-splitter.exe -p cookies
# 輸出: key 和 value 用 tab 分隔，每組單獨一行

# 自訂分隔字元
echo "name:John,age:30" | rs/release/kv-splitter.exe -i "," -k ":" -I "\n" -K " = "
# 輸出: name = John
#       age = 30
```

**功能特色:**
- 支援預定義 pattern (`path`, `cookies`)
- 自訂項目分隔字元和 key/value 分隔字元
- 自訂輸出格式的替代字元
- 可擴充的 pattern 系統

**實用批次檔:**
- `cmd/kvpath.cmd` - 快速格式化剪貼簿中的 PATH 環境變數
- `cmd/kvcookies.cmd` - 快速格式化剪貼簿中的 Cookies

詳細說明請參考 [rs/kv-splitter/README.md](rs/kv-splitter/README.md)

### 剪貼簿工具

用於在命令列和剪貼簿之間傳輸資料，取自 [dotfiles-cli-tools](https://github.com/ChrisTorng/dotfiles-cli-tools)。

- **pasta** - 將剪貼簿內容輸出到標準輸出
- **cp** - 從標準輸入讀取內容並複製到剪貼簿

詳細說明請參考該 repository。

### 批次檔工具組合

在 `cmd/` 資料夾中提供了整合多個工具的批次檔，用於快速處理剪貼簿內容。

#### dequote.cmd - 移除雙引號處理流程

將剪貼簿中的文字移除前後雙引號後，複製回剪貼簿並顯示。

```batch
pasta | dequote | tee | cp
pasta
```

**處理流程:**
1. `pasta` - 讀取剪貼簿內容
2. `dequote` - 移除前後雙引號
3. `tee` - 同時輸出到螢幕和下一個工具
4. `cp` - 複製到剪貼簿
5. `pasta` - 再次顯示剪貼簿內容（驗證結果）

#### kvpath.cmd - PATH 環境變數格式化

將剪貼簿中的 PATH 環境變數（以 `;` 分隔）格式化為每行一個路徑，並複製回剪貼簿。

```batch
pasta | kv-splitter -p path | cp
pasta
```

**使用情境:**
複製 Windows PATH 環境變數後執行，可將 `C:\Path1;C:\Path2` 格式化為：
```
C:\Path1
C:\Path2
```

#### kvcookies.cmd - Cookies 格式化

將剪貼簿中的 Cookies（以 `;` 和 `=` 分隔）格式化為每行一個 key-value 對，並複製回剪貼簿。

```batch
pasta | kv-splitter -p cookies | cp
pasta
```

**使用情境:**
複製瀏覽器的 Cookies 字串後執行，可將 `name=value; name2=value2` 格式化為：
```
name	value
name2	value2
```

## 開發指南

### Rust 工具開發

Rust 是本專案的主要開發語言,提供最佳的效能和跨平台相容性。

**詳細開發指南:** [rs/RustInstructions.md](rs/RustInstructions.md)

**快速開始:**

```powershell
# 1. 安裝 Rust (首次使用)
# 訪問 https://rustup.rs/

# 2. 編譯專案
cd rs/dequote
cargo build --release

# 3. 執行專案
cargo run

# 4. 執行測試
cargo test
```

### Python 工具開發

Python 工具適合快速原型開發和跨平台腳本。

**要求:** Python 3.6+

**執行方式:**
```powershell
python py/dequote.py
```

## 發布流程

### 編譯 Rust 工具

```powershell
# 進入專案目錄
cd rs/dequote

# 編譯發布版本
cargo build --release

# 編譯後的執行檔位於 target/release/
```

### 自動化發布

使用提供的 Python 腳本自動收集所有編譯好的執行檔:

```powershell
# 在 cli-tools 目錄下執行
python rs/release/updaters.py
```

此腳本會:
1. 搜尋所有 Rust 專案的 `target/release` 資料夾
2. 將 `.exe` 檔案移動到 `rs/release/` 目錄
3. 清理 `target` 資料夾以節省空間

## 為什麼選擇 Rust?

- ✅ **跨平台**: Windows、Linux、macOS 通用
- ✅ **高效能**: 原生程式碼,執行速度快
- ✅ **記憶體安全**: 編譯時期捕捉錯誤
- ✅ **零依賴**: 不需要額外的執行環境
- ✅ **單一執行檔**: 部署簡單

## 未來計畫

- [ ] 新增更多實用的命令列工具
- [ ] PowerShell 腳本開發 (ps/ 資料夾)
- [ ] 建立 Windows 安裝程式
- [ ] Linux/macOS 版本測試與發布
- [ ] GitHub Actions 自動化建構

## 授權

請參考 [LICENSE](LICENSE) 檔案。

## 貢獻

歡迎提交 Issue 或 Pull Request!

開發新工具前,請先閱讀:
- Rust 工具: [rs/RustInstructions.md](rs/RustInstructions.md)
- 確保程式碼通過測試和格式檢查

