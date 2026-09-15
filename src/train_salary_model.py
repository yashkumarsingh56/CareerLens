import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import os
import re

def extract_avg_salary(salary_str):
    if pd.isna(salary_str):
        return np.nan
    
    # Expected format: ₹5.6L - ₹8.2L
    matches = re.findall(r'₹([\d\.]+)L', str(salary_str))
    if len(matches) == 2:
        return (float(matches[0]) + float(matches[1])) / 2.0
    elif len(matches) == 1:
        return float(matches[0])
    return np.nan

def train_model():
    print("Loading synthetic data...")
    df_synthetic = pd.read_csv('data/processed/jobs_cleaned.csv')
    
    print("Loading real-world data...")
    try:
        df_real = pd.read_csv('data/processed/jobs_real_cleaned.csv')
        df = pd.concat([df_synthetic, df_real], ignore_index=True)
        print(f"Combined dataset: {len(df_synthetic)} synthetic + {len(df_real)} real = {len(df)} total jobs")
    except Exception as e:
        print(f"Could not load real data ({e}), using only synthetic data.")
        df = df_synthetic
        
    print("Preparing features...")
    # Extract numeric target
    df['avg_salary_lakhs'] = df['salary'].apply(extract_avg_salary)
    
    # Drop rows without salary for training
    df = df.dropna(subset=['avg_salary_lakhs'])
    print(f"Jobs with valid salaries for training: {len(df)}")
    
    # Simple feature engineering for experience
    def parse_exp(exp_str):
        if pd.isna(exp_str): return 0
        matches = re.findall(r'(\d+)', str(exp_str))
        if matches:
            return float(matches[0]) # take the min experience
        return 0
        
    df['min_exp_years'] = df['experience'].apply(parse_exp)
    
    # Select features
    X = df[['job_title', 'location', 'work_mode', 'min_exp_years']]
    y = df['avg_salary_lakhs']
    
    # Preprocessing
    categorical_features = ['job_title', 'location', 'work_mode']
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', categorical_transformer, categorical_features)
        ],
        remainder='passthrough'
    )
    
    # Pipeline
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])
    
    print("Training Random Forest model...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model.fit(X_train, y_train)
    
    score = model.score(X_test, y_test)
    print(f"Model R^2 Score on Test Set: {score:.4f}")
    
    # Save model
    os.makedirs('models', exist_ok=True)
    model_path = 'models/salary_predictor.joblib'
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

if __name__ == '__main__':
    train_model()
