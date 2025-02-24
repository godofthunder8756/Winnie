@echo off
setlocal enabledelayedexpansion

REM Get the directory where the batch file is located
set "WINNIE_DIR=%~dp0"

REM Check if virtual environment exists
if not exist "%WINNIE_DIR%.venv\Scripts\activate" (
    echo Virtual environment not found. Creating...
    python -m venv .venv
    if errorlevel 1 (
        echo Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Create a VBS script to run the command hidden
echo Set WshShell = CreateObject("WScript.Shell") > "%TEMP%\run_winnie.vbs"
echo WshShell.Run chr(34) ^& "%WINNIE_DIR%.venv\Scripts\pythonw.exe" ^& chr(34) ^& " %WINNIE_DIR%src\main.py", 0 >> "%TEMP%\run_winnie.vbs"

REM Run the VBS script
start "" /b wscript.exe "%TEMP%\run_winnie.vbs"

REM Clean up
del "%TEMP%\run_winnie.vbs" 