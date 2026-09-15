import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from analytics_engine import CareerLensEngine

st.set_page_config(
    page_title="CareerLens | Overview",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    .kpi-card {
        background-color: #1E2127; padding: 20px; border-radius: 10px;
        text-align: center; border: 1px solid #2D3139;
    }
    .kpi-value { font-size: 32px; font-weight: bold; color: #4CAF50; }
    .kpi-label { font-size: 14px; color: #A0AAB5; text-transform: uppercase; letter-spacing: 1px; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_engine():
    return CareerLensEngine()

with st.sidebar:
    st.header("Data Sync")
    if st.button("Sync Latest Jobs from API", use_container_width=True):
        with st.spinner("Fetching real jobs from Remotive API..."):
            import subprocess
            subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), '..', 'src', 'fetch_real_jobs.py')])
            st.cache_resource.clear()
            st.rerun()

engine = load_engine()
df = engine.df

st.title("🚀 CareerLens Executive Overview")
st.markdown("Job Market Intelligence Platform")

# Calculate KPIs
total_jobs = len(df)
avg_salary = df['avg_salary_lakhs'].mean()
remote_pct = (len(df[df['work_mode'] == 'Remote']) / total_jobs) * 100

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-value">{total_jobs:,}</div><div class="kpi-label">Total Jobs</div></div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-value">₹{avg_salary:.1f}L</div><div class="kpi-label">Avg Salary</div></div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-value">{remote_pct:.1f}%</div><div class="kpi-label">Remote Work</div></div>""", unsafe_allow_html=True)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Hiring Trend (Last 12 Months)")
    # Group by month
    df['posted_date'] = pd.to_datetime(df['posted_date'])
    trend = df.groupby(df['posted_date'].dt.to_period('M')).size().reset_index(name='Jobs')
    trend['posted_date'] = trend['posted_date'].dt.to_timestamp()
    fig = px.line(trend, x='posted_date', y='Jobs', template='plotly_dark')
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, width='stretch')

with col2:
    st.subheader("Top Job Roles Demand")
    roles = df['job_title'].value_counts().reset_index()
    roles.columns = ['Role', 'Jobs']
    fig = px.bar(roles, x='Jobs', y='Role', orientation='h', template='plotly_dark')
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, width='stretch')
