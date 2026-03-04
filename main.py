import schedule
import time
import logging
import threading
from scraper import MetaAdsScraper, GoogleAdsScraper
from analyzer import MetaAdsAnalyzer, GoogleAdsAnalyzer, MarketAnalyzer
from reporter import ReportGenerator
from config import TARGET_DEVELOPERS

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_weekly_analysis():
    logger.info("Starting Weekly Meta & Google Ads Analysis Pipeline...")
    
    meta_scraper = MetaAdsScraper()
    meta_analyzer = MetaAdsAnalyzer()
    
    google_scraper = GoogleAdsScraper()
    google_analyzer = GoogleAdsAnalyzer()
    
    market_analyzer = MarketAnalyzer()
    reporter = ReportGenerator()
    
    all_meta_analyses = {}
    all_google_analyses = {}
    
    # Process each developer
    for dev in TARGET_DEVELOPERS:
        logger.info(f"--- Processing {dev} ---")
        
        # 1. Scrape & Analyze Meta Ads
        raw_meta_ads = meta_scraper.scrape_developer_ads(dev, max_ads=10) 
        if raw_meta_ads:
            meta_analysis = meta_analyzer.analyze_developer_ads(dev, raw_meta_ads)
            all_meta_analyses[dev] = meta_analysis
        else:
            logger.info(f"No Meta ads found for {dev}.")
            
        time.sleep(2) # Avoid aggressive rate limits
            
        # 2. Scrape & Analyze Google Ads
        raw_google_search = google_scraper.scrape_developer_ads(dev, max_ads=10)
        if raw_google_search and raw_google_search.get("search_items"):
            google_analysis = google_analyzer.analyze_google_strategy(dev, raw_google_search)
            all_google_analyses[dev] = google_analysis
        else:
            logger.info(f"No Google search items found for {dev}.")
            
        time.sleep(5) 
        
    # 3. Generate Executive Summary
    executive_summary = {}
    if all_meta_analyses or all_google_analyses:
        executive_summary = market_analyzer.generate_executive_summary(all_meta_analyses, all_google_analyses)

    # 4. Generate HTML Report and Send Email
    if all_meta_analyses or all_google_analyses:
        print(f"\n[INFO] Data collection complete. Meta: {len(all_meta_analyses)}, Google: {len(all_google_analyses)}")
        html_report = reporter.format_html_report(all_meta_analyses, all_google_analyses, executive_summary)
        reporter.send_email_report(html_report)
        logger.info("Weekly Analysis Pipeline Completed Successfully.")
        print("\n" + "="*50)
        print("PIPELINE COMPLETED SUCCESSFULLY")
        print(f"Check 'latest_report.html' in the current directory for the full output.")
        print("="*50 + "\n")
    else:
        logger.warning("No data collected across all developers. Pipeline finished without sending email.")
        print("\n[WARNING] No data collected. No report generated.")

def run_scheduler():
    logger.info("Initializing Agent Scheduler...")
    # Schedule the job every Monday at 10:00 AM
    schedule.every().monday.at("10:00").do(run_weekly_analysis)
    
    logger.info("Scheduler running. Waiting for next scheduled execution time...")
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--run-now":
        logger.info("Manual run triggered via flag.")
        run_weekly_analysis()
    else:
        # Run the scheduler in the main thread (or spawn a thread if you need a web server alongside)
        run_scheduler()
