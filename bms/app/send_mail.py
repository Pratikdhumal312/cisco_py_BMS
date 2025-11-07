from emailer import send_gmail_async
from app.config import Config

if __name__ == "__main__":
    image_path = r"C:\Users\pratdhum\OneDrive - Cisco\Desktop\Python 1\cisco_py_311025\email\Screenshot 2025-11-06 094104.png"
    body = "This is a test email with an image attachment."
    
    send_gmail_async(
        to_address=Config.NOTIFICATIONS_EMAIL,
        subject="Hello from Banking System",
        body=body,
        image_path=image_path
    )

    print("Email sending started in background...")
