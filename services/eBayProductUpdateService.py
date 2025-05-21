import json
import time
import requests
import urllib
import xml.etree.ElementTree as ET
import logging
from common_helper import read_json_file
from config.config import EBAY_API_URL, EBAY_BASE_64_ENCODE_CODE, EBAY_CLIENT_ID, EBAY_CLIENT_SECRET, EBAY_DEV_ID, EBAY_OAUTH_ACCESS_TOKEN_JSON, EBAY_OAUTH_REFRESH_TOKEN_JSON, EBAY_SCOPES, EBAY_TOKEN_URL
from config.logger_config import setup_logger
from ebaysdk.trading import Connection as Trading
# Setup logger with rotating file handler
# Initialize logger
logger = setup_logger()


def retrieve_fresh_refresh_token(refresh_token_file):
    logger.info("--------->>retrieve_fresh_refresh_token called")
    refresh_token_data = read_json_file(refresh_token_file)
    
    if refresh_token_data:
        logger.info("The refresh token is found in the refresh_token_file. Checking validity of the token.")
        refresh_token_expire_time = refresh_token_data.get("refresh_token_expires_in", 0)
        
        if int(time.time()) >= refresh_token_expire_time:
            logger.info('Refresh token is valid')
            return refresh_token_data.get("refresh_token", "")
        else:
            logger.warning('Refresh token has expired. Not generating a new refresh token.')
            return ""
    else:
        logger.error("The refresh token is not found in the refresh_token_file. Generating a new refresh token via login.")
        return ""


def generate_access_token_via_refresh_token(refresh_token, access_token_file):
    logger.info("------------>>generate_access_token_via_refresh_token function is called")
    encoded_payload = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "scope": EBAY_SCOPES
    })
    
    logger.debug(f"Encoded Payload: {encoded_payload}")
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {EBAY_BASE_64_ENCODE_CODE}'
    }
    
    logger.debug(f"Headers: {headers}")
    
    response = requests.post(EBAY_TOKEN_URL, data=encoded_payload, headers=headers)
    
    logger.debug(f"Response Status Code: {response.status_code}")
    
    if response.status_code == 200:
        with open(access_token_file, "w") as f:
            json.dump(response.json(), f, indent=4)
        logger.info("Access token generated and saved.")
        return response.json()
    else:
        logger.error(f"Failed to generate access token. Status Code: {response.status_code}")
        logger.debug(f"Response Body: {response.text}")
        return None


def generate_ebay_access_token():
    logger.info("------->>>>generate_ebay_access_token function called")
    access_token_data = read_json_file(EBAY_OAUTH_ACCESS_TOKEN_JSON)
    
    if access_token_data:
        logger.info(f'Access token found in the {EBAY_OAUTH_ACCESS_TOKEN_JSON} file.')
        return access_token_data.get("access_token", "")
    else:
        logger.warning(f'Access token not found in the {EBAY_OAUTH_ACCESS_TOKEN_JSON} file. Generating via refresh token.')
        refresh_token = retrieve_fresh_refresh_token(EBAY_OAUTH_REFRESH_TOKEN_JSON)
        if refresh_token:
            logger.info(f'Refresh token found: {refresh_token}')
            access_token = generate_access_token_via_refresh_token(refresh_token, EBAY_OAUTH_ACCESS_TOKEN_JSON)
            if access_token:
                return access_token.get("access_token", "")
        return ""


def get_ebay_product_quantity_by_item_id(item_id):
    logger.info(f"Fetching product quantity for ItemID: {item_id}")
    access_token = generate_ebay_access_token()
    if not access_token:
        logger.error("No access token found. Aborting request.")
        return ""

    url = f"{EBAY_API_URL}/ws/api.dll"
    logger.debug(f"eBay API URL: {url}")

    headers = {
        "X-EBAY-API-COMPATIBILITY-LEVEL": "967",
        "X-EBAY-API-CALL-NAME": "GetItem",
        "X-EBAY-API-SITEID": "3", 
        "Content-Type": "text/xml"
    }

    xml_payload = f"""<?xml version="1.0" encoding="utf-8"?>
    <GetItemRequest xmlns="urn:ebay:apis:eBLBaseComponents">
        <RequesterCredentials>
            <eBayAuthToken>{access_token}</eBayAuthToken>  
        </RequesterCredentials>
        <ItemID>{item_id}</ItemID>
    </GetItemRequest>
    """
    

    logger.debug(f"XML Payload: {xml_payload}")

    response = requests.post(url, data=xml_payload, headers=headers)
    
    logger.debug(f"Response Status Code: {response.status_code}")
    
    if response.status_code == 200:
        root = ET.fromstring(response.text)
        logger.debug("Parsing response XML")
        quantity = root.find(".//{urn:ebay:apis:eBLBaseComponents}Quantity")
        product_details = quantity.text if quantity is not None else ""
        return product_details
    else:
        logger.error(f"Failed to fetch product details for ItemID {item_id}. Status Code: {response.status_code}")
        logger.debug(f"Response Body: {response.text}")
        return ""


def update_ebay_listing_quantity(quantity,item_id):
    logger.info(f"Updating eBay Listing Quantity for ItemID: {item_id} with quantity: {quantity}")
    access_token = generate_ebay_access_token()
    if not access_token:
        logger.error("No access token found. Aborting request.")
        return {"item_id": item_id, "status": "failed", "message": "Access token is missing."}

    try:
        api = Trading(domain="api.ebay.com", 
                      config_file=None,
                      appid=EBAY_CLIENT_ID,
                      certid=EBAY_CLIENT_SECRET,
                      devid=EBAY_DEV_ID,
                      token=access_token)
        
        item_data = {
            "Item": {
                "ItemID": item_id
            }
        }
        if quantity:
            item_data["Item"]["Quantity"] = quantity

        logger.debug(f"Item Data for Revision: {item_data}")
        response = api.execute("ReviseItem", item_data)
        
        logger.info("Item Revised Successfully.")
        logger.debug(f"Response: {response.dict()}")

        return {"item_id": item_id, "status": "success", "message": "Item Revised Successfully"}
    
    except ConnectionError as e:
        logger.error(f"Error updating item {item_id}: {str(e)}")
        return {"item_id": item_id, "status": "failed", "message": f"Error: {str(e)}"}
