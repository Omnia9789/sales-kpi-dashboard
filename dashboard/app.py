"""
dashboard/app.py — Interactive Streamlit KPI Dashboard.

Launch:
    streamlit run dashboard/app.py
"""

import os
import sys

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import CLEAN_CSV, DASHBOARD_TITLE, DASHBOARD_FAVICON, MOM_DROP_THRESHOLD
from analysis.trend_detector import compute_monthly_revenue, detect_drops
from reports.report_generator import generate_report

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=DASHBOARD_TITLE,
    page_icon=DASHBOARD_FAVICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #1F3864, #2E75B6);
        border-radius: 12px;
        padding: 18px 22px;
        color: white;
        text-align: center;
        margin-bottom: 8px;
    }
    .metric-card h3 { margin: 0; font-size: 14px; opacity: 0.85; }
    .metric-card h1 { margin: 4px 0 0; font-size: 26px; }
    .alert-box {
        background: #fff3cd; border-left: 5px solid #ffc107;
        padding: 10px 16px; border-radius: 4px; margin-top: 8px;
    }
    [data-testid="stMetricValue"] { font-size: 22px !important; }
</style>
""", unsafe_allow_html=True)


# ── Data loader ───────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Loading data …")
def load_data(path: str = CLEAN_CSV) -> pd.DataFrame:
    if not os.path.exists(path):
        st.error(
            f"Cleaned data not found at `{path}`.\n\n"
            "Please run **`python main.py`** (or `python -m analysis.clean`) first."
        )
        st.stop()
    df = pd.read_csv(path, low_memory=False)
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    return df


# ── Sidebar filters ───────────────────────────────────────────────────────────
def sidebar_filters(df: pd.DataFrame):
    st.sidebar.header("🔍 Filters")

    years = sorted(df["order_year"].dropna().unique().astype(int))
    sel_years = st.sidebar.multiselect("Year", years, default=years)

    regions = sorted(df["region"].dropna().unique())
    sel_regions = st.sidebar.multiselect("Region", regions, default=regions)

    categories = sorted(df["category"].dropna().unique())
    sel_cats = st.sidebar.multiselect("Category", categories, default=categories)

    segments = sorted(df["segment"].dropna().unique())
    sel_segs = st.sidebar.multiselect("Segment", segments, default=segments)

    st.sidebar.markdown("---")
    st.sidebar.caption(f"MoM drop threshold: **{MOM_DROP_THRESHOLD*100:.0f}%**")

    mask = (
        df["order_year"].isin(sel_years) &
        df["region"].isin(sel_regions) &
        df["category"].isin(sel_cats) &
        df["segment"].isin(sel_segs)
    )
    return df[mask]


# ── KPI metrics row ───────────────────────────────────────────────────────────
def kpi_row(df: pd.DataFrame) -> None:
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    metrics = [
        (c1, "💰 Total Revenue",    f"${df['sales'].sum():,.0f}",       None),
        (c2, "📈 Total Profit",     f"${df['profit'].sum():,.0f}",      None),
        (c3, "📊 Profit Margin",    f"{df['profit'].sum()/df['sales'].sum()*100:.1f}%", None),
        (c4, "🛒 Total Orders",     f"{df['order_id'].nunique():,}",    None),
        (c5, "👤 Customers",        f"{df['customer_id'].nunique():,}", None),
        (c6, "📦 Products",         f"{df['product_id'].nunique():,}",  None),
    ]
    for col, label, value, delta in metrics:
        col.metric(label, value, delta)


# ── Charts ────────────────────────────────────────────────────────────────────
def monthly_trend_chart(df: pd.DataFrame) -> None:
    st.subheader("📅 Monthly Revenue Trend")

    monthly = (
        df.groupby("order_yearmonth")["sales"]
        .sum()
        .reset_index()
        .rename(columns={"sales": "revenue"})
        .sort_values("order_yearmonth")
    )
    monthly["prev"]    = monthly["revenue"].shift(1)
    monthly["mom_pct"] = ((monthly["revenue"] - monthly["prev"]) / monthly["prev"]).round(4)
    monthly["drop"]    = monthly["mom_pct"] < -MOM_DROP_THRESHOLD

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly["order_yearmonth"], y=monthly["revenue"],
        mode="lines+markers", name="Revenue",
        line=dict(color="#2E75B6", width=2),
        marker=dict(size=5),
    ))
    # Highlight drop months
    drops = monthly[monthly["drop"]]
    if not drops.empty:
        fig.add_trace(go.Scatter(
            x=drops["order_yearmonth"], y=drops["revenue"],
            mode="markers", name="⚠️ Drop > 10%",
            marker=dict(color="red", size=10, symbol="x"),
        ))
    fig.update_layout(
        xaxis_title="Month", yaxis_title="Revenue ($)",
        legend=dict(orientation="h", y=1.1),
        height=340, margin=dict(l=0, r=0, t=10, b=0),
    )
    st.plotly_chart(fig, use_container_width=True)

    n_drops = len(drops)
    if n_drops:
        st.markdown(
            f'<div class="alert-box">⚠️ <b>{n_drops} month(s)</b> had a revenue drop '
            f'greater than {MOM_DROP_THRESHOLD*100:.0f}%: '
            f'{", ".join(drops["order_yearmonth"].tolist())}</div>',
            unsafe_allow_html=True,
        )


def region_chart(df: pd.DataFrame) -> None:
    st.subheader("🗺️ Revenue by Region")
    region_df = (
        df.groupby("region")[["sales","profit"]]
        .sum().round(2).reset_index()
        .sort_values("sales", ascending=False)
    )
    fig = px.bar(
        region_df, x="region", y=["sales","profit"],
        barmode="group", color_discrete_sequence=["#2E75B6","#70AD47"],
        labels={"value":"Amount ($)","variable":"Metric"},
        height=320,
    )
    fig.update_layout(margin=dict(l=0,r=0,t=10,b=0))
    st.plotly_chart(fig, use_container_width=True)


def category_chart(df: pd.DataFrame) -> None:
    st.subheader("📦 Revenue by Category")
    cat_df = (
        df.groupby(["category","sub_category"])["sales"]
        .sum().reset_index().sort_values("sales", ascending=False)
    )
    fig = px.treemap(
        cat_df, path=["category","sub_category"], values="sales",
        color="sales", color_continuous_scale="Blues",
        height=360,
    )
    fig.update_layout(margin=dict(l=0,r=0,t=10,b=0))
    st.plotly_chart(fig, use_container_width=True)


def top_products_chart(df: pd.DataFrame, n: int = 10) -> None:
    st.subheader(f"🏆 Top {n} Products by Revenue")
    prod_df = (
        df.groupby("product_name")["sales"]
        .sum().reset_index()
        .sort_values("sales", ascending=False)
        .head(n)
    )
    fig = px.bar(
        prod_df, x="sales", y="product_name",
        orientation="h", color="sales",
        color_continuous_scale="Blues",
        labels={"sales":"Revenue ($)","product_name":"Product"},
        height=360,
    )
    fig.update_layout(yaxis=dict(autorange="reversed"), margin=dict(l=0,r=0,t=10,b=0))
    st.plotly_chart(fig, use_container_width=True)


def segment_pie(df: pd.DataFrame) -> None:
    st.subheader("👥 Revenue by Segment")
    seg_df = df.groupby("segment")["sales"].sum().reset_index()
    fig = px.pie(
        seg_df, names="segment", values="sales",
        color_discrete_sequence=px.colors.sequential.Blues_r,
        height=300,
    )
    fig.update_layout(margin=dict(l=0,r=0,t=10,b=0))
    st.plotly_chart(fig, use_container_width=True)


def profit_margin_scatter(df: pd.DataFrame) -> None:
    st.subheader("💹 Discount vs. Profit Margin")
    fig = px.scatter(
        df.sample(min(2000, len(df)), random_state=42),
        x="discount", y="profit_margin",
        color="category", opacity=0.5,
        labels={"discount":"Discount","profit_margin":"Profit Margin (%)"},
        height=320,
    )
    fig.update_layout(margin=dict(l=0,r=0,t=10,b=0))
    st.plotly_chart(fig, use_container_width=True)


# ── Raw data tab ──────────────────────────────────────────────────────────────
def raw_data_tab(df: pd.DataFrame) -> None:
    st.subheader("🗂️ Filtered Raw Data")
    st.dataframe(df.head(500), use_container_width=True, height=400)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download filtered data (CSV)", csv,
                       "filtered_sales.csv", "text/csv")


# ── Report generator tab ──────────────────────────────────────────────────────
def report_tab() -> None:
    st.subheader("📄 Generate Excel Report")
    st.write(
        "Click the button below to produce a fully formatted Excel workbook "
        "with KPI summaries, charts, and trend analysis."
    )
    if st.button("🚀 Generate Report Now", type="primary"):
        with st.spinner("Building report …"):
            try:
                path = generate_report()
                with open(path, "rb") as f:
                    st.download_button(
                        "⬇️ Download Excel Report",
                        f.read(),
                        os.path.basename(path),
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                st.success(f"Report ready: `{os.path.basename(path)}`")
            except Exception as exc:
                st.error(f"Error generating report: {exc}")


# ── App layout ────────────────────────────────────────────────────────────────
def main() -> None:
    st.title(f"{DASHBOARD_FAVICON} {DASHBOARD_TITLE}")
    st.caption("Superstore Sales Analysis · SQL-based KPIs · Automated Reporting")
    st.markdown("---")

    df_full = load_data()
    df      = sidebar_filters(df_full)

    if df.empty:
        st.warning("No data matches the current filters. Please adjust the sidebar selections.")
        return

    kpi_row(df)
    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📈 Trends & KPIs", "🗺️ Region & Segment", "📦 Products & Categories", "🗂️ Data & Reports"]
    )

    with tab1:
        monthly_trend_chart(df)
        profit_margin_scatter(df)

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            region_chart(df)
        with col2:
            segment_pie(df)

    with tab3:
        category_chart(df)
        top_products_chart(df)

    with tab4:
        col1, col2 = st.columns([3, 1])
        with col1:
            raw_data_tab(df)
        with col2:
            report_tab()


if __name__ == "__main__":
    main()
