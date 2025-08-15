import streamlit as st
import pandas as pd
import plotly.express as px

# ======================
# Load Data
# ======================

def load_data():
    return pd.read_csv("dataset/diwali_sales_data.csv", encoding="cp1252")

diwali_data = load_data()

st.title("🪔Diwali Sales Dashboard")

st.divider()

st.markdown("#### Gender-wise Customer Distribution")

gender_count = diwali_data.aggregate("Gender").value_counts()

fig = px.bar(gender_count, color=['orange', 'cyan'])
st.plotly_chart(fig, use_container_width=True)

st.markdown("#### Sales distribution over Age group")
purchases_age_data = diwali_data.groupby("Age Group").aggregate('Amount').sum()
fig = px.bar(purchases_age_data, color=['red', 'blue', 'yellow', 'orange','green', 'black', 'gray'])
st.plotly_chart(fig, use_container_width=True)

st.markdown("#### Sales distribution over Gender")
male_female_purchases = diwali_data.groupby("Gender").aggregate("Amount").sum()
fig = px.bar(male_female_purchases, color=[ 'orange','green'])
st.plotly_chart(fig, use_container_width=True)

st.markdown("#### Sales distribution over Gender")
occupation_data = diwali_data.groupby("Occupation", as_index=False).aggregate("Amount").sum()
fig = px.bar( 
    occupation_data,
    x="Occupation",
    y="Amount",
    color="Occupation",  # This now works because it's a column
    title="Sales by Occupation",
    
)
fig.update_layout(showlegend=False, xaxis_tickangle=90)
st.plotly_chart(fig, use_container_width=True)

state_puchases = diwali_data.groupby("State", as_index=False).aggregate("Amount").max()
unique_bars = len(state_puchases)
fig = px.bar( 
    state_puchases,
    x="State",
    y="Amount",
    color="State",  # This now works because it's a column
    title="Sales by State"
)
st.plotly_chart(fig, use_container_width=True)
