# test_single_stat.py
import requests

BASE_URL = "http://localhost:8000/api/v1"
AUTH_TOKEN = "47bbc0b8a806023ffe193fd324c4ff91dfee5705"
HEADERS = {
    "Authorization": f"Token {AUTH_TOKEN}",
    "Content-Type": "application/json"
}

# Step 1: Get Agriculture sector ID
print("Getting Agriculture sector...")
resp = requests.get(f"{BASE_URL}/sectors/", params={"name": "Agriculture"}, headers=HEADERS)
agriculture = resp.json()["results"][0]
sector_id = agriculture["id"]
print(f"✓ Agriculture ID: {sector_id}")

# Step 2: Get or create source
print("\nGetting/Creating source...")
resp = requests.get(f"{BASE_URL}/sources/", headers=HEADERS)
sources = resp.json().get("results", [])

if sources:
    source_id = sources[0]["id"]
    print(f"✓ Using existing source: {source_id}")
else:
    print("Creating new source...")
    source_data = {
        "name": "GAMBIH Field Research 2024",
        "year": 2024,
        "source_type": "field_survey",
        "confidence_rating": 8.5,
        "is_primary_source": True
    }
    resp = requests.post(f"{BASE_URL}/sources/", json=source_data, headers=HEADERS)
    source_id = resp.json()["id"]
    print(f"✓ Created source: {source_id}")

# Step 3: Create a stat
print("\nCreating stat...")
stat_data = {
    "sector": sector_id,
    "label": "Test Market Size",
    "value": 2.4,
    "unit": "D",
    "year": 2024,
    "is_headline": True,
    "display_order": 1,
    "source": source_id
}

resp = requests.post(f"{BASE_URL}/sector-stats/", json=stat_data, headers=HEADERS)
if resp.status_code == 201:
    print("✓ Stat created successfully!")
    print(f"  Response: {resp.json()}")
else:
    print(f"✗ Failed: {resp.status_code}")
    print(f"  Error: {resp.text}")