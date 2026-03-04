import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("SCRAPINGDOG_API_KEY")

def test_meta():
    print("Testing Meta Ads Scraper...")
    url = "https://api.scrapingdog.com/facebook/ads"
    params = {
        "api_key": API_KEY,
        "query": "Emaar",
        "limit": 5,
        "active_status": "active",
        "country": "all" # Try 'all' if 'AE' returns nothing
    }
    r = requests.get(url, params=params)
    print(f"Status: {r.status_code}")
    data = r.json()
    with open("meta_test_response.json", "w") as f:
        json.dump(data, f, indent=2)
    ads = data.get("ads", [])
    print(f"Meta Ads saved to meta_test_response.json. Found: {len(ads)}")

def test_google():
    print("\nTesting Google Ads Scraper...")
    url = "https://api.scrapingdog.com/google"
    params = {
        "api_key": API_KEY,
        "query": "Emaar Properties Dubai",
        "country": "ae",
        "advance_search": "true",
        "domain": "google.ae"
    }
    r = requests.get(url, params=params)
    print(f"Status: {r.status_code}")
    data = r.json()
    with open("google_test_response.json", "w") as f:
        json.dump(data, f, indent=2)
    ads = data.get("ads", []) or data.get("top_ads", [])
    print(f"Google Ads saved to google_test_response.json. Found: {len(ads)}")

if __name__ == "__main__":
    test_meta()
    test_google()
