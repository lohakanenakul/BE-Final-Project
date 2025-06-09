import streamlit as st
import pandas as pd
import json
from resume_parser import ResumeParser
from data_exporter import DataExporter
from database_manager import DatabaseManager
import tempfile
import os
import time

# Initialize the resume parser and database
@st.cache_resource
def get_resume_parser():
    return ResumeParser()

@st.cache_resource
def get_database_manager():
    return DatabaseManager()

def main():
    st.title("🔍 Resume Parser & Analysis Tool")
    st.markdown("Upload resumes in PDF or DOCX format to extract structured information for recruitment screening.")
    
    # Initialize parser and database
    parser = get_resume_parser()
    db_manager = get_database_manager()
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", [
        "Upload & Parse Resumes", 
        "View Stored Resumes", 
        "Search Database", 
        "Analytics Dashboard"
    ])
    
    if page == "Upload & Parse Resumes":
        upload_and_parse_page(parser, db_manager)
    elif page == "View Stored Resumes":
        view_stored_resumes_page(db_manager)
    elif page == "Search Database":
        search_database_page(db_manager)
    elif page == "Analytics Dashboard":
        analytics_dashboard_page(db_manager)

def upload_and_parse_page(parser, db_manager):
    """Upload and parse resumes page"""
    st.header("📄 Upload Resume")
    uploaded_files = st.file_uploader(
        "Choose resume files",
        type=['pdf', 'docx'],
        accept_multiple_files=True,
        help="Supported formats: PDF, DOCX"
    )
    
    if uploaded_files:
        # Process each uploaded file
        for uploaded_file in uploaded_files:
            st.subheader(f"Processing: {uploaded_file.name}")
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            try:
                # Parse the resume with timing
                start_time = time.time()
                with st.spinner("Parsing resume..."):
                    parsed_data = parser.parse_resume(tmp_file_path)
                processing_time = time.time() - start_time
                
                if parsed_data:
                    # Save to database
                    record_id = db_manager.save_parsed_resume(
                        parsed_data, 
                        uploaded_file.name, 
                        processing_time
                    )
                    
                    if record_id:
                        st.success(f"Resume saved to database with ID: {record_id}")
                    else:
                        st.warning("Resume parsed but failed to save to database")
                    
                    # Display results
                    display_parsed_results(parsed_data, uploaded_file.name)
                    
                    # Export options
                    st.subheader("📤 Export Options")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button(f"Export JSON", key=f"json_{uploaded_file.name}"):
                            json_data = DataExporter.to_json(parsed_data)
                            st.download_button(
                                label="Download JSON",
                                data=json_data,
                                file_name=f"{uploaded_file.name.split('.')[0]}_parsed.json",
                                mime="application/json"
                            )
                    
                    with col2:
                        if st.button(f"Export CSV", key=f"csv_{uploaded_file.name}"):
                            csv_data = DataExporter.to_csv(parsed_data)
                            st.download_button(
                                label="Download CSV",
                                data=csv_data,
                                file_name=f"{uploaded_file.name.split('.')[0]}_parsed.csv",
                                mime="text/csv"
                            )
                    
                    with col3:
                        if st.button(f"Export Excel", key=f"excel_{uploaded_file.name}"):
                            excel_data = DataExporter.to_excel(parsed_data)
                            if excel_data:
                                st.download_button(
                                    label="Download Excel",
                                    data=excel_data,
                                    file_name=f"{uploaded_file.name.split('.')[0]}_parsed.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                )
                else:
                    error_msg = f"Failed to parse {uploaded_file.name}"
                    st.error(error_msg)
                    # Save error record
                    db_manager.save_error_record(
                        uploaded_file.name, 
                        error_msg,
                        len(uploaded_file.getvalue())
                    )
                    
            except Exception as e:
                error_msg = f"Error processing {uploaded_file.name}: {str(e)}"
                st.error(error_msg)
                # Save error record
                db_manager.save_error_record(
                    uploaded_file.name, 
                    error_msg,
                    len(uploaded_file.getvalue())
                )
            
            finally:
                # Clean up temporary file
                if os.path.exists(tmp_file_path):
                    os.unlink(tmp_file_path)
            
            st.divider()

def view_stored_resumes_page(db_manager):
    """View stored resumes page"""
    st.header("📊 Stored Resumes")
    
    # Get all resumes
    resumes = db_manager.get_all_resumes(limit=50)
    
    if not resumes:
        st.info("No resumes found in database")
        return
    
    # Display summary
    st.metric("Total Stored Resumes", len(resumes))
    
    # Create table data
    table_data = []
    for resume in resumes:
        table_data.append({
            "ID": resume.id,
            "Name": resume.candidate_name or "Unknown",
            "Email": resume.email or "N/A",
            "Score": resume.overall_score,
            "Upload Date": resume.upload_timestamp.strftime("%Y-%m-%d %H:%M") if resume.upload_timestamp else "N/A",
            "Status": "✅ Success" if resume.is_processed_successfully else "❌ Failed"
        })
    
    df = pd.DataFrame(table_data)
    
    # Display interactive table
    selected_resume = st.selectbox(
        "Select a resume to view details:",
        options=[""] + [f"ID {r.id} - {r.candidate_name or r.filename}" for r in resumes]
    )
    
    if selected_resume:
        resume_id = int(selected_resume.split()[1])
        selected_resume_data = db_manager.get_resume_by_id(resume_id)
        
        if selected_resume_data:
            display_stored_resume_details(selected_resume_data, db_manager)
    
    # Show table
    st.dataframe(df, use_container_width=True)

def search_database_page(db_manager):
    """Search database page"""
    st.header("🔍 Search Resumes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        search_field = st.selectbox(
            "Search by:",
            ["candidate_name", "email", "location", "filename"]
        )
    
    with col2:
        search_term = st.text_input("Search term:")
    
    if search_term:
        results = db_manager.search_resumes(search_term, search_field)
        
        if results:
            st.success(f"Found {len(results)} matching resumes")
            
            for resume in results:
                with st.expander(f"{resume.candidate_name or 'Unknown'} - Score: {resume.overall_score}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Email:** {resume.email or 'N/A'}")
                        st.write(f"**Location:** {resume.location or 'N/A'}")
                        st.write(f"**Upload Date:** {resume.upload_timestamp}")
                    
                    with col2:
                        st.write(f"**Overall Score:** {resume.overall_score}")
                        st.write(f"**Filename:** {resume.filename}")
                        st.write(f"**Processing:** {'Success' if resume.is_processed_successfully else 'Failed'}")
                    
                    if resume.professional_summary:
                        st.write("**Summary:**")
                        st.write(resume.professional_summary)
        else:
            st.info("No matching resumes found")

def analytics_dashboard_page(db_manager):
    """Analytics dashboard page"""
    st.header("📈 Analytics Dashboard")
    
    # Get statistics
    stats = db_manager.get_statistics()
    
    if not stats:
        st.error("Unable to load statistics")
        return
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Resumes", stats.get('total_resumes', 0))
    
    with col2:
        st.metric("Success Rate", f"{stats.get('success_rate', 0):.1f}%")
    
    with col3:
        st.metric("Average Score", stats.get('average_score', 0))
    
    with col4:
        st.metric("Recent Uploads", stats.get('recent_uploads', 0))
    
    # Processing success chart
    st.subheader("Processing Results")
    success_data = {
        'Status': ['Successful', 'Failed'],
        'Count': [stats.get('successful_parses', 0), stats.get('failed_parses', 0)]
    }
    st.bar_chart(pd.DataFrame(success_data).set_index('Status'))
    
    # Recent resumes
    st.subheader("Recent Uploads")
    recent_resumes = db_manager.get_all_resumes(limit=10)
    
    if recent_resumes:
        recent_data = []
        for resume in recent_resumes:
            recent_data.append({
                "Name": resume.candidate_name or "Unknown",
                "Score": resume.overall_score,
                "Date": resume.upload_timestamp.strftime("%Y-%m-%d") if resume.upload_timestamp else "N/A",
                "Status": "Success" if resume.is_processed_successfully else "Failed"
            })
        
        st.dataframe(pd.DataFrame(recent_data), use_container_width=True)

def display_stored_resume_details(resume, db_manager):
    """Display detailed view of stored resume"""
    st.subheader(f"Resume Details - {resume.candidate_name or 'Unknown'}")
    
    # Basic information
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**ID:** {resume.id}")
        st.write(f"**Name:** {resume.candidate_name or 'N/A'}")
        st.write(f"**Email:** {resume.email or 'N/A'}")
        st.write(f"**Phone:** {resume.phone or 'N/A'}")
    
    with col2:
        st.write(f"**Location:** {resume.location or 'N/A'}")
        st.write(f"**Upload Date:** {resume.upload_timestamp}")
        st.write(f"**Overall Score:** {resume.overall_score}")
        st.write(f"**Processing Time:** {resume.processing_time_seconds:.2f}s" if resume.processing_time_seconds else "N/A")
    
    # Professional summary
    if resume.professional_summary:
        st.subheader("Professional Summary")
        st.write(resume.professional_summary)
    
    # Experience
    experience_data = resume.get_experience_data()
    if experience_data:
        st.subheader("Work Experience")
        for i, exp in enumerate(experience_data):
            with st.expander(f"{exp.get('title', 'Position')} at {exp.get('company', 'Company')}"):
                st.write(f"**Duration:** {exp.get('duration', 'N/A')}")
                if exp.get('description'):
                    st.write(f"**Description:** {exp['description']}")
    
    # Education
    education_data = resume.get_education_data()
    if education_data:
        st.subheader("Education")
        for edu in education_data:
            st.write(f"**{edu.get('degree', 'Degree')}** - {edu.get('institution', 'Institution')}")
            if edu.get('year'):
                st.write(f"Year: {edu['year']}")
    
    # Skills
    skills_data = resume.get_skills_data()
    if skills_data:
        st.subheader("Skills")
        skills_by_category = {}
        for skill in skills_data:
            if isinstance(skill, dict):
                category = skill.get('category', 'General')
                if category not in skills_by_category:
                    skills_by_category[category] = []
                skills_by_category[category].append(skill.get('name', ''))
        
        for category, skills in skills_by_category.items():
            st.write(f"**{category}:** {', '.join(skills)}")
    
    # Delete option
    if st.button(f"Delete Resume {resume.id}", type="secondary"):
        if db_manager.delete_resume(resume.id):
            st.success("Resume deleted successfully")
            st.rerun()
        else:
            st.error("Failed to delete resume")
    
    # Instructions and information
    with st.expander("ℹ️ How to use this tool"):
        st.markdown("""
        1. **Upload resumes**: Select one or more PDF or DOCX files
        2. **View extracted data**: The tool will automatically extract and display structured information
        3. **Export results**: Download the parsed data in JSON or CSV format
        
        **What information is extracted:**
        - Personal information (name, contact details)
        - Professional summary
        - Work experience
        - Education background
        - Skills and competencies
        - Certifications and achievements
        
        **Scoring system:**
        - Experience score based on years and relevance
        - Skills score based on keyword matching
        - Education score based on qualifications
        - Overall candidate score (0-100)
        """)
    
    with st.expander("⚠️ Privacy & Security"):
        st.markdown("""
        - All uploaded files are processed locally and temporarily
        - No resume data is stored permanently on our servers
        - Files are automatically deleted after processing
        - Your data privacy is our priority
        """)

def display_parsed_results(parsed_data, filename):
    """Display parsed resume data in organized sections"""
    
    # Overall score
    if 'overall_score' in parsed_data:
        score = parsed_data['overall_score']
        st.metric("Overall Candidate Score", f"{score}/100", 
                 delta=f"{'Above Average' if score > 60 else 'Below Average'}")
    
    # Personal Information
    st.subheader("👤 Personal Information")
    personal_info = parsed_data.get('personal_info', {})
    
    if personal_info:
        col1, col2 = st.columns(2)
        with col1:
            if personal_info.get('name'):
                st.write(f"**Name:** {personal_info['name']}")
            if personal_info.get('email'):
                st.write(f"**Email:** {personal_info['email']}")
            if personal_info.get('phone'):
                st.write(f"**Phone:** {personal_info['phone']}")
        
        with col2:
            if personal_info.get('location'):
                st.write(f"**Location:** {personal_info['location']}")
            if personal_info.get('linkedin'):
                st.write(f"**LinkedIn:** {personal_info['linkedin']}")
    else:
        st.write("No personal information extracted")
    
    # Professional Summary
    if parsed_data.get('summary'):
        st.subheader("📝 Professional Summary")
        st.write(parsed_data['summary'])
    
    # Experience
    st.subheader("💼 Work Experience")
    experience = parsed_data.get('experience', [])
    
    if experience:
        for i, exp in enumerate(experience):
            with st.expander(f"{exp.get('title', 'Position')} at {exp.get('company', 'Company')}", expanded=i==0):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Position:** {exp.get('title', 'N/A')}")
                    st.write(f"**Company:** {exp.get('company', 'N/A')}")
                with col2:
                    st.write(f"**Duration:** {exp.get('duration', 'N/A')}")
                    st.write(f"**Location:** {exp.get('location', 'N/A')}")
                
                if exp.get('description'):
                    st.write("**Description:**")
                    st.write(exp['description'])
    else:
        st.write("No work experience found")
    
    # Education
    st.subheader("🎓 Education")
    education = parsed_data.get('education', [])
    
    if education:
        for edu in education:
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Degree:** {edu.get('degree', 'N/A')}")
                st.write(f"**Institution:** {edu.get('institution', 'N/A')}")
            with col2:
                st.write(f"**Year:** {edu.get('year', 'N/A')}")
                if edu.get('gpa'):
                    st.write(f"**GPA:** {edu['gpa']}")
    else:
        st.write("No education information found")
    
    # Skills
    st.subheader("🛠️ Skills")
    skills = parsed_data.get('skills', [])
    
    if skills:
        # Group skills by category if available
        skill_categories = {}
        for skill in skills:
            if isinstance(skill, dict):
                category = skill.get('category', 'General')
                if category not in skill_categories:
                    skill_categories[category] = []
                skill_categories[category].append(skill.get('name', skill))
            else:
                if 'General' not in skill_categories:
                    skill_categories['General'] = []
                skill_categories['General'].append(skill)
        
        for category, category_skills in skill_categories.items():
            st.write(f"**{category}:**")
            st.write(", ".join(category_skills))
    else:
        st.write("No skills found")
    
    # Confidence Scores
    if 'confidence_scores' in parsed_data:
        st.subheader("📊 Extraction Confidence")
        confidence = parsed_data['confidence_scores']
        
        cols = st.columns(len(confidence))
        for i, (section, score) in enumerate(confidence.items()):
            with cols[i]:
                st.metric(section.title(), f"{score}%")

if __name__ == "__main__":
    main()
