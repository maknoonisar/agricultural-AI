import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.data_processor import load_sample_data
from utils.mapbox_utils import create_resource_map
from assets.image_urls import get_random_image

# Set page configuration
st.set_page_config(
    page_title="Resource Optimization - AgriPak Intelligence System",
    page_icon="💧",
    layout="wide",
)

# Page header
st.title("💧 Resource Optimization")
st.markdown("Optimize your farm's resources for improved efficiency and sustainability")

# Create tabs for different resource types
tab1, tab2, tab3, tab4 = st.tabs(["Water Management", "Fertilizer Optimization", "Energy Efficiency", "Labor Allocation"])

with tab1:
    st.header("Water Management")
    
    # Create layout
    water_col1, water_col2 = st.columns([2, 1])
    
    with water_col1:
        # Water usage map
        st.subheader("Water Usage Map")
        
        mapbox_token = "pk.eyJ1IjoiZW5ncmtpIiwiYSI6ImNrc29yeHB2aDBieDEydXFoY240bXExcWoifQ.WS7GVtVGZb4xgHn9dleszQ"
        water_map = create_resource_map(mapbox_token, resource_type="water", latitude=31.5204, longitude=74.3587, zoom=12)
        st.plotly_chart(water_map, use_container_width=True)
        
        st.markdown("""
        **Map Legend:**
        - 🔵 Low water usage
        - 🟢 Optimal water usage
        - 🟡 Moderate over-irrigation
        - 🔴 Severe over-irrigation
        """)
        
        # Water efficiency analysis
        st.subheader("Water Efficiency Analysis")
        
        # Create sample data for water efficiency
        fields = ['North Field', 'South Field', 'East Field', 'West Field']
        water_usage = [78, 65, 92, 71]  # mm/week
        optimal_usage = [65, 60, 70, 65]  # mm/week
        efficiency = [round((o / u) * 100) for u, o in zip(water_usage, optimal_usage)]
        
        # Create dataframe
        water_df = pd.DataFrame({
            'Field': fields,
            'Current Usage (mm/week)': water_usage,
            'Optimal Usage (mm/week)': optimal_usage,
            'Efficiency (%)': efficiency
        })
        
        # Create bar chart
        water_fig = go.Figure()
        
        water_fig.add_trace(go.Bar(
            x=water_df['Field'],
            y=water_df['Current Usage (mm/week)'],
            name='Current Usage',
            marker_color='blue'
        ))
        
        water_fig.add_trace(go.Bar(
            x=water_df['Field'],
            y=water_df['Optimal Usage (mm/week)'],
            name='Optimal Usage',
            marker_color='green'
        ))
        
        water_fig.add_trace(go.Scatter(
            x=water_df['Field'],
            y=water_df['Efficiency (%)'],
            mode='lines+markers',
            name='Efficiency (%)',
            marker=dict(size=8, color='red'),
            line=dict(width=2, dash='dot'),
            yaxis='y2'
        ))
        
        water_fig.update_layout(
            title='Water Usage by Field',
            barmode='group',
            xaxis_title='Field',
            yaxis=dict(
                title='Water Usage (mm/week)',
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
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            )
        )
        
        st.plotly_chart(water_fig, use_container_width=True)
        
        # Water savings potential
        st.subheader("Water Savings Potential")
        
        # Calculate water savings
        water_df['Excess Usage (mm/week)'] = water_df['Current Usage (mm/week)'] - water_df['Optimal Usage (mm/week)']
        water_df['Savings Potential (%)'] = (water_df['Excess Usage (mm/week)'] / water_df['Current Usage (mm/week)'] * 100).round(1)
        
        # Create horizontal bar chart
        savings_fig = px.bar(
            water_df,
            y='Field',
            x='Savings Potential (%)',
            orientation='h',
            color='Savings Potential (%)',
            color_continuous_scale=['green', 'yellow', 'orange', 'red'],
            labels={'Savings Potential (%)': 'Potential Water Savings (%)'},
            title='Water Savings Potential by Field'
        )
        
        st.plotly_chart(savings_fig, use_container_width=True)
        
        # Overall water efficiency
        total_current = water_df['Current Usage (mm/week)'].sum()
        total_optimal = water_df['Optimal Usage (mm/week)'].sum()
        overall_efficiency = round((total_optimal / total_current) * 100)
        potential_savings = round(((total_current - total_optimal) / total_current) * 100)
        
        st.info(f"""
        **Overall Water Efficiency: {overall_efficiency}%**
        
        Your farm is currently using {total_current} mm/week of water, while the optimal usage is estimated at {total_optimal} mm/week.
        This represents a potential water savings of {potential_savings}% across your entire farm.
        """)
        
    with water_col2:
        # Irrigation schedule recommendations
        st.subheader("Irrigation Recommendations")
        
        # Show a random image
        st.image(
            get_random_image("modern_agriculture_technology"),
            caption="Modern irrigation system",
            use_column_width=True
        )
        
        # Create irrigation schedule recommendations
        schedule_data = {
            'Field': fields,
            'Current Schedule': ['Daily, 2hr', 'Daily, 1.5hr', 'Daily, 2.5hr', 'Daily, 2hr'],
            'Recommended Schedule': ['Every 2 days, 3hr', 'Every 2 days, 2.5hr', 'Every 2 days, 3.5hr', 'Every 2 days, 3hr'],
            'Best Time': ['Early morning', 'Early morning', 'Late evening', 'Early morning']
        }
        
        schedule_df = pd.DataFrame(schedule_data)
        
        st.dataframe(schedule_df, use_container_width=True, hide_index=True)
        
        # Soil moisture targets
        st.subheader("Soil Moisture Targets")
        
        moisture_data = {
            'Soil Type': ['Clay Loam', 'Silt Loam', 'Sandy Loam'],
            'Field Capacity (%)': [36, 33, 23],
            'Optimal Range (%)': ['28-34', '26-31', '18-22'],
            'Wilting Point (%)': [17, 13, 10]
        }
        
        moisture_df = pd.DataFrame(moisture_data)
        
        st.dataframe(moisture_df, use_container_width=True, hide_index=True)
        
        # Weather considerations
        st.subheader("Weather Considerations")
        
        st.markdown("""
        **Upcoming Weather Impact:**
        
        - **Next 3 Days:** No significant rainfall expected
        - **Day 4-7:** Moderate rainfall expected (15-20mm)
        
        **Recommendation:** 
        Maintain current irrigation schedule for next 3 days, then reduce irrigation by 50% on days 4-7 to account for rainfall.
        """)
        
        # Water conservation tips
        st.subheader("Water Conservation Tips")
        
        st.markdown("""
        **1. Improve Irrigation System**
        - Install drip irrigation for 20% water savings
        - Maintain and repair leaks (5-10% savings)
        - Install soil moisture sensors (15% savings)
        
        **2. Cultural Practices**
        - Apply mulch to reduce evaporation
        - Practice deficit irrigation during non-critical growth stages
        - Implement crop rotation with water-efficient crops
        
        **3. Timing Optimization**
        - Irrigate during early morning or evening
        - Adjust irrigation based on weather forecasts
        - Implement precision irrigation scheduling
        """)
        
        # Economic impact
        st.subheader("Economic Impact")
        
        # Calculate economic metrics
        water_cost = 5000  # PKR per acre-inch
        total_acres = 50
        current_water_cost = water_cost * (total_current / 25.4) * total_acres / 12  # Convert mm to inches
        optimal_water_cost = water_cost * (total_optimal / 25.4) * total_acres / 12
        savings = current_water_cost - optimal_water_cost
        
        st.metric(
            label="Current Weekly Water Cost",
            value=f"PKR {int(current_water_cost):,}",
            help="Total cost of water usage across all fields"
        )
        
        st.metric(
            label="Potential Weekly Savings",
            value=f"PKR {int(savings):,}",
            delta=f"{potential_savings}%",
            help="Potential cost savings from optimized water usage"
        )
        
        st.metric(
            label="Annual Savings Potential",
            value=f"PKR {int(savings * 52):,}",
            help="Projected annual savings from improved water efficiency"
        )

with tab2:
    st.header("Fertilizer Optimization")
    
    # Create layout
    fert_col1, fert_col2 = st.columns([2, 1])
    
    with fert_col1:
        # Nutrient levels map
        st.subheader("Soil Nutrient Map")
        
        mapbox_token = "pk.eyJ1IjoiZW5ncmtpIiwiYSI6ImNrc29yeHB2aDBieDEydXFoY240bXExcWoifQ.WS7GVtVGZb4xgHn9dleszQ"
        nutrient_map = create_resource_map(mapbox_token, resource_type="nutrients", latitude=31.5204, longitude=74.3587, zoom=12)
        st.plotly_chart(nutrient_map, use_container_width=True)
        
        st.markdown("""
        **Map Legend:**
        - 🔵 Low nutrient levels
        - 🟢 Optimal nutrient levels
        - 🟡 Moderate over-fertilization
        - 🔴 Severe over-fertilization
        """)
        
        # Nutrient analysis
        st.subheader("Soil Nutrient Analysis")
        
        # Create sample data for nutrient levels
        fields = ['North Field', 'South Field', 'East Field', 'West Field']
        
        # Create dataframe for NPK levels
        nutrient_data = {
            'Field': fields,
            'Nitrogen (kg/ha)': [120, 90, 150, 110],
            'Phosphorus (kg/ha)': [35, 28, 42, 30],
            'Potassium (kg/ha)': [80, 65, 95, 75],
            'pH': [6.8, 7.2, 6.5, 7.0]
        }
        
        # Optimal ranges
        optimal_ranges = {
            'Nitrogen (kg/ha)': [100, 140],
            'Phosphorus (kg/ha)': [25, 35],
            'Potassium (kg/ha)': [70, 90],
            'pH': [6.5, 7.5]
        }
        
        nutrient_df = pd.DataFrame(nutrient_data)
        
        # Create radar chart for nutrient levels
        nutrients = ['Nitrogen (kg/ha)', 'Phosphorus (kg/ha)', 'Potassium (kg/ha)']
        
        fig = go.Figure()
        
        for field in fields:
            field_data = nutrient_df[nutrient_df['Field'] == field]
            
            # Normalize values for radar chart
            normalized_values = [
                field_data[nutrient].values[0] / optimal_ranges[nutrient][1]
                for nutrient in nutrients
            ]
            
            fig.add_trace(go.Scatterpolar(
                r=normalized_values + [normalized_values[0]],
                theta=nutrients + [nutrients[0]],
                fill='toself',
                name=field
            ))
        
        # Add optimal range
        fig.add_trace(go.Scatterpolar(
            r=[1, 1, 1, 1],
            theta=nutrients + [nutrients[0]],
            fill='toself',
            name='Optimal Range',
            line=dict(color='rgba(0, 255, 0, 0.5)'),
            fillcolor='rgba(0, 255, 0, 0.1)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1.5]
                )
            ),
            title='Nutrient Levels Relative to Optimal (1.0 = Optimal)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display nutrient data table
        st.dataframe(nutrient_df, use_container_width=True, hide_index=True)
        
        # Fertilizer application recommendations
        st.subheader("Fertilizer Application Recommendations")
        
        # Create sample recommendations
        recommendation_data = {
            'Field': fields,
            'Nitrogen (kg/ha)': ['+0', '+20', '-20', '+0'],
            'Phosphorus (kg/ha)': ['+0', '+5', '-10', '+5'],
            'Potassium (kg/ha)': ['+0', '+10', '-15', '+0'],
            'Lime/Acidifier': ['None', 'None', 'Lime (500 kg/ha)', 'None']
        }
        
        recommendation_df = pd.DataFrame(recommendation_data)
        
        # Add styling to the table
        def highlight_recommendations(s):
            styles = []
            for value in s:
                if isinstance(value, str):
                    if value.startswith('+'):
                        styles.append('background-color: #d4f1c5; color: #145214')
                    elif value.startswith('-'):
                        styles.append('background-color: #f8d7da; color: #721c24')
                    else:
                        styles.append('')
                else:
                    styles.append('')
            return styles
        
        st.dataframe(
            recommendation_df.style.apply(highlight_recommendations),
            use_container_width=True,
            hide_index=True
        )
        
    with fert_col2:
        # Economic analysis of fertilizer usage
        st.subheader("Economic Analysis")
        
        # Show a random image
        st.image(
            get_random_image("modern_agriculture_technology"),
            caption="Precision fertilizer application",
            use_column_width=True
        )
        
        # Create economic metrics for fertilizers
        fertilizer_costs = {
            'Type': ['Urea (N)', 'DAP (P)', 'Potash (K)', 'Micronutrients'],
            'Current Usage (kg/ha)': [250, 125, 100, 20],
            'Recommended (kg/ha)': [220, 130, 110, 25],
            'Price (PKR/kg)': [110, 150, 130, 300],
            'Current Cost (PKR/ha)': [27500, 18750, 13000, 6000],
            'Recommended Cost (PKR/ha)': [24200, 19500, 14300, 7500]
        }
        
        fertilizer_df = pd.DataFrame(fertilizer_costs)
        
        # Calculate savings and totals
        fertilizer_df['Savings (PKR/ha)'] = fertilizer_df['Current Cost (PKR/ha)'] - fertilizer_df['Recommended Cost (PKR/ha)']
        
        current_total = fertilizer_df['Current Cost (PKR/ha)'].sum()
        recommended_total = fertilizer_df['Recommended Cost (PKR/ha)'].sum()
        total_savings = current_total - recommended_total
        
        # Display economic metrics
        st.metric(
            label="Current Fertilizer Cost",
            value=f"PKR {int(current_total):,}/ha",
            help="Total cost of current fertilizer usage per hectare"
        )
        
        st.metric(
            label="Recommended Cost",
            value=f"PKR {int(recommended_total):,}/ha",
            delta=f"{'-' if total_savings > 0 else '+'}{abs(int(total_savings)):,}",
            delta_color="normal" if total_savings > 0 else "inverse",
            help="Total cost of recommended fertilizer usage per hectare"
        )
        
        farm_size = 20  # ha
        annual_savings = total_savings * farm_size
        
        st.metric(
            label="Annual Farm Savings",
            value=f"PKR {int(annual_savings):,}",
            help="Projected annual savings for entire farm"
        )
        
        # Fertilizer efficiency tips
        st.subheader("Fertilizer Efficiency Tips")
        
        st.markdown("""
        **1. Timing and Placement**
        - Apply nitrogen in split applications
        - Use banding for phosphorus
        - Apply potassium before peak growth stages
        
        **2. Precision Application**
        - Use variable rate technology
        - Apply based on soil test results
        - Adjust rates based on yield goals
        
        **3. Enhanced Efficiency Products**
        - Slow-release nitrogen fertilizers
        - Nitrification inhibitors
        - Urease inhibitors
        
        **4. Environmental Considerations**
        - Avoid application before heavy rain
        - Implement buffer zones near water bodies
        - Use cover crops to capture residual nutrients
        """)
        
        # Future recommendations
        st.subheader("Long-term Soil Health")
        
        st.markdown("""
        **Soil Improvement Plan:**
        
        - **Year 1:** Conduct detailed soil testing and establish baseline
        - **Year 2:** Address major nutrient deficiencies and pH issues
        - **Year 3:** Implement crop rotation and cover cropping
        - **Year 4:** Transition to precision farming and variable rate application
        - **Year 5:** Integrate organic nutrient sources with mineral fertilizers
        
        **Expected Benefits:**
        - 15-20% increase in nutrient use efficiency
        - 10-15% reduction in fertilizer costs
        - 5-10% yield improvement from better soil health
        """)

with tab3:
    st.header("Energy Efficiency")
    
    # Create layout
    energy_col1, energy_col2 = st.columns([2, 1])
    
    with energy_col1:
        # Energy usage breakdown
        st.subheader("Energy Usage Breakdown")
        
        # Create sample data for energy usage
        energy_data = {
            'Category': ['Irrigation', 'Machinery', 'Processing', 'Storage', 'Other'],
            'Diesel (L)': [450, 680, 120, 50, 80],
            'Electricity (kWh)': [3200, 1500, 2800, 1200, 800],
            'Cost (PKR)': [213500, 187600, 92400, 36000, 27000]
        }
        
        energy_df = pd.DataFrame(energy_data)
        
        # Create energy usage pie chart
        fig = px.pie(
            energy_df,
            values='Cost (PKR)',
            names='Category',
            title='Energy Cost Distribution',
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Create energy usage bar chart
        energy_types = pd.DataFrame({
            'Category': energy_df['Category'].repeat(2),
            'Type': ['Diesel'] * len(energy_df) + ['Electricity'] * len(energy_df),
            'Value': list(energy_df['Diesel (L)']) + list(energy_df['Electricity (kWh)']),
            'Unit': ['Liters'] * len(energy_df) + ['kWh'] * len(energy_df)
        })
        
        type_fig = px.bar(
            energy_types,
            x='Category',
            y='Value',
            color='Type',
            barmode='group',
            labels={'Value': 'Consumption', 'Category': ''},
            title='Energy Consumption by Type'
        )
        
        st.plotly_chart(type_fig, use_container_width=True)
        
        # Energy efficiency analysis
        st.subheader("Energy Efficiency Analysis")
        
        # Create sample data for efficiency analysis
        efficiency_data = {
            'Category': energy_data['Category'],
            'Current Efficiency': [72, 65, 80, 85, 75],
            'Potential Efficiency': [85, 80, 90, 92, 85],
            'Savings Potential (%)': [18, 23, 11, 8, 13]
        }
        
        efficiency_df = pd.DataFrame(efficiency_data)
        
        # Create efficiency comparison chart
        eff_fig = go.Figure()
        
        eff_fig.add_trace(go.Bar(
            x=efficiency_df['Category'],
            y=efficiency_df['Current Efficiency'],
            name='Current Efficiency (%)',
            marker_color='blue'
        ))
        
        eff_fig.add_trace(go.Bar(
            x=efficiency_df['Category'],
            y=efficiency_df['Potential Efficiency'],
            name='Potential Efficiency (%)',
            marker_color='green'
        ))
        
        eff_fig.update_layout(
            barmode='group',
            title='Current vs. Potential Energy Efficiency',
            yaxis=dict(
                title='Efficiency (%)',
                range=[0, 100]
            )
        )
        
        st.plotly_chart(eff_fig, use_container_width=True)
        
        # Display data table
        st.dataframe(efficiency_df, use_container_width=True, hide_index=True)
        
    with energy_col2:
        # Energy saving recommendations
        st.subheader("Energy Saving Recommendations")
        
        # Show a random image
        st.image(
            get_random_image("modern_agriculture_technology"),
            caption="Solar-powered irrigation system",
            use_column_width=True
        )
        
        # Create recommendations for each category
        st.markdown("### Irrigation")
        st.markdown("""
        - Convert diesel pumps to solar (60% savings)
        - Install variable frequency drives (20% savings)
        - Optimize pump sizing and maintenance (15% savings)
        - Implement scheduled irrigation (10% savings)
        """)
        
        st.markdown("### Machinery")
        st.markdown("""
        - Regular maintenance and tuning (15% savings)
        - Reduce idle time (10% savings)
        - Optimize field operations (20% savings)
        - Consider equipment sharing or leasing (variable)
        """)
        
        st.markdown("### Processing & Storage")
        st.markdown("""
        - Upgrade to energy-efficient motors (25% savings)
        - Improve insulation in storage facilities (30% savings)
        - Optimize processing schedules (15% savings)
        - Install energy management systems (20% savings)
        """)
        
        # Alternative energy options
        st.subheader("Alternative Energy Options")
        
        alternative_data = {
            'Energy Source': ['Solar PV', 'Biogas', 'Wind', 'Micro-hydro'],
            'Viability': ['High', 'Medium', 'Low', 'Site-dependent'],
            'Initial Cost': ['High', 'Medium', 'Very High', 'High'],
            'ROI Period': ['5-7 years', '3-5 years', '8-10 years', '4-6 years']
        }
        
        alternative_df = pd.DataFrame(alternative_data)
        
        st.dataframe(alternative_df, use_container_width=True, hide_index=True)
        
        # Economic impact
        st.subheader("Economic Impact")
        
        total_energy_cost = energy_df['Cost (PKR)'].sum()
        avg_savings_potential = efficiency_df['Savings Potential (%)'].mean()
        potential_savings = total_energy_cost * (avg_savings_potential / 100)
        
        st.metric(
            label="Current Annual Energy Cost",
            value=f"PKR {int(total_energy_cost):,}",
            help="Total annual energy costs for the farm"
        )
        
        st.metric(
            label="Potential Annual Savings",
            value=f"PKR {int(potential_savings):,}",
            delta=f"{avg_savings_potential:.1f}%",
            help="Potential annual savings from improved energy efficiency"
        )
        
        payback_period = 300000 / potential_savings  # Example initial investment
        
        st.metric(
            label="Average Payback Period",
            value=f"{payback_period:.1f} years",
            help="Average time to recover investment in energy efficiency improvements"
        )

with tab4:
    st.header("Labor Allocation")
    
    # Create layout
    labor_col1, labor_col2 = st.columns([2, 1])
    
    with labor_col1:
        # Labor allocation analysis
        st.subheader("Labor Allocation Analysis")
        
        # Create sample data for labor allocation
        labor_data = {
            'Activity': ['Land Preparation', 'Planting', 'Fertilizer Application', 'Pest Control', 'Irrigation', 'Harvesting', 'Post-Harvest'],
            'Hours': [120, 180, 90, 110, 160, 240, 150],
            'Cost (PKR)': [36000, 54000, 27000, 33000, 48000, 72000, 45000],
            'Efficiency Rating': [75, 70, 80, 65, 85, 60, 75]
        }
        
        labor_df = pd.DataFrame(labor_data)
        
        # Create labor allocation bar chart
        labor_fig = px.bar(
            labor_df,
            x='Activity',
            y='Hours',
            color='Efficiency Rating',
            labels={'Hours': 'Labor Hours', 'Activity': ''},
            title='Labor Hours by Activity',
            color_continuous_scale='RdYlGn'
        )
        
        st.plotly_chart(labor_fig, use_container_width=True)
        
        # Create labor cost pie chart
        cost_fig = px.pie(
            labor_df,
            values='Cost (PKR)',
            names='Activity',
            title='Labor Cost Distribution',
            color_discrete_sequence=px.colors.sequential.Plasma
        )
        
        st.plotly_chart(cost_fig, use_container_width=True)
        
        # Labor efficiency analysis
        st.subheader("Labor Efficiency Analysis")
        
        # Calculate additional metrics
        labor_df['Hours/Acre'] = (labor_df['Hours'] / 50).round(1)  # Assuming 50 acre farm
        labor_df['Cost/Acre (PKR)'] = (labor_df['Cost (PKR)'] / 50).round()
        labor_df['Optimal Hours/Acre'] = [1.8, 2.5, 1.2, 1.5, 2.0, 3.5, 2.2]
        labor_df['Potential Savings (Hours/Acre)'] = (labor_df['Hours/Acre'] - labor_df['Optimal Hours/Acre']).round(1)
        labor_df['Savings Potential (%)'] = ((labor_df['Potential Savings (Hours/Acre)'] / labor_df['Hours/Acre']) * 100).round()
        
        # Create efficiency comparison chart
        eff_fig = go.Figure()
        
        eff_fig.add_trace(go.Bar(
            x=labor_df['Activity'],
            y=labor_df['Hours/Acre'],
            name='Current Hours/Acre',
            marker_color='blue'
        ))
        
        eff_fig.add_trace(go.Bar(
            x=labor_df['Activity'],
            y=labor_df['Optimal Hours/Acre'],
            name='Optimal Hours/Acre',
            marker_color='green'
        ))
        
        eff_fig.update_layout(
            barmode='group',
            title='Current vs. Optimal Labor Hours per Acre',
            yaxis_title='Hours per Acre'
        )
        
        st.plotly_chart(eff_fig, use_container_width=True)
        
        # Display optimization potential
        opt_fig = px.bar(
            labor_df,
            x='Activity',
            y='Savings Potential (%)',
            color='Savings Potential (%)',
            labels={'Savings Potential (%)': 'Potential Savings (%)', 'Activity': ''},
            title='Labor Optimization Potential by Activity',
            color_continuous_scale='Blues'
        )
        
        st.plotly_chart(opt_fig, use_container_width=True)
        
    with labor_col2:
        # Labor optimization recommendations
        st.subheader("Labor Optimization Recommendations")
        
        # Show a random image
        st.image(
            get_random_image("modern_agriculture_technology"),
            caption="Mechanized farm operations",
            use_column_width=True
        )
        
        # Create recommendations for each activity
        recommendations = {
            'Land Preparation': [
                'Use GPS-guided equipment',
                'Implement minimum tillage',
                'Optimize field layout',
                'Potential Savings: 25%'
            ],
            'Planting': [
                'Use precision planters',
                'Optimize seed placement',
                'Implement variable rate seeding',
                'Potential Savings: 30%'
            ],
            'Harvesting': [
                'Use semi-automated equipment',
                'Optimize harvesting timing',
                'Implement batch processing',
                'Potential Savings: 35%'
            ],
            'Irrigation': [
                'Install automated systems',
                'Use soil moisture sensors',
                'Implement scheduled irrigation',
                'Potential Savings: 20%'
            ]
        }
        
        # Display recommendations in expandable sections
        for activity, tips in recommendations.items():
            with st.expander(f"{activity} Optimization"):
                for tip in tips:
                    if "Potential Savings" in tip:
                        st.info(tip)
                    else:
                        st.markdown(f"• {tip}")
        
        # Economic impact of labor optimization
        st.subheader("Economic Impact")
        
        total_labor_cost = labor_df['Cost (PKR)'].sum()
        avg_savings_potential = labor_df['Savings Potential (%)'].mean()
        potential_savings = total_labor_cost * (avg_savings_potential / 100)
        
        st.metric(
            label="Current Annual Labor Cost",
            value=f"PKR {int(total_labor_cost):,}",
            help="Total annual labor costs for the farm"
        )
        
        st.metric(
            label="Potential Annual Savings",
            value=f"PKR {int(potential_savings):,}",
            delta=f"{avg_savings_potential:.1f}%",
            help="Potential annual savings from improved labor efficiency"
        )
        
        # Labor productivity analysis
        st.subheader("Productivity Analysis")
        
        productivity_data = {
            'Metric': ['Current Output/Labor Hour', 'Benchmark Output/Labor Hour', 'Gap (%)'],
            'Value': ['15 kg', '22 kg', '32%']
        }
        
        productivity_df = pd.DataFrame(productivity_data)
        
        st.dataframe(productivity_df, use_container_width=True, hide_index=True)
        
        # Long-term strategies
        st.subheader("Long-term Strategies")
        
        st.markdown("""
        **1. Mechanization**
        - Implement appropriate machinery for farm size
        - Consider equipment sharing for specialized equipment
        - Focus on high-labor activities first
        
        **2. Training & Skill Development**
        - Train workers on efficient techniques
        - Develop specialized skill teams
        - Implement performance metrics
        
        **3. Process Optimization**
        - Redesign workflows for efficiency
        - Reduce movement and transport
        - Implement standard operating procedures
        
        **4. Technology Integration**
        - Mobile apps for task management
        - GPS and GIS for field operations
        - Remote monitoring systems
        """)

# Summary dashboard for all resources
st.header("Resource Optimization Summary")

# Create a summary dashboard
summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)

with summary_col1:
    st.subheader("Water")
    st.metric(
        label="Current Efficiency",
        value="72%",
        delta="+28% potential",
        help="Current water usage efficiency with improvement potential"
    )
    
    st.metric(
        label="Annual Savings Potential",
        value="PKR 520,000",
        help="Potential annual cost savings from water optimization"
    )

with summary_col2:
    st.subheader("Fertilizer")
    st.metric(
        label="Current Efficiency",
        value="78%",
        delta="+22% potential",
        help="Current fertilizer usage efficiency with improvement potential"
    )
    
    st.metric(
        label="Annual Savings Potential",
        value="PKR 380,000",
        help="Potential annual cost savings from fertilizer optimization"
    )

with summary_col3:
    st.subheader("Energy")
    st.metric(
        label="Current Efficiency",
        value="70%",
        delta="+30% potential",
        help="Current energy usage efficiency with improvement potential"
    )
    
    st.metric(
        label="Annual Savings Potential",
        value="PKR 450,000",
        help="Potential annual cost savings from energy optimization"
    )

with summary_col4:
    st.subheader("Labor")
    st.metric(
        label="Current Efficiency",
        value="68%",
        delta="+32% potential",
        help="Current labor efficiency with improvement potential"
    )
    
    st.metric(
        label="Annual Savings Potential",
        value="PKR 650,000",
        help="Potential annual cost savings from labor optimization"
    )

# Total potential savings
total_savings = 520000 + 380000 + 450000 + 650000
st.info(f"**Total Annual Savings Potential: PKR {total_savings:,}** through optimization of all farm resources")

# Priority recommendations section
st.subheader("Priority Recommendations")

priority_col1, priority_col2, priority_col3 = st.columns(3)

with priority_col1:
    st.markdown("### Immediate Actions (0-3 months)")
    st.markdown("""
    1. **Irrigation Scheduling Optimization**
       - Implement soil moisture-based irrigation
       - Reduced water usage: 15-20%
       - Investment: Low
    
    2. **Fertilizer Application Timing**
       - Shift to split applications
       - Improved efficiency: 10-15%
       - Investment: None
       
    3. **Equipment Maintenance**
       - Tune-up all machinery and pumps
       - Energy savings: 10-15%
       - Investment: Low
    """)

with priority_col2:
    st.markdown("### Short-term Actions (3-12 months)")
    st.markdown("""
    1. **Drip Irrigation Installation**
       - Install in high-value crop areas
       - Water savings: 30-40%
       - Investment: Moderate
    
    2. **Variable Rate Technology**
       - Implement for fertilizer application
       - Input savings: 15-25%
       - Investment: Moderate
       
    3. **Labor Process Redesign**
       - Optimize harvesting workflows
       - Labor savings: 20-30%
       - Investment: Low
    """)

with priority_col3:
    st.markdown("### Long-term Actions (1-3 years)")
    st.markdown("""
    1. **Solar Irrigation System**
       - Convert diesel pumps to solar
       - Energy savings: 60-80%
       - Investment: High
    
    2. **Precision Agriculture Suite**
       - Integrate sensors, GPS, and analytics
       - Overall efficiency gain: 25-35%
       - Investment: High
       
    3. **Mechanization Upgrade**
       - Phase in appropriate machinery
       - Labor savings: 30-50%
       - Investment: High
    """)

# Implementation plan
st.subheader("Implementation Timeline")

# Create sample data for implementation timeline
timeline_data = [
    dict(Task="Irrigation Scheduling", Start='2023-11-01', Finish='2023-12-15', Resource="Water"),
    dict(Task="Equipment Maintenance", Start='2023-11-15', Finish='2023-12-31', Resource="Energy"),
    dict(Task="Fertilizer Split Application", Start='2023-12-01', Finish='2024-02-28', Resource="Fertilizer"),
    dict(Task="Labor Process Redesign", Start='2024-01-15', Finish='2024-03-31', Resource="Labor"),
    dict(Task="Drip Irrigation Installation", Start='2024-03-01', Finish='2024-05-15', Resource="Water"),
    dict(Task="Variable Rate Technology", Start='2024-04-01', Finish='2024-07-31', Resource="Fertilizer"),
    dict(Task="Solar Irrigation System", Start='2024-06-01', Finish='2024-09-30', Resource="Energy"),
    dict(Task="Precision Agriculture Suite", Start='2024-08-01', Finish='2024-12-31', Resource="Multiple"),
    dict(Task="Mechanization Upgrade", Start='2024-10-01', Finish='2025-03-31', Resource="Labor")
]

colors = {'Water': 'rgb(46, 134, 193)', 
          'Energy': 'rgb(243, 156, 18)', 
          'Fertilizer': 'rgb(39, 174, 96)', 
          'Labor': 'rgb(142, 68, 173)',
          'Multiple': 'rgb(127, 127, 127)'}

fig = px.timeline(
    timeline_data, 
    x_start="Start", 
    x_end="Finish", 
    y="Task",
    color="Resource",
    color_discrete_map=colors
)

fig.update_layout(
    title="Resource Optimization Implementation Timeline",
    xaxis_title="Date",
    yaxis_title="",
    height=400
)

st.plotly_chart(fig, use_container_width=True)

# Download implementation plan
st.download_button(
    label="Download Implementation Plan",
    data="This would be a PDF implementation plan in a real application",
    file_name="resource_optimization_plan.pdf",
    mime="application/pdf"
)
