import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def load_sample_data(data_type):
    """
    Load sample data for various use cases in the application.
    In a production environment, this would connect to a database or API.
    
    Parameters:
    data_type (str): Type of data to load ('crop_data', 'weather_data', 'soil_data', etc.)
    
    Returns:
    DataFrame: Pandas DataFrame containing the requested data
    """
    
    # Sample data for crop health
    if data_type == "crop_health":
        # Create sample crop health data
        fields = ["North Field", "South Field", "East Field", "West Field"]
        crops = ["Wheat", "Rice", "Cotton", "Sugarcane"]
        health_scores = [85, 75, 60, 80]
        ndvi_values = [0.85, 0.75, 0.60, 0.80]
        stress_indices = [15, 25, 40, 20]
        pest_risk = ["Low", "Medium", "High", "Low"]
        disease_risk = ["Low", "Medium", "High", "Medium"]
        
        data = {
            "Field": fields,
            "Crop": crops,
            "Health Score": health_scores,
            "NDVI": ndvi_values,
            "Stress Index": stress_indices,
            "Pest Risk": pest_risk,
            "Disease Risk": disease_risk
        }
        
        return pd.DataFrame(data)
    
    # Sample data for crop yields
    elif data_type == "yield_data":
        # Create sample yield data
        years = list(range(2018, 2024))
        wheat_yield = [3.2, 3.3, 3.4, 3.3, 3.5, 3.7]
        rice_yield = [3.8, 3.9, 4.0, 3.9, 4.0, 4.2]
        cotton_yield = [2.2, 2.3, 2.4, 2.2, 2.4, 2.5]
        
        data = {
            "Year": years,
            "Wheat Yield (tons/acre)": wheat_yield,
            "Rice Yield (tons/acre)": rice_yield,
            "Cotton Yield (tons/acre)": cotton_yield
        }
        
        return pd.DataFrame(data)
    
    # Sample data for weather data
    elif data_type == "weather_data":
        # Create sample weather data for past 30 days
        dates = pd.date_range(end=datetime.now(), periods=30)
        max_temp = [32 + 5 * np.sin(i/5) + np.random.normal(0, 1) for i in range(30)]
        min_temp = [20 + 5 * np.sin(i/5) + np.random.normal(0, 1) for i in range(30)]
        rainfall = [0] * 30
        
        # Add some rainfall events
        for i in [5, 6, 15, 16, 25]:
            rainfall[i] = np.random.randint(5, 20)
        
        humidity = [60 + 20 * np.sin(i/5) + np.random.normal(0, 5) for i in range(30)]
        for i in range(30):
            if rainfall[i] > 0:
                humidity[i] = min(95, humidity[i] + rainfall[i] * 2)
        
        data = {
            "Date": dates,
            "Max Temperature (°C)": max_temp,
            "Min Temperature (°C)": min_temp,
            "Rainfall (mm)": rainfall,
            "Humidity (%)": humidity
        }
        
        return pd.DataFrame(data)
    
    # Sample data for soil data
    elif data_type == "soil_data":
        # Create sample soil data
        fields = ["North Field", "South Field", "East Field", "West Field"]
        soil_types = ["Clay Loam", "Silt Loam", "Sandy Loam", "Clay Loam"]
        ph_values = [6.8, 7.2, 6.5, 7.0]
        organic_matter = [2.5, 2.0, 1.8, 2.3]
        nitrogen = [45, 35, 30, 40]
        phosphorus = [25, 18, 15, 22]
        potassium = [180, 160, 140, 170]
        moisture = [28, 25, 18, 27]
        
        data = {
            "Field": fields,
            "Soil Type": soil_types,
            "pH": ph_values,
            "Organic Matter (%)": organic_matter,
            "Nitrogen (ppm)": nitrogen,
            "Phosphorus (ppm)": phosphorus,
            "Potassium (ppm)": potassium,
            "Moisture (%)": moisture
        }
        
        return pd.DataFrame(data)
    
    # Sample data for resource usage
    elif data_type == "resource_data":
        # Create sample resource usage data
        resources = ["Water", "Fertilizer", "Pesticides", "Energy", "Labor"]
        usage = [350000, 5000, 800, 12000, 800]  # m³, kg, liters, kWh, hours
        unit_cost = [2, 70, 312.5, 15, 400]  # PKR per unit
        total_cost = [u * c for u, c in zip(usage, unit_cost)]
        efficiency = [75, 80, 70, 65, 85]  # percent
        
        data = {
            "Resource": resources,
            "Usage": usage,
            "Unit Cost (PKR)": unit_cost,
            "Total Cost (PKR)": total_cost,
            "Efficiency (%)": efficiency
        }
        
        return pd.DataFrame(data)
    
    # Sample data for crop financials
    elif data_type == "financial_data":
        # Create sample financial data
        crops = ["Wheat", "Rice", "Cotton", "Sugarcane"]
        area = [20, 15, 10, 5]  # acres
        yield_per_acre = [3.7, 4.2, 2.5, 35.0]  # tons/acre
        price_per_ton = [40000, 60000, 90000, 5000]  # PKR/ton
        cost_per_acre = [30000, 45000, 50000, 70000]  # PKR/acre
        
        production = [a * y for a, y in zip(area, yield_per_acre)]
        revenue = [p * pr for p, pr in zip(production, price_per_ton)]
        cost = [a * c for a, c in zip(area, cost_per_acre)]
        profit = [r - c for r, c in zip(revenue, cost)]
        roi = [100 * p / c for p, c in zip(profit, cost)]
        
        data = {
            "Crop": crops,
            "Area (acres)": area,
            "Yield (tons/acre)": yield_per_acre,
            "Production (tons)": production,
            "Price (PKR/ton)": price_per_ton,
            "Revenue (PKR)": revenue,
            "Cost (PKR)": cost,
            "Profit (PKR)": profit,
            "ROI (%)": roi
        }
        
        return pd.DataFrame(data)
    
    # Default case: return empty DataFrame
    return pd.DataFrame()


def process_uploaded_data(uploaded_file, data_type):
    """
    Process data uploaded by the user.
    
    Parameters:
    uploaded_file: The file uploaded through Streamlit's file_uploader
    data_type (str): Type of data being uploaded ('crop', 'soil', 'weather', etc.)
    
    Returns:
    DataFrame: Processed DataFrame
    str: Status message
    """
    try:
        # Check file extension to determine processing method
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension == 'csv':
            df = pd.read_csv(uploaded_file)
        elif file_extension in ['xls', 'xlsx']:
            df = pd.read_excel(uploaded_file)
        else:
            return None, "Unsupported file format. Please upload CSV or Excel file."
        
        # Basic validation based on data type
        if data_type == 'crop':
            required_columns = ['Field', 'Crop', 'Date']
            if not all(col in df.columns for col in required_columns):
                return None, "Missing required columns for crop data."
        
        elif data_type == 'soil':
            required_columns = ['Field', 'pH', 'Organic Matter']
            if not all(col in df.columns for col in required_columns):
                return None, "Missing required columns for soil data."
        
        elif data_type == 'weather':
            required_columns = ['Date', 'Temperature', 'Rainfall']
            if not all(col in df.columns for col in required_columns):
                return None, "Missing required columns for weather data."
        
        # Additional processing could be done here
        
        return df, "Data successfully processed."
    
    except Exception as e:
        return None, f"Error processing file: {str(e)}"


def aggregate_data(df, agg_type, field=None):
    """
    Aggregate data by different dimensions.
    
    Parameters:
    df (DataFrame): Data to aggregate
    agg_type (str): Type of aggregation ('field', 'crop', 'time')
    field (str, optional): Field to filter by if needed
    
    Returns:
    DataFrame: Aggregated data
    """
    if df is None or df.empty:
        return pd.DataFrame()
    
    # Filter by field if specified
    if field is not None and 'Field' in df.columns:
        df = df[df['Field'] == field]
    
    # Aggregate by field
    if agg_type == 'field' and 'Field' in df.columns:
        return df.groupby('Field').agg({
            'Health Score': 'mean',
            'NDVI': 'mean',
            'Stress Index': 'mean',
            'Organic Matter (%)': 'mean' if 'Organic Matter (%)' in df.columns else None,
            'Moisture (%)': 'mean' if 'Moisture (%)' in df.columns else None
        }).reset_index()
    
    # Aggregate by crop
    elif agg_type == 'crop' and 'Crop' in df.columns:
        return df.groupby('Crop').agg({
            'Yield (tons/acre)': 'mean' if 'Yield (tons/acre)' in df.columns else None,
            'Health Score': 'mean' if 'Health Score' in df.columns else None,
            'NDVI': 'mean' if 'NDVI' in df.columns else None,
            'Revenue (PKR)': 'sum' if 'Revenue (PKR)' in df.columns else None,
            'Profit (PKR)': 'sum' if 'Profit (PKR)' in df.columns else None
        }).reset_index()
    
    # Aggregate by time (for time series data)
    elif agg_type == 'time' and 'Date' in df.columns:
        # Convert Date to datetime if it's not already
        if not pd.api.types.is_datetime64_any_dtype(df['Date']):
            df['Date'] = pd.to_datetime(df['Date'])
        
        # Aggregate by month
        return df.set_index('Date').resample('M').agg({
            'Max Temperature (°C)': 'mean' if 'Max Temperature (°C)' in df.columns else None,
            'Min Temperature (°C)': 'mean' if 'Min Temperature (°C)' in df.columns else None,
            'Rainfall (mm)': 'sum' if 'Rainfall (mm)' in df.columns else None,
            'Humidity (%)': 'mean' if 'Humidity (%)' in df.columns else None
        }).reset_index()
    
    # Return original dataframe if no aggregation applied
    return df


def calculate_indicators(crop_data, weather_data, soil_data=None):
    """
    Calculate agricultural indicators based on various data sources.
    
    Parameters:
    crop_data (DataFrame): Crop health and yield data
    weather_data (DataFrame): Weather data
    soil_data (DataFrame, optional): Soil data
    
    Returns:
    dict: Dictionary of calculated indicators
    """
    indicators = {}
    
    # Check data availability
    if crop_data is None or crop_data.empty:
        return {'error': 'No crop data available'}
    
    if weather_data is None or weather_data.empty:
        return {'error': 'No weather data available'}
    
    try:
        # Calculate crop health index (average of health scores)
        if 'Health Score' in crop_data.columns:
            indicators['crop_health_index'] = round(crop_data['Health Score'].mean(), 1)
        
        # Calculate stress index (average of stress indices)
        if 'Stress Index' in crop_data.columns:
            indicators['stress_index'] = round(crop_data['Stress Index'].mean(), 1)
        
        # Calculate average NDVI
        if 'NDVI' in crop_data.columns:
            indicators['avg_ndvi'] = round(crop_data['NDVI'].mean(), 2)
        
        # Calculate growing degree days (GDD)
        if all(col in weather_data.columns for col in ['Max Temperature (°C)', 'Min Temperature (°C)']):
            # Calculate average daily temperature
            weather_data['Avg Temp'] = (weather_data['Max Temperature (°C)'] + weather_data['Min Temperature (°C)']) / 2
            
            # Calculate GDD with base temperature of 10°C
            weather_data['GDD'] = weather_data['Avg Temp'].apply(lambda x: max(0, x - 10))
            
            indicators['growing_degree_days'] = round(weather_data['GDD'].sum(), 0)
        
        # Calculate water deficit
        if all(col in weather_data.columns for col in ['Rainfall (mm)', 'Max Temperature (°C)']):
            # Simplified potential evapotranspiration based on temperature
            weather_data['PET'] = weather_data['Max Temperature (°C)'] * 0.5  # Simplified calculation
            
            # Water deficit
            weather_data['Deficit'] = weather_data['PET'] - weather_data['Rainfall (mm)']
            weather_data['Deficit'] = weather_data['Deficit'].apply(lambda x: max(0, x))
            
            indicators['water_deficit'] = round(weather_data['Deficit'].sum(), 0)
        
        # Calculate soil health index if soil data is available
        if soil_data is not None and not soil_data.empty:
            if all(col in soil_data.columns for col in ['pH', 'Organic Matter (%)']):
                # Simple soil health index based on pH and organic matter
                # pH score: 1 for pH between 6.0 and 7.5, decreasing as it moves away
                soil_data['pH_score'] = soil_data['pH'].apply(
                    lambda x: 1 - abs((x - 6.75) / 3) if 4 <= x <= 9 else 0)
                
                # Organic matter score: higher is better, max at around 5%
                soil_data['om_score'] = soil_data['Organic Matter (%)'].apply(
                    lambda x: min(1, x / 5))
                
                # Soil health index (average of pH score and OM score)
                soil_health_index = (soil_data['pH_score'].mean() + soil_data['om_score'].mean()) / 2
                indicators['soil_health_index'] = round(soil_health_index * 100, 1)
        
        return indicators
    
    except Exception as e:
        return {'error': f'Error calculating indicators: {str(e)}'}


def get_crop_recommendations(crop_data, weather_data, soil_data=None):
    """
    Generate crop management recommendations based on data analysis.
    
    Parameters:
    crop_data (DataFrame): Crop health and yield data
    weather_data (DataFrame): Weather data
    soil_data (DataFrame, optional): Soil data
    
    Returns:
    list: List of recommendation dictionaries with 'category', 'description', and 'priority'
    """
    recommendations = []
    
    # Check data availability
    if crop_data is None or crop_data.empty:
        return [{'category': 'Error', 'description': 'No crop data available', 'priority': 'High'}]
    
    if weather_data is None or weather_data.empty:
        return [{'category': 'Error', 'description': 'No weather data available', 'priority': 'High'}]
    
    try:
        # Calculate indicators
        indicators = calculate_indicators(crop_data, weather_data, soil_data)
        
        # Crop health recommendations
        if 'crop_health_index' in indicators:
            health_index = indicators['crop_health_index']
            
            if health_index < 60:
                recommendations.append({
                    'category': 'Crop Health',
                    'description': 'Critical crop health issues detected. Immediate inspection and intervention required.',
                    'priority': 'High'
                })
            elif health_index < 75:
                recommendations.append({
                    'category': 'Crop Health',
                    'description': 'Moderate crop health issues detected. Consider foliar nutrient application and disease monitoring.',
                    'priority': 'Medium'
                })
        
        # Water management recommendations
        if 'water_deficit' in indicators:
            water_deficit = indicators['water_deficit']
            
            if water_deficit > 50:
                recommendations.append({
                    'category': 'Irrigation',
                    'description': f'Significant water deficit of {water_deficit}mm detected. Increase irrigation frequency.',
                    'priority': 'High'
                })
            elif water_deficit > 25:
                recommendations.append({
                    'category': 'Irrigation',
                    'description': f'Moderate water deficit of {water_deficit}mm detected. Monitor soil moisture closely.',
                    'priority': 'Medium'
                })
        
        # Soil health recommendations
        if 'soil_health_index' in indicators:
            soil_health = indicators['soil_health_index']
            
            if soil_health < 60:
                recommendations.append({
                    'category': 'Soil Management',
                    'description': 'Poor soil health detected. Consider soil amendments and organic matter addition.',
                    'priority': 'High'
                })
            elif soil_health < 75:
                recommendations.append({
                    'category': 'Soil Management',
                    'description': 'Moderate soil health issues. Consider cover crops and reduced tillage.',
                    'priority': 'Medium'
                })
        
        # Check for recent rainfall
        if 'Rainfall (mm)' in weather_data.columns:
            recent_rainfall = weather_data.iloc[-7:]['Rainfall (mm)'].sum()
            
            if recent_rainfall > 50:
                recommendations.append({
                    'category': 'Water Management',
                    'description': f'Heavy rainfall ({recent_rainfall}mm) in the past week. Check field drainage and delay fertilizer application.',
                    'priority': 'High'
                })
            elif recent_rainfall < 5:
                recommendations.append({
                    'category': 'Water Management',
                    'description': 'Limited rainfall in the past week. Ensure adequate irrigation.',
                    'priority': 'Medium'
                })
        
        # Check for temperature stress
        if 'Max Temperature (°C)' in weather_data.columns:
            max_temp = weather_data.iloc[-7:]['Max Temperature (°C)'].max()
            
            if max_temp > 35:
                recommendations.append({
                    'category': 'Temperature Management',
                    'description': f'High temperature stress detected ({max_temp}°C). Increase irrigation frequency and consider shade for sensitive crops.',
                    'priority': 'High'
                })
        
        # Add general recommendations if few specific ones were generated
        if len(recommendations) < 2:
            recommendations.append({
                'category': 'General Management',
                'description': 'Regular monitoring of crop health and pest pressure is recommended.',
                'priority': 'Medium'
            })
            
            recommendations.append({
                'category': 'Soil Testing',
                'description': 'Consider comprehensive soil testing to optimize fertilizer application.',
                'priority': 'Medium'
            })
        
        return recommendations
    
    except Exception as e:
        return [{'category': 'Error', 'description': f'Error generating recommendations: {str(e)}', 'priority': 'High'}]
