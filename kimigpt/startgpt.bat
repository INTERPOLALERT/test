@echo off
color 0B
title KimiGPT - Multi-Agent Website Builder

echo ╔════════════════════════════════════════════════╗
echo ║              KIMIGPT LAUNCHER                   ║
echo ║       Multi-Agent AI Website Builder            ║
echo ╚════════════════════════════════════════════════╝
echo.

:: Change to script directory
cd /d "%~dp0"

:: Pre-flight Checks
echo [⏳] Running Pre-Flight Checks...
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+
    echo    Download from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
echo ✓ Python OK

:: Check Virtual Environment
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found!
    echo    Please run installgpt.bat first
    echo.
    pause
    exit /b 1
)
echo ✓ Virtual Environment OK

:: Check .env file
if not exist ".env" (
    echo ⚠️  No .env file found!
    echo    Creating from .env.example...
    copy .env.example .env >nul
    echo.
    echo ⚠️  IMPORTANT: Please configure API keys in .env file
    echo    See api.txt for instructions
    echo.
    set /p CONTINUE="Continue anyway? (y/n): "
    if /i not "%CONTINUE%"=="y" exit /b 1
)
echo ✓ Configuration OK

:: Activate Virtual Environment
echo.
echo [🔧] Activating Virtual Environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual Environment Activated

:: Check for required packages
echo.
echo [📦] Checking Required Packages...
python -c "import flask" 2>nul
if errorlevel 1 (
    echo ⚠️  Flask not found. Installing dependencies...
    pip install -r requirements.txt --quiet
)
echo ✓ Dependencies OK

:: Test API Connections
echo.
echo [🔍] Testing API Connections...
python src/api/test_apis.py 2>nul
echo.

:: Start Services
echo [🚀] Starting KimiGPT Services...
echo.
echo    ► Starting Multi-Agent System...
echo    ► Starting API Manager (Smart Rotation)...
echo    ► Starting Web Interface...
echo.

:: Get port from environment or use default
set PORT=5000
for /f "tokens=2 delims==" %%a in ('findstr "FLASK_PORT" .env 2^>nul') do set PORT=%%a

:: Display ready message and launch
echo.
echo ╔════════════════════════════════════════════════╗
echo ║         STARTING KIMIGPT... 🚀                  ║
echo ║                                                 ║
echo ║  After server starts (2-3 seconds):            ║
echo ║  Dashboard:    http://localhost:%PORT%
echo ║  Generator:    http://localhost:%PORT%/generate
echo ║  API Status:   http://localhost:%PORT%/api/status
echo ║                                                 ║
echo ║  Browser will open automatically in 5 seconds  ║
echo ║  Press Ctrl+C to stop the server               ║
echo ╚════════════════════════════════════════════════╝
echo.

:: Open browser after delay (gives Flask time to start)
start "" cmd /c "timeout /t 5 /nobreak >nul && start http://localhost:%PORT%"

:: Start the Flask application (foreground so we can see logs)
echo [📊] Server Logs:
echo ════════════════════════════════════════════════
echo.

python src/ui/app.py

:: If server stops
echo.
echo.
echo ════════════════════════════════════════════════
echo Server stopped.
echo.
pause
