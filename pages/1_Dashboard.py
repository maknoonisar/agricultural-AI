import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.data_processor import load_sample_data
from utils.mapbox_utils import create_farm_map
from utils.visualization import create_crop_health_chart, create_yield_chart
from assets.image_urls import get_random_image

# Set page configuration
st.set_page_config(
    page_title="Dashboard - AgriPak Intelligence System",
    page_icon="📊",
    layout="wide",
)

# Page header
st.title("📊 Agricultural Dashboard")
st.markdown("Overview of your farm's key metrics and performance indicators")

# Get sample data
crop_data = load_sample_data("crop_data")
weather_data = load_sample_data("weather_data")
soil_data = load_sample_data("soil_data")

# Create farm profile section
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.subheader("Farm Profile")
    
    # Display farm information (this would normally come from a database)
    farm_name = "Demo Farm"
    location = "Punjab, Pakistan"
    total_area = "50 Acres"
    main_crops = "Wheat, Rice, Cotton"
    
    st.info(f"""
    **Farm Name:** {farm_name}  
    **Location:** {location}  
    **Total Area:** {total_area}  
    **Main Crops:** {main_crops}
    """)
    
    # Display a random image
    st.image(
        get_random_image("farming_landscapes_pakistan"),
        caption="Farm landscape view",
        use_column_width=True
    )

with col2:
    st.subheader("Farm Map View")
    
    # Create and display a MapBox map
    mapbox_token = "YOUR_MAPBOX_TOKEN"  # This would come from environment variables in production
    farm_map = create_farm_map(mapbox_token, latitude=31.5204, longitude=74.3587, zoom=10)
    st.plotly_chart(farm_map, use_container_width=True)

with col3:
    st.subheader("Current Conditions")
    
    # Weather metrics
    current_temp = "32°C"
    humidity = "65%"
    rainfall = "0.0 mm"
    soil_moisture = "42%"
    
    st.metric(label="Temperature", value=current_temp, delta="2°C")
    st.metric(label="Humidity", value=humidity, delta="-5%")
    st.metric(label="Rainfall (24h)", value=rainfall)
    st.metric(label="Avg. Soil Moisture", value=soil_moisture, delta="3%")
    
    # Show temperature prediction for next week
    st.markdown("**7-Day Temperature Forecast**")
    
    # Create sample dates and temperatures for forecast
    dates = [(datetime.now() + timedelta(days=x)).strftime('%a') for x in range(7)]
    temps = [32, 33, 31, 30, 32, 34, 33]
    
    # Create chart
    forecast_chart = px.line(
        x=dates, 
        y=temps,
        labels={"x": "Day", "y": "Temperature (°C)"},
        markers=True
    )
    forecast_chart.update_layout(height=200, margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(forecast_chart, use_container_width=True)

# Create key performance indicators section
st.subheader("Key Performance Indicators")

kpi_cols = st.columns(4)

with kpi_cols[0]:
    st.metric(
        label="Crop Health Index", 
        value="76/100", 
        delta="4",
        help="Overall health score based on various indicators"
    )

with kpi_cols[1]:
    st.metric(
        label="Estimated Yield", 
        value="4.2 tons/acre", 
        delta="0.3 tons",
        help="Predicted yield based on current conditions and historical data"
    )

with kpi_cols[2]:
    st.metric(
        label="Water Usage Efficiency", 
        value="82%", 
        delta="5%",
        help="How efficiently water resources are being utilized"
    )

with kpi_cols[3]:
    st.metric(
        label="Pest Risk Level", 
        value="Low", 
        delta="unchanged",
        help="Current risk assessment for pest infestations"
    )

# Create visualization section
st.subheader("Farm Analytics")

tab1, tab2, tab3 = st.tabs(["Crop Health", "Yield Trends", "Resource Usage"])

with tab1:
    # Create crop health visualization
    health_chart = create_crop_health_chart()
    st.plotly_chart(health_chart, use_container_width=True)
    
    # Add more context
    st.info("""
    The Crop Health Index is calculated based on multiple factors including:
    - Visual inspection data
    - Soil nutrient levels
    - Pest presence
    - Disease markers
    - Growth stage assessment
    
    Regular monitoring is recommended to maintain optimal crop health.
    """)

with tab2:
    # Create yield visualization
    yield_chart = create_yield_chart()
    st.plotly_chart(yield_chart, use_container_width=True)
    
    # Add more context
    st.info("""
    Yield forecasts are based on:
    - Historical yield data
    - Current crop health
    - Weather patterns and predictions
    - Soil conditions
    - Management practices
    
    The current season projection shows a positive trend compared to previous years.
    """)

with tab3:
    # Create resource usage visualization
    resource_data = {
        'Resource': ['Water', 'Fertilizer', 'Pesticides', 'Labor', 'Energy'],
        'Current Usage': [75, 60, 40, 85, 55],
        'Optimal Usage': [65, 55, 35, 80, 50]
    }
    
    resource_df = pd.DataFrame(resource_data)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=resource_df['Resource'],
        y=resource_df['Current Usage'],
        name='Current Usage',
        marker_color='#1F77B4'
    ))
    
    fig.add_trace(go.Bar(
        x=resource_df['Resource'],
        y=resource_df['Optimal Usage'],
        name='Optimal Usage',
        marker_color='#2CA02C'
    ))
    
    fig.update_layout(
        title='Resource Usage vs. Optimal Levels',
        barmode='group',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("""
    The chart shows current resource usage compared to optimal levels based on your farm's specific conditions.
    Opportunities for optimization exist in water and fertilizer usage, which could lead to cost savings and improved sustainability.
    """)

# Recent alerts section
st.subheader("Recent Alerts")

alerts = [
    {"date": "2023-10-14", "type": "Weather", "message": "Heavy rainfall expected in your region within 48 hours", "severity": "High"},
    {"date": "2023-10-12", "type": "Crop Health", "message": "Early signs of leaf rust detected in wheat field #3", "severity": "Medium"},
    {"date": "2023-10-10", "type": "Water", "message": "Irrigation system in north sector showing reduced efficiency", "severity": "Low"},
    {"date": "2023-10-08", "type": "Pest", "message": "Increased aphid activity detected in eastern fields", "severity": "Medium"}
]

# Convert to DataFrame for display
alerts_df = pd.DataFrame(alerts)

# Create style conditions for severity colors
def highlight_severity(s):
    return ['background-color: #ffcccc' if x == 'High' 
            else 'background-color: #ffffcc' if x == 'Medium'
            else 'background-color: #ccffcc' if x == 'Low'
            else '' for x in s]

# Display the styled dataframe
st.dataframe(alerts_df.style.apply(highlight_severity, subset=['severity']), 
             use_container_width=True, 
             hide_index=True)

# Action items section
st.subheader("Recommended Actions")

action_items = st.columns(3)

with action_items[0]:
    st.info("**Weather Preparation**\n\nSecure loose equipment and ensure proper drainage before heavy rainfall arrives.")
    
with action_items[1]:
    st.warning("**Disease Management**\n\nApply fungicide treatment to wheat field #3 to prevent leaf rust spread.")
    
with action_items[2]:
    st.success("**Resource Optimization**\n\nAdjust irrigation schedule to improve water usage efficiency in northern fields.")

# Footer
st.markdown("---")
st.caption("Dashboard last updated: October 15, 2023 at 09:30 AM")
