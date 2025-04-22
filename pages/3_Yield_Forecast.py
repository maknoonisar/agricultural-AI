import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.data_processor import load_sample_data
from utils.mapbox_utils import create_yield_forecast_map
from assets.image_urls import get_random_image

# Set page configuration
st.set_page_config(
    page_title="Yield Forecast - AgriPak Intelligence System",
    page_icon="📈",
    layout="wide",
)

# Page header
st.title("📈 Yield Forecasting")
st.markdown("Predict crop yields and identify factors affecting productivity")

# Create main sections
col1, col2 = st.columns([3, 1])

with col1:
    st.header("Yield Prediction Dashboard")
    
    # Filter controls
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        selected_crop = st.selectbox(
            "Select Crop",
            ["Wheat", "Rice", "Cotton", "Sugarcane", "Maize"]
        )
    
    with filter_col2:
        selected_season = st.selectbox(
            "Select Season",
            ["Rabi 2023-24", "Kharif 2023", "Rabi 2022-23", "Kharif 2022"]
        )
    
    with filter_col3:
        comparison_type = st.selectbox(
            "Comparison Type",
            ["Historical Average", "Previous Season", "Target Yield"]
        )
    
    # Create yield forecast map
    st.subheader("Yield Forecast Map")
    
    mapbox_token = "pk.eyJ1IjoiZW5ncmtpIiwiYSI6ImNrc29yeHB2aDBieDEydXFoY240bXExcWoifQ.WS7GVtVGZb4xgHn9dleszQ"
    yield_map = create_yield_forecast_map(mapbox_token, crop=selected_crop, season=selected_season)
    st.plotly_chart(yield_map, use_container_width=True)
    
    # Yield prediction visualization
    st.subheader("Yield Prediction Over Time")
    
    # Create sample data for the yield prediction
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    forecast_dates = [datetime.now() - timedelta(days=60 - i*5) for i in range(12)] + [datetime.now() + timedelta(days=i*5) for i in range(1, 6)]
    
    # Create different patterns based on selected crop
    if selected_crop == "Wheat":
        base_value = 3.5
        variation = 0.8
    elif selected_crop == "Rice":
        base_value = 4.0
        variation = 0.5
    else:
        base_value = 2.5
        variation = 0.4
    
    # Generate historical and forecast values
    historical_values = [base_value - variation/2 + variation * np.random.random() for _ in range(12)]
    forecast_values = [historical_values[-1] * (1 + 0.02 * i + 0.01 * np.random.random()) for i in range(1, 6)]
    
    # Combine into full dataset
    forecast_df = pd.DataFrame({
        'Date': forecast_dates,
        'Value': historical_values + forecast_values,
        'Type': ['Historical'] * 12 + ['Forecast'] * 5
    })
    
    # Create the chart
    fig = px.line(
        forecast_df, 
        x='Date', 
        y='Value', 
        color='Type',
        color_discrete_map={'Historical': 'blue', 'Forecast': 'red'},
        labels={'Value': 'Yield (tons/acre)', 'Date': 'Date'},
        title=f'{selected_crop} Yield Forecast for {selected_season}'
    )
    
    # Add confidence interval for forecast
    forecast_subset = forecast_df[forecast_df['Type'] == 'Forecast']
    
    x = forecast_subset['Date']
    y_upper = forecast_subset['Value'] * 1.1
    y_lower = forecast_subset['Value'] * 0.9
    
    fig.add_trace(
        go.Scatter(
            x=x.tolist() + x.tolist()[::-1],
            y=y_upper.tolist() + y_lower.tolist()[::-1],
            fill='toself',
            fillcolor='rgba(231,107,243,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            showlegend=True,
            name='95% Confidence Interval'
        )
    )
    
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Factors affecting yield
    st.subheader("Key Factors Affecting Yield")
    
    # Create sample data for factors
    factors_data = {
        'Factor': ['Weather Conditions', 'Soil Quality', 'Irrigation', 'Pest Control', 'Seed Quality', 'Farm Management'],
        'Impact': [0.85, 0.72, 0.68, 0.45, 0.78, 0.61],
        'Controllable': ['No', 'Partially', 'Yes', 'Yes', 'Yes', 'Yes']
    }
    
    factors_df = pd.DataFrame(factors_data)
    
    # Create horizontal bar chart
    factors_fig = px.bar(
        factors_df,
        y='Factor',
        x='Impact',
        color='Controllable',
        orientation='h',
        color_discrete_map={'Yes': 'green', 'Partially': 'orange', 'No': 'gray'},
        labels={'Impact': 'Impact on Yield', 'Factor': ''},
        title='Factors Affecting Yield and Their Controllability'
    )
    
    st.plotly_chart(factors_fig, use_container_width=True)
    
    # Regional comparison
    st.subheader("Regional Yield Comparison")
    
    # Create sample data for regional comparison
    regions = ['Punjab', 'Sindh', 'KPK', 'Balochistan', 'Your Farm']
    
    if selected_crop == "Wheat":
        yields = [3.2, 2.8, 2.5, 2.0, 3.5]
    elif selected_crop == "Rice":
        yields = [3.8, 4.1, 2.8, 2.2, 4.0]
    else:
        yields = [2.7, 2.3, 2.1, 1.8, 2.5]
        
    # Create the dataframe
    region_df = pd.DataFrame({
        'Region': regions,
        'Yield': yields
    })
    
    # Create the bar chart
    region_fig = px.bar(
        region_df,
        x='Region',
        y='Yield',
        color='Region',
        labels={'Yield': 'Yield (tons/acre)', 'Region': ''},
        title=f'Average {selected_crop} Yield by Region',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    
    # Highlight "Your Farm"
    region_fig.update_traces(
        marker_color=['blue', 'blue', 'blue', 'blue', 'green'],
        marker_line_color=['blue', 'blue', 'blue', 'blue', 'darkgreen'],
        marker_line_width=[1, 1, 1, 1, 2]
    )
    
    st.plotly_chart(region_fig, use_container_width=True)

with col2:
    st.header("Yield Insights")
    
    # Current forecast summary
    st.subheader("Current Forecast")
    
    # Show a random image
    st.image(
        get_random_image("modern_agriculture_technology"),
        caption=f"{selected_crop} field ready for harvest",
        use_column_width=True
    )
    
    # Forecast metrics
    if selected_crop == "Wheat":
        forecast_yield = "3.7 tons/acre"
        historical_avg = "3.4 tons/acre"
        forecast_change = "+8.8%"
    elif selected_crop == "Rice":
        forecast_yield = "4.2 tons/acre"
        historical_avg = "3.9 tons/acre"
        forecast_change = "+7.7%"
    else:
        forecast_yield = "2.6 tons/acre"
        historical_avg = "2.4 tons/acre"
        forecast_change = "+8.3%"
    
    st.metric(
        label="Forecasted Yield",
        value=forecast_yield,
        delta=forecast_change,
        help="Expected yield based on current conditions and historical data"
    )
    
    st.metric(
        label="Historical Average",
        value=historical_avg,
        help="5-year average yield for this crop and season"
    )
    
    # Confidence interval
    st.info("**Forecast Confidence:** 85%")
    
    # Economic impact
    st.subheader("Economic Impact")
    
    # Market price
    if selected_crop == "Wheat":
        current_price = "PKR 1,800/40kg"
        price_trend = "+5.2%"
    elif selected_crop == "Rice":
        current_price = "PKR 2,200/40kg"
        price_trend = "+3.8%"
    else:
        current_price = "PKR 6,500/40kg"
        price_trend = "+1.5%"
    
    st.metric(
        label="Current Market Price",
        value=current_price,
        delta=price_trend,
        help="Current market price with trend over last month"
    )
    
    # Estimated revenue
    st.subheader("Estimated Revenue")
    
    if selected_crop == "Wheat":
        per_acre = "PKR 168,750"
        total = "PKR 8,437,500"
    elif selected_crop == "Rice":
        per_acre = "PKR 231,000"
        total = "PKR 11,550,000"
    else:
        per_acre = "PKR 422,500"
        total = "PKR 21,125,000"
    
    st.metric(
        label="Per Acre Revenue",
        value=per_acre,
        help="Estimated revenue per acre based on current market prices"
    )
    
    st.metric(
        label="Total Farm Revenue",
        value=total,
        help="Estimated total revenue based on farm size of 50 acres"
    )
    
    # Optimization tips
    st.subheader("Yield Optimization Tips")
    
    st.markdown("""
    **1. Optimize Irrigation**
    - Schedule: Adjust timing based on soil moisture sensors
    - Amount: Reduce by 15% during mid-season
    - Potential Gain: +0.2 tons/acre
    
    **2. Nutrient Management**
    - Increase potassium by 10%
    - Apply micronutrients (Zn, B) as foliar spray
    - Potential Gain: +0.15 tons/acre
    
    **3. Pest/Disease Control**
    - Apply preventative fungicide at early heading
    - Monitor for aphids and leaf miners
    - Potential Gain: +0.25 tons/acre
    """)
    
    # Yield risk factors
    st.subheader("Risk Factors")
    
    risk_data = {
        'Risk': ['Weather Extremes', 'Pest Outbreak', 'Disease Pressure', 'Water Shortages'],
        'Probability': ['Medium', 'Low', 'Medium', 'High']
    }
    
    risk_df = pd.DataFrame(risk_data)
    
    # Add styled risk indicators
    def color_risk(val):
        color_map = {
            'Low': 'background-color: #d4f1c5; color: #145214',
            'Medium': 'background-color: #ffeeba; color: #856404',
            'High': 'background-color: #f8d7da; color: #721c24'
        }
        return color_map.get(val, '')
    
    st.dataframe(
        risk_df.style.applymap(color_risk, subset=['Probability']),
        use_container_width=True,
        hide_index=True
    )

# Historical yield analysis section
st.header("Historical Yield Analysis")

# Create tabs for different analysis views
yield_tab1, yield_tab2, yield_tab3 = st.tabs(["Seasonal Patterns", "Year-over-Year Comparison", "Yield Gap Analysis"])

with yield_tab1:
    # Seasonal patterns visualization
    
    # Create sample data for multiple years
    years = [2018, 2019, 2020, 2021, 2022, 2023]
    months_abbr = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    # Different seasonal patterns based on crop
    if selected_crop == "Wheat":
        # Rabi crop (winter) - sowing in Oct-Dec, harvest in Apr-May
        patterns = {
            2018: [0, 0, 0, 3.1, 3.2, 0, 0, 0, 0, 0.5, 1.0, 1.5],
            2019: [2.0, 2.5, 3.0, 3.2, 3.3, 0, 0, 0, 0, 0.6, 1.1, 1.6],
            2020: [2.1, 2.6, 3.1, 3.3, 3.4, 0, 0, 0, 0, 0.5, 1.0, 1.5],
            2021: [2.0, 2.5, 3.0, 3.2, 3.3, 0, 0, 0, 0, 0.6, 1.1, 1.6],
            2022: [2.1, 2.6, 3.1, 3.4, 3.5, 0, 0, 0, 0, 0.7, 1.2, 1.7],
            2023: [2.2, 2.7, 3.2, 3.5, 3.6, 0, 0, 0, 0, 0.7, 1.2, 1.7]
        }
    elif selected_crop == "Rice":
        # Kharif crop (summer) - sowing in May-Jul, harvest in Oct-Nov
        patterns = {
            2018: [0, 0, 0, 0, 0.5, 1.0, 2.0, 3.0, 3.5, 3.8, 3.9, 0],
            2019: [0, 0, 0, 0, 0.6, 1.1, 2.1, 3.1, 3.6, 3.9, 4.0, 0],
            2020: [0, 0, 0, 0, 0.7, 1.2, 2.2, 3.2, 3.7, 4.0, 4.1, 0],
            2021: [0, 0, 0, 0, 0.6, 1.1, 2.1, 3.1, 3.6, 3.9, 4.0, 0],
            2022: [0, 0, 0, 0, 0.7, 1.2, 2.2, 3.2, 3.7, 4.0, 4.1, 0],
            2023: [0, 0, 0, 0, 0.8, 1.3, 2.3, 3.3, 3.8, 4.1, 4.2, 0]
        }
    else:
        # Generic pattern
        patterns = {
            2018: [1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.5, 2.4, 2.3],
            2019: [1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.6, 2.5, 2.4],
            2020: [2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.7, 2.6, 2.5],
            2021: [1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.6, 2.5, 2.4],
            2022: [2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.7, 2.6, 2.5],
            2023: [2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 2.8, 2.7, 2.6]
        }
    
    # Create data for the chart
    seasonal_data = []
    
    for year in years:
        for i, month in enumerate(months_abbr):
            seasonal_data.append({
                'Year': year,
                'Month': month,
                'Yield': patterns[year][i]
            })
    
    seasonal_df = pd.DataFrame(seasonal_data)
    
    # Create the chart
    seasonal_fig = px.line(
        seasonal_df,
        x='Month',
        y='Yield',
        color='Year',
        markers=True,
        labels={'Yield': 'Yield (tons/acre)'},
        title=f'Seasonal Yield Patterns for {selected_crop} (2018-2023)'
    )
    
    seasonal_fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=months_abbr
        )
    )
    
    st.plotly_chart(seasonal_fig, use_container_width=True)
    
    # Add explanation
    if selected_crop == "Wheat":
        st.info("""
        **Wheat Seasonal Pattern:**
        - Sowing Period: October-December
        - Growth Phase: January-March
        - Harvest Period: April-May
        - Zero values represent periods when the crop is not in the ground
        """)
    elif selected_crop == "Rice":
        st.info("""
        **Rice Seasonal Pattern:**
        - Sowing Period: May-July
        - Growth Phase: August-September
        - Harvest Period: October-November
        - Zero values represent periods when the crop is not in the ground
        """)
    else:
        st.info(f"The chart shows the seasonal growth and yield patterns for {selected_crop} over multiple years, highlighting consistent seasonal trends.")

with yield_tab2:
    # Year over year comparison
    
    # Sample data for year over year comparison
    yearly_data = {
        'Year': [2018, 2019, 2020, 2021, 2022, 2023],
        'Yield': [3.2, 3.3, 3.4, 3.3, 3.5, 3.7] if selected_crop == "Wheat" else
                 [3.8, 3.9, 4.0, 3.9, 4.0, 4.2] if selected_crop == "Rice" else
                 [2.4, 2.5, 2.6, 2.5, 2.6, 2.7]
    }
    
    yearly_df = pd.DataFrame(yearly_data)
    
    # Calculate year-over-year percentage change
    yearly_df['YoY Change'] = yearly_df['Yield'].pct_change() * 100
    yearly_df['YoY Change'] = yearly_df['YoY Change'].fillna(0)
    
    # Create the bar chart
    yearly_fig = go.Figure()
    
    yearly_fig.add_trace(go.Bar(
        x=yearly_df['Year'],
        y=yearly_df['Yield'],
        name='Yield',
        marker_color='blue'
    ))
    
    yearly_fig.add_trace(go.Scatter(
        x=yearly_df['Year'],
        y=yearly_df['YoY Change'],
        mode='lines+markers',
        name='YoY % Change',
        marker=dict(size=8, color='red'),
        line=dict(width=2, dash='dot'),
        yaxis='y2'
    ))
    
    yearly_fig.update_layout(
        title=f'{selected_crop} Yield Year-over-Year Comparison',
        xaxis_title='Year',
        yaxis=dict(
            title='Yield (tons/acre)',
            title_font=dict(color='blue'),
            tickfont=dict(color='blue')
        ),
        yaxis2=dict(
            title='YoY % Change',
            title_font=dict(color='red'),
            tickfont=dict(color='red'),
            anchor='x',
            overlaying='y',
            side='right',
            range=[-10, 10]
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        )
    )
    
    st.plotly_chart(yearly_fig, use_container_width=True)
    
    # Add analysis table
    st.subheader("Annual Performance Analysis")
    
    # Create sample data for analysis
    analysis_data = {
        'Year': [2018, 2019, 2020, 2021, 2022, 2023],
        'Yield': yearly_df['Yield'],
        'YoY Change %': yearly_df['YoY Change'].round(1),
        'Weather Condition': ['Normal', 'Favorable', 'Favorable', 'Drought', 'Normal', 'Favorable'],
        'Key Factors': [
            'Base year',
            'Improved irrigation',
            'Better seed variety',
            'Water shortage',
            'Pest management',
            'Advanced farming techniques'
        ]
    }
    
    analysis_df = pd.DataFrame(analysis_data)
    
    # Add styling to the table
    def highlight_yield_change(s):
        if s.name == 'YoY Change %':
            return ['background-color: #d4f1c5' if x > 0 else 'background-color: #f8d7da' if x < 0 else '' for x in s]
        return [''] * len(s)
    
    st.dataframe(
        analysis_df.style.apply(highlight_yield_change),
        use_container_width=True,
        hide_index=True
    )

with yield_tab3:
    # Yield gap analysis
    
    st.subheader("Yield Gap Analysis")
    
    # Create sample data for yield gap analysis
    gap_data = {
        'Category': ['Current Farm Yield', 'Regional Average', 'National Average', 'Research Station', 'Theoretical Maximum'],
        'Yield': [3.7, 3.2, 3.0, 4.5, 5.2] if selected_crop == "Wheat" else
                 [4.2, 3.9, 3.6, 5.0, 5.8] if selected_crop == "Rice" else
                 [2.7, 2.3, 2.1, 3.5, 4.0]
    }
    
    gap_df = pd.DataFrame(gap_data)
    
    # Create the chart
    gap_fig = px.bar(
        gap_df,
        x='Category',
        y='Yield',
        color='Category',
        labels={'Yield': 'Yield (tons/acre)'},
        title=f'Yield Gap Analysis for {selected_crop}',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    
    gap_fig.add_shape(
        type="line",
        x0=-0.5,
        y0=gap_df.iloc[0, 1],
        x1=4.5,
        y1=gap_df.iloc[0, 1],
        line=dict(
            color="red",
            width=2,
            dash="dash",
        )
    )
    
    gap_fig.add_annotation(
        x=2.5,
        y=gap_df.iloc[0, 1] + 0.15,
        text="Current Yield Level",
        showarrow=False,
        font=dict(
            size=12,
            color="red"
        )
    )
    
    st.plotly_chart(gap_fig, use_container_width=True)
    
    # Yield improvement potential
    st.subheader("Yield Improvement Potential")
    
    # Create columns for different categories
    improvement_col1, improvement_col2 = st.columns(2)
    
    with improvement_col1:
        st.markdown("### Short-term Potential")
        
        # Calculate potential improvements
        current_yield = gap_data['Yield'][0]
        region_potential = ((gap_data['Yield'][1] / current_yield) - 1) * 100
        national_potential = ((gap_data['Yield'][2] / current_yield) - 1) * 100
        research_potential = ((gap_data['Yield'][3] / current_yield) - 1) * 100
        theoretical_potential = ((gap_data['Yield'][4] / current_yield) - 1) * 100
        
        short_term_data = {
            'Target': ['Match Regional Top Performers', 'Improve Irrigation Efficiency', 'Enhanced Nutrient Management', 'Better Pest Control'],
            'Potential Gain': ['+0.3 tons/acre', '+0.2 tons/acre', '+0.15 tons/acre', '+0.1 tons/acre'],
            'Timeframe': ['1 season', '1 season', '1 season', '1 season'],
            'Investment': ['Medium', 'Low', 'Low', 'Low']
        }
        
        short_term_df = pd.DataFrame(short_term_data)
        
        st.dataframe(short_term_df, use_container_width=True, hide_index=True)
    
    with improvement_col2:
        st.markdown("### Long-term Potential")
        
        long_term_data = {
            'Target': ['Reach Research Station Levels', 'Precision Agriculture', 'Improved Varieties', 'Soil Health Restoration'],
            'Potential Gain': ['+0.8 tons/acre', '+0.5 tons/acre', '+0.4 tons/acre', '+0.3 tons/acre'],
            'Timeframe': ['3-5 years', '2-3 years', '1-2 years', '2-4 years'],
            'Investment': ['High', 'High', 'Medium', 'Medium']
        }
        
        long_term_df = pd.DataFrame(long_term_data)
        
        st.dataframe(long_term_df, use_container_width=True, hide_index=True)
    
    # Add explanation of yield gap
    st.info(f"""
    **Understanding Yield Gaps**
    
    The current {selected_crop} yield at your farm is {gap_data['Yield'][0]} tons/acre, which is:
    - {abs(region_potential):.1f}% {'higher' if region_potential >= 0 else 'lower'} than the regional average
    - {abs(national_potential):.1f}% {'higher' if national_potential >= 0 else 'lower'} than the national average
    - {abs(research_potential):.1f}% {'lower' if research_potential < 0 else 'higher'} than research station yields
    - {abs(theoretical_potential):.1f}% {'lower' if theoretical_potential < 0 else 'higher'} than the theoretical maximum
    
    Closing these yield gaps represents a significant opportunity for productivity improvement.
    """)

# Footer with download and sharing options
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Download Forecast Report")
    st.download_button(
        label="Download PDF Report",
        data="This would be a PDF report in a real application",
        file_name=f"{selected_crop}_yield_forecast_{selected_season}.pdf",
        mime="application/pdf"
    )

with col2:
    st.subheader("Export Data")
    st.download_button(
        label="Export as CSV",
        data="This would be CSV data in a real application",
        file_name=f"{selected_crop}_yield_data_{selected_season}.csv",
        mime="text/csv"
    )

with col3:
    st.subheader("Share Forecast")
    st.text_input("Email Address")
    st.button("Share via Email")
