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
    uber_dashboard.py

dataset/               # Collection of datasets used in analyses
    covid.csv
    Customer_Churn.csv
    diwali_sales_data.csv
    gold_price_data.csv
    HousePricePrediction.xlsx
    iphone_sales.csv
    Iris.csv
    passanger_test_data.csv
    test.csv
    train.csv
    uber_data.csv
    zomato.csv

notebooks/             # Jupyter notebooks for data exploration
    covid_analysis.ipynb
    customer_churn.ipynb
    diwali_sales_analysis.ipynb
    gold_price_analysis.ipynb
    google_trends_analysis.ipynb
    iphone_sales_analysis.ipynb
    iris_analysis.ipynb
    real_state_Analysis.ipynb
    titanic_data_analysis.ipynb
    uber_analysis.ipynb
    zomato_analysis.ipynb
    [...existing content...]

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

## 🤝 Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements, new analyses, or bug fixes.

## 📄 License

This project is licensed under the MIT License.
