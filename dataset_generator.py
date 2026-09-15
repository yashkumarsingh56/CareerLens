import csv
import random
from datetime import datetime, timedelta

def generate_dataset(num_records=1000):
    companies = ["TCS", "Infosys", "Wipro", "Amazon", "Google", "Microsoft", "Accenture", "IBM", "Deloitte", "Flipkart"]
    locations = ["Bangalore", "Delhi NCR", "Hyderabad", "Pune", "Mumbai", "Remote"]
    job_roles = ["Data Analyst", "Senior Data Analyst", "Data Scientist", "Business Analyst", "BI Developer"]
    skills_pool = ["Excel", "SQL", "Power BI", "Python", "Tableau", "R", "AWS", "Machine Learning"]
    
    with open('job_market_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['job_id', 'company', 'role', 'location', 'experience_required', 'work_type', 'skills_required', 'min_salary_lpa', 'max_salary_lpa', 'posted_date'])
        
        for i in range(1, num_records + 1):
            company = random.choice(companies)
            role = random.choice(job_roles)
            location = random.choice(locations)
            
            # 0: Fresher, 1: 1-3 years, 2: 3-5 years, 3: 5+ years
            exp_level = random.choices(["Fresher", "1-3 years", "3-5 years", "5+ years"], weights=[0.2, 0.4, 0.3, 0.1])[0]
            work_type = random.choices(["Onsite", "Remote", "Hybrid"], weights=[0.5, 0.3, 0.2])[0]
            
            num_skills = random.randint(2, 5)
            skills = ", ".join(random.sample(skills_pool, num_skills))
            
            # Base salary logic based on experience
            if exp_level == "Fresher":
                min_sal = random.randint(3, 5)
                max_sal = min_sal + random.randint(1, 2)
            elif exp_level == "1-3 years":
                min_sal = random.randint(5, 9)
                max_sal = min_sal + random.randint(2, 4)
            elif exp_level == "3-5 years":
                min_sal = random.randint(9, 15)
                max_sal = min_sal + random.randint(3, 6)
            else:
                min_sal = random.randint(15, 25)
                max_sal = min_sal + random.randint(5, 10)
                
            # Bump salary if Python/AWS are present
            if "Python" in skills or "AWS" in skills:
                min_sal += random.randint(1, 3)
                max_sal += random.randint(1, 4)
                
            posted_date = (datetime.now() - timedelta(days=random.randint(0, 60))).strftime('%Y-%m-%d')
            
            writer.writerow([f'JOB{i:05d}', company, role, location, exp_level, work_type, skills, min_sal, max_sal, posted_date])

if __name__ == "__main__":
    generate_dataset(5000)
    print("Synthetic dataset 'job_market_data.csv' generated successfully with 5000 records!")
