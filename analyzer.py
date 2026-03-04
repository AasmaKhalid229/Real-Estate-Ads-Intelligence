import logging
import json
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List, Optional

from config import GEMINI_API_KEY

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define Pydantic models for structured output
class AdForensicAnalysis(BaseModel):
    developer: str = Field(description="Name of the real estate developer")
    ad_id: str = Field(description="Unique ID of the ad")
    ad_url: str = Field(description="URL of the ad in the Meta Ads Library")
    campaign_objective: str = Field(description="Inferred campaign objective (e.g., Lead Generation, Brand Awareness, Conversions)")
    targeting_platform: str = Field(description="Inferred platform placement (e.g., Facebook, Instagram, Audience Network)")
    target_audience: str = Field(description="Inferred target audience (e.g., HNWI, Investors, Families)")
    age_group_target: str = Field(description="Inferred primary age group target (e.g., 30-50)")
    detailed_interests: str = Field(description="Inferred detailed Meta targeting interests (e.g., Real Estate Investing, Luxury Real Estate, Dubai)")
    detailed_behaviors: str = Field(description="Inferred detailed Meta targeting behaviors (e.g., Frequent International Travelers, Expats)")
    location: str = Field(description="Inferred target location (e.g., UAE, GCC, International)")
    language: str = Field(description="Target language(s) (e.g., English, Arabic)")
    custom_audience: str = Field(description="Probable use of Custom Audiences (e.g., Website Visitors, CRM list)")
    lookalike_audience: str = Field(description="Probable use of Lookalike Audiences (e.g., 1% LAL of converters)")
    creative_strategy: str = Field(description="Deep analysis of the creative strategy (Visuals, tone, emotion, hooks)")
    ad_copy_structure: str = Field(description="Analysis of ad copy structure (Headline, body, sub-headings)")
    format: str = Field(description="Ad format (e.g., Image, Video, Carousel)")
    placements: str = Field(description="Specific placements used (e.g., Reels, Stories, Feed)")
    budget_bidding: str = Field(description="Inferred budget and bidding approach (e.g., CBO/ABO, Highest Volume)")
    pixel_conversion_tracking: str = Field(description="Analysis of Pixel and conversion tracking implementation")
    funnel_stage: str = Field(description="Marketing funnel stage (Top/Middle/Bottom of Funnel)")
    funnel_structure: str = Field(description="Overall funnel structure description")
    post_summary: str = Field(description="Brief summary of the ad copy")
    cta: str = Field(description="Call to Action text used")

class DeveloperStrategySummary(BaseModel):
    developer: str = Field(description="Name of the developer")
    best_ad_strategy: str = Field(description="Overall best ad strategy observed for this developer")
    ad_analyses: List[AdForensicAnalysis] = Field(description="List of individual ad analyses")

class GoogleAdAnalysis(BaseModel):
    developer: str = Field(description="Name of the real estate developer")
    core_ad_strategy: str = Field(description="Probable bidding strategy (e.g., Aggressive Branding vs. High-Intent Lead Gen) based on their market positioning.")
    primary_keywords: List[str] = Field(description="The high-volume 'Money Keywords' they likely bid on to capture top-of-page intent.")
    secondary_keywords: List[str] = Field(description="Specific, niche phrases they use to lower CPC while maintaining lead quality.")
    positive_keywords: List[str] = Field(description="Specific terms they likely 'target' to ensure high-quality leads.")
    negative_keywords: List[str] = Field(description="Identify the 'budget-wasters' they are likely excluding (e.g., 'free', 'jobs', 'cheap').")
    match_types: str = Field(description="Inferred keyword match types (e.g., Exact, Phrase, Broad)")
    audience_targeting: str = Field(description="Inferred Google audience targeting (e.g., In-market for Real Estate, Affinity)")
    ad_copy_components: str = Field(description="Breakdown of ad copy components (Headlines, descriptions, extensions)")
    landing_page: str = Field(description="Analysis of the likely landing page flow and content.")
    budget_bidding_strategy: str = Field(description="Inferred budget and bidding strategy (e.g., Maximize Conversions, Target CPA)")
    conversion_tracking: str = Field(description="Analysis of conversion tracking implementation (e.g., GTM, GA4 events)")
    strategy_summary: str = Field(description="A concise summary of the overall Google Ads strategy for this developer.")

class ExecutiveSummary(BaseModel):
    overall_market_trends: str = Field(description="High-level summary of the current UAE real estate ad landscape.")
    top_3_winning_strategies: List[str] = Field(description="The top 3 most effective strategies observed across all developers.")
    notable_competitor_moves: str = Field(description="Any specific aggressive or innovative tactics seen from the tracked developers.")
    recommendations: str = Field(description="Actionable advice for the user based on the analysis.")

class MetaAdsAnalyzer:
    def __init__(self):
        if not GEMINI_API_KEY:
            logger.warning("GEMINI_API_KEY is not set. Analyzer will fail.")
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_name = "gemini-2.5-flash" # Use gemini-2.5-flash for speed and cost-efficiency

    def analyze_developer_ads(self, developer: str, raw_ads: List[dict]) -> dict:
        """Analyzes a list of raw ads for a specific developer using Gemini."""
        if not raw_ads:
            logger.info(f"No ads provided for {developer} to analyze.")
            return {}

        logger.info(f"Analyzing {len(raw_ads)} ads for {developer}...")

        # Prepare the prompt
        ads_context = json.dumps(raw_ads, indent=2)
        prompt = f"""
You are an expert digital marketing AI agent specializing in Meta Ads for real estate.
I am providing you with scraped ad data for '{developer}'. 

Your task is to conduct a deep-dive analysis of these ads and extract:
1. Campaign Objective (Inferred: e.g., Lead Gen, Conversions, Awareness)
2. Audience Targeting Strategy (Target Audience, Age Group, Location, Language)
3. Detailed Targeting (Interests, Behaviors, Probable Custom/Lookalike Audiences)
4. Creative & Copy Analysis (Creative Strategy, Ad Copy Structure, Format)
5. Placements (Where the ads are appearing: Stories, Reels, Feed, etc.)
6. Budget & Bidding (Inferred strategy)
7. Pixel & Conversion Tracking (Probable implementation)
8. Funnel Forensic (Stage: TOF/MOF/BOF and Overall Funnel Structure)
9. Ad Details (Headline, CTA, and the direct Ad URL provided in the data)

For each ad in the data, ensure you populate the 'ad_url' field from the source data.
Based on the individual ads, also summarize their overall "Best Ad Strategy".

Raw Ad Data:
{ads_context}
"""

        try:
            # We use Structured Outputs via Pydantic schema
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=DeveloperStrategySummary,
                    temperature=0.2, # Low temperature for more analytical/factual output
                ),
            )
            
            # The response text will be a JSON string matching the DeveloperStrategySummary schema
            return json.loads(response.text)

        except Exception as e:
            logger.error(f"Error during Gemini analysis for {developer}: {e}")
            return {}

class GoogleAdsAnalyzer:
    def __init__(self):
        if not GEMINI_API_KEY:
            logger.warning("GEMINI_API_KEY is not set. Analyzer will fail.")
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_name = "gemini-2.5-flash"

    def analyze_google_strategy(self, developer: str, search_data: dict) -> dict:
        """Analyzes scraped Google Search/Ads data to infer Search Strategy."""
        search_items = search_data.get("search_items", [])
        if not search_items:
            logger.info(f"No Google search items provided for {developer} to analyze.")
            return {}

        logger.info(f"Analyzing {len(search_items)} search items for {developer} to infer Google Ads Strategy...")

        # Prepare the prompt
        search_context = json.dumps(search_items, indent=2)
        prompt = f"""
You are a Senior Google Ads Strategist and PPC Competitor Analyst with 15 years of experience in high-conversion UAE real estate lead generation.

Task: Conduct a deep-dive Google Ads strategy analysis for '{developer}'.
Objective: reverse-engineer their advertising strategy in detail.

I am providing you with scraped Google search results (Ads & Organic) for the developer.
Analyze the data and infer:
1. Core Ad Strategy & Bidding: Probable bidding strategy and budget approach.
2. Keyword Intelligence: Primary (Money), Secondary (Niche), Positive (Quality), and Negative (Excluded) Keywords.
3. Targeting Specifics: Match Types used and Audience Targeting (In-market, Affinities).
4. Ad Copy Analysis: Breakdown of Ad Copy Components (Hooks, Headlines, descriptions).
5. Lead Flow & Conversion: Landing Page analysis and Conversion Tracking implementation.
6. Strategy Summary: A high-level overview of their Google Ads approach.

Raw Search Data:
{search_context}
"""

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=GoogleAdAnalysis,
                    temperature=0.2, # Low temperature for more analytical/factual output
                ),
            )
            return json.loads(response.text)
        except Exception as e:
            logger.error(f"Error during Google Ads Strategy Gemini analysis for {developer}: {e}")
            return {}

class MarketAnalyzer:
    def __init__(self):
        if not GEMINI_API_KEY:
            logger.warning("GEMINI_API_KEY is not set. Analyzer will fail.")
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_name = "gemini-2.5-flash"

    def generate_executive_summary(self, all_meta_analyses: dict, all_google_analyses: dict) -> dict:
        """Generates a high-level executive summary across all developers."""
        logger.info("Generating high-level executive summary...")
        
        combined_context = {
            "meta": {k: v.get("best_ad_strategy") for k, v in all_meta_analyses.items()},
            "google": {k: v.get("strategy_summary") for k, v in all_google_analyses.items()}
        }
        
        prompt = f"""
You are a Senior Growth Marketer specializing in the UAE Real Estate sector.
Based on the following competitor analysis summaries for top developers (Emaar, DAMAC, etc.), provide a high-level executive summary.

Analyze the trends, winning strategies, and notable moves across the market.
Provide actionable recommendations.

Competitor Data:
{json.dumps(combined_context, indent=2)}
"""
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ExecutiveSummary,
                    temperature=0.3,
                ),
            )
            return json.loads(response.text)
        except Exception as e:
            logger.error(f"Error generating executive summary: {e}")
            return {}

if __name__ == "__main__":
    # Test the Meta analyzer
    meta_analyzer = MetaAdsAnalyzer()
    dummy_meta_ads = [
        {
            "ad_id": "12345",
            "developer": "Emaar Properties",
            "ad_text": "Invest in luxury beachfront apartments at Emaar Beachfront. Yields up to 8%...",
            "format": "Image",
            "ctaText": "Learn More"
        }
    ]
    meta_result = meta_analyzer.analyze_developer_ads("Emaar Properties", dummy_meta_ads)
    print(f"Meta Test Analysis Result:\n{json.dumps(meta_result, indent=2)}")
    
    # Test the Google analyzer
    google_analyzer = GoogleAdsAnalyzer()
    dummy_google_search = {
        "developer": "Emaar Properties",
        "search_items": [
            {
                "type": "Sponsored Ad",
                "title": "Emaar Beachfront | Luxury Properties in Dubai",
                "description": "Discover premium waterfront apartments by Emaar. High ROI. Download Brochure.",
                "url": "https://www.emaar.com"
            }
        ]
    }
    google_result = google_analyzer.analyze_google_strategy("Emaar Properties", dummy_google_search)
    print(f"Google Test Analysis Result:\n{json.dumps(google_result, indent=2)}")

