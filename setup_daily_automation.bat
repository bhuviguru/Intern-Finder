@echo off
REM Internship Bot - Windows Task Scheduler Setup
echo ================================================
echo  Internship Bot - Automatic Daily Setup
echo ================================================
echo.

REM Get current directory
set BOT_DIR=%~dp0
cd /d "%BOT_DIR%"

REM Find Python installation
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python not found in PATH!
    echo Please install Python or add it to PATH
    pause
    exit /b 1
)

REM Get Python path
for /f "delims=" %%i in ('where python') do set PYTHON_PATH=%%i
echo Found Python at: %PYTHON_PATH%

REM Install dependencies
echo.
echo Installing dependencies...
echo.
"%PYTHON_PATH%" -m pip install -r requirements.txt
"%PYTHON_PATH%" -m playwright install chromium

REM Check for .env file
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Creating template .env file...
    echo SMTP_EMAIL=your_email@gmail.com > .env
    echo SMTP_PASSWORD=your_app_password >> .env
    echo SMTP_SERVER=smtp.gmail.com >> .env
    echo SMTP_PORT=587 >> .env
    echo.
    echo Please edit .env file with your credentials before running!
    pause
    exit /b 1
)

REM Create the task
echo.
echo Creating Windows Task Scheduler task...
echo This will make the bot run EVERY DAY at 9:00 AM automatically.
echo.

echo.
echo Executing Advanced Setup via PowerShell...
PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& '%~dp0setup_task.ps1'"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================
    echo  SUCCESS! Task created successfully!
    echo ================================================
    echo.
    echo The bot will now run EVERY DAY at 9:00 AM
    echo Even if you restart your computer!
    echo.
    echo To check logs:
    echo   Open logs\task_output.log
    echo.
    echo To test it right now manually:
    echo   Double-click run_finder.bat
    echo.
    echo To see the task in Task Scheduler:
    echo   Press Win+R, type: taskschd.msc
    echo.
) else (
    echo.
    echo ERROR: Failed to create task!
    echo Please run this script as Administrator
    echo.
)

pause
