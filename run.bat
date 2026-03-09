@echo off
title Resume-Job Matching System Setup & Run
color 0A

echo ============================================================
echo   Resume-to-Job Matching System - Setup and Run
echo ============================================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.9+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed or not in PATH.
    echo Please install Node.js 18+ from https://nodejs.org/
    pause
    exit /b 1
)

:: Check npm
npm --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] npm is not installed or not in PATH.
    pause
    exit /b 1
)

echo [OK] Python found
echo [OK] Node.js found
echo [OK] npm found
echo.

:: ============================================================
:: BACKEND SETUP
:: ============================================================
echo ============================================================
echo   Step 1: Setting up Backend
echo ============================================================
echo.

cd backend

:: Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Install Python dependencies
echo Installing Python dependencies...
pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
if errorlevel 1 (
    echo [WARNING] Some packages may have failed to install. Continuing...
)
echo [OK] Python dependencies installed
echo.

:: Download NLTK data
echo Downloading NLTK data...
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('punkt_tab', quiet=True); nltk.download('stopwords', quiet=True); nltk.download('wordnet', quiet=True); nltk.download('averaged_perceptron_tagger', quiet=True); nltk.download('averaged_perceptron_tagger_eng', quiet=True)"
echo [OK] NLTK data downloaded
echo.

:: Download spaCy model
echo Downloading spaCy English model...
python -m spacy download en_core_web_sm >nul 2>&1
echo [OK] spaCy model downloaded
echo.

:: Create necessary directories
if not exist "data" mkdir data
if not exist "models" mkdir models

:: Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file with default settings...
    (
        echo MONGODB_URL=mongodb://localhost:27017
        echo DATABASE_NAME=resume_matching
        echo SECRET_KEY=your-secret-key-change-in-production
    ) > .env
    echo [OK] .env file created
)

:: Prepare training data and train models
echo.
echo ============================================================
echo   Step 2: Training ML Models
echo ============================================================
echo.

echo Preparing training data...
python scripts/prepare_data.py
if errorlevel 1 (
    echo [WARNING] Data preparation had issues. Continuing...
)

echo Training TF-IDF model...
python scripts/train_model.py
if errorlevel 1 (
    echo [WARNING] Model training had issues. Continuing...
)

echo Setting up MongoDB collections...
python scripts/setup_mongodb.py
if errorlevel 1 (
    echo [WARNING] MongoDB setup had issues. Make sure MongoDB is running.
    echo You can still start the app - MongoDB will be set up when the server starts.
)

echo.
echo [OK] ML models trained successfully
echo.

cd ..

:: ============================================================
:: FRONTEND SETUP
:: ============================================================
echo ============================================================
echo   Step 3: Setting up Frontend
echo ============================================================
echo.

cd frontend

:: Install Node.js dependencies
echo Installing frontend dependencies...
call npm install
if errorlevel 1 (
    echo [ERROR] Failed to install frontend dependencies
    pause
    exit /b 1
)
echo [OK] Frontend dependencies installed
echo.

cd ..

:: ============================================================
:: START SERVERS
:: ============================================================
echo ============================================================
echo   Step 4: Starting Application
echo ============================================================
echo.
echo   Backend API:  http://localhost:8000
echo   API Docs:     http://localhost:8000/docs
echo   Frontend:     http://localhost:3000
echo.
echo   Press Ctrl+C in each window to stop the servers.
echo ============================================================
echo.

:: Start backend server in a new window
echo Starting backend server...
start "Backend - Resume Matcher" cmd /k "cd backend && call venv\Scripts\activate.bat && python main.py"

:: Wait a moment for backend to start
timeout /t 3 /nobreak >nul

:: Start frontend server in a new window
echo Starting frontend server...
start "Frontend - Resume Matcher" cmd /k "cd frontend && npm start"

echo.
echo ============================================================
echo   Both servers are starting!
echo.
echo   1. Backend: http://localhost:8000 (API + Docs)
echo   2. Frontend: http://localhost:3000 (Web App)
echo.
echo   Make sure MongoDB is running on localhost:27017
echo   You can now create jobs, upload resumes, and calculate matches!
echo ============================================================
echo.
pause
