#!/usr/bin/env python3
"""
The Leap Dashboard - Data Sync Script
Pushes daily tracking data to Supabase
"""

import os
from datetime import datetime, date
from supabase import create_client

# Supabase config
SUPABASE_URL = "https://sdgmpjfyzgecfgjpkeua.supabase.co"
# Using service_role key for write access with RLS enabled
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNkZ21wamZ5emdlY2ZnanBrZXVhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTA4MDQxOSwiZXhwIjoyMDg2NjU2NDE5fQ.BvkDc7nPpPYjGhMSU-9whQM_wDG8CN3sOMsbLTjazIc"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def log_daily_entry(
    wake_time=None,
    wake_on_time=None,
    trading_pnl=None,
    trading_notes=None,
    calories=None,
    protein=None,
    gym_done=None,
    gym_workout=None,
    notes=None
):
    """Log a daily entry"""
    data = {
        "date": date.today().isoformat(),
        "wake_time": wake_time,
        "wake_on_time": wake_on_time,
        "trading_pnl": trading_pnl,
        "trading_notes": trading_notes,
        "calories": calories,
        "protein": protein,
        "gym_done": gym_done,
        "gym_workout": gym_workout,
        "notes": notes
    }
    
    # Remove None values
    data = {k: v for k, v in data.items() if v is not None}
    
    response = supabase.table("daily_logs").upsert(data).execute()
    return response


def update_streak(streak_type, success=True):
    """Update a consistency streak"""
    # Get current streak
    response = supabase.table("consistency_streaks").select("*").eq("streak_type", streak_type).execute()
    
    if response.data:
        streak = response.data[0]
        if success:
            new_streak = streak["current_streak"] + 1
            longest = max(new_streak, streak["longest_streak"])
        else:
            new_streak = 0
            longest = streak["longest_streak"]
        
        supabase.table("consistency_streaks").update({
            "current_streak": new_streak,
            "longest_streak": longest,
            "last_success_date": date.today().isoformat()
        }).eq("streak_type", streak_type).execute()
    else:
        # Create new streak
        supabase.table("consistency_streaks").insert({
            "streak_type": streak_type,
            "current_streak": 1 if success else 0,
            "longest_streak": 1 if success else 0,
            "last_success_date": date.today().isoformat()
        }).execute()


def log_portfolio_snapshot(
    total_value_cad,
    total_value_usd,
    holdings,
    biggest_mover_symbol=None,
    biggest_mover_pct=None
):
    """Log daily portfolio value"""
    data = {
        "date": date.today().isoformat(),
        "total_value_cad": total_value_cad,
        "total_value_usd": total_value_usd,
        "holdings": holdings,
        "biggest_mover_symbol": biggest_mover_symbol,
        "biggest_mover_pct": biggest_mover_pct
    }
    
    supabase.table("portfolio_snapshots").upsert(data).execute()


def add_school_deadline(
    course_code,
    course_name,
    assignment_name,
    due_date,
    weight_pct=None,
    notes=None
):
    """Add a school deadline"""
    data = {
        "course_code": course_code,
        "course_name": course_name,
        "assignment_name": assignment_name,
        "due_date": due_date,
        "weight_pct": weight_pct,
        "completed": False,
        "notes": notes
    }
    
    supabase.table("school_deadlines").insert(data).execute()


# Example usage
if __name__ == "__main__":
    # Log today's entry
    log_daily_entry(
        wake_time="09:58",
        wake_on_time=False,
        calories=2867,
        protein=137,
        gym_done=True,
        gym_workout="Back & Bi"
    )
    
    # Update streaks
    update_streak("wake_up", success=False)  # Woke up late
    update_streak("gym", success=True)  # Did gym
    update_streak("nutrition", success=False)  # Short on protein
    
    print("✅ Daily data synced to Supabase")
