import json
from pathlib import Path
import walmart
import pandas as pd

'''
assert "SCRAPFLY_KEY" in os.environ, "Please set SCRAPFLY_KEY environment variable."
'''

def run():
    print("running Walmart scrape and saving results to ./ouput directory")
    ### Change the file name to the name of the file you want to scrape 
    df= pd.read_excel("short_data.xlsx")# Load the Excel file 
    df = df.dropna(subset=["id", "product_name"])
    # Convert to dictionary
    product_dict = dict(zip(df['id'], df['product_name']))
    price_info_list = []
    for id, url in product_dict.items():
        product_info = walmart.scrape_search_product(url)
        try:
            image_info = product_info['image_info']
            price = product_info.get('price_info', None)
            walmart.download_image(image_info, f'{id}.png')
            price_info_list.append(price)
        except:
            print(f"product {id} not found")
            price_info_list.append(0)

    df['price_info'] = price_info_list
    # Save to a new Excel file
    df.to_excel("walmart_products_withprice.xlsx", index=False)
    print("Price info saved to walmart_products_withprice.xlsx")
    
if __name__ == "__main__":
    run()

