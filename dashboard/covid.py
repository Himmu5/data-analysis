import pandas as pd
import matplotlib.pyplot as mlt
import seaborn as sns
import plotly.express as px
import streamlit as st

# ======================
# Load Data
# ======================
@st.cache_data
def load_data():
    return pd.read_csv("dataset/covid.csv", encoding="cp1252")

covid_data = load_data()

# ======================
# Dashboard Title
# ======================
st.set_page_config(page_title="Covid Dashboard", layout="wide")
st.title("🦠 Covid Cases Insights Dashboard")
st.markdown("Global Overview of Cases, Deaths, and Recoveries")

total_cases = covid_data['TotalCases'].sum()
total_deaths = covid_data['TotalDeaths'].sum()
total_recovered = covid_data["TotalRecovered"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("🌍 Total Cases", f"{total_cases:,.0f}")
col2.metric("❤️ Total Recovered", f"{total_recovered:,}")
col3.metric("☠️ Total Deaths", total_deaths)

st.divider()

st.subheader("📊 Gender-wise Customer Distribution")
top10_deaths_country = covid_data.groupby("Country/Region").aggregate("TotalDeaths").sum().sort_values(ascending=False).head(10)
# gender_count.columns = ["Gender", "Count"]
