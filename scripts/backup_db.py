import os
import subprocess
import json
import requests

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
BACKUP_FILE = "supabase_backup.json"

def backup_tables():
    tables = ["users", "profiles", "medications", "reminders"]
    backup_data = {}
    headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
    for table in tables:
        url = f"{SUPABASE_URL}/rest/v1/{table}"
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            backup_data[table] = resp.json()
        else:
            print(f"Failed to backup {table}")
    with open(BACKUP_FILE, "w") as f:
        json.dump(backup_data, f, indent=2)
    print("Database backup completed")

if __name__ == "__main__":
    backup_tables()