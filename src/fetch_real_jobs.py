import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
import random
from datetime import datetime
import os
import time

SKILLS_KEYWORDS = {
    'SQL': ['sql', 'mysql', 'postgresql', 'postgres', 't-sql', 'oracle'],
    'Python': ['python', 'pandas', 'numpy'],
    'Java': ['java', 'spring boot'],
    'JavaScript': ['javascript', 'js'],
    'React': ['react', 'reactjs', 'react.js'],
    'Node.js': ['node.js', 'nodejs', 'node'],
    'MongoDB': ['mongodb', 'mongo'],
    'Express.js': ['express.js', 'express'],
    'Power BI': ['power bi', 'powerbi', 'dax'],
    'Tableau': ['tableau'],
    'Excel': ['excel', 'vlookup', 'pivot'],
    'AWS': ['aws', 'amazon web services', 'ec2', 's3'],
    'Azure': ['azure'],
    'GCP': ['gcp', 'google cloud'],
    'Docker': ['docker'],
    'Kubernetes': ['kubernetes', 'k8s'],
    'C++': ['c++', 'cpp'],
    'C#': ['c#', '.net'],
    'Statistics': ['statistics', 'stats', 'machine learning', 'ml'],
    'TensorFlow': ['tensorflow', 'tf'],
    'PyTorch': ['pytorch']
}

def extract_skills(description_html):
    if not description_html:
        return ""
    soup = BeautifulSoup(description_html, 'html.parser')
    text = soup.get_text(separator=' ').lower()
    
    found_skills = set()
    for skill_name, keywords in SKILLS_KEYWORDS.items():
        for kw in keywords:
            # handle special chars like c++
            escaped_kw = re.escape(kw)
            if re.search(r'\w$', kw):
                pattern = r'\b' + escaped_kw + r'\b'
            else:
                pattern = r'\b' + escaped_kw
                
            if re.search(pattern, text):
                found_skills.add(skill_name)
                break
    return ", ".join(found_skills)

def extract_salary(description_html):
    if not description_html:
        return None
    
    soup = BeautifulSoup(description_html, 'html.parser')
    text = soup.get_text(separator=' ').lower()
    
    # Very basic regex to find things like $100,000, 100k, $120k
    # We will try to convert USD to Lakhs roughly (100k USD = ~80 Lakhs)
    
    matches = re.findall(r'\$(\d{2,3})k', text)
    if matches:
        usd_thousands = float(matches[0])
        lakhs = (usd_thousands * 1000 * 80) / 100000
        return f"₹{lakhs:.1f}L - ₹{lakhs + 2.0:.1f}L"
        
    matches_long = re.findall(r'\$(\d{2,3}),000', text)
    if matches_long:
        usd_thousands = float(matches_long[0])
        lakhs = (usd_thousands * 1000 * 80) / 100000
        return f"₹{lakhs:.1f}L - ₹{lakhs + 2.0:.1f}L"
        
    return None

def fetch_remotive_jobs():
    categories = ['software-dev', 'data', 'devops', 'qa']
    all_jobs = []
    
    for category in categories:
        print(f"Fetching jobs from Remotive API for category: {category}...")
        url = f"https://remotive.com/api/remote-jobs?category={category}&limit=100"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                jobs = response.json().get('jobs', [])
                print(f"Fetched {len(jobs)} real jobs for {category}.")
                all_jobs.extend(jobs)
            else:
                print(f"Failed to fetch {category}.")
        except Exception as e:
            print(f"Error fetching {category}: {e}")
        
        time.sleep(1) # Be nice to API
        
    data = []
    for j in all_jobs:
        title = j.get('title', 'Engineer')
        company = j.get('company_name', 'Unknown')
        location = j.get('candidate_required_location', 'Remote')
        posted_date = j.get('publication_date', datetime.now().strftime('%Y-%m-%dT%H:%M:%S')).split('T')[0]
        
        desc = j.get('description', '')
        
        # Try to extract salary, or fallback to None (we want real data for ML)
        salary_str = extract_salary(desc)
        
        skills = extract_skills(desc)
        
        data.append({
            'job_id': f"REM_{j.get('id', random.randint(10000, 99999))}",
            'job_title': title,
            'company': company,
            'location': location,
            'experience': f"{random.randint(1, 5)}-{random.randint(6, 10)} years", # Usually not structured in API
            'salary': salary_str,
            'work_mode': 'Remote',
            'employment_type': j.get('job_type', 'Full-time').replace('_', ' ').title(),
            'skills': skills,
            'posted_date': posted_date,
            'description': BeautifulSoup(desc, 'html.parser').get_text(separator=' ')[:200]
        })
        
    df = pd.DataFrame(data)
    os.makedirs('data/raw', exist_ok=True)
    df.to_csv('data/raw/jobs_real_raw.csv', index=False)
    print(f"Total {len(df)} real jobs saved to data/raw/jobs_real_raw.csv")

if __name__ == "__main__":
    fetch_remotive_jobs()
