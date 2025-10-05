@echo off
REM Setup script for Playwright Website Validator
REM Run this script to set up the project

echo ========================================
echo Playwright Website Validator - Setup
echo ========================================
echo.

REM Check Python installation
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)
python --version
echo.

REM Create virtual environment (optional)
echo [2/4] Do you want to create a virtual environment? (recommended)
set /p CREATE_VENV="Create venv? (y/n): "
if /i "%CREATE_VENV%"=="y" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created!
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
    echo.
)

REM Install dependencies
echo [3/4] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

REM Install Playwright browsers
echo [4/4] Installing Playwright browsers...
playwright install chromium
if errorlevel 1 (
    echo ERROR: Failed to install Playwright browsers
    pause
    exit /b 1
)
echo Playwright browsers installed successfully!
echo.

REM Create .env file if not exists
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo .env file created! Please edit it with your settings.
    echo.
)

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file with your target URL (optional)
echo 2. Run: python run.py
echo.
echo For tests, run: pytest
echo.
pause
