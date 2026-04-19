"""
analysis/trend_detector.py — Month-over-month revenue trend detection.

Flags any month where revenue dropped more than MOM_DROP_THRESHOLD vs the
prior month.

Usage:
    python -m analysis.trend_detector
"""

import os
import sys
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import CLEAN_CSV, MOM_DROP_THRESHOLD


def compute_monthly_revenue(csv_path: str = CLEAN_CSV) -> pd.DataFrame:
    """Aggregate cleaned sales data to monthly revenue totals."""
    df = pd.read_csv(csv_path, low_memory=False)

    if "order_yearmonth" not in df.columns:
        df["order_date"]      = pd.to_datetime(df["order_date"], errors="coerce")
        df["order_yearmonth"] = df["order_date"].dt.to_period("M").astype(str)

    monthly = (
        df.groupby("order_yearmonth")["sales"]
        .sum()
        .reset_index()
        .rename(columns={"sales": "revenue"})
        .sort_values("order_yearmonth")
    )
    return monthly


def detect_drops(
    monthly: pd.DataFrame,
    threshold: float = MOM_DROP_THRESHOLD,
) -> pd.DataFrame:
    """
    Add MoM change columns and a boolean `is_drop` flag.

    Returns the same DataFrame with these extra columns:
        prev_revenue   — prior month's revenue
        mom_change     — absolute change
        mom_pct        — percentage change (negative = decline)
        is_drop        — True when drop exceeds threshold
    """
    monthly = monthly.copy()
    monthly["prev_revenue"] = monthly["revenue"].shift(1)
    monthly["mom_change"]   = monthly["revenue"] - monthly["prev_revenue"]
    monthly["mom_pct"]      = (monthly["mom_change"] / monthly["prev_revenue"]).round(4)
    monthly["is_drop"]      = monthly["mom_pct"] < -threshold
    return monthly


def summarise_trends(monthly: pd.DataFrame) -> None:
    """Print a human-readable trend summary."""
    drops = monthly[monthly["is_drop"] == True]
    print("\n── Monthly Revenue Trend ──────────────────────────────────────")
    print(
        monthly[["order_yearmonth", "revenue", "mom_pct", "is_drop"]]
        .to_string(index=False)
    )
    print(f"\n⚠️  Months with revenue drop > {MOM_DROP_THRESHOLD*100:.0f}%: {len(drops)}")
    if not drops.empty:
        for _, row in drops.iterrows():
            print(
                f"   • {row['order_yearmonth']}: "
                f"${row['revenue']:,.0f}  ({row['mom_pct']*100:+.1f}%)"
            )
    print()


def run(csv_path: str = CLEAN_CSV, threshold: float = MOM_DROP_THRESHOLD) -> pd.DataFrame:
    """Full pipeline: load → compute → detect → summarise → return."""
    monthly  = compute_monthly_revenue(csv_path)
    monthly  = detect_drops(monthly, threshold)
    summarise_trends(monthly)
    return monthly


if __name__ == "__main__":
    run()
