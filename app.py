import streamlit as st
import pandas as pd
import plotly.express as px
from geopy.geocoders import Nominatim
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import ast

df = pd.read_csv("updated_with_lat_lon.csv")
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
    .heatmap-container {
        height: 600px; /* Height for the heatmap */
        width: 1200px; /* Increased width for the heatmap */
        border-radius: 8px; /* Rounded corners for the heatmap container */
        background-color: #ffffff; /* White background for better contrast */
        margin: 0 auto; /* Center the heatmap */
        padding: 0; /* No padding around the heatmap */
        margin-top: 10px; /* Margin-top to reduce the gap between the title and heatmap */
    }
    </style>
    """, unsafe_allow_html=True)

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
    st.markdown('<h1 class="header center-text">Disaster Heatmap</h1>', unsafe_allow_html=True)

    # Parsing extracted_locations as actual lists of dictionaries
    df['extracted_locations'] = df['extracted_locations'].apply(ast.literal_eval)

    # Extracting location data for the heatmap
    location_data = []
    for location_list in df['extracted_locations']:
        for loc in location_list:
            location_data.append([loc['latitude'], loc['longitude']])

    # Create the Folium map
    m = folium.Map(location=[0, 0], zoom_start=2, control_scale=True)

    # Add HeatMap
    HeatMap(location_data, radius=10, blur=15, max_zoom=13).add_to(m)

    # Display the map in Streamlit
    st.markdown('<div class="heatmap-container">', unsafe_allow_html=True)
    folium_static(m)
    st.markdown('</div>', unsafe_allow_html=True)

# About Us section
if nav == "About Us":
    st.markdown('<h1 class="header center-text">About Us</h1>', unsafe_allow_html=True)
    st.markdown('<p class="center-text text-large">Details about the team and project...</p>', unsafe_allow_html=True)
