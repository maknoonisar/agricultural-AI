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
    page_title="Reports & Analytics - AgriPak Intelligence System",
    page_icon="📝",
    layout="wide",
)

# Page header
st.title("📝 Reports & Analytics")
st.markdown("Generate detailed reports and analytics for your farm")

# Create report creation form
st.header("Report Generation")

# Create columns for report type and period
col1, col2 = st.columns(2)

with col1:
    report_type = st.selectbox(
        "Report Type",
        ["Farm Overview", "Crop Health", "Yield Analysis", "Resource Utilization", "Weather Impact", "Financial Performance", "Custom"]
    )

with col2:
    report_period = st.selectbox(
        "Report Period",
        ["Last Week", "Last Month", "Last Quarter", "Last 6 Months", "Last Year", "Custom Period"]
    )

# Custom period selector (show if Custom Period is selected)
if report_period == "Custom Period":
    start_date, end_date = st.columns(2)
    with start_date:
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
    with end_date:
        end_date = st.date_input("End Date", datetime.now())

# Additional report options
st.subheader("Report Options")

# Create columns for options
options_col1, options_col2, options_col3 = st.columns(3)

with options_col1:
    include_charts = st.checkbox("Include Visualizations", value=True)
    include_maps = st.checkbox("Include Farm Maps", value=True)
    include_recommendations = st.checkbox("Include Recommendations", value=True)

with options_col2:
    include_raw_data = st.checkbox("Include Raw Data Tables", value=False)
    include_benchmarks = st.checkbox("Include Industry Benchmarks", value=True)
    include_trends = st.checkbox("Include Trend Analysis", value=True)

with options_col3:
    report_format = st.radio("Report Format", ["PDF", "Excel", "Web Dashboard"])
    automatic_scheduling = st.checkbox("Schedule Recurring Report", value=False)

# If scheduling is enabled, show scheduling options
if automatic_scheduling:
    schedule_col1, schedule_col2 = st.columns(2)
    
    with schedule_col1:
        schedule_frequency = st.selectbox(
            "Frequency",
            ["Daily", "Weekly", "Bi-weekly", "Monthly", "Quarterly"]
        )
    
    with schedule_col2:
        delivery_method = st.multiselect(
            "Delivery Method",
            ["Email", "SMS Notification", "WhatsApp", "In-App"]
        )
    
    email_recipients = st.text_input("Email Recipients (comma-separated)", "farmer@example.com")

# Generate Report button
if st.button("Generate Report", type="primary"):
    st.success("Report generation initiated. Your report will be ready shortly.")
    
    # Show progress bar
    progress_bar = st.progress(0)
    for i in range(100):
        # Simulate report generation
        progress_bar.progress(i + 1)
    
    st.balloons()

# Report preview section
st.header("Report Preview")

# Different previews based on report type
if report_type == "Farm Overview":
    tab1, tab2, tab3 = st.tabs(["Summary", "Crop Status", "Resource Overview"])
    
    with tab1:
        # Create columns for summary information
        summary_col1, summary_col2 = st.columns([1, 2])
        
        with summary_col1:
            st.subheader("Farm Information")
            
            st.markdown("""
            **Farm Name:** Demo Farm  
            **Location:** Punjab, Pakistan  
            **Total Area:** 50 Acres  
            **Main Crops:** Wheat, Rice, Cotton  
            **Reporting Period:** Last Month  
            **Report Generated:** October 15, 2023
            """)
            
            # Show a random image
            st.image(
                get_random_image("farming_landscapes_pakistan"),
                caption="Farm overview",
                use_column_width=True
            )
        
        with summary_col2:
            st.subheader("Farm Performance Summary")
            
            # Create KPI metrics
            kpi_col1, kpi_col2 = st.columns(2)
            
            with kpi_col1:
                st.metric(label="Overall Health Score", value="76/100", delta="4")
                st.metric(label="Resource Efficiency", value="82%", delta="5%")
                st.metric(label="Predicted Yield", value="4.2 tons/acre", delta="0.3 tons")
            
            with kpi_col2:
                st.metric(label="Weather Risk Level", value="Low", delta="unchanged")
                st.metric(label="Pest Pressure", value="Medium", delta="-10%")
                st.metric(label="Projected Revenue", value="PKR 8.4M", delta="12%")
            
            # Create farm map
            st.subheader("Farm Map")
            mapbox_token = "YOUR_MAPBOX_TOKEN"  # This would come from environment variables in production
            farm_map = create_farm_map(mapbox_token, latitude=31.5204, longitude=74.3587, zoom=10)
            st.plotly_chart(farm_map, use_container_width=True)
    
    with tab2:
        st.subheader("Crop Status Summary")
        
        # Create sample data for crop status
        crop_data = {
            'Crop': ['Wheat', 'Rice', 'Cotton', 'Sugarcane'],
            'Area (Acres)': [20, 15, 10, 5],
            'Health Score': [85, 78, 65, 80],
            'Growth Stage': ['Harvesting', 'Flowering', 'Boll Development', 'Grand Growth'],
            'Yield Forecast': ['4.5 tons/acre', '3.8 tons/acre', '2.2 tons/acre', '35 tons/acre']
        }
        
        crop_df = pd.DataFrame(crop_data)
        
        # Display crop status table
        st.dataframe(crop_df, use_container_width=True, hide_index=True)
        
        # Create crop area visualization
        area_fig = px.pie(
            crop_df,
            values='Area (Acres)',
            names='Crop',
            title='Crop Area Distribution',
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        
        st.plotly_chart(area_fig, use_container_width=True)
        
        # Create crop health visualization
        health_fig = px.bar(
            crop_df,
            x='Crop',
            y='Health Score',
            color='Health Score',
            color_continuous_scale='RdYlGn',
            title='Crop Health Scores'
        )
        
        st.plotly_chart(health_fig, use_container_width=True)
    
    with tab3:
        st.subheader("Resource Utilization Summary")
        
        # Create sample data for resource utilization
        resource_data = {
            'Resource': ['Water', 'Fertilizer', 'Pesticides', 'Energy', 'Labor'],
            'Usage': [350000, 5000, 800, 12000, 800],
            'Unit': ['m³', 'kg', 'liters', 'kWh', 'hours'],
            'Cost (PKR)': [700000, 350000, 250000, 180000, 320000],
            'Efficiency Score': [85, 72, 68, 76, 80]
        }
        
        resource_df = pd.DataFrame(resource_data)
        
        # Display resource utilization table
        st.dataframe(resource_df, use_container_width=True, hide_index=True)
        
        # Create resource cost visualization
        cost_fig = px.pie(
            resource_df,
            values='Cost (PKR)',
            names='Resource',
            title='Resource Cost Distribution',
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        
        cost_fig.update_layout(
            height=400
        )
        
        resource_col1, resource_col2 = st.columns(2)
        
        with resource_col1:
            st.plotly_chart(cost_fig, use_container_width=True)
        
        with resource_col2:
            # Create efficiency visualization
            efficiency_fig = px.bar(
                resource_df,
                x='Resource',
                y='Efficiency Score',
                color='Efficiency Score',
                color_continuous_scale='RdYlGn',
                title='Resource Efficiency Scores'
            )
            
            efficiency_fig.update_layout(
                height=400
            )
            
            st.plotly_chart(efficiency_fig, use_container_width=True)
        
        # Resource utilization recommendations
        st.subheader("Resource Optimization Recommendations")
        
        st.info("""
        **Water Management**
        - Implement drip irrigation in cotton fields to reduce water usage by 20-25%
        - Schedule irrigation based on soil moisture readings to optimize timing
        - Repair leaks in the northern field irrigation system
        
        **Fertilizer Application**
        - Switch to split application method to improve nitrogen use efficiency
        - Reduce phosphorus application in southern fields based on soil tests
        - Consider precision application technology for variable rate application
        
        **Energy Conservation**
        - Shift irrigation pumping to morning/evening to reduce electricity costs
        - Conduct maintenance on farm machinery to improve fuel efficiency
        - Investigate solar pumping options for long-term cost savings
        """)

elif report_type == "Crop Health":
    # Crop health report preview
    crop_health_col1, crop_health_col2 = st.columns([2, 1])
    
    with crop_health_col1:
        st.subheader("Crop Health Analysis")
        
        # Create crop health visualization
        health_chart = create_crop_health_chart()
        st.plotly_chart(health_chart, use_container_width=True)
        
        # Disease detection summary
        st.subheader("Disease Detection Summary")
        
        disease_data = {
            'Date': ['2023-10-12', '2023-10-05', '2023-09-28', '2023-09-15'],
            'Crop': ['Wheat', 'Rice', 'Wheat', 'Cotton'],
            'Field': ['North Field', 'East Field', 'South Field', 'West Field'],
            'Disease': ['Leaf Rust', 'Blast', 'Powdery Mildew', 'Leaf Curl Virus'],
            'Severity': ['Low', 'Medium', 'Low', 'High'],
            'Treatment': ['Fungicide Applied', 'Fungicide Applied', 'Monitoring', 'Insecticide Applied']
        }
        
        disease_df = pd.DataFrame(disease_data)
        
        # Function to apply styling based on severity
        def highlight_severity(s):
            styles = []
            for val in s:
                if val == "High":
                    styles.append('background-color: #f8d7da; color: #721c24')
                elif val == "Medium":
                    styles.append('background-color: #fff3cd; color: #856404')
                elif val == "Low":
                    styles.append('background-color: #d4edda; color: #155724')
                else:
                    styles.append('')
            return styles
        
        # Display styled dataframe
        st.dataframe(
            disease_df.style.apply(highlight_severity, subset=['Severity']),
            use_container_width=True,
            hide_index=True
        )
        
        # Disease distribution visualization
        disease_count = disease_df.groupby(['Disease', 'Severity']).size().reset_index(name='Count')
        
        disease_fig = px.bar(
            disease_count,
            x='Disease',
            y='Count',
            color='Severity',
            title='Disease Distribution',
            color_discrete_map={'Low': 'green', 'Medium': 'orange', 'High': 'red'}
        )
        
        st.plotly_chart(disease_fig, use_container_width=True)
    
    with crop_health_col2:
        st.subheader("Health Metrics")
        
        # Display crop images
        st.image(
            get_random_image("crop_disease_examples"),
            caption="Recent crop health scan",
            use_column_width=True
        )
        
        # Key health metrics
        health_metrics = {
            'Metric': ['NDVI Average', 'Leaf Area Index', 'Canopy Temperature', 'Chlorophyll Content', 'Stress Detection'],
            'Value': ['0.76', '3.8', '28°C', '42 CCI', '12%'],
            'Status': ['Good', 'Good', 'Optimal', 'Good', 'Low']
        }
        
        health_metrics_df = pd.DataFrame(health_metrics)
        
        st.dataframe(health_metrics_df, use_container_width=True, hide_index=True)
        
        # Treatment recommendations
        st.subheader("Treatment Recommendations")
        
        st.info("""
        **Wheat Leaf Rust (North Field)**
        - Apply propiconazole fungicide at 125g/acre
        - Monitor for 7 days following application
        - Increase potassium in next fertilizer application
        
        **Rice Blast (East Field)**
        - Apply tricyclazole fungicide at recommended rate
        - Ensure proper water management
        - Monitor nitrogen levels and avoid excess
        
        **Preventative Measures**
        - Implement regular monitoring schedule
        - Consider resistant varieties for next planting
        - Maintain balanced nutrition program
        """)
        
        # Preventative schedule
        st.subheader("Preventative Schedule")
        
        preventative_data = {
            'Week': ['Oct 16-22', 'Oct 23-29', 'Oct 30-Nov 5', 'Nov 6-12'],
            'Action': ['Fungicide Application', 'Monitoring', 'Foliar Nutrition', 'Monitoring'],
            'Fields': ['North, East', 'All Fields', 'North, South', 'All Fields'],
            'Priority': ['High', 'Medium', 'Medium', 'Medium']
        }
        
        preventative_df = pd.DataFrame(preventative_data)
        
        st.dataframe(preventative_df, use_container_width=True, hide_index=True)

elif report_type == "Yield Analysis":
    # Yield analysis report preview
    st.subheader("Yield Forecast Summary")
    
    # Create columns for summary information
    yield_col1, yield_col2 = st.columns([2, 1])
    
    with yield_col1:
        # Create yield visualization
        yield_chart = create_yield_chart()
        st.plotly_chart(yield_chart, use_container_width=True)
        
        # Create year over year comparison
        years = [2019, 2020, 2021, 2022, 2023]
        
        yoy_data = {
            'Year': years,
            'Wheat Yield': [3.2, 3.3, 3.2, 3.5, 3.7],
            'Rice Yield': [3.8, 3.9, 3.8, 3.9, 4.2],
            'Cotton Yield': [2.2, 2.3, 2.1, 2.3, 2.5]
        }
        
        yoy_df = pd.DataFrame(yoy_data)
        
        # Melt the dataframe for better visualization
        yoy_df_melted = pd.melt(
            yoy_df, 
            id_vars=['Year'], 
            value_vars=['Wheat Yield', 'Rice Yield', 'Cotton Yield'],
            var_name='Crop', 
            value_name='Yield (tons/acre)'
        )
        
        yoy_fig = px.line(
            yoy_df_melted,
            x='Year',
            y='Yield (tons/acre)',
            color='Crop',
            markers=True,
            title='Yield Trends (2019-2023)'
        )
        
        st.plotly_chart(yoy_fig, use_container_width=True)
        
        # Yield comparison with benchmarks
        benchmark_data = {
            'Crop': ['Wheat', 'Rice', 'Cotton', 'Sugarcane'],
            'Your Farm': [3.7, 4.2, 2.5, 35.0],
            'District Average': [3.2, 3.7, 2.2, 32.0],
            'Provincial Average': [3.0, 3.5, 2.0, 30.0],
            'National Average': [2.8, 3.3, 1.8, 28.0]
        }
        
        benchmark_df = pd.DataFrame(benchmark_data)
        
        # Melt the dataframe for better visualization
        benchmark_df_melted = pd.melt(
            benchmark_df,
            id_vars=['Crop'],
            value_vars=['Your Farm', 'District Average', 'Provincial Average', 'National Average'],
            var_name='Benchmark',
            value_name='Yield (tons/acre)'
        )
        
        benchmark_fig = px.bar(
            benchmark_df_melted,
            x='Crop',
            y='Yield (tons/acre)',
            color='Benchmark',
            barmode='group',
            title='Yield Comparison with Benchmarks'
        )
        
        st.plotly_chart(benchmark_fig, use_container_width=True)
    
    with yield_col2:
        st.subheader("Current Forecasts")
        
        # Display yield forecasts
        forecast_data = {
            'Crop': ['Wheat', 'Rice', 'Cotton', 'Sugarcane'],
            'Current Forecast': ['3.7 tons/acre', '4.2 tons/acre', '2.5 tons/acre', '35.0 tons/acre'],
            'Change': ['+5.7%', '+7.7%', '+8.7%', '+3.0%'],
            'Confidence': ['85%', '82%', '75%', '90%']
        }
        
        forecast_df = pd.DataFrame(forecast_data)
        
        st.dataframe(forecast_df, use_container_width=True, hide_index=True)
        
        # Show a farm image
        st.image(
            get_random_image("farming_landscapes_pakistan"),
            caption="Wheat field ready for harvest",
            use_column_width=True
        )
        
        # Yield optimization recommendations
        st.subheader("Yield Optimization Recommendations")
        
        st.info("""
        **For Wheat:**
        - Apply potassium fertilizer at heading stage
        - Optimize irrigation during grain filling
        - Monitor and control rust diseases proactively
        
        **For Rice:**
        - Maintain optimal water levels during flowering
        - Apply additional nitrogen after panicle initiation
        - Implement alternate wetting and drying irrigation
        
        **For Cotton:**
        - Apply plant growth regulators to control height
        - Focus on pest management during boll development
        - Optimize irrigation to prevent stress during flowering
        """)
        
        # Factors affecting yield
        st.subheader("Key Yield Factors")
        
        factors_data = {
            'Factor': ['Water Management', 'Fertilization', 'Pest Control', 'Variety Selection', 'Planting Date'],
            'Impact': ['High', 'High', 'Medium', 'High', 'Medium']
        }
        
        factors_df = pd.DataFrame(factors_data)
        
        st.dataframe(factors_df, use_container_width=True, hide_index=True)

elif report_type == "Resource Utilization":
    # Resource utilization report preview
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Water Usage", "Fertilizer Usage", "Energy Usage"])
    
    with tab1:
        st.subheader("Resource Utilization Summary")
        
        # Create sample data for resource utilization
        resource_overview = {
            'Resource': ['Water', 'Fertilizer', 'Pesticides', 'Energy', 'Labor'],
            'Current Usage': [350000, 5000, 800, 12000, 800],
            'Unit': ['m³', 'kg', 'liters', 'kWh', 'hours'],
            'Cost (PKR)': [700000, 350000, 250000, 180000, 320000],
            'Efficiency': ['75%', '82%', '68%', '70%', '85%'],
            'Savings Potential': ['25%', '18%', '22%', '30%', '15%']
        }
        
        resource_overview_df = pd.DataFrame(resource_overview)
        
        # Display resource overview table
        st.dataframe(resource_overview_df, use_container_width=True, hide_index=True)
        
        # Create resource cost visualization
        cost_fig = px.pie(
            resource_overview_df,
            values='Cost (PKR)',
            names='Resource',
            title='Resource Cost Distribution',
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        
        st.plotly_chart(cost_fig, use_container_width=True)
        
        # Create potential savings visualization
        # First, calculate the potential savings in PKR
        resource_overview_df['Savings (PKR)'] = [
            int(cost * float(savings.strip('%')) / 100) 
            for cost, savings in zip(resource_overview_df['Cost (PKR)'], resource_overview_df['Savings Potential'])
        ]
        
        savings_fig = px.bar(
            resource_overview_df,
            x='Resource',
            y='Savings (PKR)',
            color='Resource',
            title='Potential Cost Savings by Resource'
        )
        
        st.plotly_chart(savings_fig, use_container_width=True)
        
        # Total cost and potential savings
        total_cost = sum(resource_overview_df['Cost (PKR)'])
        total_savings = sum(resource_overview_df['Savings (PKR)'])
        
        st.info(f"""
        **Resource Utilization Summary:**
        - Total Resource Cost: PKR {total_cost:,}
        - Potential Annual Savings: PKR {total_savings:,} ({(total_savings/total_cost)*100:.1f}%)
        - Efficiency Improvement Potential: Significant opportunities in Water, Energy, and Pesticide usage
        """)
    
    with tab2:
        st.subheader("Water Usage Analysis")
        
        # Create sample data for water usage by field
        fields = ['North Field', 'South Field', 'East Field', 'West Field']
        crops = ['Wheat', 'Rice', 'Cotton', 'Sugarcane']
        areas = [20, 15, 10, 5]  # acres
        water_usage = [120, 180, 90, 110]  # mm/week
        total_usage = [water * area * 25.4 / 304.8 for water, area in zip(water_usage, areas)]  # acre-feet
        cost_per_acre_foot = 5000  # PKR
        water_cost = [usage * cost_per_acre_foot for usage in total_usage]
        efficiency = [75, 65, 85, 70]  # percent
        
        water_data = {
            'Field': fields,
            'Crop': crops,
            'Area (acres)': areas,
            'Water Usage (mm/week)': water_usage,
            'Total Usage (acre-feet)': [round(u, 2) for u in total_usage],
            'Cost (PKR)': [int(c) for c in water_cost],
            'Efficiency (%)': efficiency
        }
        
        water_df = pd.DataFrame(water_data)
        
        # Display water usage table
        st.dataframe(water_df, use_container_width=True, hide_index=True)
        
        # Create water usage by field visualization
        water_field_fig = px.bar(
            water_df,
            x='Field',
            y='Water Usage (mm/week)',
            color='Crop',
            title='Water Usage by Field'
        )
        
        # Create water efficiency visualization
        water_eff_fig = px.bar(
            water_df,
            x='Field',
            y='Efficiency (%)',
            color='Efficiency (%)',
            color_continuous_scale='Blues',
            title='Water Efficiency by Field'
        )
        
        water_col1, water_col2 = st.columns(2)
        
        with water_col1:
            st.plotly_chart(water_field_fig, use_container_width=True)
        
        with water_col2:
            st.plotly_chart(water_eff_fig, use_container_width=True)
        
        # Water usage recommendations
        st.subheader("Water Optimization Recommendations")
        
        st.info("""
        **Field-Specific Recommendations:**
        
        **South Field (Rice):**
        - Implement alternate wetting and drying irrigation
        - Install soil moisture sensors for better timing
        - Repair leaks in irrigation channels
        Potential savings: 25-30%
        
        **North Field (Wheat):**
        - Adjust irrigation schedule based on evapotranspiration
        - Apply mulch to reduce evaporation
        - Consider deficit irrigation during less sensitive stages
        Potential savings: 15-20%
        
        **Overall Recommendations:**
        - Implement drip irrigation for high-value crops
        - Schedule irrigation during early morning or evening
        - Improve maintenance of irrigation infrastructure
        """)
    
    with tab3:
        st.subheader("Fertilizer Usage Analysis")
        
        # Create sample data for fertilizer usage
        fertilizer_types = ['Urea', 'DAP', 'Potash', 'Zinc Sulfate', 'Boron']
        applications = [150, 85, 60, 5, 2]  # kg/acre
        total_application = [app * 50 for app in applications]  # for 50 acres
        unit_costs = [110, 150, 130, 300, 500]  # PKR/kg
        total_costs = [app * cost for app, cost in zip(total_application, unit_costs)]
        efficiency_ratings = [80, 70, 85, 75, 65]  # percent
        
        fertilizer_data = {
            'Fertilizer': fertilizer_types,
            'Application Rate (kg/acre)': applications,
            'Total Application (kg)': total_application,
            'Unit Cost (PKR/kg)': unit_costs,
            'Total Cost (PKR)': [int(c) for c in total_costs],
            'Efficiency (%)': efficiency_ratings
        }
        
        fertilizer_df = pd.DataFrame(fertilizer_data)
        
        # Display fertilizer usage table
        st.dataframe(fertilizer_df, use_container_width=True, hide_index=True)
        
        # Create fertilizer usage visualization
        fert_fig = px.bar(
            fertilizer_df,
            x='Fertilizer',
            y='Total Cost (PKR)',
            color='Efficiency (%)',
            color_continuous_scale='RdYlGn',
            title='Fertilizer Cost and Efficiency'
        )
        
        st.plotly_chart(fert_fig, use_container_width=True)
        
        # Create nutrient balance visualization
        nutrient_data = {
            'Nutrient': ['Nitrogen', 'Phosphorus', 'Potassium', 'Zinc', 'Boron'],
            'Applied': [100, 45, 60, 2.5, 0.5],  # kg/acre
            'Recommended': [90, 50, 70, 3, 0.6],  # kg/acre
            'Balance': ['+10', '-5', '-10', '-0.5', '-0.1']  # kg/acre
        }
        
        nutrient_df = pd.DataFrame(nutrient_data)
        
        # Create nutrient balance visualization
        nutrient_fig = go.Figure()
        
        nutrient_fig.add_trace(go.Bar(
            x=nutrient_df['Nutrient'],
            y=nutrient_df['Applied'],
            name='Applied',
            marker_color='blue'
        ))
        
        nutrient_fig.add_trace(go.Bar(
            x=nutrient_df['Nutrient'],
            y=nutrient_df['Recommended'],
            name='Recommended',
            marker_color='green'
        ))
        
        nutrient_fig.update_layout(
            title='Nutrient Balance Analysis',
            barmode='group'
        )
        
        st.plotly_chart(nutrient_fig, use_container_width=True)
        
        # Fertilizer recommendations
        st.subheader("Fertilizer Optimization Recommendations")
        
        st.info("""
        **Nutrient-Specific Recommendations:**
        
        **Nitrogen:**
        - Reduce urea application by 10% to avoid excess
        - Switch to split application (3-4 applications)
        - Consider using nitrogen inhibitors
        Potential savings: 10-15%
        
        **Phosphorus:**
        - Increase DAP application by 10%
        - Apply in bands near root zone for better efficiency
        - Consider foliar application for immediate response
        
        **Potassium:**
        - Increase application by 15% to meet crop requirements
        - Apply before flowering/grain filling stages
        - Consider foliar application during stress periods
        
        **Micronutrients:**
        - Increase zinc and boron applications slightly
        - Apply as foliar spray for better absorption
        - Mix with major fertilizer applications
        """)
    
    with tab4:
        st.subheader("Energy Usage Analysis")
        
        # Create sample data for energy usage
        energy_sources = ['Electricity', 'Diesel', 'Petrol', 'Natural Gas', 'Solar']
        consumption = [9500, 1200, 300, 200, 0]  # kWh, liters, liters, m³, kWh
        units = ['kWh', 'liters', 'liters', 'm³', 'kWh']
        unit_costs = [22, 150, 180, 1400, 0]  # PKR per unit
        total_costs = [cons * cost for cons, cost in zip(consumption, unit_costs)]
        co2_emissions = [5700, 3240, 690, 400, 0]  # kg CO2
        
        energy_data = {
            'Energy Source': energy_sources,
            'Consumption': consumption,
            'Unit': units,
            'Unit Cost (PKR)': unit_costs,
            'Total Cost (PKR)': [int(c) for c in total_costs],
            'CO2 Emissions (kg)': co2_emissions
        }
        
        energy_df = pd.DataFrame(energy_data)
        
        # Display energy usage table
        st.dataframe(energy_df, use_container_width=True, hide_index=True)
        
        # Create energy cost visualization
        energy_cost_fig = px.pie(
            energy_df,
            values='Total Cost (PKR)',
            names='Energy Source',
            title='Energy Cost Distribution',
            color_discrete_sequence=px.colors.sequential.Plasma
        )
        
        # Create CO2 emissions visualization
        emissions_fig = px.bar(
            energy_df,
            x='Energy Source',
            y='CO2 Emissions (kg)',
            color='Energy Source',
            title='CO2 Emissions by Energy Source'
        )
        
        energy_col1, energy_col2 = st.columns(2)
        
        with energy_col1:
            st.plotly_chart(energy_cost_fig, use_container_width=True)
        
        with energy_col2:
            st.plotly_chart(emissions_fig, use_container_width=True)
        
        # Energy usage by operation
        operations = ['Irrigation', 'Tillage', 'Harvesting', 'Processing', 'Transport']
        energy_by_op = [50, 15, 20, 10, 5]  # percentage
        
        op_data = {
            'Operation': operations,
            'Energy Usage (%)': energy_by_op
        }
        
        op_df = pd.DataFrame(op_data)
        
        op_fig = px.bar(
            op_df,
            x='Operation',
            y='Energy Usage (%)',
            color='Operation',
            title='Energy Usage by Operation'
        )
        
        st.plotly_chart(op_fig, use_container_width=True)
        
        # Energy optimization recommendations
        st.subheader("Energy Optimization Recommendations")
        
        st.info("""
        **Source-Specific Recommendations:**
        
        **Electricity:**
        - Install variable frequency drives on irrigation pumps
        - Shift irrigation to off-peak hours
        - Implement proper maintenance of motors
        Potential savings: 20-25%
        
        **Diesel:**
        - Optimize tractor operations with GPS guidance
        - Regular maintenance of engines
        - Reduce idling time during operations
        Potential savings: 15-20%
        
        **Alternative Energy:**
        - Install solar pumping system for irrigation
        - Estimated cost: PKR 800,000
        - Payback period: 3-4 years
        - Potential annual savings: PKR 200,000+
        
        **Overall Recommendations:**
        - Conduct energy audit of major equipment
        - Train operators on energy-efficient practices
        - Monitor and track energy usage by operation
        """)

elif report_type == "Weather Impact":
    # Weather impact report preview
    weather_col1, weather_col2 = st.columns([2, 1])
    
    with weather_col1:
        st.subheader("Weather Pattern Analysis")
        
        # Create sample data for temperature over time
        dates = pd.date_range(start='2023-09-15', end='2023-10-15')
        max_temps = [32 + 5 * np.sin(i/5) + np.random.normal(0, 1) for i in range(len(dates))]
        min_temps = [20 + 5 * np.sin(i/5) + np.random.normal(0, 1) for i in range(len(dates))]
        rainfall = [0] * len(dates)
        
        # Add some rainfall events
        for i in [5, 6, 15, 16, 25]:
            if i < len(dates):
                rainfall[i] = np.random.randint(5, 20)
        
        weather_data = {
            'Date': dates,
            'Max Temp (°C)': max_temps,
            'Min Temp (°C)': min_temps,
            'Rainfall (mm)': rainfall
        }
        
        weather_df = pd.DataFrame(weather_data)
        
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
        
        temp_fig.update_layout(
            title='Temperature Trends (Last 30 Days)',
            xaxis_title='Date',
            yaxis_title='Temperature (°C)'
        )
        
        st.plotly_chart(temp_fig, use_container_width=True)
        
        # Create rainfall chart
        rain_fig = px.bar(
            weather_df,
            x='Date',
            y='Rainfall (mm)',
            title='Rainfall (Last 30 Days)',
            color='Rainfall (mm)',
            color_continuous_scale='Blues'
        )
        
        st.plotly_chart(rain_fig, use_container_width=True)
        
        # Weather deviation from normal
        st.subheader("Weather Deviation from Normal")
        
        # Create sample data for deviations
        deviation_data = {
            'Month': ['Jun', 'Jul', 'Aug', 'Sep', 'Oct'],
            'Temperature Deviation (°C)': [1.5, 2.1, 1.8, 1.2, 0.9],
            'Rainfall Deviation (%)': [-15, -20, -10, 5, 10]
        }
        
        deviation_df = pd.DataFrame(deviation_data)
        
        # Create deviation chart
        dev_fig = go.Figure()
        
        dev_fig.add_trace(go.Bar(
            x=deviation_df['Month'],
            y=deviation_df['Temperature Deviation (°C)'],
            name='Temperature Deviation (°C)',
            marker_color='red'
        ))
        
        dev_fig.add_trace(go.Scatter(
            x=deviation_df['Month'],
            y=deviation_df['Rainfall Deviation (%)'],
            mode='lines+markers',
            name='Rainfall Deviation (%)',
            marker=dict(size=8, color='blue'),
            line=dict(width=2),
            yaxis='y2'
        ))
        
        dev_fig.update_layout(
            title='Weather Deviation from Normal (Last 5 Months)',
            xaxis_title='Month',
            yaxis=dict(
                title='Temperature Deviation (°C)',
                title_font=dict(color='red'),
                tickfont=dict(color='red')
            ),
            yaxis2=dict(
                title='Rainfall Deviation (%)',
                title_font=dict(color='blue'),
                tickfont=dict(color='blue'),
                anchor='x',
                overlaying='y',
                side='right'
            ),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            )
        )
        
        st.plotly_chart(dev_fig, use_container_width=True)
    
    with weather_col2:
        st.subheader("Weather Impact Summary")
        
        # Display an image
        st.image(
            get_random_image("agricultural_drone_imagery"),
            caption="Weather impact visualization",
            use_column_width=True
        )
        
        # Weather metrics
        weather_metrics = {
            'Metric': ['Average Temperature', 'Total Rainfall', 'Growing Degree Days', 'Heat Stress Days', 'Water Deficit'],
            'Value': ['28.5°C', '35mm', '550', '8 days', '15mm'],
            'Impact': ['Moderate', 'Negative', 'Positive', 'Negative', 'Moderate']
        }
        
        weather_metrics_df = pd.DataFrame(weather_metrics)
        
        st.dataframe(weather_metrics_df, use_container_width=True, hide_index=True)
        
        # Crop-specific weather impacts
        st.subheader("Crop-Specific Impacts")
        
        st.info("""
        **Wheat:**
        - Higher temperatures accelerated development
        - Slight moisture stress during grain filling
        - Overall impact: Neutral to slightly negative
        
        **Rice:**
        - Higher temperatures increased water requirements
        - Adequate irrigation prevented significant stress
        - Overall impact: Neutral
        
        **Cotton:**
        - Heat stress during flowering stage
        - Increased pest pressure due to hot conditions
        - Overall impact: Moderate negative
        """)
        
        # Weather alerts summary
        st.subheader("Weather Alert Summary")
        
        alerts_data = {
            'Date': ['Sep 20', 'Oct 1', 'Oct 10'],
            'Alert Type': ['Heat Warning', 'Heavy Rain', 'Wind Advisory'],
            'Impact': ['Moderate', 'Minimal', 'Minimal'],
            'Action Taken': ['Increased Irrigation', 'Delayed Fertilizer', 'Delayed Spray']
        }
        
        alerts_df = pd.DataFrame(alerts_data)
        
        st.dataframe(alerts_df, use_container_width=True, hide_index=True)
        
        # Weather adaptation recommendations
        st.subheader("Weather Adaptation Recommendations")
        
        st.info("""
        **Short-term Adjustments:**
        - Increase irrigation frequency in cotton fields
        - Apply foliar potassium to mitigate heat stress
        - Monitor for increased pest activity
        
        **Long-term Adaptations:**
        - Adopt heat-tolerant crop varieties
        - Improve water storage capacity
        - Implement climate-smart farming practices:
          - Conservation tillage
          - Crop diversification
          - Improved water management
        """)
        
        # Seasonal forecast
        st.subheader("Seasonal Forecast")
        
        st.warning("""
        **Next 3 Months Outlook:**
        - Temperature: 1-2°C above normal
        - Precipitation: Near normal
        - Key concern: Potential early heat stress in spring
        
        **Recommended Preparations:**
        - Adjust planting dates for spring crops
        - Ensure irrigation systems are ready
        - Plan for heat-tolerant varieties
        """)

elif report_type == "Financial Performance":
    # Financial performance report preview
    financial_col1, financial_col2 = st.columns([2, 1])
    
    with financial_col1:
        st.subheader("Financial Performance Overview")
        
        # Create sample data for revenues and costs
        crops = ['Wheat', 'Rice', 'Cotton', 'Sugarcane']
        areas = [20, 15, 10, 5]  # acres
        yields = [3.7, 4.2, 2.5, 35.0]  # tons/acre
        prices = [40000, 60000, 90000, 5000]  # PKR/ton
        productions = [area * yield_val for area, yield_val in zip(areas, yields)]  # tons
        revenues = [prod * price for prod, price in zip(productions, prices)]  # PKR
        
        costs = [30000, 45000, 50000, 70000]  # PKR/acre
        total_costs = [area * cost for area, cost in zip(areas, costs)]  # PKR
        
        profits = [rev - cost for rev, cost in zip(revenues, total_costs)]  # PKR
        profit_margins = [profit / rev * 100 for profit, rev in zip(profits, revenues)]  # %
        roi = [profit / cost * 100 for profit, cost in zip(profits, total_costs)]  # %
        
        financial_data = {
            'Crop': crops,
            'Area (acres)': areas,
            'Yield (tons/acre)': yields,
            'Production (tons)': [round(p, 1) for p in productions],
            'Price (PKR/ton)': prices,
            'Revenue (PKR)': [int(r) for r in revenues],
            'Cost/acre (PKR)': costs,
            'Total Cost (PKR)': [int(c) for c in total_costs],
            'Profit (PKR)': [int(p) for p in profits],
            'Profit Margin (%)': [round(pm, 1) for pm in profit_margins],
            'ROI (%)': [round(r, 1) for r in roi]
        }
        
        financial_df = pd.DataFrame(financial_data)
        
        # Display financial table
        st.dataframe(financial_df, use_container_width=True, hide_index=True)
        
        # Create revenue and cost visualization
        fin_fig = go.Figure()
        
        fin_fig.add_trace(go.Bar(
            x=financial_df['Crop'],
            y=financial_df['Revenue (PKR)'],
            name='Revenue',
            marker_color='green'
        ))
        
        fin_fig.add_trace(go.Bar(
            x=financial_df['Crop'],
            y=financial_df['Total Cost (PKR)'],
            name='Cost',
            marker_color='red'
        ))
        
        fin_fig.update_layout(
            title='Revenue vs. Cost by Crop',
            barmode='group',
            yaxis_title='PKR'
        )
        
        st.plotly_chart(fin_fig, use_container_width=True)
        
        # Create profit margin visualization
        margin_fig = px.bar(
            financial_df,
            x='Crop',
            y='Profit Margin (%)',
            color='Profit Margin (%)',
            color_continuous_scale='RdYlGn',
            title='Profit Margin by Crop'
        )
        
        st.plotly_chart(margin_fig, use_container_width=True)
        
        # Cost breakdown
        st.subheader("Cost Breakdown")
        
        # Create sample data for cost categories
        cost_categories = ['Land Preparation', 'Seeds', 'Fertilizer', 'Pesticides', 'Irrigation', 'Labor', 'Harvesting', 'Others']
        wheat_costs = [3000, 5000, 8000, 3000, 4000, 3000, 2000, 2000]  # PKR/acre
        rice_costs = [4000, 6000, 10000, 4000, 8000, 5000, 4000, 4000]  # PKR/acre
        cotton_costs = [3500, 8000, 12000, 8000, 6000, 6000, 3000, 3500]  # PKR/acre
        sugarcane_costs = [5000, 15000, 15000, 5000, 10000, 10000, 5000, 5000]  # PKR/acre
        
        cost_data = {
            'Category': cost_categories,
            'Wheat (PKR/acre)': wheat_costs,
            'Rice (PKR/acre)': rice_costs,
            'Cotton (PKR/acre)': cotton_costs,
            'Sugarcane (PKR/acre)': sugarcane_costs
        }
        
        cost_df = pd.DataFrame(cost_data)
        
        # Create a stacked bar chart for cost breakdown
        cost_df_melted = pd.melt(
            cost_df,
            id_vars=['Category'],
            value_vars=['Wheat (PKR/acre)', 'Rice (PKR/acre)', 'Cotton (PKR/acre)', 'Sugarcane (PKR/acre)'],
            var_name='Crop',
            value_name='Cost (PKR/acre)'
        )
        
        cost_breakdown_fig = px.bar(
            cost_df_melted,
            x='Crop',
            y='Cost (PKR/acre)',
            color='Category',
            title='Cost Breakdown by Category and Crop'
        )
        
        st.plotly_chart(cost_breakdown_fig, use_container_width=True)
    
    with financial_col2:
        st.subheader("Financial Metrics")
        
        # Calculate overall farm metrics
        total_revenue = sum(financial_df['Revenue (PKR)'])
        total_cost = sum(financial_df['Total Cost (PKR)'])
        total_profit = sum(financial_df['Profit (PKR)'])
        overall_margin = (total_profit / total_revenue) * 100
        overall_roi = (total_profit / total_cost) * 100
        
        # Display metrics
        st.metric(
            label="Total Revenue",
            value=f"PKR {total_revenue:,}",
            help="Total farm revenue from all crops"
        )
        
        st.metric(
            label="Total Cost",
            value=f"PKR {total_cost:,}",
            help="Total farm costs for all crops"
        )
        
        st.metric(
            label="Total Profit",
            value=f"PKR {total_profit:,}",
            delta=f"{overall_margin:.1f}% margin",
            help="Total farm profit and profit margin"
        )
        
        st.metric(
            label="Return on Investment",
            value=f"{overall_roi:.1f}%",
            help="Return on investment (profit / cost)"
        )
        
        # Show a farm image
        st.image(
            get_random_image("farming_landscapes_pakistan"),
            caption="Farm revenue generators",
            use_column_width=True
        )
        
        # Profitability analysis
        st.subheader("Profitability Analysis")
        
        # Calculate per-acre metrics
        per_acre_data = {
            'Crop': crops,
            'Revenue/acre': [int(rev / area) for rev, area in zip(revenues, areas)],
            'Cost/acre': costs,
            'Profit/acre': [int(profit / area) for profit, area in zip(profits, areas)],
            'ROI (%)': [round(r, 1) for r in roi]
        }
        
        per_acre_df = pd.DataFrame(per_acre_data)
        
        st.dataframe(per_acre_df, use_container_width=True, hide_index=True)
        
        # Financial recommendations
        st.subheader("Financial Recommendations")
        
        st.info("""
        **Crop Mix Optimization:**
        - Increase rice area by 5 acres (high ROI)
        - Reduce wheat area by 5 acres (lower ROI)
        - Maintain cotton and sugarcane area
        Potential profit increase: PKR 150,000
        
        **Cost Reduction Opportunities:**
        - Optimize fertilizer application (10% savings)
        - Implement integrated pest management (15% savings)
        - Improve irrigation efficiency (20% savings)
        Potential cost reduction: PKR 320,000
        
        **Revenue Enhancement Opportunities:**
        - Improve crop quality for premium prices
        - Consider direct marketing channels
        - Explore value-added processing options
        Potential revenue increase: PKR 200,000
        """)
        
        # Market trends
        st.subheader("Market Trends")
        
        st.markdown("""
        **Wheat:** Prices expected to remain stable with 5-7% increase likely due to increased demand
        
        **Rice:** Strong export demand could push prices up 8-10% in coming months
        
        **Cotton:** International prices volatile; local prices expected to rise 5-8%
        
        **Sugarcane:** Stable outlook with 2-3% price increase expected
        """)

else:  # Custom report
    st.info("Select report elements to include in your custom report")
    
    # Custom report elements
    custom_elements = st.multiselect(
        "Report Elements",
        ["Farm Overview", "Crop Health Analysis", "Yield Forecast", "Resource Optimization", 
         "Weather Analysis", "Financial Performance", "Recommendations"],
        ["Farm Overview", "Crop Health Analysis", "Yield Forecast", "Recommendations"]
    )
    
    if "Farm Overview" in custom_elements:
        st.subheader("Farm Overview")
        
        # Create columns for information
        overview_col1, overview_col2 = st.columns([1, 2])
        
        with overview_col1:
            st.markdown("""
            **Farm Information:**
            - Name: Demo Farm
            - Location: Punjab, Pakistan
            - Total Area: 50 acres
            - Main Crops: Wheat, Rice, Cotton, Sugarcane
            - Growing Season: Rabi 2023-24
            """)
            
            # Show a random image
            st.image(
                get_random_image("farming_landscapes_pakistan"),
                caption="Farm aerial view",
                use_column_width=True
            )
        
        with overview_col2:
            # Create farm map
            mapbox_token = "YOUR_MAPBOX_TOKEN"  # This would come from environment variables in production
            farm_map = create_farm_map(mapbox_token, latitude=31.5204, longitude=74.3587, zoom=10)
            st.plotly_chart(farm_map, use_container_width=True)
    
    if "Crop Health Analysis" in custom_elements:
        st.subheader("Crop Health Analysis")
        
        # Create crop health visualization
        health_chart = create_crop_health_chart()
        st.plotly_chart(health_chart, use_container_width=True)
    
    if "Yield Forecast" in custom_elements:
        st.subheader("Yield Forecast")
        
        # Create yield visualization
        yield_chart = create_yield_chart()
        st.plotly_chart(yield_chart, use_container_width=True)
    
    if "Recommendations" in custom_elements:
        st.subheader("Recommendations")
        
        st.info("""
        **Key Recommendations:**
        
        1. **Crop Health Management:**
           - Apply fungicide in northern wheat fields to control early signs of leaf rust
           - Increase potassium application in cotton fields to improve stress tolerance
           - Implement integrated pest management for rice to reduce insecticide usage
        
        2. **Resource Optimization:**
           - Improve irrigation scheduling using soil moisture sensors (potential water savings: 20%)
           - Implement variable rate fertilizer application based on soil tests
           - Shift to solar pumping for irrigation to reduce energy costs
        
        3. **Yield Enhancement:**
           - Optimize planting density in wheat fields
           - Improve drainage in low-lying areas of rice fields
           - Consider precision agriculture technologies for future seasons
        """)

# Saved Reports Section
st.header("Saved Reports")

# Create sample data for saved reports
saved_reports = [
    {"date": "2023-10-01", "type": "Farm Overview", "period": "September 2023", "format": "PDF"},
    {"date": "2023-09-15", "type": "Crop Health", "period": "Kharif 2023", "format": "Excel"},
    {"date": "2023-09-01", "type": "Yield Analysis", "period": "August 2023", "format": "PDF"},
    {"date": "2023-08-15", "type": "Resource Utilization", "period": "Q3 2023", "format": "Web Dashboard"},
    {"date": "2023-08-01", "type": "Financial Performance", "period": "July 2023", "format": "PDF"}
]

# Convert to DataFrame
saved_reports_df = pd.DataFrame(saved_reports)

# Display saved reports
st.dataframe(saved_reports_df, use_container_width=True, hide_index=True)

# Download options for saved reports
st.download_button(
    label="Download Selected Report",
    data="This would be a PDF report in a real application",
    file_name="selected_report.pdf",
    mime="application/pdf"
)

# Report Templates section
st.header("Report Templates")

templates = [
    {"name": "Monthly Farm Overview", "description": "Complete overview of farm performance updated monthly", "frequency": "Monthly"},
    {"name": "Crop Health Status", "description": "Detailed health analysis and treatment recommendations", "frequency": "Weekly"},
    {"name": "Resource Efficiency", "description": "Analysis of resource usage and optimization opportunities", "frequency": "Monthly"},
    {"name": "Seasonal Yield Forecast", "description": "Detailed yield predictions and comparative analysis", "frequency": "Seasonal"},
    {"name": "Financial Summary", "description": "Revenue, costs, and profitability analysis", "frequency": "Quarterly"}
]

# Convert to DataFrame
templates_df = pd.DataFrame(templates)

# Display template options
st.dataframe(templates_df, use_container_width=True, hide_index=True)

# Template actions
col1, col2 = st.columns(2)

with col1:
    st.button("Use Selected Template")

with col2:
    st.button("Create New Template")

# Share and export options
st.header("Share and Export Options")

share_col1, share_col2, share_col3 = st.columns(3)

with share_col1:
    st.subheader("Email Report")
    email = st.text_input("Email Address", "farmer@example.com")
    email_format = st.selectbox("Format", ["PDF", "Excel", "Link to Dashboard"])
    st.button("Send Email")

with share_col2:
    st.subheader("Download Report")
    download_format = st.selectbox("Download Format", ["PDF", "Excel", "CSV Data", "Images Only"])
    download_quality = st.select_slider("Quality", options=["Standard", "High", "Print Quality"])
    st.download_button(
        label="Download Report",
        data="This would be the report file in a real application",
        file_name=f"custom_farm_report.{download_format.lower()}",
        mime="application/pdf"
    )

with share_col3:
    st.subheader("Print or Share")
    include_options = st.multiselect(
        "Include in Shared Report",
        ["Cover Page", "Table of Contents", "Executive Summary", "Detailed Data", "Recommendations", "Farm Maps"],
        ["Cover Page", "Executive Summary", "Recommendations"]
    )
    st.button("Print Report")
    st.button("Share via WhatsApp")

# Footer
st.markdown("---")
st.caption("© 2023 AgriPak Intelligence System | Reports last updated: October 15, 2023")
