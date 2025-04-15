import requests
import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

from utils import match_str
from phillips.schema import ITEM_SCHEMA, METADATA_SCHEMA


class PhillipsCrawler:
    MAIN_URLS = [
        "https://www.phillips.com/auctions/past",
        "https://www.phillips.com/calendar",
    ]
    FILTER_URLS = ["/auction/"]

    @classmethod
    async def crawl_links(cls, crawler):
        links = []
        for url in cls.MAIN_URLS:
            result = await crawler.arun(
                url=url,
            )
            for link in result.links["internal"]:
                href = link.get("href", "")
                if match_str(href, cls.FILTER_URLS):
                    links.append(href)

        return links

    @classmethod
    async def crawl_auction(cls, crawler, url):
        print("Crawling url: ", url)
        html_content = requests.get(url).content
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
    def transform(cls, auction_id, items, metadata):
        pass

    @classmethod
    async def run(cls):
        async with AsyncWebCrawler() as crawler:
            links = await cls.crawl_links(crawler)
            for link in links:
                auction_id = link.split("/")[-1]
                items, metadata = await cls.crawl_auction(crawler, link)
                cls.transform(auction_id, items, metadata)
                return
