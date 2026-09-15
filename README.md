# CareerLens 🚀

**AI-Powered Job Market Intelligence & Career Analytics Platform**

CareerLens is an end-to-end data analytics portfolio project that analyzes real job-market data and provides actionable insights. It tells candidates where the jobs are, what skills employers want, what those skills are worth, and how well the candidate matches the current market.

This project goes beyond generic dashboards by simulating a real SaaS analytics product built across a modern data stack.

## 🎯 What makes CareerLens different?
Instead of a simple "Dataset → Excel → Dashboard" flow, CareerLens implements a robust data pipeline:
`Dataset -> Python/Pandas Pipeline -> PostgreSQL Star Schema -> SQL Analytics -> Power BI -> Candidate Analyzer App`

## 🖥️ Project Components

### 1. Market Intelligence Engine
- **Data Pipeline**: Cleaned and standardized a raw job dataset (5000+ records) using Python (`pandas`), handling missing values, standardizing inconsistent skill names, and removing duplicates.
- **SQL Analytics**: Designed a relational PostgreSQL star schema (`fact_jobs`, `dim_location`, etc.) and wrote 25+ advanced queries (window functions, CTEs) to calculate salary premiums, market demand, and opportunity scores.
- **Power BI Dashboard (Planned)**: A 5-page SaaS-style dashboard for recruiters, tracking KPIs, hiring trends, and skill combinations.

### 2. Candidate Analyzer (App)
A lightweight web interface built with **Streamlit** where candidates can enter their target role, experience, location, and current skills to get:
- **CareerLens Score**: A weighted job match percentage.
- **Skill Gap Analyzer**: Identifies the top missing skills based on actual market demand percentages.
- **Career Roadmap**: A personalized 90-day learning plan focusing on the highest ROI skills.

## 🗃️ Repository Structure

```
CareerLens/
│
├── data/                  # Raw and Processed CSV data
├── notebooks/             # Exploratory Data Analysis (EDA) notebooks
├── src/
│   ├── generate_synthetic_data.py # Data generator
│   ├── data_cleaning.py           # Pandas cleaning pipeline
│   ├── load_to_postgres.py        # SQLAlchemy loader for PostgreSQL
│   └── analytics_engine.py        # Python market & matching logic
│
├── sql/
│   ├── schema.sql         # PostgreSQL Star Schema definition
│   └── analysis.sql       # 25+ analytical queries (Beginner to Advanced)
│
├── dashboard/             # Power BI dashboard files
├── app/
│   └── app.py             # Streamlit Candidate Analyzer UI
│
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

1. **Clone the repository and set up the environment:**
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Generate and Clean Data (Optional, already included in `/data`):**
   ```bash
   python src/generate_synthetic_data.py
   python src/data_cleaning.py
   ```

3. **Run the Candidate Analyzer App:**
   ```bash
   streamlit run app/app.py
   ```

## 🧠 Business Insights Discovered
- **Skill Premium**: Identifying the direct salary premium associated with learning secondary skills (e.g., Python + SQL vs SQL alone).
- **Opportunity Scoring**: Combining Job Demand + Average Salary + Remote Availability into a normalized Opportunity Score for different cities.
- **Data Quality**: Flagging potential data anomalies such as missing salaries or impossible experience requirements using SQL filtering.

## 💼 Skills Demonstrated
- **Python / Pandas**: Data manipulation, ETL, feature engineering.
- **SQL / PostgreSQL**: Data modeling, advanced querying (Joins, CTEs, Window Functions, Rank, Percentiles).
- **Statistics**: Salary distribution, market demand calculations.
- **Product Thinking**: Translating raw data into an interactive, user-facing application (Streamlit).
