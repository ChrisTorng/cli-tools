use std::env;
use std::fs::OpenOptions;
use std::io::{self, BufRead, BufReader, Write};
use std::path::Path;

fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect();
    
    // 檢查是否有 -a (append) 參數
    let mut append_mode = false;
    let mut file_paths: Vec<String> = Vec::new();
    
    let mut i = 1;
    while i < args.len() {
        if args[i] == "-a" || args[i] == "--append" {
            append_mode = true;
        } else {
            file_paths.push(args[i].clone());
        }
        i += 1;
    }
    
    // 開啟檔案
    let mut files: Vec<Box<dyn Write>> = Vec::new();
    for path in &file_paths {
        let file = OpenOptions::new()
            .create(true)
            .write(true)
            .append(append_mode)
            .truncate(!append_mode)
            .open(Path::new(path))?;
        files.push(Box::new(file));
    }
    
    // 讀取標準輸入並寫入
    let stdin = io::stdin();
    let reader = BufReader::new(stdin);
    let mut stdout = io::stdout();
    
    for line in reader.lines() {
        let line = line?;
        
        // 寫入標準輸出
        writeln!(stdout, "{}", line)?;
        
        // 寫入所有檔案
        for file in &mut files {
            writeln!(file, "{}", line)?;
        }
    }
    
    // 確保所有輸出都被寫入
    stdout.flush()?;
    for file in &mut files {
        file.flush()?;
    }
    
    Ok(())
}
