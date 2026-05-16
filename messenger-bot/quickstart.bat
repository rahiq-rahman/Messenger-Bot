@echo off
REM Messenger Bot - Quick Start Script (Windows)
REM This script automates the setup process

echo.
echo ===============================================================
echo  Messenger Bot - Quick Start Setup (Windows)
echo ===============================================================
echo.

REM Check Python
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo OK - Python %PYTHON_VERSION% found
echo.

REM Check Redis
echo [2/6] Checking Redis installation...
redis-cli.exe --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Redis is not installed or not in PATH
    echo Installing Redis is recommended for production
    echo Download from: https://github.com/microsoftarchive/redis/releases
    echo Or use WSL2: wsl sudo apt-get install redis-server
    echo.
    echo For now, you can continue but you'll need Redis running later
    pause
)
echo.

REM Create virtual environment
echo [3/6] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists
) else (
    python -m venv venv
    echo OK - Virtual environment created
)
echo.

REM Activate virtual environment
echo [4/6] Activating virtual environment...
call venv\Scripts\activate.bat
echo OK - Virtual environment activated
echo.

REM Install dependencies
echo [5/6] Installing dependencies...
echo This may take a few minutes...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo OK - Dependencies installed
echo.

REM Create .env file
echo [6/6] Setting up configuration...
if not exist .env (
    copy .env.example .env
    echo IMPORTANT: Edit .env file with your Facebook credentials!
    echo You'll need:
    echo   - FACEBOOK_PAGE_ACCESS_TOKEN
    echo   - FACEBOOK_VERIFY_TOKEN
)
echo.

REM Run migrations
echo Running database migrations...
python manage.py makemigrations
python manage.py migrate
echo OK - Migrations completed
echo.

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput
echo OK - Static files collected
echo.

REM Create superuser
echo.
echo Creating superuser account...
python manage.py createsuperuser
echo.

REM Done
echo.
echo ===============================================================
echo  Setup Complete!
echo ===============================================================
echo.
echo NEXT STEPS:
echo.
echo 1. Edit .env file with your Facebook credentials
echo    (Open .env in your text editor)
echo.
echo 2. You need to run 4 applications (open 4 Command Prompts):
echo.
echo    Command Prompt 1 - Django Web Server:
echo    venv\Scripts\activate.bat
echo    python manage.py runserver
echo.
echo    Command Prompt 2 - Redis Server:
echo    redis-server.exe
echo    (Or: redis-server if installed via WSL)
echo.
echo    Command Prompt 3 - Celery Worker:
echo    venv\Scripts\activate.bat
echo    celery -A config worker --loglevel=info
echo.
echo    Command Prompt 4 - Celery Beat Scheduler:
echo    venv\Scripts\activate.bat
echo    celery -A config beat --loglevel=info
echo.
echo 3. Open your browser and go to:
echo    http://localhost:8000
echo.
echo 4. Login with your superuser credentials
echo.
echo 5. Go to Groups tab and add your Facebook groups!
echo.
echo Documents:
echo   - SETUP_GUIDE.md - Detailed setup instructions
echo   - README.md - Full documentation
echo.
pause
