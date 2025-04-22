import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.data_processor import load_sample_data
from utils.weather_api import get_weather_forecast, get_historical_weather
from utils.mapbox_utils import create_weather_map
from assets.image_urls import get_random_image

# Set page configuration
st.set_page_config(
    page_title="Weather Data - AgriPak Intelligence System",
    page_icon="🌦️",
    layout="wide",
)

# Page header
st.title("🌦️ Weather Data")
st.markdown("Access historical weather data, forecasts, and analyze weather patterns")

# Create tabs for different weather analyses
tab1, tab2, tab3 = st.tabs(["Weather Forecast", "Historical Analysis", "Weather Alerts"])

with tab1:
    st.header("Weather Forecast")
    
    # Create columns for location selection and date range
    col1, col2, col3 = st.columns(3)
    
    with col1:
        location = st.selectbox(
            "Select Location",
            ["Current Farm Location", "Lahore", "Karachi", "Islamabad", "Faisalabad", "Multan", "Peshawar", "Quetta"]
        )
    
    with col2:
        forecast_days = st.slider(
            "Forecast Days",
            min_value=1,
            max_value=14,
            value=7
        )
    
    with col3:
        forecast_type = st.selectbox(
            "Forecast Type",
            ["Standard", "Detailed", "Agricultural"]
        )
    
    # Display the weather map
    st.subheader("Weather Map")
    
    mapbox_token = "pk.eyJ1IjoiZW5ncmtpIiwiYSI6ImNrc29yeHB2aDBieDEydXFoY240bXExcWoifQ.WS7GVtVGZb4xgHn9dleszQ"
    weather_map = create_weather_map(mapbox_token, latitude=31.5204, longitude=74.3587, zoom=6)
    st.plotly_chart(weather_map, use_container_width=True)
    
    # Create columns for current conditions and forecast
    current_col, forecast_col = st.columns([1, 2])
    
    with current_col:
        st.subheader("Current Conditions")
        
        # Show a random weather image
        st.image(
            get_random_image("farming_landscapes_pakistan"),
            caption="Current weather conditions",
            use_column_width=True
        )
        
        # Display current weather metrics
        if location == "Current Farm Location" or location == "Lahore":
            current_temp = "32°C"
            feels_like = "34°C"
            humidity = "65%"
            wind_speed = "12 km/h"
            pressure = "1010 hPa"
            visibility = "10 km"
            weather_desc = "Partly Cloudy"
        else:
            # For other locations, we would normally call a weather API
            # Using sample values for demonstration
            current_temp = "29°C"
            feels_like = "31°C"
            humidity = "70%"
            wind_speed = "15 km/h"
            pressure = "1012 hPa"
            visibility = "8 km"
            weather_desc = "Mostly Sunny"
        
        # Display weather information in metrics and info boxes
        st.markdown(f"### {location}")
        st.markdown(f"**{weather_desc}**")
        st.markdown(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        st.metric(label="Temperature", value=current_temp, delta="2°C")
        st.metric(label="Feels Like", value=feels_like)
        st.metric(label="Humidity", value=humidity, delta="-5%")
        
        # Additional weather information
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Wind:** {wind_speed}")
            st.markdown(f"**Pressure:** {pressure}")
        
        with col2:
            st.markdown(f"**Visibility:** {visibility}")
            st.markdown(f"**Dew Point:** 24°C")
    
    with forecast_col:
        st.subheader(f"{forecast_days}-Day Forecast")
        
        # Create a sample forecast data
        dates = [datetime.now() + timedelta(days=i) for i in range(forecast_days)]
        
        # Different weather patterns based on location
        if location in ["Lahore", "Faisalabad", "Multan", "Current Farm Location"]:
            max_temps = [32, 33, 34, 33, 32, 31, 32, 33, 34, 35, 33, 32, 31, 30][:forecast_days]
            min_temps = [24, 25, 26, 25, 24, 23, 24, 25, 26, 27, 25, 24, 23, 22][:forecast_days]
            precip_prob = [10, 5, 5, 20, 30, 40, 20, 10, 5, 0, 5, 10, 30, 40][:forecast_days]
            conditions = ["Partly Cloudy", "Sunny", "Sunny", "Partly Cloudy", "Cloudy", "Light Rain", 
                         "Partly Cloudy", "Sunny", "Sunny", "Clear", "Partly Cloudy", "Partly Cloudy", 
                         "Cloudy", "Light Rain"][:forecast_days]
        elif location in ["Karachi"]:
            max_temps = [34, 35, 34, 34, 33, 35, 36, 35, 34, 33, 34, 35, 36, 35][:forecast_days]
            min_temps = [27, 28, 27, 26, 26, 27, 28, 27, 26, 26, 27, 28, 28, 27][:forecast_days]
            precip_prob = [5, 0, 0, 5, 10, 5, 0, 0, 5, 10, 15, 10, 5, 0][:forecast_days]
            conditions = ["Sunny", "Clear", "Sunny", "Sunny", "Partly Cloudy", "Sunny", 
                         "Clear", "Sunny", "Partly Cloudy", "Partly Cloudy", "Cloudy", 
                         "Partly Cloudy", "Sunny", "Clear"][:forecast_days]
        else:
            max_temps = [30, 29, 28, 27, 26, 28, 29, 30, 31, 30, 29, 28, 27, 26][:forecast_days]
            min_temps = [22, 21, 20, 19, 18, 20, 21, 22, 23, 22, 21, 20, 19, 18][:forecast_days]
            precip_prob = [20, 30, 40, 50, 60, 40, 30, 20, 10, 20, 30, 40, 50, 60][:forecast_days]
            conditions = ["Partly Cloudy", "Cloudy", "Light Rain", "Rain", "Heavy Rain", 
                         "Light Rain", "Cloudy", "Partly Cloudy", "Sunny", "Partly Cloudy", 
                         "Cloudy", "Light Rain", "Rain", "Heavy Rain"][:forecast_days]
        
        # Create DataFrame
        forecast_data = {
            'Date': dates,
            'Day': [d.strftime('%a') for d in dates],
            'Max Temp (°C)': max_temps,
            'Min Temp (°C)': min_temps,
            'Precipitation (%)': precip_prob,
            'Conditions': conditions
        }
        
        forecast_df = pd.DataFrame(forecast_data)
        
        # Create temperature chart
        temp_fig = go.Figure()
        
        temp_fig.add_trace(go.Scatter(
            x=forecast_df['Day'],
            y=forecast_df['Max Temp (°C)'],
            mode='lines+markers',
            name='Max Temp',
            line=dict(color='red', width=2),
            marker=dict(size=8)
        ))
        
        temp_fig.add_trace(go.Scatter(
            x=forecast_df['Day'],
            y=forecast_df['Min Temp (°C)'],
            mode='lines+markers',
            name='Min Temp',
            line=dict(color='blue', width=2),
            marker=dict(size=8)
        ))
        
        temp_fig.update_layout(
            title='Temperature Forecast',
            xaxis_title='Day',
            yaxis_title='Temperature (°C)',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin=dict(l=20, r=20, t=40, b=20),
            height=300
        )
        
        st.plotly_chart(temp_fig, use_container_width=True)
        
        # Create precipitation chart
        precip_fig = px.bar(
            forecast_df,
            x='Day',
            y='Precipitation (%)',
            color='Precipitation (%)',
            color_continuous_scale='Blues',
            labels={'Precipitation (%)': 'Probability (%)'},
            title='Precipitation Probability'
        )
        
        precip_fig.update_layout(
            xaxis_title='Day',
            yaxis_title='Probability (%)',
            margin=dict(l=20, r=20, t=40, b=20),
            height=250
        )
        
        st.plotly_chart(precip_fig, use_container_width=True)
        
        # Display daily forecast details in expandable sections
        st.subheader("Daily Details")
        
        for i, row in forecast_df.iterrows():
            date_str = row['Date'].strftime('%A, %B %d')
            with st.expander(f"{date_str} - {row['Conditions']}"):
                daily_col1, daily_col2 = st.columns(2)
                
                with daily_col1:
                    st.markdown(f"**Temperature:** {row['Min Temp (°C)']}°C to {row['Max Temp (°C)']}°C")
                    st.markdown(f"**Precipitation Chance:** {row['Precipitation (%)']}%")
                    
                    # Add more weather details that would normally come from an API
                    if row['Precipitation (%)'] > 30:
                        precipitation = f"{np.random.randint(1, 10)} mm"
                    else:
                        precipitation = "0 mm"
                        
                    st.markdown(f"**Expected Precipitation:** {precipitation}")
                    st.markdown(f"**Humidity:** {np.random.randint(50, 85)}%")
                
                with daily_col2:
                    st.markdown(f"**Wind:** {np.random.randint(5, 20)} km/h")
                    st.markdown(f"**UV Index:** {np.random.randint(1, 11)}/10")
                    st.markdown(f"**Sunrise:** {(datetime.now() + timedelta(minutes=np.random.randint(-10, 10))).strftime('%H:%M')}")
                    st.markdown(f"**Sunset:** {(datetime.now() + timedelta(hours=12) + timedelta(minutes=np.random.randint(-10, 10))).strftime('%H:%M')}")
    
    # Agricultural impacts section
    if forecast_type == "Agricultural":
        st.subheader("Agricultural Weather Impacts")
        
        # Calculate growing degree days based on temperature
        forecast_df['GDD'] = ((forecast_df['Max Temp (°C)'] + forecast_df['Min Temp (°C)']) / 2) - 10  # Base temp of 10°C
        forecast_df['GDD'] = forecast_df['GDD'].apply(lambda x: max(0, x))  # GDD can't be negative
        
        # Create GDD chart
        gdd_fig = px.bar(
            forecast_df,
            x='Day',
            y='GDD',
            title='Growing Degree Days (Base 10°C)',
            color='GDD',
            color_continuous_scale='Viridis'
        )
        
        gdd_fig.update_layout(
            xaxis_title='Day',
            yaxis_title='GDD',
            height=300
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(gdd_fig, use_container_width=True)
            
            # Calculate cumulative GDD
            forecast_df['Cumulative GDD'] = forecast_df['GDD'].cumsum()
            
            # Create cumulative GDD chart
            cumulative_gdd_fig = px.line(
                forecast_df,
                x='Day',
                y='Cumulative GDD',
                title='Cumulative Growing Degree Days',
                markers=True
            )
            
            cumulative_gdd_fig.update_layout(
                xaxis_title='Day',
                yaxis_title='Cumulative GDD',
                height=300
            )
            
            st.plotly_chart(cumulative_gdd_fig, use_container_width=True)
        
        with col2:
            # Agricultural recommendations based on forecast
            st.subheader("Weather-Based Recommendations")
            
            avg_temp = sum(forecast_df['Max Temp (°C)']) / len(forecast_df)
            total_rain_chance = sum(1 for p in forecast_df['Precipitation (%)'] if p > 30)
            
            if total_rain_chance >= 3:
                rain_status = "high"
            elif total_rain_chance >= 1:
                rain_status = "moderate"
            else:
                rain_status = "low"
                
            if avg_temp > 32:
                temp_status = "high"
            elif avg_temp > 28:
                temp_status = "moderate"
            else:
                temp_status = "low"
                
            # Irrigation recommendations
            st.markdown("### Irrigation Planning")
            
            if rain_status == "high":
                st.success("⚠️ Significant rainfall expected. Consider reducing irrigation volumes by 30-50%.")
            elif rain_status == "moderate":
                st.info("⚠️ Some rainfall expected. Consider reducing irrigation volumes by 10-20%.")
            else:
                st.warning("⚠️ Minimal rainfall expected. Maintain regular irrigation schedule.")
                
            # Field operations recommendations
            st.markdown("### Field Operations")
            
            if rain_status == "high":
                st.warning("⚠️ Plan field operations around expected rainfall. Not suitable for spraying or fertilizer application.")
            elif rain_status == "moderate":
                st.info("⚠️ Limited window for field operations. Prioritize critical tasks.")
            else:
                st.success("⚠️ Good conditions for most field operations. Ideal for spraying and fertilizer application.")
                
            # Pest and disease risk
            st.markdown("### Pest & Disease Risk")
            
            if temp_status == "high" and rain_status != "low":
                st.error("⚠️ High risk for fungal diseases and rapid pest development. Monitor crops closely.")
            elif temp_status == "moderate" and rain_status == "high":
                st.warning("⚠️ Elevated risk for fungal diseases. Consider preventative fungicide application.")
            elif temp_status == "high" and rain_status == "low":
                st.warning("⚠️ Elevated risk for insect pests. Monitor for aphids and mites.")
            else:
                st.success("⚠️ Normal pest and disease pressure expected. Maintain regular monitoring.")
                
            # Crop-specific advice
            st.markdown("### Crop-Specific Advice")
            
            crops = ["Wheat", "Rice", "Cotton", "Sugarcane", "Maize"]
            selected_crop = st.selectbox("Select crop for specific recommendations", crops)
            
            crop_advice = {
                "Wheat": {
                    "high_temp_high_rain": "High risk of rust and powdery mildew. Apply fungicide if in vulnerable growth stage.",
                    "high_temp_low_rain": "Monitor for aphids and heat stress. Ensure adequate irrigation.",
                    "low_temp_high_rain": "Watch for waterlogging. Ensure field drainage is working properly.",
                    "low_temp_low_rain": "Favorable conditions. Good opportunity for fertilizer application if needed."
                },
                "Rice": {
                    "high_temp_high_rain": "Risk of bacterial leaf blight. Monitor water depth to prevent flooding.",
                    "high_temp_low_rain": "Maintain proper water depth. Good conditions for top dressing nitrogen.",
                    "low_temp_high_rain": "Monitor water depth. Not ideal for fertilizer application.",
                    "low_temp_low_rain": "May slow growth. Maintain proper water depth and monitor for pests."
                },
                "Cotton": {
                    "high_temp_high_rain": "High risk of boll rot. Consider growth regulator if plants are lush.",
                    "high_temp_low_rain": "Monitor for spider mites and whiteflies. Ensure adequate irrigation.",
                    "low_temp_high_rain": "Delayed boll development possible. Monitor for boll rot.",
                    "low_temp_low_rain": "Slower growth expected. Good conditions for fertilizer application."
                },
                "Sugarcane": {
                    "high_temp_high_rain": "Watch for red rot disease. Ensure proper drainage.",
                    "high_temp_low_rain": "Excellent growing conditions. Ensure adequate irrigation.",
                    "low_temp_high_rain": "Monitor for waterlogging. Check field drainage.",
                    "low_temp_low_rain": "Slower growth expected. Good time for weed control operations."
                },
                "Maize": {
                    "high_temp_high_rain": "Risk of foliar diseases. Monitor for fall armyworm after rain.",
                    "high_temp_low_rain": "Risk of pollination issues if during tasseling. Ensure irrigation.",
                    "low_temp_high_rain": "Growth may slow. Watch for waterlogging in low areas.",
                    "low_temp_low_rain": "Good conditions for most operations. Monitor soil moisture."
                }
            }
            
            # Determine which advice to show
            temp_rain_condition = f"{temp_status}_temp_{rain_status}_rain"
            
            # Find the closest matching condition if exact one doesn't exist
            if temp_rain_condition not in crop_advice[selected_crop]:
                if temp_status == "moderate":
                    temp_status = "high" if avg_temp > 30 else "low"
                if rain_status == "moderate":
                    rain_status = "high" if total_rain_chance >= 2 else "low"
                temp_rain_condition = f"{temp_status}_temp_{rain_status}_rain"
            
            st.info(f"**{selected_crop} Recommendation:** {crop_advice[selected_crop].get(temp_rain_condition, 'No specific recommendation available.')}")

with tab2:
    st.header("Historical Weather Analysis")
    
    # Create columns for filters
    hist_col1, hist_col2, hist_col3 = st.columns(3)
    
    with hist_col1:
        hist_location = st.selectbox(
            "Select Location",
            ["Current Farm Location", "Lahore", "Karachi", "Islamabad", "Faisalabad", "Multan", "Peshawar", "Quetta"],
            key="hist_location"
        )
    
    with hist_col2:
        hist_period = st.selectbox(
            "Select Period",
            ["Last Month", "Last 3 Months", "Last 6 Months", "Last Year", "Last 5 Years"]
        )
    
    with hist_col3:
        hist_parameter = st.selectbox(
            "Select Parameter",
            ["Temperature", "Precipitation", "Humidity", "All Parameters"]
        )
    
    # Convert period to number of days
    if hist_period == "Last Month":
        days = 30
    elif hist_period == "Last 3 Months":
        days = 90
    elif hist_period == "Last 6 Months":
        days = 180
    elif hist_period == "Last Year":
        days = 365
    else:  # Last 5 Years
        days = 1825
    
    # Generate date range
    if days <= 365:
        dates = pd.date_range(end=datetime.now(), periods=days)
    else:
        # For multi-year data, use monthly aggregates
        dates = pd.date_range(end=datetime.now(), periods=60, freq='M')
    
    # Create sample historical data based on location
    if hist_location in ["Lahore", "Faisalabad", "Multan", "Current Farm Location"]:
        # Punjab region weather patterns
        if days <= 365:
            max_temps = [32 + 10 * np.sin(2 * np.pi * i / 365) + np.random.normal(0, 2) for i in range(days)]
            min_temps = [20 + 8 * np.sin(2 * np.pi * i / 365) + np.random.normal(0, 2) for i in range(days)]
            precipitation = [np.random.exponential(1) if np.random.random() < 0.3 else 0 for _ in range(days)]
            # Higher precipitation in July-August (monsoon)
            for i in range(days):
                day_of_year = (datetime.now() - timedelta(days=days-i-1)).timetuple().tm_yday
                if 180 <= day_of_year <= 240:  # Approximately July-August
                    precipitation[i] = precipitation[i] * 3 if precipitation[i] > 0 else np.random.exponential(3) if np.random.random() < 0.5 else 0
        else:
            # Monthly data for multi-year view
            max_temps = [32 + 10 * np.sin(2 * np.pi * i / 12) + np.random.normal(0, 1) for i in range(60)]
            min_temps = [20 + 8 * np.sin(2 * np.pi * i / 12) + np.random.normal(0, 1) for i in range(60)]
            precipitation = [5 + 15 * np.sin(2 * np.pi * (i % 12 - 6) / 12) + np.random.exponential(5) for i in range(60)]
    
    elif hist_location in ["Karachi"]:
        # Coastal region
        if days <= 365:
            max_temps = [34 + 6 * np.sin(2 * np.pi * i / 365) + np.random.normal(0, 1.5) for i in range(days)]
            min_temps = [24 + 5 * np.sin(2 * np.pi * i / 365) + np.random.normal(0, 1.5) for i in range(days)]
            precipitation = [np.random.exponential(0.5) if np.random.random() < 0.1 else 0 for _ in range(days)]
            # Higher precipitation in July-August (monsoon)
            for i in range(days):
                day_of_year = (datetime.now() - timedelta(days=days-i-1)).timetuple().tm_yday
                if 180 <= day_of_year <= 240:  # Approximately July-August
                    precipitation[i] = precipitation[i] * 2 if precipitation[i] > 0 else np.random.exponential(2) if np.random.random() < 0.3 else 0
        else:
            max_temps = [34 + 6 * np.sin(2 * np.pi * i / 12) + np.random.normal(0, 1) for i in range(60)]
            min_temps = [24 + 5 * np.sin(2 * np.pi * i / 12) + np.random.normal(0, 1) for i in range(60)]
            precipitation = [2 + 8 * np.sin(2 * np.pi * (i % 12 - 6) / 12) + np.random.exponential(2) for i in range(60)]
    
    else:
        # Northern regions (more rainfall, lower temps)
        if days <= 365:
            max_temps = [26 + 12 * np.sin(2 * np.pi * i / 365) + np.random.normal(0, 2) for i in range(days)]
            min_temps = [14 + 10 * np.sin(2 * np.pi * i / 365) + np.random.normal(0, 2) for i in range(days)]
            precipitation = [np.random.exponential(2) if np.random.random() < 0.4 else 0 for _ in range(days)]
            # Higher precipitation in winter and monsoon
            for i in range(days):
                day_of_year = (datetime.now() - timedelta(days=days-i-1)).timetuple().tm_yday
                if (0 <= day_of_year <= 60) or (335 <= day_of_year <= 365) or (180 <= day_of_year <= 240):
                    precipitation[i] = precipitation[i] * 2 if precipitation[i] > 0 else np.random.exponential(4) if np.random.random() < 0.6 else 0
        else:
            max_temps = [26 + 12 * np.sin(2 * np.pi * i / 12) + np.random.normal(0, 1) for i in range(60)]
            min_temps = [14 + 10 * np.sin(2 * np.pi * i / 12) + np.random.normal(0, 1) for i in range(60)]
            precipitation = [10 + 20 * (np.sin(2 * np.pi * (i % 12) / 12) + np.sin(2 * np.pi * (i % 12 - 6) / 12)) + np.random.exponential(5) for i in range(60)]
    
    # Create humidity data
    if days <= 365:
        humidity = [60 + 20 * np.sin(2 * np.pi * i / 365) + np.random.normal(0, 5) for i in range(days)]
        # Increase humidity on rainy days
        for i in range(days):
            if precipitation[i] > 0:
                humidity[i] = min(95, humidity[i] + precipitation[i] * 2)
    else:
        humidity = [60 + 20 * np.sin(2 * np.pi * i / 12) + np.random.normal(0, 3) for i in range(60)]
    
    # Create DataFrame
    if days <= 365:
        weather_data = {
            'Date': dates,
            'Max Temp (°C)': max_temps,
            'Min Temp (°C)': min_temps,
            'Avg Temp (°C)': [(max_t + min_t) / 2 for max_t, min_t in zip(max_temps, min_temps)],
            'Precipitation (mm)': precipitation,
            'Humidity (%)': humidity
        }
    else:
        weather_data = {
            'Date': dates,
            'Max Temp (°C)': max_temps,
            'Min Temp (°C)': min_temps,
            'Avg Temp (°C)': [(max_t + min_t) / 2 for max_t, min_t in zip(max_temps, min_temps)],
            'Precipitation (mm)': precipitation,
            'Humidity (%)': humidity
        }
    
    weather_df = pd.DataFrame(weather_data)
    
    # Create visualizations based on selected parameter
    if hist_parameter == "Temperature" or hist_parameter == "All Parameters":
        st.subheader("Temperature Analysis")
        
        # Create temperature chart
        temp_fig = go.Figure()
        
        temp_fig.add_trace(go.Scatter(
            x=weather_df['Date'],
            y=weather_df['Max Temp (°C)'],
            mode='lines',
            name='Max Temp',
            line=dict(color='red', width=1)
        ))
        
        temp_fig.add_trace(go.Scatter(
            x=weather_df['Date'],
            y=weather_df['Min Temp (°C)'],
            mode='lines',
            name='Min Temp',
            line=dict(color='blue', width=1)
        ))
        
        temp_fig.add_trace(go.Scatter(
            x=weather_df['Date'],
            y=weather_df['Avg Temp (°C)'],
            mode='lines',
            name='Avg Temp',
            line=dict(color='green', width=2)
        ))
        
        temp_fig.update_layout(
            title=f'Temperature Trends for {hist_location} ({hist_period})',
            xaxis_title='Date',
            yaxis_title='Temperature (°C)',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(temp_fig, use_container_width=True)
        
        # Temperature statistics
        if days <= 365:
            monthly_temp = weather_df.set_index('Date').resample('M').agg({
                'Max Temp (°C)': 'max',
                'Min Temp (°C)': 'min',
                'Avg Temp (°C)': 'mean'
            }).reset_index()
            monthly_temp['Month'] = monthly_temp['Date'].dt.strftime('%b %Y')
            
            st.subheader("Monthly Temperature Statistics")
            
            temp_stats = go.Figure()
            
            for col, color in zip(['Max Temp (°C)', 'Avg Temp (°C)', 'Min Temp (°C)'], ['red', 'green', 'blue']):
                temp_stats.add_trace(go.Bar(
                    x=monthly_temp['Month'],
                    y=monthly_temp[col],
                    name=col,
                    marker_color=color
                ))
            
            temp_stats.update_layout(
                title='Monthly Temperature Statistics',
                xaxis_title='Month',
                yaxis_title='Temperature (°C)',
                barmode='group',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            st.plotly_chart(temp_stats, use_container_width=True)
        else:
            # For multi-year data, show annual statistics
            weather_df['Year'] = weather_df['Date'].dt.year
            weather_df['Month'] = weather_df['Date'].dt.month
            
            yearly_temp = weather_df.groupby('Year').agg({
                'Max Temp (°C)': 'max',
                'Min Temp (°C)': 'min',
                'Avg Temp (°C)': 'mean'
            }).reset_index()
            
            st.subheader("Yearly Temperature Statistics")
            
            yearly_temp_stats = go.Figure()
            
            for col, color in zip(['Max Temp (°C)', 'Avg Temp (°C)', 'Min Temp (°C)'], ['red', 'green', 'blue']):
                yearly_temp_stats.add_trace(go.Bar(
                    x=yearly_temp['Year'],
                    y=yearly_temp[col],
                    name=col,
                    marker_color=color
                ))
            
            yearly_temp_stats.update_layout(
                title='Yearly Temperature Statistics',
                xaxis_title='Year',
                yaxis_title='Temperature (°C)',
                barmode='group',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            st.plotly_chart(yearly_temp_stats, use_container_width=True)
            
            # Show monthly averages across years
            monthly_avg = weather_df.groupby('Month').agg({
                'Max Temp (°C)': 'mean',
                'Min Temp (°C)': 'mean',
                'Avg Temp (°C)': 'mean'
            }).reset_index()
            
            # Map month numbers to names
            month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            monthly_avg['Month Name'] = monthly_avg['Month'].apply(lambda x: month_names[x-1])
            
            monthly_avg_fig = go.Figure()
            
            for col, color in zip(['Max Temp (°C)', 'Avg Temp (°C)', 'Min Temp (°C)'], ['red', 'green', 'blue']):
                monthly_avg_fig.add_trace(go.Scatter(
                    x=monthly_avg['Month Name'],
                    y=monthly_avg[col],
                    mode='lines+markers',
                    name=col,
                    marker=dict(size=8),
                    line=dict(color=color, width=2)
                ))
            
            monthly_avg_fig.update_layout(
                title='Average Monthly Temperatures (Multi-Year)',
                xaxis_title='Month',
                yaxis_title='Temperature (°C)',
                xaxis=dict(
                    tickmode='array',
                    tickvals=month_names
                ),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            st.plotly_chart(monthly_avg_fig, use_container_width=True)
    
    if hist_parameter == "Precipitation" or hist_parameter == "All Parameters":
        st.subheader("Precipitation Analysis")
        
        # Create precipitation chart
        if days <= 365:
            precip_fig = px.bar(
                weather_df,
                x='Date',
                y='Precipitation (mm)',
                title=f'Daily Precipitation for {hist_location} ({hist_period})',
                color='Precipitation (mm)',
                color_continuous_scale='Blues'
            )
            
            precip_fig.update_layout(
                xaxis_title='Date',
                yaxis_title='Precipitation (mm)'
            )
            
            st.plotly_chart(precip_fig, use_container_width=True)
            
            # Monthly precipitation totals
            monthly_precip = weather_df.set_index('Date').resample('M').agg({
                'Precipitation (mm)': 'sum'
            }).reset_index()
            monthly_precip['Month'] = monthly_precip['Date'].dt.strftime('%b %Y')
            
            monthly_precip_fig = px.bar(
                monthly_precip,
                x='Month',
                y='Precipitation (mm)',
                title='Monthly Precipitation Totals',
                color='Precipitation (mm)',
                color_continuous_scale='Blues'
            )
            
            monthly_precip_fig.update_layout(
                xaxis_title='Month',
                yaxis_title='Total Precipitation (mm)'
            )
            
            st.plotly_chart(monthly_precip_fig, use_container_width=True)
        else:
            # For multi-year data, show annual and monthly statistics
            weather_df['Year'] = weather_df['Date'].dt.year
            weather_df['Month'] = weather_df['Date'].dt.month
            
            yearly_precip = weather_df.groupby('Year').agg({
                'Precipitation (mm)': 'sum'
            }).reset_index()
            
            yearly_precip_fig = px.bar(
                yearly_precip,
                x='Year',
                y='Precipitation (mm)',
                title='Yearly Precipitation Totals',
                color='Precipitation (mm)',
                color_continuous_scale='Blues'
            )
            
            yearly_precip_fig.update_layout(
                xaxis_title='Year',
                yaxis_title='Total Precipitation (mm)'
            )
            
            st.plotly_chart(yearly_precip_fig, use_container_width=True)
            
            # Show monthly averages across years
            monthly_precip_avg = weather_df.groupby('Month').agg({
                'Precipitation (mm)': 'mean'
            }).reset_index()
            
            # Map month numbers to names
            month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            monthly_precip_avg['Month Name'] = monthly_precip_avg['Month'].apply(lambda x: month_names[x-1])
            
            monthly_precip_avg_fig = px.bar(
                monthly_precip_avg,
                x='Month Name',
                y='Precipitation (mm)',
                title='Average Monthly Precipitation (Multi-Year)',
                color='Precipitation (mm)',
                color_continuous_scale='Blues'
            )
            
            monthly_precip_avg_fig.update_layout(
                xaxis_title='Month',
                yaxis_title='Average Precipitation (mm)',
                xaxis=dict(
                    tickmode='array',
                    tickvals=month_names
                )
            )
            
            st.plotly_chart(monthly_precip_avg_fig, use_container_width=True)
    
    if hist_parameter == "Humidity" or hist_parameter == "All Parameters":
        st.subheader("Humidity Analysis")
        
        # Create humidity chart
        humidity_fig = go.Figure()
        
        humidity_fig.add_trace(go.Scatter(
            x=weather_df['Date'],
            y=weather_df['Humidity (%)'],
            mode='lines',
            name='Humidity',
            line=dict(color='purple', width=1.5)
        ))
        
        humidity_fig.update_layout(
            title=f'Humidity Trends for {hist_location} ({hist_period})',
            xaxis_title='Date',
            yaxis_title='Humidity (%)',
            yaxis=dict(range=[0, 100])
        )
        
        st.plotly_chart(humidity_fig, use_container_width=True)
        
        # Humidity statistics
        if days <= 365:
            monthly_humidity = weather_df.set_index('Date').resample('M').agg({
                'Humidity (%)': ['mean', 'min', 'max']
            }).reset_index()
            
            monthly_humidity.columns = ['Date', 'Mean Humidity (%)', 'Min Humidity (%)', 'Max Humidity (%)']
            monthly_humidity['Month'] = monthly_humidity['Date'].dt.strftime('%b %Y')
            
            humidity_stats_fig = go.Figure()
            
            for col, color in zip(['Mean Humidity (%)', 'Min Humidity (%)', 'Max Humidity (%)'], ['purple', 'blue', 'red']):
                humidity_stats_fig.add_trace(go.Bar(
                    x=monthly_humidity['Month'],
                    y=monthly_humidity[col],
                    name=col,
                    marker_color=color
                ))
            
            humidity_stats_fig.update_layout(
                title='Monthly Humidity Statistics',
                xaxis_title='Month',
                yaxis_title='Humidity (%)',
                barmode='group',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            st.plotly_chart(humidity_stats_fig, use_container_width=True)
        else:
            # For multi-year data, show monthly averages across years
            weather_df['Month'] = weather_df['Date'].dt.month
            
            monthly_humidity_avg = weather_df.groupby('Month').agg({
                'Humidity (%)': 'mean'
            }).reset_index()
            
            # Map month numbers to names
            month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            monthly_humidity_avg['Month Name'] = monthly_humidity_avg['Month'].apply(lambda x: month_names[x-1])
            
            monthly_humidity_avg_fig = px.line(
                monthly_humidity_avg,
                x='Month Name',
                y='Humidity (%)',
                title='Average Monthly Humidity (Multi-Year)',
                markers=True
            )
            
            monthly_humidity_avg_fig.update_layout(
                xaxis_title='Month',
                yaxis_title='Average Humidity (%)',
                xaxis=dict(
                    tickmode='array',
                    tickvals=month_names
                )
            )
            
            st.plotly_chart(monthly_humidity_avg_fig, use_container_width=True)
    
    # Weather pattern analysis
    if hist_parameter == "All Parameters":
        st.subheader("Weather Pattern Analysis")
        
        # Create a heat map to show correlation between parameters
        if days <= 365:
            # Create daily correlation data
            correlation_df = weather_df[['Max Temp (°C)', 'Min Temp (°C)', 'Avg Temp (°C)', 'Precipitation (mm)', 'Humidity (%)']].corr()
            
            corr_fig = px.imshow(
                correlation_df,
                text_auto=True,
                color_continuous_scale='RdBu_r',
                title='Correlation Between Weather Parameters'
            )
            
            st.plotly_chart(corr_fig, use_container_width=True)
            
            # Check for extreme weather days
            extreme_weather = weather_df.copy()
            extreme_weather['Extreme'] = False
            
            # Mark extreme temperature days
            extreme_weather.loc[extreme_weather['Max Temp (°C)'] > np.percentile(extreme_weather['Max Temp (°C)'], 95), 'Extreme'] = True
            extreme_weather.loc[extreme_weather['Min Temp (°C)'] < np.percentile(extreme_weather['Min Temp (°C)'], 5), 'Extreme'] = True
            
            # Mark heavy rainfall days
            extreme_weather.loc[extreme_weather['Precipitation (mm)'] > np.percentile(extreme_weather['Precipitation (mm)'][extreme_weather['Precipitation (mm)'] > 0], 90), 'Extreme'] = True
            
            extreme_count = extreme_weather['Extreme'].sum()
            extreme_percentage = (extreme_count / len(extreme_weather)) * 100
            
            st.info(f"**Extreme Weather Analysis:** {extreme_count} days ({extreme_percentage:.1f}%) showed extreme weather conditions in the selected period.")
            
            # Show some extreme days
            if extreme_count > 0:
                st.markdown("### Sample Extreme Weather Days")
                extreme_sample = extreme_weather[extreme_weather['Extreme']].sample(min(5, extreme_count))
                extreme_sample['Date'] = extreme_sample['Date'].dt.strftime('%Y-%m-%d')
                st.dataframe(extreme_sample[['Date', 'Max Temp (°C)', 'Min Temp (°C)', 'Precipitation (mm)', 'Humidity (%)']], use_container_width=True)
        
        # Show seasonal patterns for multi-year data
        if days > 365:
            st.subheader("Seasonal Weather Patterns")
            
            # Group by month and calculate statistics
            monthly_patterns = weather_df.groupby('Month').agg({
                'Max Temp (°C)': 'mean',
                'Min Temp (°C)': 'mean',
                'Precipitation (mm)': 'sum',
                'Humidity (%)': 'mean'
            }).reset_index()
            
            # Map month numbers to names
            month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            monthly_patterns['Month Name'] = monthly_patterns['Month'].apply(lambda x: month_names[x-1])
            
            # Create a radar chart for seasonal patterns
            categories = monthly_patterns['Month Name'].tolist()
            
            # Normalize the data for radar chart
            max_temp_norm = monthly_patterns['Max Temp (°C)'] / monthly_patterns['Max Temp (°C)'].max()
            min_temp_norm = monthly_patterns['Min Temp (°C)'] / monthly_patterns['Min Temp (°C)'].max()
            precip_norm = monthly_patterns['Precipitation (mm)'] / monthly_patterns['Precipitation (mm)'].max()
            humidity_norm = monthly_patterns['Humidity (%)'] / monthly_patterns['Humidity (%)'].max()
            
            radar_fig = go.Figure()
            
            radar_fig.add_trace(go.Scatterpolar(
                r=max_temp_norm,
                theta=categories,
                fill='toself',
                name='Max Temperature',
                line_color='red'
            ))
            
            radar_fig.add_trace(go.Scatterpolar(
                r=min_temp_norm,
                theta=categories,
                fill='toself',
                name='Min Temperature',
                line_color='blue'
            ))
            
            radar_fig.add_trace(go.Scatterpolar(
                r=precip_norm,
                theta=categories,
                fill='toself',
                name='Precipitation',
                line_color='green'
            ))
            
            radar_fig.add_trace(go.Scatterpolar(
                r=humidity_norm,
                theta=categories,
                fill='toself',
                name='Humidity',
                line_color='purple'
            ))
            
            radar_fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )
                ),
                title="Seasonal Weather Patterns (Normalized)",
                showlegend=True
            )
            
            st.plotly_chart(radar_fig, use_container_width=True)
            
            st.markdown("**Note:** Values are normalized to show relative seasonal patterns. Each parameter is scaled to its maximum value.")
    
    # Download options
    st.subheader("Download Historical Data")
    
    download_col1, download_col2 = st.columns(2)
    
    with download_col1:
        st.download_button(
            label="Download Raw Data (CSV)",
            data=weather_df.to_csv(index=False).encode('utf-8'),
            file_name=f"{hist_location.replace(' ', '_')}_weather_data.csv",
            mime="text/csv"
        )
    
    with download_col2:
        st.download_button(
            label="Download Report (PDF)",
            data="This would be a PDF report in a real application",
            file_name=f"{hist_location.replace(' ', '_')}_weather_report.pdf",
            mime="application/pdf"
        )

with tab3:
    st.header("Weather Alerts & Notifications")
    
    # Create columns for settings
    alert_col1, alert_col2 = st.columns(2)
    
    with alert_col1:
        st.subheader("Current Alerts")
        
        # Create sample alerts
        alerts = [
            {"severity": "High", "type": "Heavy Rain", "location": "Punjab", "description": "Heavy rainfall expected in the next 48 hours. 50-80mm precipitation possible, which may cause localized flooding.", "date": "2023-10-16"},
            {"severity": "Medium", "type": "Heat Wave", "location": "Sindh", "description": "Temperatures expected to reach 40-42°C for the next 3-4 days. Take precautions for crops and livestock.", "date": "2023-10-15"},
            {"severity": "Low", "type": "Strong Winds", "location": "Balochistan", "description": "Wind speeds of 30-40 km/h expected, which may affect spraying operations and cause mechanical damage to standing crops.", "date": "2023-10-14"},
            {"severity": "Medium", "type": "Frost Warning", "location": "Northern Areas", "description": "Overnight temperatures expected to drop below freezing. Protect sensitive crops and irrigation systems.", "date": "2023-10-13"}
        ]
        
        # Convert to DataFrame
        alert_df = pd.DataFrame(alerts)
        
        # Function to apply styling based on severity
        def highlight_severity(s):
            styles = []
            for val in s:
                if val == "High":
                    styles.append('background-color: #f8d7da; color: #721c24')
                elif val == "Medium":
                    styles.append('background-color: #fff3cd; color: #856404')
                elif val == "Low":
                    styles.append('background-color: #d1ecf1; color: #0c5460')
                else:
                    styles.append('')
            return styles
        
        # Display styled dataframe
        st.dataframe(
            alert_df.style.apply(highlight_severity, subset=['severity']),
            use_container_width=True,
            hide_index=True
        )
        
        # Display detailed alerts in expandable sections
        for i, alert in enumerate(alerts):
            with st.expander(f"{alert['severity']} Alert: {alert['type']} - {alert['date']}"):
                st.markdown(f"**Location:** {alert['location']}")
                st.markdown(f"**Description:** {alert['description']}")
                
                # Add action recommendations based on alert type
                st.markdown("### Recommended Actions")
                
                if alert['type'] == "Heavy Rain":
                    st.markdown("""
                    - Ensure proper drainage in fields to prevent waterlogging
                    - Delay fertilizer application until after rainfall
                    - Secure farm equipment and harvest any ready crops if possible
                    - Check livestock shelters and provide adequate protection
                    """)
                elif alert['type'] == "Heat Wave":
                    st.markdown("""
                    - Increase irrigation frequency but reduce volume per application
                    - Apply irrigation during early morning or evening
                    - Consider shade cloth for sensitive crops
                    - Ensure adequate water for livestock
                    - Delay spraying operations to avoid chemical burn
                    """)
                elif alert['type'] == "Strong Winds":
                    st.markdown("""
                    - Delay spraying and fertilizer application
                    - Provide support for tall crops and young trees
                    - Secure farm equipment and structures
                    - Ensure livestock have adequate shelter
                    """)
                elif alert['type'] == "Frost Warning":
                    st.markdown("""
                    - Cover sensitive crops with frost cloth or other protective material
                    - Irrigate fields in the evening to increase humidity and soil temperature
                    - Move potted plants to protected areas
                    - Drain irrigation equipment to prevent damage
                    - Ensure livestock have warm shelter
                    """)
                
                # Add impacts on specific crops
                st.markdown("### Potential Crop Impacts")
                
                if alert['type'] == "Heavy Rain":
                    st.markdown("""
                    - **Wheat:** Risk of lodging and fungal diseases. May delay planting operations.
                    - **Rice:** Generally beneficial but excessive water may cause overflow in paddies.
                    - **Cotton:** Increased risk of boll rot and delayed picking.
                    - **Vegetables:** Potential damage to tender crops and increased disease pressure.
                    """)
                elif alert['type'] == "Heat Wave":
                    st.markdown("""
                    - **Wheat:** If during grain filling, may cause shriveled grain and yield reduction.
                    - **Rice:** Can affect pollination if during flowering stage.
                    - **Cotton:** Generally tolerant but extreme heat can affect boll development.
                    - **Vegetables:** High risk of sun scald and reduced quality.
                    """)
                elif alert['type'] == "Strong Winds":
                    st.markdown("""
                    - **Wheat:** Risk of lodging if during heading stage.
                    - **Rice:** May cause lodging and grain shattering.
                    - **Cotton:** Potential physical damage to bolls and flowers.
                    - **Fruit trees:** Risk of fruit drop and branch damage.
                    """)
                elif alert['type'] == "Frost Warning":
                    st.markdown("""
                    - **Wheat:** Generally tolerant if past seedling stage.
                    - **Rice:** High sensitivity, can cause significant damage.
                    - **Vegetables:** Very sensitive, especially tomatoes, peppers, and cucurbits.
                    - **Fruit trees:** Can damage blossoms and reduce fruit set if during flowering.
                    """)
    
    with alert_col2:
        st.subheader("Alert Settings")
        
        # Create alert preferences form
        with st.form("alert_preferences"):
            st.markdown("### Notification Preferences")
            
            receive_alerts = st.toggle("Receive Weather Alerts", value=True)
            
            alert_types = st.multiselect(
                "Alert Types",
                ["Heavy Rainfall", "Drought", "Heat Wave", "Cold Wave", "Frost", "Strong Winds", "Hail", "Thunderstorms"],
                ["Heavy Rainfall", "Heat Wave", "Frost"]
            )
            
            min_severity = st.select_slider(
                "Minimum Alert Severity",
                options=["Low", "Medium", "High"],
                value="Medium"
            )
            
            notification_methods = st.multiselect(
                "Notification Methods",
                ["SMS", "Email", "App Notification", "WhatsApp"],
                ["SMS", "App Notification"]
            )
            
            alert_frequency = st.radio(
                "Alert Frequency",
                ["Immediate", "Daily Digest", "Weekly Summary"]
            )
            
            phone_number = st.text_input("Phone Number for SMS Alerts", value="+92 300 1234567")
            
            email = st.text_input("Email for Alerts", value="farmer@example.com")
            
            submit_button = st.form_submit_button("Save Preferences")
            
            if submit_button:
                st.success("Alert preferences updated successfully!")
        
        # Custom alert area
        st.subheader("Custom Weather Monitoring")
        
        with st.expander("Set Custom Weather Triggers"):
            st.markdown("Define specific weather conditions to receive alerts")
            
            trigger_type = st.selectbox(
                "Trigger Condition",
                ["Temperature Above", "Temperature Below", "Rainfall Above", "Wind Speed Above", "Humidity Below"]
            )
            
            if "Temperature" in trigger_type:
                threshold = st.slider("Temperature Threshold (°C)", min_value=0, max_value=50, value=35 if "Above" in trigger_type else 5)
            elif "Rainfall" in trigger_type:
                threshold = st.slider("Rainfall Threshold (mm/day)", min_value=5, max_value=100, value=30)
            elif "Wind" in trigger_type:
                threshold = st.slider("Wind Speed Threshold (km/h)", min_value=10, max_value=100, value=40)
            elif "Humidity" in trigger_type:
                threshold = st.slider("Humidity Threshold (%)", min_value=10, max_value=90, value=30)
            
            duration = st.selectbox(
                "Duration",
                ["Single Occurrence", "For 2+ Hours", "For 6+ Hours", "For 12+ Hours", "For 24+ Hours"]
            )
            
            specific_crop = st.selectbox(
                "For Specific Crop",
                ["All Crops", "Wheat", "Rice", "Cotton", "Sugarcane", "Maize", "Vegetables", "Fruits"]
            )
            
            st.button("Add Trigger")
        
        # Historical alerts
        st.subheader("Alert History")
        
        history_data = [
            {"date": "2023-09-25", "type": "Heavy Rain", "severity": "High", "action_taken": "Yes"},
            {"date": "2023-09-10", "type": "Heat Wave", "severity": "Medium", "action_taken": "Yes"},
            {"date": "2023-08-15", "type": "Strong Winds", "severity": "Medium", "action_taken": "No"},
            {"date": "2023-07-22", "type": "Drought Warning", "severity": "High", "action_taken": "Yes"},
            {"date": "2023-07-05", "type": "Heavy Rain", "severity": "Medium", "action_taken": "No"}
        ]
        
        history_df = pd.DataFrame(history_data)
        
        st.dataframe(history_df, use_container_width=True, hide_index=True)
        
        # Alert effectiveness
        alert_effectiveness = {
            "Received Alerts": 15,
            "Actions Taken": 12,
            "Prevented Damage": 10,
            "Estimated Savings": "PKR 350,000"
        }
        
        st.info(f"""
        **Alert Effectiveness Summary**
        
        In the last 3 months, you received {alert_effectiveness['Received Alerts']} weather alerts.
        You took action on {alert_effectiveness['Actions Taken']} of these alerts.
        An estimated {alert_effectiveness['Prevented Damage']} incidents of crop damage were prevented.
        Estimated savings: {alert_effectiveness['Estimated Savings']}
        """)

# Weather impact on agriculture section
st.header("Weather Impact on Agriculture")

impact_col1, impact_col2 = st.columns([2, 1])

with impact_col1:
    st.subheader("Crop-Specific Weather Sensitivity")
    
    # Create sample data for crop sensitivity to different weather parameters
    sensitivity_data = {
        'Crop': ['Wheat', 'Rice', 'Cotton', 'Sugarcane', 'Maize'],
        'Heat Sensitivity': [7, 8, 4, 5, 6],
        'Cold Sensitivity': [3, 9, 8, 7, 5],
        'Drought Sensitivity': [6, 9, 5, 7, 7],
        'Excess Rain Sensitivity': [7, 3, 8, 4, 6]
    }
    
    sensitivity_df = pd.DataFrame(sensitivity_data)
    
    # Create radar chart for each crop
    selected_crop = st.selectbox(
        "Select Crop",
        sensitivity_df['Crop'].tolist()
    )
    
    # Get data for selected crop
    crop_data = sensitivity_df[sensitivity_df['Crop'] == selected_crop].iloc[0]
    
    # Create radar chart
    categories = ['Heat Sensitivity', 'Cold Sensitivity', 'Drought Sensitivity', 'Excess Rain Sensitivity']
    values = [crop_data[cat] for cat in categories]
    
    # Add the first value again to close the loop
    values.append(values[0])
    categories.append(categories[0])
    
    sensitivity_fig = go.Figure()
    
    sensitivity_fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=selected_crop,
        line_color='green'
    ))
    
    sensitivity_fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )
        ),
        title=f"Weather Sensitivity Profile for {selected_crop}",
        showlegend=False
    )
    
    st.plotly_chart(sensitivity_fig, use_container_width=True)
    
    # Critical growth stages and weather needs
    st.subheader("Critical Growth Stages")
    
    growth_stages = {
        'Wheat': [
            {"stage": "Germination & Seedling", "temp": "15-20°C", "water": "25-30mm", "sensitivity": "Medium"},
            {"stage": "Tillering", "temp": "15-18°C", "water": "30-40mm", "sensitivity": "Medium"},
            {"stage": "Stem Extension", "temp": "18-22°C", "water": "40-50mm", "sensitivity": "Medium"},
            {"stage": "Heading & Flowering", "temp": "18-22°C", "water": "50-60mm", "sensitivity": "High"},
            {"stage": "Grain Filling", "temp": "20-25°C", "water": "40-50mm", "sensitivity": "High"},
            {"stage": "Ripening", "temp": "25-30°C", "water": "20-30mm", "sensitivity": "Low"}
        ],
        'Rice': [
            {"stage": "Seedling", "temp": "25-30°C", "water": "Saturated", "sensitivity": "Medium"},
            {"stage": "Tillering", "temp": "25-32°C", "water": "5-10cm depth", "sensitivity": "Medium"},
            {"stage": "Panicle Initiation", "temp": "25-35°C", "water": "5-10cm depth", "sensitivity": "High"},
            {"stage": "Flowering", "temp": "30-32°C", "water": "5-10cm depth", "sensitivity": "Very High"},
            {"stage": "Grain Filling", "temp": "25-30°C", "water": "5-10cm depth", "sensitivity": "High"},
            {"stage": "Ripening", "temp": "25-30°C", "water": "Draining", "sensitivity": "Low"}
        ],
        'Cotton': [
            {"stage": "Germination & Emergence", "temp": "18-30°C", "water": "25-30mm", "sensitivity": "Medium"},
            {"stage": "Seedling", "temp": "20-35°C", "water": "30-40mm", "sensitivity": "Medium"},
            {"stage": "Squaring", "temp": "25-35°C", "water": "40-50mm", "sensitivity": "High"},
            {"stage": "Flowering", "temp": "25-35°C", "water": "50-60mm", "sensitivity": "Very High"},
            {"stage": "Boll Development", "temp": "25-35°C", "water": "50-60mm", "sensitivity": "High"},
            {"stage": "Boll Opening", "temp": "25-35°C", "water": "30-40mm", "sensitivity": "Low"}
        ],
        'Sugarcane': [
            {"stage": "Germination", "temp": "25-32°C", "water": "40-50mm", "sensitivity": "Medium"},
            {"stage": "Tillering", "temp": "25-35°C", "water": "50-60mm", "sensitivity": "Medium"},
            {"stage": "Grand Growth", "temp": "25-35°C", "water": "60-70mm", "sensitivity": "High"},
            {"stage": "Maturation", "temp": "20-30°C", "water": "40-50mm", "sensitivity": "Medium"}
        ],
        'Maize': [
            {"stage": "Germination & Emergence", "temp": "15-30°C", "water": "25-30mm", "sensitivity": "Medium"},
            {"stage": "Vegetative", "temp": "20-30°C", "water": "40-50mm", "sensitivity": "Medium"},
            {"stage": "Tasseling", "temp": "20-30°C", "water": "50-60mm", "sensitivity": "High"},
            {"stage": "Silking & Pollination", "temp": "20-30°C", "water": "50-60mm", "sensitivity": "Very High"},
            {"stage": "Grain Filling", "temp": "20-30°C", "water": "40-50mm", "sensitivity": "High"},
            {"stage": "Maturity", "temp": "20-30°C", "water": "30-40mm", "sensitivity": "Low"}
        ]
    }
    
    if selected_crop in growth_stages:
        # Convert to DataFrame
        stages_df = pd.DataFrame(growth_stages[selected_crop])
        
        # Function to apply styling based on sensitivity
        def highlight_sensitivity(s):
            styles = []
            for val in s:
                if val == "Very High":
                    styles.append('background-color: #f8d7da; color: #721c24')
                elif val == "High":
                    styles.append('background-color: #fff3cd; color: #856404')
                elif val == "Medium":
                    styles.append('background-color: #d1ecf1; color: #0c5460')
                elif val == "Low":
                    styles.append('background-color: #d4edda; color: #155724')
                else:
                    styles.append('')
            return styles
        
        # Display styled dataframe
        st.dataframe(
            stages_df.style.apply(highlight_sensitivity, subset=['sensitivity']),
            use_container_width=True,
            hide_index=True
        )
        
        # Display growth stage specific advice
        stage_options = [stage["stage"] for stage in growth_stages[selected_crop]]
        selected_stage = st.selectbox("Select Growth Stage for Weather Advice", stage_options)
        
        # Find the selected stage
        stage_data = next((stage for stage in growth_stages[selected_crop] if stage["stage"] == selected_stage), None)
        
        if stage_data:
            st.markdown(f"### Weather Management for {selected_crop} during {selected_stage}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Temperature Management")
                
                temp_range = stage_data["temp"].split("-")
                optimal_min = int(temp_range[0].replace("°C", ""))
                optimal_max = int(temp_range[1].replace("°C", ""))
                
                st.markdown(f"**Optimal Temperature:** {stage_data['temp']}")
                
                st.markdown("**If temperatures are too high:**")
                if selected_crop == "Rice":
                    st.markdown("""
                    - Maintain higher water levels to buffer temperature
                    - Apply overhead sprinkling during extreme heat if available
                    - Consider evening/night irrigation to cool the crop
                    """)
                else:
                    st.markdown("""
                    - Increase irrigation frequency but reduce volume
                    - Apply irrigation during cooler parts of the day
                    - Apply mulch to reduce soil temperature
                    - Consider shade cloth for high-value crops
                    """)
                
                st.markdown("**If temperatures are too low:**")
                if selected_crop in ["Cotton", "Rice", "Sugarcane"]:
                    st.markdown("""
                    - Delay planting until soil temperatures are adequate
                    - Use plastic mulch to warm soil
                    - Apply irrigation during day to moderate temperature
                    - Protect young plants with row covers if available
                    """)
                else:
                    st.markdown("""
                    - Select cold-tolerant varieties
                    - Apply adequate phosphorus fertilizer
                    - Maintain optimal soil moisture
                    - Avoid waterlogging which increases cold damage
                    """)
            
            with col2:
                st.markdown("#### Water Management")
                
                if "depth" in stage_data["water"]:
                    st.markdown(f"**Optimal Water Level:** {stage_data['water']}")
                else:
                    st.markdown(f"**Optimal Water Requirement:** {stage_data['water']} per week")
                
                st.markdown("**During drought conditions:**")
                if selected_crop == "Rice":
                    st.markdown("""
                    - Maintain minimum water depth (2-3cm)
                    - Consider alternate wetting and drying irrigation
                    - Apply additional potassium to improve drought tolerance
                    - Monitor carefully for increased pest pressure
                    """)
                else:
                    st.markdown("""
                    - Prioritize irrigation during this critical stage
                    - Apply irrigation during early morning or evening
                    - Consider deficit irrigation in less sensitive stages
                    - Apply mulch to conserve soil moisture
                    """)
                
                st.markdown("**During excessive rainfall:**")
                if selected_crop == "Rice":
                    st.markdown("""
                    - Ensure drainage systems are functioning properly
                    - Monitor water depth and remove excess water
                    - Watch for increased disease pressure
                    - Consider additional nitrogen application after heavy rains
                    """)
                else:
                    st.markdown("""
                    - Ensure adequate drainage
                    - Delay additional irrigation
                    - Monitor for disease development
                    - Consider raised beds for future plantings
                    """)
    else:
        st.info(f"Detailed growth stage information not available for {selected_crop}")

with impact_col2:
    st.subheader("Weather-Based Recommendations")
    
    # Create a current status summary
    st.markdown("### Current Status")
    
    # Show a random image
    st.image(
        get_random_image("agricultural_drone_imagery"),
        caption="Recent farm conditions",
        use_column_width=True
    )
    
    # Create mock data for current conditions
    current_status = {
        "Temperature": "32°C (Above optimal)",
        "Rainfall (Last 7 days)": "5mm (Below optimal)",
        "Soil Moisture": "60% (Optimal)",
        "Growing Degree Days": "1,250 (On target)"
    }
    
    for key, value in current_status.items():
        st.markdown(f"**{key}:** {value}")
    
    # Create recommendations based on weather and crop
    st.markdown("### Immediate Recommendations")
    
    st.info("""
    **Irrigation Adjustment:**
    - Increase irrigation by 15% due to high temperatures
    - Schedule irrigation for early morning to reduce evaporation
    - Monitor soil moisture closely in northern fields
    
    **Field Operations:**
    - Suitable conditions for fertilizer application
    - Good spraying conditions in early morning (low wind)
    - Consider foliar application of potassium to improve heat tolerance
    
    **Pest & Disease Watch:**
    - Increased risk of spider mites due to hot, dry conditions
    - Monitor for early signs of leaf spot diseases
    - Consider preventative fungicide for high-value crops
    """)
    
    # Weather risk assessment
    st.markdown("### 7-Day Risk Assessment")
    
    risk_data = {
        'Risk Factor': ['Heat Stress', 'Water Deficit', 'Disease Pressure', 'Pest Pressure'],
        'Risk Level': ['High', 'Medium', 'Low', 'Medium-High']
    }
    
    risk_df = pd.DataFrame(risk_data)
    
    # Function to apply styling based on risk level
    def highlight_risk(s):
        styles = []
        for val in s:
            if val == "High":
                styles.append('background-color: #f8d7da; color: #721c24')
            elif "Medium-High" in val:
                styles.append('background-color: #ffeeba; color: #856404')
            elif val == "Medium":
                styles.append('background-color: #fff3cd; color: #856404')
            elif val == "Low":
                styles.append('background-color: #d4edda; color: #155724')
            else:
                styles.append('')
        return styles
    
    # Display styled dataframe
    st.dataframe(
        risk_df.style.apply(highlight_risk, subset=['Risk Level']),
        use_container_width=True,
        hide_index=True
    )
    
    # Long-term seasonal outlook
    st.markdown("### Seasonal Outlook")
    
    st.warning("""
    **Next 30 Days:**
    
    Temperatures are expected to remain 2-3°C above normal with below-average precipitation. Consider:
    
    - Implementing water conservation strategies
    - Adjusting planting dates for upcoming crops
    - Increased monitoring for heat-related stress
    - Preparing irrigation infrastructure for increased demand
    """)

# Download and resources section
st.markdown("---")
st.header("Weather Resources and Tools")

resource_col1, resource_col2, resource_col3 = st.columns(3)

with resource_col1:
    st.subheader("Weather Calendar")
    st.markdown("""
    Download our detailed agricultural weather calendar with key dates and weather expectations for major crops in Pakistan.
    """)
    st.download_button(
        label="Download Weather Calendar",
        data="This would be a PDF calendar in a real application",
        file_name="agricultural_weather_calendar.pdf",
        mime="application/pdf"
    )

with resource_col2:
    st.subheader("Weather-Smart Farming Guide")
    st.markdown("""
    Our comprehensive guide to weather-smart farming practices tailored for Pakistani agricultural conditions.
    """)
    st.download_button(
        label="Download Farming Guide",
        data="This would be a PDF guide in a real application",
        file_name="weather_smart_farming_guide.pdf",
        mime="application/pdf"
    )

with resource_col3:
    st.subheader("Connect with Weather Expert")
    st.markdown("""
    Schedule a consultation with an agricultural meteorologist to discuss specific weather-related challenges.
    """)
    st.link_button("Schedule Consultation", "https://example.com/consult")

