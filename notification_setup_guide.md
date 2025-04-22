# Email and SMS Notification Setup Guide for Agri-Vision System

This guide explains how to set up and use the email and SMS notification features in the Agri-Vision System. The notification system provides alerts for critical farm events such as weather conditions, crop health issues, yield forecasts, and resource management recommendations.

## Prerequisites

1. **For Email Notifications:**
   - An email account to send notifications from (Gmail recommended)
   - App password if using Gmail (for enhanced security)

2. **For SMS Notifications:**
   - A Twilio account
   - Twilio Account SID
   - Twilio Auth Token
   - Twilio Phone Number

## Setting Up Environment Variables

To enable notifications, you need to set the following environment variables:

### Email Notification Variables

```
EMAIL_SENDER=your-email@example.com
EMAIL_PASSWORD=your-email-password-or-app-password
SMTP_SERVER=smtp.gmail.com  # Optional, defaults to Gmail
SMTP_PORT=587  # Optional, defaults to 587
```

### SMS Notification Variables (Twilio)

```
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=your-twilio-phone-number
```

## Creating a Twilio Account

If you don't have a Twilio account, follow these steps to create one and set up SMS notifications:

1. **Sign up for Twilio:**
   - Go to [https://www.twilio.com/](https://www.twilio.com/) and click "Sign Up"
   - Complete the registration process

2. **Get your Twilio credentials:**
   - Log in to your Twilio account
   - Go to the Twilio Console Dashboard
   - Your Account SID and Auth Token will be displayed

3. **Purchase a Twilio phone number:**
   - Go to "Phone Numbers" > "Manage" > "Buy a Number"
   - Select a number with SMS capabilities
   - Complete the purchase

4. **Set up environment variables:**
   - Add your Twilio Account SID, Auth Token, and Phone Number to your environment variables

## Creating a Gmail App Password

If you're using Gmail for sending email notifications, you'll need to generate an App Password instead of using your regular password:

1. **Enable 2-Step Verification:**
   - Go to your Google Account security settings
   - Enable 2-Step Verification if not already enabled

2. **Generate an App Password:**
   - Go to App Passwords in your Google Account
   - Select "Mail" and your device
   - Click "Generate"
   - Use the generated 16-character password as your EMAIL_PASSWORD

## Using the Notification Features

The Agri-Vision System includes several ways to send notifications:

### 1. Notifications Page

The dedicated Notifications page allows you to:
- Configure alert settings
- Test email and SMS notifications
- View notification history
- Set up weekly reports and quiet hours

To access this page, click on "Notifications" in the sidebar navigation.

### 2. Crop Health Alerts

When a disease is detected in the Crop Health page:
1. Upload and analyze a crop image
2. If a disease is detected, you'll see a "Send Alert" section
3. Enter recipient email and/or phone number
4. Click "Send Alerts" to notify stakeholders

### 3. Weather Alerts

The Weather Data page can generate alerts for adverse weather conditions:
1. View weather forecasts and alerts
2. Use the "Send Weather Alert" button for critical conditions
3. Configure recipients and send the notification

### 4. Resource Management Alerts

The Resource Optimization page can send alerts when resource usage exceeds optimal levels:
1. Identify inefficient resource usage
2. Use the "Send Resource Alert" button
3. Configure recipients and send the notification

## Alert Types and Content

The notification system supports four main types of alerts:

1. **Weather Alerts:**
   - Alert level (Warning, Advisory, Watch)
   - Weather condition description
   - Recommended actions
   - Affected fields

2. **Crop Health Alerts:**
   - Disease/issue type
   - Severity level
   - Issue description
   - Affected area/field
   - Recommended actions

3. **Yield Forecast Alerts:**
   - Field and crop information
   - Current yield forecast
   - Change from previous forecast
   - Contributing factors
   - Recommendations

4. **Resource Management Alerts:**
   - Resource type (water, nutrients, etc.)
   - Current usage levels
   - Optimal usage levels
   - Efficiency percentage
   - Recommendations for optimization

## Programmatic API

For developers, the notification system provides a simple API through the `utils/notification.py` module:

```python
from utils.notification import send_email, send_sms, send_alert

# Send an email
success, message = send_email(
    recipient_email="farmer@example.com",
    subject="Crop Health Alert",
    message="<h1>Disease Detected</h1><p>Leaf rust detected in North Field</p>",
    attachments=["path/to/image.jpg"]  # Optional
)

# Send an SMS
success, message = send_sms(
    to_phone_number="+923001234567",
    message="ALERT: Leaf rust detected in North Field. Immediate treatment recommended."
)

# Send a structured alert (email and/or SMS)
result = send_alert(
    alert_type="crop_health",  # Options: "weather", "crop_health", "yield", "resource"
    alert_data={
        "issue_type": "Leaf Rust",
        "severity": "High",
        "description": "Leaf rust detected in wheat crop",
        "affected_area": "North section",
        "field": "North Field",
        "action": "Apply fungicide treatment immediately"
    },
    recipient_info={
        "email": "farmer@example.com",
        "phone": "+923001234567"
    }
)
```

## Troubleshooting

### Email Notifications Issues

1. **Authentication Failed:**
   - Verify your email and password are correct
   - If using Gmail, ensure you're using an App Password
   - Check that "Less secure app access" is enabled (if not using App Password)

2. **Connection Errors:**
   - Verify the SMTP server and port settings
   - Check your internet connection
   - Ensure your email provider allows SMTP access

### SMS Notification Issues

1. **Authentication Failed:**
   - Verify your Twilio Account SID and Auth Token
   - Check if your Twilio account is active and has sufficient credits

2. **Message Sending Failed:**
   - Ensure the recipient phone number is in E.164 format (e.g., +923001234567)
   - Verify that your Twilio phone number is SMS-capable
   - Check if the destination country is supported by your Twilio account

## Best Practices

1. **Notification Frequency:**
   - Avoid sending too many notifications to prevent alert fatigue
   - Use severity thresholds to filter out non-critical alerts
   - Implement quiet hours for non-urgent notifications

2. **Message Content:**
   - Keep SMS messages concise and under 160 characters
   - Include the alert type and field/crop in the first few words
   - For emails, use HTML formatting to highlight important information

3. **Security:**
   - Store all credentials securely as environment variables
   - Rotate passwords and authentication tokens periodically
   - Use HTTPS for any API communications

4. **Testing:**
   - Use the test features on the Notifications page before relying on alerts
   - Verify that recipients receive test messages correctly
   - Check how messages appear on different devices and email clients