import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from twilio.rest import Client

def send_email(recipient_email, subject, message, attachments=None):
    """
    Send an email notification with optional attachments.
    
    Parameters:
    recipient_email (str): Email address of the recipient
    subject (str): Email subject
    message (str): Email message body (HTML format supported)
    attachments (list, optional): List of file paths to attach
    
    Returns:
    bool: Success status
    str: Status message
    """
    # Email credentials from environment variables
    sender_email = os.environ.get("EMAIL_SENDER")
    sender_password = os.environ.get("EMAIL_PASSWORD")
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    
    if not sender_email or not sender_password:
        return False, "Email credentials not configured. Please set EMAIL_SENDER and EMAIL_PASSWORD environment variables."
    
    try:
        # Create message container
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        # Attach message body
        msg.attach(MIMEText(message, 'html'))
        
        # Attach files if provided
        if attachments:
            for file_path in attachments:
                if not os.path.exists(file_path):
                    continue
                    
                filename = os.path.basename(file_path)
                
                # Handle different file types
                if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    with open(file_path, 'rb') as img_file:
                        img = MIMEImage(img_file.read())
                        img.add_header('Content-Disposition', 'attachment', filename=filename)
                        msg.attach(img)
                else:
                    with open(file_path, 'rb') as file:
                        attachment = MIMEApplication(file.read())
                        attachment.add_header('Content-Disposition', 'attachment', filename=filename)
                        msg.attach(attachment)
        
        # Connect to SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        
        # Send email
        server.send_message(msg)
        server.quit()
        
        return True, "Email sent successfully"
        
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"


def send_sms(to_phone_number, message):
    """
    Send SMS notification using Twilio.
    
    Parameters:
    to_phone_number (str): Recipient's phone number in E.164 format (e.g. +923001234567)
    message (str): SMS message content
    
    Returns:
    bool: Success status
    str: Status message
    """
    # Twilio credentials from environment variables
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    from_phone_number = os.environ.get("TWILIO_PHONE_NUMBER")
    
    if not account_sid or not auth_token or not from_phone_number:
        return False, "Twilio credentials not configured. Please set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER environment variables."
    
    try:
        # Initialize Twilio client
        client = Client(account_sid, auth_token)
        
        # Send message
        message = client.messages.create(
            body=message,
            from_=from_phone_number,
            to=to_phone_number
        )
        
        return True, f"SMS sent successfully with SID: {message.sid}"
        
    except Exception as e:
        return False, f"Failed to send SMS: {str(e)}"


def send_alert(alert_type, alert_data, recipient_info):
    """
    Send an alert via email and/or SMS based on alert type and recipient preferences.
    
    Parameters:
    alert_type (str): Type of alert ('weather', 'crop_health', 'yield', 'resource')
    alert_data (dict): Alert data containing message and details
    recipient_info (dict): Recipient information with email and phone
    
    Returns:
    dict: Status of email and SMS delivery
    """
    result = {"email": None, "sms": None}
    
    # Format alert messages
    if alert_type == "weather":
        email_subject = f"Weather Alert: {alert_data.get('alert_level', 'Warning')}"
        email_message = f"""
        <h2>Agri-Vision Weather Alert</h2>
        <p><strong>Alert Level:</strong> {alert_data.get('alert_level', 'Warning')}</p>
        <p><strong>Condition:</strong> {alert_data.get('condition', 'Adverse weather expected')}</p>
        <p><strong>Description:</strong> {alert_data.get('description', '')}</p>
        <p><strong>Recommended Action:</strong> {alert_data.get('action', '')}</p>
        <p><strong>Affected Fields:</strong> {', '.join(alert_data.get('affected_fields', ['All fields']))}</p>
        """
        
        sms_message = f"WEATHER ALERT: {alert_data.get('alert_level', 'Warning')} - {alert_data.get('condition', '')}. {alert_data.get('action', '')}"
        
    elif alert_type == "crop_health":
        email_subject = f"Crop Health Alert: {alert_data.get('issue_type', 'Issue Detected')}"
        email_message = f"""
        <h2>Agri-Vision Crop Health Alert</h2>
        <p><strong>Issue Type:</strong> {alert_data.get('issue_type', 'Health issue detected')}</p>
        <p><strong>Severity:</strong> {alert_data.get('severity', 'Medium')}</p>
        <p><strong>Description:</strong> {alert_data.get('description', '')}</p>
        <p><strong>Affected Area:</strong> {alert_data.get('affected_area', '')} in {alert_data.get('field', '')}</p>
        <p><strong>Recommended Action:</strong> {alert_data.get('action', '')}</p>
        """
        
        sms_message = f"CROP HEALTH ALERT: {alert_data.get('severity', 'Medium')} {alert_data.get('issue_type', '')} in {alert_data.get('field', '')}. {alert_data.get('action', '')}"
        
    elif alert_type == "yield":
        email_subject = f"Yield Forecast Update"
        email_message = f"""
        <h2>Agri-Vision Yield Forecast Update</h2>
        <p><strong>Field:</strong> {alert_data.get('field', '')}</p>
        <p><strong>Crop:</strong> {alert_data.get('crop', '')}</p>
        <p><strong>Current Forecast:</strong> {alert_data.get('forecast', '')} tons/acre</p>
        <p><strong>Change:</strong> {alert_data.get('change', '')}% from previous forecast</p>
        <p><strong>Factors:</strong> {alert_data.get('factors', '')}</p>
        <p><strong>Recommendations:</strong> {alert_data.get('recommendations', '')}</p>
        """
        
        sms_message = f"YIELD UPDATE: {alert_data.get('field', '')}, {alert_data.get('crop', '')} now forecast at {alert_data.get('forecast', '')} tons/acre ({alert_data.get('change', '')}%)."
        
    elif alert_type == "resource":
        email_subject = f"Resource Management Alert"
        email_message = f"""
        <h2>Agri-Vision Resource Management Alert</h2>
        <p><strong>Resource Type:</strong> {alert_data.get('resource_type', 'Water')}</p>
        <p><strong>Field:</strong> {alert_data.get('field', '')}</p>
        <p><strong>Current Usage:</strong> {alert_data.get('current_usage', '')} {alert_data.get('unit', '')}</p>
        <p><strong>Optimal Level:</strong> {alert_data.get('optimal', '')} {alert_data.get('unit', '')}</p>
        <p><strong>Efficiency:</strong> {alert_data.get('efficiency', '')}%</p>
        <p><strong>Recommendations:</strong> {alert_data.get('recommendations', '')}</p>
        """
        
        sms_message = f"RESOURCE ALERT: {alert_data.get('resource_type', 'Water')} usage at {alert_data.get('efficiency', '')}% efficiency in {alert_data.get('field', '')}. {alert_data.get('recommendations', '')}"
    
    else:
        email_subject = f"Agri-Vision Alert"
        email_message = f"""
        <h2>Agri-Vision Alert</h2>
        <p>{alert_data.get('message', 'Important notification from your Agri-Vision system')}</p>
        """
        
        sms_message = f"AGRI-VISION ALERT: {alert_data.get('message', 'Important notification from your Agri-Vision system')}"
    
    # Send email if recipient has email
    if recipient_info.get('email'):
        email_status, email_message = send_email(
            recipient_info['email'],
            email_subject,
            email_message,
            alert_data.get('attachments')
        )
        result["email"] = {"success": email_status, "message": email_message}
    
    # Send SMS if recipient has phone
    if recipient_info.get('phone'):
        sms_status, sms_message = send_sms(
            recipient_info['phone'],
            sms_message
        )
        result["sms"] = {"success": sms_status, "message": sms_message}
    
    return result