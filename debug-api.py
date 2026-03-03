#!/usr/bin/env python3
"""Debug: Test the exact query the dashboard makes"""
import requests

SUPABASE_URL = "https://sdgmpjfyzgecfgjpkeua.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNkZ21wamZ5emdlY2ZnanBrZXVhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTA4MDQxOSwiZXhwIjoyMDg2NjU2NDE5fQ.BvkDc7nPpPYjGhMSU-9whQM_wDG8CN3sOMsbLTjazIc"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
}

# This is exactly what the dashboard JS does
url = f"{SUPABASE_URL}/rest/v1/daily_logs?select=*&order=date.desc&limit=30"

print(f"Fetching: {url}")
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(f"\n✅ Got {len(data)} records from API")
    print("\nFirst 15 records (most recent first):")
    for row in data[:15]:
        cal = row.get('calories')
        pro = row.get('protein')
        has_nutrition = 'YES' if (cal or pro) else 'NO'
        print(f"  {row['date']}: {cal} cal / {pro}g (has data: {has_nutrition})")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
