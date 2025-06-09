import os
import json
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.dialects.sqlite import JSON as SQLiteJSON
import logging
from config import get_database_config

Base = declarative_base()

class ParsedResume(Base):
    """Database model for storing parsed resume data"""
    __tablename__ = 'parsed_resumes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    upload_timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Personal Information
    candidate_name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))
    location = Column(String(255))
    linkedin = Column(String(255))
    
    # Summary
    professional_summary = Column(Text)
    
    # Scores
    overall_score = Column(Integer, default=0)
    experience_confidence = Column(Float, default=0.0)
    education_confidence = Column(Float, default=0.0)
    skills_confidence = Column(Float, default=0.0)
    personal_confidence = Column(Float, default=0.0)
    
    # Structured data as JSON (compatible with both PostgreSQL and SQLite)
    experience_data = Column(Text)  # Store as JSON string for SQLite compatibility
    education_data = Column(Text)   # Store as JSON string for SQLite compatibility
    skills_data = Column(Text)      # Store as JSON string for SQLite compatibility
    
    # File metadata
    file_size = Column(Integer)
    text_length = Column(Integer)
    
    # Processing metadata
    processing_time_seconds = Column(Float)
    is_processed_successfully = Column(Boolean, default=True)
    error_message = Column(Text)
    
    def get_experience_data(self):
        """Parse experience data from JSON string"""
        try:
            return json.loads(self.experience_data) if self.experience_data else []
        except (json.JSONDecodeError, TypeError):
            return []
    
    def get_education_data(self):
        """Parse education data from JSON string"""
        try:
            return json.loads(self.education_data) if self.education_data else []
        except (json.JSONDecodeError, TypeError):
            return []
    
    def get_skills_data(self):
        """Parse skills data from JSON string"""
        try:
            return json.loads(self.skills_data) if self.skills_data else []
        except (json.JSONDecodeError, TypeError):
            return []

class DatabaseManager:
    """Database manager for resume parsing application"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.engine = None
        self.Session = None
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize database connection and create tables"""
        try:
            db_config = get_database_config()
            database_url = db_config['url']
            
            # Create engine with appropriate settings
            if db_config['type'] == 'sqlite':
                self.engine = create_engine(database_url, echo=False)
                self.logger.info("Using SQLite database for local development")
            else:
                self.engine = create_engine(database_url, echo=False)
                self.logger.info("Using PostgreSQL database")
            
            self.Session = sessionmaker(bind=self.engine)
            
            # Create tables
            Base.metadata.create_all(self.engine)
            self.logger.info("Database initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Database initialization failed: {str(e)}")
            return False
    
    def save_parsed_resume(self, parsed_data, filename, processing_time=None):
        """
        Save parsed resume data to database
        
        Args:
            parsed_data (dict): Parsed resume data
            filename (str): Original filename
            processing_time (float): Processing time in seconds
            
        Returns:
            int: ID of saved record, None if failed
        """
        if not self.Session:
            self.logger.error("Database not initialized")
            return None
        
        session = self.Session()
        try:
            # Extract personal information
            personal_info = parsed_data.get('personal_info', {})
            confidence_scores = parsed_data.get('confidence_scores', {})
            file_info = parsed_data.get('file_info', {})
            
            # Create database record
            resume_record = ParsedResume(
                filename=filename,
                candidate_name=personal_info.get('name'),
                email=personal_info.get('email'),
                phone=personal_info.get('phone'),
                location=personal_info.get('location'),
                linkedin=personal_info.get('linkedin'),
                professional_summary=parsed_data.get('summary'),
                overall_score=parsed_data.get('overall_score', 0),
                experience_confidence=confidence_scores.get('experience', 0.0),
                education_confidence=confidence_scores.get('education', 0.0),
                skills_confidence=confidence_scores.get('skills', 0.0),
                personal_confidence=confidence_scores.get('personal', 0.0),
                experience_data=json.dumps(parsed_data.get('experience', [])),
                education_data=json.dumps(parsed_data.get('education', [])),
                skills_data=json.dumps(parsed_data.get('skills', [])),
                file_size=file_info.get('file_size'),
                text_length=file_info.get('text_length'),
                processing_time_seconds=processing_time,
                is_processed_successfully=True
            )
            
            session.add(resume_record)
            session.commit()
            
            record_id = resume_record.id
            self.logger.info(f"Resume data saved successfully with ID: {record_id}")
            return record_id
            
        except Exception as e:
            session.rollback()
            self.logger.error(f"Error saving resume data: {str(e)}")
            return None
        finally:
            session.close()
    
    def save_error_record(self, filename, error_message, file_size=None):
        """
        Save error record when resume processing fails
        
        Args:
            filename (str): Original filename
            error_message (str): Error description
            file_size (int): File size in bytes
            
        Returns:
            int: ID of saved record, None if failed
        """
        if not self.Session:
            return None
        
        session = self.Session()
        try:
            error_record = ParsedResume(
                filename=filename,
                file_size=file_size,
                is_processed_successfully=False,
                error_message=error_message
            )
            
            session.add(error_record)
            session.commit()
            
            record_id = error_record.id
            self.logger.info(f"Error record saved with ID: {record_id}")
            return record_id
            
        except Exception as e:
            session.rollback()
            self.logger.error(f"Error saving error record: {str(e)}")
            return None
        finally:
            session.close()
    
    def get_all_resumes(self, limit=100, offset=0):
        """
        Retrieve all parsed resumes from database
        
        Args:
            limit (int): Maximum number of records to return
            offset (int): Number of records to skip
            
        Returns:
            list: List of resume records
        """
        if not self.Session:
            return []
        
        session = self.Session()
        try:
            resumes = session.query(ParsedResume)\
                           .order_by(ParsedResume.upload_timestamp.desc())\
                           .limit(limit)\
                           .offset(offset)\
                           .all()
            
            return resumes
            
        except Exception as e:
            self.logger.error(f"Error retrieving resumes: {str(e)}")
            return []
        finally:
            session.close()
    
    def get_resume_by_id(self, resume_id):
        """
        Get specific resume by ID
        
        Args:
            resume_id (int): Resume record ID
            
        Returns:
            ParsedResume: Resume record or None
        """
        if not self.Session:
            return None
        
        session = self.Session()
        try:
            resume = session.query(ParsedResume).filter(ParsedResume.id == resume_id).first()
            return resume
            
        except Exception as e:
            self.logger.error(f"Error retrieving resume {resume_id}: {str(e)}")
            return None
        finally:
            session.close()
    
    def search_resumes(self, search_term, search_field='candidate_name'):
        """
        Search resumes by various criteria
        
        Args:
            search_term (str): Term to search for
            search_field (str): Field to search in
            
        Returns:
            list: Matching resume records
        """
        if not self.Session:
            return []
        
        session = self.Session()
        try:
            query = session.query(ParsedResume)
            
            if search_field == 'candidate_name':
                query = query.filter(ParsedResume.candidate_name.ilike(f'%{search_term}%'))
            elif search_field == 'email':
                query = query.filter(ParsedResume.email.ilike(f'%{search_term}%'))
            elif search_field == 'location':
                query = query.filter(ParsedResume.location.ilike(f'%{search_term}%'))
            elif search_field == 'filename':
                query = query.filter(ParsedResume.filename.ilike(f'%{search_term}%'))
            
            resumes = query.order_by(ParsedResume.upload_timestamp.desc()).all()
            return resumes
            
        except Exception as e:
            self.logger.error(f"Error searching resumes: {str(e)}")
            return []
        finally:
            session.close()
    
    def get_statistics(self):
        """
        Get database statistics
        
        Returns:
            dict: Statistics about stored resumes
        """
        if not self.Session:
            return {}
        
        session = self.Session()
        try:
            total_resumes = session.query(ParsedResume).count()
            successful_parses = session.query(ParsedResume).filter(ParsedResume.is_processed_successfully == True).count()
            failed_parses = session.query(ParsedResume).filter(ParsedResume.is_processed_successfully == False).count()
            
            # Average scores
            avg_score_result = session.query(
                ParsedResume.overall_score
            ).filter(ParsedResume.is_processed_successfully == True).all()
            
            if avg_score_result:
                scores = [r.overall_score for r in avg_score_result if r.overall_score is not None]
                avg_score = sum(scores) / len(scores) if scores else 0
            else:
                avg_score = 0
            
            # Recent activity
            from sqlalchemy import func
            recent_uploads = session.query(ParsedResume)\
                                 .filter(ParsedResume.upload_timestamp >= func.now() - func.interval('7 days'))\
                                 .count()
            
            return {
                'total_resumes': total_resumes,
                'successful_parses': successful_parses,
                'failed_parses': failed_parses,
                'success_rate': (successful_parses / total_resumes * 100) if total_resumes > 0 else 0,
                'average_score': round(avg_score, 1),
                'recent_uploads': recent_uploads
            }
            
        except Exception as e:
            self.logger.error(f"Error getting statistics: {str(e)}")
            return {}
        finally:
            session.close()
    
    def delete_resume(self, resume_id):
        """
        Delete a resume record
        
        Args:
            resume_id (int): Resume record ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.Session:
            return False
        
        session = self.Session()
        try:
            resume = session.query(ParsedResume).filter(ParsedResume.id == resume_id).first()
            if resume:
                session.delete(resume)
                session.commit()
                self.logger.info(f"Resume {resume_id} deleted successfully")
                return True
            else:
                self.logger.warning(f"Resume {resume_id} not found")
                return False
                
        except Exception as e:
            session.rollback()
            self.logger.error(f"Error deleting resume {resume_id}: {str(e)}")
            return False
        finally:
            session.close()
    
    def close_connection(self):
        """Close database connection"""
        if self.engine:
            self.engine.dispose()
            self.logger.info("Database connection closed")