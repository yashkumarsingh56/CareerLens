import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from analytics_engine import CareerLensEngine

st.set_page_config(page_title="Latest Jobs", page_icon="💼", layout="wide")
st.markdown("""<style>.stApp { background-color: #0E1117; color: #FAFAFA; }</style>""", unsafe_allow_html=True)

@st.cache_resource
def load_engine():
    return CareerLensEngine()

engine = load_engine()
df = engine.df

st.title("💼 Latest Active Jobs")
st.markdown("Browse the real, active job postings fetched directly from the internet and apply to them instantly!")

if 'apply_link' not in df.columns:
    st.warning("Please click the 'Sync Latest Jobs from API' button on the Home page first to get apply links.")
else:
    # Select columns to display
    display_df = df[['job_title', 'company', 'location', 'skills', 'posted_date', 'apply_link']].copy()
    display_df.rename(columns={
        'job_title': 'Role',
        'company': 'Company',
        'location': 'Location',
        'skills': 'Required Skills',
        'posted_date': 'Date',
        'apply_link': 'Apply Here'
    }, inplace=True)
    
    st.dataframe(
        display_df,
        column_config={
            "Apply Here": st.column_config.LinkColumn(
                "Apply Here",
                help="Click to apply to this job",
                display_text="Apply Now ↗"
            )
        },
        hide_index=True,
        use_container_width=True
    )
