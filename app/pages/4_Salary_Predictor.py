import streamlit as st
import pandas as pd
import joblib
import os

st.set_page_config(page_title="Salary Predictor", page_icon="💰", layout="wide")

st.title("💰 IT Salary Predictor")
st.markdown("Use our machine learning model to predict the expected salary for a specific role and experience level.")

# Load the model
model_path = os.path.join(os.path.dirname(__file__), '..', '..', 'models', 'salary_predictor.joblib')

@st.cache_resource
def load_model():
    if os.path.exists(model_path):
        return joblib.load(model_path)
    return None

model = load_model()

if model is None:
    st.error("Model not found. Please run the model training script first.")
else:
    col1, col2 = st.columns(2)
    
    with col1:
        roles = [
            'Data Analyst', 'Business Analyst', 'Data Scientist', 'Data Engineer',
            'MERN Stack Engineer', 'Software Engineer', 'Cloud Engineer',
            'DevOps Engineer', 'Frontend Developer', 'Backend Developer',
            'Full Stack Developer', 'Machine Learning Engineer', 'QA Engineer',
            'Site Reliability Engineer', 'Database Administrator', 'Cybersecurity Analyst'
        ]
        selected_role = st.selectbox("Select Role", roles)
        
        locations = ['Bengaluru', 'Hyderabad', 'Pune', 'Delhi NCR', 'Mumbai', 'Chennai', 'Gurgaon', 'Noida', 'Kolkata']
        selected_location = st.selectbox("Select Location", locations)
        
    with col2:
        work_modes = ['Remote', 'On-site', 'Hybrid']
        selected_mode = st.selectbox("Select Work Mode", work_modes)
        
        experience = st.slider("Years of Experience", min_value=0, max_value=15, value=3)
    
    if st.button("Predict Salary", use_container_width=True, type="primary"):
        # Create input dataframe
        input_data = pd.DataFrame({
            'job_title': [selected_role],
            'location': [selected_location],
            'work_mode': [selected_mode],
            'min_exp_years': [experience]
        })
        
        try:
            prediction = model.predict(input_data)[0]
            st.success(f"### Predicted Average Salary: ₹{prediction:.1f} LPA")
            st.info("Note: This is an estimated average based on synthetic market data. Actual salaries may vary based on company size, exact skill set, and interview performance.")
        except Exception as e:
            st.error(f"Error making prediction: {e}")
