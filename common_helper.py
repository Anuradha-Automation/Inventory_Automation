import json
import urllib.parse
def read_json_file(file_name):
    """Loads the stored token from a file."""
    try:
        with open(file_name, "r") as f:
            return json.load(f)  # Read and parse JSON
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None
    
def decode_url(encoded_url):
    return urllib.parse.unquote(encoded_url)
def extract_login_code(current_url):
    """
    Extracts and decodes the authorization code from the eBay login redirect URL.

    :param current_url: The redirected URL after eBay login.
    :return: The extracted and decoded authorization code.
    """
    parsed_url = urllib.parse.urlparse(current_url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    if "code" in query_params:
        encoded_code = query_params["code"][0]  # Extract the first value from the list
        expires_in = query_params["expires_in"][0]  # Extract the first value from the list
        decoded_code = urllib.parse.unquote(encoded_code)  # Decode the URL-encoded value
        return encoded_code,decoded_code
    else:
        return None,None