@echo off
REM Create the virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate the virtual environment (Windows)
echo Activating virtual environment...
call venv\Scripts\activate

REM Install pip if not available
echo Ensuring pip is installed...
python -m ensurepip --upgrade

REM Install dependencies from the packages folder (Offline)
echo Installing dependencies from local packages...
pip install --find-links=packages -r requirements.txt

REM Run the application
echo Running your application...
python app.py

REM Pause to keep the window open after the app runs
pause