import spacy
import re
from datetime import datetime
import nltk
from collections import Counter
import logging

class NLPProcessor:
    """NLP processing for resume text analysis and information extraction"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            self.logger.error("spaCy English model not found. Please install with: python -m spacy download en_core_web_sm")
            raise
        
        # Download required NLTK data
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
        except:
            pass
        
        # Common skills keywords
        self.skill_keywords = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'scala', 'kotlin'],
            'web_development': ['html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'laravel'],
            'databases': ['mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'oracle', 'sql server', 'sqlite'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins', 'ci/cd'],
            'data_science': ['pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'matplotlib', 'seaborn', 'jupyter'],
            'tools': ['git', 'jira', 'confluence', 'slack', 'trello', 'figma', 'photoshop', 'illustrator']
        }
        
        # Education keywords
        self.education_keywords = ['bachelor', 'master', 'phd', 'degree', 'university', 'college', 'school', 'diploma', 'certificate']
        
        # Experience keywords
        self.experience_keywords = ['experience', 'work', 'employment', 'career', 'position', 'role', 'job']
    
    def process_resume_text(self, text):
        """
        Process resume text and extract structured information
        
        Args:
            text (str): Raw resume text
            
        Returns:
            dict: Structured resume data
        """
        # Process text with spaCy
        doc = self.nlp(text)
        
        # Extract different sections
        parsed_data = {
            'personal_info': self._extract_personal_info(text, doc),
            'summary': self._extract_summary(text),
            'experience': self._extract_experience(text),
            'education': self._extract_education(text),
            'skills': self._extract_skills(text),
            'raw_text': text
        }
        
        return parsed_data
    
    def _extract_personal_info(self, text, doc):
        """Extract personal information (name, email, phone, location)"""
        personal_info = {}
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            personal_info['email'] = emails[0]
        
        # Extract phone number
        phone_patterns = [
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # US format
            r'\(\d{3}\)\s*\d{3}[-.]?\d{4}',    # (123) 456-7890
            r'\+\d{1,3}[\s.-]?\d{3,4}[\s.-]?\d{3,4}[\s.-]?\d{3,4}',  # International
        ]
        
        for pattern in phone_patterns:
            phones = re.findall(pattern, text)
            if phones:
                personal_info['phone'] = phones[0]
                break
        
        # Extract name (first person entity or from first lines)
        name = self._extract_name(text, doc)
        if name:
            personal_info['name'] = name
        
        # Extract LinkedIn profile
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin_matches = re.findall(linkedin_pattern, text.lower())
        if linkedin_matches:
            personal_info['linkedin'] = linkedin_matches[0]
        
        # Extract location (look for city, state patterns)
        location = self._extract_location(text, doc)
        if location:
            personal_info['location'] = location
        
        return personal_info
    
    def _extract_name(self, text, doc):
        """Extract person's name from resume"""
        # Look for PERSON entities
        for ent in doc.ents:
            if ent.label_ == "PERSON" and len(ent.text.split()) >= 2:
                return ent.text.strip()
        
        # Fallback: look in first few lines for name-like patterns
        lines = text.split('\n')[:5]
        for line in lines:
            line = line.strip()
            if line and len(line.split()) >= 2 and len(line.split()) <= 4:
                # Check if it looks like a name (no numbers, reasonable length)
                if not re.search(r'\d|@|\.com', line) and len(line) < 50:
                    return line
        
        return None
    
    def _extract_location(self, text, doc):
        """Extract location information"""
        # Look for GPE (Geopolitical entity) in spaCy
        locations = []
        for ent in doc.ents:
            if ent.label_ in ["GPE", "LOC"]:
                locations.append(ent.text)
        
        # Common location patterns
        location_patterns = [
            r'([A-Z][a-z]+),\s*([A-Z]{2})',  # City, ST
            r'([A-Z][a-z]+),\s*([A-Z][a-z]+)',  # City, State
        ]
        
        for pattern in location_patterns:
            matches = re.findall(pattern, text)
            if matches:
                return f"{matches[0][0]}, {matches[0][1]}"
        
        return locations[0] if locations else None
    
    def _extract_summary(self, text):
        """Extract professional summary or objective"""
        summary_keywords = ['summary', 'objective', 'profile', 'about', 'overview']
        
        lines = text.split('\n')
        summary_started = False
        summary_lines = []
        
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            
            # Check if this line starts a summary section
            if any(keyword in line_lower for keyword in summary_keywords):
                summary_started = True
                continue
            
            # If we're in summary section, collect lines
            if summary_started:
                if line.strip():
                    # Stop if we hit another section
                    if any(keyword in line_lower for keyword in ['experience', 'education', 'skills', 'work']):
                        break
                    summary_lines.append(line.strip())
                elif summary_lines:  # Empty line after collecting some summary
                    break
        
        if summary_lines:
            return ' '.join(summary_lines)
        
        # Fallback: take first substantial paragraph
        paragraphs = text.split('\n\n')
        for para in paragraphs[1:3]:  # Skip first paragraph (usually name/contact)
            if len(para.strip()) > 100:
                return para.strip()
        
        return None
    
    def _extract_experience(self, text):
        """Extract work experience information"""
        experience_list = []
        
        # Split text into sections
        sections = self._split_into_sections(text)
        
        for section in sections:
            if any(keyword in section['title'].lower() for keyword in self.experience_keywords):
                jobs = self._parse_experience_section(section['content'])
                experience_list.extend(jobs)
        
        return experience_list
    
    def _extract_education(self, text):
        """Extract education information"""
        education_list = []
        
        # Split text into sections
        sections = self._split_into_sections(text)
        
        for section in sections:
            if any(keyword in section['title'].lower() for keyword in self.education_keywords):
                education = self._parse_education_section(section['content'])
                education_list.extend(education)
        
        return education_list
    
    def _extract_skills(self, text):
        """Extract skills and competencies"""
        skills = []
        text_lower = text.lower()
        
        # Extract from all skill categories
        for category, skill_list in self.skill_keywords.items():
            found_skills = []
            for skill in skill_list:
                if skill in text_lower:
                    found_skills.append({
                        'name': skill,
                        'category': category.replace('_', ' ').title()
                    })
            skills.extend(found_skills)
        
        # Look for skills section
        sections = self._split_into_sections(text)
        for section in sections:
            if 'skill' in section['title'].lower():
                additional_skills = self._parse_skills_section(section['content'])
                skills.extend(additional_skills)
        
        # Remove duplicates
        unique_skills = []
        seen_skills = set()
        for skill in skills:
            skill_name = skill['name'] if isinstance(skill, dict) else skill
            if skill_name not in seen_skills:
                unique_skills.append(skill)
                seen_skills.add(skill_name)
        
        return unique_skills
    
    def _split_into_sections(self, text):
        """Split resume text into logical sections"""
        sections = []
        lines = text.split('\n')
        current_section = {'title': '', 'content': ''}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if this line is a section header
            if self._is_section_header(line):
                if current_section['content']:
                    sections.append(current_section)
                current_section = {'title': line, 'content': ''}
            else:
                current_section['content'] += line + '\n'
        
        # Add last section
        if current_section['content']:
            sections.append(current_section)
        
        return sections
    
    def _is_section_header(self, line):
        """Determine if a line is a section header"""
        if len(line) > 50:
            return False
        
        # Common section headers
        section_headers = [
            'experience', 'work experience', 'employment', 'career',
            'education', 'academic background', 'qualifications',
            'skills', 'technical skills', 'competencies',
            'summary', 'profile', 'objective', 'about',
            'projects', 'achievements', 'certifications'
        ]
        
        line_lower = line.lower()
        return any(header in line_lower for header in section_headers)
    
    def _parse_experience_section(self, content):
        """Parse experience section content"""
        jobs = []
        
        # Split by common job separators
        job_blocks = re.split(r'\n(?=[A-Z][^a-z]*[A-Z])', content)
        
        for block in job_blocks:
            if len(block.strip()) < 20:
                continue
            
            job = self._parse_job_block(block)
            if job:
                jobs.append(job)
        
        return jobs
    
    def _parse_job_block(self, block):
        """Parse individual job block"""
        lines = [line.strip() for line in block.split('\n') if line.strip()]
        if not lines:
            return None
        
        job = {}
        
        # First line usually contains title and company
        first_line = lines[0]
        if '|' in first_line or '-' in first_line or 'at' in first_line.lower():
            parts = re.split(r'[|@-]|at\s+', first_line, 1)
            if len(parts) >= 2:
                job['title'] = parts[0].strip()
                job['company'] = parts[1].strip()
        
        # Look for dates
        date_pattern = r'\b(\d{4})\b|\b(\d{1,2}/\d{4})\b|\b(present|current)\b'
        for line in lines[1:3]:
            if re.search(date_pattern, line, re.IGNORECASE):
                job['duration'] = line
                break
        
        # Combine remaining lines as description
        desc_lines = []
        for line in lines[1:]:
            if not re.search(date_pattern, line, re.IGNORECASE):
                desc_lines.append(line)
        
        if desc_lines:
            job['description'] = '\n'.join(desc_lines)
        
        return job if job else None
    
    def _parse_education_section(self, content):
        """Parse education section content"""
        education_list = []
        
        # Split by degree entries
        degree_blocks = content.split('\n\n')
        
        for block in degree_blocks:
            if len(block.strip()) < 10:
                continue
            
            education = self._parse_education_block(block)
            if education:
                education_list.append(education)
        
        return education_list
    
    def _parse_education_block(self, block):
        """Parse individual education block"""
        lines = [line.strip() for line in block.split('\n') if line.strip()]
        if not lines:
            return None
        
        education = {}
        
        # Look for degree and institution
        for line in lines:
            if any(degree in line.lower() for degree in ['bachelor', 'master', 'phd', 'diploma']):
                education['degree'] = line
            elif any(inst in line.lower() for inst in ['university', 'college', 'school', 'institute']):
                education['institution'] = line
        
        # Look for year
        year_pattern = r'\b(19|20)\d{2}\b'
        for line in lines:
            years = re.findall(year_pattern, line)
            if years:
                education['year'] = years[-1]  # Take the latest year
                break
        
        # Look for GPA
        gpa_pattern = r'gpa:?\s*(\d+\.?\d*)'
        for line in lines:
            gpa_match = re.search(gpa_pattern, line.lower())
            if gpa_match:
                education['gpa'] = gpa_match.group(1)
                break
        
        return education if education else None
    
    def _parse_skills_section(self, content):
        """Parse skills section content"""
        skills = []
        
        # Split by common separators
        skill_text = re.sub(r'[•\-\*]', ',', content)
        potential_skills = re.split(r'[,\n;]', skill_text)
        
        for skill in potential_skills:
            skill = skill.strip()
            if skill and len(skill) < 50 and not skill.lower().startswith('skill'):
                skills.append({
                    'name': skill,
                    'category': 'General'
                })
        
        return skills
