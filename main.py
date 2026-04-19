"""
main.py — Run the full Sales KPI pipeline end-to-end.

Steps:
    1. Clean raw CSV  → data/processed/superstore_clean.csv
    2. Load to SQLite → data/superstore.db
    3. Run SQL KPI queries
    4. Detect MoM revenue drops
    5. Generate Excel report → reports/output/

Usage:
    python main.py
    python main.py --skip-report      # skip Excel generation
    python main.py --report-only      # skip cleaning & SQL, just make report
"""

import argparse
import os
import sys


def parse_args():
    parser = argparse.ArgumentParser(description="Sales KPI Dashboard Pipeline")
    parser.add_argument("--skip-report",  action="store_true",
                        help="Skip Excel report generation")
    parser.add_argument("--report-only",  action="store_true",
                        help="Only generate the Excel report (skip data prep)")
    return parser.parse_args()


def main():
    args = parse_args()

    # ── Step 1: Data cleaning ─────────────────────────────────────────────────
    if not args.report_only:
        print("=" * 60)
        print("STEP 1 — Data Cleaning")
        print("=" * 60)
        from analysis.clean import clean_data
        from config import RAW_CSV, CLEAN_CSV

        if not os.path.exists(RAW_CSV):
            print(
                f"\n⚠️  Raw data not found at: {RAW_CSV}\n"
                "   Please download the Superstore dataset from Kaggle:\n"
                "   https://www.kaggle.com/datasets/vivek468/superstore-dataset-final\n"
                "   and save it as  data/raw/superstore.csv\n"
            )
            sys.exit(1)

        clean_data(RAW_CSV, CLEAN_CSV)

    # ── Step 2 & 3: SQLite load + queries ────────────────────────────────────
    if not args.report_only:
        print("=" * 60)
        print("STEP 2 — Load to SQLite")
        print("=" * 60)
        from analysis.sql_runner import load_to_sqlite, run_all_queries
        from config import CLEAN_CSV, DB_PATH

        load_to_sqlite(CLEAN_CSV, DB_PATH)

        print("=" * 60)
        print("STEP 3 — Run SQL KPI Queries")
        print("=" * 60)
        results = run_all_queries()
        for name, df in results.items():
            print(f"\n── {name} ──")
            print(df.head(5).to_string(index=False))
            print(f"   … {len(df)} rows total")

    # ── Step 4: Trend detection ───────────────────────────────────────────────
    if not args.report_only:
        print("=" * 60)
        print("STEP 4 — Month-over-Month Trend Detection")
        print("=" * 60)
        from analysis.trend_detector import run as detect_trends
        detect_trends()

    # ── Step 5: Report generation ─────────────────────────────────────────────
    if not args.skip_report:
        print("=" * 60)
        print("STEP 5 — Generate Excel Report")
        print("=" * 60)
        from reports.report_generator import generate_report
        report_path = generate_report()
        print(f"✅ Report → {report_path}")

    print("\n✅ Pipeline complete.")
    print("   To launch the dashboard:  streamlit run dashboard/app.py\n")


if __name__ == "__main__":
    main()
