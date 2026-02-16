#!/usr/bin/env python3
"""
Quick data seed for The Leap Dashboard
Uses Supabase REST API directly
"""

import requests
from datetime import date

# Supabase config
SUPABASE_URL = "https://sdgmpjfyzgecfgjpkeua.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNkZ21wamZ5emdlY2ZnanBrZXVhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTA4MDQxOSwiZXhwIjoyMDg2NjU2NDE5fQ.BvkDc7nPpPYjGhMSU-9whQM_wDG8CN3sOMsbLTjazIc"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

def upsert(table, data):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    response = requests.post(url, headers=headers, json=data, params={"on_conflict": "date"})
    if response.status_code in [200, 201]:
        print(f"✅ {table}: OK")
    else:
        print(f"❌ {table}: {response.status_code} - {response.text}")
    return response

# Seed daily_logs for Feb 16
upsert("daily_logs", {
    "date": "2026-02-16",
    "wake_time": "10:15",
    "wake_on_time": False,
    "trading_pnl": None,
    "trading_notes": "Paper trading - learning liquidity. No funded account yet.",
    "calories": None,
    "protein": None,
    "gym_done": False,
    "gym_workout": "Rest (Abs & Neck)",
    "notes": "Woke up late. Focused on trading education. CMPUT 379 midterm prep starts today."
})

# Seed daily_logs for previous days (from memory)
previous_days = [
    {"date": "2026-02-15", "wake_time": "09:58", "wake_on_time": False, "gym_done": True, "gym_workout": "Legs", "calories": None, "protein": None},
    {"date": "2026-02-14", "wake_time": "09:58", "wake_on_time": False, "gym_done": True, "gym_workout": "Back & Bi", "calories": None, "protein": None},
    {"date": "2026-02-13", "wake_time": "09:17", "wake_on_time": False, "gym_done": True, "gym_workout": "Shoulders", "calories": None, "protein": None},
    {"date": "2026-02-12", "wake_time": "11:07", "wake_on_time": False, "gym_done": False, "gym_workout": None, "calories": None, "protein": None},
]

for day in previous_days:
    upsert("daily_logs", day)

# Seed streaks
streaks = [
    {"streak_type": "wake_up", "current_streak": 0, "longest_streak": 0, "last_success_date": None},
    {"streak_type": "gym", "current_streak": 3, "longest_streak": 3, "last_success_date": "2026-02-15"},
    {"streak_type": "nutrition", "current_streak": 0, "longest_streak": 0, "last_success_date": None},
]

for streak in streaks:
    url = f"{SUPABASE_URL}/rest/v1/consistency_streaks"
    response = requests.post(url, headers=headers, json=streak, params={"on_conflict": "streak_type"})
    if response.status_code in [200, 201]:
        print(f"✅ streaks/{streak['streak_type']}: OK")
    else:
        print(f"❌ streaks/{streak['streak_type']}: {response.status_code}")

# Seed portfolio snapshot (from today's cron check)
upsert("portfolio_snapshots", {
    "date": "2026-02-16",
    "total_value_cad": 1670,
    "total_value_usd": 1168.58,
    "holdings": {
        "VFV": {"shares": 1, "price_cad": 165.25, "value_cad": 165.25},
        "USDC": {"amount": 323, "price": 1.0, "value_usd": 323},
        "SOL": {"amount": 2.23, "price": 83.16, "value_usd": 185.34},
        "XRP": {"amount": 200, "price": 1.47, "value_usd": 294},
        "ONDO": {"amount": 589, "price": 0.27, "value_usd": 159.28},
        "CRV": {"amount": 250, "price": 0.25, "value_usd": 62.48},
        "TON": {"amount": 11, "price": 1.44, "value_usd": 15.84},
        "AERO": {"amount": 42, "price": 0.31, "value_usd": 12.96}
    },
    "biggest_mover_symbol": "SOL",
    "biggest_mover_pct": -4.72
})

# Seed school deadlines
deadlines = [
    {"course_code": "CMPUT 379", "course_name": "Operating Systems", "assignment_name": "Midterm 1", "due_date": "2026-02-23", "weight_pct": 10, "completed": False, "notes": "In-class exam"},
    {"course_code": "OM 252", "course_name": "Operations Management", "assignment_name": "Homework 5", "due_date": "2026-02-26", "weight_pct": None, "completed": False, "notes": "~Feb 26"},
    {"course_code": "BTM 417", "course_name": "Telecommunications", "assignment_name": "Individual Assignment", "due_date": "2026-03-05", "weight_pct": 15, "completed": False, "notes": "Before 1:00 PM"},
    {"course_code": "SEM 210", "course_name": "Strategy & Entrepreneurship", "assignment_name": "Group Project", "due_date": "2026-03-27", "weight_pct": 8, "completed": False, "notes": "Due 22:00"},
    {"course_code": "CMPUT 379", "course_name": "Operating Systems", "assignment_name": "Assignment 2", "due_date": "2026-03-30", "weight_pct": 10, "completed": False, "notes": "Sockets programming"},
]

for deadline in deadlines:
    url = f"{SUPABASE_URL}/rest/v1/school_deadlines"
    response = requests.post(url, headers=headers, json=deadline)
    if response.status_code in [200, 201]:
        print(f"✅ deadline/{deadline['assignment_name']}: OK")
    else:
        print(f"❌ deadline/{deadline['assignment_name']}: {response.status_code}")

print("\n🚀 Dashboard data seeded!")
