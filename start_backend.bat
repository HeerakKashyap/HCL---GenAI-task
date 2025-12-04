@echo off
echo Starting RAG Backend Server...
echo.
cd /d "%~dp0"
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv venv
    pause
    exit /b 1
)
call venv\Scripts\activate.bat
echo Virtual environment activated
echo.
echo Installing/checking dependencies...
pip install -q -r requirements.txt
echo.
echo Starting Flask server...
python app.py
pause

