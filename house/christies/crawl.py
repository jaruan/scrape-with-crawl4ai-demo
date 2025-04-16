import json
from house.base import BaseCrawler
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode


class ChristiesCrawler(BaseCrawler):
    def __init__(self) -> None:
        super().__init__(
            main_urls=[
                "https://www.christies.com/en/calendar",
                "https://www.christies.com/en/results",
            ],
            filter_keys=["/auction/", "onlineonly."],
            house_name="christies",
        )

    async def crawl_auction(self, crawler: AsyncWebCrawler, url: str):
        print(f"Crawling {self._house_name}'s url: ", url)
        load_all_item_js = [
            # Get total number of items
            "const totalItems = parseInt(document.querySelector('a.chr-page-nav__link--active[data-title^=\"Browse lots\"]').getAttribute('data-title').match(/\\((\\d+)\\)/)[1]);",
            "window.scrollTo(0, document.body.scrollHeight);",
            "document.querySelector('button.chr-button--link-underline[aria-label=\"Load all remaining lots\"]').click();",
        ]
        json_css_extraction_strategy = []

        config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            js_code=load_all_item_js,
            wait_for="document.querySelectorAll('li.chr-browse-lot-tile-wrapper').length === totalItems",
            extraction_strategy=json_css_extraction_strategy,
        )

        await crawler.arun(
            url=url,
            config=config,
        )
