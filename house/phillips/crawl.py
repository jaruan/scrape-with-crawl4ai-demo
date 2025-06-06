import requests
import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

from house.base import BaseCrawler
from house.phillips.schema import ITEM_SCHEMA, METADATA_SCHEMA


class PhillipsCrawler(BaseCrawler):
    def __init__(self) -> None:
        super().__init__(
            main_urls=[
                "https://www.phillips.com/auctions/past",
                "https://www.phillips.com/calendar",
            ],
            filter_link_by_keys=["/auction/"],
            house_name="phillips",
        )

    async def crawl_auction(
        self, crawler: AsyncWebCrawler, url: str
    ) -> tuple[list, list]:
        print(f"Crawling {self._house_name}'s url: ", url)
        html_content = requests.get(url).content
        items_result = await crawler.arun(
            url="raw:" + html_content.decode("utf-8"),
            config=CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                extraction_strategy=JsonCssExtractionStrategy(ITEM_SCHEMA),
            ),
        )

        items = json.loads(items_result.extracted_content)
        print("items: ", items)

        metadata_result = await crawler.arun(
            url="raw:" + html_content.decode("utf-8"),
            config=CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                extraction_strategy=JsonCssExtractionStrategy(METADATA_SCHEMA),
            ),
        )
        metadata = json.loads(metadata_result.extracted_content)
        print("metadata: ", metadata)

        return items, metadata
