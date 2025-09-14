import pandas as pd
import plotly.express as plt
import streamlit as st
from sqlalchemy import create_engine

st.set_page_config(page_title='Walmart Data Analysis', layout="wide")

st.title("🛍️ Walmart Data Analysis Dashboard")
st.caption("Interactive overview of Walmart's sales, profit margins, and category performance.")

# ------------------- DB Connection -------------------
def load_data():
    username = st.secrets["secrets"]['username'] 
    password = st.secrets["secrets"]["password"]
    host = st.secrets["secrets"]["host"]
    port = st.secrets["secrets"]["port"]
    database = st.secrets["secrets"]["database"]
    url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
    return create_engine(url)

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

st.markdown("## 🔹 Profitability & High-Value Transactions") 
st.markdown("### 🔝 Top 10 Invoices by Revenue")

top_invoices = pd.read_sql("""
    SELECT invoice_id, SUM(total) as total_revenue
    FROM walmart
    GROUP BY invoice_id
    ORDER BY total_revenue DESC
    LIMIT 10;
""", con=conn)

fig = plt.bar(
    data_frame=top_invoices,
    x="invoice_id",
    y="total_revenue",
    title="Top 10 Invoices by Revenue",
    text="total_revenue"
)
fig.update_traces(texttemplate="$%{text:,.2f}", textposition="outside")
fig.update_layout(yaxis_title="Revenue ($)", xaxis_title="Invoice ID")

st.plotly_chart(fig, use_container_width=True)

# ------------------- Quantity vs Profit Margin -------------------
st.divider()
st.markdown("## 📊 Quantity vs Profit Margin")

# Query to calculate average profit margin by quantity
quantity_vs_margin = pd.read_sql("""
    SELECT 
        quantity, 
        AVG(profit_margin) AS avg_profit_margin
    FROM walmart
    GROUP BY quantity
    ORDER BY quantity;
""", con=conn)

# Line chart (trend view)
fig_line = plt.line(
    data_frame=quantity_vs_margin,
    x="quantity",
    y="avg_profit_margin",
    markers=True,
    title="Average Profit Margin by Quantity Purchased"
)
st.plotly_chart(fig_line, use_container_width=True)

# Optional: Scatter chart (distribution view)
fig_scatter = plt.scatter(
    data_frame=quantity_vs_margin,
    x="quantity",
    y="avg_profit_margin",
    size="avg_profit_margin",
    color="avg_profit_margin",
    title="Scatter: Quantity vs Avg Profit Margin"
)
st.plotly_chart(fig_scatter, use_container_width=True)

# ------------------- Conclusion -------------------
st.divider()
st.markdown("## 📝 Key Insights & Conclusion")
with st.expander("🔍 View Summary Insights", expanded=True):
    st.markdown(
        f"""
        ### 📌 Business Highlights
        - 🏬 **Branch & City Performance**  
          Top branches and cities are driving revenue & profit — opportunities to replicate their success.  

        - 📦 **Product Categories**  
          **{category_name}** is the **highest revenue generator**, while **{rating_category}** leads customer satisfaction with an avg. rating of **{avg_rating:.2f}/5**.  

        - ⚖️ **Profitability Trade-offs**  
          Some categories sell in **large quantities but at lower margins** — potential pricing & cost optimization needed.  

        - 💳 **Payment Preferences**  
          **{top_method}** transactions deliver the **highest average value (${top_value:,.2f})**, making it the most profitable payment method to encourage.  

        - 🧾 **High-Value Customers**  
          A few invoices account for a **large revenue share** — valuable customers worth focusing retention strategies on.  

        - 📊 **Quantity vs Profit Margin**  
          Higher purchase volumes don’t always equal higher profitability — balance between volume & margins is essential.  
        """,
        unsafe_allow_html=True
    )

st.info("✅ These insights can guide strategy in pricing, promotions, customer retention, and branch-level decision making.")


# ------------------- Footer -------------------
st.divider()
st.caption("📈 Dashboard built with Streamlit, Plotly, and MySQL • Walmart Sales Analysis")

