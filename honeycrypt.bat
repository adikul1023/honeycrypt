@echo off
REM HoneyCrypt CLI Wrapper Script for Windows CMD
REM This script uses the python command from your PATH

setlocal

REM Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"

REM Check if virtual environment exists
if exist "%SCRIPT_DIR%.venv\Scripts\python.exe" (
    "%SCRIPT_DIR%.venv\Scripts\python.exe" "%SCRIPT_DIR%honeycrypt_cli.py" %*
) else if exist "%SCRIPT_DIR%venv\Scripts\python.exe" (
    "%SCRIPT_DIR%venv\Scripts\python.exe" "%SCRIPT_DIR%honeycrypt_cli.py" %*
) else (
    REM Use python from PATH
    python "%SCRIPT_DIR%honeycrypt_cli.py" %*
)
