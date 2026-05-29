import os
import requests
import smtplib
from email.mime.text import MIMEText

APP_URL = os.environ.get("APP_URL", "https://docai-app.streamlit.app")  # change after deployment
EMAIL_TO = os.environ.get("ALERT_EMAIL")   # your email
EMAIL_FROM = os.environ.get("EMAIL_FROM")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

def send_alert(message):
    if not EMAIL_TO:
        print("No alert email configured")
        return
    msg = MIMEText(message)
    msg["Subject"] = "🚨 DOCAI Uptime Alert"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)

try:
    response = requests.get(APP_URL, timeout=30)
    if response.status_code != 200:
        send_alert(f"DOCAI app is down! Status code: {response.status_code}\nURL: {APP_URL}")
    else:
        print("App is UP")
except Exception as e:
    send_alert(f"DOCAI app is unreachable!\nError: {str(e)}")