import requests
import json
import time
from datetime import datetime, timedelta
from math import radians, sin, cos, sqrt, atan2

# -------- CONFIG -------- #
user_lat = 12.9352
user_lng = 77.6141
sport_id = "SP5"
user_id = "8871905885"
device_type = 99
auth_token = "b4ee93df154de37b0e38aa6a5dfda071aa751bfa"
venue_api_token = "5534898698eb3426d00168b6ed447d23d000026552ed6200"
days_to_check = 2
pages_to_fetch = 5

# -------- HEADERS -------- #
headers_venue = {
    "Content-Type": "application/json",
    "Authorization": venue_api_token
}

headers_slot = {
    "accept": "application/json",
    "authorization": auth_token,
    "origin": "https://playo.co",
    "referer": "https://playo.co/",
    "user-agent": "Mozilla/5.0"
}

# -------- UTILS -------- #
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return round(R * c, 2)

# -------- FETCH VENUES -------- #
all_venues = []
for page in range(1, pages_to_fetch + 1):
    payload = {
        "category": "venue",
        "page": page,
        "lat": user_lat,
        "lng": user_lng,
        "sportId": [sport_id],
        "avgRatingSort": 0
    }

    response = requests.post("https://api.playo.io/venue-public/v2/list", headers=headers_venue, json=payload)
    if not response.ok:
        print(f"Failed to fetch page {page}")
        continue

    venue_list = response.json().get("data", {}).get("venueList", [])
    if not venue_list:
        print(f"No venues found on page {page}")
        break

    all_venues.extend(venue_list)
    print(f"✅ Page {page}: {len(venue_list)} venues")
    time.sleep(1)

# -------- CHECK SLOTS -------- #
today = datetime.now()
all_slots = []

for venue in all_venues:
    venue_id = venue.get("venueId")
    venue_name = venue.get("name")
    coords = venue.get("geoLocation", {}).get("coordinates", [])
    if len(coords) != 2:
        continue
    venue_lng, venue_lat = coords
    distance = haversine(user_lat, user_lng, venue_lat, venue_lng)

    for day in range(days_to_check):
        date_str = (today + timedelta(days=day)).strftime("%Y-%m-%d")
        url = f"https://playo.club/book-api/v5/availability/{venue_id}/{sport_id}/{date_str}/?userId={user_id}&deviceType={device_type}"

        res = requests.get(url, headers=headers_slot)
        if not res.ok:
            continue

        court_list = res.json().get("data", {}).get("courtList", [])
        for court in court_list:
            court_name = court.get("courtName", "Unknown Court")
            for slot in court.get("slotInfo", []):
                if slot.get("status") == 1:
                    try:
                        price_values = [float(p.strip()) for p in slot["price"].split(",") if p.strip()]
                        price = min(price_values)
                    except Exception as e:
                        print(f"❌ Error parsing price at {venue_name} - {court_name} - {slot.get('time')}: {slot['price']}")
                        continue

                    all_slots.append({
                        "venue": venue_name,
                        "court": court_name,
                        "date": date_str,
                        "time": slot["time"],
                        "price": price,
                        "distance_km": distance
                    })

        time.sleep(0.5)

# -------- SORT & SAVE -------- #
sorted_slots = sorted(all_slots, key=lambda x: (x["price"], x["distance_km"], x["date"], x["time"]))

with open("available_slots_multi_venue.json", "w") as f:
    json.dump(sorted_slots, f, indent=2)

print(f"\n🎯 Done! {len(sorted_slots)} available slots saved to 'available_slots_multi_venue.json'")
