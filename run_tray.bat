@echo off
cd /d %~dp0
call venv\Scripts\activate
pythonw run_with_tray.py