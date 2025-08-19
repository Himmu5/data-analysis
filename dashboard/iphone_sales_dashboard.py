import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
from itertools import combinations
from collections import Counter

# ======================
# Load Data
# ======================
@st.cache_data
def load_data():
    return pd.read_csv("dataset/iphone_sales.csv")

iphone_sales_data = load_data()

# ======================
# Page Setup
# ======================
st.set_page_config(page_title="Product Sales Dashboard", layout='wide')
st.title("📱 Product Sales Dashboard")

# ======================
# Sidebar Filters
# ======================
st.sidebar.header("🔎 Filters")

# Date filter (if you have a Date column)
if "Date" in iphone_sales_data.columns:
    iphone_sales_data["Date"] = pd.to_datetime(iphone_sales_data["Date"])
    date_range = st.sidebar.date_input(
        "Select Date Range",
        [iphone_sales_data["Date"].min(), iphone_sales_data["Date"].max()]
    )
    if len(date_range) == 2:
        start, end = date_range
        iphone_sales_data = iphone_sales_data[
            (iphone_sales_data["Date"] >= pd.to_datetime(start)) &
            (iphone_sales_data["Date"] <= pd.to_datetime(end))
        ]

# Customer filter
all_customers = sorted(iphone_sales_data["Name"].unique())
selected_customers = st.sidebar.multiselect("Select Customers", all_customers)
if selected_customers:
    iphone_sales_data = iphone_sales_data[iphone_sales_data["Name"].isin(selected_customers)]

# Product filter
all_products = sorted(set(iphone_sales_data["Product"].str.split(",").explode()))
selected_products = st.sidebar.multiselect("Select Products", all_products)
if selected_products:
    iphone_sales_data = iphone_sales_data[
        iphone_sales_data["Product"].apply(lambda x: any(p in x for p in selected_products))
    ]

st.sidebar.markdown("---")
st.sidebar.write(f"📊 Showing **{len(iphone_sales_data)}** transactions")

# ======================
# KPIs
# ======================
total_transactions = iphone_sales_data.aggregate("Name").count()
total_products = iphone_sales_data['Product'].str.split(",").explode().nunique()
iphone_sales_data['Product Count'] = iphone_sales_data["Product"].str.split(",").apply(len)
average_product_per_transaction = round(iphone_sales_data['Product Count'].mean(), 1)

col1, col2, col3 = st.columns(3)
col1.metric("💸 Total transactions", f"{total_transactions:,.0f}")
col2.metric("👥 Unique products", f"{total_products:,}")
col3.metric("📍 Avg products per transaction", average_product_per_transaction)

st.divider()

# ======================
# Customer Insights
# ======================
st.markdown("### Customer Insights")

# Top customers
st.markdown("#### Top Customers by Number of Purchases")
top_n = st.slider("Select number of top customers", 5, 20, 10)
top_customer = iphone_sales_data["Name"].value_counts().reset_index().head(top_n)
fig = px.bar(top_customer, x="Name", y="count", color='Name')
st.plotly_chart(fig, use_container_width=True)

# Domain distribution
st.markdown("#### Email Domains Distribution")
iphone_sales_data['domain'] = iphone_sales_data['Email'].str.split("@").str[-1]
top_domain = st.slider("Select number of top domains", 5, 20, 10)
top_domain_df = iphone_sales_data['domain'].value_counts().head(top_domain).reset_index()
fig = px.bar(top_domain_df, x="domain", y="count", color='domain')
st.plotly_chart(fig, use_container_width=True)

# ======================
# Product Insights
# ======================
st.markdown("### Product Insights")

# Top purchased products
st.markdown("#### Most Frequently Purchased Products")
top_product = st.slider("Select number of top products", 5, 20, 10)
top_product_df = iphone_sales_data['Product'].str.split(",").explode().value_counts().reset_index().head(top_product)
fig = px.bar(top_product_df, x='Product', y='count', color="Product")
st.plotly_chart(fig, use_container_width=True)

# Products bought together
st.markdown("#### Products Often Bought Together")
transactions = iphone_sales_data['Product'].str.split(",")
pair_product = Counter()
for products in transactions:
    if len(products) > 1:
        pair = combinations(sorted(products), 2)
        pair_product.update(pair)

product_pair_df = pd.DataFrame(pair_product.items(), columns=["Product Pair", "Count"])
if not product_pair_df.empty:
    product_pair_df[["Product1", "Product2"]] = pd.DataFrame(product_pair_df['Product Pair'].tolist(), index=product_pair_df.index)
    heat_map = product_pair_df.pivot(index='Product1', values='Count', columns='Product2')
    fig = px.density_heatmap(heat_map, color_continuous_scale='Viridis')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No product pair data available after filters.")

# Single vs Multi-product
st.markdown("#### Single vs Multi-Product Transactions")
iphone_sales_data['is_multi_product'] = iphone_sales_data['Product Count'] > 1
iphone_sales_data['transaction_type'] = iphone_sales_data['is_multi_product'].map({True: "Multi-Product", False: "Single-Product"})
single_multi_product = iphone_sales_data['transaction_type'].value_counts().reset_index()
single_multi_product.columns = ["transaction_type", "count"]

fig = px.pie(
    single_multi_product,
    names="transaction_type",
    values="count",
    color="transaction_type",
    color_discrete_map={
        "Single-Product": "green",
        "Multi-Product": "orange"
    },
    hole=0.3
)
fig.update_traces(textinfo="percent+label")
st.plotly_chart(fig, use_container_width=True)
