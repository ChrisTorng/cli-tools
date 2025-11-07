@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "REPO_DIR=%SCRIPT_DIR%.."
set "REPO_URL=https://github.com/ChrisTorng/cli-tools"

echo === 更新 cli-tools 倉儲 ===
cd /d "%REPO_DIR%"
git pull origin main

echo.
echo === 下載 Rust 工具 ===
python "%REPO_DIR%\py\dl-latest-rs.py" "%REPO_URL%" "%REPO_DIR%\rs\release\"