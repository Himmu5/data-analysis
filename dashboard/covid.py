import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ======================
# Dashboard Configuration
# ======================
st.set_page_config(
    page_title="🦠 COVID-19 Analytics Dashboard", 
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🦠"
)

# Custom CSS for modern design
st.markdown(
    """
    <style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #2c3e50;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: white;
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Metric cards styling */
    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border-left: 5px solid #4ecdc4;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        text-align: center;
        margin-bottom: 1rem;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    .metric-card h3 {
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0 0 0.3rem 0;
        line-height: 1.1;
        color: #2c3e50;
        text-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    .metric-card h1 {
        font-size: 2rem;
        font-weight: 700;
        margin: 0.3rem 0;
        line-height: 1;
        color: #2c3e50;
        text-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    .metric-card p {
        font-size: 0.75rem;
        margin: 0;
        line-height: 1.2;
        color: #34495e;
        font-weight: 600;
        padding: 0 0.5rem;
        word-wrap: break-word;
        overflow-wrap: break-word;
        text-shadow: 0 1px 1px rgba(0,0,0,0.1);
    }
    
    /* Section headers */
    .section-header {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        padding: 1rem 2rem;
        border-radius: 10px;
        margin: 2rem 0 1rem 0;
        font-size: 1.5rem;
        font-weight: 600;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Chart containers */
    .js-plotly-plot {
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    /* Custom divider */
    .custom-divider {
        height: 3px;
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
        border-radius: 2px;
        margin: 2rem 0;
    }
    
    /* Improved spacing and layout */
    .stContainer {
        padding: 0.5rem;
    }
    
    /* Better column spacing */
    .stColumn {
        padding: 0.25rem;
    }
    
    /* Enhanced info boxes */
    .stInfo {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Loading spinner styling */
    .stSpinner {
        color: #667eea;
    }
    
    /* Success message styling */
    .stSuccess {
        background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
        color: white;
        border: none;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Modern header
st.markdown(
    """
    <div class="main-header">
        <h1>🦠 COVID-19 Analytics Dashboard</h1>
        <p>Comprehensive insights into the global impact of COVID-19 with advanced analytics and interactive visualizations</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ======================
# Sidebar Configuration
# ======================
st.sidebar.markdown("## 🎛️ Dashboard Controls")

# Data loading with progress indicator
@st.cache_data
def load_data():
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    status_text.text("🔄 Loading COVID-19 dataset...")
    progress_bar.progress(25)
    
    data = pd.read_csv("dataset/covid.csv", encoding="cp1252")
    progress_bar.progress(50)
    status_text.text("🔄 Processing data...")
    
    # Data preprocessing
    data = data.fillna(0)
    data['RecoveryRate'] = (data['TotalRecovered'] / data['TotalCases'] * 100).round(2)
    data['DeathRate'] = (data['TotalDeaths'] / data['TotalCases'] * 100).round(2)
    data['ActiveRate'] = (data['ActiveCases'] / data['TotalCases'] * 100).round(2)
    
    progress_bar.progress(100)
    status_text.text("✅ Data loaded successfully!")
    
    # Clear progress indicators
    progress_bar.empty()
    status_text.empty()
    
    return data

covid_data = load_data()
st.sidebar.success(f"📊 **{len(covid_data)}** countries loaded")

# Sidebar filters with improved UX
st.sidebar.markdown("### 🔍 Data Filters")

# Continent filter with better styling
st.sidebar.markdown("**🌍 Continents**")
selected_continents = st.sidebar.multiselect(
    "Select Continents",
    options=covid_data['Continent'].unique(),
    default=covid_data['Continent'].unique(),
    help="Choose which continents to include in the analysis"
)

# Population filter with better formatting
st.sidebar.markdown("**👥 Population Filter**")
min_population = st.sidebar.number_input(
    "Minimum Population (Millions)",
    min_value=0,
    max_value=int(covid_data['Population'].max() / 1e6),
    value=0,
    step=1,
    help="Filter countries by minimum population size"
)

# Cases filter with better formatting
st.sidebar.markdown("**🦠 Cases Filter**")
min_cases = st.sidebar.number_input(
    "Minimum Total Cases",
    min_value=0,
    max_value=int(covid_data['TotalCases'].max()),
    value=0,
    step=1000,
    help="Filter countries by minimum number of cases"
)

# Apply filters
filtered_data = covid_data[
    (covid_data['Continent'].isin(selected_continents)) &
    (covid_data['Population'] >= min_population * 1e6) &
    (covid_data['TotalCases'] >= min_cases)
]

st.sidebar.markdown(f"**Filtered Countries:** {len(filtered_data)}")

# Export options with better UX
st.sidebar.markdown("### 📊 Export Options")
st.sidebar.markdown("**💾 Data Export**")

if st.sidebar.button("📥 Download Filtered Data", help="Download the currently filtered dataset"):
    csv = filtered_data.to_csv(index=False)
    st.sidebar.download_button(
        label="📄 Download CSV",
        data=csv,
        file_name=f"covid_data_filtered_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        help="Download the filtered COVID-19 data as a CSV file"
    )

# Additional export options
st.sidebar.markdown("**📈 Quick Stats**")
st.sidebar.metric("Countries", len(filtered_data))
st.sidebar.metric("Continents", len(filtered_data['Continent'].unique()))
st.sidebar.metric("Total Cases", f"{filtered_data['TotalCases'].sum()/1e6:.1f}M")
st.sidebar.metric("Total Deaths", f"{filtered_data['TotalDeaths'].sum()/1e6:.1f}M")

# ======================
# Enhanced KPIs Section
# ======================
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">📊 Global COVID-19 Overview</div>', unsafe_allow_html=True)

# Calculate metrics for filtered data
total_cases = filtered_data['TotalCases'].sum()
total_deaths = filtered_data['TotalDeaths'].sum()
total_recovered = filtered_data["TotalRecovered"].sum()
total_active = filtered_data['ActiveCases'].sum()
total_tests = filtered_data['TotalTests'].sum()
total_population = filtered_data['Population'].sum()

# Calculate rates
global_death_rate = (total_deaths / total_cases * 100) if total_cases > 0 else 0
global_recovery_rate = (total_recovered / total_cases * 100) if total_cases > 0 else 0
global_active_rate = (total_active / total_cases * 100) if total_cases > 0 else 0

# Create enhanced metrics layout
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="metric-card" style="border-left-color: #e74c3c;">
            <h3 style="color: #e74c3c;">🌍 Total Cases</h3>
            <h1 style="color: #2c3e50;">{total_cases/1e6:.2f}M</h1>
            <p style="color: #34495e;">Confirmed worldwide</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-card" style="border-left-color: #27ae60;">
            <h3 style="color: #27ae60;">❤️ Total Recovered</h3>
            <h1 style="color: #2c3e50;">{total_recovered/1e6:.2f}M</h1>
            <p style="color: #34495e;">Rate: {global_recovery_rate:.1f}%</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="metric-card" style="border-left-color: #e67e22;">
            <h3 style="color: #e67e22;">☠️ Total Deaths</h3>
            <h1 style="color: #2c3e50;">{total_deaths/1e6:.2f}M</h1>
            <p style="color: #34495e;">Rate: {global_death_rate:.1f}%</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="metric-card" style="border-left-color: #9b59b6;">
            <h3 style="color: #9b59b6;">🧪 Total Tests</h3>
            <h1 style="color: #2c3e50;">{total_tests/1e6:.2f}M</h1>
            <p style="color: #34495e;">Tests conducted</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Additional metrics row - using same card styling for symmetry
col5, col6, col7, col8 = st.columns(4)

with col5:
    st.markdown(
        f"""
        <div class="metric-card" style="border-left-color: #3498db;">
            <h3 style="color: #3498db;">🏥 Active Cases</h3>
            <h1 style="color: #2c3e50;">{total_active/1e6:.2f}M</h1>
            <p style="color: #34495e;">{global_active_rate:.1f}% of total</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col6:
    st.markdown(
        f"""
        <div class="metric-card" style="border-left-color: #8e44ad;">
            <h3 style="color: #8e44ad;">👥 Population</h3>
            <h1 style="color: #2c3e50;">{total_population/1e6:.0f}M</h1>
            <p style="color: #34495e;">Total analyzed</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col7:
    cases_per_million = (total_cases / total_population * 1e6) if total_population > 0 else 0
    st.markdown(
        f"""
        <div class="metric-card" style="border-left-color: #f39c12;">
            <h3 style="color: #f39c12;">📈 Cases/Million</h3>
            <h1 style="color: #2c3e50;">{cases_per_million:.0f}</h1>
            <p style="color: #34495e;">Per capita rate</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col8:
    tests_per_million = (total_tests / total_population * 1e6) if total_population > 0 else 0
    st.markdown(
        f"""
        <div class="metric-card" style="border-left-color: #1abc9c;">
            <h3 style="color: #1abc9c;">🔬 Tests/Million</h3>
            <h1 style="color: #2c3e50;">{tests_per_million:.0f}</h1>
            <p style="color: #34495e;">Testing intensity</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ======================
# Enhanced Global Insights
# ======================
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">🌍 Global Insights & Trends</div>', unsafe_allow_html=True)

# Top performers analysis
colA, colB = st.columns(2)

with colA:
    st.markdown("### 🏆 Top 10 Countries by COVID-19 Deaths")
    top10_deaths_country = (
        filtered_data.groupby("Country/Region")["TotalDeaths"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    
    fig = px.bar(
        top10_deaths_country,
        x="TotalDeaths",
        y="Country/Region",
        orientation='h',
        color="TotalDeaths",
        color_continuous_scale="Reds",
        template="plotly_white",
        title="Countries with Highest COVID-19 Deaths",
        labels={"TotalDeaths": "Total Deaths", "Country/Region": "Country"}
    )
    fig.update_layout(
        height=500,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)

with colB:
    st.markdown("### 📊 Top 10 Countries by Recovery Rate")
    recovery_data = filtered_data[filtered_data['TotalCases'] > 10000]  # Filter for meaningful data
    top_recovery = (
        recovery_data.groupby("Country/Region")
        .agg({
            'TotalRecovered': 'sum',
            'TotalCases': 'sum',
            'RecoveryRate': 'mean'
        })
        .reset_index()
    )
    top_recovery = top_recovery.sort_values('RecoveryRate', ascending=False).head(10)
    
    fig = px.bar(
        top_recovery,
        x="RecoveryRate",
        y="Country/Region",
        orientation='h',
        color="RecoveryRate",
        color_continuous_scale="Greens",
        template="plotly_white",
        title="Countries with Highest Recovery Rates",
        labels={"RecoveryRate": "Recovery Rate (%)", "Country/Region": "Country"}
    )
    fig.update_layout(
        height=500,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)

# Correlation analysis
st.markdown("### 📈 Correlation Analysis of COVID-19 Metrics")
corr_data = filtered_data[["TotalCases", "TotalDeaths", "TotalRecovered", "ActiveCases", "TotalTests", "Population"]].corr()

fig = px.imshow(
    corr_data,
    text_auto=True,
    aspect="auto",
    color_continuous_scale="RdBu",
    title="Correlation Matrix of COVID-19 Metrics"
)
fig.update_layout(
    height=500,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig, use_container_width=True)

# ======================
# Enhanced Geographic Distribution
# ======================
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">🗺️ Geographic Distribution & Mapping</div>', unsafe_allow_html=True)

# Map visualization options
map_metric = st.selectbox(
    "Select Metric for Map Visualization",
    ["Tot Cases/1M pop", "Deaths/1M pop", "Tests/1M pop", "RecoveryRate", "DeathRate"],
    index=0
)

metric_labels = {
    "Tot Cases/1M pop": "Cases per Million Population",
    "Deaths/1M pop": "Deaths per Million Population", 
    "Tests/1M pop": "Tests per Million Population",
    "RecoveryRate": "Recovery Rate (%)",
    "DeathRate": "Death Rate (%)"
}

st.markdown(f"### 🌍 {metric_labels[map_metric]} - Global Distribution")

fig = px.choropleth(
    filtered_data,
    locations="iso_alpha",
    color=map_metric,
    hover_name="Country/Region",
    hover_data=["TotalCases", "TotalDeaths", "TotalRecovered", "Population"],
    color_continuous_scale="Reds" if "Death" in map_metric else "Viridis",
    template="plotly_white",
    title=f"Global Distribution of {metric_labels[map_metric]}",
    labels={map_metric: metric_labels[map_metric]}
)
fig.update_layout(
    height=600,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig, use_container_width=True)

# ======================
# Enhanced Continent Insights
# ======================
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">🌎 Continental Analysis</div>', unsafe_allow_html=True)

colC, colD = st.columns(2)

with colC:
    st.markdown("### 🦠 Continent-wise COVID-19 Cases Distribution")
    continent_cases = filtered_data.groupby("Continent").agg({
        'TotalCases': 'sum',
        'TotalDeaths': 'sum',
        'TotalRecovered': 'sum',
        'Population': 'sum'
    }).reset_index()
    
    fig = px.pie(
        continent_cases,
        names="Continent",
        values="TotalCases",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set2,
        title="Distribution of COVID-19 Cases by Continent"
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)

with colD:
    st.markdown("### 📊 Continent-wise Performance Metrics")
    continent_metrics = filtered_data.groupby("Continent").agg({
        'TotalCases': 'sum',
        'TotalDeaths': 'sum',
        'TotalRecovered': 'sum',
        'Population': 'sum'
    }).reset_index()
    
    continent_metrics['DeathRate'] = (continent_metrics['TotalDeaths'] / continent_metrics['TotalCases'] * 100).round(2)
    continent_metrics['RecoveryRate'] = (continent_metrics['TotalRecovered'] / continent_metrics['TotalCases'] * 100).round(2)
    continent_metrics['CasesPerMillion'] = (continent_metrics['TotalCases'] / continent_metrics['Population'] * 1e6).round(0)
    
    fig = px.bar(
        continent_metrics,
        x="Continent",
        y=["DeathRate", "RecoveryRate"],
        title="Death Rate vs Recovery Rate by Continent",
        barmode="group",
        color_discrete_sequence=["#e74c3c", "#27ae60"]
    )
    fig.update_layout(
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        yaxis_title="Rate (%)"
    )
    st.plotly_chart(fig, use_container_width=True)

# Continent comparison table
st.markdown("### 📋 Continental Comparison Table")
continent_summary = continent_metrics.copy()
continent_summary = continent_summary.sort_values('TotalCases', ascending=False)
continent_summary['TotalCases'] = continent_summary['TotalCases'].apply(lambda x: f"{x/1e6:.2f}M")
continent_summary['TotalDeaths'] = continent_summary['TotalDeaths'].apply(lambda x: f"{x/1e3:.1f}K")
continent_summary['TotalRecovered'] = continent_summary['TotalRecovered'].apply(lambda x: f"{x/1e6:.2f}M")
continent_summary['Population'] = continent_summary['Population'].apply(lambda x: f"{x/1e6:.0f}M")

st.dataframe(
    continent_summary[['Continent', 'TotalCases', 'TotalDeaths', 'TotalRecovered', 'DeathRate', 'RecoveryRate', 'CasesPerMillion']],
    use_container_width=True,
    hide_index=True
)

# ======================
# Enhanced Country-Specific Insights
# ======================
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">🌏 Country-Specific Analysis</div>', unsafe_allow_html=True)

# Country selection and comparison
colE, colF = st.columns([2, 1])

with colE:
    selected_countries = st.multiselect(
        "Select Countries for Comparison",
        options=filtered_data["Country/Region"].unique(),
        default=[filtered_data["Country/Region"].iloc[0]] if len(filtered_data) > 0 else []
    )

with colF:
    comparison_metric = st.selectbox(
        "Comparison Metric",
        ["TotalCases", "TotalDeaths", "TotalRecovered", "RecoveryRate", "DeathRate", "Tests/1M pop"],
        index=0
    )

if selected_countries:
    country_data = filtered_data[filtered_data["Country/Region"].isin(selected_countries)]
    
    # Country comparison chart
    st.markdown("### 📊 Country Comparison")
    fig = px.bar(
        country_data,
        x="Country/Region",
        y=comparison_metric,
        color="Country/Region",
        title=f"Comparison of {comparison_metric} by Country",
        template="plotly_white"
    )
    fig.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed country statistics
    st.markdown("### 📋 Detailed Country Statistics")
    country_stats = country_data.groupby("Country/Region").agg({
        'TotalCases': 'sum',
        'TotalDeaths': 'sum',
        'TotalRecovered': 'sum',
        'ActiveCases': 'sum',
        'TotalTests': 'sum',
        'Population': 'sum',
        'RecoveryRate': 'mean',
        'DeathRate': 'mean'
    }).reset_index()
    
    country_stats['MortalityRate'] = (country_stats['TotalDeaths'] / country_stats['TotalCases'] * 100).round(2)
    country_stats['ActiveRate'] = (country_stats['ActiveCases'] / country_stats['TotalCases'] * 100).round(2)
    
    # Format numbers for display
    display_stats = country_stats.copy()
    display_stats['TotalCases'] = display_stats['TotalCases'].apply(lambda x: f"{x:,.0f}")
    display_stats['TotalDeaths'] = display_stats['TotalDeaths'].apply(lambda x: f"{x:,.0f}")
    display_stats['TotalRecovered'] = display_stats['TotalRecovered'].apply(lambda x: f"{x:,.0f}")
    display_stats['ActiveCases'] = display_stats['ActiveCases'].apply(lambda x: f"{x:,.0f}")
    display_stats['TotalTests'] = display_stats['TotalTests'].apply(lambda x: f"{x:,.0f}")
    display_stats['Population'] = display_stats['Population'].apply(lambda x: f"{x:,.0f}")
    
    st.dataframe(
        display_stats,
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("Please select at least one country to view detailed analysis.")

# ======================
# Enhanced Testing Efficiency Analysis
# ======================
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">🧪 Testing Efficiency & Healthcare Analysis</div>', unsafe_allow_html=True)

colG, colH = st.columns(2)

with colG:
    st.markdown("### 🧮 Testing vs Cases Analysis")
    testing_data = filtered_data[filtered_data['Tests/1M pop'] > 0]  # Filter countries with testing data
    
    fig = px.scatter(
        testing_data,
        x="Tot Cases/1M pop",
        y="Tests/1M pop",
        size="Population",
        color="Continent",
        hover_name="Country/Region",
        hover_data=["TotalCases", "TotalTests", "RecoveryRate", "DeathRate"],
        title="Testing Intensity vs Case Rate",
        template="plotly_white",
        labels={
            "Tot Cases/1M pop": "Cases per Million Population",
            "Tests/1M pop": "Tests per Million Population"
        }
    )
    fig.update_layout(
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)

with colH:
    st.markdown("### 🏥 Healthcare System Performance")
    healthcare_data = filtered_data[filtered_data['TotalCases'] > 1000]  # Filter for meaningful data
    
    fig = px.scatter(
        healthcare_data,
        x="RecoveryRate",
        y="DeathRate",
        size="TotalCases",
        color="Continent",
        hover_name="Country/Region",
        hover_data=["TotalCases", "TotalDeaths", "TotalRecovered", "Tests/1M pop"],
        title="Recovery Rate vs Death Rate",
        template="plotly_white",
        labels={
            "RecoveryRate": "Recovery Rate (%)",
            "DeathRate": "Death Rate (%)"
        }
    )
    fig.update_layout(
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)

# Testing efficiency insights
st.markdown("### 📈 Testing Efficiency Insights")
testing_insights = filtered_data[filtered_data['Tests/1M pop'] > 0].copy()
testing_insights['TestEfficiency'] = (testing_insights['TotalCases'] / testing_insights['TotalTests'] * 100).round(2)

# Top and bottom performers
colI, colJ = st.columns(2)

with colI:
    st.markdown("#### 🏆 Most Efficient Testing (Lowest Cases/Test Ratio)")
    efficient_testing = testing_insights.nsmallest(10, 'TestEfficiency')[['Country/Region', 'TestEfficiency', 'Tests/1M pop', 'Tot Cases/1M pop']]
    st.dataframe(efficient_testing, use_container_width=True, hide_index=True)

with colJ:
    st.markdown("#### ⚠️ Least Efficient Testing (Highest Cases/Test Ratio)")
    inefficient_testing = testing_insights.nlargest(10, 'TestEfficiency')[['Country/Region', 'TestEfficiency', 'Tests/1M pop', 'Tot Cases/1M pop']]
    st.dataframe(inefficient_testing, use_container_width=True, hide_index=True)

# ======================
# Advanced Analytics & Insights
# ======================
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">📊 Advanced Analytics & Insights</div>', unsafe_allow_html=True)

# Statistical insights
st.markdown("### 📈 Statistical Summary")
colK, colL, colM = st.columns(3)

with colK:
    st.metric("📊 Countries Analyzed", len(filtered_data))
    st.metric("🌍 Continents Covered", len(filtered_data['Continent'].unique()))

with colL:
    avg_recovery_rate = filtered_data['RecoveryRate'].mean()
    avg_death_rate = filtered_data['DeathRate'].mean()
    st.metric("📈 Average Recovery Rate", f"{avg_recovery_rate:.1f}%")
    st.metric("📉 Average Death Rate", f"{avg_death_rate:.1f}%")

with colM:
    total_population_analyzed = filtered_data['Population'].sum()
    global_coverage = (total_population_analyzed / covid_data['Population'].sum() * 100)
    st.metric("👥 Population Coverage", f"{global_coverage:.1f}%")
    st.metric("🧪 Countries with Testing Data", len(filtered_data[filtered_data['Tests/1M pop'] > 0]))

# Key insights
st.markdown("### 🔍 Key Insights")
insights_col1, insights_col2 = st.columns(2)

with insights_col1:
    st.markdown("""
    #### 🏆 **Top Performers**
    - **Highest Recovery Rate**: Countries with best healthcare outcomes
    - **Most Efficient Testing**: Countries with optimal testing strategies
    - **Lowest Death Rate**: Countries with effective pandemic management
    """)

with insights_col2:
    st.markdown("""
    #### ⚠️ **Areas of Concern**
    - **High Death Rates**: Countries needing urgent healthcare support
    - **Low Testing Rates**: Countries with limited testing capacity
    - **Low Recovery Rates**: Countries with healthcare system challenges
    """)

# Footer
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align: center; padding: 2rem; background: linear-gradient(90deg, #667eea, #764ba2); border-radius: 15px; color: white;">
        <h3>🦠 COVID-19 Analytics Dashboard</h3>
        <p>Built with Streamlit • Data-driven insights for pandemic analysis</p>
        <p><em>Last updated: {}</em></p>
    </div>
    """.format(datetime.now().strftime("%B %d, %Y")),
    unsafe_allow_html=True
)
