import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Constants for generating data
ROLES = [
    'Data Analyst', 'Business Analyst', 'Data Scientist', 'Data Engineer',
    'MERN Stack Engineer', 'Software Engineer', 'Cloud Engineer',
    'DevOps Engineer', 'Frontend Developer', 'Backend Developer',
    'Full Stack Developer', 'Machine Learning Engineer', 'QA Engineer',
    'Site Reliability Engineer', 'Database Administrator', 'Cybersecurity Analyst'
]

COMPANIES = [f'Company {chr(65+i)}' for i in range(26)] + [f'Company {chr(65+i)}{chr(65+i)}' for i in range(10)] + [None] * 4  # Some missing companies
LOCATIONS = ['Bengaluru', 'Hyderabad', 'Pune', 'Delhi NCR', 'Mumbai', 'Chennai', 'Gurgaon', 'Noida', 'Kolkata', None]
WORK_MODES = ['Remote', 'On-site', 'Hybrid']
EMPLOYMENT_TYPES = ['Full-time', 'Contract', 'Part-time']

# Messy skill names for cleaning
SKILLS_POOL = [
    ['SQL', 'MySQL', 'PostgreSQL', 'MS SQL', 'Oracle'],
    ['Python', 'python', 'PYTHON', 'Python 3'],
    ['Java', 'JAVA', 'Core Java', 'Spring Boot'],
    ['JavaScript', 'JS', 'Javascript', 'Vanilla JS'],
    ['React', 'ReactJS', 'React.js', 'react'],
    ['Node.js', 'Node', 'NodeJS', 'node.js'],
    ['MongoDB', 'Mongo', 'mongodb'],
    ['Express.js', 'Express', 'express'],
    ['Power BI', 'PowerBI', 'power bi', 'POWER BI'],
    ['Tableau', 'tableau'],
    ['Excel', 'MS Excel', 'excel'],
    ['AWS', 'aws', 'Amazon Web Services', 'Amazon AWS'],
    ['Azure', 'MS Azure', 'azure'],
    ['GCP', 'Google Cloud', 'gcp'],
    ['Docker', 'docker'],
    ['Kubernetes', 'K8s', 'kubernetes'],
    ['C++', 'CPP', 'c++'],
    ['C#', '.NET', 'C Sharp'],
    ['Statistics', 'Stats'],
    ['Machine Learning', 'ML', 'Machine learning'],
    ['TensorFlow', 'tensorflow', 'TF'],
    ['PyTorch', 'pytorch']
]

def generate_messy_skills(role):
    # Determine base skills based on role to make it somewhat realistic
    base_skills = []
    if 'MERN' in role:
        base_skills = [4, 5, 6, 7] # React, Node, Mongo, Express
    elif 'Data' in role or 'Machine' in role:
        base_skills = [0, 1, 18] # SQL, Python, Stats
    elif 'Cloud' in role or 'DevOps' in role:
        base_skills = [11, 12, 13, 14, 15] # AWS, Azure, GCP, Docker, K8s
    elif 'Frontend' in role:
        base_skills = [3, 4] # JS, React
    elif 'Backend' in role:
        base_skills = [0, 2, 5] # SQL, Java, Node
    else:
        base_skills = [0, 1, 3] # Generic fallback
    
    # Pick 2-4 base skills
    num_base = min(len(base_skills), random.randint(2, 4))
    chosen_indices = random.sample(base_skills, num_base)
    
    # Pick 1-2 random other skills
    other_indices = [i for i in range(len(SKILLS_POOL)) if i not in chosen_indices]
    chosen_indices.extend(random.sample(other_indices, random.randint(1, 2)))
    
    chosen_groups = [SKILLS_POOL[i] for i in chosen_indices]
    skills = [random.choice(group) for group in chosen_groups]
    return ", ".join(skills)

def generate_dataset(num_records=10000):
    data = []
    
    start_date = datetime.now() - timedelta(days=365)
    
    for i in range(num_records):
        role = random.choice(ROLES)
        company = random.choice(COMPANIES)
        location = random.choice(LOCATIONS)
        work_mode = random.choice(WORK_MODES)
        emp_type = random.choice(EMPLOYMENT_TYPES)
        
        # Experience
        exp_min = random.randint(0, 8)
        exp_max = exp_min + random.randint(1, 4)
        experience = f"{exp_min}-{exp_max} years"
        
        # Salary (some missing, some outliers, realistic base)
        if random.random() < 0.05:
            salary = None # 5% missing
        elif random.random() < 0.01:
            salary = "₹60L" # outlier
        else:
            base_salary = random.randint(4, 15)
            # Add premium for experience and certain roles
            base_salary += exp_min * 1.2
            
            # High paying roles
            if role in ['Machine Learning Engineer', 'Data Scientist', 'Cloud Engineer', 'Site Reliability Engineer', 'MERN Stack Engineer']:
                base_salary *= 1.4
            # Medium paying
            elif role in ['Data Engineer', 'Software Engineer', 'DevOps Engineer', 'Full Stack Developer', 'Backend Developer']:
                base_salary *= 1.2
                
            salary_str = f"₹{round(base_salary, 1)}L - ₹{round(base_salary + random.uniform(2.0, 5.0), 1)}L"
            salary = salary_str
            
        skills = generate_messy_skills(role)
        
        # Date
        posted_date = start_date + timedelta(days=random.randint(0, 365))
        
        # Description
        description = f"We are looking for a highly skilled {role} to join our engineering team. Required skills include {skills}. Apply now to join {company if company else 'our fast-growing startup'}."
        
        data.append({
            'job_id': f"JOB_{i:05d}",
            'job_title': role,
            'company': company,
            'location': location,
            'experience': experience,
            'salary': salary,
            'work_mode': work_mode,
            'employment_type': emp_type,
            'skills': skills,
            'posted_date': posted_date.strftime('%Y-%m-%d'),
            'description': description
        })
        
    df = pd.DataFrame(data)
    
    # Introduce some duplicates
    duplicates = df.sample(frac=0.03)
    df = pd.concat([df, duplicates], ignore_index=True)
    
    # Shuffle
    df = df.sample(frac=1).reset_index(drop=True)
    
    return df

if __name__ == "__main__":
    print("Generating synthetic job dataset with comprehensive IT roles...")
    df = generate_dataset(10000)
    output_path = "data/raw/jobs_raw.csv"
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} records and saved to {output_path}")
