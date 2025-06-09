# Resume Parser Installation Guide

## Complete Source Code Package

This package contains a fully functional Resume Parser application with Machine Learning and NLP capabilities, including database storage for persistent data management.

## Quick Start Options

### Option 1: Automated Setup (Recommended)
```bash
# Clone/download all files to a directory
# Run the automated setup script
python run.py
```

### Option 2: Manual Installation

#### Step 1: Install Python Dependencies
```bash
pip install streamlit spacy nltk PyPDF2 pdfplumber python-docx pandas openpyxl psycopg2-binary sqlalchemy
```

#### Step 2: Download NLP Model
```bash
python -m spacy download en_core_web_sm
```

#### Step 3: Run Application
```bash
streamlit run app.py
```

### Option 3: Platform-Specific Scripts

#### Windows Users:
```bash
# Double-click install.bat or run:
install.bat
```

#### Linux/macOS Users:
```bash
chmod +x install.sh
./install.sh
```

## File Structure

```
resume-parser/
├── app.py                    # Main Streamlit application
├── resume_parser.py          # Core parsing logic
├── nlp_processor.py          # NLP and ML processing
├── text_extractors.py        # PDF/DOCX text extraction
├── data_exporter.py          # Export functionality
├── database_manager.py       # Database operations
├── config.py                 # Configuration settings
├── dependencies.txt          # Required packages
├── setup.py                  # Package setup
├── run.py                    # Cross-platform runner
├── install.bat              # Windows installer
├── install.sh               # Linux/macOS installer
├── .streamlit/
│   └── config.toml          # Streamlit configuration
└── README.md                # Documentation
```

## Database Options

### SQLite (Default - No Setup Required)
The application automatically uses SQLite for local development. No additional database setup needed.

### PostgreSQL (Production)
Set environment variable:
```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/resume_parser"
```

## Features

### Core Functionality
- Upload PDF and DOCX resume files
- Extract structured data using ML/NLP
- Store resumes in database
- Search and analytics dashboard
- Export to JSON, CSV, Excel

### Pages Available
1. **Upload & Parse Resumes** - Main parsing interface
2. **View Stored Resumes** - Browse saved resumes
3. **Search Database** - Search by name, email, location
4. **Analytics Dashboard** - Statistics and metrics

## System Requirements

- Python 3.8 or higher
- 2GB RAM minimum
- 500MB disk space
- Internet connection (initial setup only)

## Usage Instructions

1. **Start the application**:
   ```bash
   streamlit run app.py
   ```

2. **Access in browser**:
   Open `http://localhost:8501`

3. **Upload resumes**:
   - Use the "Upload & Parse Resumes" page
   - Select PDF or DOCX files
   - View extracted information

4. **View results**:
   - Check "View Stored Resumes" for saved data
   - Use "Search Database" to find specific resumes
   - Monitor "Analytics Dashboard" for insights

## Troubleshooting

### Common Issues

**1. Module Import Errors**
```bash
# Reinstall dependencies
pip install -r dependencies.txt
```

**2. spaCy Model Missing**
```bash
python -m spacy download en_core_web_sm
```

**3. Database Connection Issues**
- For SQLite: Ensure write permissions in application directory
- For PostgreSQL: Check DATABASE_URL environment variable

**4. Port Already in Use**
```bash
streamlit run app.py --server.port 8502
```

### Performance Tips

- For large files (>5MB), processing may take 10-30 seconds
- SQLite handles up to 1000 resumes efficiently
- For production use, consider PostgreSQL

## Environment Variables

```bash
# Optional: Database configuration
DATABASE_URL=postgresql://user:pass@host:port/dbname

# Optional: Custom SQLite path
SQLITE_DB_PATH=custom_path.db
```

## Customization

### Adding Skills
Edit `nlp_processor.py`:
```python
self.skill_keywords = {
    'your_category': ['skill1', 'skill2', 'skill3']
}
```

### Modifying Scoring
Edit `resume_parser.py` in `_calculate_overall_score` method.

### Database Schema
Modify `database_manager.py` for additional fields.

## Support

For issues:
1. Check this troubleshooting guide
2. Verify all dependencies are installed
3. Ensure Python 3.8+ is being used
4. Check file permissions for database writes

## License

Open source under MIT License - free for personal and commercial use.