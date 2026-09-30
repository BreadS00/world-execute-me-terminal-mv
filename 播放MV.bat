@echo off
rem ============================================================
rem  world.execute(me) -- terminal ascii MV launcher
rem  double-click this file. running it = world.execute(me).
rem  on normal end the script clears the screen, prints its
rem  termination report + exit code, then the window closes.
rem  (pause only happens if python itself crashed)
rem ============================================================
setlocal
cd /d "%~dp0"
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
where python >nul 2>nul
if errorlevel 1 (
    echo [error] python not found in PATH. please install Python 3.8+
    pause
    exit /b 1
)
start "world.execute(me)" /max cmd /c "chcp 65001 >nul & python -X utf8 world_execute_me_mv.py & if errorlevel 1 if not errorlevel 130 pause"
endlocal
