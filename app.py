import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from geopy.geocoders import Nominatim

df = pd.read_csv("updated_with_relevance.csv")
geolocator = Nominatim(user_agent="geoapiExercises")

# Function to geocode locations
def geocode_location(location):
    try:
        loc = geolocator.geocode(location)
        if loc:
            print(f'{loc.latitude} - {loc.longitude}')
            return loc.latitude, loc.longitude
        else:
            return None, None
    except Exception as e:
        return None, None

with st.sidebar:
    st.image("assets/Disaster Aggregation DELAYED.png")
    nav = st.radio(
        "Navigation",
        ("Dashboard", "Dataset", "Heatmap","About Us")
    )

# Dashboard section
if nav == "Dashboard":
    st.title('Disaster Aggregation System')
    # Pie chart for 'Relevant' vs 'Not relevant' tweets
    relevance_counts = df['relevance'].value_counts()
    fig_pie = px.pie(
        relevance_counts,
        values=relevance_counts,
        names=relevance_counts.index,
        title='Relevant vs Not Relevant Tweets'
    )
    st.plotly_chart(fig_pie)

    # Bar graph showing counts for each 'label'
    label_counts = df['label'].value_counts()
    fig_bar = px.bar(
        label_counts,
        x=label_counts.index,
        y=label_counts.values,
        title='Tweet Categories based on Label',
        labels={'x': 'Label', 'y': 'Count'}
    )
    st.plotly_chart(fig_bar)

# Dataset section with pagination
if nav == "Dataset":
    st.title('Tweet Details')

    # Pagination logic
    tweets_per_page = 10
    page = st.number_input('Page number', min_value=1, max_value=(len(df) // tweets_per_page) + 1, step=1)

    start_idx = (page - 1) * tweets_per_page
    end_idx = start_idx + tweets_per_page

    # Display tweet details with pagination
    for i in range(start_idx, min(end_idx, len(df))):
        st.write(f"**Tweet Text:** {df['text'][i]}")
        st.write(f"**Relevance:** {df['relevance'][i]}")
        st.write(f"**Label:** {df['label'][i]}")
        st.write(f"**Location:** {df['location'][i]}")
        st.write("---")

if nav == "Heatmap":
    st.title("Heatmap of Tweet Locations")

    # Check if 'location' exists in the dataset
    if 'location' in df.columns:
        # Create columns for latitude and longitude if they don't exist
        if 'tweet_lat' not in df.columns or 'tweet_lon' not in df.columns:
            df['tweet_lat'], df['tweet_lon'] = zip(*df['location'].apply(geocode_location))
        
        # Drop rows where location could not be geocoded
        df_geocoded = df.dropna(subset=['tweet_lat', 'tweet_lon'])

        if not df_geocoded.empty:
            # Plot the heatmap
            fig_heatmap = px.density_mapbox(
                df_geocoded, lat='tweet_lat', lon='tweet_lon', radius=10,
                hover_name='text', mapbox_style="stamen-terrain",
                title="Heatmap of Disaster Tweets"
            )
            st.plotly_chart(fig_heatmap)
        else:
            st.write("No geocoded location data available.")
    else:
        st.write("Location data not available in the dataset.")

# About Us section
if nav == "About Us":
    st.title("About Us")
    st.write("Details about the team and project...")