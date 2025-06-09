# Resume Parser - Complete Source Code Package

## Project Overview
A comprehensive Resume Parser application using Machine Learning and Natural Language Processing with PostgreSQL database integration for automated recruitment screening.

## Quick Start (Choose One Method)

### Method 1: Simplest Setup
```bash
python simple_run.py
```

### Method 2: Manual Setup
```bash
pip install streamlit spacy nltk PyPDF2 pdfplumber python-docx pandas openpyxl sqlalchemy
python -m spacy download en_core_web_sm
streamlit run app.py
```

### Method 3: Automated Setup
```bash
python run.py
```

## Complete File List

### Core Application Files
1. **app.py** - Main Streamlit web interface with multi-page navigation
2. **resume_parser.py** - Core parsing logic with ML algorithms  
3. **nlp_processor.py** - NLP processing using spaCy and NLTK
4. **text_extractors.py** - PDF and DOCX text extraction engines
5. **data_exporter.py** - Export functionality (JSON, CSV, Excel)
6. **database_manager.py** - Database operations and models
7. **config.py** - Configuration settings and environment handling

### Setup and Installation
8. **simple_run.py** - Easiest way to run (handles everything automatically)
9. **run.py** - Cross-platform application runner with dependency management
10. **setup.py** - Python package configuration
11. **dependencies.txt** - Required packages list
12. **install.bat** - Windows automated installer
13. **install.sh** - Linux/macOS automated installer

### Configuration
14. **.streamlit/config.toml** - Streamlit server settings

### Documentation
15. **README.md** - Complete project documentation
16. **INSTALLATION_GUIDE.md** - Detailed installation instructions
17. **PACKAGE_INFO.md** - Quick start guide
18. **COMPLETE_SOURCE_CODE.md** - This file

## Application Features

### Main Interface Pages
1. **Upload & Parse Resumes** - Upload and process resume files
2. **View Stored Resumes** - Browse and manage saved resume data
3. **Search Database** - Search resumes by name, email, location, filename
4. **Analytics Dashboard** - View statistics and processing metrics

### Core Capabilities
- Parse PDF and DOCX resume files
- Extract personal information, work experience, education, skills
- ML-powered candidate scoring (0-100 points)
- Database storage with PostgreSQL or SQLite
- Export results to JSON, CSV, Excel formats
- Search and analytics functionality
- Confidence scoring for extracted data

### Database Features
- Automatic table creation
- Resume data persistence
- Search and filtering
- Analytics and statistics
- Error tracking and logging

## System Requirements
- Python 3.8 or higher
- 2GB RAM minimum
- 500MB disk space
- Internet connection (initial setup only)

## Dependencies
- streamlit (Web interface)
- spacy (NLP processing)
- nltk (Text processing)
- PyPDF2 (PDF extraction)
- pdfplumber (Advanced PDF parsing)
- python-docx (Word document processing)
- pandas (Data manipulation)
- openpyxl (Excel export)
- sqlalchemy (Database ORM)
- psycopg2-binary (PostgreSQL driver, optional)

## Environment Configuration

### Database Options
**SQLite (Default)** - No setup required, stores data locally
```bash
# Automatically uses SQLite if no DATABASE_URL is set
```

**PostgreSQL (Production)**
```bash
export DATABASE_URL="postgresql://user:password@host:port/database"
```

### Optional Settings
```bash
export SQLITE_DB_PATH="custom_resume_parser.db"
```

## Usage Instructions

1. **Start Application**
   ```bash
   python simple_run.py
   # OR
   streamlit run app.py
   ```

2. **Access Interface**
   - Open browser to `http://localhost:8501`
   - Navigate using sidebar menu

3. **Upload Resumes**
   - Go to "Upload & Parse Resumes"
   - Select PDF or DOCX files
   - View extracted structured data
   - Data automatically saves to database

4. **Manage Data**
   - "View Stored Resumes" - Browse all saved resumes
   - "Search Database" - Find specific candidates
   - "Analytics Dashboard" - View processing statistics

5. **Export Data**
   - Download individual resume data as JSON, CSV, or Excel
   - Export from upload page after processing

## Customization Guide

### Adding Skills Categories
Edit `nlp_processor.py`:
```python
self.skill_keywords = {
    'your_category': ['skill1', 'skill2'],
    'another_category': ['tool1', 'tool2']
}
```

### Modifying Scoring Algorithm
Edit `resume_parser.py`:
```python
def _calculate_overall_score(self, parsed_data):
    # Adjust weights and calculations
    experience_weight = 40
    education_weight = 25
    # ... your modifications
```

### Database Schema Changes
Edit `database_manager.py`:
```python
class ParsedResume(Base):
    # Add new columns
    new_field = Column(String(255))
```

## Troubleshooting

### Common Solutions
```bash
# Missing dependencies
pip install -r dependencies.txt

# spaCy model missing
python -m spacy download en_core_web_sm

# Port conflicts
streamlit run app.py --server.port 8502

# Database issues
# Check file permissions for SQLite
# Verify DATABASE_URL for PostgreSQL
```

### Performance Notes
- Processing time: 5-30 seconds per resume
- SQLite: Handles 1000+ resumes efficiently
- PostgreSQL: Recommended for production use
- Large files (>5MB): May require additional processing time

## Architecture Overview

```
User Upload → Text Extraction → NLP Processing → Database Storage → Web Display
     ↓              ↓               ↓              ↓             ↓
   PDF/DOCX    pdfplumber/      spaCy/NLTK    SQLAlchemy    Streamlit
              python-docx                                      Pages
```

## Security and Privacy
- Files processed locally and temporarily
- No permanent file storage on server
- Automatic cleanup of temporary files
- Database stores structured data only (no raw files)
- All processing happens within your environment

## License
MIT License - Free for personal and commercial use

## Support
This is a complete, standalone package that runs independently in any Python environment. All source code is included and can be modified as needed.

For issues:
1. Verify Python 3.8+ installation
2. Check all dependencies are installed
3. Ensure proper file permissions
4. Review console output for specific errors