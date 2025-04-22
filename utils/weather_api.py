import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_weather_forecast(location="Lahore", days=7):
    """
    Get weather forecast for a location.
    In a production environment, this would connect to a weather API.
    
    Parameters:
    location (str): Location for forecast
    days (int): Number of days to forecast
    
    Returns:
    DataFrame: Pandas DataFrame containing forecast data
    """
    # In a real application, this would call a weather API
    # For demonstration, we'll return simulated results
    
    # Generate dates for the forecast
    dates = [datetime.now() + timedelta(days=i) for i in range(days)]
    
    # Different weather patterns based on location
    if location in ["Lahore", "Faisalabad", "Multan"]:
        # Hot and occasionally rainy
        max_temps = [32 + np.random.normal(0, 2) for _ in range(days)]
        min_temps = [24 + np.random.normal(0, 2) for _ in range(days)]
        precip_prob = [5 + i*5 + np.random.normal(0, 5) for i in range(days)]
        precip_prob = [max(0, min(100, p)) for p in precip_prob]  # Bound between 0-100
        
        # Generate conditions based on precipitation probability
        conditions = []
        for prob in precip_prob:
            if prob < 10:
                conditions.append("Sunny")
            elif prob < 30:
                conditions.append("Partly Cloudy")
            elif prob < 60:
                conditions.append("Cloudy")
            else:
                conditions.append("Light Rain")
    
    elif location == "Karachi":
        # Hot and humid
        max_temps = [34 + np.random.normal(0, 1.5) for _ in range(days)]
        min_temps = [27 + np.random.normal(0, 1.5) for _ in range(days)]
        precip_prob = [max(0, min(100, 5 + np.random.normal(0, 5))) for _ in range(days)]
        
        # Generate conditions
        conditions = []
        for prob in precip_prob:
            if prob < 10:
                conditions.append("Sunny")
            elif prob < 30:
                conditions.append("Partly Cloudy")
            else:
                conditions.append("Cloudy")
    
    else:
        # Other locations (default pattern)
        max_temps = [30 + np.random.normal(0, 3) for _ in range(days)]
        min_temps = [22 + np.random.normal(0, 3) for _ in range(days)]
        precip_prob = [20 + i*5 + np.random.normal(0, 10) for i in range(days)]
        precip_prob = [max(0, min(100, p)) for p in precip_prob]
        
        # Generate conditions
        conditions = []
        for prob in precip_prob:
            if prob < 10:
                conditions.append("Sunny")
            elif prob < 30:
                conditions.append("Partly Cloudy")
            elif prob < 60:
                conditions.append("Cloudy")
            elif prob < 80:
                conditions.append("Light Rain")
            else:
                conditions.append("Rain")
    
    # Create humidity values (higher when precipitation probability is higher)
    humidity = [max(50, min(95, 50 + prob/2 + np.random.normal(0, 5))) for prob in precip_prob]
    
    # Create wind speed values
    wind_speed = [5 + np.random.normal(0, 2) for _ in range(days)]
    wind_speed = [max(0, w) for w in wind_speed]
    
    # Create DataFrame
    forecast_data = {
        'Date': dates,
        'Day': [d.strftime('%a') for d in dates],
        'Max Temp (°C)': max_temps,
        'Min Temp (°C)': min_temps,
        'Precipitation (%)': precip_prob,
        'Conditions': conditions,
        'Humidity (%)': humidity,
        'Wind Speed (km/h)': wind_speed
    }
    
    return pd.DataFrame(forecast_data)

def get_historical_weather(location="Lahore", days=30):
    """
    Get historical weather data for a location.
    In a production environment, this would connect to a weather API or database.
    
    Parameters:
    location (str): Location for historical data
    days (int): Number of days of historical data
    
    Returns:
    DataFrame: Pandas DataFrame containing historical weather data
    """
    # In a real application, this would call a weather API or database
    # For demonstration, we'll return simulated results
    
    # Generate dates for the historical data (going backward from yesterday)
    end_date = datetime.now() - timedelta(days=1)
    dates = [end_date - timedelta(days=i) for i in range(days)]
    dates.reverse()  # Put in chronological order
    
    # Different weather patterns based on location
    if location in ["Lahore", "Faisalabad", "Multan"]:
        # Create temperature patterns with seasonal trends and daily noise
        base_temp = 30  # Base temperature
        season_amplitude = 5  # Seasonal variation
        daily_noise = 2  # Daily random variation
        
        # Create smooth seasonal pattern with some randomness
        max_temps = [base_temp + season_amplitude * np.sin(i/30*np.pi) + np.random.normal(0, daily_noise) for i in range(days)]
        min_temps = [base_temp - 8 + season_amplitude * np.sin(i/30*np.pi) + np.random.normal(0, daily_noise) for i in range(days)]
        
        # Create rainfall with occasional rain events
        rainfall = [0] * days
        for i in range(days):
            if np.random.random() < 0.15:  # 15% chance of rain on any day
                rainfall[i] = np.random.exponential(10)  # Exponential distribution for rainfall amounts
        
        # Higher humidity on and after rainy days
        humidity = [50 + np.random.normal(0, 5) for _ in range(days)]
        for i in range(days):
            if rainfall[i] > 0:
                humidity[i] = min(95, humidity[i] + rainfall[i] * 2)
                # Also increase humidity for the next day
                if i < days - 1:
                    humidity[i+1] = min(95, humidity[i+1] + rainfall[i])
    
    elif location == "Karachi":
        # Hotter, less seasonal variation, less rainfall
        base_temp = 33
        season_amplitude = 3
        daily_noise = 1.5
        
        max_temps = [base_temp + season_amplitude * np.sin(i/30*np.pi) + np.random.normal(0, daily_noise) for i in range(days)]
        min_temps = [base_temp - 7 + season_amplitude * np.sin(i/30*np.pi) + np.random.normal(0, daily_noise) for i in range(days)]
        
        rainfall = [0] * days
        for i in range(days):
            if np.random.random() < 0.08:  # 8% chance of rain
                rainfall[i] = np.random.exponential(5)  # Less rainfall when it does rain
        
        humidity = [60 + np.random.normal(0, 8) for _ in range(days)]
        for i in range(days):
            if rainfall[i] > 0:
                humidity[i] = min(95, humidity[i] + rainfall[i] * 2)
                if i < days - 1:
                    humidity[i+1] = min(95, humidity[i+1] + rainfall[i])
    
    else:
        # Generic pattern for other locations
        base_temp = 28
        season_amplitude = 4
        daily_noise = 2.5
        
        max_temps = [base_temp + season_amplitude * np.sin(i/30*np.pi) + np.random.normal(0, daily_noise) for i in range(days)]
        min_temps = [base_temp - 8 + season_amplitude * np.sin(i/30*np.pi) + np.random.normal(0, daily_noise) for i in range(days)]
        
        rainfall = [0] * days
        for i in range(days):
            if np.random.random() < 0.25:  # 25% chance of rain
                rainfall[i] = np.random.exponential(15)  # More rainfall when it does rain
        
        humidity = [55 + np.random.normal(0, 10) for _ in range(days)]
        for i in range(days):
            if rainfall[i] > 0:
                humidity[i] = min(95, humidity[i] + rainfall[i] * 2)
                if i < days - 1:
                    humidity[i+1] = min(95, humidity[i+1] + rainfall[i])
    
    # Create DataFrame
    historical_data = {
        'Date': dates,
        'Max Temperature (°C)': max_temps,
        'Min Temperature (°C)': min_temps,
        'Rainfall (mm)': rainfall,
        'Humidity (%)': humidity
    }
    
    return pd.DataFrame(historical_data)

def get_agricultural_weather_metrics(weather_data):
    """
    Calculate agricultural weather metrics from weather data.
    
    Parameters:
    weather_data (DataFrame): Weather data containing temperature and rainfall
    
    Returns:
    dict: Dictionary of agricultural weather metrics
    """
    if weather_data is None or weather_data.empty:
        return {"error": "No weather data available"}
    
    metrics = {}
    
    try:
        # Calculate Growing Degree Days (GDD) with base temperature of 10°C
        if all(col in weather_data.columns for col in ['Max Temperature (°C)', 'Min Temperature (°C)']):
            # Calculate average daily temperature
            weather_data['Avg Temp'] = (weather_data['Max Temperature (°C)'] + weather_data['Min Temperature (°C)']) / 2
            
            # Calculate GDD
            weather_data['GDD'] = weather_data['Avg Temp'].apply(lambda x: max(0, x - 10))
            
            metrics['gdd_sum'] = round(weather_data['GDD'].sum(), 1)
            metrics['gdd_avg'] = round(weather_data['GDD'].mean(), 1)
        
        # Calculate rainfall metrics
        if 'Rainfall (mm)' in weather_data.columns:
            metrics['total_rainfall'] = round(weather_data['Rainfall (mm)'].sum(), 1)
            metrics['rainy_days'] = int((weather_data['Rainfall (mm)'] > 0.5).sum())
            
            # Calculate dry spells (consecutive days with < 1mm rain)
            rainfall_series = weather_data['Rainfall (mm)'] < 1
            dry_spell = 0
            max_dry_spell = 0
            
            for is_dry in rainfall_series:
                if is_dry:
                    dry_spell += 1
                    max_dry_spell = max(max_dry_spell, dry_spell)
                else:
                    dry_spell = 0
            
            metrics['max_dry_spell'] = max_dry_spell
        
        # Calculate heat stress days (days above 35°C)
        if 'Max Temperature (°C)' in weather_data.columns:
            metrics['heat_stress_days'] = int((weather_data['Max Temperature (°C)'] > 35).sum())
        
        # Calculate cold stress days (days below 5°C)
        if 'Min Temperature (°C)' in weather_data.columns:
            metrics['cold_stress_days'] = int((weather_data['Min Temperature (°C)'] < 5).sum())
        
        # Calculate reference evapotranspiration (simplified calculation)
        if all(col in weather_data.columns for col in ['Max Temperature (°C)', 'Min Temperature (°C)', 'Humidity (%)']):
            # Simplified ET0 calculation based on temperature
            weather_data['ET0'] = 0.0023 * (weather_data['Max Temperature (°C)'] + 17.8) * \
                                 (weather_data['Max Temperature (°C)'] - weather_data['Min Temperature (°C)'])**0.5
            
            metrics['total_et0'] = round(weather_data['ET0'].sum(), 1)
            metrics['avg_et0'] = round(weather_data['ET0'].mean(), 1)
        
        return metrics
    
    except Exception as e:
        return {"error": f"Error calculating agricultural metrics: {str(e)}"}

def get_weather_alert_level(forecast_data):
    """
    Determine weather alert level based on forecast.
    
    Parameters:
    forecast_data (DataFrame): Weather forecast data
    
    Returns:
    dict: Alert information including level and description
    """
    if forecast_data is None or forecast_data.empty:
        return {"level": "Unknown", "description": "No forecast data available"}
    
    try:
        # Check for heavy rainfall (> 20mm predicted)
        heavy_rain = any(
            'Rain' in condition and prob > 80 
            for condition, prob in zip(forecast_data['Conditions'], forecast_data['Precipitation (%)'])
        )
        
        # Check for heat wave (consecutive days above 40°C)
        heat_wave = False
        consecutive_hot_days = 0
        
        for temp in forecast_data['Max Temp (°C)']:
            if temp > 40:
                consecutive_hot_days += 1
                if consecutive_hot_days >= 3:
                    heat_wave = True
                    break
            else:
                consecutive_hot_days = 0
        
        # Check for frost risk (min temp below 2°C)
        frost_risk = any(temp < 2 for temp in forecast_data['Min Temp (°C)'])
        
        # Check for severe weather patterns
        if heavy_rain:
            return {
                "level": "High",
                "description": "Heavy rainfall expected. Potential for flooding and waterlogging.",
                "recommendations": [
                    "Ensure proper drainage in fields",
                    "Delay irrigation",
                    "Postpone fertilizer application",
                    "Secure farm equipment"
                ]
            }
        elif heat_wave:
            return {
                "level": "High",
                "description": "Heat wave conditions expected. Risk of crop stress and increased water needs.",
                "recommendations": [
                    "Increase irrigation frequency",
                    "Apply irrigation during cooler parts of day",
                    "Consider temporary shading for sensitive crops",
                    "Monitor for heat stress symptoms"
                ]
            }
        elif frost_risk:
            return {
                "level": "High",
                "description": "Frost risk detected. Potential damage to sensitive crops.",
                "recommendations": [
                    "Prepare frost protection measures",
                    "Irrigate before frost event",
                    "Use crop covers where applicable",
                    "Delay planting of new crops"
                ]
            }
        
        # Check for moderate alert conditions
        high_wind_days = sum(speed > 30 for speed in forecast_data['Wind Speed (km/h)'])
        moderate_rain_days = sum(
            'Rain' in condition or prob > 60 
            for condition, prob in zip(forecast_data['Conditions'], forecast_data['Precipitation (%)'])
        )
        hot_days = sum(temp > 38 for temp in forecast_data['Max Temp (°C)'])
        
        if high_wind_days >= 2 or moderate_rain_days >= 3 or hot_days >= 4:
            return {
                "level": "Medium",
                "description": "Potentially challenging weather conditions expected.",
                "recommendations": [
                    "Monitor crops closely",
                    "Adjust irrigation schedules as needed",
                    "Be prepared to adapt field operations"
                ]
            }
        
        # Default to low alert level
        return {
            "level": "Low",
            "description": "No significant weather concerns in the forecast period.",
            "recommendations": [
                "Continue normal farm operations",
                "Monitor weather updates regularly"
            ]
        }
        
    except Exception as e:
        return {"level": "Unknown", "description": f"Error analyzing forecast: {str(e)}"}