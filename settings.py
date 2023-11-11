import os
from dotenv import load_dotenv
load_dotenv()

class AppSettings:
    url_scrapping_api: str = os.environ.get('URL_SCRAPING_API', None)