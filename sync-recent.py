#!/usr/bin/env python3
"""Sync recent data to Leap Dashboard"""
from supabase import create_client
from datetime import date

SUPABASE_URL = "https://sdgmpjfyzgecfgjpkeua.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNkZ21wamZ5emdlY2ZnanBrZXVhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTA4MDQxOSwiZXhwIjoyMDg2NjU2NDE5fQ.BvkDc7nPpPYjGhMSU-9whQM_wDG8CN3sOMsbLTjazIc"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Nutrition data from Shivam
nutrition_data = [
    {"date": "2026-02-21", "calories": 3153, "protein": 127},
    {"date": "2026-02-22", "calories": 3566, "protein": 117},
    {"date": "2026-02-23", "calories": 2200, "protein": 108},
    {"date": "2026-02-24", "calories": 3209, "protein": 135},
    {"date": "2026-02-25", "calories": 3555, "protein": 124},
    {"date": "2026-02-26", "calories": 2500, "protein": 94},
    {"date": "2026-02-27", "calories": 3226, "protein": 157},
    {"date": "2026-02-28", "calories": 2700, "protein": 114},
    {"date": "2026-03-01", "calories": 2811, "protein": 130},
]

print("📊 Syncing nutrition data...")
for entry in nutrition_data:
    try:
        # Check if entry exists
        result = supabase.table("daily_logs").select("id").eq("date", entry["date"]).execute()
        
        data = {
            "date": entry["date"],
            "calories": entry["calories"],
            "protein": entry["protein"]
        }
        
        if result.data:
            # Update existing
            supabase.table("daily_logs").update(data).eq("date", entry["date"]).execute()
            print(f"  ✅ Updated {entry['date']}: {entry['calories']} cal / {entry['protein']}g")
        else:
            # Insert new
            supabase.table("daily_logs").insert(data).execute()
            print(f"  ✅ Inserted {entry['date']}: {entry['calories']} cal / {entry['protein']}g")
    except Exception as e:
        print(f"  ❌ Failed {entry['date']}: {e}")

# Add USAR to portfolio
print("\n📈 Adding USAR to portfolio...")
try:
    # Get current holdings
    result = supabase.table("portfolio_snapshots").select("*").order("date", desc=True).limit(1).execute()
    
    if result.data:
        holdings = result.data[0].get("holdings", {})
        if isinstance(holdings, dict):
            # Add USAR
            if "stocks" not in holdings:
                holdings["stocks"] = {}
            holdings["stocks"]["USAR"] = 8
            
            supabase.table("portfolio_snapshots").update({
                "holdings": holdings
            }).eq("date", result.data[0]["date"]).execute()
            print(f"  ✅ Added 8 shares USAR to {result.data[0]['date']}")
    else:
        print("  ⚠️ No portfolio snapshot found to update")
except Exception as e:
    print(f"  ❌ Failed to update portfolio: {e}")

# Add urgent school deadline
print("\n🎓 Adding school deadlines...")
deadlines = [
    {
        "course_code": "BTM 417",
        "course_name": "Telecommunications in Business",
        "assignment_name": "Individual Assignment",
        "due_date": "2026-03-05",
        "weight_pct": 15,
        "completed": False,
        "notes": "Due before 1:00 PM"
    },
    {
        "course_code": "OM 252", 
        "course_name": "Operations Management",
        "assignment_name": "HW 5",
        "due_date": "2026-02-26",
        "weight_pct": None,
        "completed": True,
        "notes": "Completed"
    },
    {
        "course_code": "OM 252",
        "course_name": "Operations Management", 
        "assignment_name": "Midterm 2",
        "due_date": "2026-03-21",
        "weight_pct": 15,
        "completed": False,
        "notes": "Saturday exam"
    },
    {
        "course_code": "SEM 210",
        "course_name": "Strategy, Entrepreneurship & Management",
        "assignment_name": "Group Project",
        "due_date": "2026-03-27",
        "weight_pct": 8,
        "completed": False,
        "notes": "Due 22:00"
    }
]

for deadline in deadlines:
    try:
        # Check if already exists
        result = supabase.table("school_deadlines").select("id").eq("course_code", deadline["course_code"]).eq("assignment_name", deadline["assignment_name"]).execute()
        
        if not result.data:
            supabase.table("school_deadlines").insert(deadline).execute()
            print(f"  ✅ Added {deadline['course_code']} - {deadline['assignment_name']} ({deadline['due_date']})")
        else:
            # Update due date in case it changed
            supabase.table("school_deadlines").update({
                "due_date": deadline["due_date"],
                "weight_pct": deadline["weight_pct"],
                "notes": deadline["notes"]
            }).eq("id", result.data[0]["id"]).execute()
            print(f"  ✅ Updated {deadline['course_code']} - {deadline['assignment_name']}")
    except Exception as e:
        print(f"  ❌ Failed {deadline['course_code']}: {e}")

print("\n✅ Sync complete!")

# Calculate protein avg for last 7 days
recent_protein = [e["protein"] for e in nutrition_data[-7:]]
avg_protein = sum(recent_protein) / len(recent_protein)
print(f"\n📈 Last 7 days avg protein: {avg_protein:.1f}g (target: 150g)")

# Calculate calorie avg for last 7 days  
recent_cal = [e["calories"] for e in nutrition_data[-7:]]
avg_cal = sum(recent_cal) / len(recent_cal)
print(f"📈 Last 7 days avg calories: {avg_cal:.0f} (target: 3000)")
