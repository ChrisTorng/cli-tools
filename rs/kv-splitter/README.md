# kv-splitter

一個用於切割和格式化 key/value 字串的命令列工具。

## 功能

- 從 stdin 讀取輸入，處理後輸出到 stdout
- 支援預定義的 pattern（path、cookies）
- 支援自訂分隔字元和替代字元
- 可擴充的 pattern 系統

## 安裝

```bash
cargo build --release
```

## 使用方式

### 使用預定義 pattern

#### PATH 環境變數處理

```bash
echo "C:\Python313\Scripts\;C:\Python313\;C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8\bin" | kv-splitter -p path
```

輸出：
```
C:\Python313\Scripts\
C:\Python313\
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8\bin
```

#### Cookies 處理

```bash
echo "_device_id=abc123; _octo=GH1.1.1471563711.1750766196; saved_user_sessions=123abc" | kv-splitter -p cookies
```

輸出：
```
_device_id	abc123
_octo	GH1.1.1471563711.1750766196
saved_user_sessions	123abc
```

### 自訂分隔字元

```bash
echo "name:John,age:30,city:Taipei" | kv-splitter -i "," -k ":" -I "\n" -K " = "
```

輸出：
```
name = John
age = 30
city = Taipei
```

## 參數說明

- `-p, --pattern <PATTERN>` - 使用預定義的 pattern（path 或 cookies）
- `-i, --item-separator <SEP>` - 項目間的分隔字元（預設：`;`）
- `-k, --kv-separator <SEP>` - key/value 之間的分隔字元（可選）
- `-I, --item-replacement <REP>` - 項目間的替代字元（預設：`\n`）
- `-K, --kv-replacement <REP>` - key/value 之間的替代字元（預設：`\t`）

## 預定義 Pattern

### path
- 項目分隔：`;`
- 無 key/value 分隔
- 項目替代：換行符號 `\n`

### cookies
- 項目分隔：`;`
- key/value 分隔：`=`
- 項目替代：換行符號 `\n`
- key/value 替代：跳格符號 `\t`

## 擴充 Pattern

要新增新的 pattern，只需在 `src/main.rs` 的 `SplitConfig::from_pattern` 函式中加入新的 match 分支：

```rust
"your-pattern" => Some(Self {
    item_separator: "分隔字元".to_string(),
    kv_separator: Some("key/value分隔字元".to_string()),
    item_replacement: "項目替代字元".to_string(),
    kv_replacement: "key/value替代字元".to_string(),
}),
```

## 測試

```bash
cargo test
```

## 授權

MIT

