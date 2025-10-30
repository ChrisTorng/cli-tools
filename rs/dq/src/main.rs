use std::io::{self, Read};

fn main() {
    let mut input = String::new();
    
    // 從 stdin 讀取所有輸入
    if let Err(e) = io::stdin().read_to_string(&mut input) {
        eprintln!("讀取輸入時發生錯誤: {}", e);
        std::process::exit(1);
    }
    
    // 移除前後的雙引號
    let output = remove_quotes(&input);
    
    // 輸出到 stdout
    print!("{}", output);
}

fn remove_quotes(s: &str) -> String {
    let bytes = s.as_bytes();
    let len = bytes.len();
    
    // 如果字串長度小於 2，或前後不是雙引號，直接返回原字串
    if len < 2 || bytes[0] != b'"' || bytes[len - 1] != b'"' {
        return s.to_string();
    }
    
    // 移除前後各一個雙引號
    s[1..len-1].to_string()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_remove_quotes() {
        assert_eq!(remove_quotes(r#""hello""#), "hello");
        assert_eq!(remove_quotes(r#""test"#), r#""test"#);
        assert_eq!(remove_quotes(r#"test""#), r#"test""#);
        assert_eq!(remove_quotes("test"), "test");
        assert_eq!(remove_quotes(r#""""#), "");
        assert_eq!(remove_quotes(r#""a""#), "a");
    }
}
