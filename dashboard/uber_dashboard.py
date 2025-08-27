import streamlit as st
import pandas as pd
import plotly.express as px
import calendar

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

vehicle_data = uber_data.aggregate("Vehicle Type").value_counts().reset_index().sort_values(by="count", ascending=False)
st.markdown("###### Number of bookings per vehicle type")
fig = px.bar(vehicle_data, x="Vehicle Type", y="count", color="Vehicle Type")
st.plotly_chart(fig, use_container_width=True)


def set_ride_status(booking_status):
    if booking_status == "Completed":
        return "Completed";
    return "Cancelled"

uber_data['ride status'] = uber_data['Booking Status'].apply(set_ride_status)
vehicle_booking_distribution = uber_data.groupby("Vehicle Type").aggregate("ride status").value_counts().reset_index()
st.markdown("###### Vehicle type vs Booking Status (e.g., how many Auto rides completed vs cancelled)")
fig = px.bar(vehicle_booking_distribution, x="Vehicle Type", y="count", color="ride status", barmode='stack',color_discrete_map={
        "Cancelled": "#6D600D",  # Navy Blue
        "Completed": "#f2a104"   # Gold/Amber
    })
st.plotly_chart(fig, use_container_width=True)

st.markdown("### ⏰ Time & Trend Analysis")
st.markdown("#### Rides per month (trend of bookings over time)")

uber_data["Date"] = pd.to_datetime(uber_data["Date"], errors="coerce")
# Group by month
monthly_rides = (
    uber_data.groupby(uber_data["Date"].dt.month)["Booking ID"]
    .count()
    .reset_index(name="Ride Count")
    .rename(columns={"Date": "Month"})
)

# Convert month number → month name
monthly_rides["Month"] = monthly_rides["Month"].apply(lambda x: calendar.month_name[x])

# Ensure months are ordered Jan → Dec
month_order = list(calendar.month_name)[1:]  # ['January', 'February', ...]
monthly_rides["Month"] = pd.Categorical(monthly_rides["Month"], categories=month_order, ordered=True)
monthly_rides = monthly_rides.sort_values("Month")

# Plot
fig = px.line(monthly_rides, x="Month", y="Ride Count", markers=True)
st.plotly_chart(fig, use_container_width=True)


st.markdown("#### Monthly ride revenue")
monthly_revenue = (
    uber_data.groupby(uber_data["Date"].dt.month)["Booking Value"]
    .sum()
    .reset_index(name="Revenue")
)
monthly_revenue['month'] = monthly_revenue['Date'].apply(
    lambda x: pd.to_datetime(f"2000-{x}-01").strftime("%B")
)
fig = px.bar(monthly_revenue, x="month", y='Revenue', color="month")
st.plotly_chart(fig, use_container_width=True)


st.markdown("### 👤 Customer & Driver Insights")
st.markdown("#### Top 10 customers by number of bookings")
top_10_customer = uber_data.aggregate("Customer ID").value_counts().reset_index().head(10)
fig = px.bar(top_10_customer, x='count', y='Customer ID', orientation='h', color="Customer ID")
st.plotly_chart(fig, use_container_width=True)

