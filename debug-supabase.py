#!/usr/bin/env python3
"""Debug: Check what's in Supabase"""
from supabase import create_client

SUPABASE_URL = "https://sdgmpjfyzgecfgjpkeua.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNkZ21wamZ5emdlY2ZnanBrZXVhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTA4MDQxOSwiZXhwIjoyMDg2NjU2NDE5fQ.BvkDc7nPpPYjGhMSU-9whQM_wDG8CN3sOMsbLTjazIc"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("📊 Checking daily_logs...")
result = supabase.table("daily_logs").select("*").order("date", desc=True).limit(20).execute()

if result.data:
    print(f"\nFound {len(result.data)} records:")
    for row in result.data:
        cal = row.get('calories', 'NULL')
        pro = row.get('protein', 'NULL')
        print(f"  {row['date']}: {cal} cal / {pro}g protein")
else:
    print("  No data found!")

# Check date range
print("\n📅 Date range check...")
all_result = supabase.table("daily_logs").select("date").order("date", desc=True).execute()
if all_result.data:
    dates = [r['date'] for r in all_result.data]
    print(f"  Most recent: {dates[0] if dates else 'None'}")
    print(f"  Oldest: {dates[-1] if dates else 'None'}")
    print(f"  Total records: {len(dates)}")
    
    # Check for Feb/March dates
    feb_march = [d for d in dates if d.startswith('2026-02') or d.startswith('2026-03')]
    print(f"  Feb/March records: {len(feb_march)}")
    if feb_march:
        print(f"  Feb/March dates: {feb_march}")
