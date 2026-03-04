# UAE Real Estate Ads Competitor Intelligence Agent

An AI-powered marketing agent that scrapes Meta and Google Ads from top UAE real estate developers and analyzes their strategies using Gemini AI.

## Features
- **Meta Ads Scraping**: Uses Scrapingdog to fetch active ads from Facebook and Instagram.
- **Google Ads Intelligence**: Scrapes Google Search results to analyze competitor PPC strategies.
- **AI Analysis**: Leverages Google Gemini (2.5-flash) to infer hooks, value propositions, and creative formats.
- **Automated Reporting**: Generates HTML reports and sends them via email.
- **Live Dashboard**: Built with Streamlit for easy interaction.

## Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd "Markting Agent"
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Create a `.env` file in the root directory with the following:
   ```env
   SCRAPINGDOG_API_KEY=your_scrapingdog_key
   GEMINI_API_KEY=your_gemini_key
   SENDER_EMAIL=your_email@gmail.com
   SENDER_PASSWORD=your_app_password
   RECEIVER_EMAIL=recipient@example.com
   ```

5. **Run the Dashboard**:
   ```bash
   streamlit run app.py
   ```

## Technologies Used
- **Python**: Core logic.
- **Streamlit**: Web interface.
- **Scrapingdog**: Web scraping API.
- **Google Gemini**: AI analysis.
- **Pandas**: Data handling.
- **SMTP**: Email reporting.
