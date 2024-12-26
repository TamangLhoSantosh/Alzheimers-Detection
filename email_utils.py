import os
import smtplib  # For sending emails
from email.message import EmailMessage  # For constructing email messages
import ssl  # For creating a secure connection
from dotenv import load_dotenv
import asyncio

load_dotenv()

# Retrieve email server configurations from environment variables
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 465))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

if not EMAIL_HOST or not EMAIL_PORT or not EMAIL_USER or not EMAIL_PASSWORD:
    raise ValueError("Missing email configuration in environment variables.")


async def send_email(email, subject, body):
    # Create an email message object
    message = EmailMessage()
    message["From"] = EMAIL_USER
    message["To"] = email
    message["Subject"] = subject
    # Set the email content as HTML
    message.set_content("Please open this email in an HTML-compatible client.")
    message.add_alternative(body, subtype="html")

    def send():
        # Establish a secure SMTP connection and send the email
        with smtplib.SMTP_SSL(
            EMAIL_HOST,
            EMAIL_PORT,
            context=ssl.create_default_context(),  # Create a secure SSL context
        ) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL_USER, email, message.as_string())

    await asyncio.to_thread(send)


async def send_verification_email(email: str, token: str):
    # Create a verification link using the provided token
    verification_link = f"http://localhost:8000/verify-email?token={token}"
    subject = "Email Verification"
    body = f"""
    <h1>Verify Your Email</h1>
    <p>Please click <a href="{verification_link}">here</a> to verify your email.</p>
    """
    await send_email(email, subject, body)


async def send_reset_email(email: str, token: str):
    # Create a password reset link using the provided token
    reset_link = f"http://localhost:5173/password-reset/confirm?token={token}"
    subject = "Password Reset"
    body = f"""
    <h1>Reset Your Password</h1>
    <p>Please click <a href="{reset_link}">here</a> to reset your password.</p>
    """
    await send_email(email, subject, body)
