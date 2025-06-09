"""
Configuration settings for the Resume Parser application.
This file contains environment-specific settings that can be modified
for different deployment environments.
"""

import os
from urllib.parse import urlparse

# Database Configuration
# For PostgreSQL (production/cloud deployment)
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/resume_parser')

# For SQLite (local development - no PostgreSQL needed)
SQLITE_DATABASE_PATH = os.getenv('SQLITE_DB_PATH', 'resume_parser.db')

# Determine database type based on URL
def get_database_config():
    """
    Returns database configuration based on environment.
    Falls back to SQLite if PostgreSQL is not available.
    """
    db_url = os.getenv('DATABASE_URL')
    
    if db_url and db_url.startswith('postgresql'):
        return {
            'type': 'postgresql',
            'url': db_url
        }
    else:
        # Use SQLite for local development
        sqlite_url = f"sqlite:///{SQLITE_DATABASE_PATH}"
        return {
            'type': 'sqlite',
            'url': sqlite_url
        }

# Application Settings
APP_TITLE = "Resume Parser & Analysis Tool"
APP_DESCRIPTION = "Upload resumes in PDF or DOCX format to extract structured information for recruitment screening."

# File Upload Settings
MAX_FILE_SIZE_MB = 10
ALLOWED_EXTENSIONS = ['pdf', 'docx']
UPLOAD_TEMP_DIR = 'temp_uploads'

# Processing Settings
DEFAULT_PROCESSING_TIMEOUT = 30  # seconds
MAX_TEXT_LENGTH = 100000  # characters

# Scoring Configuration
SCORING_WEIGHTS = {
    'experience': 40,  # max points for experience
    'education': 25,   # max points for education
    'skills': 25,      # max points for skills
    'contact': 10      # max points for contact info
}

# Database Table Limits
MAX_RESUMES_PER_PAGE = 50
MAX_SEARCH_RESULTS = 100

# SpaCy Model
SPACY_MODEL = 'en_core_web_sm'

# NLTK Data
NLTK_DOWNLOADS = ['punkt', 'stopwords']