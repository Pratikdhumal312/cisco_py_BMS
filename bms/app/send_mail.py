import os
import sys

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.emailer import send_gmail_async
from app.config import Config

if __name__ == "__main__":
    # Get email details from user
    to_address = input("Enter recipient's email address: ")
    subject = input("Enter email subject: ")
    print("Enter email body (press Enter twice to finish):")
    
    # Collect body text until user enters a blank line
    body_lines = []
    while True:
        line = input()
        if line == "":
            break
        body_lines.append(line)
    body = "\n".join(body_lines)

    # Ask about image attachment
    attach_image = input("Do you want to attach an image? (yes/no): ").lower().strip() == 'yes'
    image_path = None
    if attach_image:
        image_path = input("Enter the full path to the image file: ")
        if not os.path.exists(image_path):
            print(f"Warning: Image file not found at {image_path}")
            image_path = None
    
    print("\nSending email...")
    send_gmail_async(
        to_address=to_address,
        subject=subject,
        body=body,
        image_path=image_path
    )
    print("Email sending started in background...")

    print("Email sending started in background...")
