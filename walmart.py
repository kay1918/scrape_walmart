# walmart.py
import os
import json
import string
from scrapfly import ScrapeConfig, ScrapflyClient, ScrapeApiResponse
from typing import Dict, List, TypedDict
import pandas as pd

scrapfly_key = 'scp-live-9c54a3a13fd049639946db64eabde488' #get own key from scrapfly
SCRAPFLY = ScrapflyClient(key=scrapfly_key)
BASE_CONFIG = {"asp": True, "country": "US", "proxy_pool": "public_residential_pool", "render_js": True}
'''
SCRAPFLY = ScrapflyClient(key=os.environ["SCRAPFLY_KEY"])
'''

def parse_product(response:ScrapeApiResponse):
    try:
        sel = response.selector
        raw = json.loads(sel.xpath('//script[@id="__NEXT_DATA__"]/text()').get())
    except Exception as e:
        print(f"Error parsing product: {e}")
        return {}

    try:
        product = raw["props"]["pageProps"]["initialData"]["searchResult"]["itemStacks"][0]["items"][0]

        name_info = product['name']
        id_info = product['usItemId']
        image_info = product['imageInfo']['thumbnailUrl']
        price_info = product['priceInfo']['linePrice']
        product_info = {"name": name_info,
            "product_id": id_info,
            "product_url": f"https://www.walmart.com/ip/{id_info}",
            "price_info": price_info,
            "image_info": image_info}

        return product_info

    except Exception as e:
        return {"error": str(e)}

def scrape_search_product(product: string) -> Dict:
    results = []
    search_walmart= "https://www.walmart.com/search?q="
    if pd.isna(product):  # Skip if product is NaN
        return {}
    print(f"Scraping {product}")
    config = ScrapeConfig(search_walmart+product+"&page=1", **BASE_CONFIG)
    response = SCRAPFLY.scrape(config)
    product_info = parse_product(response)
    return product_info

def data_to_csv(results:List[Dict]):

  df = pd.DataFrame(results)
  df = df[['product_id', 'name', 'product_url','price_info', 'image_info']]
  output_path = "/result/walmart_products.xlsx"  # This saves under the result directory
  df.to_excel(output_path, index=False)