# CareerLens: SQL Analysis Blueprint (Phase 1)

Here are the 25 SQL questions designed to analyze the job market data. Once your data is loaded into a database (e.g., MySQL or PostgreSQL), you can use these to build your portfolio.

## Basic Data Exploration
1. Retrieve all job postings for a 'Data Analyst' role.
2. Count the total number of jobs available in 'Bangalore'.
3. Find the minimum, maximum, and average 'min_salary_lpa' across all jobs.
4. List the top 5 companies with the most job postings.
5. How many jobs offer a 'Remote' work type?

## Salary Intelligence
6. Find the average 'max_salary_lpa' for 'Fresher' roles.
7. Compare the average salary of 'Data Analyst' vs 'Data Scientist'.
8. Which location offers the highest average salary for Data Analysts?
9. Show the top 10 highest-paying job postings (based on max salary).
10. Does a 'Hybrid' work type pay more on average than an 'Onsite' work type?

## Skills Intelligence (Advanced String Manipulation)
11. Count how many jobs require 'SQL' as a skill.
12. Find the percentage of jobs that require both 'Excel' AND 'SQL'.
13. Which skill is the most demanded for '1-3 years' experience?
14. Calculate the average salary difference between jobs that require 'Python' vs those that don't.
15. List the jobs that require 'Power BI' but do NOT require 'Tableau'.

## Trend & Company Analysis
16. Which companies are hiring the most 'Freshers'?
17. Find the number of jobs posted in the last 30 days.
18. Rank the locations based on the number of job openings using Window Functions.
19. Identify companies that pay above the overall market average salary.
20. Categorize companies into 'High Paying' (avg max salary > 15), 'Medium' (10-15), and 'Standard' (<10).

## Complex/Advanced Queries
21. Find the 2nd highest paying Data Analyst job in 'Delhi NCR'.
22. Use a CTE to find companies that have job postings in more than 3 different locations.
23. Calculate the running total of job postings by date.
24. Find the skill combination that yields the highest average salary.
25. Create a pivot-like summary showing the number of jobs per role for each location.
