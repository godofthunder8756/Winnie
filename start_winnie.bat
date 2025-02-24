@echo off
REM Activate virtual environment and start Winnie without showing command prompt
start /min "" cmd /c "cd /d %~dp0 && .venv\Scripts\activate && pythonw src\main.py"