import logging
import requests
import os
from config import SCRAPINGDOG_API_KEY, TARGET_DEVELOPERS

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MetaAdsScraper:
    def __init__(self):
        self.api_key = SCRAPINGDOG_API_KEY
        self.url = "https://api.scrapingdog.com/facebook/ads"
        
        # Mapping developers to their Facebook Page URLs
        self.developer_urls = {
            "Emaar Properties": "https://www.facebook.com/emaardubai/",
            "DAMAC Properties": "https://www.facebook.com/DAMACPropertiesOfficial/",
            "Nakheel": "https://www.facebook.com/NakheelOfficial/",
            "Sobha Realty": "https://www.facebook.com/SobhaRealty/",
            "Aldar Properties": "https://www.facebook.com/aldar/",
            "Binghatti Developers": "https://www.facebook.com/Binghatti/",
            "Meraas": "https://www.facebook.com/MeraasDubai/",
            "Dubai Properties": "https://www.facebook.com/DubaiProperties/",
            "Azizi Developments": "https://www.facebook.com/AziziGroup/",
            "Danube Properties": "https://www.facebook.com/danubeproperties/"
        }

    def scrape_developer_ads(self, developer_name: str, max_ads: int = 15):
        """Scrapes recent active ads for a given developer using Scrapingdog."""
        logger.info(f"Starting Meta ad scrape for {developer_name} via Scrapingdog...")
        
        params = {
            "api_key": self.api_key,
            "query": developer_name,
            "limit": max_ads,
            "active_status": "active",
            "country": "all"
        }

        try:
            response = requests.get(self.url, params=params)
            response.raise_for_status()
            data = response.json()
            
            raw_ads = data.get("ads", [])
            results = []
            
            for item in raw_ads:
                snapshot = item.get("snapshot", {})
                ad_data = {
                    "developer": developer_name,
                    "ad_id": item.get("ad_archive_id"),
                    "page_name": snapshot.get("page_name", developer_name),
                    "ad_text": snapshot.get("body", {}).get("text", ""),
                    "start_date": item.get("start_date"),
                    "format": snapshot.get("display_format", "Unknown"),
                    "media_urls": snapshot.get("images", []) + snapshot.get("videos", []),
                    "cta_text": snapshot.get("cta_text", "Learn More"),
                    "ad_url": snapshot.get("link") or f"https://www.facebook.com/ads/library/?id={item.get('ad_archive_id')}"
                }
                results.append(ad_data)
                if len(results) >= max_ads:
                    break
                    
            logger.info(f"Successfully scraped {len(results)} Meta ads for {developer_name}")
            return results
            
        except Exception as e:
            logger.error(f"Error scraping Meta ads for {developer_name}: {e}")
            return []

    def scrape_all_developers(self):
        """Scrapes ads for all target developers."""
        all_ads = {}
        for developer in TARGET_DEVELOPERS:
            ads = self.scrape_developer_ads(developer)
            all_ads[developer] = ads
        return all_ads

class GoogleAdsScraper:
    def __init__(self):
        self.api_key = SCRAPINGDOG_API_KEY
        self.url = "https://api.scrapingdog.com/google"
        
        # Mapping developers for search
        self.developer_queries = {
            "Emaar Properties": "emaar properties ads",
            "DAMAC Properties": "damac properties ads",
            "Nakheel": "nakheel properties ads",
            "Sobha Realty": "sobha realty ads",
            "Aldar Properties": "aldar properties ads",
            "Binghatti Developers": "binghatti developers ads",
            "Meraas": "meraas dubai ads",
            "Dubai Properties": "dubai properties ads",
            "Azizi Developments": "azizi developments ads",
            "Danube Properties": "danube properties ads"
        }

    def scrape_developer_ads(self, developer_name: str, max_ads: int = 15):
        """Scrapes Google Ads using Scrapingdog Search API."""
        logger.info(f"Starting Google ad scrape for {developer_name} via Scrapingdog...")
        
        query = self.developer_queries.get(developer_name, f"{developer_name} ads")

        params = {
            "api_key": self.api_key,
            "query": query,
            "country": "ae",
            "advance_search": "true",
            "domain": "google.ae"
        }

        try:
            response = requests.get(self.url, params=params)
            response.raise_for_status()
            data = response.json()
            
            results = {
                "developer": developer_name,
                "search_items": []
            }
            
            # Scrapingdog returns ads in 'ads', 'top_ads', or similar
            ads = data.get("ads", []) or data.get("top_ads", []) or data.get("bottom_ads", [])
            
            # If no ads, fallback to first few organic results but mark them as organic
            if not ads:
                logger.info(f"No sponsored ads found for {developer_name}, using organic fallback.")
                ads = data.get("organic_results", [])[:5]
                type_label = "Organic Result"
            else:
                type_label = "Sponsored Ad"

            for item in ads:
                results["search_items"].append({
                    "type": type_label,
                    "title": item.get("title", developer_name),
                    "description": item.get("description") or item.get("snippet") or "",
                    "url": item.get("link") or "",
                    "displayed_url": item.get("displayed_link", ""),
                    "format": "TEXT" 
                })
                if len(results["search_items"]) >= max_ads:
                    break
                    
            logger.info(f"Successfully scraped {len(results['search_items'])} Google items for {developer_name}")
            return results
            
        except Exception as e:
            logger.error(f"Error scraping Google for {developer_name}: {e}")
            return {"developer": developer_name, "search_items": []}

    def scrape_all_developers(self):
        all_ads = {}
        for developer in TARGET_DEVELOPERS:
            ads = self.scrape_developer_ads(developer)
            all_ads[developer] = ads
        return all_ads

if __name__ == "__main__":
    # Test the scraper
    meta_scraper = MetaAdsScraper()
    test_result_meta = meta_scraper.scrape_developer_ads("Emaar Properties", max_ads=1)
    print(f"Meta Test Result: {test_result_meta}")
    
    google_scraper = GoogleAdsScraper()
    test_result_google = google_scraper.scrape_developer_ads("Emaar Properties", max_ads=2)
    print(f"Google Test Result: {test_result_google}")
