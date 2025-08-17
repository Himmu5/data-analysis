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

st.subheader("📊 Top 10 countries with most number of deaths")
top10_deaths_country = covid_data.groupby("Country/Region").aggregate("TotalDeaths").sum().sort_values(ascending=False).head(10).reset_index()
fig = px.bar(
    top10_deaths_country,
    x="Country/Region",
    y="TotalDeaths",
    color="Country/Region",
    template="plotly_white"
)
st.plotly_chart(fig, use_container_width=True)


st.subheader("📈 Correlation Between COVID-19 Metrics")
plt.style.use("dark_background")
corr = covid_data[["TotalCases", "TotalDeaths", "TotalRecovered", "ActiveCases", "TotalTests"]].corr()
fig, ax = plt.subplots(figsize=(8,4))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
st.pyplot(fig) 

st.subheader("Geographic Distribution of COVID-19 Cases per Million")
fig = px.choropleth(
    covid_data,
    locations="iso_alpha",            # ISO country codes
    color="Tot Cases/1M pop",         # Cases per million
    hover_name="Country/Region",      # Show country on hover
    color_continuous_scale="Reds",    # Color scale
)
st.plotly_chart(fig, use_container_width=True)

continent_cases = covid_data.groupby("Continent")["TotalCases"].sum()
fig, ax = plt.subplots(figsize=(7,7))
ax.pie(
    continent_cases.values,
    labels=continent_cases.index,
    autopct="%1.1f%%",
    startangle=90,
    colors=plt.cm.Paired.colors
)

ax.set_title("🦠 Distribution of COVID-19 Cases Across Continents")
st.pyplot(fig) 