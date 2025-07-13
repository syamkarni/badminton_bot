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

print(f"Status: {response.status_code}")
if response.ok:
    print("\n=== RAW JSON ===")
    print(response.text)  


    with open("sample_json/raw_slot_response.json", "w") as f:
        f.write(response.text)

else:
    print("Request failed")
    print(response.text)
