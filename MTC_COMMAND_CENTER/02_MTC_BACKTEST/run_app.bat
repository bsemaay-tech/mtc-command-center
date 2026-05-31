@echo off
setlocal

REM Always run from this BAT's directory (fixes relative path issues)
cd /d "%~dp0"

set "PORT=8501"
if not "%~1"=="" set "PORT=%~1"

REM ========================================
REM  MTC Python Backtest & Optimization
REM  Windows Launcher
REM ========================================

echo.
echo ========================================
echo  MTC Python Backtest ^& Optimization
echo  Version: 1.0.0
echo ========================================
echo Usage: run_app.bat [PORT] (Default: 8501)
echo.

REM Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.11+
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo [INFO] Python version: %PYVER%

REM Create venv if not exists
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)

REM Activate venv
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/upgrade pip
python -m pip install --upgrade pip -q

REM Install requirements
echo [INFO] Checking dependencies...
pip install -r requirements.txt -q
if errorlevel 1 (
    echo [WARNING] Some dependencies may have failed to install
)
echo [OK] Dependencies ready

REM Create required directories
if not exist "data" mkdir data
if not exist "exports" mkdir exports
if not exist "exports\runs" mkdir exports\runs
if not exist "logs" mkdir logs

:CHECK_PORT
netstat -an | find ":%PORT% " >nul
if %errorlevel%==0 (
    echo [WARNING] Port %PORT% is in use.
    set /a PORT=%PORT%+1
    goto CHECK_PORT
)

REM Launch Streamlit
echo.
echo [INFO] Starting MTC Backtest Application...
echo [INFO] Opening browser at http://localhost:%PORT%
echo [INFO] Press Ctrl+C to stop the server
echo.

python -m streamlit run app.py ^
    --server.port %PORT% ^
    --server.headless false ^
    --browser.gatherUsageStats false ^
    --theme.base dark

if errorlevel 1 (
    echo.
    echo [ERROR] Application stopped with an error.
    echo If the error was "Port is not available", try running with a different port:
    echo Example: run_app.bat 8502
)

pause
