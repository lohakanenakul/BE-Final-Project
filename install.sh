#!/bin/bash

echo "Resume Parser Setup - Linux/macOS"
echo "=================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8+ from your package manager or https://python.org"
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Error: Python $required_version or higher is required (found $python_version)"
    exit 1
fi

echo "Creating virtual environment..."
python3 -m venv resume_parser_env
if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment"
    exit 1
fi

echo "Activating virtual environment..."
source resume_parser_env/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing dependencies..."
pip install streamlit spacy nltk PyPDF2 pdfplumber python-docx pandas openpyxl psycopg2-binary sqlalchemy
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

echo "Downloading spaCy model..."
python -m spacy download en_core_web_sm
if [ $? -ne 0 ]; then
    echo "Warning: Failed to download spaCy model"
    echo "You may need to run: python -m spacy download en_core_web_sm"
fi

echo ""
echo "Setup complete! To run the application:"
echo "1. Activate the environment: source resume_parser_env/bin/activate"
echo "2. Run the app: streamlit run app.py"
echo ""