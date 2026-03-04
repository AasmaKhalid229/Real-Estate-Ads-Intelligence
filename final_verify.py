import logging
import json
import os
from apify_client import ApifyClient
from scraper import MetaAdsScraper, GoogleAdsScraper

logging.basicConfig(level=logging.INFO)

def verify_final():
    print("--- Verifying Meta Ads (apify/facebook-ads-scraper) ---")
    meta = MetaAdsScraper()
    res_meta = meta.scrape_developer_ads("Emaar Properties", max_ads=1)
    print(f"Meta Results: {len(res_meta)}")
    if res_meta:
        print(json.dumps(res_meta[0], indent=2))
        
    print("\n--- Verifying Google Ads (memo23/google-ad-transparency-scraper-cheerio) ---")
    google = GoogleAdsScraper()
    res_google = google.scrape_developer_ads("Emaar Properties", max_ads=1)
    print(f"Google Results: {len(res_google.get('search_items', []))}")
    if res_google.get('search_items'):
        print(json.dumps(res_google['search_items'][0], indent=2))

if __name__ == "__main__":
    verify_final()
