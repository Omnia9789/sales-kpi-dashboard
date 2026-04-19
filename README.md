# Sales KPI Dashboard & Automated Reporting

> A full data analysis project that cleans, analyzes, and visualizes retail sales data — with an automated Python reporting engine that generates Excel summaries and an interactive Streamlit dashboard for KPI tracking.

---

## Overview

This project covers the complete data analyst workflow: data cleaning with Python, SQL-based extraction and analysis, interactive dashboard creation, and automated Excel report generation. Built on the [Superstore Sales dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final), it demonstrates the tools and thinking expected in a data analysis internship.

**Built to showcase:** SQL analytics, dashboard design (Streamlit), automated reporting, trend detection, data cleaning, documentation, and business communication of findings.

---

## Key Features

- **Data Cleaning** — Handles missing values, type casting, outlier detection (IQR ×3), and derived column generation
- **SQL Analytics** — 8 business-focused queries covering revenue, growth, rankings, anomalies, and variance
- **KPI Dashboard** — Interactive Streamlit dashboard with sidebar filters, tabbed views, and Plotly charts
- **Trend Detection** — Python logic that flags month-over-month revenue drops greater than 10%
- **Automated Reports** — `report_generator.py` produces a fully-formatted multi-sheet Excel report on every run
- **Business Findings** — Documented insights with supporting data

---

## Dashboard Preview

> 📸 **Screenshot goes here** — see [Screenshots to Take](#screenshots-to-take) section below.

![Dashboard Overview](assets/dashboard_screenshot.png)

---

## Project Structure

```
sales-kpi-dashboard/
│
├── data/
│   ├── raw/
│   │   └── superstore.csv          # Original dataset (from Kaggle)
│   └── processed/
│       └── superstore_clean.csv    # Cleaned dataset (auto-generated)
│
├── notebooks/
│   └── 01_eda.ipynb                # Exploratory Data Analysis
│
├── sql/
│   ├── schema.sql                  # Table definition reference
│   ├── load_data.sql               # CLI data-loading reference
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
│   └── trend_detector.py          # MoM variance flagging logic
│
├── dashboard/
│   └── app.py                      # Streamlit dashboard
│
├── reports/
│   ├── report_generator.py         # Auto-generates Excel report
│   └── output/                     # Generated .xlsx reports land here
│
├── assets/
│   └── dashboard_screenshot.png   # Screenshot for README
│
├── config.py                       # Paths, thresholds, settings
├── main.py                         # Run full pipeline end-to-end
├── requirements.txt
└── README.md
```

---

## Tech Stack

| Purpose        | Tool                                      |
|----------------|-------------------------------------------|
| Language       | Python 3.10+                              |
| Data Cleaning  | `pandas`, `numpy`                         |
| Database       | SQLite + `sqlalchemy`                     |
| SQL Analytics  | Raw SQL via `sqlite3` / `pandas.read_sql` |
| Dashboard      | Streamlit                                 |
| Charts         | `plotly`, `matplotlib`, `seaborn`         |
| Excel Reports  | `openpyxl`                                |
| Version Control| Git & GitHub                              |

---

## Getting Started

### Prerequisites

- **Python 3.10+** — [python.org](https://www.python.org/downloads/)
- **VS Code** (recommended) — [code.visualstudio.com](https://code.visualstudio.com/)
- **Git** — [git-scm.com](https://git-scm.com/)

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/sales-kpi-dashboard.git
cd sales-kpi-dashboard
```

### 2. Create a virtual environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

> **VS Code tip:** Press `Ctrl+Shift+P` → *Python: Select Interpreter* → choose the `.venv` interpreter.  
> The terminal will show `(.venv)` in the prompt when active.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download the dataset

1. Go to [Kaggle — Superstore Dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)
2. Download `Sample - Superstore.csv`
3. Rename it to `superstore.csv`
4. Place it at `data/raw/superstore.csv`

### 5. Run the full pipeline

```bash
python main.py
```

This will:
1. Clean the raw CSV → `data/processed/superstore_clean.csv`
2. Load data into SQLite → `data/superstore.db`
3. Execute all 8 SQL KPI queries
4. Detect month-over-month revenue drops
5. Generate a timestamped Excel report → `reports/output/`

### 6. Launch the dashboard

```bash
streamlit run dashboard/app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Usage — Individual Modules

### Data cleaning only
```bash
python -m analysis.clean
```

### SQL queries only
```bash
# Run all queries
python -m analysis.sql_runner

# Run a specific query
python -m analysis.sql_runner 03_top_products
```

### Trend detection only
```bash
python -m analysis.trend_detector
```

### Generate Excel report only
```bash
python reports/report_generator.py
```

### EDA Notebook
```bash
jupyter notebook notebooks/01_eda.ipynb
```

---

## SQL KPI Queries

| File | Description |
|------|-------------|
| `01_revenue_by_region.sql` | Total revenue, profit, and margin by region |
| `02_monthly_growth.sql` | Month-over-month growth rate (with LAG window function) |
| `03_top_products.sql` | Top 10 products by revenue |
| `04_category_breakdown.sql` | Revenue and margin by category/sub-category |
| `05_customer_segments.sql` | Order count, revenue, and AOV by segment |
| `06_profit_margin.sql` | Loss-making products (negative margin) |
| `07_shipping_analysis.sql` | Revenue and average days-to-ship by shipping mode |
| `08_anomaly_detection.sql` | Orders with discount ≥ 40% AND negative profit |

---

## Business Findings

| # | Finding | Source |
|---|---------|--------|
| 1 | **West** generates the highest revenue; **Central** has the best profit margin | `01_revenue_by_region.sql` |
| 2 | **Technology** is the most profitable category; **Furniture** produces losses in several sub-categories | `04_category_breakdown.sql` |
| 3 | High discounts (≥ 40%) consistently drive **negative profit** — a clear pricing risk | `08_anomaly_detection.sql` |
| 4 | **Consumer** segment accounts for ~50% of all orders but has the lowest average order value | `05_customer_segments.sql` |
| 5 | Revenue has a strong **Q4 seasonal peak** each year, with notable MoM drops in January | Monthly trend detector |
| 6 | **Standard Class** shipping carries the majority of revenue; **Same Day** is high-cost, low-volume | `07_shipping_analysis.sql` |

---

## Configuration

All adjustable settings live in `config.py`:

| Setting | Default | Description |
|---------|---------|-------------|
| `MOM_DROP_THRESHOLD` | `0.10` | % drop that triggers a trend alert |
| `TOP_N` | `10` | Number of top products/customers in reports |
| `DB_PATH` | `data/superstore.db` | SQLite database location |
| `REPORTS_OUTPUT_DIR` | `reports/output/` | Where Excel files are saved |

---

## Screenshots to Take

After running the project, capture these screenshots and place them in the `assets/` folder:

| Screenshot | Filename | What to capture |
|------------|----------|-----------------|
| **Dashboard Overview** | `dashboard_screenshot.png` | Full browser window of the Streamlit app showing KPI cards + trend chart |
| **Trend Tab** | `trend_chart.png` | Monthly Revenue Trend chart with red-marked drop months highlighted |
| **Region Chart** | `region_chart.png` | Grouped bar chart of Revenue vs Profit by Region |
| **Category Treemap** | `category_treemap.png` | The treemap showing category/sub-category revenue breakdown |
| **Top Products** | `top_products.png` | Horizontal bar chart of the Top 10 products |
| **Excel Report** | `excel_report.png` | Excel open at the Executive Summary sheet showing KPI cards |
| **Terminal Pipeline** | `pipeline_run.png` | VS Code terminal showing `python main.py` running all 5 steps |
| **SQL Query Result** | `sql_query.png` | VS Code or terminal showing a SQL query output (e.g. revenue by region) |

> **Tip:** Use **Windows Snipping Tool** (`Win+Shift+S`) or **Lightshot** for clean screenshots.  
> Aim for 1200–1600 px wide. Crop to remove any personal info from your browser/taskbar.

---

## Roadmap

- [ ] Add Power BI `.pbix` file as alternative dashboard
- [ ] Dockerize for one-command deployment
- [ ] Add pytest unit tests for `clean.py` and `trend_detector.py`
- [ ] Schedule report auto-generation via GitHub Actions

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Author

**Omnia** — [GitHub @Omnia9789](https://github.com/Omnia9789)

*Built as a data analysis portfolio project showcasing SQL, Python, Streamlit, and automated Excel reporting.*
