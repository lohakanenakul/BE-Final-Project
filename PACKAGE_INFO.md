# Resume Parser Project Package

## Quick Start

### For Windows Users:
1. Download all project files to a folder
2. Double-click `install.bat` to set up everything automatically
3. Run: `streamlit run app.py`

### For Linux/macOS Users:
1. Download all project files to a folder
2. Run: `chmod +x install.sh && ./install.sh`
3. Run: `streamlit run app.py`

### Alternative Method:
1. Run: `python run.py` (handles setup automatically)

## Required Files for Standalone Deployment:

### Core Application Files:
- `app.py` - Main Streamlit web interface
- `resume_parser.py` - Core parsing logic
- `nlp_processor.py` - NLP and ML processing
- `text_extractors.py` - PDF/DOCX text extraction
- `data_exporter.py` - Export functionality

### Configuration Files:
- `.streamlit/config.toml` - Streamlit server settings
- `setup.py` - Python package configuration

### Setup and Documentation:
- `README.md` - Complete documentation
- `run.py` - Cross-platform application runner
- `install.bat` - Windows setup script
- `install.sh` - Linux/macOS setup script
- `PACKAGE_INFO.md` - This file

## Dependencies (Auto-installed):
- streamlit (Web interface)
- spacy (NLP processing)
- nltk (Text processing)
- PyPDF2 (PDF extraction)
- pdfplumber (Advanced PDF extraction)
- python-docx (Word document processing)
- pandas (Data manipulation)
- openpyxl (Excel export)

## System Requirements:
- Python 3.8 or higher
- 2GB RAM minimum
- Internet connection (for initial setup only)

## Features:
- Upload PDF/DOCX resumes
- Extract personal information, experience, education, skills
- ML-powered candidate scoring (0-100)
- Export to JSON, CSV, Excel
- Confidence metrics for extracted data
- Professional web interface

## Usage:
1. Start the application
2. Upload resume files through the web interface
3. View extracted and structured information
4. Download results in your preferred format

This is a complete, standalone package that runs independently in any Python environment.