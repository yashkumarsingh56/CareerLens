# CareerLens: Interview Preparation Guide

This guide contains talking points and Q&A to help you confidently discuss the CareerLens project during Data Analyst interviews.

## 🎤 The "Tell me about a project you've worked on" Pitch

**Don't start with technology. Start with the problem:**
> "I noticed that job seekers often don't know which skills are actually in demand, which locations have better opportunities, or how their current skill set compares with the market. So I built CareerLens, an analytics platform that uses job-market data to answer those questions."

**Explain the process:**
> "I collected and cleaned the data using Python and Pandas to handle missing values and standardize text. I then stored the structured data in a PostgreSQL star schema, performed analytical queries using SQL (including window functions and CTEs), and planned an interactive Power BI dashboard."

**Highlight the differentiator:**
> "The unique part of the project is the Candidate Analyzer component I built using Streamlit. It compares a candidate's specific skills against market demand and identifies their highest-ROI skill gaps. The main objective wasn't just visualization—I wanted the project to convert raw job postings into actionable career insights."

---

## 🧠 Anticipated Interview Questions

### 1. Data Cleaning & Preparation
**Q: What were the biggest challenges with the raw data and how did you clean it?**
A: "The biggest challenge was standardizing text inputs, particularly skills. A single skill like 'Power BI' was entered as 'PowerBI', 'power bi', or 'POWER BI'. I wrote a Python script using pandas and regex to normalize these values, handled missing values by keeping them as 'Unknown' to preserve other valid data points (like location and salary), and removed duplicate postings."

### 2. SQL & Database Design
**Q: How did you model the data in PostgreSQL?**
A: "I used a Star Schema. I created a central `fact_jobs` table containing metrics like salary and experience, and a `fact_job_skills` bridge table. These connected to dimension tables for Location, Company, Role, and Skill. This made aggregations much faster and more intuitive for analytical queries."

**Q: Tell me about a complex SQL query you wrote for this.**
A: "I wrote a query to calculate the 'Opportunity Score' for different cities. I used a CTE to aggregate total demand, average salary, and remote work percentage per city. Then, I normalized these metrics and combined them into a single score. I also used Window Functions like `DENSE_RANK()` to find the highest paying roles per city."

### 3. Business Analytics & Logic
**Q: How did you calculate the 'Skill Premium'?**
A: "I wanted to find out which skills are associated with higher salaries. I calculated the overall baseline average salary, and then calculated the average salary of jobs requiring a specific skill. The difference between the two is what I called the 'Salary Premium'. I made sure to frame it as an 'association' rather than causation to maintain analytical rigor."

### 4. Product Thinking (Candidate Analyzer)
**Q: How does your Job Match engine work?**
A: "It doesn't just do a simple count of matching skills. It extracts the market demand percentage for each skill required for a specific role and location. It then assigns a higher weight to the most demanded skills. If a candidate has the highly demanded skills, their match score is significantly higher than if they only match on nice-to-have skills."

### 5. Data Quality
**Q: How did you handle data quality issues in your dashboard?**
A: "Instead of just ignoring bad data, I built a Data Quality Monitor. I used SQL to flag suspicious postings—for example, jobs requiring 0 experience but offering an outlier salary of 50 Lakhs, or postings missing critical information like location. This demonstrates that I understand analytics starts with reliable data."
