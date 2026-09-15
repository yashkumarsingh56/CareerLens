import streamlit as st
import pandas as pd
import fitz  # PyMuPDF
import re

st.set_page_config(page_title="Resume Parser", page_icon="📄", layout="wide")

st.title("📄 AI Resume Parser & Market Fit")
st.markdown("Upload your resume (PDF) to automatically extract skills and see how well you match current IT market demands.")

# Skill vocabulary based on our dataset
SKILL_VOCAB = [
    'SQL', 'Python', 'Java', 'JavaScript', 'React', 'Node.js', 'MongoDB', 
    'Express.js', 'Power BI', 'Tableau', 'Excel', 'AWS', 'Azure', 'GCP', 
    'Docker', 'Kubernetes', 'C++', 'C#', 'Statistics', 'Machine Learning', 
    'TensorFlow', 'PyTorch'
]

def extract_text_from_pdf(uploaded_file):
    try:
        # Read the file bytes
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

def extract_skills(text):
    text_lower = text.lower()
    found_skills = []
    
    for skill in SKILL_VOCAB:
        # Simple string matching (can be improved with regex word boundaries)
        # Using word boundaries for short skills like C++ or C# can be tricky due to special chars
        # For alphanumeric skills, we use \b
        
        # Escape special characters in skill name for regex
        escaped_skill = re.escape(skill.lower())
        
        # If skill contains special characters at the end (like C++, C#), don't enforce word boundary at the end
        if re.search(r'\w$', skill):
            pattern = r'\b' + escaped_skill + r'\b'
        else:
            pattern = r'\b' + escaped_skill
            
        if re.search(pattern, text_lower):
            found_skills.append(skill)
            
    return found_skills

uploaded_file = st.file_uploader("Upload Resume (PDF format)", type=['pdf'])

if uploaded_file is not None:
    with st.spinner("Analyzing resume..."):
        text = extract_text_from_pdf(uploaded_file)
        
        if text:
            extracted_skills = extract_skills(text)
            
            st.success("Analysis Complete!")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.subheader("Extracted Skills")
                if not extracted_skills:
                    st.warning("No standard IT skills detected. Ensure your resume contains keywords like Python, React, AWS, etc.")
                else:
                    for skill in extracted_skills:
                        st.markdown(f"✅ **{skill}**")
                        
            with col2:
                st.subheader("Market Fit Analysis")
                
                if extracted_skills:
                    # Let's mock a simple market fit based on the number of skills
                    # Ideally, we'd query the generated data, but for simplicity we calculate a score
                    
                    score = min(len(extracted_skills) * 10, 100)
                    
                    st.progress(score / 100.0)
                    st.markdown(f"**Overall Market Match Score: {score}%**")
                    
                    if score > 80:
                        st.success("Excellent! You have a highly competitive skill set.")
                    elif score > 50:
                        st.info("Good! You have a solid foundation. Consider learning more modern frameworks or cloud technologies.")
                    else:
                        st.warning("Needs Improvement. You may want to acquire more in-demand skills like Cloud (AWS/Azure) or specific frameworks.")
                    
                    # Missing Skills Recommendation
                    missing_skills = [s for s in ['Python', 'AWS', 'SQL', 'React', 'Docker'] if s not in extracted_skills]
                    if missing_skills:
                        st.markdown("### Top Skills to Learn Next for Highest ROI")
                        for s in missing_skills:
                            st.markdown(f"- 🚀 **{s}**")
                else:
                    st.info("Upload a resume with IT skills to see your market fit.")
