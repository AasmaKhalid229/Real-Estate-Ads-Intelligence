import streamlit as st
import pandas as pd
import time
from scraper import MetaAdsScraper, GoogleAdsScraper
from analyzer import MetaAdsAnalyzer, GoogleAdsAnalyzer, MarketAnalyzer
from reporter import ReportGenerator
from config import TARGET_DEVELOPERS

st.set_page_config(page_title="UAE Real Estate Ads Intelligence", page_icon="📈", layout="wide")

st.title("📈 UAE Real Estate Ads Competitor Intelligence")
st.markdown("Analyze the latest active Facebook, Instagram, and Google Search ads from the top UAE Real Estate developers using AI.")

st.sidebar.header("Configuration")
num_ads = st.sidebar.slider("Number of Ads per Developer to Analyze", min_value=1, max_value=20, value=5)
send_email = st.sidebar.checkbox("Send Email Report when complete", value=True)

if st.button("🚀 Run AI Analysis Pipeline", type="primary"):
    
    progress_bar = st.progress(0, text="Initializing Pipeline...")
    
    meta_scraper = MetaAdsScraper()
    meta_analyzer = MetaAdsAnalyzer()
    
    google_scraper = GoogleAdsScraper()
    google_analyzer = GoogleAdsAnalyzer()
    
    market_analyzer = MarketAnalyzer()
    reporter = ReportGenerator()
    
    all_meta_analyses = {}
    all_google_analyses = {}
    
    tabs = st.tabs(TARGET_DEVELOPERS)
    tab_mapping = {dev: tab for dev, tab in zip(TARGET_DEVELOPERS, tabs)}
    
    total_devs = len(TARGET_DEVELOPERS)
    
    for idx, dev in enumerate(TARGET_DEVELOPERS):
        progress_msg = f"Processing {dev} ({idx+1}/{total_devs})..."
        progress_bar.progress(idx / total_devs, text=progress_msg)
        
        with tab_mapping[dev]:
            col1, col2 = st.columns(2)
            
            # --- Meta Ads ---
            with col1:
                st.subheader("🔵 Meta Ads Intelligence")
                with st.spinner(f"Scraping Meta Ads for {dev}..."):
                    raw_meta_ads = meta_scraper.scrape_developer_ads(dev, max_ads=num_ads)
                    
                if raw_meta_ads:
                    st.success(f"Scraped {len(raw_meta_ads)} Meta ads.")
                    with st.spinner(f"Analyzing Meta strategies with AI..."):
                        meta_analysis = meta_analyzer.analyze_developer_ads(dev, raw_meta_ads)
                        all_meta_analyses[dev] = meta_analysis
                        
                    if meta_analysis:
                        st.info(f"**Core Strategy:**\n{meta_analysis.get('best_ad_strategy', 'N/A')}")
                        ad_list = meta_analysis.get("ad_analyses", [])
                        if ad_list:
                            df = pd.DataFrame(ad_list)
                            # Display key fields in a clean table
                            st.dataframe(df[["format", "campaign_objective", "cta", "funnel_stage", "target_audience", "location"]], use_container_width=True)
                            
                            with st.expander("View Detailed Targeting & Creative Strategy"):
                                for ad in ad_list:
                                    st.markdown(f"---")
                                    st.markdown(f"**Copy Structure:** {ad.get('ad_copy_structure')}")
                                    st.markdown(f"**Creative Strategy:** {ad.get('creative_strategy')}")
                                    st.markdown(f"**Interests:** {ad.get('detailed_interests')}")
                                    st.markdown(f"**Behaviors:** {ad.get('detailed_behaviors')}")
                                    st.markdown(f"**Placements:** {ad.get('placements')}")
                                    st.markdown(f"[View Ad Library]({ad.get('ad_url')})")
                else:
                    st.warning("No active Meta ads found.")
            
            # --- Google Ads ---
            with col2:
                st.subheader("🔴 Google Ads Intelligence")
                with st.spinner(f"Scraping Google Search for {dev}..."):
                    raw_google_search = google_scraper.scrape_developer_ads(dev, max_ads=num_ads)
                    
                if raw_google_search and raw_google_search.get("search_items"):
                    st.success(f"Scraped {len(raw_google_search.get('search_items'))} Google search items.")
                    with st.spinner(f"Analyzing Google Search strategies with AI..."):
                        google_analysis = google_analyzer.analyze_google_strategy(dev, raw_google_search)
                        all_google_analyses[dev] = google_analysis
                        
                    if google_analysis:
                        st.info(f"**Strategy Summary:**\n{google_analysis.get('strategy_summary', 'N/A')}")
                        st.write(f"**Primary Keywords:** {', '.join(google_analysis.get('primary_keywords', []))}")
                        st.write(f"**Secondary Keywords:** {', '.join(google_analysis.get('secondary_keywords', []))}")
                        st.write(f"**Negative Keywords:** {', '.join(google_analysis.get('negative_keywords', []))}")
                        st.write(f"**Ad Copy Components:** {google_analysis.get('ad_copy_components', 'N/A')}")
                        st.write(f"**Landing Page:** {google_analysis.get('landing_page', 'N/A')}")
                else:
                    st.warning("No relevant Google search items found.")
            
            time.sleep(2)
            
    progress_bar.progress(0.9, text="Generating Market Executive Summary...")
    executive_summary = market_analyzer.generate_executive_summary(all_meta_analyses, all_google_analyses)
    
    progress_bar.progress(1.0, text="Analysis Complete!")
    
    if all_meta_analyses or all_google_analyses:
        st.success("🎉 Analysis finished! See the tabs above for developer-specific data.")
        
        # --- Executive Summary UI ---
        st.divider()
        st.header("🏢 Market Executive Summary")
        ex_col1, ex_col2 = st.columns(2)
        with ex_col1:
            st.markdown(f"**Overall Market Trends:**\n{executive_summary.get('overall_market_trends')}")
            st.markdown("**Top Winning Strategies:**")
            for s in executive_summary.get('top_3_winning_strategies', []):
                st.markdown(f"- {s}")
        with ex_col2:
            st.markdown(f"**Notable Competitor Moves:**\n{executive_summary.get('notable_competitor_moves')}")
            st.markdown(f"**Strategic Recommendations:**\n{executive_summary.get('recommendations')}")

        if send_email:
            with st.spinner("Sending Email Report..."):
                html_report = reporter.format_html_report(all_meta_analyses, all_google_analyses, executive_summary)
                reporter.send_email_report(html_report)
            st.success("📧 Email report sent!")
            
            st.divider()
            st.header("📄 HTML Report Preview")
            st.components.v1.html(html_report, height=800, scrolling=True)
    else:
        st.error("No data collected across all developers.")
