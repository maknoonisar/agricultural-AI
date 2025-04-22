import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

def create_farm_map(mapbox_token, latitude=31.5204, longitude=74.3587, zoom=10):
    """
    Create a MapBox map centered on a farm with field boundaries.
    
    Parameters:
    mapbox_token (str): MapBox access token
    latitude (float): Center latitude for the map
    longitude (float): Center longitude for the map
    zoom (int): Zoom level for the map
    
    Returns:
    Figure: Plotly figure with MapBox map
    """
    # Create sample field locations around the center point
    # In a real application, these would come from a database or GeoJSON file
    fields = [
        {"name": "North Field", "type": "Wheat", "area": 20, "health": 85, 
         "coordinates": create_field_coords(latitude + 0.01, longitude - 0.01, 0.008, 0.012)},
        {"name": "South Field", "type": "Rice", "area": 15, "health": 75, 
         "coordinates": create_field_coords(latitude - 0.01, longitude + 0.01, 0.007, 0.011)},
        {"name": "East Field", "type": "Cotton", "area": 10, "health": 60, 
         "coordinates": create_field_coords(latitude + 0.005, longitude + 0.015, 0.006, 0.009)},
        {"name": "West Field", "type": "Sugarcane", "area": 5, "health": 80, 
         "coordinates": create_field_coords(latitude - 0.008, longitude - 0.012, 0.005, 0.008)}
    ]
    
    # Create a Plotly figure with a MapBox map
    fig = go.Figure()
    
    # Add field polygons
    for field in fields:
        # Determine color based on health (green for good health, red for poor health)
        health_score = field["health"]
        if health_score >= 80:
            color = "green"
        elif health_score >= 70:
            color = "yellowgreen"
        elif health_score >= 60:
            color = "orange"
        else:
            color = "red"
        
        # Add polygon for the field
        fig.add_trace(go.Scattermapbox(
            lat=[coord[0] for coord in field["coordinates"]],
            lon=[coord[1] for coord in field["coordinates"]],
            mode="lines",
            fill="toself",
            fillcolor=f"rgba({','.join([str(c) for c in px.colors.hex_to_rgb(px.colors.sequential.Viridis[int(health_score/14)])])}, 0.5)",
            line=dict(color=color, width=2),
            name=field["name"],
            text=f"{field['name']}<br>Crop: {field['type']}<br>Area: {field['area']} acres<br>Health: {field['health']}/100",
            hoverinfo="text"
        ))
    
    # Add markers for important farm features
    features = [
        {"name": "Main Farm House", "lat": latitude, "lon": longitude, "icon": "home"},
        {"name": "Water Source", "lat": latitude - 0.005, "lon": longitude - 0.005, "icon": "water"},
        {"name": "Equipment Shed", "lat": latitude + 0.003, "lon": longitude + 0.002, "icon": "warehouse"},
        {"name": "Irrigation Pump", "lat": latitude - 0.002, "lon": longitude + 0.007, "icon": "industry"}
    ]
    
    # Add the feature markers
    for feature in features:
        fig.add_trace(go.Scattermapbox(
            lat=[feature["lat"]],
            lon=[feature["lon"]],
            mode="markers",
            marker=dict(size=12, color="blue"),
            name=feature["name"],
            text=feature["name"],
            hoverinfo="text"
        ))
    
    # Configure the map layout
    fig.update_layout(
        mapbox=dict(
            style="open-street-map",  # Use OpenStreetMap as a fallback if MapBox token is not available
            center=dict(lat=latitude, lon=longitude),
            zoom=zoom,
            accesstoken=mapbox_token
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=500,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=0.02,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255, 255, 255, 0.8)"
        )
    )
    
    return fig


def create_crop_health_map(mapbox_token, latitude=31.5204, longitude=74.3587, zoom=12):
    """
    Create a MapBox map displaying crop health information.
    
    Parameters:
    mapbox_token (str): MapBox access token
    latitude (float): Center latitude for the map
    longitude (float): Center longitude for the map
    zoom (int): Zoom level for the map
    
    Returns:
    Figure: Plotly figure with MapBox map showing crop health
    """
    # Create sample field data with health information
    fields = [
        {"name": "North Field", "type": "Wheat", "health": 85, "ndvi": 0.82, 
         "coordinates": create_field_coords(latitude + 0.01, longitude - 0.01, 0.008, 0.012)},
        {"name": "South Field", "type": "Rice", "health": 75, "ndvi": 0.71, 
         "coordinates": create_field_coords(latitude - 0.01, longitude + 0.01, 0.007, 0.011)},
        {"name": "East Field", "type": "Cotton", "health": 60, "ndvi": 0.56, 
         "coordinates": create_field_coords(latitude + 0.005, longitude + 0.015, 0.006, 0.009)},
        {"name": "West Field", "type": "Sugarcane", "health": 80, "ndvi": 0.78, 
         "coordinates": create_field_coords(latitude - 0.008, longitude - 0.012, 0.005, 0.008)}
    ]
    
    # Add grid cells within each field for detailed health visualization
    all_cells = []
    
    for field in fields:
        base_lat, base_lon = field["coordinates"][0]
        width = abs(field["coordinates"][2][1] - field["coordinates"][0][1])
        height = abs(field["coordinates"][2][0] - field["coordinates"][0][0])
        
        # Base health value for the field
        base_health = field["ndvi"]
        
        # Create a grid of cells
        for i in range(10):
            for j in range(10):
                # Add some random variation to health within the field
                health_variation = np.random.normal(0, 0.05)
                cell_health = min(max(base_health + health_variation, 0), 1)
                
                # Cell coordinates
                cell_lat = base_lat + (height * i / 10)
                cell_lon = base_lon + (width * j / 10)
                cell_width = width / 10
                cell_height = height / 10
                
                all_cells.append({
                    "field": field["name"],
                    "lat": cell_lat + cell_height/2,
                    "lon": cell_lon + cell_width/2,
                    "ndvi": cell_health,
                    "coordinates": [
                        [cell_lat, cell_lon],
                        [cell_lat, cell_lon + cell_width],
                        [cell_lat + cell_height, cell_lon + cell_width],
                        [cell_lat + cell_height, cell_lon],
                        [cell_lat, cell_lon]  # Close the polygon
                    ]
                })
    
    # Create a Plotly figure with a MapBox map
    fig = go.Figure()
    
    # Add field boundaries
    for field in fields:
        fig.add_trace(go.Scattermapbox(
            lat=[coord[0] for coord in field["coordinates"]],
            lon=[coord[1] for coord in field["coordinates"]],
            mode="lines",
            line=dict(color="white", width=2),
            name=field["name"],
            text=f"{field['name']}<br>Crop: {field['type']}<br>Health: {field['health']}/100<br>NDVI: {field['ndvi']:.2f}",
            hoverinfo="text",
            showlegend=True
        ))
    
    # Add cell polygons for detailed health visualization
    for cell in all_cells:
        # Determine color based on NDVI
        ndvi = cell["ndvi"]
        if ndvi >= 0.8:
            color_index = 0  # Excellent
        elif ndvi >= 0.6:
            color_index = 1  # Good
        elif ndvi >= 0.4:
            color_index = 2  # Moderate
        else:
            color_index = 3  # Poor
            
        colors = ["green", "yellowgreen", "orange", "red"]
        color = colors[color_index]
        
        # Add polygon for the cell
        # Color mapping without using hex_to_rgb
        color_mapping = {
            "green": "rgba(0,128,0,0.5)",
            "yellowgreen": "rgba(154,205,50,0.5)",
            "orange": "rgba(255,165,0,0.5)",
            "red": "rgba(255,0,0,0.5)"
        }
            
        fig.add_trace(go.Scattermapbox(
            lat=[coord[0] for coord in cell["coordinates"]],
            lon=[coord[1] for coord in cell["coordinates"]],
            mode="lines",
            fill="toself",
            fillcolor=color_mapping.get(color, "rgba(128,128,128,0.5)"),
            line=dict(color=color, width=0.5),
            name=f"{cell['field']} Cell",
            text=f"Field: {cell['field']}<br>NDVI: {cell['ndvi']:.2f}",
            hoverinfo="text",
            showlegend=False
        ))
    
    # Configure the map layout
    fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=latitude, lon=longitude),
            zoom=zoom,
            accesstoken=mapbox_token
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=600,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=0.02,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255, 255, 255, 0.8)"
        )
    )
    
    return fig


def create_yield_forecast_map(mapbox_token, crop="Wheat", season="Rabi 2023-24", latitude=31.5204, longitude=74.3587, zoom=12):
    """
    Create a MapBox map showing yield forecasts.
    
    Parameters:
    mapbox_token (str): MapBox access token
    crop (str): Crop type to display
    season (str): Growing season
    latitude (float): Center latitude for the map
    longitude (float): Center longitude for the map
    zoom (int): Zoom level for the map
    
    Returns:
    Figure: Plotly figure with MapBox map showing yield forecasts
    """
    # Create sample field data with yield forecasts
    if crop == "Wheat":
        fields = [
            {"name": "North Field", "area": 20, "yield_forecast": 4.5, "yield_last_year": 4.2, 
             "coordinates": create_field_coords(latitude + 0.01, longitude - 0.01, 0.008, 0.012)},
            {"name": "South Field", "area": 15, "yield_forecast": 4.3, "yield_last_year": 4.1, 
             "coordinates": create_field_coords(latitude - 0.01, longitude + 0.01, 0.007, 0.011)}
        ]
    elif crop == "Rice":
        fields = [
            {"name": "East Field", "area": 10, "yield_forecast": 3.8, "yield_last_year": 3.5, 
             "coordinates": create_field_coords(latitude + 0.005, longitude + 0.015, 0.006, 0.009)},
            {"name": "West Field", "area": 5, "yield_forecast": 4.0, "yield_last_year": 3.7, 
             "coordinates": create_field_coords(latitude - 0.008, longitude - 0.012, 0.005, 0.008)}
        ]
    else:
        # Default fields for other crops
        fields = [
            {"name": "North Field", "area": 20, "yield_forecast": 2.5, "yield_last_year": 2.3, 
             "coordinates": create_field_coords(latitude + 0.01, longitude - 0.01, 0.008, 0.012)},
            {"name": "South Field", "area": 15, "yield_forecast": 2.3, "yield_last_year": 2.1, 
             "coordinates": create_field_coords(latitude - 0.01, longitude + 0.01, 0.007, 0.011)},
            {"name": "East Field", "area": 10, "yield_forecast": 2.6, "yield_last_year": 2.4, 
             "coordinates": create_field_coords(latitude + 0.005, longitude + 0.015, 0.006, 0.009)},
            {"name": "West Field", "area": 5, "yield_forecast": 2.4, "yield_last_year": 2.2, 
             "coordinates": create_field_coords(latitude - 0.008, longitude - 0.012, 0.005, 0.008)}
        ]
    
    # Add grid cells within each field for detailed yield visualization
    all_cells = []
    
    for field in fields:
        base_lat, base_lon = field["coordinates"][0]
        width = abs(field["coordinates"][2][1] - field["coordinates"][0][1])
        height = abs(field["coordinates"][2][0] - field["coordinates"][0][0])
        
        # Base yield value for the field
        base_yield = field["yield_forecast"]
        
        # Create a grid of cells
        for i in range(10):
            for j in range(10):
                # Add some random variation to yield within the field
                yield_variation = np.random.normal(0, 0.2)
                cell_yield = max(base_yield + yield_variation, 0)
                
                # Cell coordinates
                cell_lat = base_lat + (height * i / 10)
                cell_lon = base_lon + (width * j / 10)
                cell_width = width / 10
                cell_height = height / 10
                
                all_cells.append({
                    "field": field["name"],
                    "lat": cell_lat + cell_height/2,
                    "lon": cell_lon + cell_width/2,
                    "yield": cell_yield,
                    "coordinates": [
                        [cell_lat, cell_lon],
                        [cell_lat, cell_lon + cell_width],
                        [cell_lat + cell_height, cell_lon + cell_width],
                        [cell_lat + cell_height, cell_lon],
                        [cell_lat, cell_lon]  # Close the polygon
                    ]
                })
    
    # Create a Plotly figure with a MapBox map
    fig = go.Figure()
    
    # Add field boundaries
    for field in fields:
        fig.add_trace(go.Scattermapbox(
            lat=[coord[0] for coord in field["coordinates"]],
            lon=[coord[1] for coord in field["coordinates"]],
            mode="lines",
            line=dict(color="white", width=2),
            name=field["name"],
            text=f"{field['name']}<br>Area: {field['area']} acres<br>Forecast: {field['yield_forecast']} tons/acre<br>Change: {((field['yield_forecast']/field['yield_last_year'])-1)*100:.1f}%",
            hoverinfo="text",
            showlegend=True
        ))
    
    # Add cell polygons for detailed yield visualization
    for cell in all_cells:
        # Determine color based on yield forecast
        yield_val = cell["yield"]
        
        if crop == "Wheat":
            max_yield = 5.0
        elif crop == "Rice":
            max_yield = 4.5
        else:
            max_yield = 3.0
            
        # Normalize yield to a 0-1 scale for color mapping
        normalized_yield = min(yield_val / max_yield, 1)
        
        # Generate color from a continuous scale
        color_scale = px.colors.sequential.Viridis
        color_idx = int(normalized_yield * (len(color_scale) - 1))
        color = color_scale[color_idx]
        
        # Add polygon for the cell
        fig.add_trace(go.Scattermapbox(
            lat=[coord[0] for coord in cell["coordinates"]],
            lon=[coord[1] for coord in cell["coordinates"]],
            mode="lines",
            fill="toself",
            fillcolor=f"rgba(0,255,0,0.7)",  # Simple green with opacity
            line=dict(color=color, width=0.5),
            name=f"{cell['field']} Cell",
            text=f"Field: {cell['field']}<br>Yield Forecast: {cell['yield']:.2f} tons/acre",
            hoverinfo="text",
            showlegend=False
        ))
    
    # Add legend for yield levels
    legend_entries = [
        {"name": "High Yield", "color": px.colors.sequential.Viridis[-1]},
        {"name": "Medium-High Yield", "color": px.colors.sequential.Viridis[int(len(px.colors.sequential.Viridis)*0.75)]},
        {"name": "Medium Yield", "color": px.colors.sequential.Viridis[int(len(px.colors.sequential.Viridis)*0.5)]},
        {"name": "Medium-Low Yield", "color": px.colors.sequential.Viridis[int(len(px.colors.sequential.Viridis)*0.25)]},
        {"name": "Low Yield", "color": px.colors.sequential.Viridis[0]}
    ]
    
    for entry in legend_entries:
        fig.add_trace(go.Scattermapbox(
            lat=[latitude + 0.03],
            lon=[longitude + 0.03],
            mode="markers",
            marker=dict(size=10, color=entry["color"]),
            name=entry["name"],
            showlegend=True,
            visible=True
        ))
    
    # Configure the map layout
    fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=latitude, lon=longitude),
            zoom=zoom,
            accesstoken=mapbox_token
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=600,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=0.02,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255, 255, 255, 0.8)"
        ),
        title=dict(
            text=f"{crop} Yield Forecast - {season}",
            y=0.98
        )
    )
    
    return fig


def create_resource_map(mapbox_token, resource_type="water", latitude=31.5204, longitude=74.3587, zoom=12):
    """
    Create a MapBox map showing resource usage (water, nutrients, etc.).
    
    Parameters:
    mapbox_token (str): MapBox access token
    resource_type (str): Type of resource to display ('water', 'nutrients', 'energy')
    latitude (float): Center latitude for the map
    longitude (float): Center longitude for the map
    zoom (int): Zoom level for the map
    
    Returns:
    Figure: Plotly figure with MapBox map showing resource usage
    """
    # Create sample field data with resource usage information
    fields = [
        {"name": "North Field", "type": "Wheat", "area": 20, 
         "water_usage": 78, "water_optimal": 65,  # mm/week
         "nutrient_levels": {"N": 120, "P": 35, "K": 80}, 
         "nutrient_optimal": {"N": 110, "P": 30, "K": 85},
         "coordinates": create_field_coords(latitude + 0.01, longitude - 0.01, 0.008, 0.012)},
        {"name": "South Field", "type": "Rice", "area": 15, 
         "water_usage": 65, "water_optimal": 60,
         "nutrient_levels": {"N": 90, "P": 28, "K": 65}, 
         "nutrient_optimal": {"N": 100, "P": 30, "K": 75},
         "coordinates": create_field_coords(latitude - 0.01, longitude + 0.01, 0.007, 0.011)},
        {"name": "East Field", "type": "Cotton", "area": 10, 
         "water_usage": 92, "water_optimal": 70,
         "nutrient_levels": {"N": 150, "P": 42, "K": 95}, 
         "nutrient_optimal": {"N": 120, "P": 35, "K": 80},
         "coordinates": create_field_coords(latitude + 0.005, longitude + 0.015, 0.006, 0.009)},
        {"name": "West Field", "type": "Sugarcane", "area": 5, 
         "water_usage": 71, "water_optimal": 65,
         "nutrient_levels": {"N": 110, "P": 30, "K": 75}, 
         "nutrient_optimal": {"N": 110, "P": 30, "K": 75},
         "coordinates": create_field_coords(latitude - 0.008, longitude - 0.012, 0.005, 0.008)}
    ]
    
    # Add grid cells within each field for detailed resource visualization
    all_cells = []
    
    for field in fields:
        base_lat, base_lon = field["coordinates"][0]
        width = abs(field["coordinates"][2][1] - field["coordinates"][0][1])
        height = abs(field["coordinates"][2][0] - field["coordinates"][0][0])
        
        # Resource values for the field
        if resource_type == "water":
            base_value = field["water_usage"]
            optimal_value = field["water_optimal"]
            efficiency = optimal_value / base_value
        elif resource_type == "nutrients":
            # Calculate overall nutrient balance (simplification for visualization)
            actual_sum = sum(field["nutrient_levels"].values())
            optimal_sum = sum(field["nutrient_optimal"].values())
            base_value = actual_sum
            optimal_value = optimal_sum
            efficiency = min(actual_sum / optimal_sum, optimal_sum / actual_sum)  # Lower for both excess and deficiency
        else:
            # Default resource visualization
            base_value = 75
            optimal_value = 65
            efficiency = optimal_value / base_value
        
        # Create a grid of cells
        for i in range(10):
            for j in range(10):
                # Add some random variation to resource usage within the field
                value_variation = np.random.normal(0, base_value * 0.1)
                cell_value = max(base_value + value_variation, 0)
                cell_efficiency = optimal_value / cell_value if cell_value > 0 else 1
                
                # Cell coordinates
                cell_lat = base_lat + (height * i / 10)
                cell_lon = base_lon + (width * j / 10)
                cell_width = width / 10
                cell_height = height / 10
                
                all_cells.append({
                    "field": field["name"],
                    "lat": cell_lat + cell_height/2,
                    "lon": cell_lon + cell_width/2,
                    "value": cell_value,
                    "optimal": optimal_value,
                    "efficiency": cell_efficiency,
                    "coordinates": [
                        [cell_lat, cell_lon],
                        [cell_lat, cell_lon + cell_width],
                        [cell_lat + cell_height, cell_lon + cell_width],
                        [cell_lat + cell_height, cell_lon],
                        [cell_lat, cell_lon]  # Close the polygon
                    ]
                })
    
    # Create a Plotly figure with a MapBox map
    fig = go.Figure()
    
    # Add field boundaries
    for field in fields:
        if resource_type == "water":
            info_text = f"{field['name']}<br>Crop: {field['type']}<br>Water Usage: {field['water_usage']} mm/week<br>Optimal: {field['water_optimal']} mm/week<br>Efficiency: {(field['water_optimal']/field['water_usage']*100):.0f}%"
        elif resource_type == "nutrients":
            info_text = f"{field['name']}<br>Crop: {field['type']}<br>N: {field['nutrient_levels']['N']} kg/ha (Optimal: {field['nutrient_optimal']['N']})<br>P: {field['nutrient_levels']['P']} kg/ha (Optimal: {field['nutrient_optimal']['P']})<br>K: {field['nutrient_levels']['K']} kg/ha (Optimal: {field['nutrient_optimal']['K']})"
        else:
            info_text = f"{field['name']}<br>Crop: {field['type']}<br>Area: {field['area']} acres"
        
        fig.add_trace(go.Scattermapbox(
            lat=[coord[0] for coord in field["coordinates"]],
            lon=[coord[1] for coord in field["coordinates"]],
            mode="lines",
            line=dict(color="white", width=2),
            name=field["name"],
            text=info_text,
            hoverinfo="text",
            showlegend=True
        ))
    
    # Add cell polygons for detailed resource visualization
    for cell in all_cells:
        # Determine color based on efficiency
        efficiency = cell["efficiency"]
        
        if efficiency >= 0.9:
            color = "#3366CC"  # Good (low resource usage)
        elif efficiency >= 0.8:
            color = "#33CC33"  # Optimal
        elif efficiency >= 0.7:
            color = "#FFCC00"  # Moderate over-usage
        else:
            color = "#FF3333"  # Severe over-usage
        
        # Create hover text based on resource type
        if resource_type == "water":
            hover_text = f"Field: {cell['field']}<br>Water Usage: {cell['value']:.1f} mm/week<br>Optimal: {cell['optimal']} mm/week<br>Efficiency: {(cell['efficiency']*100):.0f}%"
        elif resource_type == "nutrients":
            hover_text = f"Field: {cell['field']}<br>Nutrient Level: {cell['value']:.1f}<br>Optimal: {cell['optimal']:.1f}<br>Balance: {(cell['efficiency']*100):.0f}%"
        else:
            hover_text = f"Field: {cell['field']}<br>Resource Usage: {cell['value']:.1f}<br>Optimal: {cell['optimal']:.1f}<br>Efficiency: {(cell['efficiency']*100):.0f}%"
        
        # Add polygon for the cell
        fig.add_trace(go.Scattermapbox(
            lat=[coord[0] for coord in cell["coordinates"]],
            lon=[coord[1] for coord in cell["coordinates"]],
            mode="lines",
            fill="toself",
            fillcolor=f"rgba(50,150,255,0.5)" if color == "#3366CC" else
                       f"rgba(50,200,50,0.5)" if color == "#33CC33" else
                       f"rgba(255,200,0,0.5)" if color == "#FFCC00" else
                       f"rgba(255,50,50,0.5)",  # Default for #FF3333
            line=dict(color=color, width=0.5),
            name=f"{cell['field']} Cell",
            text=hover_text,
            hoverinfo="text",
            showlegend=False
        ))
    
    # Configure the map layout
    fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=latitude, lon=longitude),
            zoom=zoom,
            accesstoken=mapbox_token
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=600,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=0.02,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255, 255, 255, 0.8)"
        ),
        title=dict(
            text=f"{resource_type.capitalize()} Usage Efficiency Map",
            y=0.98
        )
    )
    
    return fig


def create_weather_map(mapbox_token, latitude=31.5204, longitude=74.3587, zoom=6):
    """
    Create a MapBox map showing weather information.
    
    Parameters:
    mapbox_token (str): MapBox access token
    latitude (float): Center latitude for the map
    longitude (float): Center longitude for the map
    zoom (int): Zoom level for the map
    
    Returns:
    Figure: Plotly figure with MapBox map showing weather information
    """
    # Create sample weather data for major cities/regions
    weather_points = [
        {"name": "Lahore", "lat": 31.5204, "lon": 74.3587, "temp": 32, "humidity": 65, "rainfall": 0, "wind": 12, "conditions": "Partly Cloudy"},
        {"name": "Multan", "lat": 30.1575, "lon": 71.5249, "temp": 33, "humidity": 60, "rainfall": 0, "wind": 15, "conditions": "Sunny"},
        {"name": "Faisalabad", "lat": 31.4504, "lon": 73.1350, "temp": 31, "humidity": 68, "rainfall": 0, "wind": 10, "conditions": "Partly Cloudy"},
        {"name": "Islamabad", "lat": 33.6844, "lon": 73.0479, "temp": 28, "humidity": 75, "rainfall": 5, "wind": 8, "conditions": "Light Rain"},
        {"name": "Peshawar", "lat": 34.0151, "lon": 71.5249, "temp": 30, "humidity": 70, "rainfall": 0, "wind": 12, "conditions": "Cloudy"},
        {"name": "Karachi", "lat": 24.8607, "lon": 67.0011, "temp": 34, "humidity": 75, "rainfall": 0, "wind": 18, "conditions": "Sunny"},
        {"name": "Quetta", "lat": 30.1798, "lon": 66.9750, "temp": 26, "humidity": 45, "rainfall": 0, "wind": 15, "conditions": "Clear"},
        {"name": "Hyderabad", "lat": 25.3960, "lon": 68.3578, "temp": 35, "humidity": 72, "rainfall": 0, "wind": 16, "conditions": "Sunny"}
    ]
    
    # Create rainfall area polygons
    rainfall_areas = [
        {"name": "Light Rain", "center_lat": 33.6844, "center_lon": 73.0479, "radius": 0.5, "rainfall": 5},
        {"name": "Moderate Rain", "center_lat": 32.1877, "center_lon": 74.1945, "radius": 0.3, "rainfall": 15},
        {"name": "Heavy Rain", "center_lat": 31.1704, "center_lon": 72.7097, "radius": 0.2, "rainfall": 30}
    ]
    
    # Create a Plotly figure with a MapBox map
    fig = go.Figure()
    
    # Add rainfall area polygons
    for area in rainfall_areas:
        # Create a circular polygon for the rainfall area
        circle_points = 20
        radius = area["radius"]
        center_lat = area["center_lat"]
        center_lon = area["center_lon"]
        
        # Generate circle coordinates
        circle_lats = [center_lat + radius * np.cos(2 * np.pi * i / circle_points) for i in range(circle_points+1)]
        circle_lons = [center_lon + radius * np.sin(2 * np.pi * i / circle_points) for i in range(circle_points+1)]
        
        # Determine color based on rainfall intensity
        rainfall = area["rainfall"]
        if rainfall < 10:
            color = "rgba(135, 206, 250, 0.5)"  # Light blue for light rain
        elif rainfall < 20:
            color = "rgba(30, 144, 255, 0.5)"  # Blue for moderate rain
        else:
            color = "rgba(0, 0, 128, 0.5)"  # Dark blue for heavy rain
        
        # Add the rainfall area
        fig.add_trace(go.Scattermapbox(
            lat=circle_lats,
            lon=circle_lons,
            mode="lines",
            fill="toself",
            fillcolor=color,
            line=dict(color="blue", width=1),
            name=area["name"],
            text=f"{area['name']}<br>Rainfall: {area['rainfall']} mm",
            hoverinfo="text",
            showlegend=True
        ))
    
    # Add weather points for major cities
    for point in weather_points:
        # Determine marker color based on temperature
        temp = point["temp"]
        if temp >= 35:
            color = "#FF3333"  # red
        elif temp >= 30:
            color = "#FF9933"  # orange
        elif temp >= 25:
            color = "#FFCC00"  # yellow
        elif temp >= 20:
            color = "#33CC33"  # green
        else:
            color = "#3366CC"  # blue
        
        # Add the weather point
        fig.add_trace(go.Scattermapbox(
            lat=[point["lat"]],
            lon=[point["lon"]],
            mode="markers",
            marker=dict(size=12, color=color),
            name=point["name"],
            text=f"{point['name']}<br>Temperature: {point['temp']}°C<br>Humidity: {point['humidity']}%<br>Rainfall: {point['rainfall']} mm<br>Wind: {point['wind']} km/h<br>Conditions: {point['conditions']}",
            hoverinfo="text"
        ))
    
    # Configure the map layout
    fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=latitude, lon=longitude),
            zoom=zoom,
            accesstoken=mapbox_token
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=600,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=0.02,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255, 255, 255, 0.8)"
        ),
        title=dict(
            text="Current Weather Conditions",
            y=0.98
        )
    )
    
    return fig


def create_field_coords(base_lat, base_lon, width, height):
    """
    Create coordinates for a rectangular field.
    
    Parameters:
    base_lat (float): Base latitude (southwest corner)
    base_lon (float): Base longitude (southwest corner)
    width (float): Width of the field in degrees longitude
    height (float): Height of the field in degrees latitude
    
    Returns:
    list: List of [lat, lon] coordinate pairs forming a rectangle
    """
    return [
        [base_lat, base_lon],  # Southwest corner
        [base_lat, base_lon + width],  # Southeast corner
        [base_lat + height, base_lon + width],  # Northeast corner
        [base_lat + height, base_lon],  # Northwest corner
        [base_lat, base_lon]  # Close the polygon by returning to the start
    ]
