import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
SCRAPINGDOG_API_KEY = os.getenv("SCRAPINGDOG_API_KEY", "")
APIFY_API_KEY = os.getenv("APIFY_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")


# Email Settings
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL", "")

# Target Developers
TARGET_DEVELOPERS = [
    "Emaar Properties",
    "DAMAC Properties",
    "Nakheel",
    "Sobha Realty",
    "Aldar Properties",
    "Binghatti Developers",
    "Meraas",
    "Dubai Properties",
    "Azizi Developments",
    "Danube Properties"
]
