import streamlit as st
import pandas as pd
import plotly.express as px

# ======================
# Load Data
# ======================
@st.cache_data
def load_data():
    return pd.read_csv("dataset/zomato.csv", encoding="latin")

zomato_data = load_data()

st.set_page_config(
    page_title="🍽️ Zomato Data Analysis",
    page_icon="🍱",
    layout="wide"
)

st.title("🍱 Zomato Data Analysis Dashboard")
st.markdown("Explore insights about restaurants, cuisines, and ratings around the world 🌍")
st.divider()

st.subheader("📊 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Restaurants", f"{zomato_data['Restaurant ID'].nunique():,}")
col2.metric("Cities", f"{zomato_data['City'].nunique():,}")
col3.metric("Countries", f"{zomato_data['Country Code'].nunique():,}")
col4.metric("Cuisines", f"{zomato_data['Cuisines'].nunique():,}")

st.divider()

st.markdown("#### Top Cities with Most Restaurants")
top_5_city_restaurant = zomato_data.groupby('City')['Restaurant ID'].count().reset_index(name="count").sort_values(ascending=False, by='count').head()
st.markdown("New Delhi hosts the largest number of restaurants on Zomato, making it the top city by restaurant availability.")
fig = px.bar(data_frame=top_5_city_restaurant,x='City', y='count', color="City")
st.plotly_chart(fig, use_container_width=True)


st.markdown("#### Count of restaurants by cuisine (top 10 cuisines)")
st.markdown("North Indian cuisine is the most widely offered cuisine across restaurants on Zomato.")
top_5_cuisines = zomato_data['Cuisines'].str.split(",").explode().str.strip().value_counts().reset_index().head(10)
fig = px.bar(data_frame=top_5_cuisines, x='count', y='Cuisines', orientation='h', color="Cuisines", height=600)
st.plotly_chart(fig, use_container_width=True)


def add_rating(rate):
    if rate >= 4.5:
        return "Excellent";
    elif rate >= 4:
        return "Very Good"
    elif rate >= 3:
        return "Good"
    else:
        return "Bad"
st.markdown("#### Distribution of restaurant ratings (Excellent, Very Good, Good, Poor, etc.)")
st.markdown("The majority of restaurants fall under ‘Good’, with many rated ‘Bad’, and only a few reaching ‘Very Good’ or ‘Excellent’.")
zomato_data['rating'] = zomato_data['Aggregate rating'].apply(add_rating)
rating_distribution = zomato_data['rating'].value_counts().reset_index().head() 
fig = px.pie(rating_distribution,names="rating", values="count", labels='rating')
st.plotly_chart(fig, use_container_width=True)