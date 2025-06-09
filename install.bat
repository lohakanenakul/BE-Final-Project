@echo off
echo Resume Parser Setup - Windows
echo ============================

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Creating virtual environment...
python -m venv resume_parser_env
if errorlevel 1 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)

echo Activating virtual environment...
call resume_parser_env\Scripts\activate

echo Installing dependencies...
pip install streamlit spacy nltk PyPDF2 pdfplumber python-docx pandas openpyxl psycopg2-binary sqlalchemy
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo Downloading spaCy model...
python -m spacy download en_core_web_sm
if errorlevel 1 (
    echo Warning: Failed to download spaCy model
    echo You may need to run: python -m spacy download en_core_web_sm
)

echo.
echo Setup complete! To run the application:
echo 1. Activate the environment: resume_parser_env\Scripts\activate
echo 2. Run the app: streamlit run app.py
echo.
pause