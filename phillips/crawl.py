import xml.etree.ElementTree as ET
import requests
import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

from utils import match_str
from phillips.model import ITEM_SCHEMA, METADATA_SCHEMA


class PhillipsCrawler:
    SITEMAP_URL = "https://www.phillips.com/sitemap.xml"
    FILTER_URLS = ["/auction/"]

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
        html_content = requests.get(url).content

        async with AsyncWebCrawler() as crawler:
            items_result = await crawler.arun(
                url="raw://" + html_content.decode("utf-8"),
                config=CrawlerRunConfig(
                    cache_mode=CacheMode.BYPASS,
                    extraction_strategy=JsonCssExtractionStrategy(ITEM_SCHEMA),
                ),
            )

            items = json.loads(items_result.extracted_content)
            print("items: ", items)

            metadata_result = await crawler.arun(
                url="raw://" + html_content.decode("utf-8"),
                config=CrawlerRunConfig(
                    cache_mode=CacheMode.BYPASS,
                    extraction_strategy=JsonCssExtractionStrategy(METADATA_SCHEMA),
                ),
            )
            metadata = json.loads(metadata_result.extracted_content)
            print("metadata: ", metadata)

            return items, metadata

    @classmethod
    def transform(cls, items, metadata):
        pass

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
