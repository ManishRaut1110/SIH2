import streamlit as st
import pandas as pd
import plotly.express as px
from geopy.geocoders import Nominatim

df = pd.read_csv("updated_with_relevance.csv")
geolocator = Nominatim(user_agent="geoapiExercises")

# CSS for improved styling
st.markdown("""
    <style>
    .center-text {
        text-align: center;
    }
    .sidebar .sidebar-content {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .sidebar .sidebar-content .css-1v3fvcr {
        text-align: center;
    }
    .css-1v3fvcr {
        margin: 0 auto;
    }
    .header {
        color: #007acc;
        font-size: 3rem; /* Increased font size for header */
        font-weight: bold;
    }
    .section-title {
        font-size: 2rem; /* Increased font size for section titles */
        color: #007acc;
        margin-top: 2rem;
    }
    .chart-container {
        padding: 1rem;
        background-color: #f0f2f6; /* Light background for the charts */
        border-radius: 8px; /* Rounded corners for the chart containers */
    }
    body {
        background-color: #e5e5e5; /* Background color for the whole page */
    }
    .text-large {
        font-size: 1.25rem; /* Increased font size for large text elements */
    }
    </style>
    """, unsafe_allow_html=True)

# Function to geocode locations
def geocode_location(location):
    try:
        loc = geolocator.geocode(location)
        if loc:
            return loc.latitude, loc.longitude
        else:
            return None, None
    except Exception as e:
        return None, None

with st.sidebar:
    st.image("assets/Disaster Aggregation DELAYED.png", use_column_width=True)
    st.markdown('<h2 class="center-text text-large">Navigation</h2>', unsafe_allow_html=True)
    nav = st.radio(
        "",
        ("Dashboard", "Dataset", "Heatmap", "About Us"),
        index=0
    )

# Dashboard section
if nav == "Dashboard":
    st.markdown('<h1 class="header center-text">Disaster Aggregation System</h1>', unsafe_allow_html=True)
    
    # Pie chart for 'Relevant' vs 'Not relevant' tweets
    relevance_counts = df['relevance'].value_counts()
    fig_pie = px.pie(
        relevance_counts,
        values=relevance_counts,
        names=relevance_counts.index,
        title='Relevant vs Not Relevant Tweets',
        template="plotly_dark"  # Dark theme for better aesthetics
    )
    fig_pie.update_traces(textinfo='percent+label', pull=[0.1, 0.1])
    fig_pie.update_layout(
        width=800,  # Adjust width
        height=500, # Adjust height
        margin=dict(l=20, r=20, t=30, b=20)  # Adjust margins
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    # Bar graph showing counts for each 'label'
    label_counts = df['label'].value_counts()
    fig_bar = px.bar(
        label_counts,
        x=label_counts.index,
        y=label_counts.values,
        title='Tweet Categories based on Label',
        labels={'x': 'Label', 'y': 'Count'},
        template="plotly_dark"  # Dark theme for better aesthetics
    )
    fig_bar.update_layout(
        width=800,  # Adjust width
        height=500, # Adjust height
        bargap=0.2  # Adjust spacing between bars
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# Dataset section with pagination
if nav == "Dataset":
    st.markdown('<h1 class="header center-text">Tweet Details</h1>', unsafe_allow_html=True)

    # Pagination logic
    tweets_per_page = 10
    page = st.number_input('Page number', min_value=1, max_value=(len(df) // tweets_per_page) + 1, step=1)

    start_idx = (page - 1) * tweets_per_page
    end_idx = start_idx + tweets_per_page

    # Display tweet details with pagination
    for i in range(start_idx, min(end_idx, len(df))):
        st.markdown(f"<p class='center-text text-large'><b>Tweet Text:</b> {df['text'][i]}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='center-text text-large'><b>Relevance:</b> {df['relevance'][i]}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='center-text text-large'><b>Label:</b> {df['label'][i]}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='center-text text-large'><b>Location:</b> {df['location'][i]}</p>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)

# Heatmap section
if nav == "Heatmap":
    st.markdown('<h1 class="header center-text">Heatmap of Tweet Locations</h1>', unsafe_allow_html=True)

    if 'location' in df.columns:
        # Create latitude and longitude columns
        if 'tweet_lat' not in df.columns or 'tweet_lon' not in df.columns:
            df['tweet_lat'], df['tweet_lon'] = zip(*df['location'].apply(geocode_location))

        # Drop rows where geocoding failed
        df_geocoded = df.dropna(subset=['tweet_lat', 'tweet_lon'])

        if not df_geocoded.empty:
            # Plot the heatmap
            fig_heatmap = px.density_mapbox(
                df_geocoded, lat='tweet_lat', lon='tweet_lon', radius=10,
                hover_name='text', mapbox_style="stamen-terrain",
                title="Heatmap of Disaster Tweets",
                template="plotly_dark"  # Dark theme for better aesthetics
            )
            fig_heatmap.update_layout(
                width=800,  # Adjust width
                height=500, # Adjust height
                margin=dict(l=0, r=0, t=30, b=0)  # Adjust margins
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)
        else:
            st.markdown('<p class="center-text text-large">No geocoded location data available.</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="center-text text-large">Location data not available in the dataset.</p>', unsafe_allow_html=True)

# About Us section
if nav == "About Us":
    st.markdown('<h1 class="header center-text">About Us</h1>', unsafe_allow_html=True)
    st.markdown('<p class="center-text text-large">Details about the team and project...</p>', unsafe_allow_html=True)
