import pandas as pd
from sqlalchemy import create_engine
import re

# IMPORTANT: Ensure you have PostgreSQL installed and running.
# Update the connection string with your PostgreSQL username, password, host, and database name.
DB_USER = 'postgres'
DB_PASSWORD = 'password'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'careerlens'

def parse_salary(salary_str):
    if pd.isna(salary_str):
        return None, None
    # Extract numbers from format like "₹4.0L - ₹5.5L" or "₹50L"
    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", salary_str)
    if len(numbers) >= 2:
        return float(numbers[0]), float(numbers[1])
    elif len(numbers) == 1:
        return float(numbers[0]), float(numbers[0])
    return None, None

def load_data_to_postgres():
    print("Loading cleaned dataset...")
    df = pd.read_csv('data/processed/jobs_cleaned.csv')
    
    print("Connecting to PostgreSQL...")
    engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
    
    # 1. Populate Dimensions
    print("Populating Dimensions...")
    
    # dim_location
    locations = df[['location']].drop_duplicates().dropna().rename(columns={'location': 'city'})
    locations.to_sql('dim_location', engine, if_exists='append', index=False)
    
    # dim_company
    companies = df[['company']].drop_duplicates().dropna().rename(columns={'company': 'company_name'})
    companies.to_sql('dim_company', engine, if_exists='append', index=False)
    
    # dim_role
    roles = df[['job_title']].drop_duplicates().dropna()
    roles.to_sql('dim_role', engine, if_exists='append', index=False)
    
    # dim_skill
    skills_set = set()
    for skills_str in df['skills'].dropna():
        for skill in skills_str.split(','):
            skills_set.add(skill.strip())
    skills_df = pd.DataFrame(list(skills_set), columns=['skill_name'])
    skills_df.to_sql('dim_skill', engine, if_exists='append', index=False)
    
    # 2. Fetch Dimension Mappings
    print("Fetching mappings...")
    loc_map = pd.read_sql("SELECT location_id, city FROM dim_location", engine).set_index('city')['location_id'].to_dict()
    comp_map = pd.read_sql("SELECT company_id, company_name FROM dim_company", engine).set_index('company_name')['company_id'].to_dict()
    role_map = pd.read_sql("SELECT role_id, job_title FROM dim_role", engine).set_index('job_title')['role_id'].to_dict()
    skill_map = pd.read_sql("SELECT skill_id, skill_name FROM dim_skill", engine).set_index('skill_name')['skill_id'].to_dict()
    
    # 3. Populate Fact Tables
    print("Populating Fact Tables...")
    fact_jobs = []
    fact_job_skills = []
    
    for _, row in df.iterrows():
        job_id = row['job_id']
        sal_min, sal_max = parse_salary(row['salary'])
        
        fact_jobs.append({
            'job_id': job_id,
            'role_id': role_map.get(row['job_title']),
            'company_id': comp_map.get(row['company']),
            'location_id': loc_map.get(row['location']),
            'experience': row['experience'],
            'salary_string': row['salary'],
            'salary_min': sal_min,
            'salary_max': sal_max,
            'work_mode': row['work_mode'],
            'employment_type': row['employment_type'],
            'posted_date': row['posted_date']
        })
        
        # Job Skills
        if pd.notna(row['skills']):
            for skill in row['skills'].split(','):
                skill_id = skill_map.get(skill.strip())
                if skill_id:
                    fact_job_skills.append({
                        'job_id': job_id,
                        'skill_id': skill_id
                    })
                    
    pd.DataFrame(fact_jobs).to_sql('fact_jobs', engine, if_exists='append', index=False)
    pd.DataFrame(fact_job_skills).to_sql('fact_job_skills', engine, if_exists='append', index=False)
    
    print("Data successfully loaded into PostgreSQL!")

if __name__ == '__main__':
    load_data_to_postgres()
