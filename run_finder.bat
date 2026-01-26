@echo off
REM Windows Task Scheduler Wrapper Script
REM This script is called by Windows to run the bot and log execution.

REM 1. Navigate to the correct directory (Script's directory)
cd /d "%~dp0"

REM 2. Create logs folder if it doesn't exist
if not exist "logs" mkdir logs

REM 3. Run the bot and redirect ALL output (stdout and stderr) to log file
REM Appending to log file so we can see history.
echo [%DATE% %TIME%] Starting Daily Run via Task Scheduler >> logs\task_output.log
echo [%DATE% %TIME%] Running: python -m src.main >> logs\task_output.log

REM Run Python using 'python' command (assuming it's in PATH from setup)
REM If you have a specific venv, you'd use that python path here.
python -m src.main >> logs\task_output.log 2>&1

echo [%DATE% %TIME%] Finished Daily Run (Exit Code: %ERRORLEVEL%) >> logs\task_output.log
echo ----------------------------------------------------------- >> logs\task_output.log
