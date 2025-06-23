# Walmart Scraper for Images and Prices

This scraper is using [scrapfly.io](https://scrapfly.io/) and Python to scrape product listing data from Walmart.com. 

The scraping code is located in the `walmart.py` file and scraper run code can be found in `run.py` file.

This scraper scrapes:
- Walmart search pages (search query(product) given)
- Walmart Product pages (scrape the json and fetch image url for download)

For output examples see the `./outputs` directory.


## Setup and Use

This Walmart.com scraper uses __Python 3.11__ with [scrapfly-sdk](https://pypi.org/project/scrapfly-sdk/) package which is used to scrape and parse Walmart's data.

1. Retrieve your Scrapfly API key from <https://scrapfly.io/dashboard> and set `SCRAPFLY_KEY` environment variable:
```shell
    $ export SCRAPFLY_KEY="YOUR SCRAPFLY KEY"
```

2. Run scrape:
    ```shell
    $ python run.py
    ```
