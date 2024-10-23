import os  # To interact with the operating system

import smtplib  # For sending emails
from email.message import (
    EmailMessage,
)  # For constructing email messages
import ssl  # For creating a secure connection
from dotenv import load_dotenv

load_dotenv()

# Retrieve email server configurations from environment variables
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


async def send_email(email, subject, body):
    # Create an email message object
    message = EmailMessage()
    message["From"] = EMAIL_USER
    message["To"] = email
    message["Subject"] = subject
    message.set_content(body, subtype="html")  # Set the email content as HTML

    context = ssl.create_default_context()  # Create a secure SSL context

    # Establish a secure SMTP connection and send the email
    with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT, context=context) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASSWORD)
        smtp.sendmail(EMAIL_USER, email, message.as_string())


async def send_verification_email(email: str, token: str):
    # Create a verification link using the provided token
    verification_link = f"http://localhost:8000/verify-email?token={token}"
    subject = "Email Verification"
    body = f"""
    <h1>Verify Your Email</h1>
    <p>Please click <a href="{verification_link}">here</a> to verify your email.</p>
"""

    # Call the send_email function to send the verification email
    await send_email(email, subject, body)


async def send_reset_email(email: str, token: str):
    # Create a password reset link using the provided token
    reset_link = f"http://localhost:8000/password-reset/confirm?token={token}"
    subject = "Password Reset"
    body = f"""
    <h1>Reset Your Password</h1>
    <p>Please click <a href="{reset_link}">here</a> to reset your password.</p>
"""

    # Call the send_email function to send the reset email
    await send_email(email, subject, body)
