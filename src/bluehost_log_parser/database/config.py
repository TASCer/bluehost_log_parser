import os

from dotenv import load_dotenv

load_dotenv()

# CREDS
DB_HOSTNAME: str = f"{os.environ['DB_HOST']}"
DB_NAME: str = f"{os.environ['DB_NAME']}"
DB_USER: str = f"{os.environ['DB_USER']}"
DB_PASSWORD: str = f"{os.environ['DB_USER_PASS']}"
DB_URI = f"{DB_USER}:{DB_PASSWORD}@{DB_HOSTNAME}/{DB_NAME}"
# TABLES
COUNTRIES_TABLE: str = "countries"
SOURCES_TABLE: str = "sources"
VIEW_COUNTRY_ACTIVITY = "country_activity"
PUBLIC_LOGS_TABLE = "public_logs"
SOHO_LOGS_TABLE: str = "soho_logs"
SOURCES_TABLE: str = "sources"
VIEW_COUNTRY_ACTIVITY = "country_activity"
VIEW_SOHO_NON_200_RESP = "soho_non_200_reponse"
