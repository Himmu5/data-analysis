import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config("Spotify Dashboard", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
        /* Title Styling */
        .spotify-title {
            font-size: 36px !important;
            font-weight: bold !important;
            color: #1DB954; /* Spotify green */
            text-align: center;
            margin-bottom: 0.2em;
        }
        .spotify-caption {
            font-size: 18px !important;
            color: #666;
            text-align: center;
            margin-bottom: 2em;
        }

        /* Metric Card Styling */
        [data-testid="stMetric"] {
            background-color: #121212;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            color: #fff;
        }
        [data-testid="stMetric"] div {
            color: #fff !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

def load_data():
    try:
        username = st.secrets["secrets"]['username'] 
        password = st.secrets["secrets"]["password"]
        host = st.secrets["secrets"]["host"]
        port = st.secrets["secrets"]["port"]
        database = st.secrets["secrets"]["database"]
        url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
        return create_engine(url)
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None

conn = load_data()

if conn:
    st.markdown('<h1 class="spotify-title">Spotify Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="spotify-caption">Interactive overview of Spotify data.</p>', unsafe_allow_html=True)

    # Load data from the database
    @st.cache_data
    def fetch_data(query):
        try:
            return pd.read_sql(query, conn)
        except Exception as e:
            st.error(f"Error fetching data: {e}")
            return pd.DataFrame()

    # Example queries
    total_singers_query = "SELECT COUNT(DISTINCT artist) AS total_singers FROM spotify;" 
    top_songs_query = "SELECT COUNT(DISTINCT Track) as total_song from spotify;"
    total_album_query = "SELECT COUNT(DISTINCT Album) as total_album from spotify;"
    total_singers = fetch_data(total_singers_query)
    total_album = fetch_data(total_album_query)
    top_songs = fetch_data(top_songs_query)

    # Display metrics with style
    col1, col2, col3 = st.columns(3)
    col1.metric("🎤 Total Singers", total_singers['total_singers'][0] if not total_singers.empty else "N/A")
    col2.metric("🎵 Total Songs", f"{top_songs['total_song'][0]}")
    col3.metric("💿 Total Albums", f"{total_album['total_album'][0]}") 

    # Top 5 artists by total streams
    top_5_artist = fetch_data(
        """
        SELECT Artist, COUNT(Stream) AS total_stream
        FROM spotify
        GROUP BY Artist
        ORDER BY total_stream DESC
        LIMIT 5;
        """
    )

    # Improved Spotify-themed bar plot using Plotly
    if not top_5_artist.empty:
        st.subheader("🎧 Top 5 Artists by Total Streams")
        fig = px.bar(
            top_5_artist,
            x='Artist',
            y='total_stream',
            title="Top 5 Artists by Total Streams",
            labels={'total_stream': 'Total Streams', 'Artist': 'Artist'},
            color_discrete_sequence=["#1DB954"]
        )
        fig.update_layout(
            plot_bgcolor="#121212",
            paper_bgcolor="#121212",
            font_color="white",
            title_font=dict(size=18, color="#1DB954", family="Arial"),
            xaxis=dict(title_font=dict(size=12, color="white")),
            yaxis=dict(title_font=dict(size=12, color="white"))
        )
        st.plotly_chart(fig, use_container_width=True)

    # Query for albums with highest average danceability
    danceability_query = """
    SELECT Album, AVG(Danceability) AS avg_danceability
    FROM spotify
    GROUP BY Album
    ORDER BY avg_danceability DESC
    LIMIT 10;
    """
    danceability_data = fetch_data(danceability_query)

    # Query for average loudness variation across artists
    loudness_query = """
    SELECT Artist, AVG(Loudness) AS avg_loudness
    FROM spotify
    GROUP BY Artist
    ORDER BY avg_loudness DESC;
    """
    loudness_data = fetch_data(loudness_query)

    # Query for consistency in loudness and tempo
    consistency_query = """
    SELECT Artist, STDDEV(Loudness) AS loudness_stddev, STDDEV(Tempo) AS tempo_stddev
    FROM spotify
    GROUP BY Artist
    ORDER BY loudness_stddev ASC, tempo_stddev ASC
    LIMIT 10;
    """
    consistency_data = fetch_data(consistency_query)

    # Query for artists with highest engagement
    engagement_query = """
    SELECT Artist, AVG(Likes/Views) AS engagement_ratio
    FROM spotify
    GROUP BY Artist
    ORDER BY engagement_ratio DESC
    LIMIT 10;
    """
    engagement_data = fetch_data(engagement_query)

    # Query for likes, views, and comments growth across album types
    growth_query = """
    SELECT Album_type, AVG(Likes) AS avg_likes, AVG(Views) AS avg_views, AVG(Comments) AS avg_comments
    FROM spotify
    GROUP BY Album_type;
    """
    growth_data = fetch_data(growth_query)

    # Query for artists dominating both Spotify and YouTube
    dominance_query = """
    SELECT Artist, SUM(Stream) AS total_spotify_streams, SUM(Views) AS total_youtube_views
    FROM spotify
    GROUP BY Artist
    HAVING total_spotify_streams > 1000000 AND total_youtube_views > 1000000
    ORDER BY total_spotify_streams DESC, total_youtube_views DESC;
    """
    dominance_data = fetch_data(dominance_query)

    # Query for artists with the largest gap between views and streams
    gap_query = """
    SELECT Artist, AVG(Views - Stream) AS avg_gap
    FROM spotify
    GROUP BY Artist
    ORDER BY avg_gap DESC
    LIMIT 10;
    """
    gap_data = fetch_data(gap_query)

    # Query for track popularity distribution across official vs non-official releases
    popularity_query = """
    SELECT official_video, COUNT(*) AS track_count, AVG(Likes) AS avg_likes
    FROM spotify
    GROUP BY official_video;
    """
    popularity_data = fetch_data(popularity_query)

    # Query for artists with the highest variance in tempo
    tempo_variance_query = """
    SELECT Artist, VARIANCE(Tempo) AS tempo_variance
    FROM spotify
    GROUP BY Artist
    ORDER BY tempo_variance DESC
    LIMIT 10;
    """
    tempo_variance_data = fetch_data(tempo_variance_query)

    # Display albums with highest average danceability
    if not danceability_data.empty:
        st.subheader("🎶 Albums with Highest Average Danceability")
        fig = px.bar(danceability_data, x='Album', y='avg_danceability',
                     title="Top 10 Albums by Average Danceability",
                     labels={'avg_danceability': 'Average Danceability', 'Album': 'Album'},
                     color_discrete_sequence=["#1DB954"])
        st.plotly_chart(fig, use_container_width=True)

    # Display average loudness variation across artists
    if not loudness_data.empty:
        st.subheader("🔊 Average Loudness Across Artists")
        fig = px.bar(loudness_data, x='Artist', y='avg_loudness',
                     title="Average Loudness by Artist",
                     labels={'avg_loudness': 'Average Loudness', 'Artist': 'Artist'},
                     color_discrete_sequence=["#1DB954"])
        st.plotly_chart(fig, use_container_width=True)

    # Display most consistent artists in loudness and tempo
    if not consistency_data.empty:
        st.subheader("🎵 Most Consistent Artists in Loudness and Tempo")
        st.dataframe(consistency_data, use_container_width=True)

    # Display artists with highest engagement
    if not engagement_data.empty:
        st.subheader("🔥 Artists with Highest Engagement")
        fig = px.bar(engagement_data, x='Artist', y='engagement_ratio',
                     title="Top 10 Artists by Engagement Ratio",
                     labels={'engagement_ratio': 'Engagement Ratio', 'Artist': 'Artist'},
                     color_discrete_sequence=["#1DB954"])
        st.plotly_chart(fig, use_container_width=True)

    # Display likes, views, and comments growth across album types
    if not growth_data.empty:
        st.subheader("📈 Growth Comparison Across Album Types")
        fig = px.bar(growth_data, x='Album_type', y=['avg_likes', 'avg_views', 'avg_comments'],
                     title="Likes, Views, and Comments Growth by Album Type",
                     labels={'value': 'Average Count', 'Album_type': 'Album Type'},
                     barmode='group', color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig, use_container_width=True)

    # Display artists dominating both Spotify and YouTube
    if not dominance_data.empty:
        st.subheader("🌟 Artists Dominating Both Spotify and YouTube")
        st.dataframe(dominance_data, use_container_width=True)

    # Display artists with the largest gap between views and streams
    if not gap_data.empty:
        st.subheader("📊 Artists with the Largest Gap Between Views and Streams")
        fig = px.bar(gap_data, x='Artist', y='avg_gap',
                     title="Top 10 Artists by View-Stream Gap",
                     labels={'avg_gap': 'Average Gap', 'Artist': 'Artist'},
                     color_discrete_sequence=["#1DB954"])
        st.plotly_chart(fig, use_container_width=True)

    # Display track popularity distribution across official vs non-official releases
    if not popularity_data.empty:
        st.subheader("🎵 Track Popularity Distribution")
        fig = px.pie(popularity_data, names='official_video', values='track_count',
                     title="Track Distribution by Release Type",
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)

    # Display artists with the highest variance in tempo
    if not tempo_variance_data.empty:
        st.subheader("🎶 Artists with the Highest Variance in Tempo")
        fig = px.bar(tempo_variance_data, x='Artist', y='tempo_variance',
                     title="Top 10 Artists by Tempo Variance",
                     labels={'tempo_variance': 'Tempo Variance', 'Artist': 'Artist'},
                     color_discrete_sequence=["#1DB954"])
        st.plotly_chart(fig, use_container_width=True)

