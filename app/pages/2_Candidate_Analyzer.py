import streamlit as st
import pandas as pd
import sys
import os

# Add src directory to path to import engine
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from analytics_engine import CareerLensEngine

# Configure page
st.set_page_config(
    page_title="CareerLens | Candidate Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark SaaS theme
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .kpi-card {
        background-color: #1E2127;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        text-align: center;
        border: 1px solid #2D3139;
    }
    .kpi-value {
        font-size: 32px;
        font-weight: bold;
        color: #4CAF50;
    }
    .kpi-label {
        font-size: 14px;
        color: #A0AAB5;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_engine():
    try:
        return CareerLensEngine()
    except FileNotFoundError:
        st.error("Data not found. Please run the data generator and cleaning scripts first.")
        st.stop()

engine = load_engine()

# Layout
st.title("🔍 CareerLens Candidate Analyzer")
st.markdown("Know your position in the market based on real job data.")

# Sidebar Inputs
with st.sidebar:
    st.header("Your Profile")
    roles = engine.get_roles()
    locations = ['All'] + engine.get_locations()
    skills_list = engine.get_all_skills()
    
    target_role = st.selectbox("Target Role", roles)
    location = st.selectbox("Location", locations)
    experience = st.selectbox("Experience", ["Fresher (0-1 yrs)", "Junior (1-3 yrs)", "Mid-level (3-5 yrs)", "Senior (5+ yrs)"])
    
    candidate_skills = st.multiselect("Your Skills", skills_list, default=['SQL', 'Excel'])
    
    analyze_btn = st.button("ANALYZE MY PROFILE", type="primary", use_container_width=True)

if analyze_btn or 'analyzed' not in st.session_state:
    st.session_state.analyzed = True
    
    if not candidate_skills:
        st.warning("Please select at least one skill to analyze.")
    else:
        results, missing_skills = engine.analyze_candidate(target_role, location, candidate_skills)
        
        if not results or missing_skills.empty:
            st.info("Not enough data for this specific combination. Try selecting 'All' locations.")
        else:
            # Score Section
            st.markdown("### CareerLens Score")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-value">{results['match_score']}%</div>
                    <div class="kpi-label">Job Match Score</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-value">{len(candidate_skills)}</div>
                    <div class="kpi-label">Verified Skills</div>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-value">₹{results['market_avg_salary']}L</div>
                    <div class="kpi-label">Market Avg Salary</div>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("---")
            
            # Gap Analysis
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("✅ Strong Market Fit")
                for skill in candidate_skills:
                    st.markdown(f"- ✓ **{skill}**")
                    
            with col2:
                st.subheader("🚨 Skill Gap Analyzer")
                st.markdown("Based on market demand, here is your next best skill to learn:")
                
                top_missing = missing_skills.head(3)
                
                if not top_missing.empty:
                    st.success(f"**TOP RECOMMENDATION:** Learn **{top_missing.iloc[0]['Skill']}**")
                    st.caption(f"{top_missing.iloc[0]['Demand (%)']:.1f}% of {target_role} jobs in {location} mention it.")
                    
                    st.markdown("Other recommended skills:")
                    for i, row in top_missing.iloc[1:].iterrows():
                        st.markdown(f"- ⚠ **{row['Skill']}** (Demand: {row['Demand (%)']:.1f}%)")
                else:
                    st.success("You have all the highly demanded skills for this role!")

            # Career Roadmap
            st.markdown("---")
            st.subheader("📈 Personalized Career Roadmap")
            
            if not top_missing.empty:
                st.markdown(f"""
                - **CURRENT:** Solidify {", ".join(candidate_skills[:3])}
                - **NEXT 30 DAYS:** Fundamentals of **{top_missing.iloc[0]['Skill']}**
                - **30-60 DAYS:** Practical projects using {top_missing.iloc[0]['Skill']}
                - **JOB READY:** {target_role}
                """)
            
            st.caption(f"Analysis based on {results['total_jobs_analyzed']} recent job postings.")
