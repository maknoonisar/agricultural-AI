import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_crop_health_chart():
    """
    Create a chart showing crop health metrics over time.
    
    Returns:
    Figure: Plotly figure with crop health visualization
    """
    # Create sample data for crop health over time
    dates = pd.date_range(end=datetime.now(), periods=30)
    
    # Different health patterns for different crops
    wheat_health = [75 + 10 * np.sin(i/5) + np.random.normal(0, 2) for i in range(30)]
    rice_health = [70 + 8 * np.sin(i/4 + 2) + np.random.normal(0, 2) for i in range(30)]
    cotton_health = [65 + 15 * np.sin(i/6 + 4) + np.random.normal(0, 3) for i in range(30)]
    
    # Create DataFrame
    health_data = {
        'Date': dates,
        'Wheat': wheat_health,
        'Rice': rice_health,
        'Cotton': cotton_health
    }
    
    health_df = pd.DataFrame(health_data)
    
    # Melt the dataframe for better visualization
    health_df_melted = pd.melt(
        health_df, 
        id_vars=['Date'], 
        value_vars=['Wheat', 'Rice', 'Cotton'],
        var_name='Crop', 
        value_name='Health Score'
    )
    
    # Create the line chart
    fig = px.line(
        health_df_melted,
        x='Date',
        y='Health Score',
        color='Crop',
        markers=True,
        title='Crop Health Trends (Last 30 Days)'
    )
    
    # Update layout for better appearance
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Health Score (0-100)',
        yaxis=dict(range=[50, 100]),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_yield_chart():
    """
    Create a chart showing yield trends and forecasts.
    
    Returns:
    Figure: Plotly figure with yield visualization
    """
    # Create sample data for historical yield
    years = [2018, 2019, 2020, 2021, 2022, 2023]
    
    # Different yield patterns for different crops
    wheat_yield = [3.2, 3.3, 3.4, 3.3, 3.5, 3.7]
    rice_yield = [3.8, 3.9, 4.0, 3.9, 4.0, 4.2]
    cotton_yield = [2.2, 2.3, 2.4, 2.2, 2.4, 2.5]
    
    # Create forecast for 2024
    forecast_year = 2024
    wheat_forecast = 3.8
    rice_forecast = 4.3
    cotton_forecast = 2.6
    
    # Combine historical and forecast data
    all_years = years + [forecast_year]
    all_wheat = wheat_yield + [wheat_forecast]
    all_rice = rice_yield + [rice_forecast]
    all_cotton = cotton_yield + [cotton_forecast]
    
    # Create DataFrame
    yield_data = {
        'Year': all_years,
        'Wheat': all_wheat,
        'Rice': all_rice,
        'Cotton': all_cotton,
        'Type': ['Historical'] * len(years) + ['Forecast']
    }
    
    yield_df = pd.DataFrame(yield_data)
    
    # Melt the dataframe for better visualization
    yield_df_melted = pd.melt(
        yield_df, 
        id_vars=['Year', 'Type'], 
        value_vars=['Wheat', 'Rice', 'Cotton'],
        var_name='Crop', 
        value_name='Yield (tons/acre)'
    )
    
    # Create the line chart
    fig = px.line(
        yield_df_melted,
        x='Year',
        y='Yield (tons/acre)',
        color='Crop',
        markers=True,
        title='Historical Yield Trends and Forecast',
        line_dash='Type'
    )
    
    # Update layout for better appearance
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Yield (tons/acre)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Add annotations for forecast
    for crop, yield_val in zip(['Wheat', 'Rice', 'Cotton'], [wheat_forecast, rice_forecast, cotton_forecast]):
        fig.add_annotation(
            x=forecast_year,
            y=yield_val,
            text=f"{crop}: {yield_val}",
            showarrow=True,
            arrowhead=1,
            ax=40,
            ay=-40
        )
    
    return fig

def create_weather_chart(weather_data=None):
    """
    Create a chart showing weather patterns.
    
    Parameters:
    weather_data (DataFrame, optional): Weather data to visualize
    
    Returns:
    Figure: Plotly figure with weather visualization
    """
    if weather_data is None or weather_data.empty:
        # Create sample weather data
        dates = pd.date_range(end=datetime.now(), periods=30)
        max_temp = [32 + 5 * np.sin(i/5) + np.random.normal(0, 1) for i in range(30)]
        min_temp = [20 + 5 * np.sin(i/5) + np.random.normal(0, 1) for i in range(30)]
        rainfall = [0] * 30
        
        # Add some rainfall events
        for i in [5, 6, 15, 16, 25]:
            rainfall[i] = np.random.randint(5, 20)
        
        weather_data = pd.DataFrame({
            'Date': dates,
            'Max Temperature (°C)': max_temp,
            'Min Temperature (°C)': min_temp,
            'Rainfall (mm)': rainfall
        })
    
    # Create the figure
    fig = go.Figure()
    
    # Add temperature lines
    fig.add_trace(go.Scatter(
        x=weather_data['Date'],
        y=weather_data['Max Temperature (°C)'],
        name='Max Temp',
        line=dict(color='red', width=2),
        mode='lines+markers'
    ))
    
    fig.add_trace(go.Scatter(
        x=weather_data['Date'],
        y=weather_data['Min Temperature (°C)'],
        name='Min Temp',
        line=dict(color='blue', width=2),
        mode='lines+markers'
    ))
    
    # Add rainfall bars
    fig.add_trace(go.Bar(
        x=weather_data['Date'],
        y=weather_data['Rainfall (mm)'],
        name='Rainfall',
        marker_color='skyblue',
        yaxis='y2'
    ))
    
    # Update layout
    fig.update_layout(
        title='Weather Patterns (Last 30 Days)',
        xaxis_title='Date',
        yaxis=dict(
            title='Temperature (°C)',
            title_font=dict(color='red'),
            tickfont=dict(color='red')
        ),
        yaxis2=dict(
            title='Rainfall (mm)',
            title_font=dict(color='blue'),
            tickfont=dict(color='blue'),
            anchor='x',
            overlaying='y',
            side='right'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_resource_usage_chart():
    """
    Create a chart showing resource usage.
    
    Returns:
    Figure: Plotly figure with resource usage visualization
    """
    # Create sample data for resource usage
    resources = ['Water', 'Fertilizer', 'Pesticides', 'Labor', 'Energy']
    current = [75, 60, 40, 85, 55]
    optimal = [65, 55, 35, 80, 50]
    
    # Create DataFrame
    resource_data = {
        'Resource': resources,
        'Current Usage': current,
        'Optimal Usage': optimal
    }
    
    resource_df = pd.DataFrame(resource_data)
    
    # Calculate efficiency
    resource_df['Efficiency (%)'] = (resource_df['Optimal Usage'] / resource_df['Current Usage'] * 100).round(1)
    
    # Create the bar chart
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
    
    # Add efficiency line
    fig.add_trace(go.Scatter(
        x=resource_df['Resource'],
        y=resource_df['Efficiency (%)'],
        mode='lines+markers',
        name='Efficiency (%)',
        marker=dict(size=8, color='red'),
        line=dict(width=2, dash='dot'),
        yaxis='y2'
    ))
    
    # Update layout
    fig.update_layout(
        title='Resource Usage vs. Optimal Levels',
        xaxis_title='Resource',
        yaxis=dict(
            title='Usage (relative units)',
            title_font=dict(color='blue'),
            tickfont=dict(color='blue')
        ),
        yaxis2=dict(
            title='Efficiency (%)',
            title_font=dict(color='red'),
            tickfont=dict(color='red'),
            anchor='x',
            overlaying='y',
            side='right',
            range=[0, 120]
        ),
        barmode='group',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig