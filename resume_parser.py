import os
from text_extractors import PDFExtractor, DOCXExtractor
from nlp_processor import NLPProcessor
import logging

class ResumeParser:
    """Main resume parsing class that coordinates text extraction and NLP processing"""
    
    def __init__(self):
        self.pdf_extractor = PDFExtractor()
        self.docx_extractor = DOCXExtractor()
        self.nlp_processor = NLPProcessor()
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def parse_resume(self, file_path):
        """
        Parse a resume file and extract structured information
        
        Args:
            file_path (str): Path to the resume file
            
        Returns:
            dict: Parsed resume data with structured information
        """
        try:
            # Extract text based on file type
            text = self._extract_text(file_path)
            
            if not text or len(text.strip()) < 50:
                self.logger.warning(f"Insufficient text extracted from {file_path}")
                return None
            
            # Process text with NLP
            parsed_data = self.nlp_processor.process_resume_text(text)
            
            # Add metadata
            parsed_data['file_info'] = {
                'filename': os.path.basename(file_path),
                'file_size': os.path.getsize(file_path),
                'text_length': len(text)
            }
            
            # Calculate overall score
            parsed_data['overall_score'] = self._calculate_overall_score(parsed_data)
            
            # Add confidence scores
            parsed_data['confidence_scores'] = self._calculate_confidence_scores(parsed_data, text)
            
            return parsed_data
            
        except Exception as e:
            self.logger.error(f"Error parsing resume {file_path}: {str(e)}")
            return None
    
    def _extract_text(self, file_path):
        """Extract text from file based on extension"""
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            return self.pdf_extractor.extract_text(file_path)
        elif file_extension == '.docx':
            return self.docx_extractor.extract_text(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    def _calculate_overall_score(self, parsed_data):
        """Calculate an overall candidate score based on extracted information"""
        score = 0
        
        # Experience score (0-40 points)
        experience = parsed_data.get('experience', [])
        if experience:
            years_experience = sum([self._extract_years_from_duration(exp.get('duration', '')) for exp in experience])
            experience_score = min(years_experience * 4, 40)  # Max 40 points for 10+ years
            score += experience_score
        
        # Education score (0-25 points)
        education = parsed_data.get('education', [])
        if education:
            education_score = len(education) * 8  # 8 points per degree, max ~25
            score += min(education_score, 25)
        
        # Skills score (0-25 points)
        skills = parsed_data.get('skills', [])
        if skills:
            skills_score = min(len(skills) * 2, 25)  # 2 points per skill, max 25
            score += skills_score
        
        # Contact information completeness (0-10 points)
        personal_info = parsed_data.get('personal_info', {})
        contact_score = 0
        if personal_info.get('email'): contact_score += 3
        if personal_info.get('phone'): contact_score += 3
        if personal_info.get('name'): contact_score += 2
        if personal_info.get('location'): contact_score += 2
        score += contact_score
        
        return min(int(score), 100)
    
    def _extract_years_from_duration(self, duration_text):
        """Extract years of experience from duration text"""
        import re
        
        if not duration_text:
            return 0
        
        # Try to find year patterns
        year_pattern = r'(\d{4})\s*[-–]\s*(\d{4}|present|current)'
        matches = re.findall(year_pattern, duration_text.lower())
        
        total_years = 0
        for match in matches:
            start_year = int(match[0])
            end_year = 2024 if match[1] in ['present', 'current'] else int(match[1])
            total_years += max(0, end_year - start_year)
        
        return total_years
    
    def _calculate_confidence_scores(self, parsed_data, original_text):
        """Calculate confidence scores for each extracted section"""
        scores = {}
        
        # Personal info confidence
        personal_info = parsed_data.get('personal_info', {})
        personal_score = 0
        if personal_info.get('email') and '@' in personal_info['email']:
            personal_score += 30
        if personal_info.get('phone'):
            personal_score += 25
        if personal_info.get('name') and len(personal_info['name'].split()) >= 2:
            personal_score += 25
        if personal_info.get('location'):
            personal_score += 20
        scores['personal'] = personal_score
        
        # Experience confidence
        experience = parsed_data.get('experience', [])
        exp_score = min(len(experience) * 20, 100) if experience else 0
        scores['experience'] = exp_score
        
        # Education confidence
        education = parsed_data.get('education', [])
        edu_score = min(len(education) * 30, 100) if education else 0
        scores['education'] = edu_score
        
        # Skills confidence
        skills = parsed_data.get('skills', [])
        skills_score = min(len(skills) * 5, 100) if skills else 0
        scores['skills'] = skills_score
        
        return scores
