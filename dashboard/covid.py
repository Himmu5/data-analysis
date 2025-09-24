import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

# ======================
# Dashboard Configuration
# ======================
st.set_page_config(page_title="🦠 Covid-19 Dashboard", layout="wide")
st.markdown(
    """
    <style>
    .main {
        background-color: #f0f4c3; /* Light lime background */
        color: #37474f; /* Charcoal text color */
        font-family: Arial, sans-serif;
    }
    .stMetric {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        color: #37474f; /* Charcoal text color for metrics */
    }
    .stButton > button {
        background-color: #8bc34a; /* Lime green button color */
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
    }
    .stButton > button:hover {
        background-color: #689f38; /* Dark lime hover color */
    }
    .stMarkdown h2 {
        color: #558b2f; /* Olive green for section headers */
    }
    .stMarkdown h3 {
        color: #33691e; /* Dark olive green for subsection headers */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🦠 COVID-19 Data Analysis Dashboard")
st.caption("Interactive insights into the global impact of COVID-19, including cases, recoveries, deaths, and testing efficiency.")

# ======================
# Load Data
# ======================
st.markdown("### 📂 Data Loading")
st.info("The data is sourced from a reliable dataset and includes metrics such as total cases, deaths, recoveries, and testing statistics.")
@st.cache_data
def load_data():
    return pd.read_csv("dataset/covid.csv", encoding="cp1252")

covid_data = load_data()

# ======================
# KPIs Section
# ======================
st.divider()
st.markdown("## 📌 Key Metrics")
st.info("This section highlights the most critical COVID-19 statistics globally, including total cases, recoveries, and deaths.")

col1, col2, col3 = st.columns(3)

total_cases = covid_data['TotalCases'].sum()
total_deaths = covid_data['TotalDeaths'].sum()
total_recovered = covid_data["TotalRecovered"].sum()

col1.metric("🌍 Total Cases", f"{total_cases/1e6:.2f}M", "Total confirmed cases worldwide.")
col2.metric("❤️ Total Recovered", f"{total_recovered/1e6:.2f}M", "Total recoveries from COVID-19 globally.")
col3.metric("☠️ Total Deaths", f"{total_deaths/1e6:.2f}M", "Total fatalities due to COVID-19 worldwide.")

# ======================
# Global Insights
# ======================
st.divider()
st.markdown("## 🌍 Global Insights")
st.info("Explore global trends, including the top 10 countries by deaths and correlations between key metrics.")

colA, colB = st.columns(2)

with colA:
    st.markdown("### ☠️ Top 10 Countries by COVID-19 Deaths")
    st.info("This bar chart shows the countries with the highest number of COVID-19-related deaths.")
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
        template="plotly_white",
        title="Top 10 Countries with Highest COVID-19 Deaths",
    )
    st.plotly_chart(fig, use_container_width=True)

with colB:
    st.markdown("### 📈 Correlation Between COVID-19 Metrics")
    st.info("This heatmap visualizes the relationships between key COVID-19 metrics, such as cases, deaths, and recoveries.")
    corr = covid_data[["TotalCases", "TotalDeaths", "TotalRecovered", "ActiveCases", "TotalTests"]].corr()
    fig, ax = plt.subplots(figsize=(8,5))
    sns.set(style="whitegrid")
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    ax.set_facecolor("white")
    plt.title("Correlation of COVID-19 Metrics", fontsize=14)
    st.pyplot(fig)

# ======================
# Geographic Distribution
# ======================
st.divider()
st.markdown("## 🗺️ Geographic Distribution")
st.info("This section provides a global view of COVID-19 cases per million population using a choropleth map.")

st.markdown("### 🌍 COVID-19 Cases per Million Population (World Map)")
fig = px.choropleth(
    covid_data,
    locations="iso_alpha",
    color="Tot Cases/1M pop",
    hover_name="Country/Region",
    color_continuous_scale="Reds",
    template="plotly_white",
)
st.plotly_chart(fig, use_container_width=True)

# ======================
# Continent Insights
# ======================
st.divider()
st.markdown("## 🌎 Continent Insights")
st.info("Analyze the distribution of COVID-19 cases across different continents.")

st.markdown("### 🦠 Continent-wise COVID-19 Cases Distribution")
continent_cases = covid_data.groupby("Continent")["TotalCases"].sum().reset_index()
fig = px.pie(
    continent_cases,
    names="Continent",
    values="TotalCases",
    hole=0.4,
    color_discrete_sequence=px.colors.qualitative.Set2
)
st.plotly_chart(fig, use_container_width=True)

# ======================
# Country-Specific Insights
# ======================
st.divider()
st.markdown("## 🌏 Country-Specific Insights")
st.info("Select a country to view detailed statistics, including total cases, deaths, recoveries, active cases, and mortality rate.")

selected_country = st.selectbox("Select a Country", covid_data["Country/Region"].unique())
country_data = covid_data[covid_data["Country/Region"] == selected_country]
        f"- **Total Recovered:** {country_data['TotalRecovered'].sum():,.0f}\n"
        f"- **Active Cases:** {country_data['ActiveCases'].sum():,.0f}\n"
        f"- **Mortality Rate:** {(country_data['TotalDeaths'].sum() / country_data['TotalCases'].sum() * 100):.2f}%"
    )
else:
    st.warning("No data available for the selected country.")

# ======================
# Testing Efficiency Analysis
# ======================
st.divider()
st.markdown("## 🧪 Testing Efficiency Analysis")
st.info("This scatter plot compares the number of tests conducted per million population with the number of cases per million population.")

st.markdown("### 🧮 Tests per Million vs Cases per Million")
fig = px.scatter(
    covid_data,
    x="Tot Cases/1M pop",
    y="Tests/1M pop",
    size="Population",
    color="Continent",
    hover_name="Country/Region",
    title="Tests per Million vs Cases per Million",
    template="plotly_white",
    labels={
        "Tot Cases/1M pop": "Cases per Million",
        "Tests/1M pop": "Tests per Million"
    }
)
st.plotly_chart(fig, use_container_width=True)

# ======================
# Recovery vs Death Rate Analysis
# ======================
st.divider()
st.markdown("## ❤️ Recovery vs Death Rate Analysis")
st.info(
    """
    This analysis provides insights into the relationship between recovery rates and death rates across different countries. 
    - **Recovery Rate (%)**: The percentage of total cases that have recovered.
    - **Death Rate (%)**: The percentage of total cases that resulted in fatalities.

    By analyzing this relationship, we can identify countries with high recovery rates and low death rates, which may indicate effective healthcare systems and pandemic management strategies. Conversely, countries with low recovery rates and high death rates may highlight areas requiring urgent attention.
    """
)

covid_data["RecoveryRate"] = (
    covid_data["TotalRecovered"] / covid_data["TotalCases"] * 100
).round(2)
covid_data["DeathRate"] = (
    covid_data["TotalDeaths"] / covid_data["TotalCases"] * 100
).round(2)

fig = px.scatter(
    covid_data,
    x="RecoveryRate",
    y="DeathRate",
    size="TotalCases",
    color="Continent",
    hover_name="Country/Region",
    title="Recovery Rate vs Death Rate by Country",
    template="plotly_white",
    labels={
        "RecoveryRate": "Recovery Rate (%)",
        "DeathRate": "Death Rate (%)"
    }
)
st.plotly_chart(fig, use_container_width=True)
