# Rust 工具集

這個資料夾收集了使用 Rust 開發的跨平台命令列小工具。

## 為什麼選擇 Rust?

- **跨平台**: 單一程式碼庫可編譯到 Windows、Linux、macOS
- **高效能**: 編譯為原生程式碼,執行速度快
- **可靠性**: 記憶體安全,編譯時期即可捕捉大部分錯誤
- **獨立執行**: 編譯後的執行檔不需要額外的執行環境

## 目錄結構

```
rs/
├── dq/          - 移除字串前後雙引號的工具
├── kv-splitter/ - Key/Value 字串切割和格式化工具
├── tee/         - Windows tee 命令的 Rust 實作
├── release/     - 編譯後的執行檔和發布腳本
│   ├── dq.exe
│   ├── kv-splitter.exe
│   ├── tee.exe
│   └── updaters.py
└── RustInstructions.md
```

## 工具清單

### dq - 雙引號移除工具

從標準輸入讀取文字,移除前後的雙引號並輸出。

**使用範例:**
```powershell
echo '"hello"' | dq
# 輸出: hello
```

### tee - 標準輸入複製工具

從標準輸入讀取資料,同時輸出到標準輸出和指定的檔案。

**使用範例:**
```powershell
# 基本用法
echo "Hello" | tee output.txt

# 附加模式
echo "World" | tee -a output.txt
```

詳細說明請參考 [tee/README.md](tee/README.md)

### kv-splitter - Key/Value 字串切割工具

從標準輸入讀取 key/value 格式的字串，進行切割和格式化輸出。支援預定義的 pattern（如 PATH、Cookies）或自訂分隔字元。

**使用範例:**
```powershell
# PATH 環境變數格式化
echo "C:\Python313\Scripts\;C:\Python313\" | kv-splitter -p path

# Cookies 格式化
echo "_device_id=abc123; _octo=GH1.1" | kv-splitter -p cookies

# 自訂分隔字元
echo "name:John,age:30" | kv-splitter -i "," -k ":" -I "\n" -K " = "
```

詳細說明請參考 [kv-splitter/README.md](kv-splitter/README.md)

## 開發環境設定

### 安裝 Rust

1. 從 [rustup.rs](https://rustup.rs/) 下載並安裝 Rust 工具鏈
2. 安裝後會包含:
   - `rustc`: Rust 編譯器
   - `cargo`: Rust 套件管理和建構工具
   - `rustup`: Rust 工具鏈管理器

### 驗證安裝

```powershell
rustc --version
cargo --version
```

## 建構與編譯

### 建構單一專案

```powershell
# 進入專案資料夾
cd rs\dq

# 除錯建構
cargo build

# 發布建構(最佳化)
cargo build --release
```

編譯後的執行檔位置:
- 除錯版本: `target\debug\<專案名稱>.exe`
- 發布版本: `target\release\<專案名稱>.exe`

### 執行專案

```powershell
# 直接執行(會自動建構)
cargo run

# 傳遞參數
cargo run -- arg1 arg2

# 執行測試
cargo test
```

### 清理建構產物

```powershell
cargo clean
```

## 建立新工具

### 使用 cargo 建立新專案

```powershell
# 在 rs 資料夾下
cd rs

# 建立新的二進位專案
cargo new <工具名稱>

# 例如:
cargo new mytool
```

### 專案結構

```
<工具名稱>/
├── Cargo.toml      - 專案設定檔
└── src/
    └── main.rs     - 主程式
```

### 基本程式碼範本

```rust
use std::io;

fn main() {
    println!("Hello from my tool!");
    
    // 讀取命令列參數
    let args: Vec<String> = std::env::args().collect();
    
    // 處理邏輯
    // ...
}
```

## 發布流程

1. 確保程式碼通過測試: `cargo test`
2. 建構發布版本: `cargo build --release`
3. 測試執行檔功能
4. 將執行檔複製到 `release` 資料夾
5. 更新相關文件

## 最佳實務

### 錯誤處理

```rust
use std::io::{self, Read};

fn main() {
    if let Err(e) = run() {
        eprintln!("錯誤: {}", e);
        std::process::exit(1);
    }
}

fn run() -> io::Result<()> {
    // 主要邏輯
    Ok(())
}
```

### 命令列參數處理

對於簡單的參數,使用 `std::env::args()`:

```rust
let args: Vec<String> = std::env::args().collect();
```

對於複雜的參數,考慮使用 `clap` 套件:

```toml
[dependencies]
clap = { version = "4.5", features = ["derive"] }
```

**實際範例:**
- `kv-splitter` 使用 clap 處理命令列參數,支援多種選項和預定義 pattern

### 測試

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_function() {
        assert_eq!(my_function(input), expected_output);
    }
}
```

## 常用 cargo 命令

```powershell
# 檢查程式碼(不編譯)
cargo check

# 格式化程式碼
cargo fmt

# 程式碼檢查(linter)
cargo clippy

# 更新相依套件
cargo update

# 顯示相依樹
cargo tree

# 產生文件
cargo doc --open
```

## 效能優化

### Cargo.toml 設定

```toml
[profile.release]
opt-level = 3        # 最高最佳化等級
lto = true          # 連結時期最佳化
codegen-units = 1   # 減少程式碼分段以提升效能
strip = true        # 移除除錯符號以減小檔案大小
```

## 疑難排解

### 編譯錯誤

- 仔細閱讀錯誤訊息,Rust 的錯誤訊息通常很詳細
- 使用 `cargo check` 快速檢查語法
- 查看 [Rust 官方文件](https://doc.rust-lang.org/)

### 執行時期錯誤

- 使用 `cargo run` 執行除錯版本,會有更好的錯誤訊息
- 加入適當的錯誤處理和日誌輸出

## 學習資源

- [The Rust Programming Language (Book)](https://doc.rust-lang.org/book/)
- [Rust by Example](https://doc.rust-lang.org/rust-by-example/)
- [Rust Standard Library Documentation](https://doc.rust-lang.org/std/)
- [Rust Cookbook](https://rust-lang-nursery.github.io/rust-cookbook/)

## 貢獻指南

1. 確保程式碼符合 Rust 慣例: `cargo fmt` 和 `cargo clippy`
2. 撰寫測試: `cargo test`
3. 更新相關文件(README.md)
4. 提交前確認發布建構正常: `cargo build --release`
