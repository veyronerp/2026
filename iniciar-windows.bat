@echo off
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (py -3 monitor.py %*) else (python monitor.py %*)
pause
