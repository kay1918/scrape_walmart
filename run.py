import asyncio
import json
from pathlib import Path
import walmart
import pandas as pd

output = Path(__file__).parent / "results"
output.mkdir(exist_ok=True)

'''
assert "SCRAPFLY_KEY" in os.environ, "Please set SCRAPFLY_KEY environment variable."
'''

def run():
    print("running Walmart scrape and saving results to ./results directory")
    df= pd.read_excel("raw_data_copy.xlsx")
    product_names = df['product_name']
    products_data = walmart.scrape_search_products(product_names)
    walmart.data_to_csv(products_data)

if __name__ == "__main__":
    run()

