import json
import os


with open("sample_json/playo_data.json", "r") as f:
    data = json.load(f)

sports_list = data["props"]["pageProps"]["allSports"]["list"]
sports_data = []

for sport in sports_list:
    name = sport.get("name", "Unknown Sport")
    code = sport.get("sportId", "Unknown Code")
    print(f"Sport Name: {name}")
    print(f"Sport Code: {code}")
    print()
    sports_data.append({
        "name": name,
        "sportId": code
    })
output_path = "sample_json/sports_codes.json"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w") as f:
    json.dump(sports_data, f, indent=2)
