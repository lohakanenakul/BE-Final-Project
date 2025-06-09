#!/usr/bin/env python3
"""
Resume Parser Application Runner

This script provides an easy way to run the resume parser application
in different environments and with various configurations.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'streamlit',
        'spacy',
        'nltk',
        'PyPDF2',
        'pdfplumber',
        'docx',
        'pandas',
        'openpyxl'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            if package == 'docx':
                missing_packages.append('python-docx')
            else:
                missing_packages.append(package)
    
    return missing_packages

def install_dependencies():
    """Install missing dependencies"""
    print("Installing required dependencies...")
    
    packages = [
        'streamlit>=1.28.0',
        'spacy>=3.7.0',
        'nltk>=3.8.1',
        'PyPDF2>=3.0.1',
        'pdfplumber>=0.10.0',
        'python-docx>=1.1.0',
        'pandas>=2.1.0',
        'openpyxl>=3.1.0',
        'psycopg2-binary>=2.9.0',
        'sqlalchemy>=2.0.0'
    ]
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + packages)
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

def download_spacy_model():
    """Download the required spaCy language model"""
    print("Downloading spaCy English language model...")
    try:
        subprocess.check_call([sys.executable, '-m', 'spacy', 'download', 'en_core_web_sm'])
        print("spaCy model downloaded successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error downloading spaCy model: {e}")
        print("You may need to run: python -m spacy download en_core_web_sm")
        return False

def run_app(port=8501, host='localhost'):
    """Run the Streamlit application"""
    app_file = Path(__file__).parent / 'app.py'
    
    if not app_file.exists():
        print("Error: app.py not found in the current directory")
        return False
    
    print(f"Starting Resume Parser application on http://{host}:{port}")
    print("Press Ctrl+C to stop the application")
    
    try:
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', str(app_file),
            '--server.port', str(port),
            '--server.address', host
        ])
        return True
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running application: {e}")
        return False

def main():
    """Main function to setup and run the application"""
    print("Resume Parser with ML & NLP")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        sys.exit(1)
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        print(f"Missing dependencies: {', '.join(missing)}")
        install_choice = input("Install missing dependencies? (y/n): ").lower().strip()
        
        if install_choice in ['y', 'yes']:
            if not install_dependencies():
                print("Failed to install dependencies. Please install manually.")
                sys.exit(1)
        else:
            print("Please install the missing dependencies manually:")
            print("pip install " + " ".join(missing))
            sys.exit(1)
    
    # Check spaCy model
    try:
        import spacy
        spacy.load('en_core_web_sm')
    except OSError:
        print("spaCy English model not found.")
        model_choice = input("Download spaCy model? (y/n): ").lower().strip()
        
        if model_choice in ['y', 'yes']:
            if not download_spacy_model():
                print("Please download the model manually:")
                print("python -m spacy download en_core_web_sm")
                sys.exit(1)
        else:
            print("spaCy model is required. Please download it manually:")
            print("python -m spacy download en_core_web_sm")
            sys.exit(1)
    
    # Get port configuration
    port = 8501
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port number: {sys.argv[1]}")
            sys.exit(1)
    
    # Run the application
    print("\nAll dependencies are ready!")
    if not run_app(port=port):
        sys.exit(1)

if __name__ == "__main__":
    main()