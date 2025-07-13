import requests
import json
import time

headers = {
    "Content-Type": "application/json",
    #!!!below might not be the same everytime!!!!
    "Authorization": "5534898698eb3426d00168b6ed447d23d000026552ed6200" 
}

all_venues = []
page = 1

while page<5: #adjust the range in the future!
    payload = {
        "category": "venue",
        "page": page,
        "lat": 12.9715987,
        "lng": 77.59456269999998,
        "sportId": ["SP5"],
        "avgRatingSort": 0
    }

    response = requests.post("https://api.playo.io/venue-public/v2/list", headers=headers, json=payload)
    if not response.ok:
        print(f"Page {page} failed: {response.status_code}")
        break

    data = response.json()
    venues = data.get("data", {}).get("venueList", [])
    
    if not venues:
        print(f"No more venues found at page {page}.")
        break

    all_venues.extend(venues)
    print(f"Fetched page {page} with {len(venues)} venues.")
    
    page += 1
    time.sleep(1)

with open("sample_json/all_badminton_venues.json", "w") as f:
    json.dump(all_venues, f, indent=2)

print(f"✅ Total venues fetched: {len(all_venues)}")
