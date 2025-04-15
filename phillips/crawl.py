import xml.etree.ElementTree as ET
import requests
import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

from utils import match_str

class PhillipsCrawler:
    SITEMAP_URL = "https://www.phillips.com/sitemap.xml"
    FILTER_URLS = ["/auction/"]
    ITEM_SCHEMA = {
        "name": "PHILLIPS Items",
        "baseSelector": "div.seldon-grid-item",
        "fields": [
            {"name": "reserve_flag", "selector": "div.seldon-object-tile__badge", "type": "text"},
            {"name": "lot_number", "selector": "div.seldon-object-tile__lot-number", "type": "text"},
            {"name": "author", "selector": "div.seldon-object-tile__maker", "type": "text"},
            {"name": "title", "selector": "div.seldon-object-tile__title", "type": "text"},
            {"name": "link", "selector": "a.seldon-object-tile", "type": "attribute", "attribute": "href"},
            # {"name": "sale_price", "", "selector": "dd.seldon-detail__value", "type": "text"},
            # {"name": "sold_price", "selector": "dd.seldon-detail__value", "type": "text"},
        ]
    }

    @classmethod
    def parseXML(cls, xml_content):
        root = ET.fromstring(xml_content)
        # Define the namespace
        namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        # Find all <loc> elements using the namespace
        urls = root.findall(".//ns:loc", namespaces=namespace)

        return urls

    @classmethod
    async def crawl(cls, url):
        print("Crawling url: ", url)
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(
            url=url,
            config=CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                extraction_strategy=JsonCssExtractionStrategy(cls.ITEM_SCHEMA)
            )
        )
        data = json.loads(result.extracted_content)
        print(data)

    @classmethod
    async def run(cls):
        response = requests.get(cls.SITEMAP_URL)
        if response.status_code != 200:
            raise Exception("Failed to fetch sitemap")

        xml_urls = cls.parseXML(response.content)

        for xml_url in xml_urls:
            is_match = match_str(xml_url.text, cls.FILTER_URLS)
            if is_match:
                await cls.crawl(xml_url.text)   
                return              