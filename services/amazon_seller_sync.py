
import http
import json
import time
import urllib
from config.config import AMAZON_OAUTH_ACCESS_TOKEN_JSON, CLIENT_ID, CLIENT_SECRET, MARKETPLACE_ID, REFRESH_TOKEN, SELLER_APIS, SELLER_ID, TOKEN_URL


def get_token():
    """Refreshes the access token by making a POST request to the token URL."""
    try:
        print("Refreshing token...")
        conn = http.client.HTTPSConnection(TOKEN_URL)
        payload = f"client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&refresh_token={REFRESH_TOKEN}&grant_type=refresh_token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        conn.request("POST", "/auth/o2/token", payload, headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        token_data = json.loads(data)
        token_data["expires_at"] = time.time() + token_data["expires_in"]
        with open(AMAZON_OAUTH_ACCESS_TOKEN_JSON, "w") as f:
            json.dump(token_data, f)
        print("✅ Token refreshed successfully.")
        return token_data
    except Exception as e:
        print(f"⚠️ Error refreshing token: {e}")
        return None

def load_token():
    """Loads the stored token from a file named 'token.txt'."""
    try:
        with open(AMAZON_OAUTH_ACCESS_TOKEN_JSON, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(" Token file not found.")
        return None

def get_valid_token():
    """Retrieves a valid access token, refreshing it if necessary."""
    token_data = load_token()
    if not token_data or time.time() >= token_data.get("expires_at", 0):
        return get_token()
    return token_data

def fetch_product_details_from_amazon_by_sku(sku_id):
    access_token = get_valid_token()["access_token"]
    # print('access_token', access_token)
    conn = http.client.HTTPSConnection(SELLER_APIS)
    headers = {"x-amz-access-token": access_token, "Content-Type": "application/json"}
    # print('headers', headers)
    encoded_sku = urllib.parse.quote(sku_id)
    url = f"/listings/2021-08-01/items/{SELLER_ID}/{encoded_sku}?marketplaceIds={MARKETPLACE_ID}&issueLocale=en_US&includedData=summaries,attributes,issues,offers,fulfillmentAvailability,procurement,relationships,productTypes"
    conn.request("GET", url, "", headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    json_data = json.loads(data)
    with open('AMAZON_OAUTH_ACCESS_TOKEN_JSON.json', "w") as f:
            json.dump(json_data, f)
    fulfillmentAvailability = json_data.get("fulfillmentAvailability", [])
    return str(fulfillmentAvailability[0].get("quantity", '0'))

def update_amazon_product(new_quantity,sku):
    try:
        conn = http.client.HTTPSConnection(SELLER_APIS)
        access_token = get_valid_token()["access_token"]
        # print('access_token', access_token)
        headers = {
            "x-amz-access-token": access_token,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        print(f" Updating quantity for SKU: {sku} to {new_quantity}")
        update_data = {
            "productType":"GUILD_HOME",
            "patches": [
                {
                    "op": "replace",
                     "path": "/attributes/fulfillment_availability",
                    "value": [
                        {
                            "fulfillment_channel_code": "DEFAULT",  
                            "quantity": new_quantity,
                            "marketplaceId": MARKETPLACE_ID
                        }
                    ]
                }
            ]
        }
        encoded_sku = urllib.parse.quote(sku)
        url = f"/listings/2021-08-01/items/{SELLER_ID}/{encoded_sku}?marketplaceIds={MARKETPLACE_ID}"
        request_body = json.dumps(update_data)
        conn.request("PATCH", url, body=request_body, headers=headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        json_data = json.loads(data)
        print(f"Update response: {json_data}")
        if "errors" in json_data:
            return {"sku": sku, "status": "Failed", "message": json_data["errors"][0]["message"]}
        
        return {"sku": sku, "status": "Success", "message": "Product updated successfully"}
    except Exception as e:

        return {"sku": sku, "status": "Failed", "message": str(e)}
    
