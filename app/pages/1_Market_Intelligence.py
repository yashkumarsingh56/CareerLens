import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from analytics_engine import CareerLensEngine

st.set_page_config(page_title="Market Intelligence", page_icon="📊", layout="wide")
st.markdown("""<style>.stApp { background-color: #0E1117; color: #FAFAFA; }</style>""", unsafe_allow_html=True)

@st.cache_resource
def load_engine():
    return CareerLensEngine()

engine = load_engine()
df = engine.df

st.title("📊 Market Intelligence Dashboard")

tab1, tab2, tab3 = st.tabs(["Skills Intelligence", "Salary Intelligence", "Location Intelligence"])

with tab1:
    st.subheader("Top Skills in Demand")
    target_role = st.selectbox("Filter by Role:", ['All'] + engine.get_roles(), key="skill_role")
    
    role_to_analyze = df['job_title'].iloc[0] if target_role == 'All' else target_role # Just passing a valid role to get all if All is not natively supported by engine, wait.
    
    # Actually, let's just do custom extraction for the dashboard for all roles
    if target_role != 'All':
        filtered_df = df[df['job_title'] == target_role]
    else:
        filtered_df = df
        
    skills_series = filtered_df['skills'].dropna().str.split(',').explode().str.strip()
    skill_counts = skills_series.value_counts().head(15).reset_index()
    skill_counts.columns = ['Skill', 'Demand']
    
    fig = px.bar(skill_counts, x='Skill', y='Demand', color='Demand', template='plotly_dark')
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, width='stretch')

with tab2:
    st.subheader("Salary Distribution")
    role_filter = st.selectbox("Filter by Role:", ['All'] + engine.get_roles(), key="sal_role")
    sal_df = df.dropna(subset=['avg_salary_lakhs'])
    if role_filter != 'All':
        sal_df = sal_df[sal_df['job_title'] == role_filter]
        
    fig = px.box(sal_df, x='job_title' if role_filter == 'All' else 'location', y='avg_salary_lakhs', 
                 template='plotly_dark', points="all")
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, width='stretch')

with tab3:
    st.subheader("Location Opportunities")
    loc_stats = df.groupby('location').agg(
        Jobs=('job_id', 'count'),
        Avg_Salary=('avg_salary_lakhs', 'mean')
    ).reset_index().sort_values('Jobs', ascending=False).head(10)
    
    fig = px.scatter(loc_stats, x='Jobs', y='Avg_Salary', text='location', size='Jobs', 
                     color='Avg_Salary', template='plotly_dark')
    fig.update_traces(textposition='top center')
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, width='stretch')
