"""
analysis/sql_runner.py — Load cleaned data into SQLite and execute SQL queries.

Usage:
    python -m analysis.sql_runner                  # run all queries
    python -m analysis.sql_runner 03_top_products  # run one query by name
"""

import os
import sys
import sqlite3
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import CLEAN_CSV, DB_PATH, QUERIES_DIR


# ── Database setup ────────────────────────────────────────────────────────────

def get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return sqlite3.connect(db_path)


def load_to_sqlite(csv_path: str = CLEAN_CSV, db_path: str = DB_PATH) -> None:
    """Write the cleaned CSV into an SQLite table called `sales`."""
    print(f"[sql_runner] Loading '{csv_path}' → SQLite table 'sales' in '{db_path}'")
    df = pd.read_csv(csv_path, low_memory=False)
    conn = get_connection(db_path)
    df.to_sql("sales", conn, if_exists="replace", index=False)
    conn.close()
    print(f"  Loaded {len(df):,} rows.\n")


# ── Query runner ──────────────────────────────────────────────────────────────

def run_query_file(sql_file: str, db_path: str = DB_PATH) -> pd.DataFrame:
    """Execute a .sql file and return results as a DataFrame."""
    with open(sql_file, "r") as f:
        sql = f.read()
    conn = get_connection(db_path)
    try:
        df = pd.read_sql_query(sql, conn)
    finally:
        conn.close()
    return df


def run_all_queries(queries_dir: str = QUERIES_DIR, db_path: str = DB_PATH) -> dict[str, pd.DataFrame]:
    """Run every .sql file in queries_dir and return {name: DataFrame}."""
    results = {}
    sql_files = sorted(f for f in os.listdir(queries_dir) if f.endswith(".sql"))
    for fname in sql_files:
        path = os.path.join(queries_dir, fname)
        name = fname.replace(".sql", "")
        print(f"  [sql_runner] Running {fname} …", end=" ")
        try:
            df = run_query_file(path, db_path)
            results[name] = df
            print(f"{len(df)} rows")
        except Exception as exc:
            print(f"ERROR — {exc}")
            results[name] = pd.DataFrame()
    return results


# ── CLI entry point ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        load_to_sqlite()

    if len(sys.argv) > 1:
        query_name = sys.argv[1]
        if not query_name.endswith(".sql"):
            query_name += ".sql"
        sql_file = os.path.join(QUERIES_DIR, query_name)
        if not os.path.exists(sql_file):
            print(f"Query file not found: {sql_file}")
            sys.exit(1)
        df = run_query_file(sql_file)
        print(df.to_string(index=False))
    else:
        load_to_sqlite()
        results = run_all_queries()
        for name, df in results.items():
            print(f"\n── {name} ──")
            print(df.to_string(index=False))
