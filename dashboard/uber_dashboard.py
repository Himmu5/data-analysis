import streamlit as st
import pandas as pd
import plotly.express as px

# ======================
# Load Data
# ======================
@st.cache_data
def load_data():
    return pd.read_csv("dataset/uber_data.csv", encoding="cp1252")

uber_data = load_data()

st.set_page_config(page_title="Uber Dashboard", layout="wide")
st.title("🚖 Uber Ride Insights: Trends & Patterns")
st.markdown("An in-depth look at customer behavior, ride trends, and booking outcomes.")
st.divider()

total_rides = uber_data['Booking ID'].count()
total_customers = len(uber_data['Customer ID'].value_counts().values)
total_booking_value = uber_data['Booking Value'].sum()
completed_rides = (uber_data['Booking Status'].str.strip() == "Completed").sum()
cancelled_rides = (uber_data['Booking Status'].str.strip() == "Cancelled").sum() 
avg_booking_value = round(uber_data['Booking Value'].mean(), 2)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("🚖 Total Rides", f"{total_rides:,}")
col2.metric("👥 Unique Customers", f"{total_customers:,}")
col4.metric("✅ Completed Rides", f"{completed_rides:,}") 
col3.metric("📊 Avg Booking Value", f"₹{avg_booking_value}")
col5.metric("💰 Total Booking Value", f"₹{total_booking_value:,.0f}")


booking_data = uber_data.aggregate("Booking Status").value_counts().reset_index()
st.markdown("#### 📊 Booking & Status Overview")
st.markdown("###### Booking Status distribution (Completed, Incomplete, Cancelled, No Driver Found)")
fig = px.pie(booking_data, names="Booking Status", values="count", color="Booking Status")
st.plotly_chart(fig, use_container_width=True)

# st.markdown("###### Booking Status distribution (Completed, Incomplete, Cancelled, No Driver Found)")
# fig = px.pie(booking_data, names="Booking Status", values="count", color="Booking Status")
# st.plotly_chart(fig, use_container_width=True)