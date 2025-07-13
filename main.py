import requests
from bs4 import BeautifulSoup
import json

url = "https://playo.co/venues/bangalore/sports/badminton"
# url1="https://playo.club/book-api/v5/availability/c7463e9b-08b4-4c3f-9894-ed9cfc79efc9/SP5/2025-07-12"
response = requests.get(url)


soup = BeautifulSoup(response.text, 'html.parser')
script_tag = soup.find("script", {"id": "__NEXT_DATA__", "type": "application/json"})

if script_tag:
    data = json.loads(script_tag.string)
    print(json.dumps(data, indent=2))  # Pretty print the JSON
    with open("sample_json/playo_data.json", "w") as f:
        json.dump(data, f, indent=2)

else:
    print("Script tag not found")

# print(requests.get(url1))

