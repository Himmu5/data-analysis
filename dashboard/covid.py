import pandas as pd
import matplotlib.pyplot as plt
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
# Dashboard Config
# ======================
st.set_page_config(page_title="🦠 Covid-19 Dashboard", page_icon="🌍", layout="wide")
st.title("🦠 Global COVID-19 Insights Dashboard")
st.markdown("An interactive overview of worldwide cases, recoveries, and deaths.")

# ======================
# KPI Section
# ======================
total_cases = covid_data['TotalCases'].sum()
total_deaths = covid_data['TotalDeaths'].sum()
total_recovered = covid_data["TotalRecovered"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("🌍 Total Cases", f"{total_cases/1e6:.2f}M")
col2.metric("❤️ Total Recovered", f"{total_recovered/1e6:.2f}M")
col3.metric("☠️ Total Deaths", f"{total_deaths/1e6:.2f}M")

st.divider()

# ======================
# Top 10 Deaths by Country
# ======================
st.subheader("☠️ Top 10 Countries by COVID-19 Deaths")
top10_deaths_country = (
    covid_data.groupby("Country/Region")["TotalDeaths"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
fig = px.bar(
    top10_deaths_country,
    x="Country/Region",
    y="TotalDeaths",
    color="Country/Region",
    template="plotly_dark",
    title="Top 10 Countries with Highest COVID-19 Deaths",
)
st.plotly_chart(fig, use_container_width=True)

# ======================
# Correlation Heatmap
# ======================
st.subheader("📈 Correlation Between COVID-19 Metrics")
corr = covid_data[["TotalCases", "TotalDeaths", "TotalRecovered", "ActiveCases", "TotalTests"]].corr()
fig, ax = plt.subplots(figsize=(8,5))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
plt.title("Correlation of COVID-19 Metrics", fontsize=14)
st.pyplot(fig) 

# ======================
# Geographic Distribution
# ======================
st.subheader("🌍 COVID-19 Cases per Million Population (World Map)")
fig = px.choropleth(
    covid_data,
    locations="iso_alpha",
    color="Tot Cases/1M pop",
    hover_name="Country/Region",
    color_continuous_scale="Reds",
    template="plotly_dark",
)
st.plotly_chart(fig, use_container_width=True)

# ======================
# Continent-wise Distribution (Donut)
# ======================
st.subheader("🦠 Continent-wise COVID-19 Cases Distribution")
continent_cases = covid_data.groupby("Continent")["TotalCases"].sum().reset_index()
fig = px.pie(
    continent_cases,
    names="Continent",
    values="TotalCases",
    hole=0.4,
    color_discrete_sequence=px.colors.qualitative.Set2
)
st.plotly_chart(fig, use_container_width=True)
