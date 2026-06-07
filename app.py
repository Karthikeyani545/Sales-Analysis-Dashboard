import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration (Dashboard Layout)
st.set_page_config(page_title="Sales & Revenue Dashboard", layout="wide", page_icon="📊")

st.title("📊 Sales & Revenue Analysis Dashboard")
st.markdown("Welcome to the interactive business intelligence dashboard. Upload your sales data to analyze performance.")

# 2. Sidebar - File Uploader
st.sidebar.header("📁 Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

# Default ga manam generate chesina dataset ni stream chese facility (optional fallback)
if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
else:
    # Safe side - user file upload cheyakapothe alert chupisthundhi
    st.info("💡 Please upload the 'sales_data.csv' file from the sidebar to visualize the live dashboard.")
    st.stop()

# Data basic cleaning (Date column conversion)
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'])

# 3. Sidebar - Interactive Filters (Slicers)
st.sidebar.header("🔍 Filter Options")

# Region Filter
selected_region = st.sidebar.multiselect(
    "Select Region:",
    options=df['Region'].unique(),
    default=df['Region'].unique()
)

# Category Filter
selected_category = st.sidebar.multiselect(
    "Select Product Category:",
    options=df['Category'].unique(),
    default=df['Category'].unique()
)

# Apply filters to dataframe
filtered_df = df[
    (df['Region'].isin(selected_region)) & 
    (df['Category'].isin(selected_category))
]

# 4. Key Performance Indicators (KPIs) Metrics
st.subheader("📌 Key Performance Indicators (KPIs)")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_sales = filtered_df['Sales_Amount'].sum()
total_profit = filtered_df['Profit'].sum()
total_qty = filtered_df['Quantity'].sum()
profit_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0

kpi1.metric(label="💰 Total Revenue", value=f"${total_sales:,.2f}")
kpi2.metric(label="📈 Total Profit", value=f"${total_profit:,.2f}")
kpi3.metric(label="📦 Items Sold", value=f"{total_qty:,}")
kpi4.metric(label="🎯 Profit Margin", value=f"{profit_margin:.1f}%")

st.markdown("---")

# 5. Visualizations Section
st.subheader("📈 Business Performance Analysis")

# Row 1: Charts
col1, col2 = st.columns(2)

# Chart 1: Revenue Trend Over Time (Line Chart)
with col1:
    st.write("### Revenue Trend Over Time")
    trend_df = filtered_df.groupby('Date')['Sales_Amount'].sum().reset_index()
    fig_trend = px.line(trend_df, x='Date', y='Sales_Amount', 
                        labels={'Sales_Amount': 'Revenue ($)'},
                        template='plotly_white', color_discrete_sequence=['#1f77b4'])
    st.plotly_chart(fig_trend, use_container_width=True)

# Chart 2: Top Performing Products (Bar Chart)
with col2:
    st.write("### Top 10 Products by Revenue")
    product_df = filtered_df.groupby('Product_Name')['Sales_Amount'].sum().reset_index()
    product_df = product_df.sort_values(by='Sales_Amount', ascending=True).tail(10) # sorted for horizontal bar
    fig_product = px.bar(product_df, x='Sales_Amount', y='Product_Name', orientation='h',
                         labels={'Sales_Amount': 'Total Sales ($)', 'Product_Name': 'Product'},
                         template='plotly_white', color_discrete_sequence=['#2ca02c'])
    st.plotly_chart(fig_product, use_container_width=True)

# Row 2: Charts
col3, col4 = st.columns(2)

# Chart 3: Sales Share by Category (Pie Chart)
with col3:
    st.write("### Revenue Share by Category")
    cat_df = filtered_df.groupby('Category')['Sales_Amount'].sum().reset_index()
    fig_pie = px.pie(cat_df, values='Sales_Amount', names='Category', 
                     hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_pie, use_container_width=True)

# Chart 4: Sales Channel Analysis (Grouped Bar Chart)
with col4:
    st.write("### Regional Sales by Channel")
    channel_df = filtered_df.groupby(['Region', 'Channel'])['Sales_Amount'].sum().reset_index()
    fig_channel = px.bar(channel_df, x='Region', y='Sales_Amount', color='Channel', barmode='group',
                         labels={'Sales_Amount': 'Sales ($)'}, template='plotly_white')
    st.plotly_chart(fig_channel, use_container_width=True)

# 6. Raw Data Showcase
st.markdown("---")
st.subheader("📋 Filtered Data Preview")
st.dataframe(filtered_df.head(100), use_container_width=True)