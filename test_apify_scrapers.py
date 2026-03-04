import logging
import json
from scraper import MetaAdsScraper, GoogleAdsScraper

logging.basicConfig(level=logging.INFO)

def test_apify_scrapers():
    print("--- Testing Meta Ads Scraper (Apify) ---")
    meta_scraper = MetaAdsScraper()
    
    developers = ["Emaar Properties"]
    
    for dev in developers:
        print(f"\n>> Testing for: {dev}")
        # Test 1: URL based
        results = meta_scraper.scrape_developer_ads(dev, max_ads=2)
        print(f"Results: {len(results)}")
        if results:
            print(json.dumps(results[0], indent=2))

    print("\n--- Testing Google Ads Scraper (Apify) ---")
    google_scraper = GoogleAdsScraper()
    google_results = google_scraper.scrape_developer_ads("Emaar Properties", max_ads=2)
    print(f"Google Ads Found: {len(google_results.get('search_items', []))}")

if __name__ == "__main__":
    test_apify_scrapers()
