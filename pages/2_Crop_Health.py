import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from utils.data_processor import load_sample_data
from utils.mapbox_utils import create_crop_health_map
from utils.crop_analysis import analyze_crop_image
from utils.notification import send_alert
from assets.image_urls import get_random_image, get_crop_disease_images

# Set page configuration
st.set_page_config(
    page_title="Crop Health - AgriPak Intelligence System",
    page_icon="🌱",
    layout="wide",
)

# Page header
st.title("🌱 Crop Health Analysis")
st.markdown("Monitor crop health, detect diseases, and receive treatment recommendations")

# Create tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["Health Dashboard", "Disease Detection", "Treatment Recommendations"])

with tab1:
    st.header("Crop Health Dashboard")
    
    # Filter controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_crop = st.selectbox(
            "Select Crop",
            ["All Crops", "Wheat", "Rice", "Cotton", "Sugarcane", "Maize"]
        )
    
    with col2:
        selected_field = st.selectbox(
            "Select Field",
            ["All Fields", "North Field", "South Field", "East Field", "West Field"]
        )
    
    with col3:
        selected_date = st.date_input(
            "Select Date",
            datetime.now()
        )
    
    # Create health map visualization
    st.subheader("Crop Health Map")
    
    mapbox_token = "pk.eyJ1IjoiZW5ncmtpIiwiYSI6ImNrc29yeHB2aDBieDEydXFoY240bXExcWoifQ.WS7GVtVGZb4xgHn9dleszQ"
    health_map = create_crop_health_map(mapbox_token, latitude=31.5204, longitude=74.3587, zoom=12)
    st.plotly_chart(health_map, use_container_width=True)
    
    st.markdown("""
    **Map Legend:**
    - 🟢 Excellent health (NDVI > 0.8)
    - 🟡 Good health (NDVI 0.6-0.8)
    - 🟠 Moderate health (NDVI 0.4-0.6)
    - 🔴 Poor health (NDVI < 0.4)
    """)
    
    # Health metrics by field
    st.subheader("Health Metrics by Field")
    
    # Sample data for health metrics
    field_metrics = {
        'Field': ['North Field', 'South Field', 'East Field', 'West Field'],
        'NDVI': [0.82, 0.71, 0.56, 0.78],
        'Moisture': [78, 65, 59, 72],
        'Stress Index': [12, 24, 38, 18],
        'Disease Risk': ['Low', 'Low', 'Medium', 'Low']
    }
    
    field_df = pd.DataFrame(field_metrics)
    
    # Create a bar chart for NDVI values
    ndvi_fig = px.bar(
        field_df,
        x='Field',
        y='NDVI',
        color='NDVI',
        color_continuous_scale=['red', 'yellow', 'green'],
        labels={'NDVI': 'Vegetation Index'},
        title='NDVI by Field'
    )
    
    st.plotly_chart(ndvi_fig, use_container_width=True)
    
    # Display health metrics table
    st.dataframe(field_df, use_container_width=True, hide_index=True)
    
    # Time series of health metrics
    st.subheader("Health Trends (Last 30 Days)")
    
    # Create sample time series data
    dates = pd.date_range(end=datetime.now(), periods=30).tolist()
    ndvi_values = [0.7 + np.random.normal(0, 0.05) for _ in range(30)]
    moisture_values = [70 + np.random.normal(0, 5) for _ in range(30)]
    
    # Create time series chart
    time_series_df = pd.DataFrame({
        'Date': dates,
        'NDVI': ndvi_values,
        'Moisture': moisture_values
    })
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=time_series_df['Date'],
        y=time_series_df['NDVI'],
        name='NDVI',
        line=dict(color='green', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=time_series_df['Date'],
        y=[v/100 for v in time_series_df['Moisture']],
        name='Soil Moisture',
        line=dict(color='blue', width=2),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title='Crop Health Indicators Over Time',
        xaxis_title='Date',
        yaxis=dict(
            title='NDVI',
            range=[0, 1]
        ),
        yaxis2=dict(
            title='Soil Moisture',
            title_font=dict(color='blue'),
            tickfont=dict(color='blue'),
            anchor='x',
            overlaying='y',
            side='right',
            range=[0, 1]
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Disease Detection")
    
    # Create columns for upload and example options
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Upload Crop Images")
        uploaded_file = st.file_uploader("Upload a photo of your crop for analysis", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            # Display the uploaded image
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            
            # Add an analyze button
            if st.button("Analyze Image"):
                with st.spinner("Analyzing crop image..."):
                    # In a real app, this would call an actual ML model
                    analysis_result = analyze_crop_image(uploaded_file)
                    
                    # Display results
                    st.subheader("Analysis Results")
                    
                    if analysis_result.get("success", False):
                        if analysis_result.get("disease_detected", False):
                            st.error(f"**Disease Detected:** {analysis_result['disease_name']}")
                            st.markdown(f"**Confidence:** {analysis_result['confidence']}%")
                            st.markdown(f"**Description:** {analysis_result['description']}")
                            
                            # Add notification options
                            st.markdown("---")
                            st.subheader("Send Alert")
                            
                            col_a, col_b = st.columns(2)
                            with col_a:
                                send_email_alert = st.checkbox("Send Email Alert", value=True)
                                recipient_email = st.text_input("Recipient Email", value="", 
                                                               placeholder="farmer@example.com", 
                                                               disabled=not send_email_alert)
                            
                            with col_b:
                                send_sms_alert = st.checkbox("Send SMS Alert", value=True)
                                recipient_phone = st.text_input("Recipient Phone", value="", 
                                                              placeholder="+923001234567", 
                                                              disabled=not send_sms_alert)
                            
                            if st.button("Send Alerts"):
                                if not send_email_alert and not send_sms_alert:
                                    st.warning("Please select at least one alert method")
                                else:
                                    # Prepare alert data
                                    alert_data = {
                                        "issue_type": analysis_result['disease_name'],
                                        "severity": "High" if analysis_result['confidence'] > 80 else "Medium",
                                        "description": analysis_result['description'],
                                        "affected_area": "Detected area",
                                        "field": selected_field if selected_field != "All Fields" else "North Field",
                                        "action": "Apply recommended treatment immediately"
                                    }
                                    
                                    # Prepare recipient info
                                    recipient_info = {}
                                    if send_email_alert and recipient_email:
                                        recipient_info["email"] = recipient_email
                                    if send_sms_alert and recipient_phone:
                                        recipient_info["phone"] = recipient_phone
                                    
                                    if recipient_info:
                                        # Send the alert
                                        with st.spinner("Sending alerts..."):
                                            result = send_alert("crop_health", alert_data, recipient_info)
                                            
                                            # Show results
                                            if result["email"] and result["email"]["success"]:
                                                st.success("Email alert sent successfully!")
                                            elif result["email"]:
                                                st.error(f"Email alert failed: {result['email']['message']}")
                                                
                                            if result["sms"] and result["sms"]["success"]:
                                                st.success("SMS alert sent successfully!")
                                            elif result["sms"]:
                                                st.error(f"SMS alert failed: {result['sms']['message']}")
                                    else:
                                        st.warning("Please provide at least one recipient")
                        else:
                            st.success("No disease detected. Your crop appears healthy.")
                    else:
                        st.error(f"Analysis failed: {analysis_result.get('error', 'Unknown error')}")
        
        st.markdown("---")
        
        st.subheader("Bulk Analysis")
        st.markdown("Upload multiple images for batch processing")
        
        uploaded_files = st.file_uploader("Upload multiple crop images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
        
        if uploaded_files:
            st.write(f"{len(uploaded_files)} images uploaded")
            if st.button("Analyze All Images"):
                st.info("Bulk analysis functionality would process all images here in a production system")
    
    with col2:
        st.subheader("Common Crop Diseases")
        st.markdown("Examples of common crop diseases in Pakistan")
        
        # Display example crop disease images with descriptions
        disease_images = get_crop_disease_images()
        
        for i, (disease, image_url) in enumerate(disease_images.items()):
            with st.expander(f"{disease}"):
                st.image(image_url, caption=disease, use_column_width=True)
                
                # Simplified disease descriptions
                descriptions = {
                    "Wheat Leaf Rust": "Orange-brown pustules on leaves. Reduce photosynthesis and yield. Control with fungicides and resistant varieties.",
                    "Rice Blast": "Diamond-shaped lesions on leaves. Can kill plants at seedling stage. Manage with fungicides and resistant varieties.",
                    "Cotton Leaf Curl Virus": "Upward curling of leaves with thickened veins. Spread by whiteflies. Use resistant varieties and control insect vectors.",
                    "Sugarcane Red Rot": "Red discoloration inside stalks. Causes withering and death. Use disease-free seed cane and resistant varieties.",
                    "Potato Late Blight": "Dark water-soaked spots on leaves that quickly enlarge. Manage with fungicides and proper field ventilation.",
                    "Tomato Yellow Leaf Curl Virus": "Yellowing and curling of leaves, stunted growth. Transmitted by whiteflies. Use resistant varieties."
                }
                
                if disease in descriptions:
                    st.markdown(descriptions[disease])
                else:
                    st.markdown("Detailed description not available.")

with tab3:
    st.header("Treatment Recommendations")
    
    # Create a selector for crop and disease
    col1, col2 = st.columns(2)
    
    with col1:
        treatment_crop = st.selectbox(
            "Select Crop",
            ["Wheat", "Rice", "Cotton", "Sugarcane", "Maize", "Potato", "Tomato"],
            key="treatment_crop"
        )
    
    with col2:
        # Disease options based on selected crop
        disease_options = {
            "Wheat": ["Leaf Rust", "Stem Rust", "Powdery Mildew", "Septoria Leaf Blotch"],
            "Rice": ["Blast", "Bacterial Leaf Blight", "Sheath Blight", "Brown Spot"],
            "Cotton": ["Leaf Curl Virus", "Anthracnose", "Alternaria Leaf Spot", "Bacterial Blight"],
            "Sugarcane": ["Red Rot", "Smut", "Wilt", "Yellow Leaf Disease"],
            "Maize": ["Leaf Blight", "Stalk Rot", "Ear Rot", "Rust"],
            "Potato": ["Late Blight", "Early Blight", "Black Scurf", "Bacterial Wilt"],
            "Tomato": ["Yellow Leaf Curl Virus", "Early Blight", "Fusarium Wilt", "Bacterial Spot"]
        }
        
        treatment_disease = st.selectbox(
            "Select Disease",
            disease_options.get(treatment_crop, ["No diseases available"]),
            key="treatment_disease"
        )
    
    # Display treatment recommendations based on selection
    if treatment_crop and treatment_disease:
        st.subheader(f"Treatment for {treatment_disease} in {treatment_crop}")
        
        # Sample treatment information - in a real app, this would come from a database
        treatments = {
            "Wheat_Leaf Rust": {
                "chemical": ["Propiconazole", "Tebuconazole", "Azoxystrobin"],
                "biological": ["Trichoderma harzianum", "Bacillus subtilis"],
                "cultural": ["Crop rotation", "Use resistant varieties", "Proper spacing", "Early sowing"],
                "severity": "Medium to High",
                "timing": "Apply fungicides at first sign of infection or as preventative measure"
            },
            "Rice_Blast": {
                "chemical": ["Tricyclazole", "Isoprothiolane", "Azoxystrobin"],
                "biological": ["Pseudomonas fluorescens", "Bacillus subtilis"],
                "cultural": ["Use resistant varieties", "Proper water management", "Balanced fertilization"],
                "severity": "High",
                "timing": "Preventative application at tillering stage, repeat if necessary"
            }
        }
        
        key = f"{treatment_crop}_{treatment_disease}"
        
        if key in treatments:
            treatment_data = treatments[key]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Chemical Controls")
                for chemical in treatment_data["chemical"]:
                    st.markdown(f"- {chemical}")
                
                st.markdown("### Biological Controls")
                for biological in treatment_data["biological"]:
                    st.markdown(f"- {biological}")
            
            with col2:
                st.markdown("### Cultural Practices")
                for practice in treatment_data["cultural"]:
                    st.markdown(f"- {practice}")
                
                st.markdown(f"**Severity Level:** {treatment_data['severity']}")
                st.markdown(f"**Application Timing:** {treatment_data['timing']}")
        else:
            # Generate generic recommendations when specific ones aren't available
            st.info("Detailed treatment information not available for this specific disease-crop combination. Here are general recommendations:")
            
            st.markdown("### General Recommendations")
            st.markdown("""
            - Consult with local agricultural extension officers for specific products available in your area
            - Consider integrated pest management (IPM) approaches
            - Rotate chemical controls to prevent resistance development
            - Apply treatments early in disease development for best results
            - Follow all safety guidelines when applying chemical treatments
            """)
        
        # Display related information
        st.subheader("Economic Impact")
        
        impact_data = {
            'Factor': ['Yield Loss Without Treatment', 'Cost of Treatment', 'Return on Investment'],
            'Value': ['20-40%', 'PKR 2,500-5,000 per acre', '300-500%']
        }
        
        impact_df = pd.DataFrame(impact_data)
        st.table(impact_df)
        
        # Prevention tips
        st.subheader("Prevention Tips")
        st.markdown("""
        1. **Crop Rotation**: Rotate with non-host crops to break disease cycles
        2. **Resistant Varieties**: Use disease-resistant varieties when available
        3. **Field Sanitation**: Remove and destroy infected plant debris
        4. **Seed Treatment**: Use certified disease-free seed or treat seeds before planting
        5. **Balanced Fertilization**: Avoid excessive nitrogen which can increase disease susceptibility
        6. **Water Management**: Avoid overhead irrigation and waterlogging conditions
        7. **Regular Monitoring**: Scout fields regularly for early detection
        """)
        
        # Expert advice section
        st.subheader("Expert Advice")
        st.info("""
        **Dr. Ahmed Khan, Plant Pathologist:**  
        "Early detection and prompt action are critical for effective disease management. 
        Integrated approaches combining resistant varieties, cultural practices, and judicious use of 
        chemical controls provide the most sustainable and effective strategy for disease management in the long term."
        """)

# Footer with additional resources
st.markdown("---")
st.subheader("Additional Resources")

resource_col1, resource_col2, resource_col3 = st.columns(3)

with resource_col1:
    st.markdown("""
    ### Disease Identification Guide
    Download our comprehensive guide to identifying crop diseases in Pakistan
    """)
    st.download_button(
        label="Download Guide",
        data="This would be a PDF file in a real application",
        file_name="crop_disease_guide.pdf",
        mime="application/pdf"
    )

with resource_col2:
    st.markdown("""
    ### Treatment Calculator
    Calculate optimal treatment amounts based on your field size and disease severity
    """)
    st.link_button("Open Calculator", "https://example.com/calculator")

with resource_col3:
    st.markdown("""
    ### Expert Consultation
    Connect with agricultural experts for personalized advice
    """)
    st.link_button("Schedule Consultation", "https://example.com/consult")
