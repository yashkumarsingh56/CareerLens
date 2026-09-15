import pandas as pd
import re

def clean_data(input_path, output_path):
    print(f"Loading data from {input_path}...")
    df = pd.read_csv(input_path)
    
    # 1. Remove duplicates
    initial_count = len(df)
    df.drop_duplicates(inplace=True)
    print(f"Removed {initial_count - len(df)} duplicate rows.")
    
    # 2. Handle missing values
    df['company'] = df['company'].fillna('Unknown')
    df['location'] = df['location'].fillna('Unknown')
    # Not dropping missing salaries to allow for Data Quality checks later
    
    # 3. Standardize skills
    def standardize_skills(skills_str):
        if pd.isna(skills_str):
            return skills_str
        
        skills = [s.strip() for s in skills_str.split(',')]
        cleaned_skills = []
        for s in skills:
            s_lower = s.lower()
            if 'power' in s_lower and 'bi' in s_lower:
                cleaned_skills.append('Power BI')
            elif 'mysql' in s_lower or 'postgresql' in s_lower or 'oracle' in s_lower or 'sql' in s_lower:
                cleaned_skills.append('SQL')
            elif 'python' in s_lower:
                cleaned_skills.append('Python')
            elif 'java' in s_lower and not 'javascript' in s_lower:
                cleaned_skills.append('Java')
            elif 'javascript' in s_lower or 'js' == s_lower or 'vanilla js' in s_lower:
                cleaned_skills.append('JavaScript')
            elif 'react' in s_lower:
                cleaned_skills.append('React')
            elif 'node' in s_lower:
                cleaned_skills.append('Node.js')
            elif 'mongo' in s_lower:
                cleaned_skills.append('MongoDB')
            elif 'express' in s_lower:
                cleaned_skills.append('Express.js')
            elif 'tableau' in s_lower:
                cleaned_skills.append('Tableau')
            elif 'excel' in s_lower:
                cleaned_skills.append('Excel')
            elif 'aws' in s_lower or 'amazon' in s_lower:
                cleaned_skills.append('AWS')
            elif 'azure' in s_lower:
                cleaned_skills.append('Azure')
            elif 'gcp' in s_lower or 'google cloud' in s_lower:
                cleaned_skills.append('GCP')
            elif 'docker' in s_lower:
                cleaned_skills.append('Docker')
            elif 'k8s' in s_lower or 'kubernetes' in s_lower:
                cleaned_skills.append('Kubernetes')
            elif 'c++' in s_lower or 'cpp' in s_lower:
                cleaned_skills.append('C++')
            elif 'c#' in s_lower or '.net' in s_lower or 'c sharp' in s_lower:
                cleaned_skills.append('C#')
            elif 'stat' in s_lower:
                cleaned_skills.append('Statistics')
            elif 'machine learning' in s_lower or 'ml' == s_lower:
                cleaned_skills.append('Machine Learning')
            elif 'tensor' in s_lower or 'tf' == s_lower:
                cleaned_skills.append('TensorFlow')
            elif 'pytorch' in s_lower:
                cleaned_skills.append('PyTorch')
            else:
                cleaned_skills.append(s)
                
        # Remove duplicate skills within the same job
        return ", ".join(sorted(list(set(cleaned_skills))))

    df['skills'] = df['skills'].apply(standardize_skills)
    
    # 4. Standardize Text (e.g. trimming whitespace)
    df['job_title'] = df['job_title'].str.strip()
    
    # Save processed data
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {output_path}. Total records: {len(df)}")

if __name__ == '__main__':
    clean_data('data/raw/jobs_raw.csv', 'data/processed/jobs_cleaned.csv')
