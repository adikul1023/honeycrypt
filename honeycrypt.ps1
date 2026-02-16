# HoneyCrypt CLI Wrapper Script for Windows PowerShell
# This script automatically uses the virtual environment if available

# Get the directory where this script is located
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Check if virtual environment exists
if (Test-Path "$ScriptDir\.venv\Scripts\python.exe") {
    & "$ScriptDir\.venv\Scripts\python.exe" "$ScriptDir\honeycrypt_cli.py" $args
} elseif (Test-Path "$ScriptDir\venv\Scripts\python.exe") {
    & "$ScriptDir\venv\Scripts\python.exe" "$ScriptDir\honeycrypt_cli.py" $args
} else {
    # Use python from PATH
    & python "$ScriptDir\honeycrypt_cli.py" $args
}
