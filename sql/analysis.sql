-- CareerLens: 25+ Analytical SQL Queries

-- =========================================
-- BEGINNER QUERIES
-- =========================================

-- 1. Total jobs posted
SELECT COUNT(*) AS total_jobs FROM fact_jobs;

-- 2. Total companies hiring
SELECT COUNT(*) AS total_companies FROM dim_company;

-- 3. Jobs by location
SELECT l.city, COUNT(j.job_id) AS total_jobs
FROM fact_jobs j
JOIN dim_location l ON j.location_id = l.location_id
GROUP BY l.city
ORDER BY total_jobs DESC;

-- 4. Jobs by role
SELECT r.job_title, COUNT(j.job_id) AS total_jobs
FROM fact_jobs j
JOIN dim_role r ON j.role_id = r.role_id
GROUP BY r.job_title
ORDER BY total_jobs DESC;

-- 5. Average salary (overall)
SELECT ROUND(AVG((salary_min + salary_max) / 2), 2) AS avg_salary_lakhs
FROM fact_jobs
WHERE salary_min IS NOT NULL;

-- 6. Total skills in demand
SELECT COUNT(DISTINCT skill_id) AS distinct_skills
FROM fact_job_skills;

-- =========================================
-- INTERMEDIATE QUERIES
-- =========================================

-- 7. Top 10 companies hiring
SELECT c.company_name, COUNT(j.job_id) AS job_count
FROM fact_jobs j
JOIN dim_company c ON j.company_id = c.company_id
GROUP BY c.company_name
ORDER BY job_count DESC
LIMIT 10;

-- 8. Top 20 skills in demand
SELECT s.skill_name, COUNT(fs.job_id) AS demand_count
FROM fact_job_skills fs
JOIN dim_skill s ON fs.skill_id = s.skill_id
GROUP BY s.skill_name
ORDER BY demand_count DESC
LIMIT 20;

-- 9. Jobs by work mode
SELECT work_mode, COUNT(*) AS job_count,
       ROUND((COUNT(*) * 100.0) / (SELECT COUNT(*) FROM fact_jobs), 2) AS percentage
FROM fact_jobs
GROUP BY work_mode;

-- 10. Remote percentage by role
SELECT r.job_title,
       COUNT(j.job_id) AS total_jobs,
       SUM(CASE WHEN j.work_mode = 'Remote' THEN 1 ELSE 0 END) AS remote_jobs,
       ROUND(SUM(CASE WHEN j.work_mode = 'Remote' THEN 1 ELSE 0 END) * 100.0 / COUNT(j.job_id), 2) AS remote_pct
FROM fact_jobs j
JOIN dim_role r ON j.role_id = r.role_id
GROUP BY r.job_title
ORDER BY remote_pct DESC;

-- 11. Average Salary by location
SELECT l.city, ROUND(AVG((j.salary_min + j.salary_max) / 2), 2) AS avg_salary
FROM fact_jobs j
JOIN dim_location l ON j.location_id = l.location_id
WHERE j.salary_min IS NOT NULL
GROUP BY l.city
ORDER BY avg_salary DESC;

-- 12. Average Salary by role
SELECT r.job_title, ROUND(AVG((j.salary_min + j.salary_max) / 2), 2) AS avg_salary
FROM fact_jobs j
JOIN dim_role r ON j.role_id = r.role_id
WHERE j.salary_min IS NOT NULL
GROUP BY r.job_title
ORDER BY avg_salary DESC;

-- 13. Jobs posted by month
SELECT DATE_TRUNC('month', posted_date) AS month, COUNT(*) AS job_count
FROM fact_jobs
GROUP BY DATE_TRUNC('month', posted_date)
ORDER BY month;

-- =========================================
-- ADVANCED QUERIES
-- =========================================

-- 14. Salary ranking using window functions (Top paying roles per city)
WITH RoleCitySalaries AS (
    SELECT l.city, r.job_title, ROUND(AVG((j.salary_min + j.salary_max) / 2), 2) AS avg_salary
    FROM fact_jobs j
    JOIN dim_location l ON j.location_id = l.location_id
    JOIN dim_role r ON j.role_id = r.role_id
    WHERE j.salary_min IS NOT NULL
    GROUP BY l.city, r.job_title
)
SELECT city, job_title, avg_salary,
       RANK() OVER(PARTITION BY city ORDER BY avg_salary DESC) as rank_in_city
FROM RoleCitySalaries;

-- 15. Top skill per location
WITH LocationSkills AS (
    SELECT l.city, s.skill_name, COUNT(*) as demand_count,
           RANK() OVER(PARTITION BY l.city ORDER BY COUNT(*) DESC) as rnk
    FROM fact_job_skills fs
    JOIN fact_jobs j ON fs.job_id = j.job_id
    JOIN dim_location l ON j.location_id = l.location_id
    JOIN dim_skill s ON fs.skill_id = s.skill_id
    GROUP BY l.city, s.skill_name
)
SELECT city, skill_name, demand_count
FROM LocationSkills
WHERE rnk = 1;

-- 16. Salary quartiles using percentile_cont
SELECT r.job_title,
       percentile_cont(0.25) WITHIN GROUP (ORDER BY (salary_min+salary_max)/2) AS salary_p25,
       percentile_cont(0.50) WITHIN GROUP (ORDER BY (salary_min+salary_max)/2) AS median_salary,
       percentile_cont(0.75) WITHIN GROUP (ORDER BY (salary_min+salary_max)/2) AS salary_p75
FROM fact_jobs j
JOIN dim_role r ON j.role_id = r.role_id
WHERE salary_min IS NOT NULL
GROUP BY r.job_title;

-- 17. Running total of jobs posted over time
SELECT posted_date, COUNT(*) as daily_jobs,
       SUM(COUNT(*)) OVER (ORDER BY posted_date) as running_total
FROM fact_jobs
GROUP BY posted_date;

-- 18. Month-over-month job growth
WITH MonthlyJobs AS (
    SELECT DATE_TRUNC('month', posted_date) AS month, COUNT(*) AS job_count
    FROM fact_jobs
    GROUP BY DATE_TRUNC('month', posted_date)
)
SELECT month, job_count,
       LAG(job_count) OVER (ORDER BY month) AS prev_month_jobs,
       ROUND(((job_count - LAG(job_count) OVER (ORDER BY month)) * 100.0 / NULLIF(LAG(job_count) OVER (ORDER BY month), 0)), 2) AS mom_growth_pct
FROM MonthlyJobs;

-- 19. Two-skill combinations (e.g. SQL + Python)
SELECT s1.skill_name AS skill_1, s2.skill_name AS skill_2, COUNT(*) AS co_occurrence_count
FROM fact_job_skills f1
JOIN fact_job_skills f2 ON f1.job_id = f2.job_id AND f1.skill_id < f2.skill_id
JOIN dim_skill s1 ON f1.skill_id = s1.skill_id
JOIN dim_skill s2 ON f2.skill_id = s2.skill_id
GROUP BY s1.skill_name, s2.skill_name
ORDER BY co_occurrence_count DESC
LIMIT 10;

-- 20. Company salary ranking
SELECT c.company_name, ROUND(AVG((j.salary_min + j.salary_max) / 2), 2) AS avg_salary,
       DENSE_RANK() OVER (ORDER BY AVG((j.salary_min + j.salary_max) / 2) DESC) as company_rank
FROM fact_jobs j
JOIN dim_company c ON j.company_id = c.company_id
WHERE j.salary_min IS NOT NULL
GROUP BY c.company_name;

-- =========================================
-- BUSINESS ANALYTICS QUERIES
-- =========================================

-- 21. Which skills are associated with higher salaries? (Salary Premium)
WITH OverallAvg AS (
    SELECT AVG((salary_min + salary_max) / 2) as baseline_salary FROM fact_jobs
)
SELECT s.skill_name,
       COUNT(j.job_id) as jobs_with_skill,
       ROUND(AVG((j.salary_min + j.salary_max) / 2), 2) AS avg_salary_with_skill,
       ROUND(AVG((j.salary_min + j.salary_max) / 2) - (SELECT baseline_salary FROM OverallAvg), 2) AS salary_premium
FROM fact_job_skills fs
JOIN fact_jobs j ON fs.job_id = j.job_id
JOIN dim_skill s ON fs.skill_id = s.skill_id
WHERE j.salary_min IS NOT NULL
GROUP BY s.skill_name
HAVING COUNT(j.job_id) > 50
ORDER BY salary_premium DESC;

-- 22. Which cities have the best opportunity score? (Score = Demand * Salary * Remote%)
WITH CityMetrics AS (
    SELECT l.city,
           COUNT(j.job_id) AS demand,
           AVG((j.salary_min + j.salary_max) / 2) AS avg_salary,
           SUM(CASE WHEN j.work_mode = 'Remote' THEN 1 ELSE 0 END) * 1.0 / COUNT(j.job_id) AS remote_pct
    FROM fact_jobs j
    JOIN dim_location l ON j.location_id = l.location_id
    GROUP BY l.city
)
SELECT city, demand, ROUND(avg_salary, 2) as avg_salary, ROUND(remote_pct * 100, 2) as remote_pct,
       ROUND((demand / (SELECT MAX(demand) FROM CityMetrics)) *
             (avg_salary / (SELECT MAX(avg_salary) FROM CityMetrics)) *
             (remote_pct / (SELECT MAX(remote_pct) FROM CityMetrics)) * 100, 2) AS opportunity_score
FROM CityMetrics
ORDER BY opportunity_score DESC;

-- 23. Which companies offer high salary + remote work?
SELECT c.company_name,
       COUNT(j.job_id) AS job_count,
       ROUND(AVG((j.salary_min + j.salary_max) / 2), 2) AS avg_salary,
       ROUND(SUM(CASE WHEN j.work_mode = 'Remote' THEN 1 ELSE 0 END) * 100.0 / COUNT(j.job_id), 2) AS remote_pct
FROM fact_jobs j
JOIN dim_company c ON j.company_id = c.company_id
WHERE j.salary_min IS NOT NULL
GROUP BY c.company_name
HAVING AVG((j.salary_min + j.salary_max) / 2) > 8.0 -- Assuming 8.0L is the threshold
   AND (SUM(CASE WHEN j.work_mode = 'Remote' THEN 1 ELSE 0 END) * 100.0 / COUNT(j.job_id)) > 50
ORDER BY avg_salary DESC;

-- 24. Jobs requiring 3 or more skills vs Average Salary
WITH SkillCounts AS (
    SELECT job_id, COUNT(skill_id) AS skill_count
    FROM fact_job_skills
    GROUP BY job_id
)
SELECT CASE WHEN sc.skill_count >= 3 THEN '3+ Skills' ELSE '<3 Skills' END AS skill_requirement,
       COUNT(j.job_id) AS total_jobs,
       ROUND(AVG((j.salary_min + j.salary_max) / 2), 2) AS avg_salary
FROM fact_jobs j
JOIN SkillCounts sc ON j.job_id = sc.job_id
GROUP BY CASE WHEN sc.skill_count >= 3 THEN '3+ Skills' ELSE '<3 Skills' END;

-- 25. Which skill should a candidate learn next? (Top missing skill for Data Analysts in Bengaluru)
-- Example: Candidate has SQL and Excel, but not Python. What are the most demanded skills for a specific slice?
SELECT s.skill_name, COUNT(j.job_id) AS demand_count, ROUND(AVG((j.salary_min+j.salary_max)/2), 2) as avg_salary
FROM fact_job_skills fs
JOIN fact_jobs j ON fs.job_id = j.job_id
JOIN dim_skill s ON fs.skill_id = s.skill_id
JOIN dim_role r ON j.role_id = r.role_id
JOIN dim_location l ON j.location_id = l.location_id
WHERE r.job_title = 'Data Analyst'
  AND l.city = 'Bengaluru'
  AND s.skill_name NOT IN ('SQL', 'Excel') -- Excluding skills the candidate already has
GROUP BY s.skill_name
ORDER BY demand_count DESC
LIMIT 5;

-- 26. Data Quality Monitor: Find Suspicious Postings
SELECT job_id, r.job_title, j.experience, j.salary_string, l.city, c.company_name
FROM fact_jobs j
JOIN dim_role r ON j.role_id = r.role_id
JOIN dim_location l ON j.location_id = l.location_id
JOIN dim_company c ON j.company_id = c.company_id
WHERE j.salary_max > 30 -- E.g. > 30 Lakhs
  AND j.experience LIKE '0-%' -- Fresher
  AND (c.company_name = 'Unknown' OR l.city = 'Unknown');
