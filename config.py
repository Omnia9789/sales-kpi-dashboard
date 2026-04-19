"""
config.py — Central configuration for paths, thresholds, and settings.
"""

import os

# ── Base directory (project root) ────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Data paths ────────────────────────────────────────────────────────────────
DATA_RAW_DIR       = os.path.join(BASE_DIR, "data", "raw")
DATA_PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

RAW_CSV      = os.path.join(DATA_RAW_DIR,       "superstore.csv")
CLEAN_CSV    = os.path.join(DATA_PROCESSED_DIR, "superstore_clean.csv")

# ── Database ──────────────────────────────────────────────────────────────────
DB_PATH = os.path.join(BASE_DIR, "data", "superstore.db")

# ── SQL ───────────────────────────────────────────────────────────────────────
SQL_DIR     = os.path.join(BASE_DIR, "sql")
QUERIES_DIR = os.path.join(SQL_DIR, "queries")

# ── Reports ───────────────────────────────────────────────────────────────────
REPORTS_OUTPUT_DIR = os.path.join(BASE_DIR, "reports", "output")

# ── Analysis thresholds ───────────────────────────────────────────────────────
# Month-over-month revenue drop that triggers an alert flag
MOM_DROP_THRESHOLD = 0.10   # 10 %

# Top-N products / customers to surface in reports
TOP_N = 10

# ── Dashboard ─────────────────────────────────────────────────────────────────
DASHBOARD_TITLE   = "Sales KPI Dashboard"
DASHBOARD_FAVICON = "📊"
