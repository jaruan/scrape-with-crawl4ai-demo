import json

from house.base import BaseCrawler
from crawl4ai import (
    AsyncWebCrawler,
    CrawlerRunConfig,
    CacheMode,
    JsonCssExtractionStrategy,
)

from house.christies.schema import ITEM_SCHEMA, METADATA_SCHEMA


class ChristiesCrawler(BaseCrawler):
    def __init__(self) -> None:
        super().__init__(
            main_urls=[
                "https://www.christies.com/en/calendar",
                "https://www.christies.com/en/results",
            ],
            filter_link_by_keys=["/auction/", "onlineonly."],
            house_name="christies",
        )

    async def crawl_auction(self, crawler: AsyncWebCrawler, url: str):
        print(f"Crawling {self._house_name}'s url: ", url)
        # For first step, make sure the load all items button is visible
        wait_for_items_js = """
            () => {
                const loadAllItemsButton = document.querySelector('button.chr-button--link-underline[aria-label=\"Load all remaining lots\"]');
                return loadAllItemsButton !== null
            }
        """

        # For second step, click the load all items button
        load_all_item_js = [
            "window.scrollTo(0, document.body.scrollHeight);",
            "document.querySelector('button.chr-button--link-underline[aria-label=\"Load all remaining lots\"]').click();",
        ]
        # Until the total items is equal to the loaded items
        wait_for_js = """
            () => {
                const totalItemsText = document.querySelector('a.chr-page-nav__link.chr-page-nav__link--active').text;
                const totalItems = parseInt(totalItemsText.match(/\((\d+)\)/)[1]);
                const loadedItems = document.querySelectorAll('li.chr-browse-lot-tile-wrapper').length;
                return loadedItems === totalItems;
            }
        """
        first_step_result = await crawler.arun(
            url=url,
            config=CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                wait_for=f"js:{wait_for_items_js}",
            ),
        )
        if not first_step_result.success:
            raise Exception(first_step_result.error_message)

        all_items_result = await crawler.arun(
            url=url,
            config=CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                extraction_strategy=JsonCssExtractionStrategy(ITEM_SCHEMA),
                js_code=load_all_item_js,
                wait_for=f"js:{wait_for_js}",
            ),
        )
        if not all_items_result.success:
            raise Exception(all_items_result.error_message)

        items = json.loads(all_items_result.extracted_content)
        # print("items: ", items)

        metadata_result = await crawler.arun(
            url="raw:" + all_items_result.html,
            config=CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                extraction_strategy=JsonCssExtractionStrategy(METADATA_SCHEMA),
            ),
        )
        metadata = json.loads(metadata_result.extracted_content)
        print("metadata: ", metadata)

        return items, metadata
