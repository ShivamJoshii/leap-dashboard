#!/usr/bin/env python3
"""Update existing daily_logs with nutrition data"""
import requests

SUPABASE_URL = "https://sdgmpjfyzgecfgjpkeua.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNkZ21wamZ5emdlY2ZnanBrZXVhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTA4MDQxOSwiZXhwIjoyMDg2NjU2NDE5fQ.BvkDc7nPpPYjGhMSU-9whQM_wDG8CN3sOMsbLTjazIc"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

updates = [
    {"date": "2026-02-12", "calories": 3000, "protein": 138},
    {"date": "2026-02-13", "calories": 3414, "protein": 128},
]

for update in updates:
    url = f"{SUPABASE_URL}/rest/v1/daily_logs?date=eq.{update['date']}"
    data = {"calories": update["calories"], "protein": update["protein"]}
    response = requests.patch(url, headers=headers, json=data)
    if response.status_code in [200, 204]:
        print(f"✅ Updated {update['date']}: {update['calories']} cal / {update['protein']}g protein")
    else:
        print(f"❌ Failed {update['date']}: {response.status_code} - {response.text}")
