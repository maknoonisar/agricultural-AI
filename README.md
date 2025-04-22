# Agri-Vision System

A comprehensive agricultural intelligence system designed for farmers in Pakistan with interactive MapBox visualizations, data processing, and actionable insights to enhance agricultural productivity and profitability.

## Overview

The Agri-Vision System is an AI-powered agricultural intelligence platform that empowers farmers with data-driven insights for improved decision-making. The system provides real-time crop health diagnostics using computer vision, yield forecasting through temporal data analysis, and resource optimization recommendations for irrigation and fertilization. It integrates drone and satellite imagery with live weather data to present information through an interactive dashboard with MapBox integration.

## Features

- **Interactive Dashboard**: Comprehensive overview of farm health, productivity, and weather conditions
- **Crop Health Analysis**: Visual representation of crop health with NDVI mapping and disease detection
- **Yield Forecasting**: Predictive analysis of crop yields based on current conditions and historical data
- **Resource Optimization**: Recommendations for water usage, fertilizer application, and other resources
- **Weather Data Integration**: Real-time weather data and forecasts with agricultural impact analysis
- **Comprehensive Reports**: Detailed insights and recommendations in downloadable formats

## Technology Stack

- **Frontend**: Streamlit for interactive web interface with multipage support
- **Data Visualization**: Plotly for interactive charts, graphs, and data tables
- **Geospatial Visualization**: MapBox for interactive maps and field visualization
- **Data Processing**: Pandas and NumPy for data manipulation and analysis
- **Data Formatting**: Streamlit styling and formatting for tables and metrics
- **Image Processing**: PIL/Pillow for handling crop health images
- **Notifications**: Twilio for SMS alerts and SMTP for email notifications
- **Styling**: CSS customization for Streamlit components
- **Data Storage**: File-based data with optional PostgreSQL database integration
- **AI/Machine Learning**: Computer vision and predictive analytics (simulated)
- **Chart Types**: Bar charts, line charts, scatter plots, heatmaps, and time series
- **Security**: Environment variables for API key management

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/agri-vision-system.git
   cd agri-vision-system
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the root directory
   - Add your MapBox API token: `MAPBOX_TOKEN=your_mapbox_token`

4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Project Structure

- `app.py`: Main application entry point
- `/assets`: Static resources and image URLs
- `/pages`: Streamlit multipage app components
  - `1_Dashboard.py`: Main dashboard overview
  - `2_Crop_Health.py`: Crop health monitoring and analysis
  - `3_Yield_Forecast.py`: Yield prediction and forecasting
  - `4_Resource_Optimization.py`: Resource usage optimization
  - `5_Weather_Data.py`: Weather data and forecasts
  - `6_Reports.py`: Comprehensive reporting module
- `/utils`: Utility functions and modules
  - `crop_analysis.py`: Crop health analysis functions
  - `data_processor.py`: Data processing utilities
  - `mapbox_utils.py`: MapBox integration utilities
  - `visualization.py`: Data visualization functions
  - `weather_api.py`: Weather data processing functions

## Using the Application

1. **Dashboard**: Start with the main dashboard for a quick overview of farm conditions
2. **Crop Health**: Upload images for analysis or view NDVI maps of your fields
3. **Yield Forecast**: View yield predictions for different crops and seasons
4. **Resource Optimization**: Get recommendations for optimal resource usage
5. **Weather Data**: Access current weather conditions and forecasts
6. **Reports**: Generate and download comprehensive reports

## Customization

The application can be customized for specific crops, regions, and farming practices:

- Modify crop types in the selection menus
- Adjust optimal resource usage parameters in the utilities
- Update geographic coordinates for different farm locations

## Future Enhancements

- Integration with IoT sensors for real-time soil and crop monitoring
- Mobile app for field data collection
- Machine learning models for pest detection and disease prediction
- Integration with farm management software for comprehensive farm operations

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions, suggestions, or collaboration opportunities, please contact [your email]