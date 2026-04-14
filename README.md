# Sales KPI Dashboard & Automated Reporting

> A full data analysis project that cleans, analyzes, and visualizes retail sales data — with an automated Python reporting engine that generates Excel summaries and a Streamlit/Power BI dashboard for KPI tracking.

---

## Overview

This project covers the complete data analyst workflow: data cleaning with Python, SQL-based extraction and analysis, interactive dashboard creation, and automated Excel report generation. Built on the [Superstore Sales dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final), it demonstrates the tools and thinking expected in a data analysis internship.

**Built to showcase:** SQL analytics, dashboard design (Power BI / Streamlit), automated reporting, trend detection, data cleaning, documentation, and business communication of findings.

---

## Key Features

- **Data Cleaning** — Handles missing values, type casting, outlier detection, and schema normalization
- **SQL Analytics** — 8 business-focused queries covering revenue, growth, rankings, and variance
- **KPI Dashboard** — Interactive Streamlit dashboard (or Power BI `.pbix` file) with filters and charts
- **Trend Detection** — Python logic that flags month-over-month revenue drops greater than 10%
- **Automated Reports** — `report_generator.py` produces a formatted Excel report on every run
- **Business Findings** — Documented insights with supporting data in the README

---

## Project Structure

```
sales-kpi-dashboard/
│
├── data/
│   ├── raw/
│   │   └── superstore.csv          # Original dataset (from Kaggle)
│   └── processed/
│       └── superstore_clean.csv    # Cleaned dataset
│
├── notebooks/
│   └── 01_eda.ipynb                # Exploratory Data Analysis
│
├── sql/
│   ├── schema.sql                  # Table creation script
│   ├── load_data.sql               # Data loading script
│   └── queries/
│       ├── 01_revenue_by_region.sql
│       ├── 02_monthly_growth.sql
│       ├── 03_top_products.sql
│       ├── 04_category_breakdown.sql
│       ├── 05_customer_segments.sql
│       ├── 06_profit_margin.sql
│       ├── 07_shipping_analysis.sql
│       └── 08_anomaly_detection.sql
│
├── analysis/
│   ├── __init__.py
│   ├── clean.py                    # Data cleaning pipeline
│   ├── sql_runner.py               # Execute SQL queries via Python
│   └── trend_detector.py           # MoM variance flagging logic
│
├── dashboard/
│   ├── app.py                      # Streamlit dashboard
│   └── sales_dashboard.pbix        # Power BI file (alternative)
│
├── reports/
│   ├── report_generator.py         # Auto-generates Excel report
│   └── output/                     # Generated .xlsx reports land here
│
├── assets/
│   └── dashboard_screenshot.png    # Screenshot for README
│
├── config.py                       # Paths, thresholds, settings
├── main.py                         # Run full pipeline end-to-end
├── requirements.txt
└── README.md
```

---

## Tech Stack

| Purpose | Tool |
|---|---|
| Language | Python 3.10+ |
| Data Cleaning | `pandas`, `numpy` |
| Database | SQLite + `SQLAlchemy` |
| SQL Analytics | Raw SQL via `sqlite3` / `pandas.read_sql` |
| Dashboard | Streamlit (or Power BI Desktop) |
| Charts | `plotly`, `matplotlib` |
| Excel Reports | `openpyxl` |
| Version Control | Git & GitHub |

---

## Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/sales-kpi-dashboard.git
cd sales-kpi-dashboard
```

### 2. Download the dataset
Download `Superstore.csv` from [Kaggle](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final) and place it in `data/raw/`.

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the full pipeline
```bash
python main.py
```

### 5. Launch the dashboard
```bash
streamlit run dashboard/app.py
```

### 6. Generate an Excel report
```bash
python reports/report_generator.py
```

---

## SQL Queries

| # | Query | Description |
|---|---|---|
| 01 | Revenue by Region | Total and average sales per region |
| 02 | Monthly Growth | Month-over-month revenue with % change |
| 03 | Top Products | Top 10 products by revenue and profit |
| 04 | Category Breakdown | Sales and profit margin per category |
| 05 | Customer Segments | Revenue and order count by customer segment |
| 06 | Profit Margin | Profit margin % ranked by sub-category |
| 07 | Shipping Analysis | Average shipping delay by ship mode |
| 08 | Anomaly Detection | Months where profit dropped > 10% MoM |

---

## Dashboard KPIs

The Streamlit dashboard includes:

- **Total Revenue**, **Total Profit**, **Profit Margin %**, **Total Orders** — metric cards at the top
- **Revenue Over Time** — line chart with monthly granularity
- **Revenue by Region** — bar chart with color-coded comparison
- **Top 10 Products** — horizontal bar chart
- **Category Breakdown** — grouped bar chart (sales vs. profit)
- **Trend Alerts** — table of flagged months with anomalous MoM drops

**Filters available:** Date range, Region, Category, Customer Segment

---

## Automated Excel Report

`reports/report_generator.py` produces a formatted `.xlsx` file on every run with:
- Summary KPI sheet (Revenue, Profit, Orders, Margin)
- Monthly trend sheet with a built-in chart
- Top products sheet
- Anomaly flags sheet

Output saved to `reports/output/sales_report_YYYY-MM-DD.xlsx`

---

## Key Findings

> *(Update with real insights from your first run)*

- The **West region** generated the highest total revenue, accounting for ~32% of overall sales
- **Q4** consistently outperformed other quarters — November was the strongest single month
- **Technology** had the highest profit margin at ~18%, while **Furniture** ran near breakeven
- MoM revenue drops greater than 10% were detected in **3 months**, all following major holiday periods
- **Standard Class** shipping accounted for 60% of orders but had the longest average delay (5.3 days)

---

## Requirements

```
pandas
numpy
sqlalchemy
streamlit
plotly
matplotlib
openpyxl
```

---

## Author

**Omnia Ali Mohamed Ali**
Data Analysis & AI | Cairo University, CS (AI Major)
[GitHub](https://github.com/YOUR_USERNAME) · [LinkedIn](https://linkedin.com/in/YOUR_PROFILE) · [Portfolio](YOUR_PORTFOLIO)
