import requests
import json

venue_id = "c7463e9b-08b4-4c3f-9894-ed9cfc79efc9"
sport_id = "SP5"
date = "2025-07-13"
user_id = "8871905885"
device_type = 99

url = f"https://playo.club/book-api/v5/availability/{venue_id}/{sport_id}/{date}/?userId={user_id}&deviceType={device_type}"

headers = {
    "accept": "application/json",
    "authorization": "b4ee93df154de37b0e38aa6a5dfda071aa751bfa",
    "origin": "https://playo.co",
    "referer": "https://playo.co/",
    "user-agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

if response.ok:
    data = response.json()
    court_list = data.get("data", {}).get("courtList", [])
    
    available_slots = []
    
    for court in court_list:
        court_name = court.get("courtName")
        for slot in court.get("slotInfo", []):
            if slot.get("status") == 1:
                available_slots.append({
                    "court": court_name,
                    "time": slot["time"],
                    "price": float(slot["price"])
                })
    

    sorted_slots = sorted(available_slots, key=lambda x: (x["price"], x["time"]))

    for slot in sorted_slots:
        print(f"{slot['court']} - {slot['time']} - ₹{slot['price']}")
    
    if not sorted_slots:
        print("No slots available.")
else:
    print(f"Request failed: {response.status_code}")
    print(response.text)
