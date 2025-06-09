# Resume Parser with Machine Learning & NLP

A comprehensive Python application that uses Machine Learning and Natural Language Processing to extract structured data from resumes in PDF and DOCX formats. This tool automates the recruitment screening process by intelligently parsing resumes and providing candidate scoring.

## Features

- **Multi-format Support**: Parse PDF and DOCX resume files
- **Intelligent Extraction**: Extract personal information, work experience, education, skills
- **ML-powered Analysis**: Uses spaCy NLP models for entity recognition
- **Database Storage**: PostgreSQL database for persistent data storage
- **Candidate Scoring**: Automated scoring system (0-100) based on experience, education, skills
- **Export Options**: Export parsed data to JSON, CSV, and Excel formats
- **Search & Analytics**: Search stored resumes and view analytics dashboard
- **Confidence Metrics**: Provides confidence scores for extracted information
- **Web Interface**: Easy-to-use Streamlit web application with multiple pages

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone or download the project files**
2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv resume_parser_env
   source resume_parser_env/bin/activate  # On Windows: resume_parser_env\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install streamlit spacy nltk PyPDF2 pdfplumber python-docx pandas openpyxl
   ```

4. **Download spaCy language model**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Run the application**:
   ```bash
   streamlit run app.py
   ```

6. **Access the application**:
   Open your web browser and go to `http://localhost:8501`

## Project Structure

```
resume-parser/
├── app.py                 # Main Streamlit application
├── resume_parser.py       # Core resume parsing logic
├── nlp_processor.py       # NLP processing and information extraction
├── text_extractors.py     # PDF and DOCX text extraction
├── data_exporter.py       # Export functionality (JSON, CSV, Excel)
├── setup.py              # Package setup configuration
├── .streamlit/
│   └── config.toml       # Streamlit configuration
└── README.md             # This file
```

## Usage

1. **Start the application** using the command above
2. **Upload resume files** (PDF or DOCX format)
3. **View extracted information** organized in sections:
   - Personal Information (name, email, phone, location)
   - Professional Summary
   - Work Experience
   - Education Background
   - Skills and Competencies
4. **Review candidate scoring** and confidence metrics
5. **Export results** in your preferred format (JSON, CSV, Excel)

## What Information is Extracted

- **Personal Details**: Name, email, phone number, location, LinkedIn profile
- **Professional Summary**: Objective or summary statements
- **Work Experience**: Job titles, companies, employment duration, descriptions
- **Education**: Degrees, institutions, graduation years, GPA
- **Skills**: Technical and soft skills categorized by type
- **Scoring**: Overall candidate score based on experience, education, and skills

## Scoring System

The application provides an automated scoring system (0-100 points):
- **Experience Score** (0-40 points): Based on years of experience and relevance
- **Education Score** (0-25 points): Based on number and level of qualifications
- **Skills Score** (0-25 points): Based on identified technical and professional skills
- **Contact Information** (0-10 points): Completeness of contact details

## Privacy & Security

- All files are processed locally on your machine
- No data is stored permanently or sent to external servers
- Temporary files are automatically cleaned up after processing
- Your resume data remains completely private

## Customization

### Adding New Skills
Edit the `skill_keywords` dictionary in `nlp_processor.py` to add industry-specific skills:

```python
self.skill_keywords = {
    'programming': ['python', 'java', 'your_new_skill'],
    'new_category': ['skill1', 'skill2', 'skill3']
}
```

### Modifying Scoring Algorithm
Adjust the scoring weights in `resume_parser.py` in the `_calculate_overall_score` method.

### Adding New Export Formats
Extend the `DataExporter` class in `data_exporter.py` to support additional export formats.

## Troubleshooting

### Common Issues

1. **spaCy model not found**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

2. **Import errors**:
   Ensure all dependencies are installed:
   ```bash
   pip install --upgrade streamlit spacy nltk PyPDF2 pdfplumber python-docx pandas openpyxl
   ```

3. **PDF extraction issues**:
   Some PDFs may have complex layouts. The application uses multiple extraction methods for better compatibility.

4. **Port already in use**:
   If port 8501 is busy, specify a different port:
   ```bash
   streamlit run app.py --server.port 8502
   ```

## Technical Details

### NLP Processing
- Uses spaCy's English language model for entity recognition
- NLTK for additional text processing capabilities
- Regular expressions for pattern matching (emails, phones, dates)

### Text Extraction
- **PDF**: Uses pdfplumber as primary method, PyPDF2 as fallback
- **DOCX**: Extracts from paragraphs, tables, headers, and footers
- Handles complex document layouts and formatting

### Machine Learning Features
- Named Entity Recognition (NER) for person names and locations
- Pattern-based extraction for structured information
- Confidence scoring based on extraction quality
- Skill categorization using keyword matching

## Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make your improvements
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues or questions:
- Check the troubleshooting section above
- Review the code comments for implementation details
- Ensure all dependencies are properly installed