import html
from bs4 import BeautifulSoup
from house.base import BaseCrawler
from crawl4ai import (
    AsyncWebCrawler,
    CrawlerRunConfig,
    CacheMode,
    JsonCssExtractionStrategy,
)
from house.sothebys.schema import ITEM_SCHEMA, METADATA_SCHEMA
import json


class SothebysCrawler(BaseCrawler):
    def __init__(self) -> None:
        super().__init__(
            main_urls=[
                "https://www.sothebys.com/en/calendar",
                "https://www.sothebys.com/en/results",
            ],
            filter_link_by_keys=["/auction/"],
            house_name="sothebys",
        )

    async def crawl_auction(self, crawler: AsyncWebCrawler, url) -> tuple[list, list]:
        print(f"Crawling {self._house_name}'s url: ", url)
        items = []
        metadata = []
        while True:
            items_result = await crawler.arun(
                url=url,
                config=CrawlerRunConfig(
                    cache_mode=CacheMode.BYPASS,
                    extraction_strategy=JsonCssExtractionStrategy(ITEM_SCHEMA),
                ),
            )
            if not items_result.success:
                raise Exception(items_result.error_message)

            items = json.loads(items_result.extracted_content)
            print("items: ", items)
            html_content = items_result.html
            with open("test.html", "w") as f:
                f.write(html_content)

            soup = BeautifulSoup(html_content, "html.parser")
            next_page_button = soup.find("button", {"aria-label": "Go to next page."})
            if not next_page_button:
                break
            elif "disabled" in next_page_button.attrs:
                break

        metadata_result = await crawler.arun(
            url="raw:" + html_content,
            config=CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                extraction_strategy=JsonCssExtractionStrategy(METADATA_SCHEMA),
            ),
        )
        metadata = json.loads(metadata_result.extracted_content)
        print("metadata: ", metadata)

        return items, metadata
