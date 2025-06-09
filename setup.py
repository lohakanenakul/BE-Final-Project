from setuptools import setup, find_packages

setup(
    name="resume-parser-ml",
    version="1.0.0",
    description="Resume Parser using Machine Learning and Natural Language Processing",
    author="Resume Parser Project",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.28.0",
        "spacy>=3.7.0",
        "nltk>=3.8.1",
        "PyPDF2>=3.0.1",
        "pdfplumber>=0.10.0",
        "python-docx>=1.1.0",
        "pandas>=2.1.0",
        "openpyxl>=3.1.0",
        "psycopg2-binary>=2.9.0",
        "sqlalchemy>=2.0.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)