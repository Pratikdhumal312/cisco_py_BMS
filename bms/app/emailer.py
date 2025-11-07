import smtplib
from threading import Thread
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from app.config import Config
from app.logger import logger
from app.exceptions import EmailError



def send_gmail_async(to_address: str, subject: str, body: str, image_path: str = None) -> None:
    """
    Send Gmail email asynchronously with optional image attachment.
    """

    def _send_email():
        try:
            # Create email
            msg = MIMEMultipart()
            msg["From"] = Config.SMTP_USERNAME  # usually your Gmail address
            msg["To"] = to_address
            msg["Subject"] = subject

            # Add text
            msg.attach(MIMEText(body, "plain"))

            # Optional: Add image
            if image_path:
                try:
                    with open(image_path, "rb") as f:
                        img_data = f.read()
                    image = MIMEImage(img_data, name=image_path.split("\\")[-1])
                    msg.attach(image)
                    logger.info("email_image_attached", image=image_path)
                except Exception as e:
                    logger.warning("image_attachment_failed", error=str(e), image=image_path)

            # Connect to Gmail SMTP
            with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
                server.starttls()
                server.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
                server.send_message(msg)

            logger.info("email_sent", to=to_address, subject=subject)

        except Exception as e:
            logger.error("email_send_failed", error=str(e), to=to_address)
            raise EmailError(f"Failed to send email: {str(e)}")

    # Send in background
    Thread(target=_send_email).start()


def notify_account_created(account_number: str, account_name: str, balance: float, to_email: str = None) -> None:
    """Convenience wrapper to notify about account creation."""
    if to_email is None:
        to_email = Config.NOTIFICATIONS_EMAIL

    subject = f"New Account Created: {account_number}"
    body = (
        f"A new account has been created:\n\n"
        f"Account Number: {account_number}\n"
        f"Account Name: {account_name}\n"
        f"Initial Balance: ${balance:.2f}\n\n"
        "This is an automated notification from BMS."
    )

    send_gmail_async(to_email, subject, body)
