import os
import sys
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, time
import requests
import json

# Supabase credentials (from GitHub secrets)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
EMAIL_FROM = os.environ.get("EMAIL_FROM")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

def get_reminders_due_now():
    headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
    now = datetime.now().strftime("%H:%M")
    # Query medications where reminder_time equals current hour:minute
    url = f"{SUPABASE_URL}/rest/v1/medications?reminder_time=eq.{now}&select=*,users(email,username)"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch reminders")
        return []

def send_email(to_email, subject, body):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_FROM
        msg["To"] = to_email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Email failed: {e}")
        return False

def main():
    reminders = get_reminders_due_now()
    for med in reminders:
        user_email = med.get("users", {}).get("email")
        if not user_email:
            continue
        body = f"""Hi {med['users']['username']},

It's time to take your medication:
- Medicine: {med['medicine_name']}
- Dosage: {med['dosage']}

Please take it as prescribed. Stay healthy!

- DOCAI Medical Assistant
"""
        send_email(user_email, "💊 Medication Reminder", body)
        print(f"Reminder sent to {user_email} for {med['medicine_name']}")

if __name__ == "__main__":
    main()