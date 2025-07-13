import requests
import json

url = "https://api.playo.io/venue-public/v2/list"

payload = {
    "lat": 12.9716,
    "lng": 77.5946,
    "city": "Bengaluru",
    "offset": 0,
    "limit": 40,
    "sports": ["SP5"],  # You can try ["SP5"] after this works
    "search": "",
    "sort": 0
}

headers = {
    "Content-Type": "application/json",
    "Authorization": "5534898698eb3426d00168b6ed447d23d000026552ed6200"
}

response = requests.post(url, headers=headers, json=payload)

if response.ok:
    data = response.json()
    with open("sample_json/venue_list_response.json", "w") as f:
        json.dump(data, f, indent=2)
    print("Saved venue list data.")
else:
    print(f"Request failed: {response.status_code}, {response.text}")
