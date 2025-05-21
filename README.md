# Amazon Seller API Data Fetcher

## Overview
This script automates the retrieval of product details using SKUs from the Amazon Selling Partner API and saves them in a structured CSV file. It manages authentication seamlessly by handling token refresh automatically, ensuring uninterrupted data fetching.

## Features
- Reads SKU values from an input CSV file.
- Connects to the Amazon Selling Partner API to extract detailed product information.
- Maintains a logging mechanism for debugging and tracking API requests.
- Stores retrieved product data in a structured CSV format for further analysis.
- Automatically manages API token expiration and refresh to ensure continuous operation.
- Provides robust error handling to prevent data loss or script failure.

## Prerequisites
- Python 3.x installed.
- An active Amazon Selling Partner API account with valid credentials.
- Required API credentials: `CLIENT_ID`, `CLIENT_SECRET`, `REFRESH_TOKEN`, `TOKEN_URL`, `SELLER_APIS`, `MARKETPLACE_ID`, and `SELLER_ID`.
- Necessary Python libraries installed for seamless execution.

## 2.Setup 
    ## Setting Up a Virtual Environment
    Using a virtual environment helps keep dependencies isolated and avoids conflicts. Follow these steps based on your operating system:

    ### Windows
    1. Open Command Prompt and navigate to your project folder:
    ```sh
    cd path/to/your/project
    ```
    2. Create a virtual environment:
    ```sh
    python -m venv venv
    ```
    3. Activate the virtual environment:
    ```sh
    venv\Scripts\activate
    ```
    4. Install dependencies within the virtual environment:
    ```sh
    pip install -r requirements.txt
    ```

    ### Ubuntu/Linux
    1. Open a terminal and navigate to your project folder:
    ```sh
    cd path/to/your/project
    ```
    2. Ensure the `python3-venv` package is installed:
    ```sh
    sudo apt install python3-venv
    ```
    3. Create a virtual environment:
    ```sh
    python3 -m venv venv
    ```
    4. Activate the virtual environment:
    ```sh
    source venv/bin/activate
    ```
    5. Install dependencies within the virtual environment:
    ```sh
    pip install -r requirements.txt
    ```

### 2. Configure Environment Variables
Create a `.env` file in the project directory with the following structure:
```
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
REFRESH_TOKEN=your_refresh_token
TOKEN_URL=api.amazon.com
SELLER_APIS=sellingpartnerapi-eu.amazon.com
MARKETPLACE_ID=your_marketplace_id
SELLER_ID=your_seller_id
```

### 3. Input CSV Format
The script expects an `amazon_listings.csv` file containing SKU values in the following format:
```
sku
12345
67890
ABCDE
```

## Execution
Run the script using the command:
```sh
python script.py
```

## Logging Mechanism
All API interactions, errors, and execution logs are stored in `storage/logs/YYYY-MM-DD/log.txt`, ensuring transparency and easy debugging.

## Output Data
The output CSV file `amazon_data_output.csv` contains the retrieved product details, structured for further analysis and integration.

## Error Handling
- Logs all API request failures with detailed error messages.
- Automatically refreshes expired tokens to prevent authentication failures.
- Skips invalid or missing data to ensure continuous execution without disruptions.



## License
This project is intended for internal use and testing purposes only. Redistribution or commercial use without proper authorization is prohibited.

## Author
Developed by [Your Name / Company]. For inquiries, please contact [your email or website].

