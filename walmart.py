# walmart.py
import os
import json
import string
from scrapfly import ScrapeConfig, ScrapflyClient, ScrapeApiResponse
from typing import Dict, List, TypedDict
import pandas as pd
import requests

scrapfly_key = 'scp-live-9c54a3a13fd049639946db64eabde488' #get own key from scrapfly
SCRAPFLY = ScrapflyClient(key=scrapfly_key)
BASE_CONFIG = {"asp": True, "country": "US", "proxy_pool": "public_residential_pool", "render_js": True}
'''
SCRAPFLY = ScrapflyClient(key=os.environ["SCRAPFLY_KEY"])
'''

def parse_product(response:ScrapeApiResponse):
    sel = response.selector
    raw = json.loads(sel.xpath('//script[@id="__NEXT_DATA__"]/text()').get())

    try:
        product = raw["props"]["pageProps"]["initialData"]["searchResult"]["itemStacks"][0]["items"][0]
        price_info = product['priceInfo']['linePrice']
        image_info = product['imageInfo']['thumbnailUrl']
        product_info = {"price_info": price_info,
            "image_info": image_info}
        '''name_info = product['name']
        id_info = product['usItemId']
        price_info = product['priceInfo']['linePrice']
        product_info = {"name": name_info,
            "product_id": id_info,
            "product_url": f"https://www.walmart.com/ip/{id_info}",
            "price_info": price_info,
            "image_info": image_info}'''
        return product_info
    
    except Exception as e:
        return {"error": str(e)}

def scrape_search_product(url: str) -> Dict:
    search_walmart= "https://www.walmart.com/search?q="
    config = ScrapeConfig(search_walmart+url+"&page=1", **BASE_CONFIG)
    print(f"Scraping {url}")
    try:
        response = SCRAPFLY.scrape(config)
        product_info = parse_product(response)
        return product_info
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return {}

def download_image(image_info, save_as):
    try:
      os.makedirs("output", exist_ok=True)
      response = requests.get(image_info)
      with open(f"output/"+save_as, 'wb') as file:
          file.write(response.content)
          print(save_as + " image file saved")
    except Exception as e:
        print(save_as + " image not found")
        return {"error": str(e)}

'''def data_to_csv(results:List[Dict]):
  df = pd.DataFrame(results)
  df = df[['product_id', 'name', 'product_url','price_info', 'image_info']]
  output_path = "/result/walmart_products.xlsx"  # This saves under the result directory
  df.to_excel(output_path, index=False)'''