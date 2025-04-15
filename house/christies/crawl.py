from house.base_crawler import BaseCrawler
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode


class ChristiesCrawler(BaseCrawler):
    def __init__(self) -> None:
        super().__init__(
            main_urls=[
                "https://www.christies.com/en/calendar",
                "https://www.christies.com/en/results",
            ],
            filter_keys=["/auction/", "onlineonly."],
        )

    async def crawl_auction(self, crawler: AsyncWebCrawler, url: str):
        pass
