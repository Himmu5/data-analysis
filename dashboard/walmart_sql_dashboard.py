import pandas as pd
import plotly.express as plt
import streamlit as st
from sqlalchemy import create_engine

st.set_page_config(page_title='Walmart Data Analysis', layout="wide")

st.title("🛍️ Walmart Data Analysis Dashboard")

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
col1, col2, col3, col4 = st.columns(4)

total_store = pd.read_sql("SELECT COUNT(DISTINCT Branch) as total FROM walmart;", con=conn)['total'].iloc[0]
total_revenue = pd.read_sql("SELECT SUM(total) as total FROM walmart;", con=conn)['total'].iloc[0]
total_transactions = pd.read_sql("SELECT COUNT(*) as total FROM walmart;", con=conn)['total'].iloc[0]
average_revenue_per_transaction = total_revenue / total_transactions if total_transactions > 0 else 0

col1.metric('🏬 Total Stores', f"{total_store}")
col2.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
col3.metric('🧾 Total Transactions', f"{total_transactions:,}")
col4.metric("📊 Avg. Revenue / Txn", f"${average_revenue_per_transaction:,.0f}")

st.divider() 


