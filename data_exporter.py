import json
import csv
import io
import pandas as pd
from datetime import datetime
import logging

class DataExporter:
    """Export parsed resume data to various formats"""
    
    @staticmethod
    def to_json(parsed_data, pretty=True):
        """
        Export parsed data to JSON format
        
        Args:
            parsed_data (dict): Parsed resume data
            pretty (bool): Whether to format JSON with indentation
            
        Returns:
            str: JSON string
        """
        try:
            # Create a clean copy for export
            export_data = DataExporter._prepare_export_data(parsed_data)
            
            if pretty:
                return json.dumps(export_data, indent=2, ensure_ascii=False)
            else:
                return json.dumps(export_data, ensure_ascii=False)
                
        except Exception as e:
            logging.error(f"Error exporting to JSON: {str(e)}")
            return json.dumps({"error": "Failed to export data"})
    
    @staticmethod
    def to_csv(parsed_data):
        """
        Export parsed data to CSV format
        
        Args:
            parsed_data (dict): Parsed resume data
            
        Returns:
            str: CSV string
        """
        try:
            # Flatten the data for CSV export
            flattened_data = DataExporter._flatten_for_csv(parsed_data)
            
            # Create CSV in memory
            output = io.StringIO()
            
            if flattened_data:
                # Get all unique keys for CSV headers
                all_keys = set()
                for record in flattened_data:
                    all_keys.update(record.keys())
                
                fieldnames = sorted(list(all_keys))
                writer = csv.DictWriter(output, fieldnames=fieldnames)
                
                writer.writeheader()
                for record in flattened_data:
                    writer.writerow(record)
            
            return output.getvalue()
            
        except Exception as e:
            logging.error(f"Error exporting to CSV: {str(e)}")
            return "error,message\nExport Error,Failed to export data"
    
    @staticmethod
    def to_excel(parsed_data):
        """
        Export parsed data to Excel format
        
        Args:
            parsed_data (dict): Parsed resume data
            
        Returns:
            bytes: Excel file bytes
        """
        try:
            # Create Excel file in memory
            output = io.BytesIO()
            
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                # Personal Information Sheet
                personal_df = DataExporter._create_personal_info_df(parsed_data)
                personal_df.to_excel(writer, sheet_name='Personal Info', index=False)
                
                # Experience Sheet
                experience_df = DataExporter._create_experience_df(parsed_data)
                if not experience_df.empty:
                    experience_df.to_excel(writer, sheet_name='Experience', index=False)
                
                # Education Sheet
                education_df = DataExporter._create_education_df(parsed_data)
                if not education_df.empty:
                    education_df.to_excel(writer, sheet_name='Education', index=False)
                
                # Skills Sheet
                skills_df = DataExporter._create_skills_df(parsed_data)
                if not skills_df.empty:
                    skills_df.to_excel(writer, sheet_name='Skills', index=False)
                
                # Summary Sheet
                summary_df = DataExporter._create_summary_df(parsed_data)
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            output.seek(0)
            return output.getvalue()
            
        except Exception as e:
            logging.error(f"Error exporting to Excel: {str(e)}")
            return None
    
    @staticmethod
    def _prepare_export_data(parsed_data):
        """Prepare data for export by cleaning and organizing"""
        export_data = {}
        
        # Add metadata
        export_data['export_timestamp'] = datetime.now().isoformat()
        export_data['file_info'] = parsed_data.get('file_info', {})
        
        # Add scores
        export_data['overall_score'] = parsed_data.get('overall_score', 0)
        export_data['confidence_scores'] = parsed_data.get('confidence_scores', {})
        
        # Add extracted information
        export_data['personal_info'] = parsed_data.get('personal_info', {})
        export_data['summary'] = parsed_data.get('summary', '')
        export_data['experience'] = parsed_data.get('experience', [])
        export_data['education'] = parsed_data.get('education', [])
        export_data['skills'] = parsed_data.get('skills', [])
        
        # Don't include raw text in export by default
        # export_data['raw_text'] = parsed_data.get('raw_text', '')
        
        return export_data
    
    @staticmethod
    def _flatten_for_csv(parsed_data):
        """Flatten nested data structure for CSV export"""
        flattened_records = []
        
        # Base record with personal info and scores
        base_record = {
            'export_timestamp': datetime.now().isoformat(),
            'filename': parsed_data.get('file_info', {}).get('filename', ''),
            'overall_score': parsed_data.get('overall_score', 0),
            'name': parsed_data.get('personal_info', {}).get('name', ''),
            'email': parsed_data.get('personal_info', {}).get('email', ''),
            'phone': parsed_data.get('personal_info', {}).get('phone', ''),
            'location': parsed_data.get('personal_info', {}).get('location', ''),
            'linkedin': parsed_data.get('personal_info', {}).get('linkedin', ''),
            'summary': parsed_data.get('summary', ''),
        }
        
        # Add confidence scores
        confidence_scores = parsed_data.get('confidence_scores', {})
        for key, value in confidence_scores.items():
            base_record[f'confidence_{key}'] = value
        
        # If there's experience data, create records for each job
        experience = parsed_data.get('experience', [])
        if experience:
            for i, exp in enumerate(experience):
                record = base_record.copy()
                record.update({
                    'experience_index': i + 1,
                    'job_title': exp.get('title', ''),
                    'company': exp.get('company', ''),
                    'job_duration': exp.get('duration', ''),
                    'job_location': exp.get('location', ''),
                    'job_description': exp.get('description', ''),
                })
                flattened_records.append(record)
        else:
            # If no experience, just add the base record
            flattened_records.append(base_record)
        
        # Add education data to the first record or create separate records
        education = parsed_data.get('education', [])
        if education and flattened_records:
            for i, edu in enumerate(education):
                if i < len(flattened_records):
                    flattened_records[i].update({
                        'degree': edu.get('degree', ''),
                        'institution': edu.get('institution', ''),
                        'graduation_year': edu.get('year', ''),
                        'gpa': edu.get('gpa', ''),
                    })
        
        # Add skills as a comma-separated list
        skills = parsed_data.get('skills', [])
        if skills and flattened_records:
            skill_names = []
            for skill in skills:
                if isinstance(skill, dict):
                    skill_names.append(skill.get('name', ''))
                else:
                    skill_names.append(str(skill))
            
            skills_text = ', '.join(filter(None, skill_names))
            flattened_records[0]['skills'] = skills_text
        
        return flattened_records
    
    @staticmethod
    def _create_personal_info_df(parsed_data):
        """Create DataFrame for personal information"""
        personal_info = parsed_data.get('personal_info', {})
        
        data = [{
            'Field': key.replace('_', ' ').title(),
            'Value': value
        } for key, value in personal_info.items()]
        
        # Add scores
        data.append({'Field': 'Overall Score', 'Value': parsed_data.get('overall_score', 0)})
        
        confidence_scores = parsed_data.get('confidence_scores', {})
        for key, value in confidence_scores.items():
            data.append({'Field': f'Confidence - {key.title()}', 'Value': f'{value}%'})
        
        return pd.DataFrame(data)
    
    @staticmethod
    def _create_experience_df(parsed_data):
        """Create DataFrame for work experience"""
        experience = parsed_data.get('experience', [])
        
        if not experience:
            return pd.DataFrame()
        
        return pd.DataFrame(experience)
    
    @staticmethod
    def _create_education_df(parsed_data):
        """Create DataFrame for education"""
        education = parsed_data.get('education', [])
        
        if not education:
            return pd.DataFrame()
        
        return pd.DataFrame(education)
    
    @staticmethod
    def _create_skills_df(parsed_data):
        """Create DataFrame for skills"""
        skills = parsed_data.get('skills', [])
        
        if not skills:
            return pd.DataFrame()
        
        # Normalize skills data
        skills_data = []
        for skill in skills:
            if isinstance(skill, dict):
                skills_data.append({
                    'Skill': skill.get('name', ''),
                    'Category': skill.get('category', 'General')
                })
            else:
                skills_data.append({
                    'Skill': str(skill),
                    'Category': 'General'
                })
        
        return pd.DataFrame(skills_data)
    
    @staticmethod
    def _create_summary_df(parsed_data):
        """Create DataFrame for summary information"""
        summary_data = []
        
        # File information
        file_info = parsed_data.get('file_info', {})
        for key, value in file_info.items():
            summary_data.append({
                'Category': 'File Info',
                'Field': key.replace('_', ' ').title(),
                'Value': value
            })
        
        # Summary text
        summary_text = parsed_data.get('summary', '')
        if summary_text:
            summary_data.append({
                'Category': 'Professional Summary',
                'Field': 'Summary',
                'Value': summary_text
            })
        
        # Counts
        summary_data.extend([
            {'Category': 'Statistics', 'Field': 'Experience Entries', 'Value': len(parsed_data.get('experience', []))},
            {'Category': 'Statistics', 'Field': 'Education Entries', 'Value': len(parsed_data.get('education', []))},
            {'Category': 'Statistics', 'Field': 'Skills Count', 'Value': len(parsed_data.get('skills', []))},
        ])
        
        return pd.DataFrame(summary_data)
