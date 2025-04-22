import streamlit as st
import pandas as pd
import numpy as np
import os
from utils.data_processor import load_sample_data
from assets.image_urls import get_random_image

# Set page configuration
st.set_page_config(
    page_title="AgriPak Intelligence System",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main app header
st.title("🌾 AgriPak Intelligence System")

# App description
st.markdown("""
Welcome to AgriPak Intelligence System - a comprehensive agricultural intelligence platform
designed specifically for farmers in Pakistan. Our system provides actionable insights,
interactive visualizations, and data-driven recommendations to improve crop yield and resource management.
""")

# Key Features section with full width
st.markdown("""
### Key Features of AgriPak Intelligence System:
- 📊 Real-time agricultural data analysis
- 🌱 Crop health monitoring and disease detection
- 🌦️ Weather forecasting and alerts
- 📈 Yield prediction and optimization
- 🚜 Resource management recommendations
- 📝 Customizable reports and insights
""")

# App styling with gradient background
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to bottom right, #f0fff4, #e6fffa);
    }
    /* Common card styles for consistency */
    .dashboard-card {
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 10px;
        text-align: center;
        cursor: pointer;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
        min-height: 180px; /* Fixed height for all cards */
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .dashboard-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }
    .dashboard-card h3 {
        margin-top: 0;
        margin-bottom: 15px;
        font-size: 1.3rem;
    }
    .dashboard-card p {
        margin-bottom: 0;
        font-size: 0.9rem;
    }
    /* Specific gradients for each card type */
    .gradient-card {
        background: linear-gradient(to bottom right, #4CAF50, #2E7D32);
    }
    .resource-card {
        background: linear-gradient(to bottom right, #3b7fb4, #153567);
    }
    .weather-card {
        background: linear-gradient(to bottom right, #ff9800, #e65100);
    }
    .yield-card {
        background: linear-gradient(to bottom right, #9c27b0, #4a148c);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Quick access section with clickable cards
st.subheader("Quick Access Dashboard")
quick_access = st.columns(5)

with quick_access[0]:
    dashboard_clicked = st.markdown(
        """
        <div class="dashboard-card gradient-card" onclick="parent.window.location.href='Dashboard'">
            <h3>📊 Dashboard</h3>
            <p>View your agricultural dashboard with key metrics and analytics</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Go to Dashboard", key="dash_btn", use_container_width=True):
        st.switch_page("pages/1_Dashboard.py")

with quick_access[1]:
    health_clicked = st.markdown(
        """
        <div class="dashboard-card gradient-card" onclick="parent.window.location.href='Crop_Health'">
            <h3>🌱 Crop Health</h3>
            <p>Monitor crop health and get disease diagnosis recommendations</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Go to Crop Health", key="health_btn", use_container_width=True):
        st.switch_page("pages/2_Crop_Health.py")

with quick_access[2]:
    weather_clicked = st.markdown(
        """
        <div class="dashboard-card weather-card" onclick="parent.window.location.href='Weather_Data'">
            <h3>🌦️ Weather Data</h3>
            <p>Access weather forecasts, alerts and historical weather data</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Go to Weather Data", key="weather_btn", use_container_width=True):
        st.switch_page("pages/5_Weather_Data.py")

with quick_access[3]:
    yield_clicked = st.markdown(
        """
        <div class="dashboard-card yield-card" onclick="parent.window.location.href='Yield_Forecast'">
            <h3>📈 Yield Forecast</h3>
            <p>View yield predictions and optimization recommendations</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Go to Yield Forecast", key="yield_btn", use_container_width=True):
        st.switch_page("pages/3_Yield_Forecast.py")
        
with quick_access[4]:
    resource_clicked = st.markdown(
        """
        <div class="dashboard-card resource-card" onclick="parent.window.location.href='Resource_Optimization'">
            <h3>💧 Resource Optimization</h3>
            <p>Optimize water, fertilizer, and other resources efficiently</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Go to Resource Optimization", key="resource_btn", use_container_width=True):
        st.switch_page("pages/4_Resource_Optimization.py")

# Latest Updates Section
st.subheader("Latest Updates")
updates_data = [
    {"date": "2023-10-15", "title": "Rain forecast updated for Punjab region", "type": "Weather"},
    {"date": "2023-10-14", "title": "New satellite imagery available for Sindh province", "type": "Imagery"},
    {"date": "2023-10-13", "title": "Wheat disease alert in Northern districts", "type": "Alert"},
    {"date": "2023-10-10", "title": "Resource optimization tips for rice farmers", "type": "Tip"}
]

updates_df = pd.DataFrame(updates_data)
st.dataframe(updates_df, use_container_width=True, hide_index=True)

# Getting Started Section
st.subheader("Getting Started")
st.markdown("""
1. Navigate to the **Dashboard** for an overview of your agricultural data
2. Check **Crop Health** for disease detection and health monitoring
3. View **Yield Forecast** for predictions and optimization recommendations
4. Use **Resource Optimization** for efficient resource management
5. Access **Weather Data** for forecasts and historical analysis
6. Generate custom **Reports** for your farm's performance
""")

# Footer
st.markdown("---")
st.markdown("© 2023 AgriPak Intelligence System | Empowering Pakistani Farmers with Data")

# Sidebar with user profile and navigation
with st.sidebar:
    st.title("AgriPak")
    
    # User profile section
    st.subheader("Farm Profile")
    farm_name = st.text_input("Farm Name", value="Demo Farm")
    farm_location = st.selectbox(
        "Location",
        ["Punjab", "Sindh", "Khyber Pakhtunkhwa", "Balochistan", "Gilgit-Baltistan", "Azad Kashmir"]
    )
    
    # Main crop selection
    selected_crops = st.multiselect(
        "Main Crops",
        ["Wheat", "Rice", "Cotton", "Sugarcane", "Maize", "Potato", "Tomato", "Onion", "Mango", "Citrus"],
        ["Wheat", "Rice"]
    )
    
    # Farm size
    farm_size = st.slider("Farm Size (Acres)", 1, 1000, 50)
    
    st.markdown("---")
    
    # Navigation links
    st.subheader("Navigation")
    st.page_link("app.py", label="Home", icon="🏠")
    st.page_link("pages/1_Dashboard.py", label="Dashboard", icon="📊")
    st.page_link("pages/2_Crop_Health.py", label="Crop Health Analysis", icon="🌱")
    st.page_link("pages/3_Yield_Forecast.py", label="Yield Forecasting", icon="📈")
    st.page_link("pages/4_Resource_Optimization.py", label="Resource Optimization", icon="💧")
    st.page_link("pages/5_Weather_Data.py", label="Weather Data", icon="🌦️")
    st.page_link("pages/6_Reports.py", label="Reports & Analytics", icon="📝")
    
    st.markdown("---")
    st.caption("Version 1.0.0")
