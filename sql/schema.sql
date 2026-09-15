-- CareerLens PostgreSQL Schema Design
-- Star Schema Approach for Analytical Workload

-- 1. Locations Dimension
CREATE TABLE dim_location (
    location_id SERIAL PRIMARY KEY,
    city VARCHAR(100) UNIQUE NOT NULL
);

-- 2. Companies Dimension
CREATE TABLE dim_company (
    company_id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) UNIQUE NOT NULL
);

-- 3. Roles Dimension (Optional, but good for aggregation)
CREATE TABLE dim_role (
    role_id SERIAL PRIMARY KEY,
    job_title VARCHAR(255) UNIQUE NOT NULL
);

-- 4. Skills Dimension
CREATE TABLE dim_skill (
    skill_id SERIAL PRIMARY KEY,
    skill_name VARCHAR(100) UNIQUE NOT NULL
);

-- 5. Fact Table: Jobs
CREATE TABLE fact_jobs (
    job_id VARCHAR(50) PRIMARY KEY,
    role_id INT REFERENCES dim_role(role_id),
    company_id INT REFERENCES dim_company(company_id),
    location_id INT REFERENCES dim_location(location_id),
    experience VARCHAR(50),
    salary_string VARCHAR(100),
    salary_min NUMERIC,
    salary_max NUMERIC,
    work_mode VARCHAR(50),
    employment_type VARCHAR(50),
    posted_date DATE
);

-- 6. Fact Table: Job Skills (Many-to-Many bridge)
CREATE TABLE fact_job_skills (
    job_id VARCHAR(50) REFERENCES fact_jobs(job_id),
    skill_id INT REFERENCES dim_skill(skill_id),
    PRIMARY KEY (job_id, skill_id)
);
