import smtplib
from threading import Thread
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from app.config import Config
from app.logger import logger  # optional: your existing logger

def send_gmail_async(to_address, subject, body, image_path=None):
    """
    Send Gmail email asynchronously with optional image attachment.
    """

    def _send_email():
        try:
            # Create email
            msg = MIMEMultipart()
            msg["From"] = Config.SMTP_USERNAME  # sender email
            msg["To"] = to_address
            msg["Subject"] = subject

            # Add plain text body
            msg.attach(MIMEText(body, "plain"))

            # Optional image attachment
            if image_path:
                try:
                    with open(image_path, "rb") as f:
                        img_data = f.read()
                    image_name = image_path.split("\\")[-1].split("/")[-1]
                    msg.attach(MIMEImage(img_data, name=image_name))
                    logger.info(f"✅ Attached image: {image_name}")
                except Exception as e:
                    logger.warning(f"⚠️ Failed to attach image: {e}")

            # Check test mode: if enabled, log and skip real send
            if getattr(Config, 'EMAIL_TEST_MODE', False):
                logger.info(f"[TEST MODE] Would send email to {to_address}: {subject}")
            else:
                # Connect and send using configured SMTP server
                smtp_server = getattr(Config, 'SMTP_SERVER', 'smtp.gmail.com')
                smtp_port = int(getattr(Config, 'SMTP_PORT', 587))
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
                    server.send_message(msg)

            logger.info(f"📧 Email sent successfully to {to_address}")

        except Exception as e:
            logger.error(f"❌ Failed to send email: {e}")

    # Send in a background thread
    Thread(target=_send_email).start()


# Example usage:
# Notification wrapper functions
def notify_account_created(user_email, username):
    """Send welcome email to newly created account."""
    subject = "Welcome to BMS - Account Created Successfully"
    body = f"Hello {username},\n\nYour account has been successfully created in the BMS system.\n\nBest regards,\nBMS Team"
    send_gmail_async(user_email, subject, body)

def notify_batch_processed(admin_email, batch_id, status, details):
    """Notify admin about batch processing results."""
    subject = f"BMS Batch Processing Report - Batch {batch_id}"
    body = f"Batch Processing Status: {status}\n\nDetails:\n{details}"
    send_gmail_async(admin_email, subject, body)

def notify_error(admin_email, error_type, error_details):
    """Notify admin about system errors."""
    subject = f"BMS System Alert - {error_type}"
    body = f"An error occurred in the BMS system:\n\nType: {error_type}\nDetails: {error_details}"
    send_gmail_async(admin_email, subject, body)

# if __name__ == "__main__":
#     # Test email sending
#     send_gmail_async(
#         to_address=Config.NOTIFICATIONS_EMAIL,
#         subject="BMS Test Email",
#         body="Hello! This is a test email from the BMS Project.",
#     )
