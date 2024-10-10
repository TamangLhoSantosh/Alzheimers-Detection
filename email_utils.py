import os

import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import ssl

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


async def send_email(email, subject, body):
    message = EmailMessage()
    message["From"] = EMAIL_USER
    message["To"] = email
    message["Subject"] = subject
    message.set_content(body, subtype="html")

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT, context=context) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASSWORD)
        smtp.sendmail(EMAIL_USER, email, message.as_string())


async def send_verification_email(email: str, token: str):
    verification_link = f"http://localhost:8000/verify-email?token={token}"
    subject = "Email Verification"
    body = f"""
    <h1>Verify Your Email</h1>
    <p>Please click <a href="{verification_link}">here</a> to verify your email.</p>
"""
    await send_email(email, subject, body)


async def send_reset_email(email: str, token: str):
    reset_link = f"http://localhost:8000/password-reset/confirm?token={token}"
    subject = "Password Reset"
    body = f"""
    <h1>Reset Your Password</h1>
    <p>Please click <a href="{reset_link}">here</a> to reset password.</p>
"""
    await send_email(email, subject, body)
