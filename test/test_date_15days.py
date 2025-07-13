import requests
import json
from datetime import datetime, timedelta

venue_id = "c7463e9b-08b4-4c3f-9894-ed9cfc79efc9"
sport_id = "SP5"
user_id = "8871905885"
device_type = 99
auth_token = "b4ee93df154de37b0e38aa6a5dfda071aa751bfa"

headers = {
    "accept": "application/json",
    "authorization": auth_token,
    "origin": "https://playo.co",
    "referer": "https://playo.co/",
    "user-agent": "Mozilla/5.0"
}

today = datetime.now()
days_to_check = 15

all_slots = []

for i in range(days_to_check):
    date_obj = today + timedelta(days=i)
    date = date_obj.strftime("%Y-%m-%d")
    url = f"https://playo.club/book-api/v5/availability/{venue_id}/{sport_id}/{date}/?userId={user_id}&deviceType={device_type}"
    
    print(f"\n📅 Checking: {date}")
    response = requests.get(url, headers=headers)
    
    if not response.ok:
        print(f"❌ Failed ({response.status_code})")
        continue
    
    data = response.json()
    courts = data.get("data", {}).get("courtList", [])
    
    for court in courts:
        court_name = court.get("courtName")
        for slot in court.get("slotInfo", []):
            if slot.get("status") == 1:
                all_slots.append({
                    "date": date,
                    "court": court_name,
                    "time": slot["time"],
                    "price": float(slot["price"])
                })


sorted_slots = sorted(all_slots, key=lambda x: (x["price"], x["date"], x["time"]))


if sorted_slots:
    print(f"\n🎯 Found {len(sorted_slots)} available slots in next {days_to_check} days:\n")
    for s in sorted_slots:
        print(f"{s['date']} - {s['court']} - {s['time']} - ₹{s['price']}")
else:
    print("🚫 No available slots found.")
