@echo off
REM Messenger Bot - Quick Start Script for Windows
REM This script starts Django, Celery Worker, and Celery Beat in separate windows

setlocal enabledelayedexpansion

REM Colors
set "GREEN=[92m"
set "YELLOW=[93m"
set "RED=[91m"
set "RESET=[0m"

echo.
echo ========================================
echo   Messenger Bot - Starting Services
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "manage.py" (
    echo ERROR: manage.py not found!
    echo Please run this script from the messenger-bot directory
    pause
    exit /b 1
)

REM Start Django Server
echo [*] Starting Django Development Server...
echo     Access at: http://localhost:8000
start "Django Server" cmd /k python manage.py runserver
timeout /t 2 >nul

REM Start Celery Worker
echo [*] Starting Celery Worker...
echo     This executes scheduled message tasks
start "Celery Worker" cmd /k celery -A config worker -l info
timeout /t 2 >nul

REM Start Celery Beat
echo [*] Starting Celery Beat Scheduler...
echo     This schedules messages to be sent
start "Celery Beat" cmd /k celery -A config beat -l info
timeout /t 2 >nul

echo.
echo ========================================
echo [✓] All services started!
echo ========================================
echo.
echo Services running:
echo   1. Django Server - Terminal 1
echo   2. Celery Worker - Terminal 2
echo   3. Celery Beat   - Terminal 3
echo.
echo To stop services:
echo   - Close each terminal window or press Ctrl+C
echo.
echo Troubleshooting:
echo   - Check CELERY_SETUP.md for detailed instructions
echo   - Verify Facebook token in .env file
echo   - Make sure Redis connection is working
echo.
pause
