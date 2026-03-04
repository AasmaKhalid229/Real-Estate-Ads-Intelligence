import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

from config import SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ReportGenerator:
    def format_html_report(self, all_meta_analyses: dict, all_google_analyses: dict, executive_summary: dict = None) -> str:
        """Formats the AI analyses into an HTML report."""
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 1200px; margin: 0 auto; padding: 20px; }}
                h1 {{ color: #2C3E50; border-bottom: 3px solid #3498DB; padding-bottom: 10px; text-align: center; }}
                h2 {{ color: #E67E22; margin-top: 40px; border-bottom: 2px solid #eee; padding-bottom: 5px; background: #fdf2e9; padding: 10px; border-radius: 5px; }}
                h3 {{ color: #2980B9; margin-top: 20px; margin-bottom: 10px; border-left: 5px solid #2980B9; padding-left: 10px; }}
                table {{ border-collapse: collapse; width: 100%; margin-top: 15px; margin-bottom: 25px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
                th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; font-size: 13px; }}
                th {{ background-color: #34495E; color: white; font-weight: bold; position: sticky; top: 0; }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
                .exec-summary {{ background-color: #f4f6f7; border: 2px solid #3498DB; padding: 20px; border-radius: 8px; margin-bottom: 30px; }}
                .strategy-box {{ background-color: #E8F8F5; padding: 15px; border-radius: 5px; margin-bottom: 15px; border-left: 5px solid #1ABC9C; }}
                .google-box {{ background-color: #FDEDEC; padding: 15px; border-radius: 5px; margin-bottom: 15px; border-left: 5px solid #E74C3C; }}
                .tag {{ display: inline-block; background: #eee; padding: 2px 8px; border-radius: 10px; font-size: 11px; margin-right: 5px; }}
                .url-link {{ color: #3498DB; text-decoration: none; font-size: 11px; word-break: break-all; }}
            </style>
        </head>
        <body>
            <h1>Weekly Digital Ads Competitor Intelligence ({today})</h1>
        """

        if executive_summary:
            html += f"""
            <div class="exec-summary">
                <h2 style="margin-top:0; background:none; border:none; color:#2C3E50;">Market Executive Summary</h2>
                <p><strong>Overall Trends:</strong> {executive_summary.get('overall_market_trends', 'N/A')}</p>
                <p><strong>Top Winning Strategies:</strong></p>
                <ul>
                    {"".join([f"<li>{s}</li>" for s in executive_summary.get('top_3_winning_strategies', [])])}
                </ul>
                <p><strong>Competitor Moves:</strong> {executive_summary.get('notable_competitor_moves', 'N/A')}</p>
                <p><strong>Strategic Recommendations:</strong> {executive_summary.get('recommendations', 'N/A')}</p>
            </div>
            """
        
        all_developers = sorted(set(list(all_meta_analyses.keys()) + list(all_google_analyses.keys())))
        
        for dev in all_developers:
            meta_res = all_meta_analyses.get(dev, {})
            google_res = all_google_analyses.get(dev, {})
            
            if not meta_res and not google_res:
                continue
                
            html += f"<h2>{dev}</h2>"
            
            # --- Meta Ads HTML ---
            if meta_res:
                html += f"<h3>Meta Ads Strategy</h3>"
                best_strategy = meta_res.get("best_ad_strategy", "N/A")
                html += f"<div class='strategy-box'><strong>Core Strategy:</strong> {best_strategy}</div>"
                
                ad_analyses = meta_res.get("ad_analyses", [])
                if ad_analyses:
                    html += """
                    <table>
                        <tr>
                            <th>Format & URL</th>
                            <th>Headline & CTA</th>
                            <th>Funnel & Platform</th>
                            <th>Target Audience & Age</th>
                            <th>Interests & Behaviors</th>
                            <th>Strategy Summary</th>
                        </tr>
                    """
                    for ad in ad_analyses[:5]: # Show top 5
                        html += f"""
                        <tr>
                            <td style="min-width:150px;">
                                <strong>{ad.get('format', 'N/A')}</strong> ({ad.get('campaign_objective', 'N/A')})<br>
                                <a href="{ad.get('ad_url', '#')}" class="url-link" target="_blank">View Ad</a><br>
                                <small>Placements: {ad.get('placements', 'N/A')}</small>
                            </td>
                            <td>
                                <strong>Headline/Copy Structure:</strong> {ad.get('ad_copy_structure', 'N/A')}<br>
                                <span class="tag">CTA: {ad.get('cta', 'N/A')}</span>
                            </td>
                            <td>
                                <strong>{ad.get('funnel_stage', 'N/A')}</strong><br>
                                <small>{ad.get('funnel_structure', 'N/A')}</small><br>
                                <small>Tracking: {ad.get('pixel_conversion_tracking', 'N/A')}</small>
                            </td>
                            <td>
                                {ad.get('target_audience', 'N/A')}<br>
                                <span class="tag">Age: {ad.get('age_group_target', 'N/A')}</span><br>
                                <small>Loc: {ad.get('location', 'N/A')} ({ad.get('language', 'N/A')})</small>
                            </td>
                            <td>
                                <small><strong>Int:</strong> {ad.get('detailed_interests', 'N/A')}</small><br>
                                <small><strong>Beh:</strong> {ad.get('detailed_behaviors', 'N/A')}</small><br>
                                <small><strong>LAL/Custom:</strong> {ad.get('lookalike_audience', 'N/A')} / {ad.get('custom_audience', 'N/A')}</small>
                            </td>
                            <td>
                                <strong>Creative:</strong> {ad.get('creative_strategy', 'N/A')}<br>
                                <strong>Bidding:</strong> {ad.get('budget_bidding', 'N/A')}
                            </td>
                        </tr>
                        """
                    html += "</table>"
            
            # --- Google Ads HTML ---
            if google_res:
                html += f"<h3>Google Ads Strategy</h3>"
                core_strategy = google_res.get("core_ad_strategy", "N/A")
                
                primary = ", ".join(google_res.get("primary_keywords", []))
                secondary = ", ".join(google_res.get("secondary_keywords", []))
                positive = ", ".join(google_res.get("positive_keywords", []))
                negative = ", ".join(google_res.get("predicted_negative_keywords", []))
                
                html += f"""
                <div class='google-box'>
                    <p><strong>Strategy Summary:</strong> {google_res.get('strategy_summary', 'N/A')}</p>
                    <p><strong>Core Bidding Strategy:</strong> {core_strategy}</p>
                    <table>
                        <tr><th>Primary Keywords</th><td>{primary}</td></tr>
                        <tr><th>Secondary Keywords</th><td>{secondary}</td></tr>
                        <tr><th>Positive Keywords</th><td>{positive}</td></tr>
                        <tr><th>Negative Keywords</th><td>{negative}</td></tr>
                        <tr><th>Match Types</th><td>{google_res.get('match_types', 'N/A')}</td></tr>
                        <tr><th>Audience Targeting</th><td>{google_res.get('audience_targeting', 'N/A')}</td></tr>
                        <tr><th>Ad Copy Components</th><td>{google_res.get('ad_copy_components', 'N/A')}</td></tr>
                        <tr><th>Landing Page Analysis</th><td>{google_res.get('landing_page', 'N/A')}</td></tr>
                        <tr><th>Budget & Bidding Details</th><td>{google_res.get('budget_bidding_strategy', 'N/A')}</td></tr>
                        <tr><th>Conversion Tracking</th><td>{google_res.get('conversion_tracking', 'N/A')}</td></tr>
                    </table>
                </div>
                """
                
        html += "</body></html>"
        return html

    def send_email_report(self, html_content: str):
        """Sends the HTML report via email and saves it locally."""
        
        # --- NEW: Save HTML locally for user visibility ---
        # --- Save reports locally ---
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        latest_filename = "latest_report.html"
        timestamped_filename = f"report_{timestamp}.html"
        
        try:
            # Save as latest
            with open(latest_filename, "w", encoding="utf-8") as f:
                f.write(html_content)
            # Save with timestamp
            with open(timestamped_filename, "w", encoding="utf-8") as f:
                f.write(html_content)
                
            abs_path = os.path.abspath(latest_filename)
            logger.info(f"HTML report saved locally to: {abs_path}")
            print(f"\n[SUCCESS] Report stored at: {abs_path}")
            print(f"[SUCCESS] Timestamped copy stored as: {timestamped_filename}")
        except Exception as e:
            logger.error(f"Failed to save local HTML report: {e}")

        if not SENDER_EMAIL or not SENDER_PASSWORD or not RECEIVER_EMAIL:
            logger.error("Email credentials not fully configured in environment. Skipping email.")
            print("[WARNING] Email credentials not set. Skipping email notification.")
            return

        logger.info(f"Sending Weekly Intelligence email to {RECEIVER_EMAIL}...")
        print(f"[INFO] Sending report email to {RECEIVER_EMAIL}...")
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"Weekly Digital Ads Competitor Intelligence - {datetime.now().strftime('%Y-%m-%d')}"
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL

        part = MIMEText(html_content, 'html')
        msg.attach(part)

        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.ehlo() # Explicitly identify ourselves to the server
                server.starttls()
                server.ehlo() # Re-identify after encryption
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
            logger.info("Email sent successfully!")
            print("[SUCCESS] Email sent successfully!")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            print(f"[ERROR] Failed to send email: {e}")

if __name__ == "__main__":
    # Test Report Generator
    reporter = ReportGenerator()
    dummy_data = {
        "Emaar Properties": {
            "developer": "Emaar Properties",
            "best_ad_strategy": "Highlighting luxury waterfront living with high ROI.",
            "ad_analyses": [
                {
                    "format": "Video",
                    "headline": "Own a piece of the shoreline",
                    "cta": "Learn More",
                    "funnel_stage": "Top of Funnel",
                    "targeting_platform": "Facebook, Instagram",
                    "target_audience": "High Net Worth Individuals / Investors",
                    "age_group_target": "35-65",
                    "post_summary": "Video showcasing beachfront apartments at Emaar Beachfront."
                }
            ]
        }
    }
    html = reporter.format_html_report(dummy_data, {})
    # Uncomment to test actual sending (needs valid credentials)
    # reporter.send_email_report(html)
    print("Report HTML generated successfully. Length:", len(html))
