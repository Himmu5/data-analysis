# Data Analysis Projects

Welcome to the Data Analysis repository! This project contains various data analysis scripts, dashboards, and Jupyter notebooks for exploring and visualizing multiple datasets.

## 📁 Folder Structure

```
main.py                # Entry point for running analyses
pyproject.toml         # Project configuration
uv.lock                # Python dependencies lock file
README.md              # Project documentation

dashboard/             # Python scripts for interactive dashboards
    covid.py
    diwali_sales.py
    iphone_sales_dashboard.py
    spotify_dashboard.py
    uber_dashboard.py
    walmart_sql_dashboard.py
    zomato.py

dataset/               # Collection of datasets used in analyses
    auth_logs.csv
    covid.csv
    Customer_Churn.csv
    diwali_sales_data.csv
    firewall_logs.csv
    gold_price_data.csv
    HousePricePrediction.xlsx
    iphone_sales.csv
    Iris.csv
    netflix_titles.csv
    passanger_test_data.csv
    retail_data.csv
    spotify_data.csv
    test.csv
    train.csv
    uber_data.csv
    Walmart.csv
    web_logs.csv
    zomato.csv

notebooks/             # Jupyter notebooks for data exploration
    covid_analysis.ipynb
    customer_churn.ipynb
    cyber_analysis.ipynb
    diwali_sales_analysis.ipynb
    gold_price_analysis.ipynb
    google_trends_analysis.ipynb
    iphone_sales_analysis.ipynb
    iris_analysis.ipynb
    netflix_analysis.ipynb
    real_state_Analysis.ipynb
    retail_sale_analysis.ipynb
    spotify_analysis.ipynb
    titanic_data_analysis.ipynb
    uber_analysis.ipynb
    walmart_analysis.ipynb
    zomato_analysis.ipynb

project/               # Additional project scripts
    main.py
    pyproject.toml
    README.md
    scrapper.py

sql/                   # SQL scripts for data analysis
    retail_analysis.sql
```

## 🚀 Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Himmu5/data-analysis.git
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   # or use poetry if pyproject.toml is configured
   poetry install
   ```

## 📊 How to Run Analyses

- **Dashboards:**
  - Navigate to the `dashboard/` folder and run the desired script, e.g.:
    ```bash
    python dashboard/covid.py
    ```

All datasets used for analysis are stored in the `dataset/` folder. Each notebook or dashboard script specifies which dataset it uses.

## 📝 Notebooks Overview

- COVID-19 Data Analysis
- Customer Churn Prediction
- Titanic Survival Analysis
- Uber Data Insights
- Zomato Restaurant Analysis
- Spotify Data Analysis
- Walmart Sales Analysis
- Netflix Titles Exploration
- Gold Price Trends
- Iris Flower Classification
- Retail Sales Insights
- Cybersecurity Log Analysis
- Diwali Sales Insights
- Real Estate Market Analysis
- Google Trends Analysis

## 🛒 Walmart SQL Dashboard

A new interactive dashboard for Walmart sales analysis is now available, built using Streamlit, Plotly, and MySQL for fast, flexible SQL-powered analytics.

**How to Run:**
- Ensure your MySQL database is set up and credentials are configured in `.streamlit/secrets.toml`.
- Launch the dashboard with:
    ```bash
    python dashboard/walmart_sql_dashboard.py
    ```
- The dashboard provides:
    - Revenue and profit KPIs
    - Top branches and cities
    - Product category insights
    - Payment method analysis
    - High-value transactions and profitability trends

See [dashboard/walmart_sql_dashboard.py](dashboard/walmart_sql_dashboard.py) for implementation details.

## 🤝 Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements, new analyses, or bug fixes.

## 📄 License

This project is licensed under the MIT License.
