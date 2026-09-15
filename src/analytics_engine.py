import pandas as pd
import numpy as np
import re
import os

class CareerLensEngine:
    def __init__(self, data_path=None):
        if data_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_path = os.path.join(base_dir, 'data', 'processed', 'jobs_cleaned.csv')
        self.df = pd.read_csv(data_path)
        self._prepare_data()
        
    def _prepare_data(self):
        # Extract numerical salary min/max for calculations
        def parse_salary(s):
            if pd.isna(s):
                return None
            nums = re.findall(r"[-+]?\d*\.\d+|\d+", s)
            if len(nums) >= 2:
                return (float(nums[0]) + float(nums[1])) / 2
            elif len(nums) == 1:
                return float(nums[0])
            return None
            
        self.df['avg_salary_lakhs'] = self.df['salary'].apply(parse_salary)
        
        # Build skills corpus
        self.all_skills = set()
        for skills_str in self.df['skills'].dropna():
            for s in skills_str.split(','):
                if s.strip():
                    self.all_skills.add(s.strip())
        self.all_skills = sorted(list(self.all_skills))
        
    def get_roles(self):
        return sorted(self.df['job_title'].dropna().unique().tolist())
        
    def get_locations(self):
        return sorted(self.df['location'].dropna().unique().tolist())
        
    def get_all_skills(self):
        return self.all_skills
        
    def analyze_market_demand(self, target_role, location=None):
        """Analyzes market demand for skills for a specific role/location."""
        mask = self.df['job_title'] == target_role
        if location and location != 'All':
            mask &= (self.df['location'] == location)
            
        role_df = self.df[mask]
        total_jobs = len(role_df)
        
        if total_jobs == 0:
            return pd.DataFrame()
            
        skill_counts = {}
        skill_salaries = {}
        
        for _, row in role_df.iterrows():
            if pd.isna(row['skills']):
                continue
            skills = [s.strip() for s in row['skills'].split(',')]
            for s in skills:
                skill_counts[s] = skill_counts.get(s, 0) + 1
                if pd.notna(row['avg_salary_lakhs']):
                    if s not in skill_salaries:
                        skill_salaries[s] = []
                    skill_salaries[s].append(row['avg_salary_lakhs'])
                    
        stats = []
        for s in skill_counts:
            demand_pct = (skill_counts[s] / total_jobs) * 100
            avg_sal = np.mean(skill_salaries[s]) if s in skill_salaries else None
            stats.append({
                'Skill': s,
                'Demand (%)': demand_pct,
                'Avg Salary (Lakhs)': avg_sal,
                'Job Count': skill_counts[s]
            })
            
        if not stats:
            return pd.DataFrame(columns=['Skill', 'Demand (%)', 'Avg Salary (Lakhs)', 'Job Count'])
            
        stats_df = pd.DataFrame(stats).sort_values('Demand (%)', ascending=False)
        return stats_df
        
    def analyze_candidate(self, target_role, location, candidate_skills):
        """Returns Job Match Score and Skill Gap Analysis"""
        market_stats = self.analyze_market_demand(target_role, location)
        
        if market_stats.empty:
            return None, None
            
        # Calculate Match Score
        # Weight top 5 skills heavily
        top_skills = market_stats.head(10)
        
        score_earned = 0
        total_possible = 0
        
        for _, row in top_skills.iterrows():
            weight = row['Demand (%)'] / 100.0
            total_possible += weight
            if row['Skill'] in candidate_skills:
                score_earned += weight
                
        job_match_score = (score_earned / total_possible) * 100 if total_possible > 0 else 0
        
        # Skill Gap Analysis
        missing_skills = market_stats[~market_stats['Skill'].isin(candidate_skills)].copy()
        
        return {
            'match_score': round(job_match_score, 1),
            'market_avg_salary': round(self.df[self.df['job_title'] == target_role]['avg_salary_lakhs'].mean(), 2),
            'total_jobs_analyzed': len(self.df[(self.df['job_title'] == target_role) & (self.df['location'] == location) if location != 'All' else (self.df['job_title'] == target_role)])
        }, missing_skills
