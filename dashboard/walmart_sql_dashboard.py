import pandas as pd
import plotly.express as plt
import streamlit as st
from sqlalchemy import create_engine

st.set_page_config(page_title='Walmart Data Analysis', layout="wide")

st.title("🛍️ Walmart Data Analysis Dashboard")
st.caption("Interactive overview of Walmart's sales, profit margins, and category performance.")

# ------------------- DB Connection -------------------
def load_data():
    username = "root"
    password = ""
    host = "localhost"
    port = 3306
    database = 'data_analysis'
    return create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}")

conn = load_data()

# ------------------- KPIs -------------------
st.divider()
st.markdown("## 📌 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

total_store = pd.read_sql("SELECT COUNT(DISTINCT Branch) as total FROM walmart;", con=conn)['total'].iloc[0]
total_revenue = pd.read_sql("SELECT SUM(total) as total FROM walmart;", con=conn)['total'].iloc[0]
total_transactions = pd.read_sql("SELECT COUNT(*) as total FROM walmart;", con=conn)['total'].iloc[0]
average_revenue_per_transaction = total_revenue / total_transactions if total_transactions > 0 else 0

col1.metric('🏬 Total Stores', f"{total_store}")
col2.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
col3.metric('🧾 Total Transactions', f"{total_transactions:,}")
col4.metric("📊 Avg. Revenue / Txn", f"${average_revenue_per_transaction:,.0f}")

# ------------------- Overview -------------------
st.divider()
st.markdown("## 🌍 Revenue & Profit Overview")

colA, colB = st.columns(2)

with colA:
    st.markdown("### 🏢 Top 5 Branches by Revenue")
    total_revenue_by_branch = pd.read_sql("""
        SELECT branch, SUM(total) as total_revenue 
        FROM walmart 
        GROUP BY branch 
        ORDER BY total_revenue DESC 
        LIMIT 5;
    """, con=conn) 
    fig_branch = plt.bar(
        data_frame=total_revenue_by_branch,
        x='branch',
        y='total_revenue',
        color='branch',
        text='total_revenue'
    )
    fig_branch.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
    st.plotly_chart(fig_branch, use_container_width=True)

with colB:
    st.markdown("### 🏙️ Top 5 Cities by Avg. Profit Margin")
    average_profit_margin = pd.read_sql("""
        SELECT city, AVG(profit_margin) as avg 
        FROM walmart 
        GROUP BY city 
        ORDER BY avg DESC 
        LIMIT 5;
    """, con=conn)
    fig_city = plt.bar(
        data_frame=average_profit_margin,
        x='city',
        y='avg',
        color='city',
        text='avg'
    )
    fig_city.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    st.plotly_chart(fig_city, use_container_width=True)

# ------------------- Category Insights -------------------
st.divider()
st.markdown("## 🔹 Product Category Insights")

# Highest Revenue Category
highest_category = pd.read_sql("""
    SELECT category, SUM(total) as total_revenue
    FROM walmart
    GROUP BY category
    ORDER BY total_revenue DESC
    LIMIT 1;
""", con=conn)

category_name = highest_category['category'].iloc[0]
category_revenue = highest_category['total_revenue'].iloc[0]

st.success(
    f"🏆 The **{category_name}** category generated the **highest revenue** "
    f"of **${category_revenue:,.2f}**."
)

# Highest Average Rating Category
highest_rating = pd.read_sql("""
    SELECT category, AVG(rating) as rating
    FROM walmart
    GROUP BY category
    ORDER BY rating DESC
    LIMIT 1;
""", con=conn)

rating_category = highest_rating['category'].iloc[0]
avg_rating = highest_rating['rating'].iloc[0]

st.info(
    f"⭐ The **{rating_category}** category has the **highest average customer rating** "
    f"of **{avg_rating:.2f} / 5**."
)

# Chart: Top 5 categories by average rating
st.markdown("### ⭐ Top 5 Categories by Average Customer Rating")
top_rated_categories = pd.read_sql("""
    SELECT category, AVG(rating) as avg_rating
    FROM walmart
    GROUP BY category
    ORDER BY avg_rating DESC
    LIMIT 5;
""", con=conn)

fig_rating = plt.bar(
    data_frame=top_rated_categories,
    x="category",
    y="avg_rating",
    color="category",
    text="avg_rating"
)
fig_rating.update_traces(texttemplate='%{text:.2f}', textposition='outside')
fig_rating.update_layout(yaxis_title="Average Rating (out of 5)")
st.plotly_chart(fig_rating, use_container_width=True)

# Chart: Top 5 categories by revenue
st.markdown("### 📊 Top 5 Categories by Revenue")
category_revenue = pd.read_sql("""
    SELECT category, SUM(total) as total_revenue
    FROM walmart
    GROUP BY category
    ORDER BY total_revenue DESC
    LIMIT 5;
""", con=conn)

fig_category = plt.pie(
    data_frame=category_revenue,
    names='category',
    values='total_revenue',
    title="Revenue Share by Category"
)
st.plotly_chart(fig_category, use_container_width=True)

# Chart: High Quantity but Low Profit Margin
st.markdown("### ⚖️ Categories Selling High Quantity but with Low Profit Margins")

quantity_profit = pd.read_sql("""
    SELECT category, SUM(quantity) as total_quantity, AVG(profit_margin) as avg_profit_margin
    FROM walmart
    GROUP BY category
    ORDER BY total_quantity DESC;
""", con=conn)

fig_quantity_margin = plt.scatter(
    data_frame=quantity_profit,
    x="total_quantity",
    y="avg_profit_margin",
    size="total_quantity",
    color="category",
    hover_name="category",
    title="Quantity vs Profit Margin by Category",
    size_max=60
)
fig_quantity_margin.update_layout(
    xaxis_title="Total Quantity Sold",
    yaxis_title="Average Profit Margin",
    legend_title="Category"
)
st.plotly_chart(fig_quantity_margin, use_container_width=True)

# ------------------- Payment Method Analysis ------------------- 
st.divider()
st.markdown("## 🔹 Payment Method Analysis")

# Query payment distribution
payment_distribution = pd.read_sql("""
    SELECT payment_method, COUNT(*) as total
    FROM walmart
    GROUP BY payment_method
    ORDER BY total DESC;
""", con=conn)

# Calculate total transactions
total_payments = payment_distribution['total'].sum()
payment_distribution['percentage'] = (payment_distribution['total'] / total_payments) * 100

# KPI Cards
col1, col2, col3 = st.columns(3)
for idx, row in payment_distribution.iterrows():
    if row['payment_method'].lower() == "cash":
        col1.metric("💵 Cash", f"{row['total']:,}", f"{row['percentage']:.1f}%")
    elif row['payment_method'].lower() == "ewallet":
        col2.metric("📱 E-Wallet", f"{row['total']:,}", f"{row['percentage']:.1f}%")
    else:
        col3.metric("💳 Credit Card", f"{row['total']:,}", f"{row['percentage']:.1f}%")

# Pie Chart
st.markdown("### 📊 Payment Method Share")
fig_pie = plt.pie(
    data_frame=payment_distribution,
    names="payment_method",
    values="total",
    hole=0.4,  # donut style
    title="Distribution of Payment Methods"
)
fig_pie.update_traces(textinfo="percent+label")
st.plotly_chart(fig_pie, use_container_width=True)

# Bar Chart
st.markdown("### 📊 Payment Method Comparison (Counts)")
fig_bar = plt.bar(
    data_frame=payment_distribution,
    x="payment_method",
    y="total",
    color="payment_method",
    text="total"
)
fig_bar.update_traces(texttemplate="%{text:,}", textposition="outside")
fig_bar.update_layout(yaxis_title="Number of Transactions")
st.plotly_chart(fig_bar, use_container_width=True)

# Average Transaction Value by Payment Method
st.markdown("### 💡 Average Transaction Value by Payment Method")
avg_txn_value = pd.read_sql("""
    SELECT payment_method, AVG(total) as avg_transaction_value
    FROM walmart
    GROUP BY payment_method
    ORDER BY avg_transaction_value DESC;
""", con=conn)

# Highlight the best payment method
top_method = avg_txn_value.iloc[0]['payment_method']
top_value = avg_txn_value.iloc[0]['avg_transaction_value']

st.success(
    f"🏆 Customers using **{top_method}** have the **highest average transaction value** "
    f"of **${top_value:,.2f}**."
)

# Bar Chart for average transaction value
fig_avg = plt.bar(
    data_frame=avg_txn_value,
    x="payment_method",
    y="avg_transaction_value",
    color="payment_method",
    text="avg_transaction_value"
)
fig_avg.update_traces(texttemplate="$%{text:,.2f}", textposition="outside")
fig_avg.update_layout(yaxis_title="Avg. Transaction Value ($)")
st.plotly_chart(fig_avg, use_container_width=True)

# ------------------- Footer -------------------
st.divider()
st.caption("📈 Dashboard built with Streamlit, Plotly, and MySQL • Walmart Sales Analysis")

