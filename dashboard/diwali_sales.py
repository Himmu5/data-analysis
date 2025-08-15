import streamlit as st
import pandas as pd
import plotly.express as px

# ======================
# Load Data
# ======================
@st.cache_data
def load_data():
    return pd.read_csv("dataset/diwali_sales_data.csv", encoding="cp1252")

diwali_data = load_data()

# ======================
# Dashboard Title
# ======================
st.set_page_config(page_title="Diwali Sales Dashboard", layout="wide")
st.title("🪔 Diwali Sales Insights Dashboard")
st.markdown("A sleek, interactive dashboard to explore Diwali sales performance across demographics and regions.")

# ======================
# KPI Section
# ======================
total_sales = diwali_data["Amount"].sum()
total_customers = diwali_data["Gender"].count()
unique_states = diwali_data["State"].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Sales", f"₹{total_sales:,.0f}")
col2.metric("👥 Total Customers", f"{total_customers:,}")
col3.metric("📍 States Covered", unique_states)

st.divider()

# ======================
# Gender-wise Customer Distribution
# ======================
st.subheader("📊 Gender-wise Customer Distribution")
gender_count = diwali_data["Gender"].value_counts().reset_index()
gender_count.columns = ["Gender", "Count"]

fig = px.bar(
    gender_count,
    x="Gender",
    y="Count",
    color="Gender",
    color_discrete_sequence=["#FF9933", "#00CED1"],
    text="Count",
    template="plotly_white"
)
fig.update_traces(textposition="outside")
st.plotly_chart(fig, use_container_width=True)

# ======================
# Sales by Age Group
# ======================
st.subheader("📈 Sales by Age Group")
age_sales = diwali_data.groupby("Age Group", as_index=False)["Amount"].sum().sort_values("Amount", ascending=False)

fig = px.bar(
    age_sales,
    x="Age Group",
    y="Amount",
    color="Age Group",
    text="Amount",
    color_discrete_sequence=px.colors.qualitative.Set2,
    template="plotly_white"
)
fig.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
st.plotly_chart(fig, use_container_width=True)

# ======================
# Sales by Gender
# ======================
st.subheader("🛍 Sales by Gender")
gender_sales = diwali_data.groupby("Gender", as_index=False)["Amount"].sum()

fig = px.pie(
    gender_sales,
    names="Gender",
    values="Amount",
    color="Gender",
    color_discrete_sequence=["#FF9933", "#00CED1"],
    hole=0.4,
    template="plotly_white"
)
st.plotly_chart(fig, use_container_width=True)

# ======================
# Sales by Occupation
# ======================
st.subheader("💼 Sales by Occupation")
occupation_data = diwali_data.groupby("Occupation", as_index=False)["Amount"].sum().sort_values("Amount", ascending=False)

fig = px.bar(
    occupation_data,
    x="Occupation",
    y="Amount",
    color="Occupation",
    text="Amount",
    template="plotly_white",
    color_discrete_sequence=px.colors.qualitative.Vivid
)
fig.update_layout(showlegend=False, xaxis_tickangle=45)
fig.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
st.plotly_chart(fig, use_container_width=True)

# ======================
# Sales by State
# ======================
st.subheader("🏙 Sales by State")
state_sales = diwali_data.groupby("State", as_index=False)["Amount"].sum().sort_values("Amount", ascending=False)

fig = px.bar(
    state_sales,
    x="State",
    y="Amount",
    color="State",
    text="Amount",
    template="plotly_white",
    color_discrete_sequence=px.colors.qualitative.Prism
)
fig.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
fig.update_layout(showlegend=False, xaxis_tickangle=45)
st.plotly_chart(fig, use_container_width=True)
