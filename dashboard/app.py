import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sqlite3
from datetime import date

# ---------------------------------------------------------------------------
# Page configuration & dark theme CSS
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Sales Data Analysis Dashboard",
    page_icon="📊",
    layout="wide",
)

# Custom CSS – dark background, neon/gradient accents, rounded cards
DARK_CSS = """
<style>
    .stApp {
        background: #0b0e13;
        color: #e0e0e0;
    }
    .sidebar .sidebar-content {
        background: #11131a;
    }
    .kpi-card {
        background: linear-gradient(135deg, #1e1b4b, #3a0a59);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        color: #fff;
        box-shadow: 0 0 12px rgba(0,255,255,0.25);
    }
    .kpi-card h3 {
        margin: 0;
        font-size: 1.1rem;
    }
    .kpi-card p {
        margin: 0.2rem 0 0;
        font-size: 1.6rem;
        font-weight: 600;
    }
    .section-header {
        color: #00ffff;
        margin-top: 0.5rem;
        margin-bottom: 0.2rem;
        font-weight: 600;
    }
</style>
"""
st.markdown(DARK_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Paths – absolute for reproducibility
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "Superstore_cleaned.csv")
DB_PATH = os.path.join(BASE_DIR, "data", "sales_analysis.db")
VIS_DIR = os.path.join(BASE_DIR, "reports", "visualizations")

# ---------------------------------------------------------------------------
# Load data – prefer SQLite, fallback to CSV
# ---------------------------------------------------------------------------
@st.cache_data
def load_data() -> pd.DataFrame | None:
    """Return cleaned dataframe from SQLite DB if present, otherwise from CSV."""
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM sales", conn)
        conn.close()
    elif os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
    else:
        st.error("Data source not found – ensure the SQLite DB or the CSV file exists.")
        return None
    # Convert order_date to datetime for filtering/forecasting
    if "order_date" in df.columns:
        df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    return df

df = load_data()
if df is None:
    st.stop()

# ---------------------------------------------------------------------------
# Sidebar – navigation & filters
# ---------------------------------------------------------------------------
st.sidebar.title("🔎 Navigation")
section = st.sidebar.radio(
    "Go to",
    ["Overview", "Advanced Visualizations", "Forecasting", "Reports & Data Table"],
)

st.sidebar.markdown("---")
st.sidebar.header("Filters")
# Date range filter
if "order_date" in df.columns:
    min_dt = df["order_date"].min().date()
    max_dt = df["order_date"].max().date()
    start_dt, end_dt = st.sidebar.date_input(
        "Order Date Range",
        value=(min_dt, max_dt),
        min_value=min_dt,
        max_value=max_dt,
    )
    if isinstance(start_dt, date) and isinstance(end_dt, date):
        df = df[(df["order_date"].dt.date >= start_dt) & (df["order_date"].dt.date <= end_dt)]
# Region filter
if "region" in df.columns:
    regions = sorted(df["region"].dropna().unique())
    selected_regions = st.sidebar.multiselect("Region", options=regions, default=regions)
    df = df[df["region"].isin(selected_regions)]
# Category filter
if "category" in df.columns:
    categories = sorted(df["category"].dropna().unique())
    selected_categories = st.sidebar.multiselect("Category", options=categories, default=categories)
    df = df[df["category"].isin(selected_categories)]

# ---------------------------------------------------------------------------
# Helper – render KPI cards (used across sections)
# ---------------------------------------------------------------------------
def render_kpis(df: pd.DataFrame):
    total_sales = df["sales"].sum() if "sales" in df.columns else 0
    total_profit = df["profit"].sum() if "profit" in df.columns else 0
    total_orders = df["order_id"].nunique() if "order_id" in df.columns else len(df)
    profit_margin = (total_profit / total_sales * 100) if total_sales != 0 else 0
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            f"""
            <div class='kpi-card'>
                <h3>Total Sales</h3>
                <p>${total_sales:,.2f}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <div class='kpi-card'>
                <h3>Total Profit</h3>
                <p>${total_profit:,.2f}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"""
            <div class='kpi-card'>
                <h3>Total Orders</h3>
                <p>{total_orders:,}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            f"""
            <div class='kpi-card'>
                <h3>Profit Margin</h3>
                <p>{profit_margin:.2f}%</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("---")

# ---------------------------------------------------------------------------
# Section implementations
# ---------------------------------------------------------------------------
if section == "Overview":
    st.subheader("📊 Overview")
    render_kpis(df)
    st.markdown("<div class='section-header'>Key Insights</div>", unsafe_allow_html=True)
    # Quick textual insights (placeholder)
    if "order_date" in df.columns:
        best_month = (
            df.groupby(df["order_date"].dt.to_period('M'))["sales"].sum().idxmax()
        ).strftime('%B %Y')
        st.write(f"- **Best month (sales)**: {best_month}")
    if "category" in df.columns:
        top_cat = df.groupby('category')['sales'].sum().idxmax()
        st.write(f"- **Top category**: {top_cat}")

elif section == "Advanced Visualizations":
    st.subheader("🚀 Advanced Visualizations")
    render_kpis(df)
    # Compact 2x2 grid
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("<div class='section-header'>Monthly Sales & Profit Trend</div>", unsafe_allow_html=True)
        if "order_date" in df.columns:
            monthly = (
                df.groupby(df["order_date"].dt.to_period('M'))
                .agg({"sales": "sum", "profit": "sum"})
                .reset_index()
            )
            monthly["order_month"] = monthly["order_date"].astype(str)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=monthly["order_month"], y=monthly["sales"], mode='lines+markers', name='Sales', line=dict(color='#00ffff')))
            fig.add_trace(go.Scatter(x=monthly["order_month"], y=monthly["profit"], mode='lines+markers', name='Profit', line=dict(color='#ff00ff')))
            fig.update_layout(template='plotly_dark', height=350, margin=dict(l=0, r=0, t=30, b=0), legend=dict(bgcolor='#11131a'))
            st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("<div class='section-header'>Category Distribution</div>", unsafe_allow_html=True)
        if "category" in df.columns:
            cat_counts = df['category'].value_counts().reset_index()
            cat_counts.columns = ['category', 'count']
            fig = px.pie(
                cat_counts,
                names='category',
                values='count',
                hole=0.4,
                title='Category Share',
                color_discrete_sequence=px.colors.sequential.Plasma_r,
                template='plotly_dark',
            )
            fig.update_layout(height=350, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig, use_container_width=True)
    # Bottom row
    col3, col4 = st.columns(2, gap="large")
    with col3:
        st.markdown("<div class='section-header'>Top 10 Profitable Products</div>", unsafe_allow_html=True)
        if "product_name" in df.columns and "profit" in df.columns:
            top_prod = (
                df.groupby('product_name')['profit'].sum().nlargest(10).reset_index()
            )
            fig = px.bar(
                top_prod,
                x='profit',
                y='product_name',
                orientation='h',
                title='Top Products by Profit',
                color='profit',
                color_continuous_scale=['#ff00ff', '#00ffff'],
                template='plotly_dark',
            )
            fig.update_layout(yaxis={'categoryorder':'total ascending'}, height=350, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig, use_container_width=True)
    with col4:
        st.markdown("<div class='section-header'>Segment Distribution</div>", unsafe_allow_html=True)
        if "segment" in df.columns:
            seg_counts = df['segment'].value_counts().reset_index()
            seg_counts.columns = ['segment', 'count']
            fig = px.bar(
                seg_counts,
                x='segment',
                y='count',
                title='Segment Breakdown',
                color='segment',
                color_discrete_sequence=px.colors.qualitative.Dark24,
                template='plotly_dark',
            )
            fig.update_layout(height=350, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig, use_container_width=True)

elif section == "Forecasting":
    st.subheader("📈 Forecasting")
    render_kpis(df)
    st.markdown("<div class='section-header'>Simple Sales Forecast (next 6 months)</div>", unsafe_allow_html=True)
    if "order_date" in df.columns:
        # Aggregate monthly sales
        monthly = (
            df.groupby(df["order_date"].dt.to_period('M'))['sales']
            .sum()
            .reset_index()
        )
        monthly['order_month'] = monthly['order_date'].dt.to_timestamp()
        monthly = monthly.sort_values('order_month')
        # Simple linear regression forecast
        monthly['timestamp'] = monthly['order_month'].astype(int) / 10**9
        X = monthly[['timestamp']]
        y = monthly['sales']
        # Fit linear model (numpy polyfit)
        coeff = np.polyfit(monthly['timestamp'], y, 1)
        # Predict next 6 months
        last_month = monthly['order_month'].iloc[-1]
        future_months = [last_month + pd.DateOffset(months=i) for i in range(1, 7)]
        future_ts = [int(m.timestamp()) for m in future_months]
        future_sales = np.polyval(coeff, future_ts)
        forecast_df = pd.DataFrame({
            'order_month': future_months,
            'sales': future_sales,
        })
        # Combine historic and forecast for chart
        combined = pd.concat([monthly[['order_month', 'sales']], forecast_df])
        combined['type'] = ['Historical'] * len(monthly) + ['Forecast'] * len(forecast_df)
        fig = px.line(
            combined,
            x='order_month',
            y='sales',
            color='type',
            title='Sales Forecast (Linear Trend)',
            template='plotly_dark',
        )
        fig.update_traces(mode='lines+markers')
        fig.update_layout(height=450, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Order date column not available for forecasting.")

elif section == "Reports & Data Table":
    st.subheader("📄 Reports & Data Table")
    render_kpis(df)
    st.markdown("<div class='section-header'>Raw Data Preview</div>", unsafe_allow_html=True)
    # Show a sample of the data
    st.dataframe(df.head(100))
    # CSV download button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download full dataset as CSV",
        data=csv,
        file_name='Superstore_cleaned.csv',
        mime='text/csv',
    )
    # Also expose previously generated static images for completeness
    st.markdown("---")
    st.markdown("<div class='section-header'>Static Visualisations (Phase 5)</div>", unsafe_allow_html=True)
    img_col1, img_col2 = st.columns(2)
    for col, imgs in [(img_col1, ["monthly_sales_trend.png", "profit_distribution.png"]), (img_col2, ["sales_by_category.png", "correlation_heatmap.png"])]:
        with col:
            for img_name in imgs:
                img_path = os.path.join(VIS_DIR, img_name)
                if os.path.exists(img_path):
                    st.image(img_path, use_container_width=True)
