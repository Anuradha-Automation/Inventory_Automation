import os
from dotenv import load_dotenv
load_dotenv()
# Load environment variables fOR Amazon Seller Services 
CLIENT_ID = os.getenv('CLIENT_ID', '')
CLIENT_SECRET = os.getenv('CLIENT_SECRET', '')
EBAY_DEV_ID  = os.getenv('EBAY_DEV_ID ', '')
REFRESH_TOKEN = os.getenv('REFRESH_TOKEN', '')
TOKEN_URL = os.getenv('TOKEN_URL', '')
SELLER_APIS = os.getenv('SELLER_APIS', '')
MARKETPLACE_ID = os.getenv('MARKETPLACE_ID', '')
SELLER_ID = os.getenv('SELLER_ID', '')
AMAZON_TOKEN_FOLER = f"storage/token/amazon"
os.makedirs(AMAZON_TOKEN_FOLER, exist_ok=True)
AMAZON_OAUTH_REFRESH_TOKEN_JSON = os.path.join(AMAZON_TOKEN_FOLER, "token_refresh_token.json")
AMAZON_OAUTH_ACCESS_TOKEN_JSON = os.path.join(AMAZON_TOKEN_FOLER, "token_access_token.json")

# Load environment variables fOR Ebey
EBAY_CLIENT_ID = os.getenv('EBAY_CLIENT_ID', '')
EBAY_CLIENT_SECRET = os.getenv('EBAY_CLIENT_SECRET', '')
EBAY_TOKEN_URL: str = os.getenv('EBAY_TOKEN_URL', '')
EBAY_SCOPES = os.getenv('EBAY_SCOPES', '')
EBEY_TOKEN_FILE = os.getenv('EBEY_TOKEN_FILE', '')
EBAY_API_URL = os.getenv('EBAY_API_URL', '')
EBEY_EXPIRE_TOKEN = os.getenv('EBEY_EXPIRE_TOKEN', '')
EBEY_USERNAME = os.getenv('EBEY_USERNAME', '')
EBEY_PASSWORD = os.getenv('EBEY_PASSWORD', '')
EBEY_AUTH_URL = os.getenv('EBEY_AUTH_URL', '')
EBEY_REDIRECT_URL = os.getenv('EBEY_REDIRECT_URL', '')
EBAY_BASE_64_ENCODE_CODE = os.getenv('EBAY_BASE_64_ENCODE_CODE', '')
LOGIN_URL = f"{EBEY_AUTH_URL}?client_id={EBAY_CLIENT_ID}&response_type=code&redirect_uri={EBEY_REDIRECT_URL}&scope={EBAY_SCOPES}"
EBAY_TOKEN_FOLER = f"storage/token/ebay"
os.makedirs(EBAY_TOKEN_FOLER, exist_ok=True)
EBAY_OAUTH_REFRESH_TOKEN_JSON = os.path.join(EBAY_TOKEN_FOLER, "token_refresh_token.json")
EBAY_OAUTH_ACCESS_TOKEN_JSON = os.path.join(EBAY_TOKEN_FOLER, "token_access_token.json")

INPUT_CSV = 'common_sku_item_Id.csv'


# LOG DIRECTORY
LOG_DIR = f"storage/logs/"
LOG_FILE = os.path.join(LOG_DIR, "log.txt")
os.makedirs(LOG_DIR, exist_ok=True)
UPDATE_FOLDER = f"storage/data/"
os.makedirs(UPDATE_FOLDER, exist_ok=True)



# Automation Configrations 

HEADLESS= True
UC = True