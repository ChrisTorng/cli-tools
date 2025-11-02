use clap::Parser;
use std::io::{self, Read};

#[derive(Parser)]
#[command(name = "kv-splitter")]
#[command(about = "切割並格式化 key/value 字串", long_about = None)]
struct Args {
    /// 使用預定義的 pattern (path, cookies)
    #[arg(short, long)]
    pattern: Option<String>,

    /// 項目間的分隔字元
    #[arg(short = 'i', long, default_value = ";")]
    item_separator: String,

    /// key/value 之間的分隔字元（如果沒有則視為純項目列表）
    #[arg(short = 'k', long)]
    kv_separator: Option<String>,

    /// 項目間的替代字元
    #[arg(short = 'I', long, default_value = "\\n")]
    item_replacement: String,

    /// key/value 之間的替代字元
    #[arg(short = 'K', long, default_value = "\\t")]
    kv_replacement: String,
}

struct SplitConfig {
    item_separator: String,
    kv_separator: Option<String>,
    item_replacement: String,
    kv_replacement: String,
}

impl SplitConfig {
    fn from_pattern(pattern: &str) -> Option<Self> {
        match pattern.to_lowercase().as_str() {
            "path" => Some(Self {
                item_separator: ";".to_string(),
                kv_separator: None,
                item_replacement: "\n".to_string(),
                kv_replacement: "\t".to_string(),
            }),
            "cookies" => Some(Self {
                item_separator: ";".to_string(),
                kv_separator: Some("=".to_string()),
                item_replacement: "\n".to_string(),
                kv_replacement: "\t".to_string(),
            }),
            _ => None,
        }
    }

    fn from_args(args: &Args) -> Self {
        Self {
            item_separator: args.item_separator.clone(),
            kv_separator: args.kv_separator.clone(),
            item_replacement: unescape(&args.item_replacement),
            kv_replacement: unescape(&args.kv_replacement),
        }
    }
}

fn unescape(s: &str) -> String {
    s.replace("\\n", "\n")
        .replace("\\t", "\t")
        .replace("\\r", "\r")
        .replace("\\\\", "\\")
}

fn process_input(input: &str, config: &SplitConfig) -> String {
    let items: Vec<&str> = input
        .split(&config.item_separator)
        .map(|s| s.trim())
        .filter(|s| !s.is_empty())
        .collect();

    let processed_items: Vec<String> = items
        .iter()
        .map(|item| {
            if let Some(kv_sep) = &config.kv_separator {
                if let Some(pos) = item.find(kv_sep.as_str()) {
                    let (key, value) = item.split_at(pos);
                    let value = &value[kv_sep.len()..];
                    return format!(
                        "{}{}{}",
                        key.trim(),
                        config.kv_replacement,
                        value.trim()
                    );
                }
            }
            item.to_string()
        })
        .collect();

    processed_items.join(&config.item_replacement)
}

fn main() -> io::Result<()> {
    let args = Args::parse();

    let config = if let Some(pattern) = &args.pattern {
        SplitConfig::from_pattern(pattern).unwrap_or_else(|| {
            eprintln!("警告: 未知的 pattern '{}'，使用預設設定", pattern);
            SplitConfig::from_args(&args)
        })
    } else {
        SplitConfig::from_args(&args)
    };

    let mut input = String::new();
    io::stdin().read_to_string(&mut input)?;

    let output = process_input(&input, &config);
    println!("{}", output);

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_path_pattern() {
        let config = SplitConfig::from_pattern("path").unwrap();
        let input = "C:\\Python313\\Scripts\\;C:\\Python313\\;C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v12.8\\bin";
        let expected = "C:\\Python313\\Scripts\\\nC:\\Python313\\\nC:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v12.8\\bin";
        assert_eq!(process_input(input, &config), expected);
    }

    #[test]
    fn test_cookies_pattern() {
        let config = SplitConfig::from_pattern("cookies").unwrap();
        let input = "_device_id=abc123; _octo=GH1.1.1471563711.1750766196; saved_user_sessions=123abc";
        let expected = "_device_id\tabc123\n_octo\tGH1.1.1471563711.1750766196\nsaved_user_sessions\t123abc";
        assert_eq!(process_input(input, &config), expected);
    }

    #[test]
    fn test_custom_separators() {
        let config = SplitConfig {
            item_separator: ",".to_string(),
            kv_separator: Some(":".to_string()),
            item_replacement: "\n".to_string(),
            kv_replacement: " = ".to_string(),
        };
        let input = "name:John, age:30, city:Taipei";
        let expected = "name = John\nage = 30\ncity = Taipei";
        assert_eq!(process_input(input, &config), expected);
    }
}
