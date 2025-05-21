import pandas as pd
from config.config import INPUT_CSV
from services.amazon_seller_sync import fetch_product_details_from_amazon_by_sku, update_amazon_product
from services.eBayProductUpdateService import get_ebay_product_quantity_by_item_id, update_ebay_listing_quantity
from config.logger_config import setup_logger

logger = setup_logger()

def syncAmazonEbayInventory(csv_file_name):
    df = pd.read_csv(csv_file_name)
    logger.info("CSV file loaded successfully.\n")
    
    results = [] 
    
    for index, row in df.iterrows():
        
        logger.info(f"\n🔍 Processing Product {index + 1}/{len(df)} | Managing Inventory... \n")
        item_uuid = row["Item ID"]
        amazon_sku = row["Amazon sku"]
        
        logger.info(f"Fetching details for item_uuid via Ebay : {item_uuid}")
        
        try:
            EbayQuantity = get_ebay_product_quantity_by_item_id(item_uuid)
            if EbayQuantity is None:
                logger.info(f"Error: No quantity found for item {item_uuid} on eBay.")
                continue
            logger.info(f"Fetched Ebay Quantity for item ID  {item_uuid}:-->> {EbayQuantity} \n")
            
            logger.info(f"Fetching details for Amazon SKU via Amazon Seller API: {amazon_sku}")
            amazon_quantity = fetch_product_details_from_amazon_by_sku(amazon_sku)
            if amazon_quantity is None:
                logger.info(f"Error: No quantity found for SKU {amazon_sku} on Amazon.")
                continue
            logger.info(f"Fetched Amazon Quantity for SKU {amazon_sku}: {amazon_quantity}" )
            
            res ={"sku": amazon_sku, "status": "success", "message": f""}
           
            if int(EbayQuantity) == int(amazon_quantity):
                logger.info(f"\n✅ Inventory Synced: {amazon_sku} ({item_uuid}) ✅\n--- Moving to next product ---\n")
                res = {"sku": amazon_sku, "status": "success", "message": "Inventory already synced between Amazon and eBay."}
            
            elif int(EbayQuantity) > int(amazon_quantity):
                logger.info(f"Updating Ebay Listing for item {item_uuid} ({amazon_sku}).")
                logger.info(f"📦 Amazon Quantity: {amazon_quantity} | 🛒 eBay Quantity: {EbayQuantity} ➡️ Updating eBay listing...")
                
                res = update_ebay_listing_quantity(amazon_quantity, str(item_uuid))
                logger.info('Updated Ebay:', res)
                
            else:
                logger.info(f"Updating Amazon  Listing for item {item_uuid} ({amazon_sku}).")
                logger.info(f"📦 Amazon Quantity: {amazon_quantity} | 🛒 eBay Quantity: {EbayQuantity} ➡️ Updating Amazon seller listing...")
                
                res = update_amazon_product(EbayQuantity,amazon_sku)
                logger.info('Updated Amazon :', res)

            results.append(res)  
        except Exception as e:
            logger.info(f"Error processing item {item_uuid} with Amazon SKU {amazon_sku}: {str(e)}")
            results.append({"sku": amazon_sku, "status": "Failed", "message": f"Error: {str(e)}"})

    # Final status check
    if all(res["status"] == "Failed" for res in results):
        return False, results  # If all items failed
    return True, results  # If at least one item was successful

if __name__ == "__main__":
    status, response = syncAmazonEbayInventory(INPUT_CSV)
    if not status:
        logger.info('Something went wrong:')
    for res in response:
        logger.info(res.get('message', 'No message available'))
