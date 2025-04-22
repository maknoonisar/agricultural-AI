import streamlit as st
import pandas as pd
import os
from utils.notification import send_email, send_sms, send_alert

# Set page config
st.set_page_config(
    page_title="Agri-Vision - Notifications",
    page_icon="📱",
    layout="wide"
)

def render_notifications_page():
    st.title("🔔 Notifications & Alerts")
    
    # Check for required environment variables
    has_twilio = all([
        os.environ.get("TWILIO_ACCOUNT_SID"),
        os.environ.get("TWILIO_AUTH_TOKEN"),
        os.environ.get("TWILIO_PHONE_NUMBER")
    ])
    
    has_email = all([
        os.environ.get("EMAIL_SENDER"),
        os.environ.get("EMAIL_PASSWORD")
    ])
    
    # Create three columns for the header section
    col1, col2, col3 = st.columns([3, 2, 2])
    
    with col1:
        st.markdown("""
        Configure and manage notifications for your agricultural alerts. 
        Set up SMS and email notifications for weather alerts, crop health issues, 
        yield forecasts, and resource management recommendations.
        """)
    
    with col2:
        st.info(f"SMS Notifications: **{'Configured ✅' if has_twilio else 'Not Configured ❌'}**")
        
    with col3:
        st.info(f"Email Notifications: **{'Configured ✅' if has_email else 'Not Configured ❌'}**")
    
    # Tabs for different notification settings
    tab1, tab2, tab3, tab4 = st.tabs(["Alert Settings", "SMS Test", "Email Test", "Notification History"])
    
    with tab1:
        st.subheader("Notification Preferences")
        
        # Create columns for form layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Alert Types")
            weather_alerts = st.toggle("Weather Alerts", value=True)
            crop_health_alerts = st.toggle("Crop Health Alerts", value=True)
            yield_alerts = st.toggle("Yield Forecast Updates", value=True)
            resource_alerts = st.toggle("Resource Management Alerts", value=True)
            
            st.markdown("### Notification Methods")
            use_sms = st.toggle("SMS Notifications", value=has_twilio)
            use_email = st.toggle("Email Notifications", value=has_email)
        
        with col2:
            st.markdown("### Alert Thresholds")
            weather_threshold = st.select_slider(
                "Weather Alert Threshold",
                options=["Low", "Medium", "High", "Critical"],
                value="Medium"
            )
            
            health_threshold = st.select_slider(
                "Crop Health Alert Threshold",
                options=["Low", "Medium", "High", "Critical"],
                value="Medium"
            )
            
            yield_change_threshold = st.slider(
                "Yield Change Threshold (%)",
                min_value=1,
                max_value=20,
                value=5,
                help="Alert when yield forecast changes by this percentage"
            )
            
            resource_efficiency_threshold = st.slider(
                "Resource Efficiency Threshold (%)",
                min_value=50,
                max_value=95,
                value=80,
                help="Alert when resource efficiency falls below this percentage"
            )
        
        # Save alert settings button
        if st.button("Save Alert Settings", type="primary"):
            # In a real app, these would be saved to a database
            st.session_state.alert_settings = {
                "weather_alerts": weather_alerts,
                "crop_health_alerts": crop_health_alerts,
                "yield_alerts": yield_alerts,
                "resource_alerts": resource_alerts,
                "use_sms": use_sms,
                "use_email": use_email,
                "weather_threshold": weather_threshold,
                "health_threshold": health_threshold,
                "yield_change_threshold": yield_change_threshold,
                "resource_efficiency_threshold": resource_efficiency_threshold
            }
            st.success("Alert settings saved successfully!")
    
    with tab2:
        st.subheader("Test SMS Notification")
        
        if not has_twilio:
            st.warning("""
            Twilio credentials not configured. Please set the following environment variables:
            - TWILIO_ACCOUNT_SID
            - TWILIO_AUTH_TOKEN
            - TWILIO_PHONE_NUMBER
            """)
            
            st.markdown("""
            To set up Twilio:
            1. Create a Twilio account at https://www.twilio.com
            2. Get your Account SID and Auth Token from the Twilio Console
            3. Purchase a Twilio phone number
            4. Set up the environment variables in your deployment
            """)
        
        phone_number = st.text_input(
            "Recipient Phone Number (E.164 format)",
            placeholder="+923001234567",
            help="Phone number must be in E.164 format, e.g. +923001234567"
        )
        
        sms_message = st.text_area(
            "SMS Message",
            value="This is a test alert from your Agri-Vision system.",
            max_chars=160
        )
        
        if st.button("Send Test SMS", disabled=not has_twilio):
            if not phone_number:
                st.error("Please enter a valid phone number")
            else:
                with st.spinner("Sending SMS..."):
                    success, message = send_sms(phone_number, sms_message)
                
                if success:
                    st.success(f"SMS sent successfully! {message}")
                else:
                    st.error(f"Failed to send SMS: {message}")
    
    with tab3:
        st.subheader("Test Email Notification")
        
        if not has_email:
            st.warning("""
            Email credentials not configured. Please set the following environment variables:
            - EMAIL_SENDER
            - EMAIL_PASSWORD
            - SMTP_SERVER (optional, defaults to smtp.gmail.com)
            - SMTP_PORT (optional, defaults to 587)
            """)
            
            st.markdown("""
            To set up email notifications:
            1. Use an email account for sending notifications
            2. If using Gmail, you may need to create an App Password
            3. Set up the environment variables in your deployment
            """)
        
        recipient_email = st.text_input(
            "Recipient Email",
            placeholder="farmer@example.com"
        )
        
        email_subject = st.text_input(
            "Email Subject",
            value="Agri-Vision Test Alert"
        )
        
        email_message = st.text_area(
            "Email Message (HTML supported)",
            value="""
            <h2>Agri-Vision Test Alert</h2>
            <p>This is a test alert from your Agri-Vision system.</p>
            <p>You can include HTML content in your email alerts, such as:</p>
            <ul>
                <li>Weather alerts</li>
                <li>Crop health issues</li>
                <li>Yield forecasts</li>
                <li>Resource management recommendations</li>
            </ul>
            """
        )
        
        if st.button("Send Test Email", disabled=not has_email):
            if not recipient_email:
                st.error("Please enter a valid email address")
            else:
                with st.spinner("Sending email..."):
                    success, message = send_email(recipient_email, email_subject, email_message)
                
                if success:
                    st.success(f"Email sent successfully! {message}")
                else:
                    st.error(f"Failed to send email: {message}")
    
    with tab4:
        st.subheader("Notification History")
        
        # In a real app, this would be loaded from a database
        # For this demo, we'll create sample notification history
        notification_data = [
            {"date": "2025-04-22", "type": "Weather", "method": "SMS & Email", "message": "Heavy rainfall expected in the next 24 hours", "status": "Delivered"},
            {"date": "2025-04-20", "type": "Crop Health", "method": "Email", "message": "Possible pest infestation detected in North Field", "status": "Delivered"},
            {"date": "2025-04-18", "type": "Resource", "method": "SMS", "message": "Water efficiency below threshold in East Field", "status": "Delivered"},
            {"date": "2025-04-15", "type": "Yield", "method": "Email", "message": "Yield forecast updated for South Field", "status": "Delivered"},
            {"date": "2025-04-12", "type": "Weather", "method": "SMS & Email", "message": "High temperature alert for next week", "status": "Delivered"}
        ]
        
        notification_df = pd.DataFrame(notification_data)
        
        # Custom CSS for table
        st.markdown("""
        <style>
        .notification-table tr:nth-child(even) {
            background-color: rgba(0, 0, 0, 0.05);
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Display notification history table
        st.dataframe(
            notification_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "date": st.column_config.DateColumn("Date"),
                "type": st.column_config.Column("Type", width="small"),
                "method": st.column_config.Column("Method", width="small"),
                "message": st.column_config.Column("Message"),
                "status": st.column_config.Column("Status", width="small")
            }
        )
        
        st.markdown("*This table shows recent notifications sent to farmers.*")
    
    # Additional settings at the bottom
    st.divider()
    
    st.subheader("Advanced Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Weekly Report")
        send_weekly = st.checkbox("Send weekly farm summary report", value=True)
        report_day = st.selectbox(
            "Day to send weekly report",
            options=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            index=0
        )
    
    with col2:
        st.markdown("### Notification Schedule")
        quiet_hours_start = st.time_input("Quiet hours start", value=pd.Timestamp("22:00").time())
        quiet_hours_end = st.time_input("Quiet hours end", value=pd.Timestamp("06:00").time())
        st.markdown("*Non-critical alerts will not be sent during quiet hours*")
    
    # Save advanced settings button
    if st.button("Save Advanced Settings"):
        # In a real app, these would be saved to a database
        st.session_state.advanced_settings = {
            "send_weekly": send_weekly,
            "report_day": report_day,
            "quiet_hours_start": quiet_hours_start,
            "quiet_hours_end": quiet_hours_end
        }
        st.success("Advanced settings saved successfully!")

# Main execution
if __name__ == "__main__":
    render_notifications_page()