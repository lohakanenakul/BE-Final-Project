#!/usr/bin/env python3
"""
Simple Resume Parser Application Runner

This is the simplest way to run the resume parser application.
It handles all dependencies and setup automatically.
"""

import subprocess
import sys
import os

def install_packages():
    """Install required packages"""
    packages = [
        'streamlit',
        'spacy',
        'nltk', 
        'PyPDF2',
        'pdfplumber',
        'python-docx',
        'pandas',
        'openpyxl',
        'sqlalchemy'
    ]
    
    print("Installing packages...")
    for package in packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"✓ {package}")
        except:
            print(f"✗ {package} (continuing anyway)")

def download_model():
    """Download spaCy model"""
    try:
        subprocess.check_call([sys.executable, '-m', 'spacy', 'download', 'en_core_web_sm'],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✓ spaCy model downloaded")
    except:
        print("✗ spaCy model download failed (will try to continue)")

def main():
    print("Resume Parser Setup")
    print("=" * 30)
    
    # Quick dependency check
    try:
        import streamlit
        print("✓ Dependencies already installed")
    except ImportError:
        install_packages()
    
    # Model check
    try:
        import spacy
        spacy.load('en_core_web_sm')
        print("✓ spaCy model ready")
    except:
        download_model()
    
    # Run the app
    print("\nStarting Resume Parser...")
    print("Application will open in your browser")
    print("Press Ctrl+C to stop")
    
    try:
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'app.py'])
    except KeyboardInterrupt:
        print("\nApplication stopped")

if __name__ == "__main__":
    main()