"""
analysis/clean.py — Data cleaning pipeline for the Superstore dataset.

Run directly:
    python -m analysis.clean
"""

import pandas as pd
import numpy as np
import os
import sys

# Allow running as a script from the project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import RAW_CSV, CLEAN_CSV, DATA_PROCESSED_DIR


# ── Column name normalizer ─────────────────────────────────────────────────────
def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Strip whitespace and lower-snake-case all column names."""
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(r"[\s\-/]+", "_", regex=True)
        .str.replace(r"[^a-z0-9_]", "", regex=True)
    )
    return df


# ── Date parser ───────────────────────────────────────────────────────────────
def _parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    for col in ["order_date", "ship_date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], infer_datetime_format=True, errors="coerce")
    return df


# ── Duplicate remover ─────────────────────────────────────────────────────────
def _remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates()
    removed = before - len(df)
    if removed:
        print(f"  [clean] Removed {removed} duplicate rows.")
    return df


# ── Missing-value handler ─────────────────────────────────────────────────────
def _handle_missing(df: pd.DataFrame) -> pd.DataFrame:
    # Postal code — fill with '00000' (non-critical for analysis)
    if "postal_code" in df.columns:
        df["postal_code"] = df["postal_code"].fillna("00000").astype(str)

    # Numeric columns — fill with median
    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        n_missing = df[col].isna().sum()
        if n_missing:
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            print(f"  [clean] Filled {n_missing} missing values in '{col}' with median ({median_val:.2f}).")

    # Categorical — fill with 'Unknown'
    cat_cols = df.select_dtypes(include=["object"]).columns
    for col in cat_cols:
        n_missing = df[col].isna().sum()
        if n_missing:
            df[col] = df[col].fillna("Unknown")
            print(f"  [clean] Filled {n_missing} missing values in '{col}' with 'Unknown'.")

    return df


# ── Type casting ──────────────────────────────────────────────────────────────
def _cast_types(df: pd.DataFrame) -> pd.DataFrame:
    for col in ["sales", "profit", "discount", "quantity"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


# ── Derived columns ───────────────────────────────────────────────────────────
def _add_derived(df: pd.DataFrame) -> pd.DataFrame:
    if "order_date" in df.columns:
        df["order_year"]  = df["order_date"].dt.year
        df["order_month"] = df["order_date"].dt.month
        df["order_yearmonth"] = df["order_date"].dt.to_period("M").astype(str)

    if "sales" in df.columns and "profit" in df.columns:
        df["profit_margin"] = np.where(
            df["sales"] != 0,
            (df["profit"] / df["sales"]) * 100,
            0.0,
        ).round(2)

    return df


# ── Outlier detection (IQR) ───────────────────────────────────────────────────
def _flag_outliers(df: pd.DataFrame) -> pd.DataFrame:
    for col in ["sales", "profit"]:
        if col not in df.columns:
            continue
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower, upper = q1 - 3 * iqr, q3 + 3 * iqr
        flag_col = f"{col}_outlier"
        df[flag_col] = ~df[col].between(lower, upper)
        n_outliers = df[flag_col].sum()
        if n_outliers:
            print(f"  [clean] Flagged {n_outliers} outliers in '{col}' (IQR ×3).")
    return df


# ── Main public function ───────────────────────────────────────────────────────
def clean_data(input_path: str = RAW_CSV, output_path: str = CLEAN_CSV) -> pd.DataFrame:
    """
    Load raw CSV → clean → save processed CSV.
    Returns the cleaned DataFrame.
    """
    print(f"\n[clean] Loading raw data from: {input_path}")
    df = pd.read_csv(input_path, encoding="latin-1")
    print(f"  Shape: {df.shape}")

    df = _normalize_columns(df)
    df = _parse_dates(df)
    df = _remove_duplicates(df)
    df = _cast_types(df)
    df = _handle_missing(df)
    df = _add_derived(df)
    df = _flag_outliers(df)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"\n[clean] Saved clean data → {output_path}")
    print(f"  Final shape: {df.shape}\n")
    return df


if __name__ == "__main__":
    clean_data()
