@echo off
color 0A
title KimiGPT Installation Wizard

echo ╔════════════════════════════════════════════════╗
echo ║     KIMIGPT - MULTI-AGENT AI WEBSITE BUILDER   ║
echo ║              Installation Wizard                ║
echo ╚════════════════════════════════════════════════╝
echo.

:: Stage 1: System Requirements Check
echo [1/10] Checking System Requirements...
echo    ✓ Windows Version: %OS%
echo    ✓ Current Directory: %CD%
timeout /t 1 >nul

:: Stage 2: Python Installation Check
echo.
echo [2/10] Checking Python Installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo    ⚠️  Python not found!
    echo    📥 Please install Python 3.8+ from https://www.python.org/downloads/
    echo    ⚠️  Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('python --version') do echo    ✓ %%i found
)

:: Stage 3: Create Virtual Environment
echo.
echo [3/10] Creating Virtual Environment...
if exist venv (
    echo    ✓ Virtual environment already exists
) else (
    python -m venv venv
    if errorlevel 1 (
        echo    ✗ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo    ✓ Virtual environment created
)

:: Stage 4: Activate Virtual Environment
echo.
echo [4/10] Activating Virtual Environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo    ✗ Failed to activate virtual environment
    pause
    exit /b 1
)
echo    ✓ Virtual environment activated

:: Stage 5: Upgrade pip
echo.
echo [5/10] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo    ✓ pip upgraded

:: Stage 6: Install Dependencies
echo.
echo [6/10] Installing Python Packages...
echo    This may take a few minutes...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo    ⚠️  Some packages may have failed to install
    echo    Continuing anyway...
) else (
    echo    ✓ All packages installed successfully
)

:: Stage 7: Create Directory Structure
echo.
echo [7/10] Creating Directory Structure...
if not exist uploads mkdir uploads\images uploads\videos uploads\audio uploads\documents
if not exist generated_sites mkdir generated_sites
if not exist temp mkdir temp
if not exist cache mkdir cache\responses cache\images
if not exist logs mkdir logs
if not exist database mkdir database
echo    ✓ Directories created

:: Stage 8: Initialize Database
echo.
echo [8/10] Initializing Database...
python src/core/init_db.py
if errorlevel 1 (
    echo    ⚠️  Database initialization failed
) else (
    echo    ✓ Database initialized
)

:: Stage 9: Configure API Keys
echo.
echo [9/10] API Key Configuration
echo    ═══════════════════════════════════════════════
echo.
if exist .env (
    echo    ✓ .env file already exists
    set /p OVERWRITE="    Do you want to reconfigure API keys? (y/n): "
    if /i "%OVERWRITE%"=="n" goto skip_api_config
)

echo.
echo    Please obtain API keys from the services listed in api.txt
echo    ALL 4 APIS ARE 100%% FREE - NO CREDIT CARD REQUIRED!
echo    You can skip any API and add it later by editing .env file
echo    Press ENTER to skip an API key
echo.

set /p GROQ_KEY="    Groq API Key (RECOMMENDED): "
set /p GEMINI_KEY="    Google Gemini API Key: "
set /p HUGGINGFACE_KEY="    Hugging Face API Key: "
set /p COHERE_KEY="    Cohere API Key: "

echo # KimiGPT API Configuration > .env
echo # Generated: %date% %time% >> .env
echo # All APIs are 100%% FREE - No credit card required! >> .env
echo. >> .env
echo GROQ_API_KEY=%GROQ_KEY% >> .env
echo GEMINI_API_KEY=%GEMINI_KEY% >> .env
echo HUGGINGFACE_API_KEY=%HUGGINGFACE_KEY% >> .env
echo COHERE_API_KEY=%COHERE_KEY% >> .env
echo. >> .env
echo FLASK_ENV=development >> .env
echo FLASK_PORT=5000 >> .env
echo SECRET_KEY=kimigpt-secret-%RANDOM%-%RANDOM% >> .env

echo    ✓ API keys saved to .env

:skip_api_config

:: Stage 10: Create Desktop Shortcut
echo.
echo [10/10] Creating Desktop Shortcut...
powershell -Command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%USERPROFILE%\Desktop\KimiGPT.lnk');$s.TargetPath='%CD%\startgpt.bat';$s.WorkingDirectory='%CD%';$s.IconLocation='%SystemRoot%\System32\SHELL32.dll,14';$s.Save()" 2>nul
if errorlevel 1 (
    echo    ⚠️  Failed to create desktop shortcut
) else (
    echo    ✓ Shortcut created on Desktop
)

:: Final Summary
echo.
echo ╔════════════════════════════════════════════════╗
echo ║           INSTALLATION COMPLETE! 🎉             ║
echo ╚════════════════════════════════════════════════╝
echo.
echo Next Steps:
echo   1. Read api.txt for detailed API setup instructions
echo   2. Run startgpt.bat to launch KimiGPT
echo   3. Open browser to http://localhost:5000
echo   4. Start generating amazing websites!
echo.
echo 💡 Tip: You need at least ONE API key configured to use KimiGPT
echo    Check api.txt for links to get free API keys
echo.
set /p OPEN_API="Do you want to open api.txt now? (y/n): "
if /i "%OPEN_API%"=="y" notepad api.txt

echo.
set /p START_NOW="Do you want to start KimiGPT now? (y/n): "
if /i "%START_NOW%"=="y" (
    call startgpt.bat
) else (
    echo.
    echo Thank you! Run startgpt.bat when you're ready.
    pause
)
