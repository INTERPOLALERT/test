@echo off
color 0E
title KimiGPT - Diagnostic Tool

echo ╔════════════════════════════════════════════════╗
echo ║        KIMIGPT DIAGNOSTIC TOOL                 ║
echo ║     Checking your installation...              ║
echo ╚════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

:: Check Python
echo [1/5] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python not found!
    echo.
    echo FIX: Install Python 3.7-3.11 from https://www.python.org/downloads/
    echo      Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

python --version
echo ✓ Python found
echo.

:: Check Virtual Environment
echo [2/5] Checking virtual environment...
if not exist "venv\Scripts\python.exe" (
    echo ✗ Virtual environment not found!
    echo.
    echo FIX: Run installgpt.bat first
    echo      Or create manually: python -m venv venv
    pause
    exit /b 1
)
echo ✓ Virtual environment exists
echo.

:: Check .env file
echo [3/5] Checking configuration...
if not exist ".env" (
    echo ⚠ .env file not found
    if exist ".env.example" (
        echo   Creating from .env.example...
        copy .env.example .env >nul
        echo ✓ Created .env file
    ) else (
        echo ✗ .env.example not found!
        pause
        exit /b 1
    )
) else (
    echo ✓ .env file exists
)

:: Check for API keys in .env
findstr /C:"GROQ_API_KEY=" .env | findstr /V "your-key-here" >nul
if not errorlevel 1 (
    echo ✓ Groq API key configured
    goto :api_found
)

findstr /C:"GEMINI_API_KEY=" .env | findstr /V "your-key-here" >nul
if not errorlevel 1 (
    echo ✓ Gemini API key configured
    goto :api_found
)

findstr /C:"HUGGINGFACE_API_KEY=" .env | findstr /V "your-token-here" >nul
if not errorlevel 1 (
    echo ✓ Hugging Face API key configured
    goto :api_found
)

findstr /C:"COHERE_API_KEY=" .env | findstr /V "your-key-here" >nul
if not errorlevel 1 (
    echo ✓ Cohere API key configured
    goto :api_found
)

echo ⚠ No API keys configured!
echo   You need at least ONE API key in .env file
echo   See api.txt for instructions
goto :after_api_check

:api_found
echo   At least one API key found

:after_api_check
echo.

:: Check if Flask is installed
echo [4/5] Checking required packages...
call venv\Scripts\activate.bat
python -c "import flask" 2>nul
if errorlevel 1 (
    echo ✗ Flask not installed!
    echo.
    echo FIX: Run this command:
    echo      venv\Scripts\activate
    echo      pip install -r requirements.txt
    pause
    exit /b 1
)
echo ✓ Flask installed

python -c "import dotenv" 2>nul
if errorlevel 1 (
    echo ⚠ python-dotenv not installed
) else (
    echo ✓ python-dotenv installed
)

python -c "import requests" 2>nul
if errorlevel 1 (
    echo ⚠ requests not installed
) else (
    echo ✓ requests installed
)
echo.

:: Run Python diagnostic
echo [5/5] Running comprehensive Python diagnostics...
echo ════════════════════════════════════════════════
echo.
python diagnose.py
if errorlevel 1 (
    echo.
    echo ✗ Diagnostic tests failed!
    echo   See errors above
    pause
    exit /b 1
)

echo.
echo ════════════════════════════════════════════════
echo.
echo  ✓ DIAGNOSTICS COMPLETE
echo.
echo  Your installation looks good!
echo  If you're still having issues, try these tests:
echo.
echo  1. Test minimal Flask: python test_flask_minimal.py
echo  2. Test full system: python test_system.py
echo  3. Read fix guide: INSTALL_FIX.md
echo.
pause
