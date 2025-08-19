import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
from itertools import combinations
from collections import Counter

@st.cache_data
def load_data():
    return pd.read_csv("dataset/iphone_sales.csv")

iphone_sales_data = load_data()

st.set_page_config(page_title="Product Sales Dashboard", layout='wide')
st.title("📱Product Sales Dashboard")

total_transactions = iphone_sales_data.aggregate("Name").count() 
total_products = iphone_sales_data['Product'].str.split(",").explode().value_counts().reset_index().count()['Product']
iphone_sales_data['Product Count'] = iphone_sales_data["Product"].str.split(",").apply(len)
average_product_per_transaction = round(iphone_sales_data['Product Count'].sum() / iphone_sales_data['Name'].count(), 1)

col1, col2, col3 = st.columns(3)
col1.metric("💸 Total transactions", f"{total_transactions:,.0f}")
col2.metric("👥 Total products", f"{total_products:,}")
col3.metric("📍 Average products per transaction", average_product_per_transaction)

st.divider()

st.markdown("### Customer Insights")
st.markdown("#### Top Customers by Number of Purchases")
top_10_customer = iphone_sales_data["Name"].value_counts().reset_index().head(10)
fig = px.bar(
    top_10_customer,
    x="Name",
    y="count",
    color='Name'
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("#### Email Domains Distribution")
iphone_sales_data['domain'] = iphone_sales_data['Email'].str.split("@").str[-1]
top_10_domain = iphone_sales_data['domain'].value_counts().head(10).reset_index()
fig = px.bar(
    top_10_domain,
    x="domain",
    y="count",
    color='domain'
)
st.plotly_chart(fig, use_container_width=True)


st.markdown("### Product Insights")
st.markdown("#### Most Frequently Purchased Products")
top_10_product_purchased = iphone_sales_data['Product'].str.split(",").explode().value_counts().reset_index().head(10)
fig = px.bar(top_10_product_purchased, x='Product', y='count', color="Product")
st.plotly_chart(fig, use_container_width=True)

st.markdown("#### Products Often Bought Together")
transactions = iphone_sales_data['Product'].str.split(",")
pair_product = Counter()
for products in transactions:
    if len(products) > 1:
        pair = combinations(sorted(products), 2)
        pair_product.update(pair)

product_pair_df = pd.DataFrame(pair_product.items(), columns=["Product Pair", "Count"])
product_pair_df[["Product1", "Product2"]] = pd.DataFrame(product_pair_df['Product Pair'].tolist(), index=product_pair_df.index)
heat_map = product_pair_df.pivot(index='Product1', values='Count', columns='Product2')
fig = px.density_heatmap(heat_map, color_continuous_scale='Viridis')
st.plotly_chart(fig, use_container_width=True)